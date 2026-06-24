import pygame
import math
import random
import os
import json

class Spark:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(50, 180)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.life = random.uniform(0.15, 0.4)
        self.max_life = self.life

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += 200 * dt
        self.life -= dt

    def draw(self, screen, camera_x, camera_y, zoom):
        draw_x = int(self.x * zoom - camera_x)
        draw_y = int(self.y * zoom - camera_y)
        size = max(1, int((2 if self.life < 0.2 else 3) * zoom))
        pygame.draw.rect(screen, self.color, (draw_x, draw_y, size, size))


class SlashEffect:
    def __init__(self, x, y, max_radius):
        self.x = x
        self.y = y
        self.radius = 5.0
        self.max_radius = max_radius
        self.life = 0.25
        self.max_life = self.life

    def update(self, dt):
        pct = (self.max_life - self.life) / self.max_life
        self.radius = 5.0 + pct * (self.max_radius - 5.0)
        self.life -= dt

    def draw(self, screen, camera_x, camera_y, zoom):
        draw_x = int(self.x * zoom - camera_x)
        draw_y = int(self.y * zoom - camera_y)
        color = (255, 255, 255) if self.life > 0.1 else (150, 220, 255)
        thickness = max(1, int((2 if self.life < 0.1 else 3) * zoom))
        pygame.draw.circle(screen, color, (draw_x, draw_y), int(self.radius * zoom), thickness)


class SettingsPanel:
    def __init__(self, engine):
        self.engine = engine
        self.font_title = pygame.font.SysFont("Courier", 22, bold=True)
        self.font_main = pygame.font.SysFont("Courier", 14)
        self.font_header = pygame.font.SysFont("Courier", 14, bold=True)
        
        # Sliders positions (X start, width, Y offset)
        self.slider_x = 380
        self.slider_w = 260
        
        # Save/load slot click zones
        self.buttons = []

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o or event.key == pygame.K_ESCAPE:
                self.engine.state = "PLAYING"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            self.handle_click(mouse_pos)
        elif event.type == pygame.MOUSEMOTION:
            # Handle dragging sliders
            if pygame.mouse.get_pressed()[0]:
                self.handle_slider_drag(event.pos)

    def handle_slider_drag(self, pos):
        mx, my = pos
        # Check if clicking horizontally near slider width
        if self.slider_x <= mx <= self.slider_x + self.slider_w:
            ratio = (mx - self.slider_x) / self.slider_w
            
            # Zoom slider (y=210)
            if 200 <= my <= 235:
                self.engine.zoom = round(1.0 + ratio * 1.5, 2)
            # SFX Volume slider (y=270)
            elif 260 <= my <= 295:
                sfx_vol = ratio
                self.engine.sound_manager.set_sfx_volume(sfx_vol)
            # Music Volume slider (y=330)
            elif 320 <= my <= 355:
                music_vol = ratio
                self.engine.sound_manager.set_music_volume(music_vol)

    def handle_click(self, pos):
        # 1. Trigger drag check first
        self.handle_slider_drag(pos)
        
        # 2. Check Save/Load slot buttons
        for btn in self.buttons:
            if btn["rect"].collidepoint(pos):
                slot = btn["slot"]
                act = btn["action"]
                
                if act == "SAVE":
                    self.engine.save_game(slot)
                    self.engine.sound_manager.play("click")
                elif act == "LOAD":
                    self.engine.load_game(slot)
                    self.engine.sound_manager.play("click")
                break

    def get_slot_metadata(self, slot_num):
        filename = f"save_slot_{slot_num}.json"
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
                lvl = data.get("player", {}).get("level", 1)
                t = data.get("survival_time", 0.0)
                m = int(t // 60)
                s = int(t % 60)
                return f"Lvl {lvl} - Time {m:02d}:{s:02d} - Gold {data.get('gold', 0)}"
            except Exception:
                return "Corrupt Data"
        return "Empty Slot"

    def draw(self, screen):
        # Transparency backdrop
        overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
        overlay.fill((20, 20, 30, 225))
        screen.blit(overlay, (0, 0))

        # Borders
        border_rect = pygame.Rect(180, 80, 664, 608)
        pygame.draw.rect(screen, (32, 38, 48), border_rect, 0, 8)
        pygame.draw.rect(screen, (80, 100, 130), border_rect, 3, 8)

        # Title
        t_surf = self.font_title.render("GAME SETTINGS & SAVE PROFILE PANEL", True, (255, 255, 255))
        screen.blit(t_surf, (512 - t_surf.get_width()//2, 100))
        
        guide = self.font_main.render("Adjust configurations and manage save states. Press [O] to Close Settings.", True, (150, 180, 200))
        screen.blit(guide, (512 - guide.get_width()//2, 134))

        # --- SLIDERS RENDERING ---
        # Slider 1: Render Zoom Scale (1.0x to 2.5x)
        ratio_zoom = (self.engine.zoom - 1.0) / 1.5
        self.draw_slider(screen, 215, "Zoom Scale", f"{self.engine.zoom:.2f}x", ratio_zoom)

        # Slider 2: SFX Volume
        ratio_sfx = self.engine.sound_manager.sfx_volume
        self.draw_slider(screen, 275, "SFX Volume", f"{int(ratio_sfx*100)}%", ratio_sfx)

        # Slider 3: Music Volume
        ratio_music = self.engine.sound_manager.music_volume
        self.draw_slider(screen, 335, "Music Volume", f"{int(ratio_music*100)}%", ratio_music)

        # --- 3-SLOT SAVE STATE MANAGER ---
        pygame.draw.line(screen, (60, 80, 110), (220, 380), (800, 380), 2)
        
        lbl_save = self.font_header.render("SAVE / LOAD GAME SLOTS", True, (255, 215, 0))
        screen.blit(lbl_save, (512 - lbl_save.get_width()//2, 395))

        self.buttons = []
        start_y = 430
        row_h = 65

        for slot in range(1, 4):
            curr_y = start_y + (slot - 1) * row_h
            
            # Slot Number Label
            s_label = self.font_header.render(f"Slot {slot}:", True, (255, 255, 255))
            screen.blit(s_label, (220, curr_y + 12))
            
            # Slot Metadata description
            meta = self.get_slot_metadata(slot)
            color = (130, 220, 150) if meta != "Empty Slot" else (150, 150, 150)
            meta_surf = self.font_main.render(meta, True, color)
            screen.blit(meta_surf, (310, curr_y + 12))

            # [SAVE BUTTON]
            btn_save = pygame.Rect(600, curr_y + 6, 80, 28)
            pygame.draw.rect(screen, (30, 60, 45), btn_save, 0, 4)
            pygame.draw.rect(screen, (100, 220, 130), btn_save, 1, 4)
            t_s = pygame.font.SysFont("Courier", 11, bold=True).render("SAVE", True, (255, 255, 255))
            screen.blit(t_s, (623, curr_y + 14))
            self.buttons.append({"rect": btn_save, "action": "SAVE", "slot": slot})

            # [LOAD BUTTON] (only highlight if exists)
            exists = meta != "Empty Slot"
            btn_load = pygame.Rect(695, curr_y + 6, 80, 28)
            bg_col = (40, 50, 65) if exists else (25, 25, 25)
            bd_col = (100, 180, 255) if exists else (70, 70, 70)
            tx_col = (255, 255, 255) if exists else (110, 110, 110)
            
            pygame.draw.rect(screen, bg_col, btn_load, 0, 4)
            pygame.draw.rect(screen, bd_col, btn_load, 1, 4)
            t_l = pygame.font.SysFont("Courier", 11, bold=True).render("LOAD", True, tx_col)
            screen.blit(t_l, (623 + 95, curr_y + 14))
            
            if exists:
                self.buttons.append({"rect": btn_load, "action": "LOAD", "slot": slot})

            # Dividing slots lines
            pygame.draw.line(screen, (40, 50, 65), (220, curr_y + row_h - 10), (800, curr_y + row_h - 10), 1)

    def draw_slider(self, screen, y, title, val_str, ratio):
        # Title Label
        lbl_surf = self.font_header.render(title, True, (220, 220, 220))
        screen.blit(lbl_surf, (220, y - 6))
        
        # Slider Line background
        pygame.draw.line(screen, (50, 60, 80), (self.slider_x, y), (self.slider_x + self.slider_w, y), 6)
        # Slider Line filled portion
        pygame.draw.line(screen, (0, 200, 255), (self.slider_x, y), (self.slider_x + int(self.slider_w * ratio), y), 6)
        
        # Sliding knob circle
        knob_x = self.slider_x + int(self.slider_w * ratio)
        pygame.draw.circle(screen, (255, 255, 255), (knob_x, y), 8)
        pygame.draw.circle(screen, (0, 150, 255), (knob_x, y), 5)

        # Value text string representation
        val_surf = self.font_header.render(val_str, True, (255, 215, 0))
        screen.blit(val_surf, (self.slider_x + self.slider_w + 20, y - 6))


class TownPanel:
    def __init__(self, engine):
        self.engine = engine
        self.font_title = pygame.font.SysFont("Courier", 22, bold=True)
        self.font_main = pygame.font.SysFont("Courier", 14)
        self.font_header = pygame.font.SysFont("Courier", 14, bold=True)
        
        self.buttons = []

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_t or event.key == pygame.K_ESCAPE:
                self.engine.state = "PLAYING"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            self.handle_click(mouse_pos)

    def handle_click(self, mouse_pos):
        for btn in self.buttons:
            if btn["rect"].collidepoint(mouse_pos):
                action = btn["action"]
                npc = btn["npc"]
                
                self.engine.sound_manager.play("click")
                if action == "ASSIGN_MINER":
                    npc["job"] = "Miner"
                elif action == "ASSIGN_BLACKSMITH":
                    npc["job"] = "Blacksmith"
                elif action == "ASSIGN_SCHOLAR":
                    npc["job"] = "Scholar"
                elif action == "LEVEL_UP":
                    cost = npc["level"] * 50
                    if self.engine.gold >= cost:
                        self.engine.gold -= cost
                        npc["level"] += 1
                
                self.engine.tick_town_simulation()
                break

    def draw(self, screen):
        overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
        overlay.fill((10, 20, 15, 230))
        screen.blit(overlay, (0, 0))

        border_rect = pygame.Rect(64, 48, 896, 672)
        pygame.draw.rect(screen, (25, 40, 30), border_rect, 0, 8)
        pygame.draw.rect(screen, (60, 110, 80), border_rect, 3, 8)

        title_surf = self.font_title.render("TOWN HALL - BASE CAMP COLONY SIMULATOR", True, (255, 255, 255))
        screen.blit(title_surf, (80, 64))
        
        info_surf = self.font_main.render("Rescue caged captives from caves to expand your colony population. Press [T] to Close.", True, (150, 200, 170))
        screen.blit(info_surf, (80, 94))

        gold_text = f"Gold: {self.engine.gold} (+{self.engine.gold_per_sec}/s)"
        iron_text = f"Iron: {self.engine.iron} (+{self.engine.iron_per_sec}/s)"
        schol_text = f"Scholar Pts: {self.engine.scholar_pts} (+{self.engine.scholar_pts_per_sec}/s)"
        
        g_surf = self.font_header.render(gold_text, True, (255, 215, 0))
        i_surf = self.font_header.render(iron_text, True, (200, 200, 220))
        s_surf = self.font_header.render(schol_text, True, (100, 220, 255))
        
        screen.blit(g_surf, (80, 130))
        screen.blit(i_surf, (340, 130))
        screen.blit(s_surf, (600, 130))

        npc_box_rect = pygame.Rect(80, 170, 864, 510)
        pygame.draw.rect(screen, (15, 25, 20), npc_box_rect)
        pygame.draw.rect(screen, (40, 70, 50), npc_box_rect, 2)
        
        headers = self.font_header.render("Survivor Name           Level    Current Job      Assign New Job / Upgrades", True, (200, 200, 200))
        screen.blit(headers, (95, 185))
        pygame.draw.line(screen, (40, 70, 50), (80, 210), (944, 210), 2)

        self.buttons = []

        if not self.engine.rescued_npcs:
            empty_surf = self.font_main.render("No survivors rescued yet! Explore the caves and break caged cells to rescue villagers.", True, (130, 160, 140))
            screen.blit(empty_surf, (120, 250))
            return

        start_y = 220
        row_h = 55
        
        for idx, npc in enumerate(self.engine.rescued_npcs):
            curr_y = start_y + idx * row_h
            if curr_y + row_h > 660:
                break

            name_surf = self.font_main.render(npc["name"], True, (255, 255, 255))
            level_surf = self.font_main.render(f"Lvl {npc['level']}", True, (255, 215, 0))
            job_surf = self.font_main.render(npc["job"], True, (120, 220, 255) if npc["job"] != "Unassigned" else (150, 150, 150))
            
            screen.blit(name_surf, (100, curr_y + 16))
            screen.blit(level_surf, (330, curr_y + 16))
            screen.blit(job_surf, (410, curr_y + 16))

            jobs = [("Miner", "ASSIGN_MINER", (200, 200, 220)), 
                    ("Smith", "ASSIGN_BLACKSMITH", (220, 160, 80)), 
                    ("Scholar", "ASSIGN_SCHOLAR", (100, 200, 250))]
            
            btn_x = 550
            for j_title, j_act, j_col in jobs:
                btn_rect = pygame.Rect(btn_x, curr_y + 10, 75, 28)
                pygame.draw.rect(screen, (30, 50, 40), btn_rect, 0, 4)
                pygame.draw.rect(screen, j_col, btn_rect, 1, 4)
                
                if npc["job"] == j_title or (j_title == "Smith" and npc["job"] == "Blacksmith"):
                    pygame.draw.rect(screen, (j_col[0]//2, j_col[1]//2, j_col[2]//2), btn_rect, 0, 4)
                
                j_surf = pygame.font.SysFont("Courier", 11, bold=True).render(j_title, True, (255, 255, 255))
                screen.blit(j_surf, (btn_x + 8, curr_y + 18))
                
                self.buttons.append({"rect": btn_rect, "action": j_act, "npc": npc})
                btn_x += 85

            upg_cost = npc["level"] * 50
            upg_btn_rect = pygame.Rect(btn_x + 10, curr_y + 10, 100, 28)
            can_afford = self.engine.gold >= upg_cost
            
            pygame.draw.rect(screen, (40, 30, 20) if can_afford else (30, 30, 30), upg_btn_rect, 0, 4)
            pygame.draw.rect(screen, (255, 180, 50) if can_afford else (100, 100, 100), upg_btn_rect, 1, 4)
            
            upg_text = f"Level+ ({upg_cost}g)"
            u_surf = pygame.font.SysFont("Courier", 10, bold=True).render(upg_text, True, (255, 255, 255) if can_afford else (130, 130, 130))
            screen.blit(u_surf, (btn_x + 15, curr_y + 18))
            
            self.buttons.append({"rect": upg_btn_rect, "action": "LEVEL_UP", "npc": npc})
            pygame.draw.line(screen, (25, 45, 30), (80, curr_y + row_h), (944, curr_y + row_h), 1)


class UIManager:
    def __init__(self, engine):
        self.engine = engine
        self.settings_panel = SettingsPanel(engine)
        self.town_panel = TownPanel(engine)
        
        self.font_hud = pygame.font.SysFont("Courier", 14, bold=True)
        self.font_large = pygame.font.SysFont("Courier", 32, bold=True)
        self.font_sub = pygame.font.SysFont("Courier", 18)
        
        self.sparks = []
        self.slashes = []
        self.customizer_buttons = []

    def spawn_sparks(self, x, y, color):
        for _ in range(random.randint(6, 12)):
            self.sparks.append(Spark(x, y, color))

    def add_slash_effect(self, x, y, max_radius):
        self.slashes.append(SlashEffect(x, y, max_radius))

    # --- CUSTOMIZER SCREEN ---
    def draw_customizer(self, screen):
        screen.fill((15, 15, 22))
        
        t_surf = self.font_large.render("CAVE SURVIVOR: TSUSHIMA STANCES", True, (255, 255, 255))
        screen.blit(t_surf, (512 - t_surf.get_width()//2, 80))
        
        sub_surf = self.font_sub.render("Character Customizer & Custom Sprite Profile Generator", True, (150, 180, 200))
        screen.blit(sub_surf, (512 - sub_surf.get_width()//2, 125))

        preview_box = pygame.Rect(180, 220, 240, 280)
        pygame.draw.rect(screen, (30, 35, 45), preview_box, 0, 12)
        pygame.draw.rect(screen, (70, 90, 120), preview_box, 3, 12)
        
        px = 300 - 42
        py = 360 - 78
        
        colors = self.engine.custom_colors
        pygame.draw.rect(screen, colors["pants"], (px + 12, py + 96, 60, 48))
        pygame.draw.rect(screen, (30, 30, 30), (px + 6, py + 144, 24, 12))
        pygame.draw.rect(screen, (30, 30, 30), (px + 54, py + 144, 24, 12))
        pygame.draw.rect(screen, colors["shirt"], (px + 6, py + 48, 72, 48))
        pygame.draw.rect(screen, colors["skin"], (px + 18, py + 6, 48, 42))
        pygame.draw.rect(screen, colors["eyes"], (px + 42, py + 18, 12, 12))
        pygame.draw.rect(screen, colors["hair"], (px + 12, py - 6, 60, 12))
        pygame.draw.rect(screen, colors["hair"], (px + 48, py + 6, 12, 24))

        labels = [
            ("Hair Style/Color", "hair"),
            ("Skin Tone/Face", "skin"),
            ("Outfit Shirt", "shirt"),
            ("Outfit Pants", "pants"),
            ("Eye Color", "eyes")
        ]
        
        self.customizer_buttons = []
        start_y = 230
        
        for idx, (label, key) in enumerate(labels):
            curr_y = start_y + idx * 55
            
            lbl_surf = self.font_sub.render(label, True, (220, 220, 220))
            screen.blit(lbl_surf, (480, curr_y + 8))
            
            l_rect = pygame.Rect(700, curr_y + 4, 35, 30)
            pygame.draw.rect(screen, (40, 50, 65), l_rect, 0, 4)
            pygame.draw.rect(screen, (80, 100, 130), l_rect, 1, 4)
            arrow_l = pygame.font.SysFont("Courier", 18, bold=True).render("<", True, (255, 255, 255))
            screen.blit(arrow_l, (712, curr_y + 8))
            
            box_rect = pygame.Rect(750, curr_y + 4, 50, 30)
            pygame.draw.rect(screen, colors[key], box_rect, 0, 4)
            pygame.draw.rect(screen, (255, 255, 255), box_rect, 2, 4)
            
            r_rect = pygame.Rect(815, curr_y + 4, 35, 30)
            pygame.draw.rect(screen, (40, 50, 65), r_rect, 0, 4)
            pygame.draw.rect(screen, (80, 100, 130), r_rect, 1, 4)
            arrow_r = pygame.font.SysFont("Courier", 18, bold=True).render(">", True, (255, 255, 255))
            screen.blit(arrow_r, (827, curr_y + 8))
            
            self.customizer_buttons.append({"rect": l_rect, "action": "PREV", "key": key})
            self.customizer_buttons.append({"rect": r_rect, "action": "NEXT", "key": key})

        start_btn = pygame.Rect(384, 590, 256, 50)
        pygame.draw.rect(screen, (30, 80, 50), start_btn, 0, 8)
        pygame.draw.rect(screen, (100, 220, 130), start_btn, 3, 8)
        btn_txt = self.font_hud.render("START GAME [ENTER]", True, (255, 255, 255))
        screen.blit(btn_txt, (512 - btn_txt.get_width()//2, 606))
        self.customizer_buttons.append({"rect": start_btn, "action": "START", "key": None})

    def handle_customizer_click(self, mouse_pos):
        for btn in self.customizer_buttons:
            if btn["rect"].collidepoint(mouse_pos):
                action = btn["action"]
                key = btn["key"]
                
                self.engine.sound_manager.play("click")
                if action == "START":
                    self.engine.start_game()
                else:
                    options = self.engine.custom_options[key]
                    idx = self.engine.custom_indices[key]
                    if action == "PREV":
                        idx = (idx - 1) % len(options)
                    elif action == "NEXT":
                        idx = (idx + 1) % len(options)
                    self.engine.custom_indices[key] = idx
                    self.engine.custom_colors[key] = options[idx]
                break

    # --- HUD & PLAYING DRAW ---
    def draw_hud(self, screen):
        p = self.engine.player
        zoom = self.engine.zoom
        
        # Camera shake calculations
        cam_shake_x = 0
        cam_shake_y = 0
        if self.engine.combat_manager.screen_shake > 0:
            intensity = int(self.engine.combat_manager.screen_shake * 12)
            cam_shake_x = random.randint(-intensity, intensity)
            cam_shake_y = random.randint(-intensity, intensity)
        
        cx = p.camera_x + cam_shake_x
        cy = p.camera_y + cam_shake_y
        
        # Render particles/sparks scaled by zoom
        for slash in self.slashes[:]:
            slash.update(self.engine.clock.get_time() / 1000.0)
            slash.draw(screen, cx, cy, zoom)
            if slash.life <= 0:
                self.slashes.remove(slash)
                
        for spark in self.sparks[:]:
            spark.update(self.engine.clock.get_time() / 1000.0)
            spark.draw(screen, cx, cy, zoom)
            if spark.life <= 0:
                self.sparks.remove(spark)

        # Screen flash
        if self.engine.combat_manager.parry_flash_timer > 0.0:
            flash_surf = pygame.Surface((1024, 768), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 255, 120))
            screen.blit(flash_surf, (0, 0))

        # Top Panel
        pygame.draw.rect(screen, (20, 20, 30), (0, 0, 1024, 45))
        pygame.draw.line(screen, (50, 50, 70), (0, 45), (1024, 45), 2)

        # MM:SS Timer
        mins = int(self.engine.survival_time // 60)
        secs = int(self.engine.survival_time % 60)
        time_txt = f"SURVIVED: {mins:02d}:{secs:02d}"
        t_surf = self.font_hud.render(time_txt, True, (255, 255, 255))
        screen.blit(t_surf, (512 - t_surf.get_width()//2, 14))

        # XP Progress Bar
        xp_pct = p.xp / p.xp_to_next
        pygame.draw.rect(screen, (40, 45, 60), (250, 5, 524, 6))
        pygame.draw.rect(screen, (0, 220, 255), (250, 5, int(524 * xp_pct), 6))
        
        lvl_surf = self.font_hud.render(f"LVL {p.level}", True, (0, 220, 255))
        screen.blit(lvl_surf, (200, 2))

        # Keybind Guide
        guide_surf = self.font_hud.render("[O] Settings [T] Base Camp [F] Tool [1-5] Slot", True, (160, 180, 200))
        screen.blit(guide_surf, (680, 14))

        # Resources Display
        res_text = f"Gold: {self.engine.gold}  Iron: {self.engine.iron}  Researches: {self.engine.scholar_pts}"
        res_surf = self.font_hud.render(res_text, True, (255, 220, 100))
        screen.blit(res_surf, (15, 14))

        # HUD Bottom Left: HP & Posture
        h_pct = p.health / p.stats["max_health"]
        pygame.draw.rect(screen, (40, 20, 20), (20, 715, 180, 14))
        pygame.draw.rect(screen, (220, 40, 40), (20, 715, int(180 * h_pct), 14))
        hp_txt = self.font_hud.render(f"HP: {p.health}/{p.stats['max_health']}", True, (255, 255, 255))
        screen.blit(hp_txt, (25, 698))

        pst_pct = p.posture / p.stats["max_posture"]
        pygame.draw.rect(screen, (40, 40, 20), (20, 738, 180, 10))
        pygame.draw.rect(screen, (220, 220, 40), (20, 738, int(180 * pst_pct), 10))
        
        # HUD Bottom Right: Stance indicator
        s_title = p.stance + " STANCE"
        s_col = (180, 180, 180)
        if p.stance == "WATER":
            s_col = (50, 150, 255)
        elif p.stance == "WIND":
            s_col = (100, 220, 150)
        st_surf = self.font_large.render(s_title, True, s_col)
        screen.blit(st_surf, (1004 - st_surf.get_width(), 710))

        # --- DRAW BOTTOM CENTER TOOLBAR ---
        # 5 slots centered. Width of each slot = 42. Border gap = 6. Total = 5*42 + 4*6 = 210 + 24 = 234.
        toolbar_start_x = 512 - 117
        toolbar_y = 705
        
        pygame.draw.rect(screen, (15, 15, 20), (toolbar_start_x - 6, toolbar_y - 6, 246, 54), 0, 6)
        pygame.draw.rect(screen, (50, 60, 75), (toolbar_start_x - 6, toolbar_y - 6, 246, 54), 2, 6)

        slot_names = ["Pick", "Katana", "Block", "Water", "Wind"]
        
        for i in range(5):
            slot_x = toolbar_start_x + i * 48
            slot_rect = pygame.Rect(slot_x, toolbar_y, 42, 42)
            
            # Highlight if selected
            bg_col = (45, 55, 70) if p.active_slot == i else (25, 30, 40)
            pygame.draw.rect(screen, bg_col, slot_rect, 0, 4)
            
            bd_col = (255, 215, 0) if p.active_slot == i else (70, 80, 95)
            bd_w = 3 if p.active_slot == i else 1
            pygame.draw.rect(screen, bd_col, slot_rect, bd_w, 4)
            
            # Draw Slot Label (compact)
            t_col = (255, 255, 255) if p.active_slot == i else (160, 170, 185)
            s_font = pygame.font.SysFont("Courier", 9, bold=True)
            lbl_surf = s_font.render(slot_names[i], True, t_col)
            screen.blit(lbl_surf, (slot_x + 21 - lbl_surf.get_width()//2, toolbar_y + 15))
            
            # Key Indicator number (1-5)
            k_surf = s_font.render(str(i+1), True, (120, 140, 160))
            screen.blit(k_surf, (slot_x + 4, toolbar_y + 4))

            # Display stack of materials for dirt slot
            if slot_names[i] == "Block":
                stk_surf = pygame.font.SysFont("Courier", 8, bold=True).render(f"x{self.engine.iron//2}", True, (200, 200, 200))
                screen.blit(stk_surf, (slot_x + 38 - stk_surf.get_width(), toolbar_y + 30))

    # --- LEVEL UP OVERLAY ---
    def draw_levelup(self, screen):
        overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
        overlay.fill((10, 10, 18, 200))
        screen.blit(overlay, (0, 0))

        dbox = pygame.Rect(200, 180, 624, 400)
        pygame.draw.rect(screen, (25, 30, 45), dbox, 0, 12)
        pygame.draw.rect(screen, (0, 220, 255), dbox, 3, 12)

        title_surf = self.font_large.render("LEVEL UP! CHOOSE AN UPGRADE", True, (255, 255, 255))
        screen.blit(title_surf, (512 - title_surf.get_width()//2, 210))

        self.levelup_buttons = []
        card_w = 160
        card_h = 240
        start_x = 240
        card_y = 280

        for idx, choice in enumerate(self.engine.level_choices):
            cx = start_x + idx * 190
            card_rect = pygame.Rect(cx, card_y, card_w, card_h)
            
            mx, my = pygame.mouse.get_pos()
            hovered = card_rect.collidepoint((mx, my))
            card_bg = (40, 50, 70) if hovered else (30, 35, 45)
            card_border = (0, 220, 255) if hovered else (70, 90, 120)

            pygame.draw.rect(screen, card_bg, card_rect, 0, 8)
            pygame.draw.rect(screen, card_border, card_rect, 2, 8)

            t_surf = self.font_hud.render(choice["title"], True, (255, 255, 255))
            screen.blit(t_surf, (cx + card_w//2 - t_surf.get_width()//2, card_y + 20))

            pygame.draw.circle(screen, (0, 220, 255) if idx == 0 else (255, 215, 0) if idx == 1 else (100, 255, 100), (cx + card_w//2, card_y + 80), 20, 2)
            
            desc_words = choice["desc"].split(" ")
            line1 = ""
            line2 = ""
            for word in desc_words:
                if len(line1) + len(word) < 18:
                    line1 += word + " "
                else:
                    line2 += word + " "
                    
            d_surf1 = pygame.font.SysFont("Courier", 11).render(line1.strip(), True, (200, 200, 200))
            d_surf2 = pygame.font.SysFont("Courier", 11).render(line2.strip(), True, (200, 200, 200))
            
            screen.blit(d_surf1, (cx + card_w//2 - d_surf1.get_width()//2, card_y + 140))
            screen.blit(d_surf2, (cx + card_w//2 - d_surf2.get_width()//2, card_y + 160))

            sel_surf = pygame.font.SysFont("Courier", 11, bold=True).render("CLICK TO EQUIP", True, (0, 220, 255))
            screen.blit(sel_surf, (cx + card_w//2 - sel_surf.get_width()//2, card_y + 205))

            self.levelup_buttons.append({"rect": card_rect, "id": choice["id"]})

    def handle_levelup_click(self, mouse_pos):
        for btn in self.levelup_buttons:
            if btn["rect"].collidepoint(mouse_pos):
                self.engine.sound_manager.play("click")
                self.engine.apply_upgrade(btn["id"])
                break

    def draw_excel(self, screen):
        # Cleared/Dormant method
        pass

    def draw_settings(self, screen):
        self.settings_panel.draw(screen)

    def draw_town(self, screen):
        self.town_panel.draw(screen)

    def draw_gameover(self, screen):
        screen.fill((10, 10, 15))
        
        go_surf = self.font_large.render("GAME OVER - YOU WERE OVERWHELMED", True, (220, 40, 40))
        screen.blit(go_surf, (512 - go_surf.get_width()//2, 180))

        mins = int(self.engine.survival_time // 60)
        secs = int(self.engine.survival_time % 60)
        stat_time = f"Time Survived: {mins:02d}:{secs:02d}"
        stat_lvl = f"Character Level: {self.engine.player.level}"
        stat_npcs = f"Survivors Rescued: {len(self.engine.rescued_npcs)}"
        stat_gold = f"Total Gold: {self.engine.gold}"

        s_t = self.font_sub.render(stat_time, True, (200, 200, 200))
        s_l = self.font_sub.render(stat_lvl, True, (200, 200, 200))
        s_n = self.font_sub.render(stat_npcs, True, (200, 200, 200))
        s_g = self.font_sub.render(stat_gold, True, (255, 215, 0))

        screen.blit(s_t, (512 - s_t.get_width()//2, 260))
        screen.blit(s_l, (512 - s_l.get_width()//2, 300))
        screen.blit(s_n, (512 - s_n.get_width()//2, 340))
        screen.blit(s_g, (512 - s_g.get_width()//2, 380))

        r_rect = pygame.Rect(384, 480, 256, 50)
        pygame.draw.rect(screen, (30, 40, 60), r_rect, 0, 8)
        pygame.draw.rect(screen, (100, 180, 255), r_rect, 2, 8)
        
        r_txt = self.font_hud.render("TRY AGAIN [ENTER]", True, (255, 255, 255))
        screen.blit(r_txt, (512 - r_txt.get_width()//2, 496))
        
        self.gameover_btn = r_rect

    def handle_gameover_click(self, mouse_pos):
        if hasattr(self, "gameover_btn") and self.gameover_btn.collidepoint(mouse_pos):
            self.engine.sound_manager.play("click")
            self.engine.state = "CUSTOMIZER"
