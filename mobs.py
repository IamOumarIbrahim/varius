import pygame
import random
import math

class Mob:
    def __init__(self, x, y, mob_type):
        self.x = x
        self.y = y
        self.mob_type = mob_type  # SLIME, ZOMBIE, GUARD
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        
        # Base dimensions & stats
        if mob_type == "SLIME":
            self.width = 16
            self.height = 12
            self.max_health = 30
            self.max_posture = 25
            self.speed = 60
            self.damage = 10
            self.color = (50, 200, 50)
            self.xp_value = 15
        elif mob_type == "ZOMBIE":
            self.width = 14
            self.height = 26
            self.max_health = 60
            self.max_posture = 40
            self.speed = 45
            self.damage = 15
            self.color = (40, 120, 80)
            self.xp_value = 25
        elif mob_type == "GUARD":
            self.width = 16
            self.height = 26
            self.max_health = 100
            self.max_posture = 70
            self.speed = 30
            self.damage = 25
            self.color = (180, 50, 50)
            self.xp_value = 50

        self.health = self.max_health
        self.posture = self.max_posture
        
        # Timers / States
        self.stagger_timer = 0.0  # Stunned when posture is broken
        self.flash_timer = 0.0
        self.attack_cooldown = 0.0

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def take_damage(self, amount, posture_amount):
        if self.stagger_timer > 0:
            # Critical damage while staggered
            amount = int(amount * 1.5)
            
        self.health -= amount
        self.flash_timer = 0.15
        
        # Posture damage
        if self.stagger_timer <= 0:
            self.posture -= posture_amount
            if self.posture <= 0:
                self.stagger_timer = 1.5  # Stunned for 1.5s
                self.posture = 0
                self.flash_timer = 1.5 # Flash yellow during stagger

    def update(self, dt, player, world):
        # Handle staggering / stun
        if self.stagger_timer > 0:
            self.stagger_timer -= dt
            self.vx = 0
            if self.stagger_timer <= 0:
                self.posture = self.max_posture  # Restore posture after stun ends
        else:
            # Simple AI: Move towards player horizontally
            dx = player.x - self.x
            if abs(dx) > 10:
                self.vx = self.speed if dx > 0 else -self.speed
            else:
                self.vx = 0

        # Jump if moving against a solid wall
        if self.vx != 0 and self.on_ground:
            # Check a bit ahead
            check_x = self.x + (10 if self.vx > 0 else -10)
            check_ty = int((self.y + self.height - 4) / world.tile_size)
            check_tx = int(check_x / world.tile_size)
            if world.is_solid(check_tx, check_ty):
                self.vy = -260  # Jump!
                self.on_ground = False

        # Apply Gravity
        self.vy += 800 * dt
        if self.vy > 500:
            self.vy = 500
            
        # Timers
        if self.flash_timer > 0:
            self.flash_timer -= dt
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        # Physics collision resolution
        self.x += self.vx * dt
        rect = self.get_rect()
        collisions = world.check_tile_collision(rect)
        for tile_rect in collisions:
            if self.vx > 0:
                self.x = tile_rect.left - self.width
            elif self.vx < 0:
                self.x = tile_rect.right
        
        self.y += self.vy * dt
        rect = self.get_rect()
        collisions = world.check_tile_collision(rect)
        self.on_ground = False
        for tile_rect in collisions:
            if self.vy > 0:
                self.y = tile_rect.top - self.height
                self.vy = 0
                self.on_ground = True
            elif self.vy < 0:
                self.y = tile_rect.bottom
                self.vy = 0

    def draw(self, screen, camera_x, camera_y, zoom):
        draw_x = int(self.x * zoom - camera_x)
        draw_y = int(self.y * zoom - camera_y)
        w = int(self.width * zoom)
        h = int(self.height * zoom)
        
        # Color flash effects
        if self.stagger_timer > 0:
            # Stunned: Flash yellow
            color = (255, 255, 100) if int(self.stagger_timer * 10) % 2 == 0 else (200, 200, 50)
        elif self.flash_timer > 0:
            # Hit: Flash red
            color = (255, 100, 100)
        else:
            color = self.color
            
        # Draw mob shape
        if self.mob_type == "SLIME":
            # Round blob
            pygame.draw.ellipse(screen, color, (draw_x, draw_y, w, h))
            # Tiny eyes
            pygame.draw.circle(screen, (0, 0, 0), (draw_x + int(4*zoom), draw_y + int(4*zoom)), max(1, int(1*zoom)))
            pygame.draw.circle(screen, (0, 0, 0), (draw_x + int(10*zoom), draw_y + int(4*zoom)), max(1, int(1*zoom)))
        elif self.mob_type == "ZOMBIE":
            # Humanoid zombie
            pygame.draw.rect(screen, color, (draw_x, draw_y, w, h))
            # Red glowing eyes
            pygame.draw.rect(screen, (250, 50, 50), (draw_x + int(3*zoom), draw_y + int(4*zoom), int(2*zoom), int(2*zoom)))
            pygame.draw.rect(screen, (250, 50, 50), (draw_x + int(9*zoom), draw_y + int(4*zoom), int(2*zoom), int(2*zoom)))
        elif self.mob_type == "GUARD":
            # Heavy guard holding a shield
            pygame.draw.rect(screen, color, (draw_x, draw_y, w, h))
            # Draw heavy metal helmet and breastplate line
            pygame.draw.rect(screen, (120, 120, 120), (draw_x + int(2*zoom), draw_y, w - int(4*zoom), int(6*zoom)))
            # Large shield on their front side
            shield_x = draw_x + w - int(3*zoom) if self.vx >= 0 else draw_x - int(3*zoom)
            pygame.draw.rect(screen, (100, 100, 110), (shield_x, draw_y + int(4*zoom), int(6*zoom), int(18*zoom)))


class XPGem:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.radius = 4
        self.vy = 0
        self.magnetized = False

    def update(self, dt, player, world):
        # Magnet effect (Vampire Survivors magnet radius = 100 pixels)
        dx = player.x + player.width/2 - self.x
        dy = player.y + player.height/2 - self.y
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist < 120:
            self.magnetized = True
            
        if self.magnetized:
            # Fly towards player
            speed = 250
            self.x += (dx / dist) * speed * dt
            self.y += (dy / dist) * speed * dt
        else:
            # Gravity falls onto ground
            self.vy += 600 * dt
            if self.vy > 300:
                self.vy = 300
                
            self.y += self.vy * dt
            
            # Simple tile snap on floor collision
            rect = pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius*2, self.radius*2)
            collisions = world.check_tile_collision(rect)
            if collisions:
                self.y = collisions[0].top - self.radius
                self.vy = 0


class MobManager:
    def __init__(self, engine):
        self.engine = engine
        self.mobs = []
        self.gems = []
        self.spawn_timer = 0.0
        self.base_spawn_rate = 3.5  # Spawn every 3.5s at first

    def update(self, dt, world):
        player = self.engine.player
        
        # 1. Update Mob Spawning
        self.spawn_timer += dt
        # Mob spawn rate scales down (spawns faster) as time increases (Vampire Survivors style difficulty)
        current_spawn_rate = max(self.base_spawn_rate - (self.engine.survival_time * 0.01), 0.8)
        if self.spawn_timer >= current_spawn_rate:
            self.spawn_timer = 0.0
            self.spawn_wave(world)

        # 2. Update existing mobs
        for mob in self.mobs[:]:
            mob.update(dt, player, world)
            
            # Damage player on overlap
            mob_rect = mob.get_rect()
            if mob_rect.colliderect(player.get_rect()) and mob.attack_cooldown <= 0 and mob.stagger_timer <= 0:
                # Trigger combat parry window check!
                # If player is currently blocking, check if it's a parry, otherwise block/take dmg
                self.engine.combat_manager.check_incoming_hit(mob)
                
            # Remove dead mobs
            if mob.health <= 0:
                self.mobs.remove(mob)
                # Spawn gem
                self.gems.append(XPGem(mob.x + mob.width/2, mob.y + mob.height/2, mob.xp_value))
                
        # 3. Update Gems
        for gem in self.gems[:]:
            gem.update(dt, player, world)
            
            # Collect gem
            gem_rect = pygame.Rect(int(gem.x - gem.radius), int(gem.y - gem.radius), gem.radius*2, gem.radius*2)
            if gem_rect.colliderect(player.get_rect()):
                self.gems.remove(gem)
                player.add_xp(gem.value)

    def spawn_wave(self, world):
        player = self.engine.player
        
        # Determine wave composition based on survival time
        time = self.engine.survival_time
        num_to_spawn = 2 + int(time / 45) # Spawn larger swarms later
        
        for _ in range(num_to_spawn):
            # Spawn just outside screen (screen is 1024 wide, camera centers on player)
            # Offset left or right of the player
            side = random.choice([-1, 1])
            spawn_x = player.x + side * random.randint(550, 700)
            
            # Ensure within world boundaries
            spawn_x = max(16, min(spawn_x, world.width * world.tile_size - 32))
            
            # Find an empty vertical slot near the player's height
            player_ty = int(player.y / world.tile_size)
            spawn_tx = int(spawn_x / world.tile_size)
            
            # Look around player height for an air tile with solid ground
            spawn_ty = player_ty
            found_slot = False
            for dy in range(-10, 10):
                ty = player_ty + dy
                if world.get_tile(spawn_tx, ty) == world.AIR and world.is_solid(spawn_tx, ty + 1):
                    spawn_ty = ty
                    found_slot = True
                    break
            
            if found_slot:
                # Choose mob type based on time
                r = random.random()
                if time < 30:
                    m_type = "SLIME"
                elif time < 90:
                    m_type = "ZOMBIE" if r < 0.7 else "SLIME"
                else:
                    if r < 0.4:
                        m_type = "GUARD"
                    elif r < 0.8:
                        m_type = "ZOMBIE"
                    else:
                        m_type = "SLIME"
                
                self.mobs.append(Mob(spawn_tx * world.tile_size, spawn_ty * world.tile_size, m_type))

    def draw(self, screen, camera_x, camera_y, zoom):
        # Draw gems
        for gem in self.gems:
            draw_x = int(gem.x * zoom - camera_x)
            draw_y = int(gem.y * zoom - camera_y)
            r = int(gem.radius * zoom)
            # Draw as glowing cyan diamond
            pygame.draw.polygon(screen, (0, 220, 255), [
                (draw_x, draw_y - r),
                (draw_x + r, draw_y),
                (draw_x, draw_y + r),
                (draw_x - r, draw_y)
            ])
            # Draw white core
            pygame.draw.circle(screen, (255, 255, 255), (draw_x, draw_y), max(1, int(1*zoom)))

        # Draw mobs
        for mob in self.mobs:
            mob.draw(screen, camera_x, camera_y, zoom)
