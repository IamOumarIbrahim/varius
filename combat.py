import pygame
import math
import random

class WindSlash:
    def __init__(self, x, y, dx, dy, dmg, crit_rate, crit_dmg):
        self.x = x
        self.y = y
        self.vx = dx * 350
        self.vy = dy * 350
        self.width = 16
        self.height = 8
        self.damage = dmg
        self.crit_rate = crit_rate
        self.crit_dmg = crit_dmg
        self.lifetime = 1.5
        self.hit_mobs = set()

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt

    def get_rect(self):
        return pygame.Rect(int(self.x - self.width/2), int(self.y - self.height/2), self.width, self.height)


class CombatManager:
    def __init__(self, engine):
        self.engine = engine
        self.water_blade_count = 1
        self.water_blade_angle = 0.0
        self.water_blade_radius = 45
        self.water_blade_dmg_ratio = 0.6
        
        self.wind_slash_cooldown = 1.8
        self.wind_slash_timer = 0.0
        
        self.stone_sweep_cooldown = 1.2
        self.stone_sweep_timer = 0.0
        
        # Parry and Stun states
        self.parry_active_timer = 0.0
        self.parry_flash_timer = 0.0
        self.screen_shake = 0.0
        
        self.projectiles = []
        self.mob_blade_hit_cooldowns = {}

    def trigger_block_parry(self):
        player = self.engine.player
        self.parry_active_timer = player.stats["parry_window_ms"] / 1000.0

    def check_incoming_hit(self, mob):
        player = self.engine.player
        
        # 1. Perfect Parry!
        if self.parry_active_timer > 0.0:
            self.trigger_perfect_parry()
            mob.attack_cooldown = 1.2
            return
            
        # 2. Normal Block (if player is holding Space)
        keys = pygame.key.get_pressed()
        is_blocking = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]
        
        if is_blocking:
            # Reduce posture
            posture_damage = mob.damage * 0.8
            player.posture -= posture_damage
            
            # Spawn spark particles and play block sound
            self.engine.ui_manager.spawn_sparks(player.x + player.width/2, player.y + player.height/2, (150, 150, 150))
            self.engine.sound_manager.play("block")
            
            if player.posture <= 0:
                player.posture = 0
                player.flash_timer = 1.5  # Stagger flash
                # Stun player
                player.vy = -100
                player.vx = -100 if player.direction == 1 else 100
                
            mob.attack_cooldown = 1.5
            return
            
        # 3. Take Damage reduced by Armor
        armor = player.stats.get("armor", 0)
        damage_taken = max(1, mob.damage - armor)
        player.take_damage(damage_taken)
        mob.attack_cooldown = 1.5

    def trigger_perfect_parry(self):
        player = self.engine.player
        mobs = self.engine.mob_manager.mobs
        
        # Flash, shake, and sound
        self.parry_flash_timer = 0.12
        self.screen_shake = 0.4
        self.parry_active_timer = 0.0
        self.engine.sound_manager.play("parry")
        
        # Visual splash: parry ring
        parry_center_x = player.x + player.width/2
        parry_center_y = player.y + player.height/2
        
        # Perfect Parry deals massive posture and counter damage
        parry_radius = 120
        for mob in mobs[:]:
            dx = (mob.x + mob.width/2) - parry_center_x
            dy = (mob.y + mob.height/2) - parry_center_y
            dist = math.sqrt(dx**2 + dy**2)
            if dist <= parry_radius:
                is_crit = random.random() < player.stats["crit_rate"]
                dmg = player.stats["base_dmg"] * 2.2
                if is_crit:
                    dmg *= player.stats["crit_dmg"]
                
                mob.take_damage(int(dmg), mob.max_posture)
                
                # Knockback
                mob.vy = -150
                mob.vx = 250 if dx > 0 else -250
                self.engine.ui_manager.spawn_sparks(mob.x + mob.width/2, mob.y + mob.height/2, (255, 255, 255))
                
        self.engine.ui_manager.add_slash_effect(parry_center_x, parry_center_y, 80)

    def trigger_manual_swing(self):
        player = self.engine.player
        mobs = self.engine.mob_manager.mobs
        
        p_center_x = player.x + player.width/2
        p_center_y = player.y + player.height/2
        
        # Slicing bounding box range
        hit_w = 52
        hit_h = 36
        
        hit_rect = pygame.Rect(
            p_center_x if player.direction == 1 else p_center_x - hit_w,
            p_center_y - hit_h/2,
            hit_w,
            hit_h
        )
        
        # Visual spark trail
        self.engine.ui_manager.add_slash_effect(p_center_x + 24 * player.direction, p_center_y, 25)
        
        hit_any = False
        for mob in mobs[:]:
            if mob.get_rect().colliderect(hit_rect):
                is_crit = random.random() < player.stats["crit_rate"]
                
                # Stance specific details
                if player.stance == "STONE":
                    # Slow, heavy posture breaks
                    dmg = player.stats["base_dmg"] * 1.55
                    posture_dmg = 28
                    mob.vx = player.direction * 320
                    mob.vy = -160
                elif player.stance == "WATER":
                    # Water Stance manual strike
                    dmg = player.stats["base_dmg"] * 1.0
                    posture_dmg = 12
                    mob.vx = player.direction * 150
                    mob.vy = -90
                else: # WIND
                    # Wind stance manual strike
                    dmg = player.stats["base_dmg"] * 0.8
                    posture_dmg = 14
                    mob.vx = player.direction * 200
                    mob.vy = -110
                
                # Homelander's Fragile Ego damage scaling
                char_name = getattr(player, "char_name", "")
                if char_name == "Homelander":
                    hp_pct = player.health / player.stats["max_health"]
                    dmg = dmg * (1.0 + hp_pct)
                    
                if is_crit:
                    dmg *= player.stats["crit_dmg"]
                    
                mob.take_damage(int(dmg), posture_dmg)
                hit_any = True
                self.engine.ui_manager.spawn_sparks(mob.x + mob.width/2, mob.y + mob.height/2, (200, 220, 255))
                
        if hit_any:
            self.screen_shake = max(self.screen_shake, 0.12)
            self.engine.sound_manager.play("hit")

    def update(self, dt):
        player = self.engine.player
        mobs = self.engine.mob_manager.mobs
        
        # Timers
        if self.parry_active_timer > 0:
            self.parry_active_timer -= dt
        if self.parry_flash_timer > 0:
            self.parry_flash_timer -= dt
        if self.screen_shake > 0:
            self.screen_shake -= dt

        # Update mob water blade invulnerability cooldowns
        for mob in list(self.mob_blade_hit_cooldowns.keys()):
            self.mob_blade_hit_cooldowns[mob] -= dt
            if self.mob_blade_hit_cooldowns[mob] <= 0:
                del self.mob_blade_hit_cooldowns[mob]

        # --- WATER STANCE: Spinning Blades (Vampire Survivors style) ---
        if player.stance == "WATER" and self.water_blade_count > 0:
            self.water_blade_angle += 3.5 * dt
            p_center_x = player.x + player.width/2
            p_center_y = player.y + player.height/2
            
            for i in range(self.water_blade_count):
                angle = self.water_blade_angle + (i * (2 * math.pi / self.water_blade_count))
                bx = p_center_x + math.cos(angle) * self.water_blade_radius
                by = p_center_y + math.sin(angle) * self.water_blade_radius
                
                blade_rect = pygame.Rect(int(bx - 6), int(by - 6), 12, 12)
                for mob in mobs:
                    if mob.get_rect().colliderect(blade_rect):
                        if mob not in self.mob_blade_hit_cooldowns:
                            is_crit = random.random() < player.stats["crit_rate"]
                            dmg = player.stats["base_dmg"] * self.water_blade_dmg_ratio
                            if is_crit:
                                dmg *= player.stats["crit_dmg"]
                            
                            mob.take_damage(int(dmg), 8)
                            self.mob_blade_hit_cooldowns[mob] = 0.4
                            self.engine.ui_manager.spawn_sparks(bx, by, (100, 180, 255))

        # --- WIND STANCE: Autoshot Wind Slashes ---
        if player.stance == "WIND":
            self.wind_slash_timer += dt
            if self.wind_slash_timer >= self.wind_slash_cooldown:
                self.wind_slash_timer = 0.0
                
                closest_mob = None
                min_dist = 9999
                p_x, p_y = player.x + player.width/2, player.y + player.height/2
                for mob in mobs:
                    dist = math.sqrt((mob.x - p_x)**2 + (mob.y - p_y)**2)
                    if dist < min_dist:
                        min_dist = dist
                        closest_mob = mob
                
                if closest_mob:
                    dx = (closest_mob.x + closest_mob.width/2) - p_x
                    dy = (closest_mob.y + closest_mob.height/2) - p_y
                    dist = math.sqrt(dx**2 + dy**2)
                    dx /= dist
                    dy /= dist
                else:
                    dx = player.direction
                    dy = 0
                
                dmg = player.stats["base_dmg"] * 0.95
                self.projectiles.append(WindSlash(p_x, p_y, dx, dy, dmg, player.stats["crit_rate"], player.stats["crit_dmg"]))
                self.engine.sound_manager.play("swing")

        # Update slash projectiles
        for proj in self.projectiles[:]:
            proj.update(dt)
            proj_rect = proj.get_rect()
            
            for mob in mobs:
                if mob not in proj.hit_mobs and mob.get_rect().colliderect(proj_rect):
                    is_crit = random.random() < proj.crit_rate
                    dmg = proj.damage
                    if is_crit:
                        dmg *= proj.crit_dmg
                        
                    mob.take_damage(int(dmg), 14)
                    mob.vx = (1 if proj.vx > 0 else -1) * 150
                    proj.hit_mobs.add(mob)
                    self.engine.ui_manager.spawn_sparks(mob.x + mob.width/2, mob.y + mob.height/2, (220, 240, 255))
            
            if proj.lifetime <= 0:
                self.projectiles.remove(proj)

    def draw(self, screen, camera_x, camera_y, zoom):
        player = self.engine.player
        p_center_x = (player.x + player.width/2) * zoom - camera_x
        p_center_y = (player.y + player.height/2) * zoom - camera_y

        # Draw parry active shield indicator (timed visual)
        if self.parry_active_timer > 0.0:
            pygame.draw.circle(screen, (100, 200, 255), (int(p_center_x), int(p_center_y)), int(20 * zoom), max(1, int(2 * zoom)))

        # Draw Water orbital blades
        if player.stance == "WATER" and self.water_blade_count > 0:
            r = self.water_blade_radius * zoom
            for i in range(self.water_blade_count):
                angle = self.water_blade_angle + (i * (2 * math.pi / self.water_blade_count))
                bx = p_center_x + math.cos(angle) * r
                by = p_center_y + math.sin(angle) * r
                
                pygame.draw.circle(screen, (0, 150, 255), (int(bx), int(by)), int(5 * zoom))
                pygame.draw.circle(screen, (200, 240, 255), (int(bx), int(by)), int(2 * zoom))
                # Tail
                tail_bx = p_center_x + math.cos(angle - 0.15) * r
                tail_by = p_center_y + math.sin(angle - 0.15) * r
                pygame.draw.circle(screen, (0, 100, 200), (int(tail_bx), int(tail_by)), int(3 * zoom))

        # Draw Wind project slashes
        for proj in self.projectiles:
            dx = proj.vx
            dy = proj.vy
            length = math.sqrt(dx**2 + dy**2)
            if length > 0:
                dx /= length
                dy /= length
            
            draw_x = proj.x * zoom - camera_x
            draw_y = proj.y * zoom - camera_y
            
            angle = math.atan2(dy, dx)
            px = -dy * 8 * zoom
            py = dx * 8 * zoom
            pygame.draw.polygon(screen, (220, 240, 255), [
                (draw_x - dx*8*zoom, draw_y - dy*8*zoom),
                (draw_x + px, draw_y + py),
                (draw_x + dx*12*zoom, draw_y + dy*12*zoom),
                (draw_x - px, draw_y - py)
            ])
            pygame.draw.polygon(screen, (255, 255, 255), [
                (draw_x - dx*4*zoom, draw_y - dy*4*zoom),
                (draw_x + px*0.5, draw_y + py*0.5),
                (draw_x + dx*8*zoom, draw_y + dy*8*zoom),
                (draw_x - px*0.5, draw_y - py*0.5)
            ])
