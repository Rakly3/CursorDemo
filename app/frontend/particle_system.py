"""
Particle System
==============

This module provides a comprehensive particle system for the Cursor IDE demo
application, featuring various particle effects and behaviors.

Author: Cursor IDE Demo
Version: 1.0.0
"""

import pygame
import random
import math
from typing import List, Tuple, Optional, Callable
from dataclasses import dataclass
from ..utils.math_utils import clamp, lerp, random_range, distance
from ..utils.color_utils import Color, random_color, random_bright_color


@dataclass
class Particle:
    """Individual particle data"""
    x: float
    y: float
    vx: float
    vy: float
    life: float
    max_life: float
    size: float
    color: Color
    alpha: float = 255.0
    rotation: float = 0.0
    rotation_speed: float = 0.0
    gravity: float = 0.0
    friction: float = 0.98
    trail_length: int = 0
    trail_positions: List[Tuple[float, float]] = None
    
    def __post_init__(self):
        """Initialize particle after creation"""
        if self.trail_positions is None:
            self.trail_positions = []
    
    def update(self, dt: float) -> bool:
        """
        Update particle state
        
        Args:
            dt: Delta time
            
        Returns:
            True if particle is still alive
        """
        # Update position
        self.x += self.vx * dt
        self.y += self.vy * dt
        
        # Apply gravity
        self.vy += self.gravity * dt
        
        # Apply friction
        self.vx *= self.friction
        self.vy *= self.friction
        
        # Update rotation
        self.rotation += self.rotation_speed * dt
        
        # Update life
        self.life -= dt
        
        # Update alpha based on life
        life_ratio = self.life / self.max_life
        self.alpha = 255.0 * life_ratio
        
        # Update trail
        if self.trail_length > 0:
            self.trail_positions.append((self.x, self.y))
            if len(self.trail_positions) > self.trail_length:
                self.trail_positions.pop(0)
        
        return self.life > 0
    
    def get_color_with_alpha(self) -> Tuple[int, int, int, int]:
        """Get color with current alpha"""
        return (self.color.r, self.color.g, self.color.b, int(self.alpha))


class ParticleEmitter:
    """
    Particle emitter that creates and manages particles
    
    This class provides various emission patterns and behaviors
    for creating dynamic particle effects.
    """
    
    def __init__(self, x: float, y: float):
        """
        Initialize particle emitter
        
        Args:
            x: Emitter X position
            y: Emitter Y position
        """
        self.x = x
        self.y = y
        self.particles: List[Particle] = []
        self.emission_rate = 10.0  # particles per second
        self.emission_timer = 0.0
        self.active = True
        
        # Emission parameters
        self.particle_life = 2.0
        self.particle_speed = 100.0
        self.particle_size = 5.0
        self.particle_color = Color(255, 255, 255)
        self.emission_angle = 0.0
        self.emission_angle_spread = 360.0
        self.gravity = 0.0
        self.friction = 0.98
        
        # Color variation
        self.color_variation = 0.0
        self.size_variation = 0.0
        self.speed_variation = 0.0
        self.life_variation = 0.0
        
        # Trail settings
        self.trail_enabled = False
        self.trail_length = 10
        
        # Burst settings
        self.burst_mode = False
        self.burst_count = 10
        self.burst_timer = 0.0
        self.burst_interval = 1.0
    
    def update(self, dt: float) -> None:
        """
        Update emitter and particles
        
        Args:
            dt: Delta time
        """
        # Update emission timer
        if self.active:
            if self.burst_mode:
                self.burst_timer += dt
                if self.burst_timer >= self.burst_interval:
                    self.emit_burst()
                    self.burst_timer = 0.0
            else:
                self.emission_timer += dt
                emission_interval = 1.0 / self.emission_rate
                
                while self.emission_timer >= emission_interval:
                    self.emit_particle()
                    self.emission_timer -= emission_interval
        
        # Update particles
        self.particles = [p for p in self.particles if p.update(dt)]
    
    def emit_particle(self) -> None:
        """Emit a single particle"""
        # Calculate emission angle
        angle_rad = math.radians(self.emission_angle + random_range(-self.emission_angle_spread/2, self.emission_angle_spread/2))
        
        # Calculate velocity
        speed = self.particle_speed * (1.0 + random_range(-self.speed_variation, self.speed_variation))
        vx = math.cos(angle_rad) * speed
        vy = math.sin(angle_rad) * speed
        
        # Calculate particle properties
        life = self.particle_life * (1.0 + random_range(-self.life_variation, self.life_variation))
        size = self.particle_size * (1.0 + random_range(-self.size_variation, self.size_variation))
        
        # Calculate color
        color = self.particle_color
        if self.color_variation > 0:
            color = Color(
                clamp(color.r + random_range(-self.color_variation, self.color_variation), 0, 255),
                clamp(color.g + random_range(-self.color_variation, self.color_variation), 0, 255),
                clamp(color.b + random_range(-self.color_variation, self.color_variation), 0, 255)
            )
        
        # Create particle
        particle = Particle(
            x=self.x,
            y=self.y,
            vx=vx,
            vy=vy,
            life=life,
            max_life=life,
            size=size,
            color=color,
            gravity=self.gravity,
            friction=self.friction,
            trail_length=self.trail_length if self.trail_enabled else 0
        )
        
        self.particles.append(particle)
    
    def emit_burst(self) -> None:
        """Emit a burst of particles"""
        for _ in range(self.burst_count):
            self.emit_particle()
    
    def set_position(self, x: float, y: float) -> None:
        """Set emitter position"""
        self.x = x
        self.y = y
    
    def set_emission_rate(self, rate: float) -> None:
        """Set emission rate"""
        self.emission_rate = max(0.0, rate)
    
    def set_particle_life(self, life: float) -> None:
        """Set particle lifetime"""
        self.particle_life = max(0.1, life)
    
    def set_particle_speed(self, speed: float) -> None:
        """Set particle speed"""
        self.particle_speed = max(0.0, speed)
    
    def set_particle_size(self, size: float) -> None:
        """Set particle size"""
        self.particle_size = max(0.1, size)
    
    def set_particle_color(self, color: Color) -> None:
        """Set particle color"""
        self.particle_color = color
    
    def set_emission_angle(self, angle: float, spread: float = 360.0) -> None:
        """Set emission angle and spread"""
        self.emission_angle = angle
        self.emission_angle_spread = spread
    
    def set_gravity(self, gravity: float) -> None:
        """Set gravity effect"""
        self.gravity = gravity
    
    def set_friction(self, friction: float) -> None:
        """Set friction effect"""
        self.friction = clamp(friction, 0.0, 1.0)
    
    def enable_trail(self, enabled: bool, length: int = 10) -> None:
        """Enable/disable particle trails"""
        self.trail_enabled = enabled
        self.trail_length = length
    
    def set_burst_mode(self, enabled: bool, count: int = 10, interval: float = 1.0) -> None:
        """Set burst emission mode"""
        self.burst_mode = enabled
        self.burst_count = count
        self.burst_interval = interval
    
    def clear_particles(self) -> None:
        """Clear all particles"""
        self.particles.clear()
    
    def get_particle_count(self) -> int:
        """Get current particle count"""
        return len(self.particles)


class ParticleSystem:
    """
    Main particle system manager
    
    This class manages multiple particle emitters and provides
    high-level control over particle effects.
    """
    
    def __init__(self):
        """Initialize particle system"""
        self.emitters: List[ParticleEmitter] = []
        self.particles: List[Particle] = []
        self.active = True
    
    def add_emitter(self, emitter: ParticleEmitter) -> None:
        """Add particle emitter"""
        self.emitters.append(emitter)
    
    def remove_emitter(self, emitter: ParticleEmitter) -> None:
        """Remove particle emitter"""
        if emitter in self.emitters:
            self.emitters.remove(emitter)
    
    def create_emitter(self, x: float, y: float) -> ParticleEmitter:
        """Create and add a new emitter"""
        emitter = ParticleEmitter(x, y)
        self.add_emitter(emitter)
        return emitter
    
    def update(self, dt: float) -> None:
        """Update all emitters and particles"""
        if not self.active:
            return
        
        # Update emitters
        for emitter in self.emitters:
            emitter.update(dt)
        
        # Collect all particles
        self.particles = []
        for emitter in self.emitters:
            self.particles.extend(emitter.particles)
    
    def render(self, surface: pygame.Surface) -> None:
        """Render all particles"""
        for particle in self.particles:
            # Render trail
            if particle.trail_positions:
                for i, (trail_x, trail_y) in enumerate(particle.trail_positions):
                    alpha = int(255 * (i / len(particle.trail_positions)))
                    trail_color = (particle.color.r, particle.color.g, particle.color.b, alpha)
                    trail_surface = pygame.Surface((particle.size * 2, particle.size * 2), pygame.SRCALPHA)
                    pygame.draw.circle(trail_surface, trail_color, (particle.size, particle.size), particle.size)
                    surface.blit(trail_surface, (trail_x - particle.size, trail_y - particle.size))
            
            # Render particle
            if particle.alpha > 0:
                particle_surface = pygame.Surface((particle.size * 2, particle.size * 2), pygame.SRCALPHA)
                particle_color = particle.get_color_with_alpha()
                pygame.draw.circle(particle_surface, particle_color, (particle.size, particle.size), particle.size)
                surface.blit(particle_surface, (particle.x - particle.size, particle.y - particle.size))
    
    def clear_all(self) -> None:
        """Clear all emitters and particles"""
        for emitter in self.emitters:
            emitter.clear_particles()
        self.particles.clear()
    
    def get_total_particles(self) -> int:
        """Get total particle count"""
        return len(self.particles)
    
    def set_active(self, active: bool) -> None:
        """Set system active state"""
        self.active = active


# Predefined particle effects
def create_fire_effect(x: float, y: float) -> ParticleEmitter:
    """Create a fire particle effect"""
    emitter = ParticleEmitter(x, y)
    emitter.set_emission_rate(20.0)
    emitter.set_particle_life(1.5)
    emitter.set_particle_speed(50.0)
    emitter.set_particle_size(3.0)
    emitter.set_particle_color(Color(255, 100, 0))
    emitter.set_emission_angle(270, 60)  # Upward with spread
    emitter.set_gravity(-50.0)  # Upward gravity
    emitter.set_friction(0.95)
    emitter.color_variation = 50.0
    emitter.size_variation = 0.5
    emitter.speed_variation = 0.3
    emitter.life_variation = 0.5
    return emitter


def create_explosion_effect(x: float, y: float) -> ParticleEmitter:
    """Create an explosion particle effect"""
    emitter = ParticleEmitter(x, y)
    emitter.set_burst_mode(True, 50, 0.1)
    emitter.set_particle_life(2.0)
    emitter.set_particle_speed(200.0)
    emitter.set_particle_size(4.0)
    emitter.set_particle_color(Color(255, 200, 0))
    emitter.set_emission_angle(0, 360)  # All directions
    emitter.set_gravity(0.0)
    emitter.set_friction(0.98)
    emitter.color_variation = 100.0
    emitter.size_variation = 0.8
    emitter.speed_variation = 0.5
    emitter.life_variation = 0.7
    emitter.enable_trail(True, 5)
    return emitter


def create_sparkle_effect(x: float, y: float) -> ParticleEmitter:
    """Create a sparkle particle effect"""
    emitter = ParticleEmitter(x, y)
    emitter.set_emission_rate(5.0)
    emitter.set_particle_life(3.0)
    emitter.set_particle_speed(30.0)
    emitter.set_particle_size(2.0)
    emitter.set_particle_color(Color(255, 255, 255))
    emitter.set_emission_angle(0, 360)
    emitter.set_gravity(0.0)
    emitter.set_friction(0.99)
    emitter.color_variation = 100.0
    emitter.size_variation = 0.3
    emitter.speed_variation = 0.2
    emitter.life_variation = 0.3
    return emitter


def create_smoke_effect(x: float, y: float) -> ParticleEmitter:
    """Create a smoke particle effect"""
    emitter = ParticleEmitter(x, y)
    emitter.set_emission_rate(8.0)
    emitter.set_particle_life(4.0)
    emitter.set_particle_speed(20.0)
    emitter.set_particle_size(8.0)
    emitter.set_particle_color(Color(100, 100, 100))
    emitter.set_emission_angle(270, 90)
    emitter.set_gravity(-20.0)
    emitter.set_friction(0.99)
    emitter.color_variation = 30.0
    emitter.size_variation = 0.8
    emitter.speed_variation = 0.4
    emitter.life_variation = 0.6
    return emitter


if __name__ == "__main__":
    # Test particle system
    print("🧪 Testing Particle System...")
    
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    
    # Create particle system
    particle_system = ParticleSystem()
    
    # Add some effects
    fire_emitter = create_fire_effect(400, 500)
    sparkle_emitter = create_sparkle_effect(200, 300)
    particle_system.add_emitter(fire_emitter)
    particle_system.add_emitter(sparkle_emitter)
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Create explosion at mouse position
                explosion = create_explosion_effect(event.pos[0], event.pos[1])
                particle_system.add_emitter(explosion)
        
        # Update particle system
        particle_system.update(dt)
        
        # Render
        screen.fill((0, 0, 0))
        particle_system.render(screen)
        pygame.display.flip()
    
    pygame.quit()
    print("✅ Particle system test completed!") 