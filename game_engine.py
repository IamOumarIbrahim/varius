import pygame
import random
import os
import json
from world import World
from player import Player
from mobs import MobManager
from combat import CombatManager
from ui import UIManager
from sounds import SoundManager
from characters import CHARACTERS_DB

class GameEngine:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "CUSTOMIZER"  # States: CUSTOMIZER, PLAYING, LEVEL_UP, SETTINGS, TOWN, GAME_OVER
        
        # Audio Synthesizer (Programmatic Sound FX and melody loop)
        self.sound_manager = SoundManager()
        self.sound_manager.start_music()
        
        # Zoom state configuration (dynamically scalable tile size)
        self.zoom = 1.5
        
        # Player appearance customizer selections
        self.custom_colors = {
            "hair": (139, 69, 19),      # Brown
            "skin": (255, 224, 189),    # Peach
            "shirt": (0, 100, 200),     # Blue
            "pants": (50, 50, 50),      # Dark Grey
            "eyes": (0, 150, 50)        # Green
        }
        self.custom_options = {
            "hair": [(139, 69, 19), (220, 200, 50), (100, 50, 150), (200, 50, 50), (30, 30, 30)],
            "skin": [(255, 224, 189), (240, 184, 135), (255, 200, 150), (141, 85, 36), (220, 150, 100)],
            "shirt": [(0, 100, 200), (200, 40, 40), (40, 180, 40), (200, 100, 0), (180, 40, 180)],
            "pants": [(50, 50, 50), (30, 70, 30), (100, 100, 120), (120, 70, 40), (10, 10, 10)],
            "eyes": [(0, 150, 50), (30, 80, 200), (100, 60, 20), (50, 50, 50), (180, 0, 0)]
        }
        self.custom_indices = {"hair": 0, "skin": 0, "shirt": 0, "pants": 0, "eyes": 0}
        self.selected_character_idx = 0
        
        # Town and Resource Simulation (Colony stats)
        self.gold = 100
        self.iron = 20
        self.gold_per_sec = 0
        self.iron_per_sec = 0
        self.scholar_pts = 0
        self.scholar_pts_per_sec = 0
        self.rescued_npcs = []  # NPC dicts: {"name": str, "job": str, "level": int}
        
        # Game session metrics
        self.survival_time = 0.0
        self.town_tick_timer = 0.0
        self.level_choices = []
        
        # Subsystems
        self.world = None
        self.player = None
        self.mob_manager = None
        self.combat_manager = None
        self.ui_manager = UIManager(self)

    def start_game(self):
        # Create systems (passing self as engine)
        char_data = CHARACTERS_DB[self.selected_character_idx]
        self.world = World(width=160, height=80) 
        self.player = Player(
            x=80 * 16, 
            y=20 * 16, 
            colors=char_data["theme"],
            engine=self
        )
        # Apply selected character stats
        self.player.char_name = char_data["name"]
        self.player.stats["max_health"] = char_data["stats"]["max_health"]
        self.player.health = char_data["stats"]["max_health"]
        self.player.stats["armor"] = char_data["stats"]["armor"]
        self.player.stats["move_speed_mult"] = char_data["stats"]["move_speed"]
        self.player.stats["magnet_range"] = char_data["stats"]["magnet_range"]
        self.player.starting_weapon = char_data["starting_weapon"]
        self.player.unique_ability = char_data["unique_ability"]
        self.player.crafting_bonus = char_data["crafting_bonus"]
        
        self.combat_manager = CombatManager(self)
        self.mob_manager = MobManager(self)
        self.ui_manager = UIManager(self)
        
        # Reset counters
        self.survival_time = 0.0
        self.town_tick_timer = 0.0
        self.gold = 100
        self.iron = 20
        self.scholar_pts = 0
        self.rescued_npcs = []
        
        self.state = "PLAYING"

    def run(self):
        while self.running:
            dt = min(self.clock.tick(60) / 1000.0, 0.1)
            self.handle_events()
            self.update(dt)
            self.draw()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            # Delegate event handling to current state
            if self.state == "CUSTOMIZER":
                self.handle_customizer_event(event)
            elif self.state == "PLAYING":
                self.handle_playing_event(event)
                self.player.handle_event(event, self.world)
            elif self.state == "LEVEL_UP":
                self.handle_levelup_event(event)
            elif self.state == "SETTINGS":
                self.ui_manager.settings_panel.handle_event(event)
            elif self.state == "TOWN":
                self.ui_manager.town_panel.handle_event(event)
            elif self.state == "GAME_OVER":
                self.handle_gameover_event(event)

    def update(self, dt):
        if self.state == "PLAYING":
            self.survival_time += dt
            self.town_tick_timer += dt
            if self.town_tick_timer >= 1.0:
                self.town_tick_timer -= 1.0
                self.tick_town_simulation()
            
            # Update clouds and entities
            self.world.update_clouds(dt)
            self.player.update(dt, self.world)
            self.mob_manager.update(dt, self.world)
            self.combat_manager.update(dt)
            
            if self.player.health <= 0:
                self.state = "GAME_OVER"

    def draw(self):
        self.screen.fill((10, 10, 15))
        
        if self.state == "CUSTOMIZER":
            self.ui_manager.draw_customizer(self.screen)
        elif self.state in ["PLAYING", "LEVEL_UP", "SETTINGS", "TOWN"]:
            # Pass self.zoom to rendering methods
            self.world.draw(self.screen, self.player.camera_x, self.player.camera_y, self.zoom)
            self.mob_manager.draw(self.screen, self.player.camera_x, self.player.camera_y, self.zoom)
            self.combat_manager.draw(self.screen, self.player.camera_x, self.player.camera_y, self.zoom)
            self.player.draw(self.screen, self.zoom)
            
            # Draw HUD
            self.ui_manager.draw_hud(self.screen)
            
            # Render overlays on top
            if self.state == "LEVEL_UP":
                self.ui_manager.draw_levelup(self.screen)
            elif self.state == "SETTINGS":
                self.ui_manager.draw_settings(self.screen)
            elif self.state == "TOWN":
                self.ui_manager.draw_town(self.screen)
                
        elif self.state == "GAME_OVER":
            self.ui_manager.draw_gameover(self.screen)
            
        pygame.display.flip()

    # --- Event Handlers for UI states ---
    def handle_customizer_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.sound_manager.play("click")
                self.start_game()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            self.ui_manager.handle_customizer_click(mouse_pos)

    def handle_playing_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:
                self.sound_manager.play("click")
                self.state = "SETTINGS"
            elif event.key == pygame.K_t:
                self.sound_manager.play("click")
                self.state = "TOWN"
            # Toolbar Slots Selection 1-5
            elif event.key == pygame.K_1:
                self.player.active_slot = 0
            elif event.key == pygame.K_2:
                self.player.active_slot = 1
                self.player.change_stance("STONE")
            elif event.key == pygame.K_3:
                self.player.active_slot = 2
            elif event.key == pygame.K_4:
                self.player.active_slot = 3
                self.player.change_stance("WATER")
            elif event.key == pygame.K_5:
                self.player.active_slot = 4
                self.player.change_stance("WIND")
            elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                self.combat_manager.trigger_block_parry()
                
        elif event.type == pygame.USEREVENT:
            action = event.dict.get("action")
            if action == "MINE_BLOCK":
                tile = event.dict.get("tile")
                if tile == 3:    # IRON
                    self.iron += 3
                elif tile == 4:  # GOLD
                    self.gold += 25
                elif tile == 5:  # COAL
                    self.gold += 6
                else:            # DIRT/STONE
                    self.gold += 1
            elif action == "RESCUE_NPC":
                self.rescue_npc()
            elif action == "LEVEL_UP":
                self.trigger_levelup()

    def handle_levelup_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            self.ui_manager.handle_levelup_click(mouse_pos)

    def handle_gameover_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.sound_manager.play("click")
                self.state = "CUSTOMIZER"
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            self.ui_manager.handle_gameover_click(mouse_pos)

    # --- Save / Load Game state slots ---
    def save_game(self, slot_num):
        save_data = {
            "survival_time": self.survival_time,
            "gold": self.gold,
            "iron": self.iron,
            "scholar_pts": self.scholar_pts,
            "rescued_npcs": self.rescued_npcs,
            "zoom": self.zoom,
            "player": {
                "x": self.player.x,
                "y": self.player.y,
                "health": self.player.health,
                "posture": self.player.posture,
                "stance": self.player.stance,
                "active_slot": self.player.active_slot,
                "level": self.player.level,
                "xp": self.player.xp,
                "xp_to_next": self.player.xp_to_next,
                "stats": self.player.stats,
                "char_name": getattr(self.player, "char_name", "Hero"),
                "colors": self.player.colors,
                "starting_weapon": getattr(self.player, "starting_weapon", "Katana"),
                "unique_ability": getattr(self.player, "unique_ability", {"name": "", "description": ""}),
                "crafting_bonus": getattr(self.player, "crafting_bonus", "")
            },
            "world_grid": self.world.grid,
            "mobs": [
                {"x": mob.x, "y": mob.y, "type": mob.mob_type, "health": mob.health, "posture": mob.posture}
                for mob in self.mob_manager.mobs
            ],
            "gems": [
                {"x": gem.x, "y": gem.y, "value": gem.value}
                for gem in self.mob_manager.gems
            ]
        }
        filename = f"save_slot_{slot_num}.json"
        with open(filename, "w") as f:
            json.dump(save_data, f)
        # Play Save confirmation sound
        self.sound_manager.play("click")

    def load_game(self, slot_num):
        filename = f"save_slot_{slot_num}.json"
        if not os.path.exists(filename):
            return
            
        with open(filename, "r") as f:
            data = json.load(f)
            
        self.survival_time = data["survival_time"]
        self.gold = data["gold"]
        self.iron = data["iron"]
        self.scholar_pts = data["scholar_pts"]
        self.rescued_npcs = data["rescued_npcs"]
        self.zoom = data.get("zoom", 1.5)
        
        # Re-build world
        grid = data["world_grid"]
        self.world = World(width=len(grid), height=len(grid[0]))
        self.world.grid = grid
        
        # Re-build player
        p_data = data["player"]
        self.player = Player(
            x=p_data["x"], 
            y=p_data["y"], 
            colors=p_data.get("colors", self.custom_colors),
            engine=self
        )
        self.player.health = p_data["health"]
        self.player.posture = p_data["posture"]
        self.player.stance = p_data["stance"]
        self.player.active_slot = p_data.get("active_slot", 0)
        self.player.level = p_data["level"]
        self.player.xp = p_data["xp"]
        self.player.xp_to_next = p_data["xp_to_next"]
        self.player.stats = p_data["stats"]
        self.player.char_name = p_data.get("char_name", "Hero")
        self.player.starting_weapon = p_data.get("starting_weapon", "Katana")
        self.player.unique_ability = p_data.get("unique_ability", {"name": "", "description": ""})
        self.player.crafting_bonus = p_data.get("crafting_bonus", "")
        
        # Re-build managers
        self.combat_manager = CombatManager(self)
        self.mob_manager = MobManager(self)
        
        from mobs import Mob, XPGem
        for m in data["mobs"]:
            mob = Mob(m["x"], m["y"], m["type"])
            mob.health = m["health"]
            mob.posture = m["posture"]
            self.mob_manager.mobs.append(mob)
            
        for g in data["gems"]:
            gem = XPGem(g["x"], g["y"], g["value"])
            self.mob_manager.gems.append(gem)
            
        self.state = "PLAYING"

    # --- Town Simulation Calculations ---
    def tick_town_simulation(self):
        self.gold_per_sec = 0
        self.iron_per_sec = 0
        self.scholar_pts_per_sec = 0
        
        for npc in self.rescued_npcs:
            mult = npc["level"]
            if npc["job"] == "Blacksmith":
                self.gold_per_sec += 2 * mult
            elif npc["job"] == "Miner":
                self.iron_per_sec += 1 * mult
            elif npc["job"] == "Scholar":
                self.scholar_pts_per_sec += 1 * mult
        
        self.gold += self.gold_per_sec
        self.iron += self.iron_per_sec
        self.scholar_pts += self.scholar_pts_per_sec

    def rescue_npc(self):
        names = ["Aria", "Brom", "Cid", "Dara", "Eldrin", "Fiona", "Gideon", "Hilda"]
        name = random.choice(names) + f" #{random.randint(10, 99)}"
        new_npc = {
            "name": name,
            "job": "Unassigned",
            "level": 1
        }
        self.rescued_npcs.append(new_npc)
        return name

    def trigger_levelup(self):
        self.state = "LEVEL_UP"
        all_choices = [
            {"id": "max_health", "title": "Heart Upgrade", "desc": "Increase Max Health by 20"},
            {"id": "atk_power", "title": "Sharper Blade", "desc": "Increase Base DMG by 15%"},
            {"id": "crit_rate", "title": "Precision Striking", "desc": "Increase Crit Rate by 10%"},
            {"id": "parry_window", "title": "Calm Reflection", "desc": "Extend Parry Window by 30ms"},
            {"id": "auto_blade", "title": "Aura of Water", "desc": "Add +1 Water stance orbital blade"},
            {"id": "wind_haste", "title": "Swift Wind", "desc": "Increase Auto-Wind Haste by 20%"},
            {"id": "mining_speed", "title": "Steel Pickaxe", "desc": "Mine blocks 25% faster"}
        ]
        self.level_choices = random.sample(all_choices, 3)

    def apply_upgrade(self, upgrade_id):
        stats = self.player.stats
        if upgrade_id == "max_health":
            stats["max_health"] += 20
            self.player.health += 20
        elif upgrade_id == "atk_power":
            stats["base_dmg"] += 5
        elif upgrade_id == "crit_rate":
            stats["crit_rate"] = min(stats["crit_rate"] + 0.10, 1.0)
        elif upgrade_id == "parry_window":
            stats["parry_window_ms"] += 30
        elif upgrade_id == "auto_blade":
            self.combat_manager.water_blade_count += 1
        elif upgrade_id == "wind_haste":
            self.combat_manager.wind_slash_cooldown = max(self.combat_manager.wind_slash_cooldown - 0.2, 0.4)
        elif upgrade_id == "mining_speed":
            stats["mining_power"] += 1
        
        self.state = "PLAYING"
