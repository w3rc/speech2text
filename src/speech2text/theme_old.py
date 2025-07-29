"""Modern dark theme styling for Speech2Text application."""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any
import sys
import platform


class DarkTheme:
    """Modern neon-themed dark theme with sleek styling."""
    
    # Color palette - Modern Black & White theme
    COLORS = {
        # Background colors - Modern grays and blacks
        'bg_primary': '#0d1117',      # GitHub dark background
        'bg_secondary': '#161b22',    # Slightly lighter panels
        'bg_tertiary': '#21262d',     # Raised elements
        'bg_hover': '#30363d',        # Hover states
        'bg_active': '#484f58',       # Active states
        'bg_glass': '#161b2280',      # Semi-transparent backgrounds
        
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
        
        # Status colors - Monochrome with subtle tints
        'success': '#238636',          # Subtle green
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
        'body': ('Segoe UI', 10),
        'body_bold': ('Segoe UI', 10, 'bold'),
        'caption': ('Segoe UI', 9),
        'monospace': ('Consolas', 10),
    }
    
    # Dimensions
    DIMENSIONS = {
        'padding_small': 8,
        'padding_medium': 16,
        'padding_large': 24,
        'border_radius': 8,
        'button_height': 36,
        'input_height': 32,
    }
    
    @classmethod
    def apply_to_root(cls, root: tk.Tk) -> None:
        """Apply dark theme to root window."""
        root.configure(bg=cls.COLORS['bg_primary'])
        
        # Apply dark title bar on Windows
        cls._apply_dark_title_bar(root)
        
        # Configure ttk styles
        style = ttk.Style()
        
        # Configure theme
        style.theme_use('clam')
        
        # Frame styles
        style.configure('Dark.TFrame', 
                       background=cls.COLORS['bg_primary'],
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
        
        # Button styles (neon themed)
        style.configure('Modern.TButton',
                       background=cls.COLORS['accent_primary'],
                       foreground=cls.COLORS['bg_primary'],
                       font=cls.FONTS['body_bold'],
                       borderwidth=2,
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
        
        # Record button (neon styled)
        style.configure('Record.TButton',
                       background=cls.COLORS['neon_green'],
                       foreground=cls.COLORS['bg_primary'],
                       font=cls.FONTS['body_bold'],
                       borderwidth=2,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 12))
        
        style.map('Record.TButton',
                 background=[('active', cls.COLORS['success']),
                           ('pressed', '#33ff33')])
        
        style.configure('Recording.TButton',
                       background=cls.COLORS['neon_pink'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body_bold'],
                       borderwidth=2,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 12))
        
        style.map('Recording.TButton',
                 background=[('active', cls.COLORS['error']),
                           ('pressed', '#ff3366')])
        
        # Entry styles
        style.configure('Modern.TEntry',
                       fieldbackground=cls.COLORS['bg_tertiary'],
                       background=cls.COLORS['bg_tertiary'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=1,
                       insertcolor=cls.COLORS['text_primary'],
                       font=cls.FONTS['body'])
        
        style.map('Modern.TEntry',
                 bordercolor=[('focus', cls.COLORS['border_focus'])])
        
        # Combobox styles
        style.configure('Modern.TCombobox',
                       fieldbackground=cls.COLORS['bg_tertiary'],
                       background=cls.COLORS['bg_tertiary'],
                       foreground=cls.COLORS['text_primary'],
                       borderwidth=1,
                       font=cls.FONTS['body'])
        
        style.map('Modern.TCombobox',
                 bordercolor=[('focus', cls.COLORS['border_focus'])])
        
        # Checkbutton styles
        style.configure('Modern.TCheckbutton',
                       background=cls.COLORS['bg_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body'],
                       focuscolor='none')
        
        # LabelFrame styles
        style.configure('Modern.TLabelframe',
                       background=cls.COLORS['bg_secondary'],
                       borderwidth=1,
                       relief='flat')
        
        style.configure('Modern.TLabelframe.Label',
                       background=cls.COLORS['bg_secondary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body_bold'])
        
        # Notebook styles
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
                 foreground=[('selected', cls.COLORS['text_primary'])])
        
        # Progressbar styles
        style.configure('Modern.TProgressbar',
                       background=cls.COLORS['accent_primary'],
                       troughcolor=cls.COLORS['bg_tertiary'],
                       borderwidth=0,
                       lightcolor=cls.COLORS['accent_primary'],
                       darkcolor=cls.COLORS['accent_primary'])
    
    @classmethod
    def _apply_dark_title_bar(cls, root: tk.Tk) -> None:
        """Apply dark title bar on Windows."""
        if platform.system() == "Windows":
            try:
                import ctypes
                from ctypes import wintypes
                
                # Wait for window to be created
                root.update_idletasks()
                
                # Get window handle
                hwnd = ctypes.windll.user32.GetParent(root.winfo_id())
                if not hwnd:
                    hwnd = root.winfo_id()
                
                # Windows 10/11 dark title bar
                DWMWA_USE_IMMERSIVE_DARK_MODE = 20
                set_window_attribute = ctypes.windll.dwmapi.DwmSetWindowAttribute
                
                # Try to set dark mode
                value = wintypes.DWORD(1)  # Enable dark mode
                set_window_attribute(
                    ctypes.wintypes.HWND(hwnd),
                    wintypes.DWORD(DWMWA_USE_IMMERSIVE_DARK_MODE),
                    ctypes.byref(value),
                    ctypes.sizeof(value)
                )
                
                # Force window refresh
                root.withdraw()
                root.deiconify()
                
            except Exception as e:
                print(f"Could not set dark title bar: {e}")
                pass


class ModernComponents:
    """Factory for creating modern styled components."""
    
    @staticmethod
    def create_card_frame(parent: tk.Widget, **kwargs) -> tk.Frame:
        """Create a glassmorphism card-style frame with neon accents."""
        frame = tk.Frame(parent, 
                        bg=DarkTheme.COLORS['bg_glass'],
                        relief='flat',
                        bd=0,
                        highlightbackground=DarkTheme.COLORS['border_glow'],
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
        self.max_radius = self.size // 2 - 20
        
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
            
            # Draw the bar with rounded edges effect
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
        """Draw the circular audio meter with radiating lines."""
        self.delete("all")
        
        if self.width <= 0 or self.height <= 0:
            return
        
        import math
        
        # Background circle
        self.create_oval(
            self.center_x - self.max_outer_radius,
            self.center_y - self.max_outer_radius,
            self.center_x + self.max_outer_radius,
            self.center_y + self.max_outer_radius,
            fill=self.bg_color, outline=self.border_color, width=1
        )
        
        # Draw radiating lines
        for i in range(self.num_lines):
            angle = (i * 360 / self.num_lines + self.rotation_angle) * math.pi / 180
            line_length = self.line_lengths[i]
            
            # Calculate line positions
            start_x = self.center_x + self.inner_radius * math.cos(angle)
            start_y = self.center_y + self.inner_radius * math.sin(angle)
            end_x = self.center_x + (self.inner_radius + line_length) * math.cos(angle)
            end_y = self.center_y + (self.inner_radius + line_length) * math.sin(angle)
            
            # Color based on line length (distance from center creates gradient effect)
            if line_length > self.min_line_length * 3:
                color = self.primary_color
                width = 2
            elif line_length > self.min_line_length * 2:
                color = self.secondary_color
                width = 2
            else:
                color = self.accent_color
                width = 1
            
            # Voice detection glow effect
            if self.voice_detected and self.pulse_alpha > 0.5:
                # Draw glow line
                self.create_line(start_x, start_y, end_x, end_y,
                               fill=self.glow_color, width=width + 2)
            
            # Draw main line
            self.create_line(start_x, start_y, end_x, end_y,
                           fill=color, width=width, capstyle='round')
        
        # Center circle with pulse effect
        pulse_radius = self.center_circle_radius
        if self.voice_detected:
            pulse_radius += int(5 * self.pulse_alpha)
            
        # Outer glow for center circle when voice detected
        if self.voice_detected and self.pulse_alpha > 0:
            glow_radius = pulse_radius + int(8 * self.pulse_alpha)
            self.create_oval(
                self.center_x - glow_radius,
                self.center_y - glow_radius,
                self.center_x + glow_radius,
                self.center_y + glow_radius,
                fill="", outline=self.glow_color, width=2
            )
        
        # Main center circle
        center_color = self.primary_color if self.voice_detected else self.accent_color
        self.create_oval(
            self.center_x - pulse_radius,
            self.center_y - pulse_radius,
            self.center_x + pulse_radius,
            self.center_y + pulse_radius,
            fill=center_color, outline=self.secondary_color, width=1
        )
        
        # Level text in center
        level_text = f"{int(self.level * 100)}%"
        text_color = self.glow_color if self.voice_detected else self.secondary_color
        self.create_text(self.center_x, self.center_y,
                        text=level_text, fill=text_color,
                        font=('Segoe UI', 10, 'bold'), anchor='center')
    
    def _draw_meter(self):
        """Draw the modern animated audio level meter."""
        self.delete("all")
        
        if self.width <= 0 or self.height <= 0:
            return
            
        # Background with subtle gradient
        self._draw_background()
        
        # Main level segments
        if self.level > 0:
            active_segments = int(self.num_segments * self.level)
            
            for i in range(active_segments):
                x = 20 + i * (self.segment_width + self.segment_spacing)
                y_center = self.height // 2
                segment_height = min(self.height - 20, 10 + (self.height - 20) * (i / self.num_segments))
                
                y1 = y_center - segment_height // 2
                y2 = y_center + segment_height // 2
                
                # Get segment color
                color = self._get_level_color(i, self.num_segments)
                
                # Voice detection glow effect
                if self.voice_detected and self.pulse_alpha > 0:
                    glow_size = int(3 * self.pulse_alpha)
                    for g in range(glow_size, 0, -1):
                        alpha = 0.3 * (glow_size - g + 1) / glow_size
                        glow_color = self._blend_color(color, self.voice_color, alpha)
                        self.create_rectangle(x - g, y1 - g, x + self.segment_width + g, y2 + g,
                                            fill=glow_color, outline="")
                
                # Main segment
                self.create_rectangle(x, y1, x + self.segment_width, y2,
                                    fill=color, outline="", width=0)
        
        # Peak indicator with enhanced glow
        if self.peak_level > 0.05:
            peak_x = 20 + int((self.width - 40) * self.peak_level)
            
            # Multi-layer glow for peak
            for width in range(4, 0, -1):
                alpha = 0.4 * (5 - width) / 4
                self.create_line(peak_x, 8, peak_x, self.height - 8,
                               fill=self.peak_color, width=width)
        
        # Particle effects
        for x, y, life in self.glow_particles:
            alpha = life / 30.0
            size = int(3 * alpha)
            if size > 0:
                self.create_oval(x - size, y - size, x + size, y + size,
                               fill=self.voice_color, outline="")
        
        # Level display with modern styling
        self._draw_level_display()
                        
    def _draw_background(self):
        """Draw the background with gradient effect."""
        # Main background
        self.create_rectangle(0, 0, self.width, self.height,
                            fill=self.bg_color, outline=self.border_color, width=1)
        
        # Subtle inner shadow effect
        shadow_color = '#1a1a2a'
        self.create_rectangle(1, 1, self.width-1, 3,
                            fill=shadow_color, outline="")
                            
    def _draw_level_display(self):
        """Draw the level percentage and voice indicator."""
        # Level text
        level_text = f"{int(self.level * 100)}%"
        text_color = DarkTheme.COLORS['text_secondary']
        
        if self.voice_detected:
            text_color = self.voice_color
            # Add voice icon with pulse
            icon_alpha = 0.5 + 0.5 * self.pulse_alpha
            self.create_text(self.width - 60, self.height // 2,
                           text="🎙️", fill=self._alpha_blend(self.voice_color, icon_alpha),
                           font=('Segoe UI', 12), anchor='center')
            
        self.create_text(self.width - 30, self.height // 2,
                        text=level_text, fill=text_color,
                        font=('Segoe UI', 10, 'bold'), anchor='center')
                        
        # Frequency bars effect (decorative)
        if self.level > 0.1:
            for i in range(5):
                x = 5 + i * 3
                bar_height = int((self.height - 10) * (0.3 + 0.7 * (i / 4)) * self.level)
                y1 = (self.height - bar_height) // 2
                y2 = y1 + bar_height
                
                alpha = 0.3 + 0.4 * self.level
                color = self._alpha_blend(DarkTheme.COLORS['accent_primary'], alpha)
                self.create_rectangle(x, y1, x + 1, y2, fill=color, outline="")
                        
    def _blend_color(self, color1: str, color2: str, ratio: float) -> str:
        """Blend two colors together."""
        # Simple color mixing (would need proper color space conversion for better results)
        return color1  # Simplified for now
        
    def _alpha_blend(self, color: str, alpha: float) -> str:
        """Apply alpha to a color (simplified)."""
        # This is a simplified alpha blend - would need proper implementation
        return color


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
        """Animate recording status with pulsing red."""
        import math
        alpha = (math.sin(self.animation_step * 0.3) + 1) / 2
        # Simple pulsing effect by alternating colors
        if self.animation_step % 20 < 10:
            color = DarkTheme.COLORS['success']
        else:
            color = '#059669'  # Darker green
        
        self.itemconfig(self.circle, fill=color)
        self.animation_step += 1
        self.animation_id = self.after(100, self._animate_recording)
    
    def _animate_processing(self) -> None:
        """Animate processing status with rotating effect."""
        # Simple color cycling for processing
        colors = [DarkTheme.COLORS['info'], '#2563eb', '#1d4ed8']
        color = colors[self.animation_step % len(colors)]
        
        self.itemconfig(self.circle, fill=color)
        self.animation_step += 1
        self.animation_id = self.after(200, self._animate_processing)


class ActivityHistoryPanel(tk.Frame):
    """Modern activity history panel showing recent transcription activities."""
    
    def __init__(self, parent: tk.Widget, **kwargs):
        super().__init__(parent, bg=DarkTheme.COLORS['bg_secondary'], **kwargs)
        
        self.activities = []
        self.max_activities = 20
        self.animation_enabled = True
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Set up the activity history UI."""
        # Header
        header_frame = tk.Frame(self, bg=DarkTheme.COLORS['bg_secondary'])
        header_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
        
        title_label = tk.Label(
            header_frame, 
            text="Recent activity",
            bg=DarkTheme.COLORS['bg_secondary'],
            fg=DarkTheme.COLORS['text_primary'],
            font=DarkTheme.FONTS['heading']
        )
        title_label.pack(side=tk.LEFT)
        
        # Clear button
        clear_btn = tk.Button(
            header_frame,
            text="Clear",
            bg=DarkTheme.COLORS['bg_tertiary'],
            fg=DarkTheme.COLORS['text_secondary'],
            font=DarkTheme.FONTS['caption'],
            border=0,
            relief='flat',
            padx=8,
            pady=4,
            command=self.clear_history
        )
        clear_btn.pack(side=tk.RIGHT)
        
        # Scrollable content
        self.canvas = tk.Canvas(
            self, 
            bg=DarkTheme.COLORS['bg_secondary'],
            highlightthickness=0
        )
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=DarkTheme.COLORS['bg_secondary'])
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side="left", fill="both", expand=True, padx=(15, 0))
        self.scrollbar.pack(side="right", fill="y", padx=(0, 15))
        
        # Initial empty state
        self._show_empty_state()
        
    def _show_empty_state(self):
        """Show empty state when no activities."""
        empty_label = tk.Label(
            self.scrollable_frame,
            text="No recent activity",
            bg=DarkTheme.COLORS['bg_secondary'],
            fg=DarkTheme.COLORS['text_muted'],
            font=DarkTheme.FONTS['body']
        )
        empty_label.pack(pady=50)
        
    def add_activity(self, activity_type: str, content: str, timestamp: str = None):
        """Add a new activity to the history."""
        from datetime import datetime
        
        if timestamp is None:
            timestamp = datetime.now().strftime("%I:%M %p")
            
        activity = {
            'type': activity_type,
            'content': content[:100] + ('...' if len(content) > 100 else ''),
            'timestamp': timestamp,
            'full_content': content
        }
        
        self.activities.insert(0, activity)  # Add to beginning
        
        # Limit activities
        if len(self.activities) > self.max_activities:
            self.activities = self.activities[:self.max_activities]
            
        self._refresh_display()
        
    def clear_history(self):
        """Clear all activity history."""
        self.activities.clear()
        self._refresh_display()
        
    def _refresh_display(self):
        """Refresh the activity display."""
        # Clear existing widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        if not self.activities:
            self._show_empty_state()
            return
            
        # Add activities
        for i, activity in enumerate(self.activities):
            self._create_activity_item(activity, i == 0)
            
        # Scroll to top
        self.canvas.yview_moveto(0)
        
    def _create_activity_item(self, activity: dict, is_first: bool = False):
        """Create a single activity item."""
        # Container frame
        item_frame = tk.Frame(
            self.scrollable_frame,
            bg=DarkTheme.COLORS['bg_secondary']
        )
        item_frame.pack(fill=tk.X, padx=10, pady=(0, 1))
        
        # Add subtle slide-in animation for new items
        if is_first and self.animation_enabled:
            self._animate_item_slide_in(item_frame)
        
        # Time frame
        time_frame = tk.Frame(item_frame, bg=DarkTheme.COLORS['bg_secondary'])
        time_frame.pack(side=tk.LEFT, anchor=tk.N, padx=(0, 10))
        
        time_label = tk.Label(
            time_frame,
            text=activity['timestamp'],
            bg=DarkTheme.COLORS['bg_secondary'],
            fg=DarkTheme.COLORS['text_muted'],
            font=DarkTheme.FONTS['caption']
        )
        time_label.pack(anchor=tk.W)
        
        # Content frame
        content_frame = tk.Frame(item_frame, bg=DarkTheme.COLORS['bg_secondary'])
        content_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Activity type indicator
        type_colors = {
            'transcription': DarkTheme.COLORS['success'],
            'recording_start': DarkTheme.COLORS['info'],
            'recording_stop': DarkTheme.COLORS['warning'],
            'error': DarkTheme.COLORS['error']
        }
        
        type_color = type_colors.get(activity['type'], DarkTheme.COLORS['text_secondary'])
        
        type_label = tk.Label(
            content_frame,
            text=activity['type'].replace('_', ' ').title(),
            bg=DarkTheme.COLORS['bg_secondary'],
            fg=type_color,
            font=DarkTheme.FONTS['caption']
        )
        type_label.pack(anchor=tk.W)
        
        # Content text
        content_label = tk.Label(
            content_frame,
            text=activity['content'],
            bg=DarkTheme.COLORS['bg_secondary'],
            fg=DarkTheme.COLORS['text_primary'],
            font=DarkTheme.FONTS['body'],
            anchor=tk.W,
            justify=tk.LEFT,
            wraplength=250
        )
        content_label.pack(anchor=tk.W, pady=(2, 8))
        
        # Separator line (except for last item)
        separator = tk.Frame(
            self.scrollable_frame,
            height=1,
            bg=DarkTheme.COLORS['border']
        )
        separator.pack(fill=tk.X, padx=20, pady=2)
    
    def _animate_item_slide_in(self, item_frame: tk.Frame):
        """Animate new activity item sliding in."""
        # Simple slide animation by temporarily hiding and showing
        original_pack = item_frame.pack_info()
        item_frame.pack_forget()
        
        def restore_item():
            item_frame.pack(**original_pack)
            
        # Restore after a brief delay for slide effect
        self.after(50, restore_item)