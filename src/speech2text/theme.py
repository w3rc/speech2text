"""Modern dark theme styling for Speech2Text application."""

import tkinter as tk
from tkinter import ttk


class DarkTheme:
    """Modern black and white themed dark theme with sleek styling."""
    
    # Color palette - Modern Black & White theme
    COLORS = {
        # Background colors - Modern grays and blacks
        'bg_primary': '#0d1117',      # GitHub dark background
        'bg_secondary': '#161b22',    # Slightly lighter panels
        'bg_tertiary': '#21262d',     # Raised elements
        'bg_hover': '#30363d',        # Hover states
        'bg_active': '#484f58',       # Active states
        'bg_glass': '#161b22',        # Semi-transparent backgrounds
        
        # Text colors - High contrast whites and grays
        'text_primary': '#ffffff',     # Pure white primary text
        'text_secondary': '#f0f6fc',   # Slightly dimmed secondary
        'text_muted': '#8b949e',       # Muted gray text
        'text_disabled': '#484f58',    # Disabled gray text
        
        # Monochrome accent colors
        'accent_primary': '#ffffff',   # White primary accent
        'accent_hover': '#f0f6fc',     # Light gray hover
        'accent_active': '#e6edf3',    # Darker gray active
        'accent_glow': '#30363d',      # Subtle glow effect
        
        # Status colors - Modern grays and blues (no green)
        'success': '#0969da',          # Blue instead of green
        'warning': '#9e6a03',          # Subtle orange
        'error': '#da3633',            # Subtle red
        'info': '#0969da',             # Subtle blue
        
        # Audio visualization - Grayscale gradient
        'audio_low': '#6e7681',        # Light gray for low
        'audio_mid': '#f0f6fc',        # White for medium
        'audio_high': '#ffffff',       # Pure white for high
        'audio_peak': '#ffffff',       # White for peaks
        
        # Borders - Subtle grays
        'border': '#30363d',           # Subtle border
        'border_focus': '#ffffff',     # White focused border
        'border_glow': '#21262d',      # Subtle glow
        'shadow': '#010409',           # Deep shadow
    }
    
    # Typography
    FONTS = {
        'heading_large': ('Segoe UI', 18, 'bold'),
        'heading': ('Segoe UI', 14, 'bold'),
        'body_bold': ('Segoe UI', 10, 'bold'),
        'body': ('Segoe UI', 10),
        'caption': ('Segoe UI', 9),
        'code': ('Consolas', 9),
    }
    
    @classmethod
    def apply_theme(cls, root: tk.Tk) -> None:
        """Apply the dark theme to the application."""
        # Configure root window
        root.configure(bg=cls.COLORS['bg_primary'])
        
        # Create and configure ttk style
        style = ttk.Style()
        
        # Configure the theme
        style.theme_use('clam')  # Use clam as base theme
        
        # Configure ttk styles
        cls._configure_ttk_styles(style)
        
    
    @classmethod
    def _configure_ttk_styles(cls, style: ttk.Style) -> None:
        """Configure all ttk widget styles."""
        
        # Frame styles - seamless, no borders
        style.configure('Dark.TFrame',
                       background=cls.COLORS['bg_primary'],
                       relief='flat',
                       borderwidth=0)
        
        style.configure('Card.TFrame',
                       background=cls.COLORS['bg_primary'],
                       relief='flat',
                       borderwidth=0)
        
        # Label styles - seamless backgrounds
        style.configure('Dark.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body'],
                       relief='flat',
                       borderwidth=0)
        
        style.configure('Heading.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['heading'],
                       relief='flat',
                       borderwidth=0)
        
        style.configure('HeadingLarge.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['heading_large'],
                       relief='flat',
                       borderwidth=0)
        
        style.configure('Muted.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_muted'],
                       font=cls.FONTS['caption'],
                       relief='flat',
                       borderwidth=0)
        
        style.configure('Status.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_secondary'],
                       font=cls.FONTS['body_bold'],
                       relief='flat',
                       borderwidth=0)
        
        # Button styles - seamless, no borders
        style.configure('Modern.TButton',
                       background=cls.COLORS['text_muted'],
                       foreground=cls.COLORS['bg_primary'],
                       font=cls.FONTS['body_bold'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(16, 8))
        
        style.map('Modern.TButton',
                 background=[('active', cls.COLORS['text_secondary']),
                           ('pressed', cls.COLORS['text_primary'])])
        
        style.configure('Secondary.TButton',
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(12, 6))
        
        style.map('Secondary.TButton',
                 background=[('active', cls.COLORS['bg_tertiary']),
                           ('pressed', cls.COLORS['bg_hover'])])
        
        # Record button - seamless, subtle styling
        style.configure('Record.TButton',
                       background=cls.COLORS['bg_tertiary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body_bold'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 12))
        
        style.map('Record.TButton',
                 background=[('active', cls.COLORS['bg_hover']),
                           ('pressed', cls.COLORS['bg_active'])])
        
        style.configure('Recording.TButton',
                       background=cls.COLORS['bg_hover'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body_bold'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 12))
        
        style.map('Recording.TButton',
                 background=[('active', cls.COLORS['bg_active']),
                           ('pressed', cls.COLORS['bg_tertiary'])])
        
        # Scrollbar styles - seamless
        style.configure('Modern.Vertical.TScrollbar',
                       background=cls.COLORS['bg_primary'],
                       troughcolor=cls.COLORS['bg_primary'],
                       borderwidth=0,
                       arrowcolor=cls.COLORS['text_muted'],
                       darkcolor=cls.COLORS['bg_primary'],
                       lightcolor=cls.COLORS['bg_primary'],
                       relief='flat')
        
        style.map('Modern.Vertical.TScrollbar',
                 background=[('active', cls.COLORS['bg_secondary']),
                           ('pressed', cls.COLORS['bg_tertiary'])])
        
        # Entry and text widget styles - seamless
        style.configure('Modern.TEntry',
                       fieldbackground=cls.COLORS['bg_secondary'],
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=0,
                       insertcolor=cls.COLORS['text_primary'],
                       relief='flat',
                       font=cls.FONTS['body'])
        
        style.map('Modern.TEntry',
                 fieldbackground=[('focus', cls.COLORS['bg_tertiary'])])
        
        # Notebook styles for settings - seamless tabs with subtle underline
        style.configure('Modern.TNotebook',
                       background=cls.COLORS['bg_primary'],
                       borderwidth=0,
                       relief='flat')
        
        style.configure('Modern.TNotebook.Tab',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_secondary'],
                       padding=(16, 12),
                       font=cls.FONTS['body'],
                       borderwidth=0,
                       relief='flat')
        
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', cls.COLORS['bg_primary'])],
                 foreground=[('selected', cls.COLORS['text_primary'])])
        
        # Add a subtle bottom border for selected tabs
        style.configure('Modern.TNotebook.Tab',
                       borderwidth=0,
                       relief='flat')
        
        style.map('Modern.TNotebook.Tab',
                 bordercolor=[('selected', cls.COLORS['text_muted'])],
                 borderwidth=[('selected', 1)],
                 relief=[('selected', 'flat')])
        
        # Add combobox styles - seamless appearance with proper hover states
        style.configure('Modern.TCombobox',
                       fieldbackground=cls.COLORS['bg_secondary'],
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=0,
                       relief='flat',
                       font=cls.FONTS['body'],
                       arrowcolor=cls.COLORS['text_primary'],
                       insertcolor=cls.COLORS['text_primary'])
        
        style.map('Modern.TCombobox',
                 fieldbackground=[('focus', cls.COLORS['bg_tertiary']),
                                ('active', cls.COLORS['bg_hover']),
                                ('readonly', cls.COLORS['bg_secondary'])],
                 background=[('focus', cls.COLORS['bg_tertiary']),
                           ('active', cls.COLORS['bg_hover']),
                           ('readonly', cls.COLORS['bg_secondary'])],
                 foreground=[('focus', cls.COLORS['text_primary']),
                           ('active', cls.COLORS['text_primary']),
                           ('readonly', cls.COLORS['text_primary'])],
                 arrowcolor=[('focus', cls.COLORS['text_primary']),
                           ('active', cls.COLORS['text_primary'])])
        
        # Add checkbutton styles - seamless
        style.configure('Modern.TCheckbutton',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body'],
                       focuscolor='none',
                       borderwidth=0,
                       relief='flat')
        
        style.map('Modern.TCheckbutton',
                 background=[('active', cls.COLORS['bg_primary'])])
        
        # Add separator styles - seamless
        style.configure('TSeparator',
                       background=cls.COLORS['bg_secondary'],
                       borderwidth=0,
                       relief='flat')
        
        # Add scale styles - seamless
        style.configure('TScale',
                       background=cls.COLORS['bg_primary'],
                       troughcolor=cls.COLORS['bg_secondary'],
                       borderwidth=0,
                       relief='flat')
        
        style.map('TScale',
                 background=[('active', cls.COLORS['bg_primary'])])


class ModernComponents:
    """Factory for creating modern styled components."""
    
    @staticmethod
    def create_card_frame(parent: tk.Widget, **kwargs) -> tk.Frame:
        """Create a seamless card-style frame that blends with background."""
        frame = tk.Frame(parent, 
                        bg=DarkTheme.COLORS['bg_primary'],
                        relief='flat',
                        bd=0,
                        highlightthickness=0,
                        **kwargs)
        return frame
    
    @staticmethod
    def create_modern_button(parent: tk.Widget, text: str, command=None, style='Modern.TButton', **kwargs) -> ttk.Button:
        """Create a modern styled button."""
        return ttk.Button(parent, text=text, command=command, style=style, **kwargs)
    
    @staticmethod
    def create_modern_entry(parent: tk.Widget, **kwargs) -> ttk.Entry:
        """Create a modern styled entry."""
        return ttk.Entry(parent, style='Modern.TEntry', **kwargs)
    
    @staticmethod
    def create_modern_label(parent: tk.Widget, text: str, style='Dark.TLabel', **kwargs) -> ttk.Label:
        """Create a modern styled label."""
        return ttk.Label(parent, text=text, style=style, **kwargs)


class AudioLevelMeter(tk.Canvas):
    """Modern minimalist audio visualization with clean bars."""
    
    def __init__(self, parent: tk.Widget, size: int = 200, **kwargs):
        super().__init__(parent, width=size, height=size, 
                        bg=DarkTheme.COLORS['bg_primary'],
                        highlightthickness=0, **kwargs)
        
        self.size = size
        self.level = 0.0
        self.peak_level = 0.0
        self.voice_detected = False
        self.animation_frame = 0
        self.current_status = 'idle'  # Track current status for color changes
        
        # Modern bar design
        self.center_x = size // 2
        self.center_y = size // 2
        self.num_bars = 20
        self.bar_width = 3
        self.bar_spacing = 8
        self.max_bar_height = 60
        
        # Base colors
        self.bg_color = DarkTheme.COLORS['bg_primary']
        
        # Status-based colors
        self.status_colors = {
            'idle': {
                'bar_color': '#ffffff',      # White for idle
                'active_color': '#ffffff',   # White for idle
                'voice_color': '#ffffff'     # White for idle
            },
            'recording': {
                'bar_color': '#00cc00',      # Green for recording
                'active_color': '#00ff00',   # Bright green for recording
                'voice_color': '#00ff00'     # Bright green for recording
            },
            'processing': {
                'bar_color': '#0080ff',      # Blue for processing
                'active_color': '#0066ff',   # Darker blue for processing
                'voice_color': '#0099ff'     # Light blue for processing
            }
        }
        
        # Set initial colors
        self._update_colors()
        
        # Animation properties
        self.bar_heights = [0] * self.num_bars
        self.target_heights = [0] * self.num_bars
        self.pulse_alpha = 0.0
        
        self.bind('<Configure>', self._on_resize)
        self._animate()
    
    def set_status(self, status: str) -> None:
        """Set the status and update colors accordingly."""
        if status in self.status_colors and status != self.current_status:
            self.current_status = status
            self._update_colors()
    
    def _update_colors(self) -> None:
        """Update colors based on current status."""
        colors = self.status_colors.get(self.current_status, self.status_colors['idle'])
        self.bar_color = colors['bar_color']
        self.active_color = colors['active_color'] 
        self.voice_color = colors['voice_color']
        
    def _on_resize(self, event):
        """Handle widget resize."""
        self.size = min(event.width, event.height)
        self.center_x = self.size // 2
        self.center_y = self.size // 2
        
    def update_level(self, level: float, voice_detected: bool = False):
        """Update the audio level display with modern bar animation."""
        self.level = max(0.0, min(1.0, level))
        self.voice_detected = voice_detected
        
        # Update peak with smooth decay
        if self.level > self.peak_level:
            self.peak_level = self.level
        else:
            self.peak_level *= 0.95
        
        # Update bar heights based on audio level
        import random
        import math
        
        # Create symmetric pattern from center outward
        center_bar = self.num_bars // 2
        
        for i in range(self.num_bars):
            # Distance from center (0 to 1)
            distance_from_center = abs(i - center_bar) / center_bar
            
            # Base height decreases from center
            base_multiplier = 1.0 - (distance_from_center * 0.6)
            
            # Add some randomness for natural feel
            if self.level > 0.05:
                variation = random.uniform(0.7, 1.3)
                # Add wave effect
                wave = math.sin((i / self.num_bars) * 4 * math.pi + self.animation_frame * 0.1) * 0.3 + 1.0
                base_multiplier *= variation * wave
            
            # Calculate target height
            target_height = self.level * self.max_bar_height * base_multiplier
            target_height = max(2, min(self.max_bar_height, target_height))
            
            self.target_heights[i] = target_height
            
    def _animate(self):
        """Clean modern animation with smooth bars."""
        self.animation_frame += 1
        
        # Smooth interpolation for bar heights
        for i in range(self.num_bars):
            current = self.bar_heights[i]
            target = self.target_heights[i]
            # Smooth interpolation
            self.bar_heights[i] = current + (target - current) * 0.25
        
        # Voice detection pulse
        if self.voice_detected:
            self.pulse_alpha = min(1.0, self.pulse_alpha + 0.1)
        else:
            self.pulse_alpha = max(0.0, self.pulse_alpha - 0.05)
        
        self._draw_modern_bars()
        self.after(33, self._animate)  # ~30 FPS
    
    def _draw_modern_bars(self):
        """Draw clean modern audio bars."""
        self.delete("all")
        
        if self.size <= 0:
            return
        
        # Calculate total width needed for bars
        total_width = (self.num_bars * self.bar_width) + ((self.num_bars - 1) * self.bar_spacing)
        start_x = (self.size - total_width) // 2
        
        # Draw bars
        for i in range(self.num_bars):
            x = start_x + i * (self.bar_width + self.bar_spacing)
            height = self.bar_heights[i]
            
            # Calculate y position (centered vertically)
            y1 = self.center_y - height // 2
            y2 = self.center_y + height // 2
            
            # Choose color based on height and voice detection
            if self.voice_detected and self.pulse_alpha > 0.5:
                color = self.voice_color
            elif height > self.max_bar_height * 0.7:
                color = self.active_color
            else:
                color = self.bar_color
            
            # Draw the bar
            self.create_rectangle(x, y1, x + self.bar_width, y2,
                                fill=color, outline="", width=0)
            
            # Add subtle glow effect for voice detection
            if self.voice_detected and self.pulse_alpha > 0:
                glow_alpha = int(self.pulse_alpha * 2)
                for g in range(1, glow_alpha + 1):
                    self.create_rectangle(x - g, y1 - g, x + self.bar_width + g, y2 + g,
                                        fill="", outline=DarkTheme.COLORS['accent_glow'], width=1)
        
        # Optional: Add level indicator text
        if self.level > 0.01:
            level_text = f"{int(self.level * 100)}%"
            self.create_text(self.center_x, self.center_y + self.max_bar_height + 20,
                           text=level_text, fill=DarkTheme.COLORS['text_muted'],
                           font=('Segoe UI', 9), anchor='center')


class StatusIndicator(tk.Canvas):
    """Modern status indicator with pulsing animation."""
    
    def __init__(self, parent: tk.Widget, size: int = 20, **kwargs):
        super().__init__(parent, width=size, height=size,
                        bg=DarkTheme.COLORS['bg_primary'],
                        highlightthickness=0, **kwargs)
        
        self.size = size
        self.status = 'idle'  # idle, recording, processing, error
        self.animation_step = 0
        self.animation_id = None
        
        # Create indicator circle
        margin = 2
        self.circle = self.create_oval(margin, margin, size-margin, size-margin,
                                     fill=DarkTheme.COLORS['text_muted'],
                                     outline='')
        
        self._update_status()
    
    def set_status(self, status: str) -> None:
        """Set the status (idle, recording, processing, error)."""
        if self.status != status:
            self.status = status
            self.animation_step = 0
            self._update_status()
    
    def _update_status(self) -> None:
        """Update the visual status."""
        if self.animation_id:
            self.after_cancel(self.animation_id)
        
        if self.status == 'idle':
            self.itemconfig(self.circle, fill='#ffffff')  # White for idle
        elif self.status == 'recording':
            self._animate_recording()
        elif self.status == 'processing':
            self._animate_processing()
        elif self.status == 'error':
            self.itemconfig(self.circle, fill=DarkTheme.COLORS['error'])
    
    def _animate_recording(self) -> None:
        """Animate recording status with pulsing green."""
        import math
        alpha = (math.sin(self.animation_step * 0.3) + 1) / 2
        # Simple pulsing effect by alternating green colors
        if self.animation_step % 20 < 10:
            color = '#00ff00'  # Bright green
        else:
            color = '#00cc00'  # Slightly darker green
        
        self.itemconfig(self.circle, fill=color)
        self.animation_step += 1
        self.animation_id = self.after(100, self._animate_recording)
    
    def _animate_processing(self) -> None:
        """Animate processing status with pulsing blue."""
        # Simple color cycling for processing with blue tones
        colors = ['#0066ff', '#0080ff', '#0099ff']  # Various blue shades
        color = colors[self.animation_step % len(colors)]
        
        self.itemconfig(self.circle, fill=color)
        self.animation_step += 1
        self.animation_id = self.after(200, self._animate_processing)


class ActivityHistoryPanel(tk.Frame):
    """Modern activity history panel showing recent transcription activities."""
    
    def __init__(self, parent: tk.Widget, width: int = 300, **kwargs):
        super().__init__(parent, bg=DarkTheme.COLORS['bg_primary'], **kwargs)
        
        self.width = width
        self.configure(width=width)
        self.storage_file = self._get_storage_path()
        
        # Header
        header_frame = tk.Frame(self, bg=DarkTheme.COLORS['bg_primary'])
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        header_label = tk.Label(header_frame, 
                               text="Activity History",
                               bg=DarkTheme.COLORS['bg_primary'],
                               fg=DarkTheme.COLORS['text_primary'],
                               font=DarkTheme.FONTS['heading'])
        header_label.pack(side='left')
        
        # Scrollable content area
        self.content_frame = tk.Frame(self, bg=DarkTheme.COLORS['bg_primary'])
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Load existing activities and initialize
        self.activities = []
        self._load_activities()
        self._update_display()
    
    def _get_storage_path(self) -> str:
        """Get the path for storing activity history."""
        import os
        import tempfile
        
        # Use user's data directory or temp directory
        if os.name == 'nt':  # Windows
            data_dir = os.path.expandvars(r'%APPDATA%\Speech2Text')
        else:  # macOS/Linux
            data_dir = os.path.expanduser('~/.speech2text')
        
        # Create directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        return os.path.join(data_dir, 'activity_history.json')
    
    def _load_activities(self) -> None:
        """Load activities from storage."""
        import json
        import os
        
        try:
            if os.path.exists(self.storage_file):
                with open(self.storage_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.activities = data.get('activities', [])
                    # Limit to recent activities
                    if len(self.activities) > 50:
                        self.activities = self.activities[:50]
        except Exception as e:
            print(f"Failed to load activity history: {e}")
            self.activities = []
    
    def _save_activities(self) -> None:
        """Save activities to storage."""
        import json
        
        try:
            data = {
                'activities': self.activities,
                'last_updated': str(__import__('datetime').datetime.now())
            }
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Failed to save activity history: {e}")
    
    def _copy_activity_to_clipboard(self, activity_text: str, button: tk.Button) -> None:
        """Copy individual activity text to clipboard."""
        try:
            import pyperclip
            pyperclip.copy(activity_text)
            
            # Visual feedback - briefly change button color
            original_bg = button['bg']
            button.config(bg=DarkTheme.COLORS['bg_hover'])
            self.after(200, lambda: button.config(bg=original_bg))
                
        except Exception as e:
            print(f"Failed to copy to clipboard: {e}")
    
    def add_activity(self, text: str, timestamp: str = None) -> None:
        """Add a new activity to the history."""
        import datetime
        
        if timestamp is None:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        activity = {
            'text': text[:100] + '...' if len(text) > 100 else text,
            'timestamp': timestamp,
            'full_text': text
        }
        
        self.activities.insert(0, activity)  # Add to beginning
        
        # Keep only last 50 activities in memory and storage
        if len(self.activities) > 50:
            self.activities = self.activities[:50]
        
        # Save to storage
        self._save_activities()
        
        self._update_display()
    
    def _update_display(self) -> None:
        """Update the display of activities."""
        # Clear existing widgets
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        if not self.activities:
            # Show empty state
            empty_label = tk.Label(self.content_frame,
                                  text="No recent activity",
                                  bg=DarkTheme.COLORS['bg_primary'],
                                  fg=DarkTheme.COLORS['text_muted'],
                                  font=DarkTheme.FONTS['caption'])
            empty_label.pack(pady=20)
            return
        
        # Display activities - seamless design with copy buttons
        for i, activity in enumerate(self.activities):
            activity_frame = tk.Frame(self.content_frame, 
                                    bg=DarkTheme.COLORS['bg_secondary'],
                                    relief='flat', bd=0)
            activity_frame.pack(fill='x', pady=(0, 8))
            
            # Header row with timestamp and copy button
            header_frame = tk.Frame(activity_frame, bg=DarkTheme.COLORS['bg_secondary'])
            header_frame.pack(fill='x', padx=12, pady=(8, 0))
            
            # Timestamp
            timestamp_label = tk.Label(header_frame,
                                     text=activity['timestamp'],
                                     bg=DarkTheme.COLORS['bg_secondary'],
                                     fg=DarkTheme.COLORS['text_muted'],
                                     font=DarkTheme.FONTS['caption'])
            timestamp_label.pack(side='left')
            
            # Copy button for this activity
            copy_btn = tk.Button(header_frame,
                                text="📋",
                                bg=DarkTheme.COLORS['bg_tertiary'], 
                                fg=DarkTheme.COLORS['text_muted'],
                                activebackground=DarkTheme.COLORS['bg_hover'],
                                activeforeground=DarkTheme.COLORS['text_primary'],
                                font=('Segoe UI', 10),
                                relief='flat',
                                borderwidth=0,
                                padx=6,
                                pady=2,
                                command=lambda text=activity['full_text'], btn=None: 
                                        self._copy_activity_to_clipboard(text, btn))
            copy_btn.pack(side='right')
            
            # Update the lambda to capture the button reference correctly
            copy_btn.config(command=lambda text=activity['full_text'], btn=copy_btn: 
                           self._copy_activity_to_clipboard(text, btn))
            
            # Text preview
            text_label = tk.Label(activity_frame,
                                text=activity['text'],
                                bg=DarkTheme.COLORS['bg_secondary'],
                                fg=DarkTheme.COLORS['text_secondary'],
                                font=DarkTheme.FONTS['body'],
                                wraplength=self.width-40,
                                justify='left')
            text_label.pack(anchor='w', padx=12, pady=(4, 8))