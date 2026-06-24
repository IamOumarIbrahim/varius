import pygame
import math
import random
import os
import json
from characters import CHARACTERS_DB

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


class CampBuildPanel:
    def __init__(self, engine):
        self.engine = engine
        self.font_title = pygame.font.SysFont("Courier", 22, bold=True)
        self.font_main = pygame.font.SysFont("Courier", 14)
        self.font_header = pygame.font.SysFont("Courier", 14, bold=True)
        self.buttons = []
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b or event.key == pygame.K_ESCAPE:
                self.engine.state = "PLAYING"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click(event.pos)
            
    def handle_click(self, pos):
        for btn in self.buttons:
            if btn["rect"].collidepoint(pos):
                self.build_structure(btn["type"])
                break
                
    def build_structure(self, stype):
        costs = {
            "HOUSE": (80, 150),  # iron, gold
            "FORGE": (100, 200),
            "LIBRARY": (50, 300)
        }
        iron_cost, gold_cost = costs[stype]
        if self.engine.iron >= iron_cost and self.engine.gold >= gold_cost:
            player = self.engine.player
            if player.y < 25 * 16:
                # Check maximum structures space or duplicate
                # If player already built Forge/Library, prevent duplicate!
                if stype in ["FORGE", "LIBRARY"]:
                    for struct in self.engine.world.structures:
                        if struct["type"] == stype:
                            return # limit to 1 Forge and 1 Library!
                            
                self.engine.iron -= iron_cost
                self.engine.gold -= gold_cost
                
                tx = int(player.x / 16)
                ty = int((player.y + player.height - 32) / 16)
                
                self.engine.world.structures.append({
                    "tx": tx,
                    "ty": ty,
                    "type": stype,
                    "level": 1
                })
                self.engine.sound_manager.play("block")
                self.engine.state = "PLAYING"
                
    def draw(self, screen):
        overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
        overlay.fill((30, 25, 20, 220))
        screen.blit(overlay, (0, 0))
        
        border_rect = pygame.Rect(200, 120, 624, 528)
        pygame.draw.rect(screen, (38, 30, 25), border_rect, 0, 8)
        pygame.draw.rect(screen, (150, 110, 80), border_rect, 3, 8)
        
        t_surf = self.font_title.render("CAMP BUILD MENU - COLONY STRUCTURES", True, (255, 255, 255))
        screen.blit(t_surf, (512 - t_surf.get_width()//2, 140))
        
        guide = self.font_main.render("Stand above-ground to place structures. Press [B] to Close.", True, (190, 170, 150))
        screen.blit(guide, (512 - guide.get_width()//2, 175))
        
        self.buttons = []
        structures_info = [
            ("NPC Cottage", "HOUSE", "Provides +2 maximum colony population capacity.", 80, 150, 220),
            ("Blacksmith Forge", "FORGE", "Enables Blacksmith job assignments.", 100, 200, 310),
            ("Scholar Library", "LIBRARY", "Enables Scholar job assignments.", 50, 300, 400)
        ]
        
        for name, stype, desc, iron_c, gold_c, y in structures_info:
            card_rect = pygame.Rect(230, y, 564, 75)
            pygame.draw.rect(screen, (25, 20, 15), card_rect, 0, 6)
            pygame.draw.rect(screen, (80, 60, 50), card_rect, 1, 6)
            
            n_surf = self.font_header.render(name, True, (255, 220, 100))
            screen.blit(n_surf, (245, y + 10))
            d_surf = self.font_main.render(desc, True, (170, 160, 150))
            screen.blit(d_surf, (245, y + 30))
            
            cost_str = f"Cost: {iron_c} Iron | {gold_c} Gold"
            c_surf = self.font_main.render(cost_str, True, (130, 220, 130))
            screen.blit(c_surf, (245, y + 50))
            
            # Check duplicate limit
            is_built = False
            if stype in ["FORGE", "LIBRARY"]:
                for struct in self.engine.world.structures:
                    if struct["type"] == stype:
                        is_built = True
                        break
            
            btn_rect = pygame.Rect(680, y + 20, 96, 35)
            can_build = self.engine.iron >= iron_c and self.engine.gold >= gold_c and not is_built
            
            bg_col = (45, 80, 50) if can_build else (25, 25, 25)
            bd_col = (100, 220, 120) if can_build else (60, 60, 60)
            tx_col = (255, 255, 255) if can_build else (100, 100, 100)
            
            pygame.draw.rect(screen, bg_col, btn_rect, 0, 4)
            pygame.draw.rect(screen, bd_col, btn_rect, 2, 4)
            
            lbl_text = "BUILT" if is_built else "BUILD"
            btn_text = self.font_header.render(lbl_text, True, tx_col)
            screen.blit(btn_text, (btn_rect.centerx - btn_text.get_width()//2, btn_rect.centery - btn_text.get_height()//2))
            
            if not is_built:
                self.buttons.append({"rect": btn_rect, "type": stype})


class InventoryPanel:
    def __init__(self, engine):
        self.engine = engine
        self.font_title = pygame.font.SysFont("Courier", 22, bold=True)
        self.font_main = pygame.font.SysFont("Courier", 14)
        self.font_header = pygame.font.SysFont("Courier", 14, bold=True)
        self.buttons = []
        self.tooltip_item = None
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                self.engine.state = "PLAYING"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.handle_click(event.pos)
            
    def handle_click(self, pos):
        player = self.engine.player
        for btn in self.buttons:
            if btn["rect"].collidepoint(pos):
                action = btn["action"]
                if action == "EQUIP":
                    player.equip_item(btn["index"])
                elif action == "UNEQUIP":
                    player.unequip_item(btn["slot"])
                break
                
    def draw(self, screen):
        player = self.engine.player
        
        overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
        overlay.fill((20, 20, 30, 230))
        screen.blit(overlay, (0, 0))
        
        border_rect = pygame.Rect(120, 80, 784, 608)
        pygame.draw.rect(screen, (24, 24, 35), border_rect, 0, 8)
        pygame.draw.rect(screen, (80, 90, 120), border_rect, 3, 8)
        
        t_surf = self.font_title.render("HERO GEAR & INVENTORY EQUIPMENT", True, (255, 255, 255))
        screen.blit(t_surf, (512 - t_surf.get_width()//2, 100))
        
        guide = self.font_main.render("Equip gear to increase stats. Press [I] to Close.", True, (150, 170, 200))
        screen.blit(guide, (512 - guide.get_width()//2, 134))
        
        self.buttons = []
        self.tooltip_item = None
        mx, my = pygame.mouse.get_pos()
        
        slots_info = [("HELMET", 180), ("RING", 260), ("CAPE", 340)]
        for slot_type, y in slots_info:
            pygame.draw.rect(screen, (15, 15, 22), (160, y, 68, 68), 0, 6)
            pygame.draw.rect(screen, (55, 65, 80), (160, y, 68, 68), 1, 6)
            
            lbl_type = self.font_header.render(slot_type[:3], True, (100, 120, 140))
            screen.blit(lbl_type, (160 + 34 - lbl_type.get_width()//2, y + 26))
            
            item = player.equipped[slot_type]
            if item is not None:
                pygame.draw.rect(screen, item["color"], (160, y, 68, 68), 0, 6)
                pygame.draw.rect(screen, (255, 215, 0), (160, y, 68, 68), 2, 6)
                
                title_sh = item["name"][:3].upper()
                t_sh_surf = self.font_header.render(title_sh, True, (255, 255, 255))
                screen.blit(t_sh_surf, (194 - t_sh_surf.get_width()//2, y + 24))
                
                item_rect = pygame.Rect(160, y, 68, 68)
                if item_rect.collidepoint((mx, my)):
                    self.tooltip_item = item
                
                self.buttons.append({"rect": item_rect, "action": "UNEQUIP", "slot": slot_type})
                
        stats_labels = [
            ("Max HP", player.stats["max_health"]),
            ("Armor", player.stats.get("armor", 0)),
            ("Damage", player.stats["base_dmg"]),
            ("Crit Rate", f"{int(player.stats['crit_rate']*100)}%"),
            ("Crit Dmg", f"{int(player.stats['crit_dmg']*100)}%"),
            ("Speed", f"{int(player.stats.get('move_speed_mult', 1.0)*100)}%"),
            ("Magnet", f"{player.stats.get('magnet_range', 3.0):.1f}")
        ]
        
        sy = 430
        for name, val in stats_labels:
            n_surf = self.font_header.render(f"{name}:", True, (180, 200, 220))
            v_surf = self.font_header.render(str(val), True, (255, 215, 0))
            screen.blit(n_surf, (160, sy))
            screen.blit(v_surf, (270, sy))
            sy += 25
            
        pygame.draw.line(screen, (60, 75, 100), (350, 170), (350, 640), 2)
        
        grid_start_x = 390
        grid_start_y = 180
        cell_size = 72
        
        for idx in range(16):
            col = idx % 4
            row = idx // 4
            cell_x = grid_start_x + col * (cell_size + 16)
            cell_y = grid_start_y + row * (cell_size + 16)
            
            cell_rect = pygame.Rect(cell_x, cell_y, cell_size, cell_size)
            pygame.draw.rect(screen, (15, 15, 22), cell_rect, 0, 8)
            pygame.draw.rect(screen, (40, 50, 70), cell_rect, 1, 8)
            
            if idx < len(player.inventory):
                item = player.inventory[idx]
                pygame.draw.rect(screen, item["color"], cell_rect, 0, 8)
                pygame.draw.rect(screen, (220, 220, 220), cell_rect, 2, 8)
                
                sh_title = item["name"][:3].upper()
                sh_surf = self.font_header.render(sh_title, True, (255, 255, 255))
                screen.blit(sh_surf, (cell_rect.centerx - sh_surf.get_width()//2, cell_rect.centery - sh_surf.get_height()//2 - 6))
                
                type_surf = self.font_main.render(item["slot"][:3], True, (230, 230, 250))
                screen.blit(type_surf, (cell_rect.centerx - type_surf.get_width()//2, cell_rect.centery + 12))
                
                if cell_rect.collidepoint((mx, my)):
                    self.tooltip_item = item
                    
                self.buttons.append({"rect": cell_rect, "action": "EQUIP", "index": idx})
                
        if self.tooltip_item is not None:
            card_x = mx + 20 if mx < 700 else mx - 260
            card_y = my + 20 if my < 500 else my - 160
            
            card_rect = pygame.Rect(card_x, card_y, 240, 140)
            pygame.draw.rect(screen, (25, 25, 38), card_rect, 0, 8)
            pygame.draw.rect(screen, self.tooltip_item["color"], card_rect, 2, 8)
            
            name_lines = self.wrap_text(self.tooltip_item["name"], 210)
            cy = card_y + 10
            for l in name_lines:
                n_surf = self.font_header.render(l, True, (255, 255, 255))
                screen.blit(n_surf, (card_x + 12, cy))
                cy += 18
                
            r_str = f"{self.tooltip_item['rarity']} {self.tooltip_item['slot']}"
            r_surf = self.font_main.render(r_str, True, self.tooltip_item["color"])
            screen.blit(r_surf, (card_x + 12, cy))
            cy += 20
            
            for stat_name, stat_val in self.tooltip_item["bonuses"].items():
                disp_name = {
                    "max_health": "+Max Health",
                    "armor": "+Armor",
                    "base_dmg": "+Base Damage",
                    "crit_rate": "+Crit Rate",
                    "crit_dmg": "+Crit Damage",
                    "move_speed_mult": "+Move Speed",
                    "magnet_range": "+Magnet Range"
                }.get(stat_name, stat_name)
                
                if stat_name in ["crit_rate", "move_speed_mult", "crit_dmg"]:
                    val_str = f"+{int(stat_val * 100)}%"
                else:
                    val_str = f"+{stat_val}"
                    
                s_line = f"{disp_name}: {val_str}"
                s_surf = self.font_main.render(s_line, True, (130, 220, 130))
                screen.blit(s_surf, (card_x + 12, cy))
                cy += 18

    def wrap_text(self, text, max_w):
        words = text.split(' ')
        lines = []
        curr = ""
        for w in words:
            test = curr + " " + w if curr else w
            if self.font_header.size(test)[0] <= max_w:
                curr = test
            else:
                lines.append(curr)
                curr = w
        if curr:
            lines.append(curr)
        return lines


class SettingsPanel:
    def __init__(self, engine):
        self.engine = engine
        self.font_title = pygame.font.SysFont("Courier", 22, bold=True)
        self.font_main = pygame.font.SysFont("Courier", 14)
        self.font_header = pygame.font.SysFont("Courier", 14, bold=True)
        self.slider_x = 380
        self.slider_w = 260
        self.buttons = []

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o or event.key == pygame.K_ESCAPE:
                self.engine.state = getattr(self.engine, "settings_prev_state", "PLAYING")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            self.handle_click(mouse_pos)
        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[0]:
                self.handle_slider_drag(event.pos)

    def handle_slider_drag(self, pos):
        mx, my = pos
        if self.slider_x <= mx <= self.slider_x + self.slider_w:
            ratio = (mx - self.slider_x) / self.slider_w
            if 200 <= my <= 235:
                self.engine.zoom = round(1.0 + ratio * 1.5, 2)
            elif 260 <= my <= 295:
                sfx_vol = ratio
                self.engine.sound_manager.set_sfx_volume(sfx_vol)
            elif 320 <= my <= 355:
                music_vol = ratio
                self.engine.sound_manager.set_music_volume(music_vol)

    def handle_click(self, pos):
        self.handle_slider_drag(pos)
        for btn in self.buttons:
            if btn["rect"].collidepoint(pos):
                slot = btn["slot"]
                act = btn["action"]
                if act == "SAVE":
                    self.engine.save_game(slot)
                elif act == "LOAD":
                    self.engine.load_game(slot)
                break

    def get_slot_metadata(self, slot_num):
        filename = f"save_slot_{slot_num}.json"
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
                char_name = data.get("player", {}).get("char_name", "Hero")
                lvl = data.get("player", {}).get("level", 1)
                t = data.get("survival_time", 0.0)
                m = int(t // 60)
                s = int(t % 60)
                return f"{char_name} (Lvl {lvl}) - {m:02d}:{s:02d} - {data.get('gold', 0)}g"
            except Exception:
                return "Corrupt Data"
        return "Empty Slot"

    def draw(self, screen):
        overlay = pygame.Surface((1024, 768), pygame.SRCALPHA)
        overlay.fill((20, 20, 30, 225))
        screen.blit(overlay, (0, 0))

        border_rect = pygame.Rect(180, 80, 664, 608)
        pygame.draw.rect(screen, (32, 38, 48), border_rect, 0, 8)
        pygame.draw.rect(screen, (80, 100, 130), border_rect, 3, 8)

        t_surf = self.font_title.render("GAME SETTINGS & SAVE PROFILE PANEL", True, (255, 255, 255))
        screen.blit(t_surf, (512 - t_surf.get_width()//2, 100))
        
        guide = self.font_main.render("Adjust configurations and manage save states. Press [O] to Close Settings.", True, (150, 180, 200))
        screen.blit(guide, (512 - guide.get_width()//2, 134))

        # Sliders
        ratio_zoom = (self.engine.zoom - 1.0) / 1.5
        self.draw_slider(screen, 215, "Zoom Scale", f"{self.engine.zoom:.2f}x", ratio_zoom)

        ratio_sfx = self.engine.sound_manager.sfx_volume
        self.draw_slider(screen, 275, "SFX Volume", f"{int(ratio_sfx*100)}%", ratio_sfx)

        ratio_music = self.engine.sound_manager.music_volume
        self.draw_slider(screen, 335, "Music Volume", f"{int(ratio_music*100)}%", ratio_music)

        pygame.draw.line(screen, (60, 80, 110), (220, 380), (800, 380), 2)
        lbl_save = self.font_header.render("SAVE / LOAD GAME SLOTS", True, (255, 215, 0))
        screen.blit(lbl_save, (512 - lbl_save.get_width()//2, 395))

        self.buttons = []
        start_y = 430
        row_h = 65

        for slot in range(1, 4):
            curr_y = start_y + (slot - 1) * row_h
            s_label = self.font_header.render(f"Slot {slot}:", True, (255, 255, 255))
            screen.blit(s_label, (220, curr_y + 12))
            
            meta = self.get_slot_metadata(slot)
            color = (130, 220, 150) if meta != "Empty Slot" else (150, 150, 150)
            meta_surf = self.font_main.render(meta, True, color)
            screen.blit(meta_surf, (310, curr_y + 12))

            # [SAVE]
            btn_save = pygame.Rect(600, curr_y + 6, 80, 28)
            pygame.draw.rect(screen, (30, 60, 45), btn_save, 0, 4)
            pygame.draw.rect(screen, (100, 220, 130), btn_save, 1, 4)
            t_s = pygame.font.SysFont("Courier", 11, bold=True).render("SAVE", True, (255, 255, 255))
            screen.blit(t_s, (623, curr_y + 14))
            self.buttons.append({"rect": btn_save, "action": "SAVE", "slot": slot})

            # [LOAD]
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
            pygame.draw.line(screen, (40, 50, 65), (220, curr_y + row_h - 10), (800, curr_y + row_h - 10), 1)

    def draw_slider(self, screen, y, title, val_str, ratio):
        lbl_surf = self.font_header.render(title, True, (220, 220, 220))
        screen.blit(lbl_surf, (220, y - 6))
        pygame.draw.line(screen, (50, 60, 80), (self.slider_x, y), (self.slider_x + self.slider_w, y), 6)
        pygame.draw.line(screen, (0, 200, 255), (self.slider_x, y), (self.slider_x + int(self.slider_w * ratio), y), 6)
        knob_x = self.slider_x + int(self.slider_w * ratio)
        pygame.draw.circle(screen, (255, 255, 255), (knob_x, y), 8)
        pygame.draw.circle(screen, (0, 150, 255), (knob_x, y), 5)
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
        forge_built = any(s["type"] == "FORGE" for s in self.engine.world.structures)
        library_built = any(s["type"] == "LIBRARY" for s in self.engine.world.structures)

        for btn in self.buttons:
            if btn["rect"].collidepoint(mouse_pos):
                action = btn["action"]
                npc = btn["npc"]
                
                if action == "ASSIGN_MINER":
                    npc["job"] = "Miner"
                elif action == "ASSIGN_BLACKSMITH" and forge_built:
                    npc["job"] = "Blacksmith"
                elif action == "ASSIGN_SCHOLAR" and library_built:
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
        
        # Cottage count capacity details
        cottages_count = sum(1 for s in self.engine.world.structures if s["type"] == "HOUSE")
        max_pop = 2 + 2 * cottages_count
        pop_str = f"Colony Population: {len(self.engine.rescued_npcs)}/{max_pop} (Houses: {cottages_count})"
        pop_surf = self.font_header.render(pop_str, True, (150, 220, 180))
        screen.blit(pop_surf, (80, 94))
        
        info_surf = self.font_main.render("Rescue caged captives from caves. Build Houses above-ground to increase capacity [T] to Close.", True, (130, 170, 150))
        screen.blit(info_surf, (80, 114))

        gold_text = f"Gold: {self.engine.gold} (+{self.engine.gold_per_sec}/s)"
        iron_text = f"Iron: {self.engine.iron} (+{self.engine.iron_per_sec}/s)"
        schol_text = f"Scholar Pts: {self.engine.scholar_pts} (+{self.engine.scholar_pts_per_sec}/s)"
        
        g_surf = self.font_header.render(gold_text, True, (255, 215, 0))
        i_surf = self.font_header.render(iron_text, True, (200, 200, 220))
        s_surf = self.font_header.render(schol_text, True, (100, 220, 255))
        
        screen.blit(g_surf, (80, 140))
        screen.blit(i_surf, (340, 140))
        screen.blit(s_surf, (600, 140))

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
        
        forge_built = any(s["type"] == "FORGE" for s in self.engine.world.structures)
        library_built = any(s["type"] == "LIBRARY" for s in self.engine.world.structures)

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
                is_locked = (j_title == "Smith" and not forge_built) or (j_title == "Scholar" and not library_built)
                btn_rect = pygame.Rect(btn_x, curr_y + 10, 75, 28)
                
                bg_col = (20, 20, 20) if is_locked else (30, 50, 40)
                bd_col = (50, 50, 50) if is_locked else j_col
                tx_col = (100, 100, 100) if is_locked else (255, 255, 255)
                
                pygame.draw.rect(screen, bg_col, btn_rect, 0, 4)
                pygame.draw.rect(screen, bd_col, btn_rect, 1, 4)
                
                if not is_locked and (npc["job"] == j_title or (j_title == "Smith" and npc["job"] == "Blacksmith")):
                    pygame.draw.rect(screen, (j_col[0]//2, j_col[1]//2, j_col[2]//2), btn_rect, 0, 4)
                
                lbl_title = "LOCKED" if is_locked else j_title
                j_surf = pygame.font.SysFont("Courier", 11, bold=True).render(lbl_title, True, tx_col)
                screen.blit(j_surf, (btn_x + 37 - j_surf.get_width()//2, curr_y + 18))
                
                if not is_locked:
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
        self.camp_build_panel = CampBuildPanel(engine)
        self.inventory_panel = InventoryPanel(engine)
        self.loot_notifications = []
        
        self.font_hud = pygame.font.SysFont("Courier", 14, bold=True)
        self.font_large = pygame.font.SysFont("Courier", 32, bold=True)
        self.font_sub = pygame.font.SysFont("Courier", 18, bold=True)
        self.font_main = pygame.font.SysFont("Courier", 14)
        
        self.sparks = []
        self.slashes = []
        
        # Grid Select state
        self.char_grid_scroll_y = 0
        self.customizer_buttons = []
        
        # Main Menu buttons
        self.main_menu_buttons = []
        
        # 4x sprite cache
        self.sprite_cache = {}

    def spawn_sparks(self, x, y, color):
        for _ in range(random.randint(6, 12)):
            self.sparks.append(Spark(x, y, color))

    def add_slash_effect(self, x, y, max_radius):
        self.slashes.append(SlashEffect(x, y, max_radius))

    def add_loot_notification(self, item):
        self.loot_notifications.append({"item": item, "timer": 2.5})
        
    def draw_inventory(self, screen):
        self.inventory_panel.draw(screen)
        
    def draw_camp_build(self, screen):
        self.camp_build_panel.draw(screen)

    def wrap_text(self, text, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if self.font_main.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    # --- 4X DETAILED PROCEDURAL SPRITE DRAWER ---
    def make_detailed_sprite(self, theme, is_swinging=False, active_tool="PICKAXE", stance="STONE", direction=1, flash_red=False):
        # Base canvas of 56x104 (4 times details than original 14x26)
        surf = pygame.Surface((56, 104), pygame.SRCALPHA)
        
        c_pants = theme["pants"]
        c_shirt = theme["shirt"]
        c_skin = theme["skin"]
        c_eyes = theme["eyes"]
        c_hair = theme["hair"]
        
        if flash_red:
            c_pants = (200, 50, 50)
            c_shirt = (255, 100, 100)
            c_skin = (255, 100, 100)
            c_eyes = (255, 0, 0)
            c_hair = (255, 100, 100)
            
        has_ponytail = theme.get("has_ponytail", False)
        has_braids = theme.get("has_braids", False)
        has_cape = theme.get("has_cape", False)
        cape_color = theme.get("cape_color", (200, 30, 30))
        if flash_red:
            cape_color = (200, 50, 50)
            
        has_goatee = theme.get("has_goatee", False)
        has_blindfold = theme.get("has_blindfold", False)
        has_straw_hat = theme.get("has_straw_hat", False)
        has_fedora = theme.get("has_fedora", False)
        has_green_cap = theme.get("has_green_cap", False)
        is_bald = theme.get("is_bald", False)
        has_scar = theme.get("has_scar", False)
        
        # 1. Draw Cape (flowing backdrop)
        if has_cape:
            for cy in range(32, 92):
                w_at_y = int(8 + (cy - 32) * 0.25)
                cx_center = 28 - direction * 6
                pygame.draw.rect(surf, cape_color, (cx_center - w_at_y//2, cy, w_at_y, 1))
                shadow_col = (max(0, cape_color[0]-40), max(0, cape_color[1]-40), max(0, cape_color[2]-40))
                surf.set_at((cx_center - w_at_y//2, cy), shadow_col)
                surf.set_at((cx_center + w_at_y//2 - 1, cy), shadow_col)
                if cy % 8 < 3:
                    surf.set_at((cx_center, cy), shadow_col)
                    
        # 2. Draw Legs and Shoes
        shadow_pants = (max(0, c_pants[0]-35), max(0, c_pants[1]-35), max(0, c_pants[2]-35))
        highlight_pants = (min(255, c_pants[0]+25), min(255, c_pants[1]+25), min(255, c_pants[2]+25))
        
        # Left Leg
        pygame.draw.rect(surf, c_pants, (16, 64, 10, 28))
        pygame.draw.rect(surf, shadow_pants, (16, 64, 3, 28))
        pygame.draw.rect(surf, highlight_pants, (23, 64, 3, 28))
        
        # Right Leg
        pygame.draw.rect(surf, c_pants, (30, 64, 10, 28))
        pygame.draw.rect(surf, shadow_pants, (30, 64, 3, 28))
        pygame.draw.rect(surf, highlight_pants, (37, 64, 3, 28))
        
        # Shoes
        c_sole = (30, 30, 30)
        c_shoe = (50, 50, 50)
        pygame.draw.rect(surf, c_shoe, (14, 92, 12, 6))
        pygame.draw.rect(surf, c_sole, (14, 98, 12, 2))
        pygame.draw.rect(surf, c_shoe, (30, 92, 12, 6))
        pygame.draw.rect(surf, c_sole, (30, 98, 12, 2))
        
        # 3. Draw Torso (Shirt)
        shadow_shirt = (max(0, c_shirt[0]-35), max(0, c_shirt[1]-35), max(0, c_shirt[2]-35))
        highlight_shirt = (min(255, c_shirt[0]+25), min(255, c_shirt[1]+25), min(255, c_shirt[2]+25))
        pygame.draw.rect(surf, c_shirt, (12, 32, 32, 32))
        pygame.draw.rect(surf, shadow_shirt, (12, 32, 6, 32))
        pygame.draw.rect(surf, highlight_shirt, (38, 32, 6, 32))
        
        # Collar neck shadow
        pygame.draw.rect(surf, (max(0, c_skin[0]-40), max(0, c_skin[1]-40), max(0, c_skin[2]-40)), (22, 32, 12, 3))
        
        # Belt
        pygame.draw.rect(surf, (40, 30, 20), (12, 60, 32, 4))
        pygame.draw.rect(surf, (240, 200, 50), (25, 60, 6, 4))
        
        # 4. Arms
        if is_swinging:
            if direction == 1:
                pygame.draw.rect(surf, c_shirt, (6, 32, 6, 16))
                pygame.draw.rect(surf, c_skin, (6, 48, 6, 6))
                
                pygame.draw.rect(surf, c_shirt, (44, 32, 12, 8))
                pygame.draw.rect(surf, c_skin, (56, 32, 6, 6))
            else:
                pygame.draw.rect(surf, c_shirt, (44, 32, 6, 16))
                pygame.draw.rect(surf, c_skin, (44, 48, 6, 6))
                
                pygame.draw.rect(surf, c_shirt, (0, 32, 12, 8))
                pygame.draw.rect(surf, c_skin, (0, 32, 6, 6))
        else:
            # Idle arms
            pygame.draw.rect(surf, c_shirt, (6, 32, 6, 22))
            pygame.draw.rect(surf, c_skin, (6, 54, 6, 6))
            pygame.draw.rect(surf, shadow_shirt, (6, 32, 2, 22))
            
            pygame.draw.rect(surf, c_shirt, (44, 32, 6, 22))
            pygame.draw.rect(surf, c_skin, (44, 54, 6, 6))
            pygame.draw.rect(surf, highlight_shirt, (48, 32, 2, 22))
            
        # 5. Head
        shadow_skin = (max(0, c_skin[0]-30), max(0, c_skin[1]-30), max(0, c_skin[2]-30))
        highlight_skin = (min(255, c_skin[0]+20), min(255, c_skin[1]+20), min(255, c_skin[2]+20))
        pygame.draw.rect(surf, c_skin, (16, 8, 24, 24))
        pygame.draw.rect(surf, shadow_skin, (16, 8, 4, 24))
        pygame.draw.rect(surf, shadow_skin, (16, 28, 24, 4))
        pygame.draw.rect(surf, highlight_skin, (36, 8, 4, 20))
        
        # Rosy cheeks
        surf.set_at((20, 24), (250, 150, 150))
        surf.set_at((21, 24), (250, 150, 150))
        surf.set_at((34, 24), (250, 150, 150))
        surf.set_at((35, 24), (250, 150, 150))
        
        if has_goatee:
            pygame.draw.rect(surf, (60, 45, 30), (22, 26, 12, 6))
            pygame.draw.rect(surf, (40, 30, 20), (25, 29, 6, 3))
            
        # 6. Detailed Eyes
        eye_shift = direction * 2
        if has_blindfold:
            pygame.draw.rect(surf, (15, 15, 15), (14, 16, 28, 5))
            pygame.draw.rect(surf, (50, 50, 50), (14, 16, 28, 1))
        else:
            # Left Eye
            pygame.draw.rect(surf, (255, 255, 255), (18 + eye_shift, 16, 4, 4))
            pygame.draw.rect(surf, c_eyes, (19 + eye_shift, 16, 2, 4))
            surf.set_at((19 + eye_shift, 17), (20, 20, 20))
            surf.set_at((18 + eye_shift, 16), (255, 255, 255))
            
            # Right Eye
            pygame.draw.rect(surf, (255, 255, 255), (30 + eye_shift, 16, 4, 4))
            pygame.draw.rect(surf, c_eyes, (31 + eye_shift, 16, 2, 4))
            surf.set_at((31 + eye_shift, 17), (20, 20, 20))
            surf.set_at((30 + eye_shift, 16), (255, 255, 255))
            
        # Scar
        if has_scar:
            surf.set_at((31, 11), (220, 30, 30))
            surf.set_at((32, 12), (220, 30, 30))
            surf.set_at((31, 13), (220, 30, 30))
            
        # Mouth
        pygame.draw.line(surf, (120, 60, 50), (25 + eye_shift, 26), (29 + eye_shift, 26), 1)
        
        # 7. Hair (layered strands & highlights)
        if not is_bald:
            shadow_hair = (max(0, c_hair[0]-35), max(0, c_hair[1]-35), max(0, c_hair[2]-35))
            highlight_hair = (min(255, c_hair[0]+30), min(255, c_hair[1]+30), min(255, c_hair[2]+30))
            pygame.draw.rect(surf, c_hair, (14, 4, 28, 8))
            pygame.draw.rect(surf, shadow_hair, (14, 4, 4, 8))
            pygame.draw.rect(surf, highlight_hair, (34, 4, 8, 4))
            
            if direction == 1:
                pygame.draw.rect(surf, c_hair, (14, 8, 4, 10))
                pygame.draw.rect(surf, c_hair, (38, 8, 4, 10))
                pygame.draw.rect(surf, c_hair, (18, 8, 8, 4))
            else:
                pygame.draw.rect(surf, c_hair, (14, 8, 4, 10))
                pygame.draw.rect(surf, c_hair, (38, 8, 4, 10))
                pygame.draw.rect(surf, c_hair, (30, 8, 8, 4))
                
            if has_ponytail:
                if direction == 1:
                    pygame.draw.rect(surf, c_hair, (8, 8, 8, 20))
                    pygame.draw.rect(surf, shadow_hair, (8, 8, 3, 20))
                else:
                    pygame.draw.rect(surf, c_hair, (40, 8, 8, 20))
                    pygame.draw.rect(surf, shadow_hair, (40, 8, 3, 20))
                    
            if has_braids:
                pygame.draw.rect(surf, c_hair, (12, 12, 4, 24))
                pygame.draw.rect(surf, highlight_hair, (12, 12, 2, 24))
                pygame.draw.rect(surf, c_hair, (40, 12, 4, 24))
                pygame.draw.rect(surf, highlight_hair, (42, 12, 2, 24))
                
        # 8. Hats
        if has_straw_hat:
            pygame.draw.rect(surf, (220, 200, 110), (8, 4, 40, 4))
            pygame.draw.rect(surf, (200, 30, 40), (14, 2, 28, 2))
            pygame.draw.rect(surf, (220, 200, 110), (18, 0, 20, 2))
        elif has_fedora:
            pygame.draw.rect(surf, (100, 70, 45), (8, 6, 40, 3))
            pygame.draw.rect(surf, (20, 20, 20), (14, 3, 28, 3))
            pygame.draw.rect(surf, (80, 50, 30), (16, 0, 24, 3))
        elif has_green_cap:
            pygame.draw.rect(surf, (50, 140, 50), (16, 2, 24, 6))
            if direction == 1:
                pygame.draw.rect(surf, (40, 120, 40), (32, 6, 12, 2))
            else:
                pygame.draw.rect(surf, (40, 120, 40), (12, 6, 12, 2))
                
        # 9. Outline Silhouette blit
        outline_color = (12, 14, 20)
        outline_surf = pygame.Surface((58, 106), pygame.SRCALPHA)
        mask = pygame.mask.from_surface(surf)
        mask_surf = mask.to_surface(setcolor=outline_color, unsetcolor=(0, 0, 0, 0))
        
        outline_surf.blit(mask_surf, (0, 1))
        outline_surf.blit(mask_surf, (2, 1))
        outline_surf.blit(mask_surf, (1, 0))
        outline_surf.blit(mask_surf, (1, 2))
        
        outline_surf.blit(surf, (1, 1))
        return outline_surf

    def draw_detailed_sprite(self, screen, x, y, theme, scale, direction=1, is_swinging=False, active_tool="PICKAXE", stance="STONE", flash_red=False):
        key = (
            theme.get("hair", (0,0,0)),
            theme.get("shirt", (0,0,0)),
            theme.get("pants", (0,0,0)),
            theme.get("skin", (0,0,0)),
            theme.get("eyes", (0,0,0)),
            theme.get("has_ponytail", False),
            theme.get("has_braids", False),
            theme.get("has_cape", False),
            theme.get("has_goatee", False),
            theme.get("has_blindfold", False),
            theme.get("has_straw_hat", False),
            theme.get("has_fedora", False),
            theme.get("has_green_cap", False),
            theme.get("is_bald", False),
            theme.get("has_scar", False),
            is_swinging,
            active_tool,
            stance,
            direction,
            flash_red
        )
        
        if key not in self.sprite_cache:
            self.sprite_cache[key] = self.make_detailed_sprite(theme, is_swinging, active_tool, stance, direction, flash_red)
            
        sprite_surf = self.sprite_cache[key]
        
        w = int(sprite_surf.get_width() * (scale / 4.0))
        h = int(sprite_surf.get_height() * (scale / 4.0))
        w = max(1, w)
        h = max(1, h)
        
        scaled_surf = pygame.transform.scale(sprite_surf, (w, h))
        
        # Center outline-padded sprite relative to original 14x26 box coordinates
        offset_x = int(-1 * (scale / 4.0))
        offset_y = int(-1 * (scale / 4.0))
        screen.blit(scaled_surf, (x + offset_x, y + offset_y))

    def draw_character_preview(self, screen, x, y, theme, scale):
        # Preview utilizes the exact same 4x outline sprite drawer scaled appropriately
        self.draw_detailed_sprite(screen, x, y, theme, scale * 4.0, direction=1)

    # --- MAIN SCREEN / MENU DRAW ---
    def draw_main_menu(self, screen):
        # Draw sky background with sun and parallax clouds
        screen.fill((140, 190, 255))
        
        # Sun
        pygame.draw.circle(screen, (255, 255, 200), (200, 80), 38)
        pygame.draw.circle(screen, (255, 220, 100), (200, 80), 30)
        
        # Floating clouds
        for cloud in self.engine.world.clouds:
            cx = int(cloud["x"])
            cy = int(cloud["y"])
            cw = int(cloud["w"])
            ch = int(cloud["h"])
            pygame.draw.ellipse(screen, (245, 248, 255), (cx, cy, cw, ch))
            pygame.draw.ellipse(screen, (255, 255, 255), (cx + 5, cy + 4, int(cw * 0.8), int(ch * 0.8)))
            
        # 3D Extruded Blocky Text Logo "VARIUS"
        title_text = "VARIUS"
        for i in range(12, 0, -1):
            offset_col = (max(0, 45 - i*2), max(0, 40 - i*2), max(0, 20 - i*2)) if i > 1 else (75, 60, 20)
            font_3d = pygame.font.SysFont("Impact", 100, bold=True)
            t_surf = font_3d.render(title_text, True, offset_col)
            screen.blit(t_surf, (512 - t_surf.get_width()//2 + i*2, 120 - i*2))
            
        t_surf_front = font_3d.render(title_text, True, (255, 215, 0))
        screen.blit(t_surf_front, (512 - t_surf_front.get_width()//2, 120))
        
        # Subtitle
        sub_t = pygame.font.SysFont("Courier", 15, bold=True).render("A Swarm & Procedural Cave Adventure", True, (60, 75, 90))
        screen.blit(sub_t, (512 - sub_t.get_width()//2, 220))
        
        # Version Badge
        v_surf = pygame.font.SysFont("Courier", 12, bold=True).render("v_beta0.3", True, (255, 255, 255))
        pygame.draw.rect(screen, (150, 40, 80), (512 - v_surf.get_width()//2 - 8, 245, v_surf.get_width() + 16, 20), 0, 4)
        screen.blit(v_surf, (512 - v_surf.get_width()//2, 248))
        
        # Render Buttons
        self.main_menu_buttons = []
        buttons_info = [
            ("START NEW GAME", "START", 320),
            ("LOAD SAVE PROFILE", "LOAD_SAVE", 395),
            ("GAME SETTINGS", "SETTINGS", 470),
            ("QUIT GAME", "EXIT", 545)
        ]
        
        mx, my = pygame.mouse.get_pos()
        for title, action, y in buttons_info:
            btn_rect = pygame.Rect(384, y, 256, 48)
            hovered = btn_rect.collidepoint((mx, my))
            
            bg_col = (40, 55, 75) if hovered else (25, 30, 42)
            bd_col = (255, 215, 0) if hovered else (70, 80, 100)
            
            pygame.draw.rect(screen, bg_col, btn_rect, 0, 8)
            pygame.draw.rect(screen, bd_col, btn_rect, 2, 8)
            
            btn_text = self.font_hud.render(title, True, (255, 255, 255))
            screen.blit(btn_text, (512 - btn_text.get_width()//2, y + 16))
            
            self.main_menu_buttons.append({"rect": btn_rect, "action": action})

    def handle_main_menu_click(self, mouse_pos):
        for btn in self.main_menu_buttons:
            if btn["rect"].collidepoint(mouse_pos):
                act = btn["action"]
                if act == "START":
                    self.engine.state = "CUSTOMIZER"
                elif act == "LOAD_SAVE":
                    self.engine.settings_prev_state = "MAIN_MENU"
                    self.engine.state = "SETTINGS"
                elif act == "SETTINGS":
                    self.engine.settings_prev_state = "MAIN_MENU"
                    self.engine.state = "SETTINGS"
                elif act == "EXIT":
                    self.engine.running = False
                break

    # --- CHARACTER SELECT OVERLAY (GRID SYSTEM) ---
    def draw_customizer(self, screen):
        screen.fill((15, 15, 22))
        
        t_surf = self.font_large.render("SELECT YOUR SURVIVOR HERO", True, (255, 255, 255))
        screen.blit(t_surf, (512 - t_surf.get_width()//2, 40))
        
        sub_surf = self.font_main.render("Navigate categories. Each hero offers unique starting gear and abilities.", True, (150, 180, 200))
        screen.blit(sub_surf, (512 - sub_surf.get_width()//2, 85))

        self.customizer_buttons = []
        
        # 1. Scrollable Grid viewport coordinates
        list_box = pygame.Rect(64, 150, 332, 500)
        pygame.draw.rect(screen, (22, 28, 38), list_box, 0, 8)
        pygame.draw.rect(screen, (60, 80, 110), list_box, 2, 8)

        # Scroll Up/Down Button definitions
        up_rect = pygame.Rect(64, 114, 332, 30)
        pygame.draw.rect(screen, (32, 40, 55), up_rect, 0, 4)
        pygame.draw.rect(screen, (80, 100, 130), up_rect, 1, 4)
        up_t = self.font_hud.render("▲ SCROLL UP", True, (255, 255, 255))
        screen.blit(up_t, (230 - up_t.get_width()//2, 122))
        self.customizer_buttons.append({"rect": up_rect, "action": "SCROLL_UP", "index": None})

        down_rect = pygame.Rect(64, 656, 332, 30)
        pygame.draw.rect(screen, (32, 40, 55), down_rect, 0, 4)
        pygame.draw.rect(screen, (80, 100, 130), down_rect, 1, 4)
        down_t = self.font_hud.render("▼ SCROLL DOWN", True, (255, 255, 255))
        screen.blit(down_t, (230 - down_t.get_width()//2, 664))
        self.customizer_buttons.append({"rect": down_rect, "action": "SCROLL_DOWN", "index": None})

        # Predefined list of category ordering
        categories = [
            "Pop Music & Reality",
            "Marvel Universe",
            "DC Universe",
            "Star Wars",
            "Anime & Manga",
            "Vampires & Twilight",
            "Gilmore Girls",
            "SpongeBob SquarePants",
            "Stranger Things & Wednesday",
            "Gaming Legends",
            "Cinematic & TV Worlds"
        ]
        
        grouped = {cat: [] for cat in categories}
        grouped["Other"] = []
        for idx, char in enumerate(CHARACTERS_DB):
            grp = char.get("group", "Other")
            if grp in grouped:
                grouped[grp].append((idx, char))
            else:
                grouped["Other"].append((idx, char))
                
        # Calculate viewport constraints
        draw_y = 160 - self.char_grid_scroll_y
        total_height = 0
        
        # Viewport clip rendering
        screen.set_clip(pygame.Rect(66, 152, 328, 496))
        
        for cat in categories:
            if not grouped[cat]:
                continue
                
            # Render category header
            cat_lbl = self.font_hud.render(f"■ {cat.upper()}", True, (255, 215, 0))
            screen.blit(cat_lbl, (74, draw_y))
            draw_y += 24
            total_height += 24
            
            # Grid columns count = 4
            for c_idx, (idx, char) in enumerate(grouped[cat]):
                col = c_idx % 4
                row = c_idx // 4
                btn_x = 74 + col * 76
                btn_y = draw_y + row * 76
                
                cell_rect = pygame.Rect(btn_x, btn_y, 68, 68)
                selected = (self.engine.selected_character_idx == idx)
                bg_col = (45, 65, 95) if selected else (25, 30, 42)
                bd_col = (0, 220, 255) if selected else (55, 65, 80)
                bd_w = 3 if selected else 1
                
                pygame.draw.rect(screen, bg_col, cell_rect, 0, 6)
                pygame.draw.rect(screen, bd_col, cell_rect, bd_w, 6)
                
                # Render character 4x sprite preview scaled down inside cell
                self.draw_detailed_sprite(screen, btn_x + 9, btn_y + 3, char["theme"], scale=4.0, direction=1)
                
                # Register hit zone
                self.customizer_buttons.append({"rect": cell_rect, "action": "SELECT_INDEX", "index": idx})
                
            rows_count = (len(grouped[cat]) - 1) // 4 + 1
            draw_y += rows_count * 76 + 12
            total_height += rows_count * 76 + 12
            
        screen.set_clip(None)
        
        # Scroll clamp variables
        self.max_scroll_y = max(0, total_height - 470)

        # 2. Right Panel: Detailed Profile Card
        prof_box = pygame.Rect(416, 114, 544, 572)
        pygame.draw.rect(screen, (32, 38, 48), prof_box, 0, 8)
        pygame.draw.rect(screen, (80, 100, 130), prof_box, 3, 8)

        sel_char = CHARACTERS_DB[self.engine.selected_character_idx]
        
        name_surf = self.font_large.render(sel_char["name"], True, (255, 220, 80))
        screen.blit(name_surf, (440, 136))
        
        orig_surf = pygame.font.SysFont("Courier", 14, italic=True).render(f"Origin: {sel_char['origin']}", True, (200, 220, 255))
        screen.blit(orig_surf, (440, 172))

        # 4x Detailed Profile Preview Box
        avatar_box = pygame.Rect(440, 200, 96, 110)
        pygame.draw.rect(screen, (22, 28, 38), avatar_box, 0, 6)
        pygame.draw.rect(screen, (60, 80, 110), avatar_box, 2, 6)
        self.draw_character_preview(screen, 460, 202, sel_char["theme"], scale=3.6)

        # Stats meters
        stats_y = 200
        stats_labels = [
            ("Max Health", sel_char["stats"]["max_health"], 200, (220, 50, 50)),
            ("Move Speed", sel_char["stats"]["move_speed"], 2.0, (50, 200, 80)),
            ("Armor Block", sel_char["stats"]["armor"], 10, (180, 180, 180)),
            ("Magnet Range", sel_char["stats"]["magnet_range"], 5.0, (0, 200, 255))
        ]
        
        for idx, (label, val, max_val, color) in enumerate(stats_labels):
            sy = stats_y + idx * 30
            lbl = self.font_hud.render(f"{label}:", True, (200, 200, 200))
            screen.blit(lbl, (554, sy))
            
            bar_pct = val / max_val
            pygame.draw.rect(screen, (40, 45, 55), (664, sy + 4, 180, 10))
            pygame.draw.rect(screen, color, (664, sy + 4, int(180 * bar_pct), 10))
            
            val_txt = self.font_hud.render(str(val), True, (255, 255, 255))
            screen.blit(val_txt, (856, sy))

        pygame.draw.line(screen, (50, 65, 85), (440, 325), (936, 325), 2)

        w_title = self.font_sub.render(f"Weapon: {sel_char['starting_weapon']}", True, (255, 255, 255))
        screen.blit(w_title, (440, 340))

        ab_title = self.font_sub.render(f"Ability: {sel_char['unique_ability']['name']}", True, (0, 220, 255))
        screen.blit(ab_title, (440, 375))
        
        ab_lines = self.wrap_text(sel_char["unique_ability"]["description"], 490)
        for idx, l in enumerate(ab_lines):
            l_surf = self.font_main.render(l, True, (200, 210, 220))
            screen.blit(l_surf, (440, 400 + idx * 18))

        cr_y = 400 + len(ab_lines) * 18 + 15
        cr_title = self.font_sub.render("Colony Crafting Bonus:", True, (100, 255, 130))
        screen.blit(cr_title, (440, cr_y))
        
        cr_lines = self.wrap_text(sel_char["crafting_bonus"], 490)
        for idx, l in enumerate(cr_lines):
            l_surf = self.font_main.render(l, True, (200, 210, 220))
            screen.blit(l_surf, (440, cr_y + 25 + idx * 18))

        # Select Button
        start_btn = pygame.Rect(540, 610, 300, 48)
        pygame.draw.rect(screen, (30, 80, 50), start_btn, 0, 8)
        pygame.draw.rect(screen, (100, 220, 130), start_btn, 3, 8)
        
        btn_txt = self.font_hud.render("SELECT SURVIVOR [ENTER]", True, (255, 255, 255))
        screen.blit(btn_txt, (690 - btn_txt.get_width()//2, 626))
        self.customizer_buttons.append({"rect": start_btn, "action": "START", "index": None})

    def handle_customizer_click(self, mouse_pos):
        for btn in self.customizer_buttons:
            if btn["rect"].collidepoint(mouse_pos):
                action = btn["action"]
                index = btn["index"]
                
                if action == "START":
                    self.engine.start_game()
                elif action == "SELECT_INDEX":
                    self.engine.selected_character_idx = index
                elif action == "SCROLL_UP":
                    self.char_grid_scroll_y = max(0, self.char_grid_scroll_y - 76)
                elif action == "SCROLL_DOWN":
                    self.char_grid_scroll_y = min(getattr(self, "max_scroll_y", 500), self.char_grid_scroll_y + 76)
                break


    # --- HUD & PLAYING DRAW ---
    def draw_hud(self, screen):
        p = self.engine.player
        zoom = self.engine.zoom
        
        cam_shake_x = 0
        cam_shake_y = 0
        if self.engine.combat_manager.screen_shake > 0:
            intensity = int(self.engine.combat_manager.screen_shake * 12)
            cam_shake_x = random.randint(-intensity, intensity)
            cam_shake_y = random.randint(-intensity, intensity)
        
        cx = p.camera_x + cam_shake_x
        cy = p.camera_y + cam_shake_y
        
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

        if self.engine.combat_manager.parry_flash_timer > 0.0:
            flash_surf = pygame.Surface((1024, 768), pygame.SRCALPHA)
            flash_surf.fill((255, 255, 255, 120))
            screen.blit(flash_surf, (0, 0))

        # Top Panel
        pygame.draw.rect(screen, (20, 20, 30), (0, 0, 1024, 45))
        pygame.draw.line(screen, (50, 50, 70), (0, 45), (1024, 45), 2)

        mins = int(self.engine.survival_time // 60)
        secs = int(self.engine.survival_time % 60)
        time_txt = f"SURVIVED: {mins:02d}:{secs:02d}"
        t_surf = self.font_hud.render(time_txt, True, (255, 255, 255))
        screen.blit(t_surf, (512 - t_surf.get_width()//2, 14))

        xp_pct = p.xp / p.xp_to_next
        pygame.draw.rect(screen, (40, 45, 60), (250, 5, 524, 6))
        pygame.draw.rect(screen, (0, 220, 255), (250, 5, int(524 * xp_pct), 6))
        
        lvl_surf = self.font_hud.render(f"LVL {p.level}", True, (0, 220, 255))
        screen.blit(lvl_surf, (200, 2))

        # Shift guide display
        guide_surf = self.font_hud.render("[O] Settings [T] Base Camp [F] Use [Shift] Block", True, (160, 180, 200))
        screen.blit(guide_surf, (635, 14))

        # Resource Display
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
        screen.blit(st_surf, (1004 - st_surf.get_width(), 702))

        # Ultimate cooldown indicator
        ult_timer = self.engine.combat_manager.ultimate_timer
        if ult_timer > 0:
            ult_pct = ult_timer / self.engine.combat_manager.ultimate_cooldown
            # Draw a nice small cooldown bar below the stance name
            bar_w = 150
            bar_h = 6
            bx = 1004 - bar_w
            by = 746
            pygame.draw.rect(screen, (40, 20, 20), (bx, by, bar_w, bar_h))
            pygame.draw.rect(screen, (255, 140, 0), (bx, by, int(bar_w * (1 - ult_pct)), bar_h))
            
            # Cooldown text
            cd_txt = self.font_hud.render(f"ULT CD: {ult_timer:.1f}s", True, (255, 140, 0))
            screen.blit(cd_txt, (1004 - cd_txt.get_width(), 727))
        else:
            # Ready indicator!
            rdy_txt = self.font_hud.render("ULT READY [Q/E]", True, (50, 255, 100))
            screen.blit(rdy_txt, (1004 - rdy_txt.get_width(), 727))

        # Bottom center toolbar
        toolbar_start_x = 512 - 144
        toolbar_y = 705
        
        # 6 slots * 48px = 288px. plus padding = 294px
        pygame.draw.rect(screen, (15, 15, 20), (toolbar_start_x - 6, toolbar_y - 6, 294, 54), 0, 6)
        pygame.draw.rect(screen, (50, 60, 75), (toolbar_start_x - 6, toolbar_y - 6, 294, 54), 2, 6)

        slot_names = ["Pick", "Katana", "Block", "Torch", "Water", "Wind"]
        
        # Check if custom starting weapon name exists
        custom_weapon_name = getattr(p, "starting_weapon", "Katana")
        # Abbreviate to fit toolbar box
        if len(custom_weapon_name) > 8:
            custom_weapon_name = custom_weapon_name[:6] + ".."
        slot_names[1] = custom_weapon_name

        for i in range(6):
            slot_x = toolbar_start_x + i * 48
            slot_rect = pygame.Rect(slot_x, toolbar_y, 42, 42)
            
            bg_col = (45, 55, 70) if p.active_slot == i else (25, 30, 40)
            pygame.draw.rect(screen, bg_col, slot_rect, 0, 4)
            
            bd_col = (255, 215, 0) if p.active_slot == i else (70, 80, 95)
            bd_w = 3 if p.active_slot == i else 1
            pygame.draw.rect(screen, bd_col, slot_rect, bd_w, 4)
            
            t_col = (255, 255, 255) if p.active_slot == i else (160, 170, 185)
            s_font = pygame.font.SysFont("Courier", 9, bold=True)
            lbl_surf = s_font.render(slot_names[i], True, t_col)
            screen.blit(lbl_surf, (slot_x + 21 - lbl_surf.get_width()//2, toolbar_y + 15))
            
            k_surf = s_font.render(str(i+1), True, (120, 140, 160))
            screen.blit(k_surf, (slot_x + 4, toolbar_y + 4))

            if i == 2: # Block stack display
                stk_surf = pygame.font.SysFont("Courier", 8, bold=True).render(f"x{self.engine.iron//2}", True, (200, 200, 200))
                screen.blit(stk_surf, (slot_x + 38 - stk_surf.get_width(), toolbar_y + 30))

        # Floating loot notifications
        dt = self.engine.clock.get_time() / 1000.0
        curr_notif_y = 645
        for notif in self.loot_notifications[:]:
            notif["timer"] -= dt
            if notif["timer"] <= 0:
                self.loot_notifications.remove(notif)
                continue
            
            # Fade out alpha
            alpha = int(min(1.0, notif["timer"] / 0.5) * 255)
            item = notif["item"]
            rarity_colors = {
                "COMMON": (230, 230, 230),
                "RARE": (50, 150, 255),
                "EPIC": (160, 50, 240),
                "LEGENDARY": (255, 140, 0)
            }
            color = rarity_colors.get(item["rarity"], (255, 255, 255))
            
            notif_txt = f"+ {item['rarity']} {item['name']}"
            notif_surf = self.font_hud.render(notif_txt, True, color)
            
            # Surface with alpha
            alpha_surf = pygame.Surface(notif_surf.get_size(), pygame.SRCALPHA)
            alpha_surf.fill((255, 255, 255, alpha))
            alpha_surf.blit(notif_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            
            float_offset = int((2.5 - notif["timer"]) * 14)
            nx = 512 - alpha_surf.get_width() // 2
            ny = curr_notif_y - float_offset
            screen.blit(alpha_surf, (nx, ny))
            curr_notif_y -= 18

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
                self.engine.apply_upgrade(btn["id"])
                break

    def draw_excel(self, screen):
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
            self.engine.state = "CUSTOMIZER"
