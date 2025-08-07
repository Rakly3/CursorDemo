"""
Cursor IDE Demo Application
===========================

This is the main demo application that showcases the capabilities of Cursor IDE
through an impressive cross-platform Pygame application with advanced features
including platform detection, hardware optimization, particle effects, and more.

Author: Cursor IDE Demo
Version: 1.0.0
"""

import pygame
import sys
import time
import threading
import signal
from typing import Dict, Any, Optional, List
from pathlib import Path

# Import our custom modules
from system.platform_detector import get_platform_detector, get_optimization_settings
from config.config_manager import get_config_manager, get_config
from utils.logger import setup_logging, get_logger, log_demo_event
from utils.performance import get_performance_monitor, PerformanceProfiler
from utils.math_utils import clamp, lerp, random_range, ease_in_out
from utils.color_utils import Color, random_color, rainbow_colors, color_gradient
from frontend.particle_system import ParticleSystem, create_fire_effect, create_explosion_effect, create_sparkle_effect


class CursorDemoApp:
    """
    Main Cursor IDE Demo Application
    
    This class provides a comprehensive demo showcasing:
    - Cross-platform compatibility
    - Hardware optimization
    - Advanced graphics and effects
    - Performance monitoring
    - Interactive features
    - Professional code structure
    """
    
    def __init__(self):
        """Initialize the demo application"""
        # Set up logging first
        self.logger = setup_logging("CursorDemo", "INFO")
        self.logger.info("🚀 Starting Cursor IDE Demo Application...")
        
        # Initialize systems
        self._init_platform_detection()
        self._init_configuration()
        self._init_pygame()
        self._init_demo_components()
        
        # Application state
        self.running = True
        self.paused = False
        self.demo_time = 0.0
        self.demo_duration = get_config("Demo", "demo_duration", 30)
        
        # Performance monitoring
        self.performance_monitor = get_performance_monitor()
        self.performance_monitor.start()
        
        # Failsafe timeout
        self.failsafe_timer = 0.0
        self.failsafe_timeout = 60.0  # 60 seconds
        
        # Demo features
        self.current_scene = 0
        self.scene_timer = 0.0
        self.scene_duration = 5.0
        
        self.logger.info("✅ Demo application initialized successfully!")
    
    def _init_platform_detection(self) -> None:
        """Initialize platform detection system"""
        self.logger.info("🔍 Initializing platform detection...")
        
        with PerformanceProfiler("platform_detection"):
            self.platform_detector = get_platform_detector()
            self.hardware_info = self.platform_detector.get_hardware_info()
            self.optimization_settings = self.platform_detector.get_optimization_settings()
        
        self.logger.info(f"📱 Platform: {self.hardware_info.platform.value}")
        self.logger.info(f"🔧 Architecture: {self.hardware_info.architecture.value}")
        self.logger.info(f"⚡ High Performance: {self.hardware_info.is_high_performance}")
        
        # Log platform summary
        platform_summary = self.platform_detector.get_platform_summary()
        self.logger.info(f"Platform Summary:\n{platform_summary}")
    
    def _init_configuration(self) -> None:
        """Initialize configuration system"""
        self.logger.info("⚙️ Loading configuration...")
        
        with PerformanceProfiler("config_loading"):
            self.config_manager = get_config_manager()
        
        # Get display settings
        self.width = get_config("Display", "width", 1280)
        self.height = get_config("Display", "height", 720)
        self.fullscreen = get_config("Display", "fullscreen", False)
        self.vsync = get_config("Display", "vsync", True)
        self.target_fps = get_config("Display", "target_fps", 60)
        
        # Get graphics settings
        self.particle_count = get_config("Graphics", "particle_count", 1000)
        self.texture_quality = get_config("Graphics", "texture_quality", "high")
        self.bloom_effect = get_config("Graphics", "bloom_effect", True)
        
        # Get demo settings
        self.show_fps = get_config("Demo", "show_fps", True)
        self.show_platform_info = get_config("Demo", "show_platform_info", True)
        self.interactive_mode = get_config("Demo", "interactive_mode", True)
        
        self.logger.info(f"📐 Display: {self.width}x{self.height}")
        self.logger.info(f"🎯 Target FPS: {self.target_fps}")
        self.logger.info(f"✨ Particle Count: {self.particle_count}")
    
    def _init_pygame(self) -> None:
        """Initialize Pygame with platform-specific optimizations"""
        self.logger.info("🎮 Initializing Pygame...")
        
        with PerformanceProfiler("pygame_init"):
            pygame.init()
            
            # Set up display flags based on platform
            flags = pygame.RESIZABLE | pygame.DOUBLEBUF
            if self.fullscreen:
                flags |= pygame.FULLSCREEN
            if self.vsync:
                flags |= pygame.HWSURFACE
            
            # Create display
            self.screen = pygame.display.set_mode((self.width, self.height), flags)
            pygame.display.set_caption("Cursor IDE Demo - Cross-Platform Pygame Application")
            
            # Set up clock
            self.clock = pygame.time.Clock()
            
            # Initialize fonts
            self.fonts = {
                'small': pygame.font.Font(None, 24),
                'medium': pygame.font.Font(None, 36),
                'large': pygame.font.Font(None, 48),
                'title': pygame.font.Font(None, 72)
            }
        
        self.logger.info("✅ Pygame initialized successfully!")
    
    def _init_demo_components(self) -> None:
        """Initialize demo-specific components"""
        self.logger.info("🎨 Initializing demo components...")
        
        # Initialize particle system
        self.particle_system = ParticleSystem()
        
        # Create initial effects
        self._create_demo_effects()
        
        # Demo state
        self.mouse_pos = (0, 0)
        self.mouse_clicked = False
        self.key_pressed = None
        
        # Animation variables
        self.animation_time = 0.0
        self.background_color = Color(20, 20, 40)
        self.text_color = Color(255, 255, 255)
        
        # Scene management
        self.scenes = [
            self._scene_platform_demo,
            self._scene_particle_demo,
            self._scene_interactive_demo,
            self._scene_performance_demo,
            self._scene_cursor_features_demo
        ]
        
        self.logger.info("✅ Demo components initialized!")
    
    def _create_demo_effects(self) -> None:
        """Create initial particle effects for the demo"""
        # Create fire effect at bottom center
        fire_emitter = create_fire_effect(self.width // 2, self.height - 50)
        self.particle_system.add_emitter(fire_emitter)
        
        # Create sparkle effects around the screen
        for i in range(5):
            x = random_range(100, self.width - 100)
            y = random_range(100, self.height - 100)
            sparkle_emitter = create_sparkle_effect(x, y)
            self.particle_system.add_emitter(sparkle_emitter)
    
    def run(self) -> None:
        """Main application loop"""
        self.logger.info("🎬 Starting demo loop...")
        
        try:
            while self.running:
                # Handle events
                self._handle_events()
                
                # Update demo
                if not self.paused:
                    self._update_demo()
                
                # Render frame
                self._render_frame()
                
                # Update display
                pygame.display.flip()
                
                # Cap frame rate
                self.clock.tick(self.target_fps)
                
                # Check failsafe timeout
                self._check_failsafe()
            
        except Exception as e:
            self.logger.error(f"❌ Error in main loop: {e}")
            raise
        finally:
            self._cleanup()
    
    def _handle_events(self) -> None:
        """Handle Pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.logger.info("👋 User requested exit")
            
            elif event.type == pygame.KEYDOWN:
                self._handle_keydown(event.key)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_click(event.pos)
            
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
    
    def _handle_keydown(self, key: int) -> None:
        """Handle keyboard input"""
        if key == pygame.K_ESCAPE:
            self.running = False
            self.logger.info("👋 Escape key pressed - exiting")
        
        elif key == pygame.K_SPACE:
            self.paused = not self.paused
            status = "paused" if self.paused else "resumed"
            self.logger.info(f"⏸️ Demo {status}")
        
        elif key == pygame.K_r:
            self._reset_demo()
            self.logger.info("🔄 Demo reset")
        
        elif key == pygame.K_n:
            self._next_scene()
            self.logger.info("➡️ Next scene")
        
        elif key == pygame.K_p:
            self._prev_scene()
            self.logger.info("⬅️ Previous scene")
        
        elif key == pygame.K_e:
            # Create explosion at mouse position
            explosion = create_explosion_effect(self.mouse_pos[0], self.mouse_pos[1])
            self.particle_system.add_emitter(explosion)
            self.logger.info("💥 Explosion created")
        
        self.key_pressed = key
    
    def _handle_mouse_click(self, pos: tuple) -> None:
        """Handle mouse clicks"""
        self.mouse_clicked = True
        
        # Create explosion effect
        explosion = create_explosion_effect(pos[0], pos[1])
        self.particle_system.add_emitter(explosion)
        
        # Log interaction
        log_demo_event("mouse_click", x=pos[0], y=pos[1])
    
    def _update_demo(self) -> None:
        """Update demo state"""
        dt = self.clock.get_time() / 1000.0
        
        # Update timers
        self.demo_time += dt
        self.scene_timer += dt
        self.failsafe_timer += dt
        
        # Update animation time
        self.animation_time += dt
        
        # Update particle system
        self.particle_system.update(dt)
        
        # Update performance monitor
        self.performance_monitor.update_fps()
        
        # Check scene transition
        if self.scene_timer >= self.scene_duration:
            self._next_scene()
            self.scene_timer = 0.0
        
        # Update current scene
        if self.current_scene < len(self.scenes):
            self.scenes[self.current_scene](dt)
    
    def _render_frame(self) -> None:
        """Render the current frame"""
        # Clear screen with animated background
        self._render_background()
        
        # Render current scene
        if self.current_scene < len(self.scenes):
            self.scenes[self.current_scene](0.0)  # 0.0 for render-only
        
        # Render particle system
        self.particle_system.render(self.screen)
        
        # Render UI
        self._render_ui()
    
    def _render_background(self) -> None:
        """Render animated background"""
        # Create gradient background
        for y in range(self.height):
            ratio = y / self.height
            r = int(lerp(20, 40, ratio))
            g = int(lerp(20, 30, ratio))
            b = int(lerp(40, 60, ratio))
            
            # Add subtle animation
            anim_offset = int(10 * ease_in_out((self.animation_time * 0.5) % 1.0))
            r = clamp(r + anim_offset, 0, 255)
            g = clamp(g + anim_offset, 0, 255)
            b = clamp(b + anim_offset, 0, 255)
            
            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.width, y))
    
    def _render_ui(self) -> None:
        """Render user interface elements"""
        # Render FPS counter
        if self.show_fps:
            fps = self.performance_monitor.get_current_metrics().fps
            fps_text = self.fonts['small'].render(f"FPS: {fps:.1f}", True, self.text_color.to_rgb_tuple())
            self.screen.blit(fps_text, (10, 10))
        
        # Render platform info
        if self.show_platform_info:
            platform_text = self.fonts['small'].render(
                f"Platform: {self.hardware_info.platform.value.title()}", 
                True, self.text_color.to_rgb_tuple()
            )
            self.screen.blit(platform_text, (10, 40))
            
            arch_text = self.fonts['small'].render(
                f"Arch: {self.hardware_info.architecture.value.upper()}", 
                True, self.text_color.to_rgb_tuple()
            )
            self.screen.blit(arch_text, (10, 70))
        
        # Render demo info
        demo_text = self.fonts['small'].render(
            f"Demo Time: {self.demo_time:.1f}s / {self.demo_duration}s", 
            True, self.text_color.to_rgb_tuple()
        )
        self.screen.blit(demo_text, (10, 100))
        
        # Render scene info
        scene_text = self.fonts['small'].render(
            f"Scene: {self.current_scene + 1}/{len(self.scenes)}", 
            True, self.text_color.to_rgb_tuple()
        )
        self.screen.blit(scene_text, (10, 130))
        
        # Render controls
        controls = [
            "Controls:",
            "ESC - Exit",
            "SPACE - Pause/Resume",
            "R - Reset",
            "N/P - Next/Previous Scene",
            "E - Explosion",
            "Click - Explosion"
        ]
        
        for i, control in enumerate(controls):
            color = Color(200, 200, 200) if i == 0 else Color(150, 150, 150)
            control_text = self.fonts['small'].render(control, True, color.to_rgb_tuple())
            self.screen.blit(control_text, (self.width - 200, 10 + i * 25))
        
        # Render particle count
        particle_count = self.particle_system.get_total_particles()
        particle_text = self.fonts['small'].render(
            f"Particles: {particle_count}", 
            True, self.text_color.to_rgb_tuple()
        )
        self.screen.blit(particle_text, (10, 160))
    
    def _scene_platform_demo(self, dt: float) -> None:
        """Platform detection and optimization demo scene"""
        # Render title
        title = self.fonts['title'].render("Platform Detection Demo", True, self.text_color.to_rgb_tuple())
        title_rect = title.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Render platform information
        info_lines = [
            f"Platform: {self.hardware_info.platform.value.title()}",
            f"Architecture: {self.hardware_info.architecture.value.upper()}",
            f"CPU Cores: {self.hardware_info.cpu_count}",
            f"CPU Frequency: {self.hardware_info.cpu_frequency:.1f} MHz",
            f"Memory: {self.hardware_info.memory_total // (1024**3):.1f} GB",
            f"High Performance: {self.hardware_info.is_high_performance}",
            "",
            "Optimization Settings:",
            f"Target FPS: {self.optimization_settings.get('target_fps', 'N/A')}",
            f"Particle Count: {self.optimization_settings.get('particle_count', 'N/A')}",
            f"Hardware Acceleration: {self.optimization_settings.get('hardware_acceleration', 'N/A')}",
            f"Multithreading: {self.optimization_settings.get('multithreading', 'N/A')}"
        ]
        
        for i, line in enumerate(info_lines):
            color = Color(255, 255, 255) if i < 6 else Color(200, 200, 200)
            text = self.fonts['medium'].render(line, True, color.to_rgb_tuple())
            text_rect = text.get_rect(center=(self.width // 2, 200 + i * 40))
            self.screen.blit(text, text_rect)
    
    def _scene_particle_demo(self, dt: float) -> None:
        """Particle system demo scene"""
        # Render title
        title = self.fonts['title'].render("Particle System Demo", True, self.text_color.to_rgb_tuple())
        title_rect = title.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Render particle system info
        info_lines = [
            "Advanced Particle System Features:",
            "• Multiple particle emitters",
            "• Physics simulation (gravity, friction)",
            "• Color and size variation",
            "• Particle trails and effects",
            "• Performance optimized rendering",
            "",
            "Click anywhere to create explosions!",
            "Press 'E' for more explosions"
        ]
        
        for i, line in enumerate(info_lines):
            color = Color(255, 255, 255) if i == 0 else Color(200, 200, 200)
            text = self.fonts['medium'].render(line, True, color.to_rgb_tuple())
            text_rect = text.get_rect(center=(self.width // 2, 200 + i * 40))
            self.screen.blit(text, text_rect)
        
        # Add some automatic effects
        if random_range(0, 1) < 0.02:  # 2% chance per frame
            x = random_range(100, self.width - 100)
            y = random_range(100, self.height - 100)
            sparkle = create_sparkle_effect(x, y)
            self.particle_system.add_emitter(sparkle)
    
    def _scene_interactive_demo(self, dt: float) -> None:
        """Interactive features demo scene"""
        # Render title
        title = self.fonts['title'].render("Interactive Demo", True, self.text_color.to_rgb_tuple())
        title_rect = title.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Render interactive elements
        info_lines = [
            "Interactive Features:",
            "• Mouse tracking and clicking",
            "• Keyboard input handling",
            "• Real-time particle creation",
            "• Scene navigation",
            "• Performance monitoring",
            "",
            "Move your mouse and click!",
            "Try different keys for effects"
        ]
        
        for i, line in enumerate(info_lines):
            color = Color(255, 255, 255) if i == 0 else Color(200, 200, 200)
            text = self.fonts['medium'].render(line, True, color.to_rgb_tuple())
            text_rect = text.get_rect(center=(self.width // 2, 200 + i * 40))
            self.screen.blit(text, text_rect)
        
        # Draw mouse cursor trail
        if hasattr(self, 'mouse_trail'):
            self.mouse_trail.append(self.mouse_pos)
            if len(self.mouse_trail) > 20:
                self.mouse_trail.pop(0)
        else:
            self.mouse_trail = [self.mouse_pos]
        
        # Render mouse trail
        for i, pos in enumerate(self.mouse_trail):
            alpha = int(255 * (i / len(self.mouse_trail)))
            size = int(5 * (i / len(self.mouse_trail)))
            color = Color(255, 255, 255, alpha)
            
            trail_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, color.to_tuple(), (size, size), size)
            self.screen.blit(trail_surface, (pos[0] - size, pos[1] - size))
    
    def _scene_performance_demo(self, dt: float) -> None:
        """Performance monitoring demo scene"""
        # Render title
        title = self.fonts['title'].render("Performance Monitoring", True, self.text_color.to_rgb_tuple())
        title_rect = title.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Get performance metrics
        metrics = self.performance_monitor.get_current_metrics()
        summary = self.performance_monitor.get_performance_summary()
        
        # Render performance info
        info_lines = [
            "Real-time Performance Monitoring:",
            f"Current FPS: {metrics.fps:.1f}",
            f"Frame Time: {metrics.frame_time:.1f}ms",
            f"CPU Usage: {metrics.cpu_usage:.1f}%",
            f"Memory Usage: {metrics.memory_usage:.1f}%",
            f"Available Memory: {metrics.memory_available:.1f} GB",
            "",
            "Performance Alerts:",
            f"Low FPS: {summary['alerts']['low_fps']}",
            f"High CPU: {summary['alerts']['high_cpu']}",
            f"High Memory: {summary['alerts']['high_memory']}"
        ]
        
        for i, line in enumerate(info_lines):
            if i < 6:
                color = Color(255, 255, 255)
            elif i == 6:
                color = Color(255, 255, 0)
            else:
                # Safely extract alert key from line
                parts = line.split(': ')
                if len(parts) >= 2:
                    alert_key = parts[1].lower()
                    alert = summary['alerts'].get(alert_key, False)
                    color = Color(255, 100, 100) if alert else Color(100, 255, 100)
                else:
                    color = Color(100, 255, 100)  # Default to green if parsing fails
            
            text = self.fonts['medium'].render(line, True, color.to_rgb_tuple())
            text_rect = text.get_rect(center=(self.width // 2, 200 + i * 40))
            self.screen.blit(text, text_rect)
    
    def _scene_cursor_features_demo(self, dt: float) -> None:
        """Cursor IDE features demo scene"""
        # Render title
        title = self.fonts['title'].render("Cursor IDE Features", True, self.text_color.to_rgb_tuple())
        title_rect = title.get_rect(center=(self.width // 2, 100))
        self.screen.blit(title, title_rect)
        
        # Render Cursor IDE features
        info_lines = [
            "Why Choose Cursor IDE?",
            "• AI-powered code completion",
            "• Advanced refactoring tools",
            "• Intelligent debugging",
            "• Cross-platform development",
            "• Performance optimization",
            "• Professional code structure",
            "",
            "This demo showcases:",
            "• Clean, maintainable code",
            "• Platform-specific optimizations",
            "• Real-time performance monitoring",
            "• Interactive graphics and effects"
        ]
        
        for i, line in enumerate(info_lines):
            if i == 0:
                color = Color(255, 255, 0)
            elif i < 7:
                color = Color(255, 255, 255)
            elif i == 8:
                color = Color(100, 255, 100)
            else:
                color = Color(200, 200, 200)
            
            text = self.fonts['medium'].render(line, True, color.to_rgb_tuple())
            text_rect = text.get_rect(center=(self.width // 2, 200 + i * 40))
            self.screen.blit(text, text_rect)
    
    def _next_scene(self) -> None:
        """Move to next scene"""
        self.current_scene = (self.current_scene + 1) % len(self.scenes)
        self.scene_timer = 0.0
        log_demo_event("scene_change", scene=self.current_scene)
    
    def _prev_scene(self) -> None:
        """Move to previous scene"""
        self.current_scene = (self.current_scene - 1) % len(self.scenes)
        self.scene_timer = 0.0
        log_demo_event("scene_change", scene=self.current_scene)
    
    def _reset_demo(self) -> None:
        """Reset demo state"""
        self.demo_time = 0.0
        self.scene_timer = 0.0
        self.current_scene = 0
        self.particle_system.clear_all()
        self._create_demo_effects()
        log_demo_event("demo_reset")
    
    def _check_failsafe(self) -> None:
        """Check failsafe timeout"""
        if self.failsafe_timer > self.failsafe_timeout:
            self.logger.warning("⚠️ Failsafe timeout reached - exiting demo")
            self.running = False
    
    def _cleanup(self) -> None:
        """Clean up resources"""
        self.logger.info("🧹 Cleaning up demo application...")
        
        # Stop performance monitoring
        if hasattr(self, 'performance_monitor'):
            self.performance_monitor.stop()
        
        # Quit Pygame
        pygame.quit()
        
        self.logger.info("✅ Demo application cleanup completed!")
        log_demo_event("demo_exit", duration=self.demo_time)


def main():
    """Main entry point"""
    print("🎬 Starting Cursor IDE Demo Application...")
    print("=" * 60)
    
    try:
        # Create and run demo application
        app = CursorDemoApp()
        app.run()
        
    except KeyboardInterrupt:
        print("\n⚠️ Demo interrupted by user")
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("=" * 60)
        print("👋 Demo application finished")


if __name__ == "__main__":
    main()
