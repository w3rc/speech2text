"""Modern dark theme styling for Speech2Text application."""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any
import sys
import platform


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
        
        # Apply after window is fully created
        root.after(100, lambda: cls._apply_system_dark_mode(root))
    
    @classmethod
    def _apply_system_dark_mode(cls, root: tk.Tk) -> None:
        """Apply system-level dark mode styling."""
        if platform.system() == 'Windows':
            try:
                import ctypes
                from ctypes import wintypes
                
                hwnd = int(root.winfo_id())
                
                # Multiple approaches to force dark mode
                
                # Method 1: DWMWA_USE_IMMERSIVE_DARK_MODE (Windows 10 build 18985+)
                try:
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        hwnd, 20, ctypes.byref(ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int)
                    )
                except:
                    pass
                
                # Method 2: DWMWA_USE_IMMERSIVE_DARK_MODE_BEFORE_20H1 (older Windows 10)
                try:
                    ctypes.windll.dwmapi.DwmSetWindowAttribute(
                        hwnd, 19, ctypes.byref(ctypes.c_int(1)), ctypes.sizeof(ctypes.c_int)
                    )
                except:
                    pass
                
                # Method 3: Set window theme to dark
                try:
                    # Set dark theme
                    ctypes.windll.uxtheme.SetWindowTheme(hwnd, "DarkMode_Explorer", None)
                except:
                    pass
                
                # Method 4: Registry-based approach
                try:
                    import winreg
                    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                       r"SOFTWARE\Microsoft\Windows\CurrentVersion\Themes\Personalize")
                    winreg.SetValueEx(key, "AppsUseLightTheme", 0, winreg.REG_DWORD, 0)
                    winreg.CloseKey(key)
                except:
                    pass
                
            except Exception:
                pass  # Silently fail if not supported
    
    @classmethod
    def _configure_ttk_styles(cls, style: ttk.Style) -> None:
        """Configure all ttk widget styles."""
        
        # Frame styles
        style.configure('Dark.TFrame',
                       background=cls.COLORS['bg_primary'],
                       relief='flat',
                       borderwidth=0)
        
        style.configure('Card.TFrame',
                       background=cls.COLORS['bg_secondary'],
                       relief='flat',
                       borderwidth=1)
        
        # Label styles
        style.configure('Dark.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body'])
        
        style.configure('Heading.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['heading'])
        
        style.configure('HeadingLarge.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['heading_large'])
        
        style.configure('Muted.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_muted'],
                       font=cls.FONTS['caption'])
        
        style.configure('Status.TLabel',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_secondary'],
                       font=cls.FONTS['body_bold'])
        
        # Button styles (modern black and white)
        style.configure('Modern.TButton',
                       background=cls.COLORS['accent_primary'],
                       foreground=cls.COLORS['bg_primary'],
                       font=cls.FONTS['body_bold'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(16, 8))
        
        style.map('Modern.TButton',
                 background=[('active', cls.COLORS['accent_hover']),
                           ('pressed', cls.COLORS['accent_active'])])
        
        style.configure('Secondary.TButton',
                       background=cls.COLORS['bg_glass'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body'],
                       borderwidth=1,
                       focuscolor='none',
                       relief='flat',
                       padding=(12, 6))
        
        style.map('Secondary.TButton',
                 background=[('active', cls.COLORS['bg_hover']),
                           ('pressed', cls.COLORS['bg_active'])],
                 bordercolor=[('focus', cls.COLORS['border_focus'])])
        
        # Record button (modern styled)
        style.configure('Record.TButton',
                       background=cls.COLORS['success'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body_bold'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 12))
        
        style.map('Record.TButton',
                 background=[('active', '#1f6feb'),
                           ('pressed', '#0550ae')])
        
        style.configure('Recording.TButton',
                       background=cls.COLORS['error'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body_bold'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 12))
        
        style.map('Recording.TButton',
                 background=[('active', '#f85149'),
                           ('pressed', '#da3633')])
        
        # Scrollbar styles
        style.configure('Modern.Vertical.TScrollbar',
                       background=cls.COLORS['bg_secondary'],
                       troughcolor=cls.COLORS['bg_primary'],
                       borderwidth=0,
                       arrowcolor=cls.COLORS['text_muted'],
                       darkcolor=cls.COLORS['bg_secondary'],
                       lightcolor=cls.COLORS['bg_secondary'])
        
        style.map('Modern.Vertical.TScrollbar',
                 background=[('active', cls.COLORS['bg_hover']),
                           ('pressed', cls.COLORS['bg_active'])])
        
        # Entry and text widget styles
        style.configure('Modern.TEntry',
                       fieldbackground=cls.COLORS['bg_tertiary'],
                       background=cls.COLORS['bg_tertiary'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=1,
                       insertcolor=cls.COLORS['accent_primary'],
                       font=cls.FONTS['body'])
        
        style.map('Modern.TEntry',
                 bordercolor=[('focus', cls.COLORS['border_focus'])])
        
        # Notebook styles for settings
        style.configure('Modern.TNotebook',
                       background=cls.COLORS['bg_primary'],
                       borderwidth=0)
        
        style.configure('Modern.TNotebook.Tab',
                       background=cls.COLORS['bg_tertiary'],
                       foreground=cls.COLORS['text_secondary'],
                       padding=(16, 8),
                       font=cls.FONTS['body'])
        
        style.map('Modern.TNotebook.Tab',
                 background=[('selected', cls.COLORS['accent_primary'])],
                 foreground=[('selected', cls.COLORS['bg_primary'])])


class ModernComponents:
    """Factory for creating modern styled components."""
    
    @staticmethod
    def create_card_frame(parent: tk.Widget, **kwargs) -> tk.Frame:
        """Create a modern card-style frame."""
        frame = tk.Frame(parent, 
                        bg=DarkTheme.COLORS['bg_secondary'],
                        relief='flat',
                        bd=1,
                        highlightbackground=DarkTheme.COLORS['border'],
                        highlightthickness=1,
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
        
        # Modern bar design
        self.center_x = size // 2
        self.center_y = size // 2
        self.num_bars = 20
        self.bar_width = 3
        self.bar_spacing = 8
        self.max_bar_height = 60
        
        # Colors
        self.bg_color = DarkTheme.COLORS['bg_primary']
        self.bar_color = DarkTheme.COLORS['audio_mid']
        self.active_color = DarkTheme.COLORS['accent_primary']
        self.voice_color = DarkTheme.COLORS['text_primary']
        
        # Animation properties
        self.bar_heights = [0] * self.num_bars
        self.target_heights = [0] * self.num_bars
        self.pulse_alpha = 0.0
        
        self.bind('<Configure>', self._on_resize)
        self._animate()
        
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
            self.itemconfig(self.circle, fill=DarkTheme.COLORS['text_muted'])
        elif self.status == 'recording':
            self._animate_recording()
        elif self.status == 'processing':
            self._animate_processing()
        elif self.status == 'error':
            self.itemconfig(self.circle, fill=DarkTheme.COLORS['error'])
    
    def _animate_recording(self) -> None:
        """Animate recording status with pulsing blue."""
        import math
        alpha = (math.sin(self.animation_step * 0.3) + 1) / 2
        # Simple pulsing effect by alternating colors
        if self.animation_step % 20 < 10:
            color = DarkTheme.COLORS['success']  # Blue
        else:
            color = '#1f6feb'  # Lighter blue
        
        self.itemconfig(self.circle, fill=color)
        self.animation_step += 1
        self.animation_id = self.after(100, self._animate_recording)
    
    def _animate_processing(self) -> None:
        """Animate processing status with rotating effect."""
        # Simple color cycling for processing
        colors = [DarkTheme.COLORS['info'], '#1f6feb', '#0969da']
        color = colors[self.animation_step % len(colors)]
        
        self.itemconfig(self.circle, fill=color)
        self.animation_step += 1
        self.animation_id = self.after(200, self._animate_processing)


class ActivityHistoryPanel(tk.Frame):
    """Modern activity history panel showing recent transcription activities."""
    
    def __init__(self, parent: tk.Widget, width: int = 300, **kwargs):
        super().__init__(parent, bg=DarkTheme.COLORS['bg_secondary'], **kwargs)
        
        self.width = width
        self.configure(width=width)
        
        # Header
        header_frame = tk.Frame(self, bg=DarkTheme.COLORS['bg_secondary'])
        header_frame.pack(fill='x', padx=20, pady=(20, 10))
        
        header_label = tk.Label(header_frame, 
                               text="Activity History",
                               bg=DarkTheme.COLORS['bg_secondary'],
                               fg=DarkTheme.COLORS['text_primary'],
                               font=DarkTheme.FONTS['heading'])
        header_label.pack(side='left')
        
        # Scrollable content area
        self.content_frame = tk.Frame(self, bg=DarkTheme.COLORS['bg_secondary'])
        self.content_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))
        
        # Initially empty
        self.activities = []
        self._update_display()
    
    def add_activity(self, text: str, timestamp: str = None) -> None:
        """Add a new activity to the history."""
        import datetime
        
        if timestamp is None:
            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        activity = {
            'text': text[:100] + '...' if len(text) > 100 else text,
            'timestamp': timestamp,
            'full_text': text
        }
        
        self.activities.insert(0, activity)  # Add to beginning
        
        # Keep only last 10 activities
        if len(self.activities) > 10:
            self.activities = self.activities[:10]
        
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
                                  bg=DarkTheme.COLORS['bg_secondary'],
                                  fg=DarkTheme.COLORS['text_muted'],
                                  font=DarkTheme.FONTS['caption'])
            empty_label.pack(pady=20)
            return
        
        # Display activities
        for i, activity in enumerate(self.activities):
            activity_frame = tk.Frame(self.content_frame, 
                                    bg=DarkTheme.COLORS['bg_tertiary'],
                                    relief='flat', bd=1)
            activity_frame.pack(fill='x', pady=(0, 5))
            
            # Timestamp
            timestamp_label = tk.Label(activity_frame,
                                     text=activity['timestamp'],
                                     bg=DarkTheme.COLORS['bg_tertiary'],
                                     fg=DarkTheme.COLORS['text_muted'],
                                     font=DarkTheme.FONTS['caption'])
            timestamp_label.pack(anchor='w', padx=10, pady=(5, 0))
            
            # Text preview
            text_label = tk.Label(activity_frame,
                                text=activity['text'],
                                bg=DarkTheme.COLORS['bg_tertiary'],
                                fg=DarkTheme.COLORS['text_secondary'],
                                font=DarkTheme.FONTS['body'],
                                wraplength=self.width-40,
                                justify='left')
            text_label.pack(anchor='w', padx=10, pady=(0, 5))