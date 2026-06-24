import pygame
import random
import math

class SpitProjectile:
    def __init__(self, x, y, dx, dy, dmg):
        self.x = x
        self.y = y
        self.vx = dx * 180
        self.vy = dy * 180
        self.width = 6
        self.height = 6
        self.damage = dmg
        self.lifetime = 3.0

    def update(self, dt, world):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt
        
        rect = self.get_rect()
        if world.check_tile_collision(rect):
            self.lifetime = 0

    def get_rect(self):
        return pygame.Rect(int(self.x - self.width/2), int(self.y - self.height/2), self.width, self.height)

    def draw(self, screen, camera_x, camera_y, zoom):
        draw_x = int(self.x * zoom - camera_x)
        draw_y = int(self.y * zoom - camera_y)
        r = int(3 * zoom)
        pygame.draw.circle(screen, (100, 255, 100), (draw_x, draw_y), r)
        pygame.draw.circle(screen, (255, 255, 255), (draw_x, draw_y), max(1, int(1*zoom)))


class ItemDrop:
    def __init__(self, x, y, item):
        self.x = x
        self.y = y
        self.item = item
        self.radius = 6
        self.vy = 0
        self.magnetized = False
        self.lifetime = 15.0

    def update(self, dt, player, world):
        self.lifetime -= dt
        dx = player.x + player.width/2 - self.x
        dy = player.y + player.height/2 - self.y
        dist = math.sqrt(dx**2 + dy**2)
        
        if dist < getattr(player, "stats", {}).get("magnet_range", 3.0) * 16 + 20:
            self.magnetized = True
            
        if self.magnetized:
            speed = 280
            self.x += (dx / dist) * speed * dt
            self.y += (dy / dist) * speed * dt
        else:
            self.vy += 600 * dt
            if self.vy > 300:
                self.vy = 300
            self.y += self.vy * dt
            
            rect = pygame.Rect(int(self.x - self.radius), int(self.y - self.radius), self.radius*2, self.radius*2)
            collisions = world.check_tile_collision(rect)
            if collisions:
                self.y = collisions[0].top - self.radius
                self.vy = 0

    def draw(self, screen, camera_x, camera_y, zoom):
        draw_x = int(self.x * zoom - camera_x)
        draw_y = int(self.y * zoom - camera_y)
        r = int(self.radius * zoom)
        
        colors = {
            "COMMON": (230, 230, 230),
            "RARE": (50, 150, 255),
            "EPIC": (160, 50, 240),
            "LEGENDARY": (255, 140, 0)
        }
        col = colors.get(self.item["rarity"], (255, 255, 255))
        
        pygame.draw.rect(screen, col, (draw_x - r, draw_y - r, r*2, r*2))
        pygame.draw.rect(screen, (30, 30, 30), (draw_x - r, draw_y - r, r*2, r*2), 1)
        pygame.draw.line(screen, (255, 215, 0), (draw_x - r + 1, draw_y), (draw_x + r - 1, draw_y), 1)


def generate_random_item(level=1):
    slots = ["HELMET", "RING", "CAPE"]
    slot = random.choice(slots)
    
    r_val = random.random()
    if r_val < 0.60:
        rarity = "COMMON"
        color = (230, 230, 230)
    elif r_val < 0.85:
        rarity = "RARE"
        color = (50, 150, 255)
    elif r_val < 0.97:
        rarity = "EPIC"
        color = (160, 50, 240)
    else:
        rarity = "LEGENDARY"
        color = (255, 140, 0)
        
    prefixes = ["Mythic", "Ancient", "Steel", "Crimson", "Shadow", "Golden", "Rusty"]
    suffixes = {
        "HELMET": ["Crown", "Great Helm", "Visor", "Cap"],
        "RING": ["Ring", "Band", "Signet", "Loop"],
        "CAPE": ["Cape", "Cloak", "Mantle", "Shroud"]
    }
    modifiers = {
        "HELMET": "of Vitality",
        "RING": "of Critical Eye",
        "CAPE": "of Swiftness"
    }
    
    name = f"{random.choice(prefixes)} {random.choice(suffixes[slot])} {modifiers[slot]}"
    
    bonuses = {}
    multiplier = {"COMMON": 1.0, "RARE": 1.6, "EPIC": 2.4, "LEGENDARY": 3.8}[rarity]
    
    if slot == "HELMET":
        bonuses["max_health"] = int(random.randint(10, 20) * multiplier)
        if rarity in ["RARE", "EPIC", "LEGENDARY"]:
            bonuses["armor"] = int(random.randint(1, 2) * (multiplier / 1.5))
    elif slot == "RING":
        bonuses["crit_rate"] = round(random.uniform(0.02, 0.05) * multiplier, 3)
        if rarity in ["EPIC", "LEGENDARY"]:
            bonuses["crit_dmg"] = round(random.uniform(0.08, 0.15) * multiplier, 2)
    elif slot == "CAPE":
        bonuses["move_speed_mult"] = round(random.uniform(0.04, 0.08) * multiplier, 2)
        if rarity in ["RARE", "EPIC", "LEGENDARY"]:
            bonuses["magnet_range"] = round(random.uniform(0.5, 1.2) * multiplier, 1)
            
    return {
        "name": name,
        "slot": slot,
        "rarity": rarity,
        "bonuses": bonuses,
        "color": color
    }


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
        elif mob_type == "SPITTER":
            self.width = 14
            self.height = 22
            self.max_health = 45
            self.max_posture = 30
            self.speed = 50
            self.damage = 8
            self.color = (140, 220, 80)
            self.xp_value = 30
            self.shoot_cooldown = 0.0
            self.projectiles = []
        elif mob_type == "SPIDER":
            self.width = 16
            self.height = 10
            self.max_health = 25
            self.max_posture = 15
            self.speed = 90
            self.damage = 12
            self.color = (150, 75, 0)
            self.xp_value = 20
            self.jump_cooldown = 0.0
        elif mob_type == "DEFENDER":
            self.width = 18
            self.height = 26
            self.max_health = 120
            self.max_posture = 90
            self.speed = 25
            self.damage = 20
            self.color = (100, 110, 120)
            self.xp_value = 60
        elif mob_type == "BAT":
            self.width = 14
            self.height = 12
            self.max_health = 20
            self.max_posture = 10
            self.speed = 75
            self.damage = 6
            self.color = (110, 60, 140)
            self.xp_value = 15

        self.health = self.max_health
        self.posture = self.max_posture
        
        # Timers / States
        self.stagger_timer = 0.0  # Stunned when posture is broken
        self.flash_timer = 0.0
        self.attack_cooldown = 0.0

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def take_damage(self, amount, posture_amount, source_x=None):
        if self.stagger_timer > 0:
            # Critical damage while staggered
            amount = int(amount * 1.5)
        elif self.mob_type == "DEFENDER" and source_x is not None:
            # Front shield blocks 75% of damage and posture damage if facing the attacker
            facing_source = (source_x > self.x and self.vx >= 0) or (source_x < self.x and self.vx <= 0)
            if facing_source:
                amount = int(amount * 0.25)
                posture_amount = int(posture_amount * 0.25)
            
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
            dx = player.x - self.x
            dy = player.y - self.y
            dist = math.sqrt(dx**2 + dy**2)
            
            if self.mob_type == "BAT":
                # Flying bat: flies directly towards player center, ignoring gravity
                if dist > 0:
                    self.vx = (dx / dist) * self.speed
                    self.vy = (dy / dist) * self.speed
                else:
                    self.vx, self.vy = 0, 0
            elif self.mob_type == "SPITTER":
                # Retreats if player is close, approaches if far, otherwise spits acid
                if dist < 140:
                    self.vx = -self.speed if dx > 0 else self.speed
                elif dist > 240:
                    self.vx = self.speed if dx > 0 else -self.speed
                else:
                    self.vx = 0
                
                # Ranged spit cooldown
                if hasattr(self, "shoot_cooldown"):
                    self.shoot_cooldown -= dt
                    if self.shoot_cooldown <= 0 and dist < 320:
                        self.shoot_cooldown = 2.0  # 2 seconds
                        sp_dx = dx / dist if dist > 0 else 1
                        sp_dy = dy / dist if dist > 0 else 0
                        self.projectiles.append(SpitProjectile(self.x + self.width/2, self.y + self.height/2, sp_dx, sp_dy, self.damage))
            elif self.mob_type == "SPIDER":
                # Crawls fast. Lunges forward if close and grounded
                if abs(dx) > 10:
                    self.vx = self.speed if dx > 0 else -self.speed
                else:
                    self.vx = 0
                
                if hasattr(self, "jump_cooldown"):
                    self.jump_cooldown -= dt
                    if self.jump_cooldown <= 0 and self.on_ground and abs(dx) < 120 and abs(dy) < 60:
                        self.jump_cooldown = 3.0  # 3s cooldown
                        self.vy = -240
                        self.vx = (self.speed * 1.6) if dx > 0 else -(self.speed * 1.6)
                        self.on_ground = False
            else:
                # ZOMBIE, SLIME, GUARD, DEFENDER
                if abs(dx) > 10:
                    self.vx = self.speed if dx > 0 else -self.speed
                else:
                    self.vx = 0

        # Jump if moving against a solid wall (Skip for BAT)
        if self.vx != 0 and self.on_ground and self.mob_type != "BAT":
            # Check a bit ahead
            check_x = self.x + (10 if self.vx > 0 else -10)
            check_ty = int((self.y + self.height - 4) / world.tile_size)
            check_tx = int(check_x / world.tile_size)
            if world.is_solid(check_tx, check_ty):
                self.vy = -260  # Jump!
                self.on_ground = False

        # Apply Gravity (Skip for BAT)
        if self.mob_type != "BAT":
            self.vy += 800 * dt
            if self.vy > 500:
                self.vy = 500
            
        # Timers
        if self.flash_timer > 0:
            self.flash_timer -= dt
        if self.attack_cooldown > 0:
            self.attack_cooldown -= dt

        # Update spitter projectiles
        if self.mob_type == "SPITTER" and hasattr(self, "projectiles"):
            for spit in self.projectiles[:]:
                spit.update(dt, world)
                if spit.get_rect().colliderect(player.get_rect()):
                    player.take_damage(self.damage)
                    spit.lifetime = 0
                if spit.lifetime <= 0:
                    self.projectiles.remove(spit)

        # Physics collision resolution
        self.x += self.vx * dt
        rect = self.get_rect()
        collisions = world.check_tile_collision(rect)
        for tile_rect in collisions:
            if self.vx > 0:
                self.x = tile_rect.left - self.width
            elif self.vx < 0:
                self.x = tile_rect.right
        
        # Only resolve vertical tile collision if not BAT (BAT can fly through tiles or we resolve it normally.
        # BAT ignores gravity and collisions to fly freely through cave walls - makes it highly dynamic bat!)
        if self.mob_type != "BAT":
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
        else:
            # For BAT, just simple flying movement
            self.y += self.vy * dt

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
        elif self.mob_type == "SPITTER":
            pygame.draw.rect(screen, color, (draw_x, draw_y, w, h))
            # Snout spitting direction
            snout_x = draw_x + w if self.vx >= 0 else draw_x - int(4*zoom)
            pygame.draw.rect(screen, (max(0, color[0]-35), max(0, color[1]-35), max(0, color[2]-35)), (snout_x, draw_y + int(6*zoom), int(4*zoom), int(6*zoom)))
            # Glowing acid eyes
            pygame.draw.rect(screen, (220, 220, 30), (draw_x + int(3*zoom), draw_y + int(3*zoom), int(2*zoom), int(2*zoom)))
            pygame.draw.rect(screen, (220, 220, 30), (draw_x + int(8*zoom), draw_y + int(3*zoom), int(2*zoom), int(2*zoom)))
        elif self.mob_type == "SPIDER":
            pygame.draw.ellipse(screen, color, (draw_x, draw_y, w, h))
            # Leg lines on sides
            for idx in range(3):
                offset_x = idx * int(4*zoom)
                pygame.draw.line(screen, (50, 30, 20), (draw_x + offset_x, draw_y + h//2), (draw_x + offset_x - int(4*zoom), draw_y + h + int(2*zoom)), max(1, int(1*zoom)))
                pygame.draw.line(screen, (50, 30, 20), (draw_x + w - offset_x, draw_y + h//2), (draw_x + w - offset_x + int(4*zoom), draw_y + h + int(2*zoom)), max(1, int(1*zoom)))
        elif self.mob_type == "DEFENDER":
            pygame.draw.rect(screen, color, (draw_x, draw_y, w, h))
            # Giant iron shield on front
            shield_x = draw_x + w - int(4*zoom) if self.vx >= 0 else draw_x - int(2*zoom)
            pygame.draw.rect(screen, (60, 65, 75), (shield_x, draw_y + int(2*zoom), int(6*zoom), h - int(4*zoom)))
            pygame.draw.rect(screen, (220, 220, 230), (shield_x, draw_y + int(2*zoom), int(6*zoom), h - int(4*zoom)), 1)
        elif self.mob_type == "BAT":
            # Bat wing flap animation
            wing_y = int(math.sin(pygame.time.get_ticks() * 0.025) * 5 * zoom)
            pygame.draw.polygon(screen, (max(0, color[0]-50), max(0, color[1]-50), max(0, color[2]-50)), [
                (draw_x, draw_y + h//2 + wing_y),
                (draw_x + w//4, draw_y + h//4),
                (draw_x + w//2, draw_y + h//2)
            ])
            pygame.draw.polygon(screen, (max(0, color[0]-50), max(0, color[1]-50), max(0, color[2]-50)), [
                (draw_x + w, draw_y + h//2 + wing_y),
                (draw_x + 3*w//4, draw_y + h//4),
                (draw_x + w//2, draw_y + h//2)
            ])
            pygame.draw.ellipse(screen, color, (draw_x + w//4, draw_y + h//4, w//2, h//2))
            # Glowing red eyes
            pygame.draw.circle(screen, (250, 30, 30), (draw_x + w//2, draw_y + h//3 + 1), max(1, int(1*zoom)))
            
        # Draw spit projectiles if any
        if self.mob_type == "SPITTER" and hasattr(self, "projectiles"):
            for spit in self.projectiles:
                spit.draw(screen, camera_x, camera_y, zoom)


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
        self.item_drops = []
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
                
                # 12% chance to drop randomized chest
                if random.random() < 0.12:
                    new_item = generate_random_item(player.level)
                    self.item_drops.append(ItemDrop(mob.x + mob.width/2, mob.y + mob.height/2, new_item))
                
        # 3. Update Gems
        for gem in self.gems[:]:
            gem.update(dt, player, world)
            
            # Collect gem
            gem_rect = pygame.Rect(int(gem.x - gem.radius), int(gem.y - gem.radius), gem.radius*2, gem.radius*2)
            if gem_rect.colliderect(player.get_rect()):
                self.gems.remove(gem)
                player.add_xp(gem.value)
                
        # 4. Update Item Drops
        for drop in self.item_drops[:]:
            drop.update(dt, player, world)
            
            # Collect chest
            drop_rect = pygame.Rect(int(drop.x - drop.radius), int(drop.y - drop.radius), drop.radius*2, drop.radius*2)
            if drop_rect.colliderect(player.get_rect()):
                self.item_drops.remove(drop)
                self.engine.sound_manager.play("block")
                added = player.add_item_to_inventory(drop.item)
                if added:
                    self.engine.ui_manager.add_loot_notification(drop.item)
            elif drop.lifetime <= 0:
                self.item_drops.remove(drop)

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
            
            # Choose mob type based on time
            r = random.random()
            if time < 35:
                m_type = "SLIME" if r < 0.75 else "BAT"
            elif time < 95:
                if r < 0.4:
                    m_type = "ZOMBIE"
                elif r < 0.7:
                    m_type = "SLIME"
                elif r < 0.85:
                    m_type = "SPIDER"
                else:
                    m_type = "BAT"
            else:
                if r < 0.25:
                    m_type = "GUARD"
                elif r < 0.45:
                    m_type = "DEFENDER"
                elif r < 0.65:
                    m_type = "ZOMBIE"
                elif r < 0.8:
                    m_type = "SPITTER"
                elif r < 0.9:
                    m_type = "SPIDER"
                else:
                    m_type = "BAT"

            if m_type == "BAT":
                # Bats spawn freely in the air
                self.mobs.append(Mob(spawn_tx * world.tile_size, player_ty * world.tile_size, m_type))
            else:
                # Find an empty slot near the player's height
                spawn_ty = player_ty
                found_slot = False
                for dy in range(-12, 12):
                    ty = player_ty + dy
                    if world.get_tile(spawn_tx, ty) == world.AIR and world.is_solid(spawn_tx, ty + 1):
                        spawn_ty = ty
                        found_slot = True
                        break
                if found_slot:
                    self.mobs.append(Mob(spawn_tx * world.tile_size, spawn_ty * world.tile_size, m_type))

    def draw(self, screen, camera_x, camera_y, zoom):
        # Draw gems
        for gem in self.gems:
            draw_x = int(gem.x * zoom - camera_x)
            draw_y = int(gem.y * zoom - camera_y)
            r = int(gem.radius * zoom)
            pygame.draw.polygon(screen, (0, 220, 255), [
                (draw_x, draw_y - r),
                (draw_x + r, draw_y),
                (draw_x, draw_y + r),
                (draw_x - r, draw_y)
            ])
            pygame.draw.circle(screen, (255, 255, 255), (draw_x, draw_y), max(1, int(1*zoom)))

        # Draw item drops
        for drop in self.item_drops:
            drop.draw(screen, camera_x, camera_y, zoom)

        # Draw mobs
        for mob in self.mobs:
            mob.draw(screen, camera_x, camera_y, zoom)
