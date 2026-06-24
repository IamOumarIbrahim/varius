# 🎮 Varius — Cave Survivor

> A Terraria × Vampire Survivors hybrid RPG — fully rewritten in **C# + Raylib** for native GPU performance.

![Version](https://img.shields.io/badge/version-beta0.4-orange)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-blue)
![Language](https://img.shields.io/badge/language-C%23%20.NET%208-purple)
![Engine](https://img.shields.io/badge/renderer-Raylib--cs%206.1.1-green)

---

## 🚀 What is Varius?

Varius is a 2D side-scrolling action RPG survival game where you:
- ⛏️ **Mine** through procedurally generated cave worlds
- ⚔️ **Fight** increasingly difficult waves of enemies
- 🏕️ **Build** a colony by rescuing caged NPCs
- 🎭 **Play as** one of **49 unique characters** from pop culture, anime, TV, and gaming
- 📈 **Level up** with randomised upgrade choices

---

## ✨ Features (Beta 0.4)

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
- A signature starting weapon
- A unique passive/active ability
- A crafting bonus
- A distinct pixel-art color theme (skin, hair, shirt, pants, eyes)

### 🌍 World
- **Procedurally generated** cave worlds (200×100 tiles) with cellular automata cave smoothing
- Animated sky with a sun, rays, and parallax clouds
- Tile types: Grass, Dirt, Stone, Iron, Gold, Coal, Bedrock, Torch, Cage
- Per-tile visual detail: ore veins, crack patterns, animated torch flicker
- **Fog of War** / cave darkness with a radial player light and torch halos

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

### 🛡️ Combat & Stances
- 3 stances: **Stone** (melee sword), **Water** (spear), **Wind** (whip)
- Critical hit system with per-character crit rate/damage
- Projectile-based combat with enemy spit attacks
- Floating damage numbers (crits in orange, normal in yellow)
- 6 enemy types: Slime, Crawler, Bomber, Bat, Skeleton, Eyeball

### 🎒 Inventory & Items
- 3 equipment slots: Helmet, Ring, Cape
- 4 rarity tiers: Common, Rare, Epic, Legendary (color-coded)
- Items grant stat bonuses (Max HP, armor, crit rate, crit damage, move speed, magnet range)
- Click to equip; right-click equipped to unequip

### 📈 Progression
- XP → Level Up with 3 randomized upgrade choices per level
- Upgrades: Max HP, damage, speed, mining power, crit, magnet, armor, haste

### 💾 Save System
- JSON-based save files (`save_slot_0.json`)
- Load from main menu → Continue option

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
│   └── World.cs          # World generation, tiles, lighting, clouds
├── Entities/
│   ├── Player.cs         # Player physics, drawing, combat
│   ├── PlayerStats.cs    # Stats class with item bonus application
│   ├── Item.cs           # Item generation, drops, physics
│   └── Mob.cs            # 6 mob types + MobManager
├── Combat/
│   └── CombatManager.cs  # Projectiles, damage numbers, hit detection
├── Audio/
│   └── SoundManager.cs   # Audio stub (future procedural synthesis)
└── UI/
    └── UIManager.cs      # All UI: main menu, character select, HUD, inventory, settings
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

### Beta 0.5 (Planned)
- [ ] NPC town system (blacksmith, scholar, trader)
- [ ] Unique character abilities fully implemented
- [ ] Procedural audio synthesis
- [ ] Boss enemies
- [ ] Full base-building mode
- [ ] Controller support

---

## 📜 Changelog

### Beta 0.4 — C# Rewrite
- **Full codebase translation from Python/Pygame → C# + Raylib**
- Native GPU rendering (OpenGL via Raylib)
- Modular architecture with 12 source files across 7 modules
- 49 characters with procedural pixel-art sprite rendering
- Detailed world rendering: sky, sun, clouds, ore vein patterns, torch flicker, cave fog of war
- 6 enemy types with animated pixel-art bodies
- Full inventory system with equipment slots and item rarity
- Settings panel with volume, zoom, GPU toggle, fullscreen
- JSON save/load system

### Beta 0.3
- Added main menu (Varius 3D pixel logo)
- Character select screen with group categories and grid layout
- 4× sprite detail increase
- F-key uses movement direction for mining/combat

### Beta 0.2
- Added: Dua Lipa, Carmy Berzatto, and more characters
- Dynamic cave lighting and torches
- Stance ultimate system (Q/E keys)

### Beta 0.1
- Initial release: 50 characters, Terraria-style world, basic combat

---

*Built with ❤️ using C# + [Raylib](https://www.raylib.com/)*
