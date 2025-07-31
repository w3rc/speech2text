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
        self.dialog.geometry("800x750")
        self.dialog.resizable(True, True)
        self.dialog.minsize(750, 650)
        
        # Apply dark theme and remove window borders
        self.dialog.configure(bg=DarkTheme.COLORS['bg_primary'], 
                             relief='flat', 
                             bd=0,
                             highlightthickness=0)
        
        # Make dialog modal
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # Center dialog on parent
        self._center_dialog()
        
        # Configure grid
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        
        # Main container with better spacing
        main_container = ttk.Frame(self.dialog, style='Dark.TFrame')
        main_container.grid(row=0, column=0, sticky="nsew", padx=25, pady=25)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
        
        # Header with subtitle
        header_frame = ttk.Frame(main_container, style='Dark.TFrame')
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 25))
        header_frame.columnconfigure(0, weight=1)
        
        header_label = ModernComponents.create_modern_label(
            header_frame, "Settings", style='HeadingLarge.TLabel'
        )
        header_label.grid(row=0, column=0, sticky="w")
        
        subtitle_label = ModernComponents.create_modern_label(
            header_frame, "Configure your Speech2Text application preferences", style='Muted.TLabel'
        )
        subtitle_label.grid(row=1, column=0, sticky="w", pady=(5, 0))
        
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
        self.notebook.add(frame, text="🔑 API Key")
        
        # Main content frame - no scrolling needed for API tab
        content_frame = ttk.Frame(frame, style='Dark.TFrame')
        content_frame.pack(fill='both', expand=True, padx=25, pady=25)
        content_frame.columnconfigure(0, weight=1)
        
        # API Key section - improved layout
        api_card = ModernComponents.create_card_frame(content_frame)
        api_card.pack(fill=tk.X, pady=(0, 20))
        
        # Card content with better spacing
        card_content = ttk.Frame(api_card, style='Card.TFrame')
        card_content.pack(fill=tk.X, padx=25, pady=25)
        card_content.columnconfigure(1, weight=1)
        
        # Section title with better spacing
        title_label = ModernComponents.create_modern_label(
            card_content, "OpenAI API Configuration", style='Heading.TLabel'
        )
        title_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 20))
        
        # API Key input with improved layout
        key_label = ModernComponents.create_modern_label(
            card_content, "API Key:", style='Dark.TLabel'
        )
        key_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 10))
        
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ModernComponents.create_modern_entry(
            card_content, textvariable=self.api_key_var, show="*", width=50
        )
        self.api_key_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(15, 10), pady=(5, 10))
        
        # Show/Hide button with better styling
        self.show_key_var = tk.BooleanVar()
        show_btn = ttk.Checkbutton(
            card_content, text="Show", variable=self.show_key_var,
            command=self._toggle_api_key_visibility, style='Modern.TCheckbutton'
        )
        show_btn.grid(row=1, column=2, sticky=tk.W, pady=(5, 10))
        
        # Button frame for better alignment
        button_frame = ttk.Frame(card_content, style='Card.TFrame')
        button_frame.grid(row=2, column=1, sticky=tk.W, padx=(15, 0), pady=(5, 15))
        
        test_btn = ModernComponents.create_modern_button(
            button_frame, "Test Connection", command=self._test_api_key,
            style='Secondary.TButton'
        )
        test_btn.pack(side=tk.LEFT)
        
        # Info section with better formatting
        info_frame = ttk.Frame(card_content, style='Card.TFrame')
        info_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(10, 0))
        
        info_icon = ModernComponents.create_modern_label(
            info_frame, "ℹ️", style='Status.TLabel'
        )
        info_icon.pack(side=tk.LEFT, anchor=tk.N, padx=(0, 10))
        
        info_text = ModernComponents.create_modern_label(
            info_frame, 
            "Your API key is encrypted and stored securely on your device.\n"
            "Get your API key from: https://platform.openai.com/api-keys\n"
            "The key should start with 'sk-' followed by your unique identifier.",
            style='Muted.TLabel'
        )
        info_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
    def _create_transcription_tab(self) -> None:
        """Create the transcription settings tab."""
        frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(frame, text="🗣️ Transcription")
        
        # Main content frame
        content_frame = ttk.Frame(frame, style='Dark.TFrame')
        content_frame.pack(fill='both', expand=True, padx=25, pady=25)
        content_frame.columnconfigure(0, weight=1)
        
        # Language settings card
        lang_card = ModernComponents.create_card_frame(content_frame)
        lang_card.pack(fill=tk.X, pady=(0, 20))
        
        # Card content with proper spacing
        lang_content = ttk.Frame(lang_card, style='Card.TFrame')
        lang_content.pack(fill=tk.X, padx=25, pady=25)
        lang_content.columnconfigure(1, weight=1)
        
        # Section title
        title_label = ModernComponents.create_modern_label(
            lang_content, "Language & Model Settings", style='Heading.TLabel'
        )
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        
        # Language selection with better layout
        lang_label = ModernComponents.create_modern_label(
            lang_content, "Language:", style='Dark.TLabel'
        )
        lang_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 10))
        
        self.language_var = tk.StringVar()
        language_options = [
            ("Auto-detect", ""),
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
            ("Chinese", "zh")
        ]
        
        self.language_combo = ttk.Combobox(
            lang_content,
            textvariable=self.language_var,
            values=[f"{name} ({code})" if code else name for name, code in language_options],
            style='Modern.TCombobox',
            state='readonly',
            width=30
        )
        self.language_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(15, 0), pady=(5, 10))
        
        # Store language mapping for lookup
        self.language_mapping = {f"{name} ({code})" if code else name: code for name, code in language_options}
        
        # Temperature settings with better layout
        temp_label = ModernComponents.create_modern_label(
            lang_content, "Temperature:", style='Dark.TLabel'
        )
        temp_label.grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        temp_frame = ttk.Frame(lang_content, style='Card.TFrame')
        temp_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(15, 0), pady=(10, 5))
        temp_frame.columnconfigure(0, weight=1)
        
        self.temperature_var = tk.DoubleVar()
        temp_scale = ttk.Scale(
            temp_frame,
            from_=0.0,
            to=1.0,
            variable=self.temperature_var,
            orient=tk.HORIZONTAL,
            length=200
        )
        temp_scale.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        # Temperature value display
        self.temp_value_label = ModernComponents.create_modern_label(
            temp_frame, "0.0", style='Status.TLabel'
        )
        self.temp_value_label.grid(row=0, column=1, padx=(10, 0))
        
        # Update temperature display when changed
        def update_temp_display(*args):
            self.temp_value_label.config(text=f"{self.temperature_var.get():.1f}")
        self.temperature_var.trace('w', update_temp_display)
        
        # Temperature help text
        temp_help = ModernComponents.create_modern_label(
            lang_content, "0.0 = deterministic, 1.0 = creative", style='Muted.TLabel'
        )
        temp_help.grid(row=3, column=1, sticky=tk.W, padx=(15, 0), pady=(0, 15))
        
        # Context prompt section
        prompt_card = ModernComponents.create_card_frame(content_frame)
        prompt_card.pack(fill=tk.X)
        
        prompt_content = ttk.Frame(prompt_card, style='Card.TFrame')
        prompt_content.pack(fill=tk.X, padx=25, pady=25)
        prompt_content.columnconfigure(0, weight=1)
        
        # Prompt section title
        prompt_title = ModernComponents.create_modern_label(
            prompt_content, "Context Prompt (Optional)", style='Heading.TLabel'
        )
        prompt_title.pack(anchor=tk.W, pady=(0, 15))
        
        # Prompt entry
        self.prompt_var = tk.StringVar()
        prompt_entry = ModernComponents.create_modern_entry(
            prompt_content, textvariable=self.prompt_var, width=60
        )
        prompt_entry.pack(fill=tk.X, pady=(0, 10))
        
        # Help text with icon
        help_frame = ttk.Frame(prompt_content, style='Card.TFrame')
        help_frame.pack(fill=tk.X)
        
        help_icon = ModernComponents.create_modern_label(
            help_frame, "💡", style='Status.TLabel'
        )
        help_icon.pack(side=tk.LEFT, anchor=tk.N, padx=(0, 10))
        
        help_text = ModernComponents.create_modern_label(
            help_frame,
            "Context prompts help Whisper understand technical terms or specific domains.\n"
            "Example: 'This is a technical discussion about Python programming and AI models.'",
            style='Muted.TLabel'
        )
        help_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
    def _create_audio_tab(self) -> None:
        """Create the audio settings tab."""
        frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(frame, text="🎤 Audio")
        
        # Main content with better padding
        content = ttk.Frame(frame, style='Dark.TFrame')
        content.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        content.columnconfigure(0, weight=1)
        
        # Recording settings card with improved layout
        recording_card = ModernComponents.create_card_frame(content)
        recording_card.pack(fill=tk.X, pady=(0, 20))
        
        card_content = ttk.Frame(recording_card, style='Card.TFrame')
        card_content.pack(fill=tk.X, padx=25, pady=25)
        card_content.columnconfigure(1, weight=1)
        
        # Title with better spacing
        ModernComponents.create_modern_label(
            card_content, "Audio Recording Settings", style='Heading.TLabel'
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        
        # Sample rate with description
        ModernComponents.create_modern_label(
            card_content, "Sample Rate:", style='Dark.TLabel'
        ).grid(row=1, column=0, sticky=tk.W, pady=(5, 10))
        
        self.sample_rate_var = tk.StringVar()
        sample_rate_combo = ttk.Combobox(
            card_content, textvariable=self.sample_rate_var,
            values=["8000 Hz (Low quality)", "16000 Hz (Good for speech)", "22050 Hz", "44100 Hz (CD quality)", "48000 Hz (Professional)"],
            state="readonly", style='Modern.TCombobox', width=35
        )
        sample_rate_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(15, 0), pady=(5, 10))
        
        # Channels with description
        ModernComponents.create_modern_label(
            card_content, "Channels:", style='Dark.TLabel'
        ).grid(row=2, column=0, sticky=tk.W, pady=(5, 10))
        
        self.channels_var = tk.StringVar()
        channels_combo = ttk.Combobox(
            card_content, textvariable=self.channels_var,
            values=["1 (Mono - Recommended)", "2 (Stereo)"],
            state="readonly", style='Modern.TCombobox', width=35
        )
        channels_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(15, 0), pady=(5, 10))
        
        # Buffer size with description
        ModernComponents.create_modern_label(
            card_content, "Buffer Size:", style='Dark.TLabel'
        ).grid(row=3, column=0, sticky=tk.W, pady=(5, 10))
        
        self.chunk_size_var = tk.StringVar()
        chunk_combo = ttk.Combobox(
            card_content, textvariable=self.chunk_size_var,
            values=["512 (Low latency)", "1024 (Recommended)", "2048 (High latency)", "4096 (Very high latency)"],
            state="readonly", style='Modern.TCombobox', width=35
        )
        chunk_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(15, 0), pady=(5, 10))
        
        # Voice detection card with improved layout
        voice_card = ModernComponents.create_card_frame(content)
        voice_card.pack(fill=tk.X)
        
        voice_content = ttk.Frame(voice_card, style='Card.TFrame')
        voice_content.pack(fill=tk.X, padx=25, pady=25)
        voice_content.columnconfigure(1, weight=1)
        
        # Title
        ModernComponents.create_modern_label(
            voice_content, "Voice Activity Detection", style='Heading.TLabel'
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        
        # Voice threshold with better layout
        ModernComponents.create_modern_label(
            voice_content, "Sensitivity:", style='Dark.TLabel'
        ).grid(row=1, column=0, sticky=tk.W, pady=(5, 10))
        
        threshold_frame = ttk.Frame(voice_content, style='Card.TFrame')
        threshold_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(15, 0), pady=(5, 10))
        threshold_frame.columnconfigure(0, weight=1)
        
        self.voice_threshold_var = tk.DoubleVar(value=0.02)
        threshold_scale = ttk.Scale(
            threshold_frame, from_=0.01, to=0.1, orient=tk.HORIZONTAL,
            variable=self.voice_threshold_var, length=200
        )
        threshold_scale.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.threshold_label = ModernComponents.create_modern_label(
            threshold_frame, "0.020", style='Status.TLabel'
        )
        self.threshold_label.grid(row=0, column=1, padx=(10, 0))
        
        # Update label when scale changes
        def update_threshold_label(value):
            self.threshold_label.config(text=f"{float(value):.3f}")
        
        threshold_scale.config(command=update_threshold_label)
        
        # Info with icon
        info_frame = ttk.Frame(voice_content, style='Card.TFrame')
        info_frame.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(15, 0), pady=(5, 0))
        
        info_icon = ModernComponents.create_modern_label(
            info_frame, "ℹ️", style='Status.TLabel'
        )
        info_icon.pack(side=tk.LEFT, anchor=tk.N, padx=(0, 10))
        
        info_text = ModernComponents.create_modern_label(
            info_frame,
            "Lower values = more sensitive (detects quieter sounds)\n"
            "Higher values = less sensitive (ignores background noise)",
            style='Muted.TLabel'
        )
        info_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
    def _create_output_tab(self) -> None:
        """Create the output settings tab."""
        frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(frame, text="💾 Output")
        
        content = ttk.Frame(frame, style='Dark.TFrame')
        content.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        content.columnconfigure(0, weight=1)
        
        # File output card with improved layout
        output_card = ModernComponents.create_card_frame(content)
        output_card.pack(fill=tk.X)
        
        card_content = ttk.Frame(output_card, style='Card.TFrame')
        card_content.pack(fill=tk.X, padx=25, pady=25)
        card_content.columnconfigure(1, weight=1)
        
        # Title
        ModernComponents.create_modern_label(
            card_content, "File Output Settings", style='Heading.TLabel'
        ).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 20))
        
        # Auto-save checkbox with better spacing
        self.auto_save_var = tk.BooleanVar()
        auto_save_check = ttk.Checkbutton(
            card_content, text="Automatically save transcriptions to file",
            variable=self.auto_save_var, style='Modern.TCheckbutton'
        )
        auto_save_check.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=(5, 15))
        
        # Save directory with improved layout
        ModernComponents.create_modern_label(
            card_content, "Save Directory:", style='Dark.TLabel'
        ).grid(row=2, column=0, sticky=tk.W, pady=(5, 10))
        
        self.save_dir_var = tk.StringVar()
        dir_entry = ModernComponents.create_modern_entry(
            card_content, textvariable=self.save_dir_var, state="readonly", width=40
        )
        dir_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(15, 10), pady=(5, 10))
        
        browse_btn = ModernComponents.create_modern_button(
            card_content, "Browse...", command=self._browse_save_directory,
            style='Secondary.TButton'
        )
        browse_btn.grid(row=2, column=2, pady=(5, 10))
        
        # File format with descriptions
        ModernComponents.create_modern_label(
            card_content, "File Format:", style='Dark.TLabel'
        ).grid(row=3, column=0, sticky=tk.W, pady=(5, 10))
        
        self.file_format_var = tk.StringVar()
        format_combo = ttk.Combobox(
            card_content, textvariable=self.file_format_var,
            values=["txt (Plain Text)", "md (Markdown)", "rtf (Rich Text Format)"],
            state="readonly", style='Modern.TCombobox', width=30
        )
        format_combo.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=(15, 0), pady=(5, 10))
        
        # Info section
        info_frame = ttk.Frame(card_content, style='Card.TFrame')
        info_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(15, 0))
        
        info_icon = ModernComponents.create_modern_label(
            info_frame, "💡", style='Status.TLabel'
        )
        info_icon.pack(side=tk.LEFT, anchor=tk.N, padx=(0, 10))
        
        info_text = ModernComponents.create_modern_label(
            info_frame,
            "When auto-save is enabled, transcriptions will be automatically saved\n"
            "with timestamps in the specified directory. You can still manually save anytime.",
            style='Muted.TLabel'
        )
        info_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
    def _create_ui_tab(self) -> None:
        """Create the UI settings tab."""
        frame = ttk.Frame(self.notebook, style='Dark.TFrame')
        self.notebook.add(frame, text="🎨 Interface")
        
        content = ttk.Frame(frame, style='Dark.TFrame')
        content.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        content.columnconfigure(0, weight=1)
        
        # Interface card with improved layout
        ui_card = ModernComponents.create_card_frame(content)
        ui_card.pack(fill=tk.X, pady=(0, 20))
        
        card_content = ttk.Frame(ui_card, style='Card.TFrame')
        card_content.pack(fill=tk.X, padx=25, pady=25)
        card_content.columnconfigure(1, weight=1)
        
        # Title
        ModernComponents.create_modern_label(
            card_content, "Interface Settings", style='Heading.TLabel'
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 20))
        
        # Theme selection
        ModernComponents.create_modern_label(
            card_content, "Theme:", style='Dark.TLabel'
        ).grid(row=1, column=0, sticky=tk.W, pady=(5, 10))
        
        self.theme_var = tk.StringVar()
        theme_combo = ttk.Combobox(
            card_content, textvariable=self.theme_var,
            values=["Dark (Current)", "Light (Coming Soon)"],
            state="readonly", style='Modern.TCombobox', width=30
        )
        theme_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(15, 0), pady=(5, 10))
        
        # Default window size
        ModernComponents.create_modern_label(
            card_content, "Default Window Size:", style='Dark.TLabel'
        ).grid(row=2, column=0, sticky=tk.W, pady=(5, 10))
        
        self.geometry_var = tk.StringVar()
        geometry_combo = ttk.Combobox(
            card_content, textvariable=self.geometry_var,
            values=["800x600 (Small)", "900x700 (Medium)", "1000x800 (Large)", "1200x900 (Extra Large - Default)"],
            state="readonly", style='Modern.TCombobox', width=30
        )
        geometry_combo.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=(15, 0), pady=(5, 10))
        
        # Advanced section with better layout
        advanced_card = ModernComponents.create_card_frame(content)
        advanced_card.pack(fill=tk.X)
        
        advanced_content = ttk.Frame(advanced_card, style='Card.TFrame')
        advanced_content.pack(fill=tk.X, padx=25, pady=25)
        
        # Title
        ModernComponents.create_modern_label(
            advanced_content, "Advanced Options", style='Heading.TLabel'
        ).pack(anchor=tk.W, pady=(0, 20))
        
        # Button grid with descriptions
        button_grid = ttk.Frame(advanced_content, style='Card.TFrame')
        button_grid.pack(fill=tk.X)
        button_grid.columnconfigure(1, weight=1)
        
        # Export settings
        export_btn = ModernComponents.create_modern_button(
            button_grid, "📤 Export Settings", command=self._export_settings,
            style='Secondary.TButton'
        )
        export_btn.grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        
        export_desc = ModernComponents.create_modern_label(
            button_grid, "Save all settings to a backup file", style='Muted.TLabel'
        )
        export_desc.grid(row=0, column=1, sticky=tk.W, padx=(15, 0), pady=(0, 10))
        
        # Import settings
        import_btn = ModernComponents.create_modern_button(
            button_grid, "📥 Import Settings", command=self._import_settings,
            style='Secondary.TButton'
        )
        import_btn.grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        
        import_desc = ModernComponents.create_modern_label(
            button_grid, "Load settings from a backup file", style='Muted.TLabel'
        )
        import_desc.grid(row=1, column=1, sticky=tk.W, padx=(15, 0), pady=(0, 10))
        
        # Reset to defaults
        reset_btn = ModernComponents.create_modern_button(
            button_grid, "🔄 Reset to Defaults", command=self._reset_to_defaults,
            style='Secondary.TButton'
        )
        reset_btn.grid(row=2, column=0, sticky=tk.W)
        
        reset_desc = ModernComponents.create_modern_label(
            button_grid, "Restore all settings to their default values", style='Muted.TLabel'
        )
        reset_desc.grid(row=2, column=1, sticky=tk.W, padx=(15, 0))
        
    def _create_button_frame(self, parent: ttk.Frame) -> None:
        """Create the dialog button frame with improved layout."""
        button_frame = ttk.Frame(parent, style='Dark.TFrame')
        button_frame.grid(row=2, column=0, sticky="ew", pady=(30, 0))
        
        # Button container
        button_container = ttk.Frame(button_frame, style='Dark.TFrame')
        button_container.pack(fill=tk.X)
        
        # Right-aligned buttons with better spacing
        ok_btn = ModernComponents.create_modern_button(
            button_container, "✓ OK", command=self._on_ok,
            style='Modern.TButton'
        )
        ok_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        apply_btn = ModernComponents.create_modern_button(
            button_container, "Apply", command=self._on_apply,
            style='Secondary.TButton'
        )
        apply_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        cancel_btn = ModernComponents.create_modern_button(
            button_container, "Cancel", command=self._on_cancel,
            style='Secondary.TButton'  
        )
        cancel_btn.pack(side=tk.RIGHT)
    
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
        
        # Audio settings with new format mapping
        audio_settings = settings.get_audio_settings()
        sample_rate = audio_settings.get("sample_rate", 44100)
        sample_rate_map = {
            8000: "8000 Hz (Low quality)",
            16000: "16000 Hz (Good for speech)", 
            22050: "22050 Hz",
            44100: "44100 Hz (CD quality)",
            48000: "48000 Hz (Professional)"
        }
        self.sample_rate_var.set(sample_rate_map.get(sample_rate, f"{sample_rate} Hz"))
        
        channels = audio_settings.get("channels", 1)
        channels_map = {1: "1 (Mono - Recommended)", 2: "2 (Stereo)"}
        self.channels_var.set(channels_map.get(channels, f"{channels} (Mono)" if channels == 1 else f"{channels} (Stereo)"))
        
        chunk_size = audio_settings.get("chunk_size", 1024)
        chunk_map = {
            512: "512 (Low latency)",
            1024: "1024 (Recommended)",
            2048: "2048 (High latency)",
            4096: "4096 (Very high latency)"
        }
        self.chunk_size_var.set(chunk_map.get(chunk_size, f"{chunk_size}"))
        
        # Voice threshold
        self.voice_threshold_var.set(audio_settings.get("voice_threshold", 0.02))
        
        # Output settings with new format mapping
        output_settings = settings.get_output_settings()
        self.auto_save_var.set(output_settings.get("auto_save", False))
        self.save_dir_var.set(output_settings.get("save_directory", ""))
        
        file_format = output_settings.get("file_format", "txt")
        format_map = {
            "txt": "txt (Plain Text)",
            "md": "md (Markdown)",
            "rtf": "rtf (Rich Text Format)"
        }
        self.file_format_var.set(format_map.get(file_format, f"{file_format}"))
        
        # UI settings with new format mapping
        ui_settings = settings.get_ui_settings()
        self.theme_var.set("Dark (Current)")
        
        geometry = ui_settings.get("window_geometry", "1200x900")
        geometry_map = {
            "800x600": "800x600 (Small)",
            "900x700": "900x700 (Medium)",
            "1000x800": "1000x800 (Large)",
            "1200x900": "1200x900 (Extra Large)"
        }
        self.geometry_var.set(geometry_map.get(geometry, geometry))
    
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
            
            # Save audio settings - extract actual values from formatted strings
            sample_rate_text = self.sample_rate_var.get()
            sample_rate = int(sample_rate_text.split()[0])  # Extract number from "44100 Hz (CD quality)"
            settings.set("audio.sample_rate", sample_rate)
            
            channels_text = self.channels_var.get()
            channels = 1 if "1 (" in channels_text else 2
            settings.set("audio.channels", channels)
            
            chunk_text = self.chunk_size_var.get()
            chunk_size = int(chunk_text.split()[0])  # Extract number from "1024 (Recommended)"
            settings.set("audio.chunk_size", chunk_size)
            
            settings.set("audio.voice_threshold", self.voice_threshold_var.get())
            
            # Save output settings - extract actual values
            settings.set("output.auto_save", self.auto_save_var.get())
            settings.set("output.save_directory", self.save_dir_var.get())
            
            format_text = self.file_format_var.get()
            file_format = format_text.split()[0]  # Extract "txt" from "txt (Plain Text)"
            settings.set("output.file_format", file_format)
            
            # Save UI settings - extract actual values
            geometry_text = self.geometry_var.get()
            if "(" in geometry_text:
                geometry = geometry_text.split()[0]  # Extract "1200x900" from "1200x900 (Extra Large)"
            else:
                geometry = geometry_text
            settings.set("ui.window_geometry", geometry)
            
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