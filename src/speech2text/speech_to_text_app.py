"""Speech2Text - Desktop speech-to-text application using OpenAI Whisper API."""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import pyaudio
import wave
import threading
import tempfile
import os
from datetime import datetime
from typing import Optional
from openai import OpenAI
from .settings import settings
from .settings_dialog import SettingsDialog


class SpeechToTextApp:
    """Main application class for Speech2Text."""
    
    def __init__(self, root: tk.Tk) -> None:
        """Initialize the Speech2Text application.
        
        Args:
            root: The main tkinter window
        """
        self.root = root
        self.root.title("Speech2Text - OpenAI Whisper")
        
        # Load UI settings
        ui_settings = settings.get_ui_settings()
        self.root.geometry(ui_settings.get("window_geometry", "600x500"))
        
        # Audio recording parameters from settings
        audio_settings = settings.get_audio_settings()
        self.chunk = audio_settings.get("chunk_size", 1024)
        self.format = pyaudio.paInt16
        self.channels = audio_settings.get("channels", 1)
        self.rate = audio_settings.get("sample_rate", 44100)
        self.recording = False
        self.frames = []
        self.audio = pyaudio.PyAudio()
        self.stream: Optional[pyaudio.Stream] = None
        
        # OpenAI client - initialize with API key from settings
        self.client: Optional[OpenAI] = None
        self._update_api_client()
        
        # Settings dialog
        self.settings_dialog: Optional[SettingsDialog] = None
        
        self._setup_ui()
        self._setup_keyboard_shortcuts()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def _update_api_client(self) -> None:
        """Update OpenAI client with current API key from settings."""
        api_key = settings.get_api_key()
        self.client = OpenAI(api_key=api_key) if api_key else None
        
    def _setup_ui(self) -> None:
        """Set up the user interface."""
        # Create menu bar
        self._create_menu_bar()
        
        self._setup_main_ui()
        
    def _create_menu_bar(self) -> None:
        """Create the application menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Recording", command=self.toggle_recording, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Save Text", command=self.save_text, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As...", command=self._save_text_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Preferences...", command=self._open_settings, accelerator="Ctrl+,")
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about, accelerator="F1")
        help_menu.add_command(label="Keyboard Shortcuts", command=self._show_shortcuts)
        
    def _setup_keyboard_shortcuts(self) -> None:
        """Set up keyboard shortcuts."""
        self.root.bind('<Control-n>', lambda e: self.toggle_recording())
        self.root.bind('<Control-s>', lambda e: self.save_text())
        self.root.bind('<Control-comma>', lambda e: self._open_settings())
        self.root.bind('<F1>', lambda e: self._show_about())
        
    def _setup_main_ui(self) -> None:
        """Set up the main user interface components."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # API Key status section
        api_frame = ttk.LabelFrame(main_frame, text="OpenAI API Status", padding="5")
        api_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.api_status_label = ttk.Label(api_frame, text="")
        self.api_status_label.grid(row=0, column=0, sticky=tk.W)
        
        # Settings button
        ttk.Button(api_frame, text="Settings", command=self._open_settings).grid(row=0, column=1, sticky=tk.E)
        
        # Update API status
        self._update_api_status()
        
        # Recording section
        record_frame = ttk.LabelFrame(main_frame, text="Audio Recording", padding="5")
        record_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.record_button = ttk.Button(record_frame, text="Start Recording", command=self.toggle_recording)
        self.record_button.grid(row=0, column=0, padx=(0, 10))
        
        self.status_label = ttk.Label(record_frame, text="Ready to record")
        self.status_label.grid(row=0, column=1)
        
        # Text display section
        text_frame = ttk.LabelFrame(main_frame, text="Transcribed Text", padding="5")
        text_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        self.text_display = scrolledtext.ScrolledText(text_frame, height=15, width=70)
        self.text_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        ttk.Button(button_frame, text="Clear Text", command=self.clear_text).grid(row=0, column=0)
        ttk.Button(button_frame, text="Save Text", command=self.save_text).grid(row=0, column=1, padx=(10, 0))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        api_frame.columnconfigure(0, weight=1)
        
    def _update_api_status(self) -> None:
        """Update the API status display."""
        if self.client:
            status_text = "✓ API Key configured"
            status_color = "green"
        else:
            status_text = "✗ No API key configured - Click Settings"
            status_color = "red"
            
        self.api_status_label.config(text=status_text, foreground=status_color)
        
    def _open_settings(self) -> None:
        """Open the settings dialog."""
        if not self.settings_dialog:
            self.settings_dialog = SettingsDialog(self.root, self._on_settings_changed)
        self.settings_dialog.show()
        
    def _on_settings_changed(self) -> None:
        """Handle settings changes."""
        # Update API client
        self._update_api_client()
        self._update_api_status()
        
        # Update audio settings
        audio_settings = settings.get_audio_settings()
        self.chunk = audio_settings.get("chunk_size", 1024)
        self.channels = audio_settings.get("channels", 1)
        self.rate = audio_settings.get("sample_rate", 44100)
        
        # Update UI settings
        ui_settings = settings.get_ui_settings()
        geometry = ui_settings.get("window_geometry", "600x500")
        self.root.geometry(geometry)
        
    def _save_text_as(self) -> None:
        """Save text with file dialog."""
        text_content = self.text_display.get(1.0, tk.END).strip()
        if not text_content:
            messagebox.showwarning("Warning", "No text to save!")
            return
            
        output_settings = settings.get_output_settings()
        initial_dir = output_settings.get("save_directory", str(os.path.expanduser("~/Documents")))
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
            ]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(text_content)
                messagebox.showinfo("Success", f"Text saved to: {filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save text: {str(e)}")
                
    def _show_about(self) -> None:
        """Show the About dialog."""
        about_text = (
            "Speech2Text v0.1.0\\n\\n"
            "A desktop application for real-time speech-to-text\\n"
            "transcription using OpenAI's Whisper API.\\n\\n"
            "Built with Python and tkinter\\n"
            "Licensed under MIT License\\n\\n"
            "© 2025 Speech2Text Contributors"
        )
        messagebox.showinfo("About Speech2Text", about_text)
        
    def _show_shortcuts(self) -> None:
        """Show keyboard shortcuts dialog."""
        shortcuts_text = (
            "Keyboard Shortcuts:\\n\\n"
            "Ctrl+N - Start/Stop Recording\\n"
            "Ctrl+S - Save Text\\n"
            "Ctrl+, - Open Settings\\n"
            "F1 - Show About Dialog\\n"
        )
        messagebox.showinfo("Keyboard Shortcuts", shortcuts_text)
        
    def toggle_recording(self) -> None:
        """Toggle recording state."""
        if not self.recording:
            self.start_recording()
        else:
            self.stop_recording()
            
    def start_recording(self) -> None:
        """Start audio recording."""
        if not self.client:
            messagebox.showerror("Error", "OpenAI API key not configured! Please go to Settings to add your API key.")
            return
            
        try:
            self.recording = True
            self.frames = []
            self.record_button.config(text="Stop Recording")
            self.status_label.config(text="Recording... Click 'Stop Recording' when done")
            
            # Start recording in a separate thread
            self.recording_thread = threading.Thread(target=self.record_audio)
            self.recording_thread.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start recording: {str(e)}")
            
    def record_audio(self) -> None:
        """Record audio from microphone."""
        try:
            self.stream = self.audio.open(
                format=self.format,
                channels=self.channels,
                rate=self.rate,
                input=True,
                frames_per_buffer=self.chunk
            )
            
            while self.recording:
                data = self.stream.read(self.chunk)
                self.frames.append(data)
                
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Recording Error", str(e)))
            
    def stop_recording(self) -> None:
        """Stop audio recording and process."""
        self.recording = False
        self.record_button.config(text="Processing...")
        self.status_label.config(text="Processing audio...")
        
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            
        # Process the recording in a separate thread
        processing_thread = threading.Thread(target=self.process_audio)
        processing_thread.start()
        
    def process_audio(self) -> None:
        """Process recorded audio and transcribe."""
        try:
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_filename = temp_file.name
                
            # Write audio data to file
            with wave.open(temp_filename, 'wb') as wf:
                wf.setnchannels(self.channels)
                wf.setsampwidth(self.audio.get_sample_size(self.format))
                wf.setframerate(self.rate)
                wf.writeframes(b''.join(self.frames))
                
            # Transcribe using OpenAI Whisper
            with open(temp_filename, 'rb') as audio_file:
                transcription_settings = settings.get_transcription_settings()
                
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
            self.root.after(0, lambda: self.display_transcription(transcript.text))
            
            # Auto-save if enabled
            output_settings = settings.get_output_settings()
            if output_settings.get("auto_save", False):
                self._auto_save_transcript(transcript.text)
            
            # Clean up temporary file
            os.unlink(temp_filename)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Transcription Error", str(e)))
        finally:
            self.root.after(0, self.reset_ui)
            
    def _auto_save_transcript(self, text: str) -> None:
        """Auto-save transcript to file."""
        try:
            output_settings = settings.get_output_settings()
            save_dir = output_settings.get("save_directory", str(os.path.expanduser("~/Documents")))
            file_format = output_settings.get("file_format", "txt")
            
            # Create filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(save_dir, f"transcript_{timestamp}.{file_format}")
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(text)
                
        except Exception:
            pass  # Silently fail auto-save
            
    def display_transcription(self, text: str) -> None:
        """Display transcribed text in the text area."""
        self.text_display.insert(tk.END, text + "\\n\\n")
        self.text_display.see(tk.END)
        
    def reset_ui(self) -> None:
        """Reset UI to ready state."""
        self.record_button.config(text="Start Recording")
        self.status_label.config(text="Ready to record")
        
    def clear_text(self) -> None:
        """Clear the text display."""
        self.text_display.delete(1.0, tk.END)
        
    def save_text(self) -> None:
        """Save text to default location or show save dialog."""
        output_settings = settings.get_output_settings()
        if output_settings.get("auto_save", False):
            # Auto-save to default location
            text_content = self.text_display.get(1.0, tk.END).strip()
            if text_content:
                self._auto_save_transcript(text_content)
                messagebox.showinfo("Success", "Text saved to default location")
            else:
                messagebox.showwarning("Warning", "No text to save!")
        else:
            # Show save dialog
            self._save_text_as()
            
    def on_closing(self) -> None:
        """Handle application closing."""
        if self.recording:
            self.recording = False
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        
        # Save current window geometry
        geometry = self.root.geometry()
        settings.set("ui.window_geometry", geometry)
        settings.save_settings()
        
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechToTextApp(root)
    root.mainloop()