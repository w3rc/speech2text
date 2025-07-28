"""Modern dark theme styling for Speech2Text application."""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any
import sys
import platform


class DarkTheme:
    """Modern dark theme with sleek styling."""
    
    # Color palette
    COLORS = {
        # Background colors
        'bg_primary': '#1e1e2e',      # Main background
        'bg_secondary': '#2a2a3e',    # Secondary panels
        'bg_tertiary': '#363650',     # Raised elements
        'bg_hover': '#4a4a6a',        # Hover states
        'bg_active': '#5a5a7a',       # Active states
        
        # Text colors
        'text_primary': '#ffffff',     # Primary text
        'text_secondary': '#b4b4c8',   # Secondary text
        'text_muted': '#8a8a9e',       # Muted text
        'text_disabled': '#6a6a7e',    # Disabled text
        
        # Accent colors
        'accent_primary': '#7c3aed',   # Primary accent (purple)
        'accent_hover': '#8b5cf6',     # Accent hover
        'accent_active': '#6d28d9',    # Accent active
        
        # Status colors
        'success': '#10b981',          # Success/recording
        'warning': '#f59e0b',          # Warning
        'error': '#ef4444',            # Error
        'info': '#3b82f6',             # Info
        
        # Audio visualization
        'audio_low': '#4ade80',        # Low audio level
        'audio_mid': '#fbbf24',        # Medium audio level
        'audio_high': '#f87171',       # High audio level
        
        # Borders
        'border': '#444461',           # Default border
        'border_focus': '#7c3aed',     # Focused border
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
        
        # Button styles
        style.configure('Modern.TButton',
                       background=cls.COLORS['accent_primary'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body_bold'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(16, 8))
        
        style.map('Modern.TButton',
                 background=[('active', cls.COLORS['accent_hover']),
                           ('pressed', cls.COLORS['accent_active'])])
        
        style.configure('Secondary.TButton',
                       background=cls.COLORS['bg_tertiary'],
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
        
        # Record button (special styling)
        style.configure('Record.TButton',
                       background=cls.COLORS['success'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body_bold'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 12))
        
        style.map('Record.TButton',
                 background=[('active', '#059669'),
                           ('pressed', '#047857')])
        
        style.configure('Recording.TButton',
                       background=cls.COLORS['error'],
                       foreground=cls.COLORS['text_primary'],
                       font=cls.FONTS['body_bold'],
                       borderwidth=0,
                       focuscolor='none',
                       relief='flat',
                       padding=(20, 12))
        
        style.map('Recording.TButton',
                 background=[('active', '#dc2626'),
                           ('pressed', '#b91c1c')])
        
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
    def create_card_frame(parent: tk.Widget, **kwargs) -> ttk.Frame:
        """Create a card-style frame with modern styling."""
        frame = ttk.Frame(parent, style='Card.TFrame', **kwargs)
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
    """Modern animated audio level meter with gradient effects and voice detection."""
    
    def __init__(self, parent: tk.Widget, width: int = 400, height: int = 50, **kwargs):
        super().__init__(parent, width=width, height=height, 
                        bg=DarkTheme.COLORS['bg_secondary'],
                        highlightthickness=0, **kwargs)
        
        self.width = width
        self.height = height
        self.level = 0.0
        self.peak_level = 0.0
        self.voice_detected = False
        self.animation_frame = 0
        
        # Enhanced colors with gradients
        self.bg_color = DarkTheme.COLORS['bg_secondary']
        self.border_color = DarkTheme.COLORS['border']
        self.level_colors = [
            '#10b981',  # Green (low)
            '#f59e0b',  # Yellow (medium) 
            '#ef4444'   # Red (high)
        ]
        self.voice_color = '#8b5cf6'  # Purple for voice detection
        self.peak_color = '#06b6d4'   # Cyan for peak
        
        # Animation properties
        self.pulse_alpha = 0
        self.pulse_direction = 1
        self.glow_particles = []
        
        # Segment properties
        self.num_segments = 30
        self.segment_width = (width - 40) // self.num_segments
        self.segment_spacing = 2
        
        self.bind('<Configure>', self._on_resize)
        self._animate()
        
    def _on_resize(self, event):
        """Handle widget resize."""
        self.width = event.width
        self.height = event.height
        self.num_segments = max(20, (self.width - 40) // 15)
        self.segment_width = (self.width - 40) // self.num_segments
        
    def update_level(self, level: float, voice_detected: bool = False):
        """Update the audio level display."""
        self.level = max(0.0, min(1.0, level))
        self.voice_detected = voice_detected
        
        # Update peak with smooth decay
        if self.level > self.peak_level:
            self.peak_level = self.level
        else:
            self.peak_level *= 0.92
            
        # Add particle effects for high levels
        if self.level > 0.8:
            self._add_particle()
            
    def _get_level_color(self, segment_index: int, total_segments: int) -> str:
        """Get color based on segment position with gradient effect."""
        ratio = segment_index / total_segments
        if ratio < 0.4:
            return self.level_colors[0]  # Green
        elif ratio < 0.7:
            return self.level_colors[1]  # Yellow
        else:
            return self.level_colors[2]  # Red
            
    def _add_particle(self):
        """Add particle effect for high audio levels."""
        import random
        if len(self.glow_particles) < 10:  # Limit particles
            x = random.randint(20, self.width - 20)
            y = random.randint(10, self.height - 10)
            life = 30  # Particle life in frames
            self.glow_particles.append((x, y, life))
            
    def _animate(self):
        """Animate the meter with pulse effects and particles."""
        self.animation_frame += 1
        
        # Voice detection pulse animation
        if self.voice_detected:
            self.pulse_alpha += self.pulse_direction * 0.15
            if self.pulse_alpha >= 1.0:
                self.pulse_alpha = 1.0
                self.pulse_direction = -1
            elif self.pulse_alpha <= 0.2:
                self.pulse_alpha = 0.2
                self.pulse_direction = 1
        else:
            self.pulse_alpha = max(0, self.pulse_alpha - 0.1)
            
        # Update particles
        self.glow_particles = [(x, y, life-1) for x, y, life in self.glow_particles if life > 0]
            
        self._draw_meter()
        self.after(33, self._animate)  # ~30 FPS animation
        
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