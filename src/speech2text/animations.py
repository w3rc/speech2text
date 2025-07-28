"""Smooth animations and transitions for Speech2Text application."""

import tkinter as tk
import math
from typing import Callable, Optional, Any
from dataclasses import dataclass


@dataclass
class AnimationState:
    """State for an ongoing animation."""
    widget: tk.Widget
    property_name: str
    start_value: float
    end_value: float
    duration: float
    start_time: float
    easing_func: Callable[[float], float]
    update_func: Callable[[tk.Widget, str, float], None]
    completion_callback: Optional[Callable] = None


class AnimationManager:
    """Manager for smooth animations and transitions."""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.active_animations = {}
        self.animation_id = 0
        self._running = False
        
    def start_animation_loop(self):
        """Start the animation update loop."""
        if not self._running:
            self._running = True
            self._update_animations()
    
    def stop_animation_loop(self):
        """Stop the animation update loop."""
        self._running = False
    
    def animate(self, 
                widget: tk.Widget,
                property_name: str,
                start_value: float,
                end_value: float,
                duration: float = 0.3,
                easing: str = 'ease_out',
                update_func: Optional[Callable] = None,
                completion_callback: Optional[Callable] = None) -> int:
        """
        Animate a property of a widget.
        
        Args:
            widget: The widget to animate
            property_name: Property name to animate
            start_value: Starting value
            end_value: Ending value
            duration: Animation duration in seconds
            easing: Easing function name
            update_func: Custom function to update the property
            completion_callback: Function to call when animation completes
            
        Returns:
            Animation ID for cancelling
        """
        import time
        
        self.animation_id += 1
        animation_id = self.animation_id
        
        easing_func = self._get_easing_function(easing)
        if update_func is None:
            update_func = self._default_update_func
            
        animation = AnimationState(
            widget=widget,
            property_name=property_name,
            start_value=start_value,
            end_value=end_value,
            duration=duration,
            start_time=time.time(),
            easing_func=easing_func,
            update_func=update_func,
            completion_callback=completion_callback
        )
        
        self.active_animations[animation_id] = animation
        
        if not self._running:
            self.start_animation_loop()
            
        return animation_id
    
    def cancel_animation(self, animation_id: int):
        """Cancel an ongoing animation."""
        if animation_id in self.active_animations:
            del self.active_animations[animation_id]
    
    def fade_in(self, widget: tk.Widget, duration: float = 0.3) -> int:
        """Fade in a widget."""
        return self.animate(
            widget, 'alpha', 0.0, 1.0, duration, 'ease_out',
            self._update_alpha
        )
    
    def fade_out(self, widget: tk.Widget, duration: float = 0.3, 
                 hide_on_complete: bool = True) -> int:
        """Fade out a widget."""
        def on_complete():
            if hide_on_complete:
                try:
                    widget.grid_remove()
                except:
                    pass
                    
        return self.animate(
            widget, 'alpha', 1.0, 0.0, duration, 'ease_in',
            self._update_alpha, on_complete
        )
    
    def slide_in(self, widget: tk.Widget, direction: str = 'left', 
                 distance: int = 100, duration: float = 0.4) -> int:
        """Slide a widget in from the specified direction."""
        if direction == 'left':
            return self.animate(
                widget, 'x_offset', -distance, 0, duration, 'ease_out',
                self._update_position
            )
        elif direction == 'right':
            return self.animate(
                widget, 'x_offset', distance, 0, duration, 'ease_out',
                self._update_position
            )
        elif direction == 'up':
            return self.animate(
                widget, 'y_offset', -distance, 0, duration, 'ease_out',
                self._update_position
            )
        elif direction == 'down':
            return self.animate(
                widget, 'y_offset', distance, 0, duration, 'ease_out',
                self._update_position
            )
    
    def scale_in(self, widget: tk.Widget, duration: float = 0.3) -> int:
        """Scale a widget in with bounce effect."""
        return self.animate(
            widget, 'scale', 0.0, 1.0, duration, 'bounce_out',
            self._update_scale
        )
    
    def pulse(self, widget: tk.Widget, intensity: float = 0.1, 
              duration: float = 0.6) -> int:
        """Create a pulse effect on a widget."""
        def pulse_complete():
            # Pulse back
            self.animate(
                widget, 'scale', 1.0 + intensity, 1.0, duration / 2, 'ease_in',
                self._update_scale
            )
            
        return self.animate(
            widget, 'scale', 1.0, 1.0 + intensity, duration / 2, 'ease_out',
            self._update_scale, pulse_complete
        )
    
    def _update_animations(self):
        """Update all active animations."""
        if not self._running:
            return
            
        import time
        current_time = time.time()
        completed_animations = []
        
        # Create a copy of the items to avoid dictionary changed during iteration
        for animation_id, animation in list(self.active_animations.items()):
            elapsed = current_time - animation.start_time
            progress = min(elapsed / animation.duration, 1.0)
            
            # Apply easing
            eased_progress = animation.easing_func(progress)
            
            # Calculate current value
            current_value = (animation.start_value + 
                           (animation.end_value - animation.start_value) * eased_progress)
            
            # Update the widget
            try:
                animation.update_func(animation.widget, animation.property_name, current_value)
            except Exception as e:
                print(f"Animation update error: {e}")
                completed_animations.append(animation_id)
                continue
            
            # Check if animation is complete
            if progress >= 1.0:
                completed_animations.append(animation_id)
                if animation.completion_callback:
                    try:
                        animation.completion_callback()
                    except Exception as e:
                        print(f"Animation completion callback error: {e}")
        
        # Remove completed animations
        for animation_id in completed_animations:
            if animation_id in self.active_animations:
                del self.active_animations[animation_id]
        
        # Schedule next update
        if self.active_animations:
            self.root.after(16, self._update_animations)  # ~60 FPS
        else:
            self._running = False
    
    def _get_easing_function(self, easing: str) -> Callable[[float], float]:
        """Get easing function by name."""
        easing_functions = {
            'linear': lambda t: t,
            'ease_in': lambda t: t * t,
            'ease_out': lambda t: 1 - (1 - t) ** 2,
            'ease_in_out': lambda t: 3 * t * t - 2 * t * t * t,
            'bounce_out': self._bounce_out,
            'elastic_out': self._elastic_out,
        }
        return easing_functions.get(easing, easing_functions['ease_out'])
    
    def _bounce_out(self, t: float) -> float:
        """Bounce out easing function."""
        if t < 1 / 2.75:
            return 7.5625 * t * t
        elif t < 2 / 2.75:
            t -= 1.5 / 2.75
            return 7.5625 * t * t + 0.75
        elif t < 2.5 / 2.75:
            t -= 2.25 / 2.75
            return 7.5625 * t * t + 0.9375
        else:
            t -= 2.625 / 2.75
            return 7.5625 * t * t + 0.984375
    
    def _elastic_out(self, t: float) -> float:
        """Elastic out easing function."""
        if t == 0 or t == 1:
            return t
        return (2 ** (-10 * t)) * math.sin((t - 0.1) * (2 * math.pi) / 0.4) + 1
    
    def _default_update_func(self, widget: tk.Widget, property_name: str, value: float):
        """Default property update function."""
        try:
            if hasattr(widget, 'config'):
                widget.config(**{property_name: value})
        except:
            pass
    
    def _update_alpha(self, widget: tk.Widget, property_name: str, value: float):
        """Update widget alpha/transparency."""
        try:
            # For Canvas widgets, we can simulate alpha by adjusting colors
            if isinstance(widget, tk.Canvas):
                # This is a simplified alpha effect
                pass
            else:
                # For other widgets, we can't directly set alpha in tkinter
                # but we can simulate it by adjusting the widget's state
                if value < 0.1:
                    widget.config(state='disabled')
                else:
                    widget.config(state='normal')
        except:
            pass
    
    def _update_position(self, widget: tk.Widget, property_name: str, value: float):
        """Update widget position for slide animations."""
        try:
            # Get current grid info
            grid_info = widget.grid_info()
            if not grid_info:
                return
                
            if property_name == 'x_offset':
                widget.grid(padx=(int(value), 0))
            elif property_name == 'y_offset':
                widget.grid(pady=(int(value), 0))
        except:
            pass
    
    def _update_scale(self, widget: tk.Widget, property_name: str, value: float):
        """Update widget scale (simplified)."""
        try:
            # For Canvas widgets, we could scale the contents
            # For other widgets, this is limited in tkinter
            pass
        except:
            pass


class AnimatedButton(tk.Button):
    """Button with built-in hover animations."""
    
    def __init__(self, parent, animation_manager: AnimationManager, **kwargs):
        super().__init__(parent, **kwargs)
        self.animation_manager = animation_manager
        self.original_bg = self.cget('bg')
        self.hover_bg = kwargs.get('hover_bg', '#4a4a6a')
        
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_click)
    
    def _on_enter(self, event):
        """Handle mouse enter."""
        self.animation_manager.animate(
            self, 'bg', self._color_to_rgb(self.original_bg), 
            self._color_to_rgb(self.hover_bg), 0.2, 'ease_out',
            self._update_bg_color
        )
    
    def _on_leave(self, event):
        """Handle mouse leave."""
        self.animation_manager.animate(
            self, 'bg', self._color_to_rgb(self.hover_bg),
            self._color_to_rgb(self.original_bg), 0.2, 'ease_out',
            self._update_bg_color
        )
    
    def _on_click(self, event):
        """Handle button click with animation."""
        self.animation_manager.pulse(self, 0.05, 0.1)
    
    def _color_to_rgb(self, color: str) -> float:
        """Convert color to RGB value (simplified)."""
        # This is a simplified conversion
        return 0.5
    
    def _update_bg_color(self, widget, property_name, value):
        """Update background color."""
        # This would need proper color interpolation
        pass