import pygame
import math

class Player:
    def __init__(self, x, y, colors, engine):
        self.x = x
        self.y = y
        self.width = 14
        self.height = 26
        self.vx = 0
        self.vy = 0
        self.engine = engine
        
        self.on_ground = False
        self.direction = 1  # 1 = Right, -1 = Left
        self.colors = colors
        
        # Player attributes & stats (Cities/Tsushima stats)
        self.stats = {
            "max_health": 100,
            "max_posture": 100,
            "base_dmg": 20,
            "crit_rate": 0.10,
            "crit_dmg": 1.50,
            "haste": 1.0,           # Attack rate multiplier
            "mining_power": 1,      # Blocks required to mine
            "parry_window_ms": 200, # Block window for perfect parry
        }
        
        self.health = self.stats["max_health"]
        self.posture = self.stats["max_posture"]
        
        # Stance (Ghost of Tsushima influence)
        self.stance = "STONE"
        
        # Toolbar & Abilities (Vampire Survivors slot influence)
        self.toolbar = ["PICKAXE", "KATANA", "BLOCK", "TORCH", "WATER", "WIND"]
        self.active_slot = 0
        
        # Inventory & Equipment
        self.inventory = []
        self.equipped = {"HELMET": None, "RING": None, "CAPE": None}
        self.base_stats = None
        
        # Leveling & Progression (Vampire Survivors level up)
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        
        # Camera
        self.camera_x = 0
        self.camera_y = 0
        
        # Animation / Interaction state
        self.is_mining = False
        self.mining_cooldown = 0.0
        self.mine_target = None
        self.mine_timer = 0.0
        
        # Swing animation variables
        self.is_swinging = False
        self.swing_timer = 0.0
        
        # Damage flash
        self.flash_timer = 0.0

    def update(self, dt, world):
        zoom = self.engine.zoom
        
        # Apply Gravity
        self.vy += 800 * dt
        if self.vy > 500:
            self.vy = 500
            
        # Recover Posture slowly over time
        if self.posture < self.stats["max_posture"]:
            self.posture = min(self.posture + 15 * dt, self.stats["max_posture"])
            
        # Flash timer
        if self.flash_timer > 0:
            self.flash_timer -= dt

        # Swing timer
        if self.is_swinging:
            self.swing_timer -= dt
            if self.swing_timer <= 0:
                self.is_swinging = False

        # Character unique passive checks
        char_name = getattr(self, "char_name", "")
        if char_name == "Deadpool":
            self.health = min(self.health + (self.stats["max_health"] * 0.03) * dt, self.stats["max_health"])
        elif char_name == "Wednesday Addams":
            if not hasattr(self, "shockwave_timer"):
                self.shockwave_timer = 0.0
            self.shockwave_timer += dt
            if self.shockwave_timer >= 8.0:
                self.shockwave_timer = 0.0
                p_x = self.x + self.width/2
                p_y = self.y + self.height/2
                for mob in self.engine.mob_manager.mobs:
                    dx = mob.x + mob.width/2 - p_x
                    dy = mob.y + mob.height/2 - p_y
                    dist = math.sqrt(dx**2 + dy**2)
                    if dist < 150:
                        mob.speed = mob.speed * 0.65
                        mob.take_damage(12, 10)

        # Handle keyboard movement inputs
        keys = pygame.key.get_pressed()
        speed = 180 * self.stats.get("move_speed_mult", 1.0)
        if self.stance == "WIND":
            speed = 220 * self.stats.get("move_speed_mult", 1.0)
            
        self.vx = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vx = -speed
            self.direction = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vx = speed
            self.direction = 1
            
        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vy = -300
            self.on_ground = False

        # Physics collision check and resolution (unzoomed boundaries)
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

        # Mine block ticking
        if self.is_mining:
            self.mine_timer += dt
            mine_speed = 0.25 / self.stats["mining_power"]
            if self.mine_timer >= mine_speed:
                self.mine_timer = 0.0
                self.complete_mining(world)
        
        # Update camera (center on player in zoomed screen space)
        target_cam_x = self.x * zoom - 512
        target_cam_y = self.y * zoom - 384
        # Smooth camera scroll
        self.camera_x += (target_cam_x - self.camera_x) * 0.1
        self.camera_y += (target_cam_y - self.camera_y) * 0.1
        
        # Clamp camera to zoomed world bounds
        max_cam_x = world.width * world.tile_size * zoom - 1024
        max_cam_y = world.height * world.tile_size * zoom - 768
        self.camera_x = max(0, min(self.camera_x, max_cam_x))
        self.camera_y = max(0, min(self.camera_y, max_cam_y))

    def get_rect(self):
        return pygame.Rect(int(self.x), int(self.y), self.width, self.height)

    def handle_event(self, event, world):
        zoom = self.engine.zoom
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                # Trigger action based on active toolbar slot
                active_tool = self.toolbar[self.active_slot]
                
                # Target tile based on movement keys pressed at this moment
                keys = pygame.key.get_pressed()
                dx, dy = 0, 0
                if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                    dx = -1
                elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                    dx = 1
                
                if keys[pygame.K_w] or keys[pygame.K_UP]:
                    dy = -1
                elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                    dy = 1
                    
                # If stationary, default target direction to player's facing direction
                if dx == 0 and dy == 0:
                    dx = self.direction
                    
                player_tx = int((self.x + self.width/2) / world.tile_size)
                player_ty = int((self.y + self.height/2) / world.tile_size)
                
                # Determine absolute target block coordinates
                tx = player_tx + dx
                if dy == -1:
                    ty = int(self.y / world.tile_size) - 1 # above head
                elif dy == 1:
                    ty = int((self.y + self.height) / world.tile_size) # below feet
                else:
                    ty = int((self.y + self.height/2) / world.tile_size) # torso level
                
                if active_tool == "PICKAXE":
                    tile_type = world.get_tile(tx, ty)
                    if tile_type != world.AIR:
                        self.is_mining = True
                        self.mine_target = (tx, ty)
                        self.mine_timer = 0.0
                        self.is_swinging = True
                        self.swing_timer = 0.2
                        self.engine.sound_manager.play("mine")
                            
                elif active_tool == "KATANA":
                    # Swing sword counter attack
                    self.is_swinging = True
                    self.swing_timer = 0.25
                    self.engine.sound_manager.play("swing")
                    # Update facing direction dynamically based on action target
                    if dx != 0:
                        self.direction = dx
                    # Register manual sword attack hits in front
                    self.engine.combat_manager.trigger_manual_swing()
                    
                elif active_tool == "BLOCK":
                    tile_type = world.get_tile(tx, ty)
                    if tile_type == world.AIR and self.engine.iron >= 2:
                        # Verify not standing in it
                        placed_rect = pygame.Rect(tx*16, ty*16, 16, 16)
                        if not self.get_rect().colliderect(placed_rect):
                            world.set_tile(tx, ty, world.DIRT)
                            self.engine.iron -= 2
                            self.is_swinging = True
                            self.swing_timer = 0.15
                            self.engine.sound_manager.play("block")
                                
                elif active_tool == "TORCH":
                    tile_type = world.get_tile(tx, ty)
                    if tile_type == world.AIR:
                        world.set_tile(tx, ty, world.TORCH)
                        self.is_swinging = True
                        self.swing_timer = 0.15
                        self.engine.sound_manager.play("block")
                                
                elif active_tool == "WATER":
                    # Toggle Water stance active ability
                    self.change_stance("WATER")
                    self.is_swinging = True
                    self.swing_timer = 0.15
                    self.engine.sound_manager.play("click")
                    
                elif active_tool == "WIND":
                    # Toggle Wind stance active ability
                    self.change_stance("WIND")
                    self.is_swinging = True
                    self.swing_timer = 0.15
                    self.engine.sound_manager.play("click")

        # Releasing F stops mining
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_f:
                self.is_mining = False
                self.mine_target = None

    def complete_mining(self, world):
        if self.mine_target:
            tx, ty = self.mine_target
            tile_type = world.get_tile(tx, ty)
            
            if tile_type == world.CAGE:
                world.set_tile(tx, ty, world.AIR)
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "RESCUE_NPC"}))
            elif tile_type != world.AIR:
                world.set_tile(tx, ty, world.AIR)
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "MINE_BLOCK", "tile": tile_type}))
                
            self.is_mining = False
            self.mine_target = None

    def take_damage(self, amount):
        if self.flash_timer <= 0:
            self.health -= amount
            self.flash_timer = 0.25
            self.engine.sound_manager.play("hit")
            if self.health < 0:
                self.health = 0

    def add_xp(self, amount):
        self.xp += amount
        if self.xp >= self.xp_to_next:
            self.xp -= self.xp_to_next
            self.level += 1
            self.xp_to_next = int(self.xp_to_next * 1.3)
            self.engine.sound_manager.play("levelup")
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, {"action": "LEVEL_UP"}))

    def change_stance(self, new_stance):
        self.stance = new_stance

    def draw(self, screen, zoom):
        # Calculate zoomed screen position
        draw_x = int(self.x * zoom - self.camera_x)
        draw_y = int(self.y * zoom - self.camera_y)
        
        w = int(self.width * zoom)
        h = int(self.height * zoom)
        
        active_tool = self.toolbar[self.active_slot]
        
        # Call the new 4x detailed sprite drawer from the engine's ui_manager
        self.engine.ui_manager.draw_detailed_sprite(
            screen, draw_x, draw_y, self.colors, zoom * 4.0, 
            direction=self.direction, is_swinging=self.is_swinging, 
            active_tool=active_tool, stance=self.stance, 
            flash_red=(self.flash_timer > 0)
        )
        
        # 6. Draw Weapon (Katana or Lightsaber)
        sword_color = self.colors.get("saber_color", (200, 200, 200)) if self.colors.get("has_lightsaber") else (200, 200, 200)
        hilt_color = (139, 69, 19)
        
        bx = draw_x + int((12 if self.direction == 1 else -4)*zoom)
        
        if self.stance == "STONE":
            pygame.draw.line(screen, hilt_color, (bx, draw_y + int(12*zoom)), (bx, draw_y + int(8*zoom)), max(1, int(2*zoom)))
            pygame.draw.line(screen, sword_color, (bx, draw_y + int(8*zoom)), (bx + int(4*self.direction*zoom), draw_y - int(4*zoom)), max(1, int(2*zoom)))
        elif self.stance == "WATER":
            pygame.draw.line(screen, hilt_color, (bx, draw_y + int(14*zoom)), (bx + int(2*self.direction*zoom), draw_y + int(14*zoom)), max(1, int(2*zoom)))
            pygame.draw.line(screen, sword_color, (bx + int(2*self.direction*zoom), draw_y + int(14*zoom)), (bx + int(12*self.direction*zoom), draw_y + int(12*zoom)), max(1, int(2*zoom)))
        elif self.stance == "WIND":
            pygame.draw.line(screen, hilt_color, (bx, draw_y + int(10*zoom)), (bx + int(2*self.direction*zoom), draw_y + int(9*zoom)), max(1, int(2*zoom)))
            pygame.draw.line(screen, sword_color, (bx + int(2*self.direction*zoom), draw_y + int(9*zoom)), (bx + int(14*self.direction*zoom), draw_y + int(4*zoom)), max(1, int(2*zoom)))
            
        # 7. Swing Animation Arc
        if self.is_swinging:
            arc_col = (255, 255, 255, 200)
            if self.toolbar[self.active_slot] == "PICKAXE":
                arc_col = (200, 200, 220, 180)
            elif self.toolbar[self.active_slot] == "BLOCK":
                arc_col = (150, 100, 80, 150)
                
            arc_surf = pygame.Surface((int(40 * zoom), int(40 * zoom)), pygame.SRCALPHA)
            pygame.draw.circle(arc_surf, arc_col, (int(20*zoom), int(20*zoom)), int(16*zoom), max(1, int(2*zoom)))
            
            # Mask out half of the circle to make it a crescent arc
            if self.direction == 1:
                screen.blit(arc_surf, (draw_x + w - int(5*zoom), draw_y - int(8*zoom)), special_flags=pygame.BLEND_RGBA_ADD)
            else:
                screen.blit(arc_surf, (draw_x - int(25*zoom), draw_y - int(8*zoom)), special_flags=pygame.BLEND_RGBA_ADD)

        # Mining overlay (cracks) scaled
        if self.is_mining and self.mine_target:
            mtx, mty = self.mine_target
            rt_size = int(16 * zoom)
            mdx = mtx * rt_size - self.camera_x
            mdy = mty * rt_size - self.camera_y
            pygame.draw.line(screen, (255, 255, 255), (mdx + int(2*zoom), mdy + int(2*zoom)), (mdx + rt_size - int(2*zoom), mdy + rt_size - int(2*zoom)), 1)
            pygame.draw.line(screen, (255, 255, 255), (mdx + rt_size - int(2*zoom), mdy + int(2*zoom)), (mdx + int(2*zoom), mdy + rt_size - int(2*zoom)), 1)

    def recalculate_stats(self):
        if not getattr(self, "base_stats", None) or self.base_stats is None:
            self.base_stats = dict(self.stats)
            
        old_max_hp = self.stats["max_health"]
        self.stats = dict(self.base_stats)
        
        # Add equipped item stats
        for slot, item in self.equipped.items():
            if item is not None:
                for stat_name, stat_val in item["bonuses"].items():
                    if stat_name in self.stats:
                        self.stats[stat_name] += stat_val
                        
        # Adjust current health if max health changed
        if self.stats["max_health"] != old_max_hp:
            diff = self.stats["max_health"] - old_max_hp
            self.health = max(1, min(self.stats["max_health"], self.health + diff))

    def add_item_to_inventory(self, item):
        if len(self.inventory) < 16:
            self.inventory.append(item)
            return True
        return False

    def equip_item(self, item_index):
        if item_index < 0 or item_index >= len(self.inventory):
            return
        item = self.inventory[item_index]
        slot = item["slot"]
        
        currently_equipped = self.equipped[slot]
        self.equipped[slot] = item
        
        if currently_equipped is not None:
            self.inventory[item_index] = currently_equipped
        else:
            self.inventory.pop(item_index)
            
        self.recalculate_stats()

    def unequip_item(self, slot):
        item = self.equipped[slot]
        if item is not None:
            if len(self.inventory) < 16:
                self.inventory.append(item)
                self.equipped[slot] = None
                self.recalculate_stats()
                return True
        return False
