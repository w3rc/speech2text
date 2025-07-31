"""Modern Speech2Text application with dark theme and audio visualization."""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import tempfile
import os
import wave
from datetime import datetime
from typing import Optional

import pyperclip
from openai import OpenAI
from .settings import settings
from .modern_settings_dialog import ModernSettingsDialog
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
        self.settings_dialog: Optional[ModernSettingsDialog] = None
        self.audio_level_meter: Optional[AudioLevelMeter] = None
        self.status_indicator: Optional[StatusIndicator] = None
        self.activity_history: Optional[ActivityHistoryPanel] = None
        
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
        # Configure window with neon theme
        self.root.configure(bg=DarkTheme.COLORS['bg_primary'])
        
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
        
        # Right pane (activity history)
        right_pane = ttk.Frame(main_container, style='Dark.TFrame')
        right_pane.grid(row=0, column=1, sticky="nsew")
        right_pane.columnconfigure(0, weight=1)
        right_pane.rowconfigure(0, weight=1)
        
        # Header section
        self._create_header_section(left_pane)
        
        # Text display section (now row 1)
        self._create_text_section(left_pane)
        
        # Footer section
        self._create_footer_section(left_pane)
        
        # Activity history section
        self._create_activity_section(right_pane)
        
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
        
        # Help button  
        help_btn = ModernComponents.create_modern_button(
            status_frame, "❓", command=self._show_help_menu, style='Secondary.TButton'
        )
        help_btn.grid(row=0, column=1, padx=(0, 5))
        
        # Settings button
        settings_btn = ModernComponents.create_modern_button(
            status_frame, "⚙️", command=self._open_settings, style='Secondary.TButton'
        )
        settings_btn.grid(row=0, column=2)
        
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
    
    def _create_activity_section(self, parent: ttk.Frame) -> None:
        """Create the activity history section."""
        # Activity history card
        activity_card = ModernComponents.create_card_frame(parent)
        activity_card.grid(row=0, column=0, sticky="nsew")
        activity_card.columnconfigure(0, weight=1)
        activity_card.rowconfigure(0, weight=1)
        
        # Activity history panel
        self.activity_history = ActivityHistoryPanel(activity_card, width=300)  
        self.activity_history.grid(row=0, column=0, sticky="nsew")
        
        # Animate panel slide-in
        self.root.after(100, lambda: self._animate_panel_slide_in(self.activity_history))
    
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
    
    def _open_settings(self) -> None:
        """Open settings dialog."""
        if not self.settings_dialog:
            self.settings_dialog = ModernSettingsDialog(self.root, self._on_settings_changed)
        self.settings_dialog.show()
    
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