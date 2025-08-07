"""
K00gar Spell Plugin
==================

This plugin creates particle effects that spell out "k00gar" when
the right mouse button is clicked. It demonstrates the plugin system
and particle manipulation capabilities.

Author: Cursor IDE Demo
Version: 1.0.0
"""

import pygame
import math
from typing import Dict, Any, List, Tuple
from .base_plugin import BasePlugin, PluginInfo

# Import particle system components
try:
    from app.frontend.particle_system import ParticleEmitter, Particle
    from app.utils.color_utils import Color
    from app.utils.math_utils import random_range
except ImportError:
    # Fallback for direct script execution
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from app.frontend.particle_system import ParticleEmitter, Particle
    from app.utils.color_utils import Color
    from app.utils.math_utils import random_range


class K00garSpellPlugin(BasePlugin):
    """
    Plugin that spells out "k00gar" with particles on right-click
    
    This plugin demonstrates:
    - Mouse event handling
    - Particle system integration
    - Text rendering with particles
    - Plugin system capabilities
    """
    
    def __init__(self):
        """Initialize the k00gar spell plugin"""
        super().__init__()
        
        # Text to spell out
        self.text = "k00gar"
        
        # Character positions (relative to click position)
        self.char_positions = [
            (-120, -20),  # k
            (-80, -20),   # 0
            (-40, -20),   # 0
            (0, -20),     # g
            (40, -20),    # a
            (80, -20),    # r
        ]
        
        # Character colors (rainbow effect)
        self.char_colors = [
            Color(255, 0, 0),    # Red
            Color(255, 165, 0),  # Orange
            Color(255, 255, 0),  # Yellow
            Color(0, 255, 0),    # Green
            Color(0, 0, 255),    # Blue
            Color(128, 0, 128),  # Purple
        ]
        
        # Active spell effects
        self.active_spells: List[Dict[str, Any]] = []
        
        # Spell configuration
        self.spell_duration = 3.0
        self.particles_per_char = 15
        self.spell_radius = 30
        
    def get_plugin_info(self) -> PluginInfo:
        """Get plugin information"""
        return PluginInfo(
            name="K00gar Spell",
            version="1.0.0",
            author="Cursor IDE Demo",
            description="Spells out 'k00gar' with particles on right-click",
            events=["mouse_click", "update", "render"]
        )
    
    def on_mouse_click(self, button: int, pos: Tuple[int, int], app_context: Dict[str, Any]) -> bool:
        """
        Handle mouse click events
        
        Args:
            button: Mouse button (1=left, 2=middle, 3=right)
            pos: Mouse position (x, y)
            app_context: Application context
            
        Returns:
            True if event was handled, False otherwise
        """
        if button == 3:  # Right mouse button
            self._create_spell_effect(pos, app_context)
            return True
        
        return False
    
    def _create_spell_effect(self, pos: Tuple[int, int], app_context: Dict[str, Any]) -> None:
        """
        Create a spell effect at the given position
        
        Args:
            pos: Position to create the spell
            app_context: Application context
        """
        try:
            particle_system = app_context.get('particle_system')
            if not particle_system:
                self.logger.warning("Particle system not found in app context")
                return
            
            # Create spell effect data
            spell_effect = {
                'pos': pos,
                'start_time': 0.0,
                'duration': self.spell_duration,
                'char_emitters': [],
                'active': True
            }
            
            # Create particle emitters for each character
            for i, (char, char_pos, char_color) in enumerate(zip(self.text, self.char_positions, self.char_colors)):
                # Calculate character position
                char_x = pos[0] + char_pos[0]
                char_y = pos[1] + char_pos[1]
                
                # Create emitter for this character
                emitter = self._create_char_emitter(char_x, char_y, char_color, i * 0.1)
                particle_system.add_emitter(emitter)
                
                spell_effect['char_emitters'].append(emitter)
            
            # Add to active spells
            self.active_spells.append(spell_effect)
            
            self.logger.info(f"Created k00gar spell effect at {pos}")
            
        except Exception as e:
            self.logger.error(f"Error creating spell effect: {e}")
    
    def _create_char_emitter(self, x: float, y: float, color: Color, delay: float) -> ParticleEmitter:
        """
        Create a particle emitter for a character
        
        Args:
            x: X position
            y: Y position
            color: Character color
            delay: Delay before starting emission
            
        Returns:
            Particle emitter
        """
        emitter = ParticleEmitter(x, y)
        
        # Configure emitter for character effect
        emitter.set_emission_rate(20.0)
        emitter.set_particle_life(2.0)
        emitter.set_particle_speed(50.0)
        emitter.set_particle_size(3.0)
        emitter.set_particle_color(color)
        emitter.set_emission_angle(0, 360)  # All directions
        emitter.set_gravity(0.0)
        emitter.set_friction(0.98)
        
        # Add variation
        emitter.color_variation = 30.0
        emitter.size_variation = 0.5
        emitter.speed_variation = 0.3
        emitter.life_variation = 0.4
        
        # Set lifetime
        emitter.set_emitter_lifetime(1.5, 0.5)
        
        # Add delay
        emitter.emission_timer = -delay  # Negative to delay start
        
        return emitter
    
    def on_update(self, dt: float, app_context: Dict[str, Any]) -> bool:
        """
        Update plugin state
        
        Args:
            dt: Delta time
            app_context: Application context
            
        Returns:
            True if update was handled, False otherwise
        """
        # Update active spells
        for spell_effect in list(self.active_spells):
            spell_effect['start_time'] += dt
            
            # Check if spell is finished
            if spell_effect['start_time'] >= spell_effect['duration']:
                spell_effect['active'] = False
                self.active_spells.remove(spell_effect)
                self.logger.debug("Spell effect finished")
        
        return True
    
    def on_render(self, surface, app_context: Dict[str, Any]) -> bool:
        """
        Render plugin elements
        
        Args:
            surface: Pygame surface to render on
            app_context: Application context
            
        Returns:
            True if rendering was handled, False otherwise
        """
        # Render active spell indicators (optional)
        for spell_effect in self.active_spells:
            if spell_effect['active']:
                pos = spell_effect['pos']
                progress = spell_effect['start_time'] / spell_effect['duration']
                
                # Draw a subtle indicator
                alpha = int(255 * (1.0 - progress))
                if alpha > 0:
                    indicator_surface = pygame.Surface((20, 20), pygame.SRCALPHA)
                    pygame.draw.circle(indicator_surface, (255, 255, 255, alpha), (10, 10), 10)
                    surface.blit(indicator_surface, (pos[0] - 10, pos[1] - 10))
        
        return True
    
    def get_config(self) -> Dict[str, Any]:
        """Get plugin configuration"""
        return {
            'text': self.text,
            'spell_duration': self.spell_duration,
            'particles_per_char': self.particles_per_char,
            'spell_radius': self.spell_radius
        }
    
    def set_config(self, config: Dict[str, Any]) -> bool:
        """Set plugin configuration"""
        try:
            if 'text' in config:
                self.text = config['text']
                # Recalculate character positions
                self._update_char_positions()
            
            if 'spell_duration' in config:
                self.spell_duration = config['spell_duration']
            
            if 'particles_per_char' in config:
                self.particles_per_char = config['particles_per_char']
            
            if 'spell_radius' in config:
                self.spell_radius = config['spell_radius']
            
            return True
            
        except Exception as e:
            self.logger.error(f"Error setting plugin config: {e}")
            return False
    
    def _update_char_positions(self) -> None:
        """Update character positions based on current text"""
        char_width = 40
        start_x = -(len(self.text) - 1) * char_width // 2
        
        self.char_positions = []
        for i in range(len(self.text)):
            x = start_x + i * char_width
            self.char_positions.append((x, -20))
        
        # Update colors if needed
        while len(self.char_colors) < len(self.text):
            # Add more rainbow colors
            hue = (len(self.char_colors) * 60) % 360
            self.char_colors.append(Color.from_hsv(hue, 100, 100)) 