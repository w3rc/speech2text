"""Modern Speech2Text application with dark theme and audio visualization."""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import tempfile
import os
import wave
from datetime import datetime
from typing import Optional, Callable

import pyperclip
from openai import OpenAI
from .settings import settings

# Import for dark title bar
try:
    import pywinstyles
    PYWINSTYLES_AVAILABLE = True
except ImportError:
    PYWINSTYLES_AVAILABLE = False
from .theme import DarkTheme, ModernComponents, AudioLevelMeter, StatusIndicator, ActivityHistoryPanel
from .audio_monitor import AudioLevelMonitor
from .global_hotkey import GlobalHotkeyManager
from .animations import AnimationManager


class ModernSpeechToTextApp:
    """Modern Speech2Text application with dark theme and real-time audio visualization."""
    
    def __init__(self, root: tk.Tk) -> None:
        """Initialize the modern Speech2Text application."""
        self.root = root
        self.root.title("Speech2Text - Modern")
        self.root.geometry("1200x900")
        self.root.minsize(900, 700)
        
        # Apply dark theme
        DarkTheme.apply_theme(self.root)
        
        # Application state
        self.recording = False
        self.processing = False
        self.frames = []
        
        # Audio components
        self.audio_monitor: Optional[AudioLevelMonitor] = None
        self.recording_stream = None
        
        # Global hotkey manager
        self.hotkey_manager = GlobalHotkeyManager()
        
        # Animation manager
        self.animation_manager = AnimationManager(self.root)
        
        # OpenAI client
        self.client: Optional[OpenAI] = None
        self._update_api_client()
        
        # UI components
        self.audio_level_meter: Optional[AudioLevelMeter] = None
        self.status_indicator: Optional[StatusIndicator] = None
        self.activity_history: Optional[ActivityHistoryPanel] = None
        self.settings_panel: Optional['EmbeddedSettingsPanel'] = None
        
        # UI state
        self.settings_visible = False
        
        # Setup UI
        self._setup_ui()
        self._setup_audio_monitor()
        self._setup_keyboard_shortcuts()
        self._setup_global_hotkeys()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Start with idle status
        self._update_status("idle")
        
        # Start animation manager and initial animations
        self.animation_manager.start_animation_loop()
        self._animate_startup()
    
    def _update_api_client(self) -> None:
        """Update OpenAI client with current API key from settings."""
        api_key = settings.get_api_key()
        self.client = OpenAI(api_key=api_key) if api_key else None
    
    def _setup_ui(self) -> None:
        """Set up the modern user interface."""
        # Configure window with dark theme
        self.root.configure(bg=DarkTheme.COLORS['bg_primary'])
        
        # Apply dark title bar if available
        if PYWINSTYLES_AVAILABLE:
            try:
                pywinstyles.apply_style(self.root, "dark")
                print("[THEME] Applied dark title bar")
            except Exception as e:
                print(f"[WARNING] Could not apply dark title bar: {e}")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=0)  # Fixed height for audio indicator
        
        # Main container - seamless integration
        main_container = tk.Frame(self.root, bg=DarkTheme.COLORS['bg_primary'])
        main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=(20, 10))
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=0)  # Fixed width for activity panel
        main_container.rowconfigure(0, weight=1)
        
        # Left pane (main content)
        left_pane = ttk.Frame(main_container, style='Dark.TFrame')
        left_pane.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left_pane.columnconfigure(0, weight=1)
        left_pane.rowconfigure(1, weight=1)  # Text area gets most space
        
        # Right pane (activity history / settings) - Fixed width
        self.right_pane = ttk.Frame(main_container, style='Dark.TFrame')
        self.right_pane.grid(row=0, column=1, sticky="nsew")
        self.right_pane.configure(width=450)  # Fixed width for consistency
        self.right_pane.grid_propagate(False)  # Prevent resizing
        self.right_pane.columnconfigure(0, weight=1)
        self.right_pane.rowconfigure(0, weight=1)
        
        # Header section
        self._create_header_section(left_pane)
        
        # Text display section (now row 1)
        self._create_text_section(left_pane)
        
        # Footer section
        self._create_footer_section(left_pane)
        
        # Right pane content (activity history by default)
        self._create_right_pane_content()
        
        # Create settings panel (hidden initially)
        self._create_settings_panel()
        
        # Audio indicator at bottom center
        self._create_bottom_audio_indicator()
    
    def _create_header_section(self, parent: ttk.Frame) -> None:
        """Create the header section with title and status."""
        header_frame = ttk.Frame(parent, style='Dark.TFrame')
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.columnconfigure(1, weight=1)
        
        # App title
        title_label = ModernComponents.create_modern_label(
            header_frame, "Speech2Text", style='HeadingLarge.TLabel'
        )
        title_label.grid(row=0, column=0, sticky="w")
        
        # API Status
        status_frame = ttk.Frame(header_frame, style='Dark.TFrame')
        status_frame.grid(row=0, column=2, sticky="e")
        
        self.api_status_label = ModernComponents.create_modern_label(
            status_frame, "", style='Status.TLabel'
        )
        self.api_status_label.grid(row=0, column=0, padx=(0, 10))
        
        # Settings button
        self.settings_btn = ModernComponents.create_modern_button(
            status_frame, "⚙️", command=self._toggle_settings_panel, style='Secondary.TButton'
        )
        self.settings_btn.grid(row=0, column=1)
        
        self._update_api_status()
    
    def _create_bottom_audio_indicator(self) -> None:
        """Create the audio indicator at the bottom center of the window."""
        # Bottom audio container
        audio_container = tk.Frame(self.root, bg=DarkTheme.COLORS['bg_primary'])
        audio_container.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        audio_container.columnconfigure(0, weight=1)
        
        # Center the audio level meter
        self.audio_level_meter = AudioLevelMeter(audio_container, size=150)
        self.audio_level_meter.grid(row=0, column=0, pady=10)
        
        # Status indicator (smaller, positioned above audio meter)
        self.status_indicator = StatusIndicator(audio_container, size=16)
        self.status_indicator.grid(row=1, column=0, pady=(5, 0))
    
    def _create_text_section(self, parent: ttk.Frame) -> None:
        """Create the text display section."""
        # Text card
        text_card = ModernComponents.create_card_frame(parent)
        text_card.grid(row=1, column=0, sticky="nsew")
        text_card.columnconfigure(0, weight=1)
        text_card.rowconfigure(1, weight=1)
        
        # Card header - seamless
        header_frame = ttk.Frame(text_card, style='Card.TFrame')
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=(15, 10))
        
        header_label = ModernComponents.create_modern_label(
            header_frame, "Transcribed Text", style='Heading.TLabel'
        )
        header_label.grid(row=0, column=0, sticky="w", padx=20)
        
        # Text display - seamless integration
        text_frame = ttk.Frame(text_card, style='Card.TFrame')
        text_frame.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Create text widget - seamless with background
        self.text_display = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=DarkTheme.FONTS['body'],
            bg=DarkTheme.COLORS['bg_primary'],
            fg=DarkTheme.COLORS['text_primary'],
            insertbackground=DarkTheme.COLORS['text_primary'],
            selectbackground=DarkTheme.COLORS['bg_tertiary'],
            selectforeground=DarkTheme.COLORS['text_primary'],
            relief='flat',
            borderwidth=0,
            highlightthickness=0,
            padx=20,
            pady=15
        )
        self.text_display.grid(row=0, column=0, sticky="nsew")
        
        # Create seamless scrollbar that only shows when needed
        self.scrollbar = tk.Scrollbar(
            text_frame,
            orient="vertical",
            command=self.text_display.yview,
            bg=DarkTheme.COLORS['bg_primary'],
            troughcolor=DarkTheme.COLORS['bg_primary'],
            activebackground=DarkTheme.COLORS['bg_secondary'],
            highlightbackground=DarkTheme.COLORS['bg_primary'],
            highlightcolor=DarkTheme.COLORS['bg_primary'],
            borderwidth=0,
            highlightthickness=0,
            relief='flat',
            elementborderwidth=0,
            width=8
        )
        
        # Configure text widget to use scrollbar
        self.text_display.config(yscrollcommand=self.scrollbar.set)
        
        # Function to show/hide scrollbar based on content
        def on_text_change(*args):
            # Get the fraction of visible content
            top, bottom = self.scrollbar.get()
            
            # Show scrollbar only if not all content is visible
            if top != 0.0 or bottom != 1.0:
                self.scrollbar.grid(row=0, column=1, sticky="ns")
            else:
                self.scrollbar.grid_remove()
        
        # Bind text changes to scrollbar visibility
        self.text_display.bind('<Configure>', on_text_change)
        self.text_display.bind('<KeyRelease>', on_text_change)
        self.text_display.bind('<<Modified>>', on_text_change)
        
        # Update scrollbar command to trigger visibility check
        original_set = self.scrollbar.set
        def scrollbar_set(*args):
            original_set(*args)
            on_text_change()
        self.scrollbar.set = scrollbar_set
    
    def _create_footer_section(self, parent: ttk.Frame) -> None:
        """Create the footer section with additional info."""
        footer_frame = ttk.Frame(parent, style='Dark.TFrame')
        footer_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        footer_frame.columnconfigure(0, weight=1)
        
        # Stats or additional info can go here
        self.footer_label = ModernComponents.create_modern_label(
            footer_frame, "Modern Speech2Text v0.1.0", style='Muted.TLabel'
        )
        self.footer_label.grid(row=0, column=0, sticky="w")
    
    def _create_right_pane_content(self) -> None:
        """Create the right pane content (activity history by default)."""
        # Activity history card
        self.activity_card = ModernComponents.create_card_frame(self.right_pane)
        self.activity_card.grid(row=0, column=0, sticky="nsew")
        self.activity_card.columnconfigure(0, weight=1)
        self.activity_card.rowconfigure(0, weight=1)
        
        # Activity history panel
        self.activity_history = ActivityHistoryPanel(self.activity_card, width=300)  
        self.activity_history.grid(row=0, column=0, sticky="nsew")
        
        # Animate panel slide-in
        self.root.after(100, lambda: self._animate_panel_slide_in(self.activity_history, 'left'))
    
    def _create_settings_panel(self) -> None:
        """Create the embedded settings panel (hidden initially)."""
        # Settings panel will be created on first access
        pass
    
    def _setup_audio_monitor(self) -> None:
        """Set up real-time audio monitoring."""
        audio_settings = settings.get_audio_settings()
        
        self.audio_monitor = AudioLevelMonitor(
            sample_rate=audio_settings.get("sample_rate", 44100),
            chunk_size=audio_settings.get("chunk_size", 1024),
            channels=audio_settings.get("channels", 1),
            update_callback=self._on_audio_level_update
        )
        
        # Start monitoring
        if self.audio_monitor.start_monitoring():
            self.footer_label.config(text="Modern Speech2Text v0.1.0")
        else:
            self.footer_label.config(text="Audio monitoring failed • Modern Speech2Text v0.1.0")
    
    def _on_audio_level_update(self, level: float, voice_detected: bool) -> None:
        """Handle audio level updates from the monitor."""
        if self.audio_level_meter:
            self.audio_level_meter.update_level(level, voice_detected)
        
        # Update status based on voice detection during recording
        if self.recording and voice_detected:
            self._update_status("recording_active")
        elif self.recording:
            self._update_status("recording")
    
    def _setup_keyboard_shortcuts(self) -> None:
        """Set up keyboard shortcuts."""
        self.root.bind('<Control-n>', lambda e: self.toggle_recording())
        self.root.bind('<Control-s>', lambda e: self.save_text())
        self.root.bind('<Control-comma>', lambda e: self._open_settings())
        self.root.bind('<F1>', lambda e: self._show_about())
        self.root.bind('<Escape>', lambda e: self._stop_recording_if_active())
    
    def _stop_recording_if_active(self) -> None:
        """Stop recording if currently active (ESC key handler)."""
        if self.recording:
            self.toggle_recording()
    
    def _setup_global_hotkeys(self) -> None:
        """Set up global keyboard shortcuts."""
        try:
            # Register the toggle hotkey
            self.hotkey_manager.register_toggle_hotkey(self._global_toggle_recording)
            
            # Start the hotkey manager
            if self.hotkey_manager.start():
                pass  # Global hotkey enabled silently
            else:
                print("Failed to start global hotkey manager")
                
        except Exception as e:
            print(f"Failed to setup global hotkeys: {e}")
    
    def _global_toggle_recording(self) -> None:
        """Global hotkey handler for toggle recording."""
        # Schedule on main thread since we're called from hotkey thread
        self.root.after(0, self.toggle_recording)
    
    # Text change animation removed - no status text to animate
    
    def _animate_button_press(self, button: tk.Widget) -> None:
        """Animate button press with scale effect."""
        self.animation_manager.pulse(button, 0.05, 0.15)
    
    def _animate_panel_slide_in(self, panel: tk.Widget, direction: str = 'right') -> None:
        """Animate panel sliding in."""
        self.animation_manager.slide_in(panel, direction, 50, 0.4)
    
    def _animate_startup(self) -> None:
        """Animate application startup with smooth entrance effects."""
        # Animate main components with staggered timing
        components = [
            (400, self.text_display),
            (600, self.audio_level_meter if self.audio_level_meter else None),
        ]
        
        for delay, component in components:
            if component:
                self.root.after(delay, lambda c=component: self.animation_manager.fade_in(c, 0.5))
    
    # Button animation methods removed - no buttons to animate
    
    def _update_status(self, status: str) -> None:
        """Update the application status - visual indicator only, no text."""
        # Map status to visual state
        visual_status = "idle"
        if status == "recording" or status == "recording_active":
            visual_status = "recording"
        elif status == "processing":
            visual_status = "processing"
        elif status == "error":
            visual_status = "error"
        
        # Update both status indicator and audio level meter colors
        if self.status_indicator:
            self.status_indicator.set_status(visual_status)
        
        if self.audio_level_meter:
            self.audio_level_meter.set_status(visual_status)
    
    def _update_api_status(self) -> None:
        """Update the API status display."""
        if self.client:
            status_text = "✓ API Key configured"
            color = DarkTheme.COLORS['success']
        else:
            status_text = "⚠ No API key - Click Settings"
            color = DarkTheme.COLORS['warning']
        
        self.api_status_label.config(text=status_text, foreground=color)
    
    def toggle_recording(self) -> None:
        """Toggle recording state."""
        if self.processing:
            return  # Don't allow toggle while processing
            
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()
    
    def start_recording(self) -> None:
        """Start audio recording."""
        if not self.client:
            messagebox.showerror(
                "API Key Required",
                "Please configure your OpenAI API key in Settings before recording.",
                parent=self.root
            )
            return
        
        try:
            import pyaudio
            
            audio_settings = settings.get_audio_settings()
            
            # Initialize audio
            audio = pyaudio.PyAudio()
            self.recording_stream = audio.open(
                format=pyaudio.paInt16,
                channels=audio_settings.get("channels", 1),
                rate=audio_settings.get("sample_rate", 44100),
                input=True,
                frames_per_buffer=audio_settings.get("chunk_size", 1024)
            )
            
            self.recording = True
            self.frames = []
            
            # Update UI status
            self._update_status("recording")
            
            # Start recording in separate thread
            self.recording_thread = threading.Thread(target=self._record_audio, daemon=True)
            self.recording_thread.start()
            
            # Recording started (no activity log needed)
            
        except Exception as e:
            messagebox.showerror("Recording Error", f"Failed to start recording: {str(e)}")
            self._update_status("error")
    
    def _record_audio(self) -> None:
        """Record audio in separate thread."""
        try:
            while self.recording and self.recording_stream:
                data = self.recording_stream.read(1024, exception_on_overflow=False)
                self.frames.append(data)
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Recording Error", str(e)))
    
    def stop_recording(self) -> None:
        """Stop recording and process audio."""
        if not self.recording:
            return
            
        self.recording = False
        self.processing = True
        
        # Update UI status
        self._update_status("processing")
        
        # Stop recording stream
        if self.recording_stream:
            self.recording_stream.stop_stream()
            self.recording_stream.close()
            self.recording_stream = None
        
        # Process in separate thread
        processing_thread = threading.Thread(target=self._process_audio, daemon=True)
        processing_thread.start()
        
        # Recording stopped (no activity log needed)
    
    def _process_audio(self) -> None:
        """Process recorded audio and transcribe."""
        try:
            if not self.frames:
                self.root.after(0, lambda: self._reset_ui("No audio recorded"))
                return
            
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_filename = temp_file.name
            
            # Write audio data
            import pyaudio
            audio = pyaudio.PyAudio()
            
            with wave.open(temp_filename, 'wb') as wf:
                audio_settings = settings.get_audio_settings()
                wf.setnchannels(audio_settings.get("channels", 1))
                wf.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
                wf.setframerate(audio_settings.get("sample_rate", 44100))
                wf.writeframes(b''.join(self.frames))
            
            audio.terminate()
            
            # Transcribe using OpenAI Whisper
            transcription_settings = settings.get_transcription_settings()
            
            with open(temp_filename, 'rb') as audio_file:
                transcript_params = {
                    "model": transcription_settings.get("model", "whisper-1"),
                    "file": audio_file,
                    "language": transcription_settings.get("language", "en"),
                    "temperature": transcription_settings.get("temperature", 0.0)
                }
                
                # Add prompt if specified
                prompt = transcription_settings.get("prompt", "").strip()
                if prompt:
                    transcript_params["prompt"] = prompt
                
                transcript = self.client.audio.transcriptions.create(**transcript_params)
            
            # Update UI with results
            self.root.after(0, lambda: self._display_transcription(transcript.text))
            
            # Auto-save if enabled
            output_settings = settings.get_output_settings()
            if output_settings.get("auto_save", False):
                self._auto_save_transcript(transcript.text)
            
            # Clean up
            os.unlink(temp_filename)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Transcription Error", str(e)))
            self.root.after(0, lambda: self._reset_ui("Transcription failed"))
        finally:
            self.processing = False
    
    def _display_transcription(self, text: str) -> None:
        """Display transcribed text with animation."""
        # Animate text appearance
        def add_text():
            self.text_display.insert(tk.END, text + "\n\n")
            self.text_display.see(tk.END)
            self._reset_ui("Transcription complete")
            
            # Animate the text area to highlight new content
            self.animation_manager.pulse(self.text_display, 0.02, 0.3)
        
        # Auto-copy transcribed text to clipboard
        try:
            pyperclip.copy(text)
        except Exception as e:
            print(f"Failed to copy to clipboard: {e}")
        
        # Log activity
        if self.activity_history:
            self.activity_history.add_activity(text)
            
        # Slight delay for animation effect
        self.root.after(100, add_text)
    
    def _reset_ui(self, message: str = "") -> None:
        """Reset UI to ready state."""
        self._update_status("idle")
        self.footer_label.config(text="Modern Speech2Text v0.1.0")
    
    def _auto_save_transcript(self, text: str) -> None:
        """Auto-save transcript to file."""
        try:
            output_settings = settings.get_output_settings()
            save_dir = output_settings.get("save_directory", str(os.path.expanduser("~/Documents")))
            file_format = output_settings.get("file_format", "txt")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(save_dir, f"transcript_{timestamp}.{file_format}")
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
                
        except Exception:
            pass  # Silently fail auto-save
    
    def clear_text(self) -> None:
        """Clear the text display."""
        self.text_display.delete(1.0, tk.END)
        self.footer_label.config(text="Text cleared • Modern Speech2Text v0.1.0")
    
    def save_text(self) -> None:
        """Save text to file."""
        text_content = self.text_display.get(1.0, tk.END).strip()
        if not text_content:
            messagebox.showwarning("Nothing to Save", "No text to save!", parent=self.root)
            return
        
        output_settings = settings.get_output_settings()
        if output_settings.get("auto_save", False):
            self._auto_save_transcript(text_content)
            messagebox.showinfo("Saved", "Text saved to default location", parent=self.root)
        else:
            self._save_text_as()
    
    def _save_text_as(self) -> None:
        """Save text with file dialog."""
        text_content = self.text_display.get(1.0, tk.END).strip()
        if not text_content:
            messagebox.showwarning("Nothing to Save", "No text to save!", parent=self.root)
            return
        
        output_settings = settings.get_output_settings()
        initial_dir = output_settings.get("save_directory", os.path.expanduser("~/Documents"))
        file_format = output_settings.get("file_format", "txt")
        
        filename = filedialog.asksaveasfilename(
            title="Save Transcription",
            initialdir=initial_dir,
            defaultextension=f".{file_format}",
            filetypes=[
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("Rich Text Format", "*.rtf"),
                ("All files", "*.*")
            ],
            parent=self.root
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                messagebox.showinfo("Saved", f"Text saved to: {filename}", parent=self.root)
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save: {str(e)}", parent=self.root)
    
    def _show_help_menu(self) -> None:
        """Show help menu with options."""
        import tkinter.messagebox as msgbox
        
        # Create a simple context menu
        help_menu = tk.Menu(self.root, tearoff=0,
                           bg=DarkTheme.COLORS['bg_secondary'],
                           fg=DarkTheme.COLORS['text_primary'],
                           activebackground=DarkTheme.COLORS['accent_primary'],
                           activeforeground=DarkTheme.COLORS['text_primary'])
        
        help_menu.add_command(label="Keyboard Shortcuts", command=self._show_shortcuts)
        help_menu.add_command(label="About", command=self._show_about)
        
        # Show menu at cursor position
        try:
            help_menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            help_menu.grab_release()
    
    def _toggle_settings_panel(self) -> None:
        """Toggle between activity history and settings panel."""
        if self.settings_visible:
            # Hide settings, show activity history
            self._hide_settings_panel()
        else:
            # Hide activity history, show settings
            self._show_settings_panel()
    
    def _show_settings_panel(self) -> None:
        """Show the settings panel and hide activity history."""
        # Create settings panel if it doesn't exist
        if not self.settings_panel:
            self.settings_panel = EmbeddedSettingsPanel(self.right_pane, self._on_settings_changed)
        
        # Hide activity history with slide-out animation
        self._animate_panel_slide_out(self.activity_card, 'left', callback=self._complete_settings_show)
        
        # Update state
        self.settings_visible = True
        
        # Update button appearance
        self._update_settings_button_state()
    
    def _hide_settings_panel(self) -> None:
        """Hide the settings panel and show activity history."""
        # Hide settings panel with slide-out animation
        if self.settings_panel:
            self._animate_panel_slide_out(self.settings_panel, 'right', callback=self._complete_settings_hide)
        
        # Update state
        self.settings_visible = False
        
        # Update button appearance
        self._update_settings_button_state()
    
    def _complete_settings_show(self) -> None:
        """Complete the settings panel show animation."""
        # Hide activity history completely
        self.activity_card.grid_remove()
        
        # Show settings panel
        self.settings_panel.grid(row=0, column=0, sticky="nsew")
        
        # Animate slide-in from right
        self.root.after(10, lambda: self._animate_panel_slide_in(self.settings_panel, 'right'))
    
    def _complete_settings_hide(self) -> None:
        """Complete the settings panel hide animation."""
        # Hide settings panel completely
        if self.settings_panel:
            self.settings_panel.grid_remove()
        
        # Show activity history
        self.activity_card.grid(row=0, column=0, sticky="nsew")
        
        # Animate slide-in from left
        self.root.after(10, lambda: self._animate_panel_slide_in(self.activity_card, 'left'))
    
    def _animate_panel_slide_out(self, panel: tk.Widget, direction: str, callback=None) -> None:
        """Animate panel sliding out."""
        # Simple fade effect for now - can be enhanced with actual sliding
        original_alpha = 1.0
        steps = 10
        
        def fade_step(step: int):
            if step >= steps:
                if callback:
                    callback()
                return
            
            alpha = original_alpha * (1.0 - step / steps)
            # Simple opacity simulation by changing colors gradually
            self.root.after(20, lambda: fade_step(step + 1))
        
        fade_step(0)
    
    def _animate_panel_slide_in(self, panel: tk.Widget, direction: str) -> None:
        """Animate panel sliding in."""
        # Simple fade-in effect for now - can be enhanced with actual sliding
        steps = 10
        
        def fade_step(step: int):
            if step >= steps:
                return
            
            alpha = step / steps
            # Simple opacity simulation 
            self.root.after(20, lambda: fade_step(step + 1))
        
        fade_step(0)
    
    def _update_settings_button_state(self) -> None:
        """Update the settings button appearance based on current state."""
        if self.settings_visible:
            # Active state - show as pressed/active
            self.settings_btn.configure(style='Modern.TButton')
            # Change icon to indicate "close settings" 
            self.settings_btn.configure(text="✕")
        else:
            # Inactive state - show as normal
            self.settings_btn.configure(style='Secondary.TButton')
            # Show settings icon
            self.settings_btn.configure(text="⚙️")
    
    def _on_settings_changed(self) -> None:
        """Handle settings changes."""
        self._update_api_client()
        self._update_api_status()
        
        # Update audio monitor settings
        if self.audio_monitor:
            self.audio_monitor.stop_monitoring()
            self._setup_audio_monitor()
    
    def _show_about(self) -> None:
        """Show about dialog."""
        about_text = (
            "Speech2Text Modern v0.1.0\n\n"
            "A modern desktop application for real-time\n"
            "speech-to-text transcription using OpenAI Whisper API.\n\n"
            "Features:\n"
            "• Dark theme interface\n"
            "• Real-time audio level visualization\n"
            "• Voice activity detection\n"
            "• Secure encrypted settings\n\n"
            "Built with Python and tkinter\n"
            "Licensed under MIT License\n\n"
            "© 2025 Speech2Text Contributors"
        )
        messagebox.showinfo("About Speech2Text", about_text, parent=self.root)
    
    def _show_shortcuts(self) -> None:
        """Show keyboard shortcuts."""
        shortcuts_text = (
            "Keyboard Shortcuts - No Buttons Needed!\n\n"
            "Recording Controls:\n"
            "Ctrl+N - Start/Stop Recording\n"
            "Esc - Stop Recording (if active)\n"
            "Ctrl+Win - Toggle Recording (global)\n\n"
            "Text Management:\n"
            "Ctrl+S - Save Text\n"
            "Text is automatically copied to clipboard\n\n"
            "Application:\n"
            "Ctrl+, - Open Settings\n"
            "F1 - Show About Dialog\n\n"
            "Pro Tip: All functionality is available via shortcuts!"
        )
        messagebox.showinfo("Keyboard Shortcuts", shortcuts_text, parent=self.root)
    
    def on_closing(self) -> None:
        """Handle application closing."""
        # Stop recording if active
        if self.recording:
            self.recording = False
            
        if self.recording_stream:
            self.recording_stream.stop_stream()
            self.recording_stream.close()
        
        # Stop audio monitoring
        if self.audio_monitor:
            self.audio_monitor.stop_monitoring()
        
        # Stop global hotkeys
        if self.hotkey_manager:
            self.hotkey_manager.stop()
        
        # Stop animations
        if self.animation_manager:
            self.animation_manager.stop_animation_loop()
        
        # Save window geometry
        geometry = self.root.geometry()
        settings.set("ui.window_geometry", geometry)
        settings.save_settings()
        
        self.root.destroy()


class EmbeddedSettingsPanel(tk.Frame):
    """Embedded settings panel that matches the main app's theme and layout."""
    
    def __init__(self, parent: tk.Widget, on_settings_changed: Optional[Callable] = None):
        super().__init__(parent, bg=DarkTheme.COLORS['bg_primary'])
        self.on_settings_changed = on_settings_changed
        
        # Set fixed dimensions to prevent resizing
        self.configure(width=450, height=600)
        self.grid_propagate(False)
        
        # Configure grid
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)  # Content area expands
        
        # Current tab
        self.current_tab = "api"
        
        # Create UI
        self._create_header()
        self._create_content_area()
        self._create_action_buttons()
        
        # Load settings
        self._load_current_settings()
        
        # Switch to first tab
        self._switch_tab("api")
    
    def _create_header(self) -> None:
        """Create the settings panel header."""
        header_frame = tk.Frame(self, bg=DarkTheme.COLORS['bg_primary'])
        header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 15))
        header_frame.columnconfigure(0, weight=1)
        
        # Title (centered)
        title_label = tk.Label(header_frame,
                              text="Settings",
                              bg=DarkTheme.COLORS['bg_primary'],
                              fg=DarkTheme.COLORS['text_primary'],
                              font=DarkTheme.FONTS['heading_large'])
        title_label.grid(row=0, column=0, sticky="w")
        
        # Settings icon (inactive state)
        settings_icon = tk.Label(header_frame,
                                text="⚙️",
                                bg=DarkTheme.COLORS['bg_primary'],
                                fg=DarkTheme.COLORS['text_muted'],
                                font=DarkTheme.FONTS['heading'])
        settings_icon.grid(row=0, column=1, sticky="e")
    
    def _create_content_area(self) -> None:
        """Create the main content area with navigation and settings."""
        content_frame = tk.Frame(self, bg=DarkTheme.COLORS['bg_primary'])
        content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=0)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Navigation tabs (vertical list)
        self._create_navigation(content_frame)
        
        # Settings content area
        self._create_settings_content(content_frame)
    
    def _create_navigation(self, parent: tk.Frame) -> None:
        """Create the navigation tab list."""
        nav_frame = tk.Frame(parent, bg=DarkTheme.COLORS['bg_secondary'], width=140)
        nav_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 15))
        nav_frame.grid_propagate(False)
        
        # Tab definitions
        self.tabs = [
            ("api", "🔑", "API"),
            ("audio", "🎤", "Audio"),
            ("output", "💾", "Files"),
            ("interface", "🎨", "Theme")
        ]
        
        self.tab_buttons = {}
        
        # Create tab buttons
        for i, (tab_id, icon, title) in enumerate(self.tabs):
            btn_frame = tk.Frame(nav_frame, bg=DarkTheme.COLORS['bg_secondary'])
            btn_frame.pack(fill='x', padx=8, pady=2)
            
            # Tab button
            tab_btn = tk.Frame(btn_frame,
                              bg=DarkTheme.COLORS['bg_secondary'],
                              relief='flat',
                              bd=0,
                              height=40)
            tab_btn.pack(fill='x', pady=2)
            
            # Icon and text
            content_frame = tk.Frame(tab_btn, bg=DarkTheme.COLORS['bg_secondary'])
            content_frame.pack(expand=True, fill='both')
            
            # Icon
            icon_label = tk.Label(content_frame,
                                 text=icon,
                                 bg=DarkTheme.COLORS['bg_secondary'],
                                 fg=DarkTheme.COLORS['text_secondary'],
                                 font=('Segoe UI', 12))
            icon_label.pack(side='left', padx=(8, 6), pady=8)
            
            # Title
            title_label = tk.Label(content_frame,
                                  text=title,
                                  bg=DarkTheme.COLORS['bg_secondary'],
                                  fg=DarkTheme.COLORS['text_primary'],
                                  font=DarkTheme.FONTS['body_bold'],
                                  anchor='w')
            title_label.pack(side='left', fill='x', expand=True, pady=8)
            
            # Store references
            self.tab_buttons[tab_id] = {
                'frame': tab_btn,
                'content': content_frame,
                'icon': icon_label,
                'title': title_label
            }
            
            # Bind events
            for widget in [tab_btn, content_frame, icon_label, title_label]:
                widget.bind("<Button-1>", lambda e, tid=tab_id: self._switch_tab(tid))
                widget.bind("<Enter>", lambda e, tid=tab_id: self._on_tab_hover(tid, True))
                widget.bind("<Leave>", lambda e, tid=tab_id: self._on_tab_hover(tid, False))
    
    def _create_settings_content(self, parent: tk.Frame) -> None:
        """Create the settings content area without scrollbar."""
        # Content container
        content_container = tk.Frame(parent, bg=DarkTheme.COLORS['bg_primary'])
        content_container.grid(row=0, column=1, sticky="nsew")
        content_container.columnconfigure(0, weight=1)
        content_container.rowconfigure(0, weight=1)
        
        # Create content frames for each tab with fixed width
        self.content_frames = {}
        for tab_id, _, _ in self.tabs:
            frame = tk.Frame(content_container, bg=DarkTheme.COLORS['bg_primary'])
            frame.configure(width=280)  # Fixed content width
            self.content_frames[tab_id] = frame
        
        # Create content for each tab
        self._create_all_tab_content()
    
    def _create_action_buttons(self) -> None:
        """Create the action buttons at the bottom."""
        button_frame = tk.Frame(self, bg=DarkTheme.COLORS['bg_primary'])
        button_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=(10, 20))
        
        # Button container
        button_container = tk.Frame(button_frame, bg=DarkTheme.COLORS['bg_primary'])
        button_container.pack(anchor='center')
        
        # Apply button
        apply_btn = tk.Button(button_container,
                             text="Apply",
                             bg=DarkTheme.COLORS['bg_hover'],
                             fg=DarkTheme.COLORS['text_primary'],
                             activebackground=DarkTheme.COLORS['bg_active'],
                             activeforeground=DarkTheme.COLORS['text_primary'],
                             font=DarkTheme.FONTS['body'],
                             relief='flat',
                             borderwidth=0,
                             padx=12,
                             pady=6,
                             command=self._apply_settings)
        apply_btn.pack(side='left', padx=(0, 8))
        
        # Reset button
        reset_btn = tk.Button(button_container,
                             text="Reset",
                             bg=DarkTheme.COLORS['bg_tertiary'],
                             fg=DarkTheme.COLORS['text_primary'],
                             activebackground=DarkTheme.COLORS['bg_hover'],
                             activeforeground=DarkTheme.COLORS['text_primary'],
                             font=DarkTheme.FONTS['body'],
                             relief='flat',
                             borderwidth=0,
                             padx=12,
                             pady=6,
                             command=self._reset_settings)
        reset_btn.pack(side='left')
    
    def _switch_tab(self, tab_id: str) -> None:
        """Switch to the specified tab without flickering."""
        # Hide all content frames by removing them from grid
        for frame in self.content_frames.values():
            frame.grid_remove()
        
        # Show selected content frame using grid (no flickering)
        if tab_id in self.content_frames:
            self.content_frames[tab_id].grid(row=0, column=0, sticky='nsew', padx=15, pady=15)
        
        # Update tab button styles efficiently
        for tid, elements in self.tab_buttons.items():
            if tid == tab_id:
                # Active tab styling - update only if not already active
                if elements['frame']['bg'] != DarkTheme.COLORS['bg_tertiary']:
                    elements['frame'].config(bg=DarkTheme.COLORS['bg_tertiary'])
                    elements['content'].config(bg=DarkTheme.COLORS['bg_tertiary'])
                    elements['icon'].config(bg=DarkTheme.COLORS['bg_tertiary'], 
                                          fg=DarkTheme.COLORS['text_primary'])
                    elements['title'].config(bg=DarkTheme.COLORS['bg_tertiary'],
                                           fg=DarkTheme.COLORS['text_primary'])
            else:
                # Inactive tab styling - update only if not already inactive
                if elements['frame']['bg'] != DarkTheme.COLORS['bg_secondary']:
                    elements['frame'].config(bg=DarkTheme.COLORS['bg_secondary'])
                    elements['content'].config(bg=DarkTheme.COLORS['bg_secondary'])
                    elements['icon'].config(bg=DarkTheme.COLORS['bg_secondary'],
                                          fg=DarkTheme.COLORS['text_secondary'])
                    elements['title'].config(bg=DarkTheme.COLORS['bg_secondary'],
                                           fg=DarkTheme.COLORS['text_primary'])
        
        self.current_tab = tab_id
    
    def _on_tab_hover(self, tab_id: str, enter: bool) -> None:
        """Handle tab hover effects efficiently."""
        if tab_id == self.current_tab or not hasattr(self, 'current_tab'):
            return
        
        elements = self.tab_buttons[tab_id]
        target_bg = DarkTheme.COLORS['bg_hover'] if enter else DarkTheme.COLORS['bg_secondary']
        target_fg = DarkTheme.COLORS['text_primary'] if enter else DarkTheme.COLORS['text_secondary']
        target_title_fg = DarkTheme.COLORS['text_primary']
        
        # Only update if the color actually changed
        if elements['frame']['bg'] != target_bg:
            elements['frame'].config(bg=target_bg)
            elements['content'].config(bg=target_bg)
            elements['icon'].config(bg=target_bg, fg=target_fg)
            elements['title'].config(bg=target_bg, fg=target_title_fg)
    
    def _create_all_tab_content(self) -> None:
        """Create content for all tabs."""
        self._create_api_tab_content()
        self._create_audio_tab_content()
        self._create_output_tab_content()
        self._create_interface_tab_content()
    
    def _create_api_tab_content(self) -> None:
        """Create API settings content."""
        frame = self.content_frames['api']
        
        # API Key section
        self._create_section(frame, "OpenAI API Key", "Configure your API key for transcription")
        
        # API Key input
        key_frame = tk.Frame(frame, bg=DarkTheme.COLORS['bg_secondary'])
        key_frame.pack(fill='x', pady=(0, 20))
        
        key_label = tk.Label(key_frame,
                            text="API Key:",
                            bg=DarkTheme.COLORS['bg_secondary'],
                            fg=DarkTheme.COLORS['text_primary'],
                            font=DarkTheme.FONTS['body_bold'])
        key_label.pack(anchor='w', padx=15, pady=(15, 5))
        
        self.api_key_var = tk.StringVar()
        key_entry = tk.Entry(key_frame,
                            textvariable=self.api_key_var,
                            bg=DarkTheme.COLORS['bg_tertiary'],
                            fg=DarkTheme.COLORS['text_primary'],
                            insertbackground=DarkTheme.COLORS['text_primary'],
                            relief='flat',
                            bd=5,
                            font=DarkTheme.FONTS['code'],
                            show="*",
                            width=40)
        key_entry.pack(fill='x', padx=15, pady=(0, 15))
    
    def _create_audio_tab_content(self) -> None:
        """Create audio settings content."""
        frame = self.content_frames['audio']
        
        # Audio quality section
        self._create_section(frame, "Audio Quality", "Configure recording parameters")
        
        audio_frame = tk.Frame(frame, bg=DarkTheme.COLORS['bg_secondary'])
        audio_frame.pack(fill='x', pady=(0, 20))
        
        # Sample rate
        rate_label = tk.Label(audio_frame,
                             text="Sample Rate:",
                             bg=DarkTheme.COLORS['bg_secondary'],
                             fg=DarkTheme.COLORS['text_primary'],
                             font=DarkTheme.FONTS['body_bold'])
        rate_label.pack(anchor='w', padx=15, pady=(15, 5))
        
        self.sample_rate_var = tk.StringVar()
        rate_combo = ttk.Combobox(
            audio_frame,
            textvariable=self.sample_rate_var,
            values=["44100 Hz (CD quality)", "22050 Hz", "16000 Hz (Good for speech)"],
            state='readonly',
            width=30,
            style='Modern.TCombobox'
        )
        rate_combo.pack(anchor='w', padx=15, pady=(0, 15))
    
    def _create_output_tab_content(self) -> None:
        """Create output settings content."""
        frame = self.content_frames['output']
        
        # File output section
        self._create_section(frame, "File Output", "Configure automatic saving")
        
        output_frame = tk.Frame(frame, bg=DarkTheme.COLORS['bg_secondary'])
        output_frame.pack(fill='x', pady=(0, 20))
        
        # Auto-save checkbox
        self.auto_save_var = tk.BooleanVar()
        auto_save_check = tk.Checkbutton(output_frame,
                                        text="Automatically save transcriptions",
                                        variable=self.auto_save_var,
                                        bg=DarkTheme.COLORS['bg_secondary'],
                                        fg=DarkTheme.COLORS['text_primary'],
                                        selectcolor=DarkTheme.COLORS['bg_tertiary'],
                                        activebackground=DarkTheme.COLORS['bg_secondary'],
                                        activeforeground=DarkTheme.COLORS['text_primary'],
                                        relief='flat',
                                        bd=0,
                                        font=DarkTheme.FONTS['body'])
        auto_save_check.pack(anchor='w', padx=15, pady=15)
    
    def _create_interface_tab_content(self) -> None:
        """Create interface settings content."""
        frame = self.content_frames['interface']
        
        # Theme section
        self._create_section(frame, "Appearance", "Customize the interface")
        
        theme_frame = tk.Frame(frame, bg=DarkTheme.COLORS['bg_secondary'])
        theme_frame.pack(fill='x', pady=(0, 20))
        
        theme_label = tk.Label(theme_frame,
                              text="Theme:",
                              bg=DarkTheme.COLORS['bg_secondary'],
                              fg=DarkTheme.COLORS['text_primary'],
                              font=DarkTheme.FONTS['body_bold'])
        theme_label.pack(anchor='w', padx=15, pady=(15, 5))
        
        self.theme_var = tk.StringVar()
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=["Dark (Current)", "Light (Coming Soon)"],
            state='readonly',
            width=30,
            style='Modern.TCombobox'
        )
        theme_combo.pack(anchor='w', padx=15, pady=(0, 15))
    
    def _create_section(self, parent: tk.Frame, title: str, subtitle: str) -> None:
        """Create a section with title and subtitle."""
        section_frame = tk.Frame(parent, bg=DarkTheme.COLORS['bg_secondary'])
        section_frame.pack(fill='x', pady=(0, 15))
        
        title_label = tk.Label(section_frame,
                              text=title,
                              bg=DarkTheme.COLORS['bg_secondary'],
                              fg=DarkTheme.COLORS['text_primary'],
                              font=DarkTheme.FONTS['heading'])
        title_label.pack(anchor='w', padx=15, pady=(15, 2))
        
        subtitle_label = tk.Label(section_frame,
                                 text=subtitle,
                                 bg=DarkTheme.COLORS['bg_secondary'],
                                 fg=DarkTheme.COLORS['text_muted'],
                                 font=DarkTheme.FONTS['caption'])
        subtitle_label.pack(anchor='w', padx=15, pady=(0, 15))
    
    def _load_current_settings(self) -> None:
        """Load current settings into the controls."""
        # Load API key
        if hasattr(self, 'api_key_var'):
            self.api_key_var.set(settings.get_api_key() or "")
        
        # Load other settings as they're created
        pass
    
    def _apply_settings(self) -> None:
        """Apply the current settings."""
        try:
            # Save API key
            if hasattr(self, 'api_key_var'):
                api_key = self.api_key_var.get().strip()
                if api_key:
                    settings.set_api_key(api_key)
            
            # Save settings
            settings.save_settings()
            
            # Notify parent
            if self.on_settings_changed:
                self.on_settings_changed()
                
            # Show feedback
            messagebox.showinfo("Settings Applied", "Settings have been applied successfully!")
            
        except Exception as e:
            messagebox.showerror("Settings Error", f"Failed to apply settings: {str(e)}")
    
    def _reset_settings(self) -> None:
        """Reset settings to defaults."""
        if messagebox.askyesno("Reset Settings", "Reset all settings to defaults?"):
            settings.reset_to_defaults()
            self._load_current_settings()
            messagebox.showinfo("Settings Reset", "Settings have been reset to defaults.")