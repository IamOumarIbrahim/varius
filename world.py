import pygame
import random
import math

class World:
    # Tile constants
    AIR = 0
    DIRT = 1
    STONE = 2
    IRON = 3
    GOLD = 4
    COAL = 5
    GRASS = 6
    BEDROCK = 7
    CAGE = 10
    TORCH = 15

    # Colors
    TILE_COLORS = {
        AIR: (10, 10, 15),          # Dark background
        DIRT: (120, 80, 50),        # Brown
        STONE: (100, 100, 100),     # Grey
        IRON: (140, 120, 100),      # Grey-Orange
        GOLD: (180, 160, 50),       # Grey-Gold
        COAL: (40, 40, 40),         # Charcoal
        GRASS: (50, 150, 50),       # Green
        BEDROCK: (20, 20, 20),      # Dark charcoal
        CAGE: (200, 160, 40),       # Gold cage
        TORCH: (250, 180, 50)       # Torch warm orange
    }

    def __init__(self, width=160, height=80, tile_size=16):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.grid = [[self.AIR for _ in range(height)] for _ in range(width)]
        self.structures = []  # List of structures built above-ground
        
        # Cloud systems (Vampire Survivors sky environment)
        self.clouds = []
        for _ in range(16):
            self.clouds.append({
                "x": random.uniform(0, width * tile_size),
                "y": random.uniform(10, 180),
                "speed": random.uniform(6, 18),
                "w": random.uniform(60, 120),
                "h": random.uniform(22, 38)
            })
            
        self.generate_world()

    def generate_world(self):
        # Phase 1: Heightmap for surface
        surface_heights = []
        for x in range(self.width):
            h = 22 + int(4 * math.sin(x * 0.1) + 2 * math.sin(x * 0.03))
            surface_heights.append(h)

        # Seed initial noise below surface
        for x in range(self.width):
            for y in range(self.height):
                sh = surface_heights[x]
                if y < sh:
                    self.grid[x][y] = self.AIR
                elif y == sh:
                    self.grid[x][y] = self.GRASS
                elif y > sh and y < sh + 5:
                    if random.random() < 0.15:
                        self.grid[x][y] = self.AIR
                    else:
                        self.grid[x][y] = self.DIRT
                elif y >= sh + 5:
                    if random.random() < 0.46:
                        self.grid[x][y] = self.AIR
                    else:
                        r = random.random()
                        if r < 0.03:
                            self.grid[x][y] = self.COAL
                        elif r < 0.05:
                            self.grid[x][y] = self.IRON
                        elif r < 0.06:
                            self.grid[x][y] = self.GOLD
                        else:
                            self.grid[x][y] = self.STONE
                
                if y == self.height - 1:
                    self.grid[x][y] = self.BEDROCK

        # Phase 2: Cellular Automata cave smoothing
        for _ in range(4):
            temp_grid = [row[:] for row in self.grid]
            for x in range(1, self.width - 1):
                for y in range(15, self.height - 1):
                    solid_neighbors = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.width and 0 <= ny < self.height:
                                if temp_grid[nx][ny] not in [self.AIR, self.CAGE]:
                                    solid_neighbors += 1

                    if temp_grid[x][y] not in [self.AIR, self.CAGE]:
                        if solid_neighbors >= 4:
                            self.grid[x][y] = temp_grid[x][y]
                        else:
                            self.grid[x][y] = self.AIR
                    else:
                        if solid_neighbors >= 5:
                            self.grid[x][y] = self.STONE if y > 30 else self.DIRT

        # Place locked cages for NPCs in cave pockets
        cages_placed = 0
        attempts = 0
        while cages_placed < 5 and attempts < 120:
            cx = random.randint(10, self.width - 10)
            cy = random.randint(35, self.height - 5)
            if self.grid[cx][cy] == self.AIR and self.grid[cx][cy+1] in [self.STONE, self.DIRT]:
                self.grid[cx][cy] = self.CAGE
                cages_placed += 1
            attempts += 1

    def update_clouds(self, dt):
        world_w_px = self.width * self.tile_size
        for cloud in self.clouds:
            cloud["x"] += cloud["speed"] * dt
            if cloud["x"] > world_w_px:
                cloud["x"] = -cloud["w"]

    def get_tile(self, tx, ty):
        if tx < 0 or tx >= self.width:
            return self.BEDROCK
        if ty < 0:
            return self.AIR
        if ty >= self.height:
            return self.BEDROCK
        return self.grid[tx][ty]

    def set_tile(self, tx, ty, value):
        if 0 <= tx < self.width and 0 <= ty < self.height:
            if self.grid[tx][ty] != self.BEDROCK:
                self.grid[tx][ty] = value

    def is_solid(self, tx, ty):
        tile = self.get_tile(tx, ty)
        return tile not in [self.AIR, self.CAGE, self.TORCH]

    def check_tile_collision(self, rect):
        start_x = max(0, int(rect.left / self.tile_size))
        end_x = min(self.width, int(rect.right / self.tile_size) + 1)
        start_y = max(0, int(rect.top / self.tile_size))
        end_y = min(self.height, int(rect.bottom / self.tile_size) + 1)

        colliding_rects = []
        for tx in range(start_x, end_x):
            for ty in range(start_y, end_y):
                if self.is_solid(tx, ty):
                    tile_rect = pygame.Rect(
                        tx * self.tile_size,
                        ty * self.tile_size,
                        self.tile_size,
                        self.tile_size
                    )
                    if rect.colliderect(tile_rect):
                        colliding_rects.append(tile_rect)
        return colliding_rects

    def draw(self, screen, camera_x, camera_y, zoom):
        screen_w, screen_h = screen.get_size()
        rt_size = int(self.tile_size * zoom)
        
        # 1. Draw sky background (light sky blue)
        # Limit at ty = 25 where caves begin
        sky_limit_y = int(26 * self.tile_size * zoom - camera_y)
        if sky_limit_y > 0:
            pygame.draw.rect(screen, (135, 206, 235), (0, 0, screen_w, min(screen_h, sky_limit_y)))
            
            # Draw Sun in the background (with slow parallax scrolling)
            sun_x = int((100 * self.tile_size) * zoom - camera_x * 0.3)
            sun_y = int((8 * self.tile_size) * zoom - camera_y * 0.3)
            sun_radius = int(32 * zoom)
            
            # Sun glow rings
            if -sun_radius < sun_x < screen_w + sun_radius and -sun_radius < sun_y < screen_h + sun_radius:
                pygame.draw.circle(screen, (255, 255, 200), (sun_x, sun_y), int(sun_radius * 1.3), 0)
                pygame.draw.circle(screen, (255, 220, 50), (sun_x, sun_y), sun_radius, 0)
                # Rays
                for angle in range(0, 360, 45):
                    rad = math.radians(angle)
                    x1 = sun_x + int(math.cos(rad) * sun_radius * 1.1)
                    y1 = sun_y + int(math.sin(rad) * sun_radius * 1.1)
                    x2 = sun_x + int(math.cos(rad) * sun_radius * 1.4)
                    y2 = sun_y + int(math.sin(rad) * sun_radius * 1.4)
                    pygame.draw.line(screen, (255, 220, 50), (x1, y1), (x2, y2), int(3 * zoom))

            # Draw Clouds (with medium parallax scrolling)
            for cloud in self.clouds:
                cx = int(cloud["x"] * zoom - camera_x * 0.5)
                cy = int(cloud["y"] * zoom - camera_y * 0.5)
                cw = int(cloud["w"] * zoom)
                ch = int(cloud["h"] * zoom)
                
                # Check screen bounds before rendering
                if -cw < cx < screen_w and -ch < cy < screen_h:
                    # Draw overlapping circles to form a fluffy cloud
                    pygame.draw.ellipse(screen, (245, 248, 255), (cx, cy, cw, ch))
                    # Highlights
                    pygame.draw.ellipse(screen, (255, 255, 255), (cx + int(5*zoom), cy + int(4*zoom), int(cw*0.8), int(ch*0.8)))

        # 2. Draw tiles
        start_x = max(0, int(camera_x / rt_size))
        end_x = min(self.width, int((camera_x + screen_w) / rt_size) + 1)
        start_y = max(0, int(camera_y / rt_size))
        end_y = min(self.height, int((camera_y + screen_h) / rt_size) + 1)

        for tx in range(start_x, end_x):
            for ty in range(start_y, end_y):
                tile = self.grid[tx][ty]
                if tile == self.AIR:
                    continue

                draw_x = tx * rt_size - camera_x
                draw_y = ty * rt_size - camera_y

                color = self.TILE_COLORS.get(tile, (255, 0, 0))
                if tile != self.TORCH:
                    pygame.draw.rect(screen, color, (draw_x, draw_y, rt_size, rt_size))
                
                # Render details scaled by zoom
                s_size = int(3 * zoom)
                s_size = max(1, s_size)
                
                if tile == self.COAL:
                    pygame.draw.rect(screen, (0, 0, 0), (draw_x + int(3*zoom), draw_y + int(3*zoom), s_size, s_size))
                    pygame.draw.rect(screen, (0, 0, 0), (draw_x + int(9*zoom), draw_y + int(9*zoom), s_size, s_size))
                elif tile == self.IRON:
                    pygame.draw.rect(screen, (220, 130, 60), (draw_x + int(4*zoom), draw_y + int(2*zoom), s_size, s_size))
                    pygame.draw.rect(screen, (220, 130, 60), (draw_x + int(8*zoom), draw_y + int(8*zoom), s_size, s_size))
                elif tile == self.GOLD:
                    pygame.draw.rect(screen, (255, 215, 0), (draw_x + int(3*zoom), draw_y + int(4*zoom), s_size, s_size))
                    pygame.draw.rect(screen, (255, 215, 0), (draw_x + int(9*zoom), draw_y + int(2*zoom), s_size, s_size))
                elif tile == self.GRASS:
                    pygame.draw.rect(screen, (100, 220, 60), (draw_x, draw_y, rt_size, int(3 * zoom)))
                elif tile == self.CAGE:
                    pygame.draw.rect(screen, (120, 120, 120), (draw_x, draw_y, rt_size, rt_size), max(1, int(2 * zoom)))
                    for i in range(4, 16, 4):
                        pygame.draw.line(screen, (150, 150, 150), (draw_x + int(i*zoom), draw_y), (draw_x + int(i*zoom), draw_y + rt_size), 1)
                    pygame.draw.circle(screen, (255, 220, 100), (int(draw_x + 8*zoom), int(draw_y + 8*zoom)), int(3*zoom))
                elif tile == self.TORCH:
                    # Draw a nice torch stick
                    pygame.draw.rect(screen, (101, 67, 33), (draw_x + int(7*zoom), draw_y + int(6*zoom), int(2*zoom), int(10*zoom)))
                    # Animated flame
                    flame_offset = random.choice([-0.5, 0, 0.5]) * zoom
                    pygame.draw.circle(screen, (255, 120, 20), (int(draw_x + 8*zoom + flame_offset), int(draw_y + 4*zoom)), int(3*zoom))
                    pygame.draw.circle(screen, (255, 255, 100), (int(draw_x + 8*zoom + flame_offset), int(draw_y + 4*zoom)), int(1.5*zoom))

        # 3. Draw structures (base camp buildings) above-ground
        for struct in self.structures:
            stx = struct["tx"]
            sty = struct["ty"]
            stype = struct["type"]
            
            draw_x = stx * rt_size - camera_x
            draw_y = sty * rt_size - camera_y
            
            # Size: width 3 tiles (48px), height 2 tiles (32px)
            w_px = int(48 * zoom)
            h_px = int(32 * zoom)
            
            if -w_px < draw_x < screen_w and -h_px < draw_y < screen_h:
                if stype == "HOUSE":
                    # Log cabin: brown walls, red roof, door, glowing window
                    pygame.draw.rect(screen, (139, 90, 43), (draw_x, draw_y + int(10*zoom), w_px, h_px - int(10*zoom)))
                    pygame.draw.polygon(screen, (160, 40, 40), [
                        (draw_x - int(4*zoom), draw_y + int(10*zoom)),
                        (draw_x + w_px // 2, draw_y - int(4*zoom)),
                        (draw_x + w_px + int(4*zoom), draw_y + int(10*zoom))
                    ])
                    # Door
                    pygame.draw.rect(screen, (90, 50, 20), (draw_x + int(12*zoom), draw_y + h_px - int(16*zoom), int(10*zoom), int(16*zoom)))
                    # window
                    pygame.draw.rect(screen, (255, 220, 100), (draw_x + int(28*zoom), draw_y + int(14*zoom), int(10*zoom), int(8*zoom)))
                    pygame.draw.rect(screen, (60, 40, 20), (draw_x + int(28*zoom), draw_y + int(14*zoom), int(10*zoom), int(8*zoom)), 1)
                elif stype == "FORGE":
                    # Blacksmith Forge: stone furnace, chimney, glowing fire opening, anvil
                    pygame.draw.rect(screen, (90, 90, 95), (draw_x, draw_y + int(8*zoom), w_px, h_px - int(8*zoom)))
                    pygame.draw.rect(screen, (70, 70, 75), (draw_x + int(6*zoom), draw_y - int(4*zoom), int(10*zoom), int(12*zoom)))
                    # Opening
                    pygame.draw.rect(screen, (30, 30, 30), (draw_x + int(24*zoom), draw_y + h_px - int(18*zoom), int(16*zoom), int(18*zoom)))
                    # Fire flame
                    fire_h = int((8 + random.randint(0, 6)) * zoom)
                    pygame.draw.rect(screen, (255, 140, 0), (draw_x + int(26*zoom), draw_y + h_px - fire_h, int(12*zoom), fire_h))
                    pygame.draw.rect(screen, (255, 230, 50), (draw_x + int(29*zoom), draw_y + h_px - int(fire_h*0.6), int(6*zoom), int(fire_h*0.6)))
                    # Anvil
                    pygame.draw.rect(screen, (50, 50, 55), (draw_x + int(6*zoom), draw_y + h_px - int(10*zoom), int(12*zoom), int(6*zoom)))
                    pygame.draw.rect(screen, (50, 50, 55), (draw_x + int(8*zoom), draw_y + h_px - int(4*zoom), int(8*zoom), int(4*zoom)))
                elif stype == "LIBRARY":
                    # Scholar library: wooden building, blue roof, books window, scroll sign
                    pygame.draw.rect(screen, (200, 160, 110), (draw_x, draw_y + int(10*zoom), w_px, h_px - int(10*zoom)))
                    pygame.draw.polygon(screen, (40, 80, 150), [
                        (draw_x - int(2*zoom), draw_y + int(10*zoom)),
                        (draw_x + w_px // 2, draw_y - int(2*zoom)),
                        (draw_x + w_px + int(2*zoom), draw_y + int(10*zoom))
                    ])
                    # Books
                    pygame.draw.rect(screen, (80, 50, 30), (draw_x + int(8*zoom), draw_y + int(14*zoom), int(16*zoom), int(12*zoom)))
                    for by in range(16, 26, 4):
                        pygame.draw.line(screen, (220, 100, 50), (draw_x + int(9*zoom), draw_y + int(by*zoom)), (draw_x + int(22*zoom), draw_y + int(by*zoom)), 1)
                    # Sign
                    pygame.draw.rect(screen, (245, 222, 179), (draw_x + int(28*zoom), draw_y + int(14*zoom), int(12*zoom), int(6*zoom)))
                    pygame.draw.rect(screen, (0, 0, 0), (draw_x + int(28*zoom), draw_y + int(14*zoom), int(12*zoom), int(6*zoom)), 1)

    def draw_lighting(self, screen, camera_x, camera_y, zoom, player, mobs, combat_manager):
        screen_w, screen_h = screen.get_size()
        rt_size = int(self.tile_size * zoom)
        
        # 1. Create light mask surface
        light_mask = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        light_mask.fill((15, 15, 25, 255))  # Ambient dark caves
        
        # 2. Draw fully bright sky above caves (y < 26)
        sky_limit_y = int(26 * self.tile_size * zoom - camera_y)
        if sky_limit_y > 0:
            pygame.draw.rect(light_mask, (255, 255, 255, 255), (0, 0, screen_w, min(screen_h, sky_limit_y)))
            
        if not hasattr(self, "light_cache"):
            self.light_cache = {}
            
        def get_light_surf(radius, color=(255, 255, 255)):
            radius = int(radius)
            if radius <= 0:
                radius = 1
            key = (radius, color)
            if key not in self.light_cache:
                surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                for r in range(radius, 0, -2):
                    alpha = int(255 * (1.0 - r / radius) ** 1.5)
                    pygame.draw.circle(surf, (color[0], color[1], color[2], alpha), (radius, radius), r)
                self.light_cache[key] = surf
            return self.light_cache[key]
            
        # 3. Blit player light (always active)
        p_cx = int((player.x + player.width / 2) * zoom - camera_x)
        p_cy = int((player.y + player.height / 2) * zoom - camera_y)
        p_rad = int(160 * zoom)
        p_light = get_light_surf(p_rad)
        light_mask.blit(p_light, (p_cx - p_rad, p_cy - p_rad), special_flags=pygame.BLEND_RGBA_MAX)
        
        # 4. Blit torch lights (visible tiles only)
        start_x = max(0, int(camera_x / rt_size))
        end_x = min(self.width, int((camera_x + screen_w) / rt_size) + 1)
        start_y = max(0, int(camera_y / rt_size))
        end_y = min(self.height, int((camera_y + screen_h) / rt_size) + 1)
        
        t_rad = int(100 * zoom)
        
        for tx in range(start_x, end_x):
            for ty in range(start_y, end_y):
                if self.grid[tx][ty] == self.TORCH:
                    tx_c = int((tx * self.tile_size + 8) * zoom - camera_x)
                    ty_c = int((ty * self.tile_size + 8) * zoom - camera_y)
                    # Add tiny flickers to torch light radius
                    flicker_rad = t_rad + random.randint(-4, 4)
                    flicker_light = get_light_surf(flicker_rad, (255, 220, 150))
                    light_mask.blit(flicker_light, (tx_c - flicker_rad, ty_c - flicker_rad), special_flags=pygame.BLEND_RGBA_MAX)
                    
        # 5. Blit Gold ore lights (warm yellow glow)
        g_rad = int(32 * zoom)
        g_light = get_light_surf(g_rad, (255, 235, 120))
        for tx in range(start_x, end_x):
            for ty in range(start_y, end_y):
                if self.grid[tx][ty] == self.GOLD:
                    tx_c = int((tx * self.tile_size + 8) * zoom - camera_x)
                    ty_c = int((ty * self.tile_size + 8) * zoom - camera_y)
                    light_mask.blit(g_light, (tx_c - g_rad, ty_c - g_rad), special_flags=pygame.BLEND_RGBA_MAX)

        # 6. Blit Stance Ultimate lights or parry shield light if active
        if combat_manager.parry_active_timer > 0.0:
            sh_rad = int(80 * zoom)
            sh_light = get_light_surf(sh_rad, (120, 200, 255))
            light_mask.blit(sh_light, (p_cx - sh_rad, p_cy - sh_rad), special_flags=pygame.BLEND_RGBA_MAX)
            
        if getattr(combat_manager, "ultimate_water_shield_active", False):
            ts_rad = int(220 * zoom)
            ts_light = get_light_surf(ts_rad, (100, 180, 255))
            light_mask.blit(ts_light, (p_cx - ts_rad, p_cy - ts_rad), special_flags=pygame.BLEND_RGBA_MAX)

        # Draw SpitProjectiles
        for mob in mobs:
            if mob.mob_type == "SPITTER" and hasattr(mob, "projectiles"):
                for spit in mob.projectiles:
                    s_cx = int(spit.x * zoom - camera_x)
                    s_cy = int(spit.y * zoom - camera_y)
                    s_rad = int(24 * zoom)
                    s_light = get_light_surf(s_rad, (100, 255, 100))
                    light_mask.blit(s_light, (s_cx - s_rad, s_cy - s_rad), special_flags=pygame.BLEND_RGBA_MAX)
                    
        # Multiply light mask with the screen
        screen.blit(light_mask, (0, 0), special_flags=pygame.BLEND_MULT)
