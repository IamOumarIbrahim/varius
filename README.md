# 🎮 Varius — Cave Survivor

> A Terraria × Vampire Survivors hybrid RPG — fully rewritten in **C# + Raylib** for native GPU performance.

![Version](https://img.shields.io/badge/version-v1.1--Release-brightgreen)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue)
![Language](https://img.shields.io/badge/language-C%23%20.NET%208-purple)
![Engine](https://img.shields.io/badge/renderer-Raylib--cs%206.1.1-green)

---

## 🚀 What is Varius?

Varius is a 2D side-scrolling action RPG survival game where you:
- ⛏️ **Mine** through procedurally generated cave worlds
- ⚔️ **Fight** increasingly difficult waves of enemies and mini-bosses
- 🏕️ **Build** a colony by rescuing caged NPCs
- 🎭 **Play as** one of **49 unique characters** from pop culture, anime, TV, and gaming
- 📈 **Level up** with randomised upgrade choices and reforge weapon levels

---

## ✨ Features (v1.1 Release)

### 🧑‍🎨 49 Selectable Characters (grouped by universe)
Characters are visually drawn as **detailed pixel-art sprites** rendered procedurally with no image files.

| Group | Characters |
|---|---|
| 🎵 Pop Music | Ariana Grande, Sabrina Carpenter, Taylor Swift, Chappell Roan, Olivia Rodrigo, Dua Lipa |
| 🧛 Vampire Diaries | Damon Salvatore |
| 📚 Gilmore Girls | Rory Gilmore |
| 🕸️ Wednesday | Wednesday Addams |
| 🔬 Breaking Bad | Walter White, Jesse Pinkman |
| 🍳 The Bear | Carmy Berzatto |
| 🦸 Marvel | Deadpool, Spider-Man, Thor, Black Widow |
| 💥 The Boys | Homelander, Billy Butcher |
| 🏴‍☠️ One Piece | Nami, Zoro |
| 👊 Jujutsu Kaisen | Gojo Satoru, Nobara Kugisaki, Yuji Itadori |
| ⚔️ Attack on Titan | Levi, Mikasa, Eren |
| 🌀 Naruto | Naruto Uzumaki, Sasuke Uchiha |
| 🎤 Vocaloid | Miku Hatsune |
| 🌸 Anime | Rem, Zero Two |
| 🔫 Arcane | Jinx, Vi, Ekko |
| 🔎 Sherlock | Sherlock Holmes, John Watson |
| 🗡️ The Witcher | Geralt, Ciri |
| 🐉 Game of Thrones | Daenerys, Jon Snow |
| ❄️ Animated | Elsa, Moana |
| 🤠 Gaming | Arthur Morgan, Joel Miller, Ellie Williams |
| 👽 Stranger Things | Max Mayfield, Eleven |
| 🏹 Folklore | Robin Hood, Mulan |

Each character has:
- Unique base stats (HP, speed, armor, magnet range)
- A signature starting weapon and reforge tier
- A unique passive/active ability
- A distinct pixel-art color theme

### 🌍 World & Weather
- **Procedurally generated** cave worlds (200×100 tiles) with cellular automata cave smoothing
- Animated sky with a sun, moon, rays, and parallax clouds
- **Dynamic Weather System**: screen rain on the surface, snowflakes in the Ice biome, volcanic embers in Magma, and purple void sparkles in the Ruins.
- Tile types: Grass, Dirt, Stone, Iron, Gold, Coal, Bedrock, Torch, Cage, Boss Chest, Ancient Brick, Obsidian, Frost Crystal, Ember Stone, Runic Shard
- **Day/Night Cycle**: smooth sky shifts, night darkness, and 3x faster surface enemy spawn rates at night.

### 🎮 Controls
| Key | Action |
|---|---|
| `A` / `D` | Move left / right |
| `Space` | Jump |
| `F` | Use tool (direction determined by WASD held) |
| `1–6` | Select toolbar slot |
| `Scroll` | Cycle toolbar |
| `Q` / `E` | Cycle stance (Stone → Water → Wind) |
| `I` | Inventory |
| `B` | Build camp |
| `T` | Town panel |
| `O` | Settings |
| `ESC` | Pause / back |

### 🛡️ Combat & Status Effects
- 3 stances: **Stone** (melee sword), **Water** (spear), **Wind** (whip)
- **Status Effects**:
  - **Freeze** (Water / Elsa): Slows enemies to 15% speed, halts attack spits, and tints them cyan.
  - **Burn** (Stone): Inflicts fire damage over time and tints them orange-red.
  - **Bleed** (Wind): Inflicts deep bleed damage over time and tints them red.
- **Stance Blast**: switching stances at 100% stance charge gauges triggers a screen-shaking explosion.
- 3 Mini-boss Arenas: Giant Slime, Shadow Wraith, Magma Golem. Spawns **Boss Chest** containing Legendary loot upon defeat.

### 🎒 Inventory, Reforges, and Research
- Detailed inventory screen with **Item Hover Tooltips** listing detailed stats and rarity colors.
- **NPC Colony Jobs**: assign rescued villagers to facilities:
  - **Merchant** (House): trades Gold for Iron, Gold, and Runic Shards.
  - **Blacksmith** (Forge): Reforges weapon damage (e.g. `KATANA +3`) and upgrades armor.
  - **Scholar** (Library): researches permanent Critical Rate and Magnet Range upgrades.
- NPC Dialogue interfaces featuring character-specific speech bubble text and pop-culture easter eggs.

### 📈 Progression & Sound
- XP → Level Up with 3 randomized upgrade choices per level
- **Procedural 8-bit Audio Synthesizer**: generates and plays raw PCM retro waves (sine, square, sweeps) in memory for all SFX without external file assets.

---

## 🏗️ Architecture (C# Modular)

```
src/
├── Core/
│   ├── Constants.cs      # All game constants
│   ├── GameEngine.cs     # Main game loop & state machine
│   ├── GameState.cs      # Game state enum
│   └── InputManager.cs   # Keyboard/mouse input abstraction
├── Data/
│   ├── CharacterData.cs  # All 49 character definitions + groups
│   └── SaveSystem.cs     # JSON save/load
├── World/
│   ├── World.cs          # World generation, tiles, lighting, clouds
│   ├── Biome.cs          # Biome boundaries, helper color lookups
│   └── WeatherSystem.cs  # Rain, snow, embers, sparkles particle simulation
├── Entities/
│   ├── Player.cs         # Player physics, abilities, drawing, reforge tracking
│   ├── PlayerStats.cs    # Stats class with item bonus application
│   ├── Item.cs           # Item generation, drops, legendary chest modifiers
│   ├── Boss.cs           # Giant Slime, Magma Golem, Wraith AI and arenas
│   └── Mob.cs            # 6 mob types, AI timers, slow/bleed/burn status ticks
├── Combat/
│   ├── CombatManager.cs  # Projectiles, damage numbers, stance blasts, hit checks
│   └── FXManager.cs      # Camera screenshake and impact particles
├── Audio/
│   └── SoundManager.cs   # Procedural WAV-header synthesizer and audio device wrappers
└── UI/
    ├── UIManager.cs      # All UI: main menu, HUD, inventory tooltips, NPC shops, dialogues
    ├── Minimap.cs        # Explored-only Fog of War map overlay and surface compass
    └── CraftingPanel.cs  # Building camp structures and resource storage
Program.cs                # Entry point
```

---

## ⚙️ Requirements & Running

### Prerequisites
- [.NET 8 SDK](https://dotnet.microsoft.com/download/dotnet/8.0)
- GPU with OpenGL 3.3+ support (auto-detected)
- Windows / Linux / macOS

### Run
```bash
# From C:\Dev\Game
dotnet run
```

### Build Release
```bash
dotnet publish -c Release -r win-x64 --self-contained
```

---

## 📦 Dependencies

| Package | Version | Purpose |
|---|---|---|
| `Raylib-cs` | 6.1.1 | GPU-accelerated rendering (wraps Raylib C library) |
| `System.Text.Json` | Built-in | Save file serialization |

---

## 🔮 Roadmap

- [ ] Controller support
- [ ] Sound settings / track options
- [ ] Extra cave biomes (Ruins unique mobs)
- [ ] Full base-building mode

---

## 📜 Changelog

### v1.1 — Core Features & Upgrades
- Added **Dynamic Weather System** (surface rain, snow, magma embers, void sparkles).
- Implemented **Mob Status Effects** (Freeze, Burn, Bleed) with visual tint overlays.
- Added **Pop-Culture Abilities** for Naruto (Shadow Clone), Taylor/Sabrina (Diva Shockwaves), Arthur Morgan (Dead Eye Bullet Storm), and Elsa (Freeze on hit).
- Added **Boss Loot Chests** spawning upon boss defeats, awarding high-tier Legendary gear when mined.
- Integrated **NPC Speech Bubbles & Custom dialogues** in Town hall panels.
- Added **Explored Zone Fog of War** to the Minimap overlay.
- Programmed a surface **Day/Night Cycle** shifting sky colors and tripling night surface mob spawns.
- Added detailed **Item Stats Hover Tooltips** to the inventory.
- Added **Weapon Reforge levels** (`KATANA +X`) and green upgrade success popups.
- Fixed 19 audio device compilation, C# casting, and pointer namespace bugs.

### v1.0 — Audio & Colony Upgrade
- Added procedural 8-bit WAV memory synthesizer.
- Added Spider-Man wall crawl physics.
- Added automatic Vampire Survivors weapons.
- Added stance ult gauge blasts.
- Added Colony camp construction (Houses, Forges, Libraries) and jobs (Merchant, Blacksmith, Scholar).

### Beta 0.4 — C# Rewrite
- Translated entire Python codebase to native C# + Raylib-cs.
- Native GPU rendering and fog of war light halos.

*Built with ❤️ using C# + [Raylib](https://www.raylib.com/)*
