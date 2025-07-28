"""
Settings dialog for Speech2Text application.

Provides a user interface for configuring application settings including
API key management, audio parameters, and output preferences.
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Callable
from settings import settings


class SettingsDialog:
    """Settings configuration dialog window."""
    
    def __init__(self, parent: tk.Tk, on_settings_changed: Optional[Callable] = None):
        self.parent = parent
        self.on_settings_changed = on_settings_changed
        self.dialog: Optional[tk.Toplevel] = None
        
        # Temporary settings storage
        self.temp_settings = {}
        
    def show(self) -> None:
        """Display the settings dialog."""
        if self.dialog and self.dialog.winfo_exists():
            self.dialog.focus()
            return
        
        self._create_dialog()
        self._load_current_settings()
        
    def _create_dialog(self) -> None:
        """Create the settings dialog window."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Settings - Speech2Text")
        self.dialog.geometry("500x600")
        self.dialog.resizable(True, True)
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog on parent
        self._center_dialog()
        
        # Create notebook for tabbed interface
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self._create_api_tab(notebook)
        self._create_audio_tab(notebook)
        self._create_output_tab(notebook)
        self._create_ui_tab(notebook)
        
        # Create button frame
        self._create_button_frame()
        
        # Handle dialog close
        self.dialog.protocol("WM_DELETE_WINDOW", self._on_cancel)
        
    def _center_dialog(self) -> None:
        """Center the dialog on the parent window."""
        self.dialog.update_idletasks()
        
        # Get parent position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Get dialog size
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()
        
        # Calculate center position
        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2
        
        self.dialog.geometry(f"+{x}+{y}")
        
    def _create_api_tab(self, notebook: ttk.Notebook) -> None:
        """Create the API configuration tab."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="API Configuration")
        
        # API Key section
        api_frame = ttk.LabelFrame(frame, text="OpenAI API Settings", padding=10)
        api_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(api_frame, text="API Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ttk.Entry(api_frame, textvariable=self.api_key_var, 
                                      show="*", width=50)
        self.api_key_entry.grid(row=0, column=1, columnspan=2, sticky=(tk.W, tk.E), 
                               padx=(10, 0), pady=5)
        
        # Show/Hide API key button
        self.show_key_var = tk.BooleanVar()
        ttk.Checkbutton(api_frame, text="Show API Key", variable=self.show_key_var,
                       command=self._toggle_api_key_visibility).grid(row=1, column=1, 
                                                                    sticky=tk.W, pady=5)
        
        # Test API key button
        ttk.Button(api_frame, text="Test API Key", 
                  command=self._test_api_key).grid(row=1, column=2, sticky=tk.E, pady=5)
        
        # API Key info
        info_text = ("Your OpenAI API key is encrypted and stored securely on your device.\n"
                    "Get your API key from: https://platform.openai.com/api-keys")
        info_label = ttk.Label(api_frame, text=info_text, wraplength=450, 
                              foreground="gray")
        info_label.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        api_frame.columnconfigure(1, weight=1)
        
    def _create_audio_tab(self, notebook: ttk.Notebook) -> None:
        """Create the audio configuration tab."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Audio Settings")
        
        # Audio recording settings
        audio_frame = ttk.LabelFrame(frame, text="Recording Settings", padding=10)
        audio_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Sample rate
        ttk.Label(audio_frame, text="Sample Rate (Hz):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.sample_rate_var = tk.StringVar()
        sample_rate_combo = ttk.Combobox(audio_frame, textvariable=self.sample_rate_var,
                                        values=["8000", "16000", "22050", "44100", "48000"],
                                        state="readonly", width=20)
        sample_rate_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Channels
        ttk.Label(audio_frame, text="Channels:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.channels_var = tk.StringVar()
        channels_combo = ttk.Combobox(audio_frame, textvariable=self.channels_var,
                                     values=["1 (Mono)", "2 (Stereo)"],
                                     state="readonly", width=20)
        channels_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Chunk size
        ttk.Label(audio_frame, text="Buffer Size:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.chunk_size_var = tk.StringVar()
        chunk_combo = ttk.Combobox(audio_frame, textvariable=self.chunk_size_var,
                                  values=["512", "1024", "2048", "4096"],
                                  state="readonly", width=20)
        chunk_combo.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Audio quality info
        quality_frame = ttk.LabelFrame(frame, text="Quality Information", padding=10)
        quality_frame.pack(fill=tk.X, padx=10, pady=10)
        
        quality_text = ("Higher sample rates provide better quality but larger file sizes.\n"
                       "44100 Hz is CD quality and recommended for most users.\n"
                       "Mono (1 channel) is sufficient for speech recognition.")
        ttk.Label(quality_frame, text=quality_text, wraplength=450,
                 foreground="gray").pack(anchor=tk.W)
        
    def _create_output_tab(self, notebook: ttk.Notebook) -> None:
        """Create the output configuration tab."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Output Settings")
        
        # File output settings
        output_frame = ttk.LabelFrame(frame, text="File Output", padding=10)
        output_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Auto-save option
        self.auto_save_var = tk.BooleanVar()
        ttk.Checkbutton(output_frame, text="Auto-save transcriptions",
                       variable=self.auto_save_var).grid(row=0, column=0, columnspan=3,
                                                         sticky=tk.W, pady=5)
        
        # Save directory
        ttk.Label(output_frame, text="Save Directory:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.save_dir_var = tk.StringVar()
        ttk.Entry(output_frame, textvariable=self.save_dir_var,
                 width=40, state="readonly").grid(row=1, column=1, sticky=(tk.W, tk.E),
                                                 padx=(10, 5), pady=5)
        ttk.Button(output_frame, text="Browse",
                  command=self._browse_save_directory).grid(row=1, column=2, sticky=tk.E, pady=5)
        
        # File format
        ttk.Label(output_frame, text="File Format:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.file_format_var = tk.StringVar()
        format_combo = ttk.Combobox(output_frame, textvariable=self.file_format_var,
                                   values=["txt", "md", "rtf"],
                                   state="readonly", width=20)
        format_combo.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        output_frame.columnconfigure(1, weight=1)
        
    def _create_ui_tab(self, notebook: ttk.Notebook) -> None:
        """Create the UI configuration tab."""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Interface")
        
        # UI settings
        ui_frame = ttk.LabelFrame(frame, text="Interface Settings", padding=10)
        ui_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Theme selection (placeholder for future implementation)
        ttk.Label(ui_frame, text="Theme:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.theme_var = tk.StringVar()
        theme_combo = ttk.Combobox(ui_frame, textvariable=self.theme_var,
                                  values=["Default", "Dark (Coming Soon)"],
                                  state="readonly", width=20)
        theme_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Window geometry
        ttk.Label(ui_frame, text="Window Size:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.geometry_var = tk.StringVar()
        geometry_combo = ttk.Combobox(ui_frame, textvariable=self.geometry_var,
                                     values=["600x500", "800x600", "1000x700", "1200x800"],
                                     state="readonly", width=20)
        geometry_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Advanced section
        advanced_frame = ttk.LabelFrame(frame, text="Advanced", padding=10)
        advanced_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Export/Import buttons
        ttk.Button(advanced_frame, text="Export Settings",
                  command=self._export_settings).grid(row=0, column=0, padx=(0, 5), pady=5)
        ttk.Button(advanced_frame, text="Import Settings",
                  command=self._import_settings).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(advanced_frame, text="Reset to Defaults",
                  command=self._reset_to_defaults).grid(row=0, column=2, padx=5, pady=5)
        
    def _create_button_frame(self) -> None:
        """Create the dialog button frame."""
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Right-aligned buttons
        ttk.Button(button_frame, text="Cancel",
                  command=self._on_cancel).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="Apply",
                  command=self._on_apply).pack(side=tk.RIGHT, padx=(5, 0))
        ttk.Button(button_frame, text="OK",
                  command=self._on_ok).pack(side=tk.RIGHT, padx=(5, 0))
        
    def _load_current_settings(self) -> None:
        """Load current settings into the dialog controls."""
        # API settings
        self.api_key_var.set(settings.get_api_key())
        
        # Audio settings
        audio_settings = settings.get_audio_settings()
        self.sample_rate_var.set(str(audio_settings.get("sample_rate", 44100)))
        channels = audio_settings.get("channels", 1)
        self.channels_var.set(f"{channels} ({'Mono' if channels == 1 else 'Stereo'})")
        self.chunk_size_var.set(str(audio_settings.get("chunk_size", 1024)))
        
        # Output settings
        output_settings = settings.get_output_settings()
        self.auto_save_var.set(output_settings.get("auto_save", False))
        self.save_dir_var.set(output_settings.get("save_directory", ""))
        self.file_format_var.set(output_settings.get("file_format", "txt"))
        
        # UI settings
        ui_settings = settings.get_ui_settings()
        self.theme_var.set(ui_settings.get("theme", "Default").title())
        self.geometry_var.set(ui_settings.get("window_geometry", "600x500"))
        
    def _toggle_api_key_visibility(self) -> None:
        """Toggle API key visibility in the entry field."""
        if self.show_key_var.get():
            self.api_key_entry.config(show="")
        else:
            self.api_key_entry.config(show="*")
            
    def _test_api_key(self) -> None:
        """Test the API key validity."""
        api_key = self.api_key_var.get().strip()
        
        if not api_key:
            messagebox.showwarning("API Key Test", "Please enter an API key first.")
            return
            
        if not settings.validate_api_key(api_key):
            messagebox.showerror("API Key Test", 
                               "Invalid API key format. Keys should start with 'sk-'.")
            return
            
        # Here you could add actual API testing
        messagebox.showinfo("API Key Test", 
                          "API key format is valid. Test connection functionality coming soon.")
        
    def _browse_save_directory(self) -> None:
        """Browse for save directory."""
        directory = filedialog.askdirectory(
            title="Select Save Directory",
            initialdir=self.save_dir_var.get()
        )
        if directory:
            self.save_dir_var.set(directory)
            
    def _export_settings(self) -> None:
        """Export settings to file."""
        file_path = filedialog.asksaveasfilename(
            title="Export Settings",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            if settings.export_settings(file_path):
                messagebox.showinfo("Export Settings", "Settings exported successfully.")
            else:
                messagebox.showerror("Export Settings", "Failed to export settings.")
                
    def _import_settings(self) -> None:
        """Import settings from file."""
        file_path = filedialog.askopenfilename(
            title="Import Settings",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            if settings.import_settings(file_path):
                self._load_current_settings()
                messagebox.showinfo("Import Settings", "Settings imported successfully.")
            else:
                messagebox.showerror("Import Settings", "Failed to import settings.")
                
    def _reset_to_defaults(self) -> None:
        """Reset all settings to defaults."""
        if messagebox.askyesno("Reset Settings", 
                             "Are you sure you want to reset all settings to defaults?\n"
                             "This action cannot be undone."):
            settings.reset_to_defaults()
            self._load_current_settings()
            messagebox.showinfo("Reset Settings", "Settings reset to defaults.")
            
    def _save_settings(self) -> bool:
        """Save current dialog settings."""
        try:
            # Save API key
            api_key = self.api_key_var.get().strip()
            if api_key and not settings.validate_api_key(api_key):
                messagebox.showerror("Invalid API Key", 
                                   "API key format is invalid. Keys should start with 'sk-'.")
                return False
            settings.set_api_key(api_key)
            
            # Save audio settings
            settings.set("audio.sample_rate", int(self.sample_rate_var.get()))
            channels_text = self.channels_var.get()
            channels = 1 if "Mono" in channels_text else 2
            settings.set("audio.channels", channels)
            settings.set("audio.chunk_size", int(self.chunk_size_var.get()))
            
            # Save output settings
            settings.set("output.auto_save", self.auto_save_var.get())
            settings.set("output.save_directory", self.save_dir_var.get())
            settings.set("output.file_format", self.file_format_var.get())
            
            # Save UI settings
            settings.set("ui.theme", self.theme_var.get().lower())
            settings.set("ui.window_geometry", self.geometry_var.get())
            
            # Persist settings
            return settings.save_settings()
            
        except ValueError as e:
            messagebox.showerror("Settings Error", f"Invalid setting value: {e}")
            return False
            
    def _on_ok(self) -> None:
        """Handle OK button click."""
        if self._save_settings():
            if self.on_settings_changed:
                self.on_settings_changed()
            self._close_dialog()
        
    def _on_apply(self) -> None:
        """Handle Apply button click."""
        if self._save_settings():
            if self.on_settings_changed:
                self.on_settings_changed()
            messagebox.showinfo("Settings", "Settings applied successfully.")
            
    def _on_cancel(self) -> None:
        """Handle Cancel button click."""
        self._close_dialog()
        
    def _close_dialog(self) -> None:
        """Close the settings dialog."""
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None