"""Modern dark-themed settings dialog for Speech2Text application."""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Callable

from .settings import settings
from .theme import DarkTheme, ModernComponents


class ModernSettingsDialog:
    """Modern dark-themed settings configuration dialog."""
    
    def __init__(self, parent: tk.Tk, on_settings_changed: Optional[Callable] = None):
        self.parent = parent
        self.on_settings_changed = on_settings_changed
        self.dialog: Optional[tk.Toplevel] = None
        
    def show(self) -> None:
        """Display the settings dialog."""
        if self.dialog and self.dialog.winfo_exists():
            self.dialog.focus()
            return
        
        self._create_dialog()
        self._load_current_settings()
        
    def _create_dialog(self) -> None:
        """Create the modern settings dialog window."""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("Settings - Speech2Text")
        self.dialog.geometry("600x700")
        self.dialog.resizable(True, True)
        
        # Apply dark theme
        self.dialog.configure(bg=DarkTheme.COLORS['bg_primary'])
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog on parent
        self._center_dialog()
        
        # Configure grid
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        
        # Main container
        main_container = ttk.Frame(self.dialog, style='Dark.TFrame')
        main_container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_container, style='Dark.TFrame')
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        header_label = ModernComponents.create_modern_label(
            header_frame, "Settings", style='HeadingLarge.TLabel'
        )
        header_label.grid(row=0, column=0, sticky="w")
        
        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(main_container, style='Modern.TNotebook')
        self.notebook.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        
        # Create tabs
        self._create_api_tab()
        self._create_transcription_tab()
        self._create_audio_tab()
        self._create_output_tab()
        self._create_ui_tab()
        
        # Create button frame
        self._create_button_frame(main_container)
        
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
        
    def _create_api_tab(self) -> None:
        """Create the API configuration tab."""
        frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(frame, text="🔑 API")
        
        # Scrollable frame for content
        canvas = tk.Canvas(frame, bg=DarkTheme.COLORS['bg_primary'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Dark.TFrame')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0), pady=20)
        scrollbar.pack(side="right", fill="y", padx=(0, 20), pady=20)
        
        # API Key section
        api_card = ModernComponents.create_card_frame(scrollable_frame)
        api_card.pack(fill=tk.X, pady=(0, 20))
        
        # Card content
        card_content = ttk.Frame(api_card, style='Card.TFrame')
        card_content.pack(fill=tk.X, padx=20, pady=20)
        card_content.columnconfigure(1, weight=1)
        
        # Section title
        title_label = ModernComponents.create_modern_label(
            card_content, "OpenAI API Configuration", style='Heading.TLabel'
        )
        title_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))
        
        # API Key input
        ttk.Label(card_content, text="API Key:", style='Dark.TLabel').grid(
            row=1, column=0, sticky=tk.W, pady=5)
        
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ModernComponents.create_modern_entry(
            card_content, textvariable=self.api_key_var, show="*", width=40
        )
        self.api_key_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=5)
        
        # Show/Hide button
        self.show_key_var = tk.BooleanVar()
        show_btn = ttk.Checkbutton(
            card_content, text="Show", variable=self.show_key_var,
            command=self._toggle_api_key_visibility, style='Modern.TCheckbutton'
        )
        show_btn.grid(row=1, column=2, sticky=tk.W, padx=(5, 0), pady=5)
        
        # Test button
        test_btn = ModernComponents.create_modern_button(
            card_content, "Test API Key", command=self._test_api_key,
            style='Secondary.TButton'
        )
        test_btn.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=(10, 0))
        
        # Info text
        info_label = ModernComponents.create_modern_label(
            card_content, 
            "Your API key is encrypted and stored securely.\n"
            "Get your key from: https://platform.openai.com/api-keys",
            style='Muted.TLabel'
        )
        info_label.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(15, 0))
        
    def _create_transcription_tab(self) -> None:
        """Create the transcription settings tab."""
        frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(frame, text="🗣️ Transcription")
        
        # Configure grid weights
        frame.columnconfigure(1, weight=1)
        
        # Language settings
        lang_card = ModernComponents.create_card_frame(frame)
        lang_card.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=20, pady=20)
        lang_card.columnconfigure(1, weight=1)
        
        # Language label and selection
        lang_label = ModernComponents.create_modern_label(
            lang_card, "Language:", style='Heading.TLabel'
        )
        lang_label.grid(row=0, column=0, sticky=tk.W, padx=20, pady=(20, 10))
        
        # Language dropdown
        self.language_var = tk.StringVar()
        language_options = [
            ("English", "en"),
            ("Spanish", "es"), 
            ("French", "fr"),
            ("German", "de"),
            ("Italian", "it"),
            ("Portuguese", "pt"),
            ("Dutch", "nl"),
            ("Polish", "pl"),
            ("Russian", "ru"),
            ("Japanese", "ja"),
            ("Korean", "ko"),
            ("Chinese", "zh"),
            ("Auto-detect", "")
        ]
        
        self.language_combo = ttk.Combobox(
            lang_card,
            textvariable=self.language_var,
            values=[f"{name} ({code})" if code else name for name, code in language_options],
            style='Modern.TCombobox',
            state='readonly'
        )
        self.language_combo.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=20, pady=(0, 10))
        
        # Store language mapping for lookup
        self.language_mapping = {f"{name} ({code})" if code else name: code for name, code in language_options}
        
        # Temperature settings
        temp_label = ModernComponents.create_modern_label(
            lang_card, "Temperature (0.0 = deterministic, 1.0 = creative):", style='Dark.TLabel'
        )
        temp_label.grid(row=2, column=0, sticky=tk.W, padx=20, pady=(10, 5))
        
        self.temperature_var = tk.DoubleVar()
        temp_scale = ttk.Scale(
            lang_card,
            from_=0.0,
            to=1.0,
            variable=self.temperature_var,
            orient=tk.HORIZONTAL
        )
        temp_scale.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=20, pady=(0, 10))
        
        # Temperature value display
        self.temp_value_label = ModernComponents.create_modern_label(
            lang_card, "0.0", style='Status.TLabel'
        )
        self.temp_value_label.grid(row=4, column=0, sticky=tk.W, padx=20, pady=(0, 10))
        
        # Update temperature display when changed
        def update_temp_display(*args):
            self.temp_value_label.config(text=f"{self.temperature_var.get():.1f}")
        self.temperature_var.trace('w', update_temp_display)
        
        # Context prompt
        prompt_label = ModernComponents.create_modern_label(
            lang_card, "Context Prompt (optional):", style='Dark.TLabel'
        )
        prompt_label.grid(row=5, column=0, sticky=tk.W, padx=20, pady=(10, 5))
        
        self.prompt_var = tk.StringVar()
        prompt_entry = ModernComponents.create_modern_entry(lang_card, textvariable=self.prompt_var)
        prompt_entry.grid(row=6, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=20, pady=(0, 20))
        
        # Help text
        help_text = ModernComponents.create_modern_label(
            lang_card,
            "Context prompt helps Whisper understand technical terms or context.\n"
            "Example: 'This is a technical discussion about Python programming.'",
            style='Muted.TLabel'
        )
        help_text.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=20, pady=(0, 20))
        
    def _create_audio_tab(self) -> None:
        """Create the audio settings tab."""
        frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(frame, text="🎤 Audio")
        
        # Main content with padding
        content = ttk.Frame(frame, style='Dark.TFrame')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Recording settings card
        recording_card = ModernComponents.create_card_frame(content)
        recording_card.pack(fill=tk.X, pady=(0, 20))
        
        card_content = ttk.Frame(recording_card, style='Card.TFrame')
        card_content.pack(fill=tk.X, padx=20, pady=20)
        card_content.columnconfigure(1, weight=1)
        
        # Title
        ModernComponents.create_modern_label(
            card_content, "Recording Settings", style='Heading.TLabel'
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        # Sample rate
        ModernComponents.create_modern_label(
            card_content, "Sample Rate (Hz):", style='Dark.TLabel'
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.sample_rate_var = tk.StringVar()
        sample_rate_combo = ttk.Combobox(
            card_content, textvariable=self.sample_rate_var,
            values=["8000", "16000", "22050", "44100", "48000"],
            state="readonly", style='Modern.TCombobox', width=15
        )
        sample_rate_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Channels
        ModernComponents.create_modern_label(
            card_content, "Channels:", style='Dark.TLabel'
        ).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.channels_var = tk.StringVar()
        channels_combo = ttk.Combobox(
            card_content, textvariable=self.channels_var,
            values=["1 (Mono)", "2 (Stereo)"],
            state="readonly", style='Modern.TCombobox', width=15
        )
        channels_combo.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Buffer size
        ModernComponents.create_modern_label(
            card_content, "Buffer Size:", style='Dark.TLabel'
        ).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.chunk_size_var = tk.StringVar()
        chunk_combo = ttk.Combobox(
            card_content, textvariable=self.chunk_size_var,
            values=["512", "1024", "2048", "4096"],
            state="readonly", style='Modern.TCombobox', width=15
        )
        chunk_combo.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Voice detection card
        voice_card = ModernComponents.create_card_frame(content)
        voice_card.pack(fill=tk.X, pady=(0, 20))
        
        voice_content = ttk.Frame(voice_card, style='Card.TFrame')
        voice_content.pack(fill=tk.X, padx=20, pady=20)
        
        ModernComponents.create_modern_label(
            voice_content, "Voice Activity Detection", style='Heading.TLabel'
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Voice threshold
        threshold_frame = ttk.Frame(voice_content, style='Card.TFrame')
        threshold_frame.pack(fill=tk.X, pady=5)
        
        ModernComponents.create_modern_label(
            threshold_frame, "Voice Threshold:", style='Dark.TLabel'
        ).pack(side=tk.LEFT)
        
        self.voice_threshold_var = tk.DoubleVar(value=0.02)
        threshold_scale = ttk.Scale(
            threshold_frame, from_=0.01, to=0.1, orient=tk.HORIZONTAL,
            variable=self.voice_threshold_var, length=200
        )
        threshold_scale.pack(side=tk.LEFT, padx=(10, 5))
        
        self.threshold_label = ModernComponents.create_modern_label(
            threshold_frame, "0.02", style='Muted.TLabel'
        )
        self.threshold_label.pack(side=tk.LEFT)
        
        # Update label when scale changes
        def update_threshold_label(value):
            self.threshold_label.config(text=f"{float(value):.3f}")
        
        threshold_scale.config(command=update_threshold_label)
        
        # Info
        ModernComponents.create_modern_label(
            voice_content,
            "Higher values = less sensitive to quiet sounds\n"
            "Lower values = more sensitive to background noise",
            style='Muted.TLabel'
        ).pack(anchor=tk.W, pady=(10, 0))
        
    def _create_output_tab(self) -> None:
        """Create the output settings tab."""
        frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(frame, text="💾 Output")
        
        content = ttk.Frame(frame, style='Dark.TFrame')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # File output card
        output_card = ModernComponents.create_card_frame(content)
        output_card.pack(fill=tk.X, pady=(0, 20))
        
        card_content = ttk.Frame(output_card, style='Card.TFrame')
        card_content.pack(fill=tk.X, padx=20, pady=20)
        card_content.columnconfigure(1, weight=1)
        
        ModernComponents.create_modern_label(
            card_content, "File Output Settings", style='Heading.TLabel'
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 15))
        
        # Auto-save
        self.auto_save_var = tk.BooleanVar()
        ttk.Checkbutton(
            card_content, text="Auto-save transcriptions",
            variable=self.auto_save_var, style='Modern.TCheckbutton'
        ).grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=5)
        
        # Save directory
        ModernComponents.create_modern_label(
            card_content, "Save Directory:", style='Dark.TLabel'
        ).grid(row=2, column=0, sticky=tk.W, pady=(15, 5))
        
        self.save_dir_var = tk.StringVar()
        dir_entry = ModernComponents.create_modern_entry(
            card_content, textvariable=self.save_dir_var, state="readonly", width=35
        )
        dir_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(10, 5), pady=(15, 5))
        
        browse_btn = ModernComponents.create_modern_button(
            card_content, "Browse", command=self._browse_save_directory,
            style='Secondary.TButton'
        )
        browse_btn.grid(row=2, column=2, sticky=tk.E, pady=(15, 5))
        
        # File format
        ModernComponents.create_modern_label(
            card_content, "File Format:", style='Dark.TLabel'
        ).grid(row=3, column=0, sticky=tk.W, pady=5)
        
        self.file_format_var = tk.StringVar()
        format_combo = ttk.Combobox(
            card_content, textvariable=self.file_format_var,
            values=["txt", "md", "rtf"],
            state="readonly", style='Modern.TCombobox', width=15
        )
        format_combo.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
    def _create_ui_tab(self) -> None:
        """Create the UI settings tab."""
        frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(frame, text="🎨 Interface")
        
        content = ttk.Frame(frame, style='Dark.TFrame')
        content.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Interface card
        ui_card = ModernComponents.create_card_frame(content)
        ui_card.pack(fill=tk.X, pady=(0, 20))
        
        card_content = ttk.Frame(ui_card, style='Card.TFrame')
        card_content.pack(fill=tk.X, padx=20, pady=20)
        card_content.columnconfigure(1, weight=1)
        
        ModernComponents.create_modern_label(
            card_content, "Interface Settings", style='Heading.TLabel'
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 15))
        
        # Theme (for future use)
        ModernComponents.create_modern_label(
            card_content, "Theme:", style='Dark.TLabel'
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.theme_var = tk.StringVar()
        theme_combo = ttk.Combobox(
            card_content, textvariable=self.theme_var,
            values=["Dark (Current)", "Light (Coming Soon)"],
            state="readonly", style='Modern.TCombobox', width=20
        )
        theme_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Window size
        ModernComponents.create_modern_label(
            card_content, "Window Size:", style='Dark.TLabel'
        ).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.geometry_var = tk.StringVar()
        geometry_combo = ttk.Combobox(
            card_content, textvariable=self.geometry_var,
            values=["900x700", "800x600", "1000x800", "1200x900"],
            state="readonly", style='Modern.TCombobox', width=20
        )
        geometry_combo.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Advanced section
        advanced_card = ModernComponents.create_card_frame(content)
        advanced_card.pack(fill=tk.X)
        
        advanced_content = ttk.Frame(advanced_card, style='Card.TFrame')
        advanced_content.pack(fill=tk.X, padx=20, pady=20)
        
        ModernComponents.create_modern_label(
            advanced_content, "Advanced Options", style='Heading.TLabel'
        ).pack(anchor=tk.W, pady=(0, 15))
        
        # Button frame
        button_frame = ttk.Frame(advanced_content, style='Card.TFrame')
        button_frame.pack(fill=tk.X)
        
        ModernComponents.create_modern_button(
            button_frame, "Export Settings", command=self._export_settings,
            style='Secondary.TButton'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ModernComponents.create_modern_button(
            button_frame, "Import Settings", command=self._import_settings,
            style='Secondary.TButton'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ModernComponents.create_modern_button(
            button_frame, "Reset to Defaults", command=self._reset_to_defaults,
            style='Secondary.TButton'
        ).pack(side=tk.LEFT)
        
    def _create_button_frame(self, parent: ttk.Frame) -> None:
        """Create the dialog button frame."""
        button_frame = ttk.Frame(parent, style='Dark.TFrame')
        button_frame.grid(row=2, column=0, sticky="ew")
        
        # Right-aligned buttons
        ModernComponents.create_modern_button(
            button_frame, "Cancel", command=self._on_cancel,
            style='Secondary.TButton'
        ).pack(side=tk.RIGHT, padx=(10, 0))
        
        ModernComponents.create_modern_button(
            button_frame, "Apply", command=self._on_apply,
            style='Secondary.TButton'
        ).pack(side=tk.RIGHT)
        
        ModernComponents.create_modern_button(
            button_frame, "OK", command=self._on_ok,
            style='Modern.TButton'
        ).pack(side=tk.RIGHT, padx=(0, 10))
    
    def _load_current_settings(self) -> None:
        """Load current settings into the dialog controls."""
        # API settings
        self.api_key_var.set(settings.get_api_key())
        
        # Transcription settings
        transcription_settings = settings.get_transcription_settings()
        language_code = transcription_settings.get("language", "en")
        
        # Find matching language display text
        language_display = "English (en)"  # Default
        for display_text, code in self.language_mapping.items():
            if code == language_code:
                language_display = display_text
                break
        self.language_var.set(language_display)
        
        self.temperature_var.set(transcription_settings.get("temperature", 0.0))
        self.prompt_var.set(transcription_settings.get("prompt", ""))
        
        # Audio settings
        audio_settings = settings.get_audio_settings()
        self.sample_rate_var.set(str(audio_settings.get("sample_rate", 44100)))
        channels = audio_settings.get("channels", 1)
        self.channels_var.set(f"{channels} ({'Mono' if channels == 1 else 'Stereo'})")
        self.chunk_size_var.set(str(audio_settings.get("chunk_size", 1024)))
        
        # Voice threshold
        self.voice_threshold_var.set(audio_settings.get("voice_threshold", 0.02))
        
        # Output settings
        output_settings = settings.get_output_settings()
        self.auto_save_var.set(output_settings.get("auto_save", False))
        self.save_dir_var.set(output_settings.get("save_directory", ""))
        self.file_format_var.set(output_settings.get("file_format", "txt"))
        
        # UI settings
        ui_settings = settings.get_ui_settings()
        self.theme_var.set("Dark (Current)")
        self.geometry_var.set(ui_settings.get("window_geometry", "900x700"))
    
    def _toggle_api_key_visibility(self) -> None:
        """Toggle API key visibility."""
        if self.show_key_var.get():
            self.api_key_entry.config(show="")
        else:
            self.api_key_entry.config(show="*")
    
    def _test_api_key(self) -> None:
        """Test API key validity."""
        api_key = self.api_key_var.get().strip()
        
        if not api_key:
            messagebox.showwarning("API Key Test", "Please enter an API key first.", parent=self.dialog)
            return
        
        if not settings.validate_api_key(api_key):
            messagebox.showerror(
                "Invalid API Key",
                "API key format is invalid. Keys should start with 'sk-'.",
                parent=self.dialog
            )
            return
        
        messagebox.showinfo(
            "API Key Valid",
            "API key format is valid!\n\nNote: This only checks the format, not if the key is active.",
            parent=self.dialog
        )
    
    def _browse_save_directory(self) -> None:
        """Browse for save directory."""
        directory = filedialog.askdirectory(
            title="Select Save Directory",
            initialdir=self.save_dir_var.get(),
            parent=self.dialog
        )
        if directory:
            self.save_dir_var.set(directory)
    
    def _export_settings(self) -> None:
        """Export settings to file."""
        file_path = filedialog.asksaveasfilename(
            title="Export Settings",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            parent=self.dialog
        )
        
        if file_path:
            if settings.export_settings(file_path):
                messagebox.showinfo("Export Complete", "Settings exported successfully!", parent=self.dialog)
            else:
                messagebox.showerror("Export Failed", "Failed to export settings.", parent=self.dialog)
    
    def _import_settings(self) -> None:
        """Import settings from file."""
        file_path = filedialog.askopenfilename(
            title="Import Settings",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            parent=self.dialog
        )
        
        if file_path:
            if settings.import_settings(file_path):
                self._load_current_settings()
                messagebox.showinfo("Import Complete", "Settings imported successfully!", parent=self.dialog)
            else:
                messagebox.showerror("Import Failed", "Failed to import settings.", parent=self.dialog)
    
    def _reset_to_defaults(self) -> None:
        """Reset settings to defaults."""
        if messagebox.askyesno(
            "Reset Settings",
            "Are you sure you want to reset all settings to defaults?\n\n"
            "This action cannot be undone.",
            parent=self.dialog
        ):
            settings.reset_to_defaults()
            self._load_current_settings()
            messagebox.showinfo("Reset Complete", "Settings have been reset to defaults.", parent=self.dialog)
    
    def _save_settings(self) -> bool:
        """Save current dialog settings."""
        try:
            # Save API key
            api_key = self.api_key_var.get().strip()
            if api_key and not settings.validate_api_key(api_key):
                messagebox.showerror(
                    "Invalid API Key",
                    "API key format is invalid. Keys should start with 'sk-'.",
                    parent=self.dialog
                )
                return False
            settings.set_api_key(api_key)
            
            # Save transcription settings
            language_display = self.language_var.get()
            language_code = self.language_mapping.get(language_display, "en")
            settings.set("transcription.language", language_code)
            settings.set("transcription.temperature", self.temperature_var.get())
            settings.set("transcription.prompt", self.prompt_var.get().strip())
            
            # Save audio settings
            settings.set("audio.sample_rate", int(self.sample_rate_var.get()))
            channels_text = self.channels_var.get()
            channels = 1 if "Mono" in channels_text else 2
            settings.set("audio.channels", channels)
            settings.set("audio.chunk_size", int(self.chunk_size_var.get()))
            settings.set("audio.voice_threshold", self.voice_threshold_var.get())
            
            # Save output settings
            settings.set("output.auto_save", self.auto_save_var.get())
            settings.set("output.save_directory", self.save_dir_var.get())
            settings.set("output.file_format", self.file_format_var.get())
            
            # Save UI settings
            settings.set("ui.window_geometry", self.geometry_var.get())
            
            # Persist settings
            return settings.save_settings()
            
        except ValueError as e:
            messagebox.showerror("Settings Error", f"Invalid setting value: {e}", parent=self.dialog)
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
            messagebox.showinfo("Settings Applied", "Settings have been applied successfully!", parent=self.dialog)
    
    def _on_cancel(self) -> None:
        """Handle Cancel button click."""
        self._close_dialog()
    
    def _close_dialog(self) -> None:
        """Close the settings dialog."""
        if self.dialog:
            self.dialog.destroy()
            self.dialog = None