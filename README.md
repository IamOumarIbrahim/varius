# ⚔️ Varius

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Library-Pygame_2.6+-yellow.svg?style=flat-square&logo=python)](https://www.pygame.org/)
[![Theme](https://img.shields.io/badge/Theme-Catppuccin_Mocha-maroon.svg?style=flat-square)](https://github.com/catppuccin/catppuccin)
[![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey.svg?style=flat-square)](https://opensource.org/licenses/MIT)

A pixelated 2D action exploration game combining the swarm mechanics of **Vampire Survivors**, the block-mining world design of **Terraria**, the stance-based combat of **Ghost of Tsushima**, and a roster of 94 pop-culture selectable heroes.

---

## 📖 Table of Contents
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Quick Setup & Installation](#-quick-setup--installation)
- [How to Play](#-how-to-play)
  - [Controls Guide](#controls-guide)
  - [Combat Stances](#combat-stances)
- [Save & Load Management](#-save--load-management)
- [License](#-license)

---

## ✨ Key Features

- 👥 **94 Selectable Heroes**: Play as Dua Lipa, Saitama, Charli XCX, Moo Deng, Chappell Roan, Olivia Rodrigo, Steve Harrington, Goku, Zoro, and many more. Each features customized pixel color themes, stats (Max Health, Speed, Armor, Magnet), and custom starting weapons.
- 🎨 **4x Detailed Sprite Rendering**: Custom procedural rendering of high-fidelity character sprites with smooth shading, dynamic visual stances, and outlines.
- 🗂️ **Grouped Character Grid**: Select from your survivors in a clean categorized grid layout organized by show and universe origins.
- 📺 **Minecraft-Style 3D Main Screen**: Start new games, adjust settings, and load save states directly from a dedicated title screen featuring an extruded blocky logo.
- ⚔️ **Stance Combat System**: Swap between **Stone** (heavy posture break), **Water** (spinning auto-shield blades), and **Wind** (seeking projectile wind slashes) stances.
- 🛡️ **Parrying & Blocking**: Hold Shift to block damage or tap it at the perfect moment to trigger a **Perfect Parry** counter-attack that sweeps surrounding mobs.
- ☁️ **Parallax Sky & Caves**: Floating clouds and a glowing sun above-ground, transitioning into dark cave layers generated procedurally.
- 📦 **Colony Simulator**: Rescue trapped NPC captives inside cages and assign them jobs (Miner, Blacksmith, Scholar) at base camp to passively generate materials.
- 💾 **3-Slot Save State**: Instantly save or load your progress through the settings menu.

---

## ⚙️ System Architecture

The following block diagram outlines the internal layout and entity interaction pipeline of the game:

```mermaid
graph TD
    Main["main.py (Entrypoint)"] --> Engine["game_engine.py (GameEngine Loop & State Manager)"]
    Engine --> UI["ui.py (UIManager: Grouped Grid Select Lobby, Main Menu, Settings & Toolbar HUD)"]
    Engine --> Player["player.py (Player movement, stats & visual appearance)"]
    Engine --> Mobs["mobs.py (Mob spawning & AI logic)"]
    Engine --> Combat["combat.py (Parries, sweeps, orbits, project wind slashes)"]
    Engine --> World["world.py (Noise map generation, sky, floating clouds & sun)"]
    Engine --> Audio["sounds.py (Silent SoundManager, audio hooks)"]
    UI --> Char["characters.py (94 Pop-Culture DB characters grouped by universe)"]

    classDef default fill:#0f172a,stroke:#3b82f6,stroke-width:2px,color:#fff;
    classDef process fill:#1e1b4b,stroke:#a855f7,stroke-width:2px,color:#fff;
    class Player,Mobs,Combat,World,UI process;
```

---

## 🚀 Quick Setup & Installation

This game requires **Python 3.12+** and **Pygame 2.6+**.

### 1️⃣ Clone or Download
Ensure all files are placed in a single directory:
```bash
git clone <YOUR_REPO_URL>
cd <REPO_DIRECTORY>
```

### 2️⃣ Install Pygame
Install the required game rendering library:
```bash
pip install -r requirements.txt
```

### 3️⃣ Launch the Game
Run the entry script:
```bash
python main.py
```

---

## 🛠️ How to Play

### Controls Guide
* **Movement**: `A` / `D` (or Left/Right Arrows)
* **Jump**: **`Space`** (or `W` / Up Arrow)
* **Block / Parry**: **`Left Shift`** or **`Right Shift`**
* **Toolbar Select**: Keys `1`–`5`
* **Use Selected Item / Attack**: **`F` Key**
  * Target tile is determined by movement keys (`W/A/S/D` or arrows) held at the moment of pressing `F`.
  * Select Slot 1 (Pickaxe) $\rightarrow$ Hold movement key towards target $\rightarrow$ Press `F` to mine.
  * Select Slot 2 (Katana/Unique weapon) $\rightarrow$ Press `F` to swing.
  * Select Slot 3 (Block) $\rightarrow$ Hold movement key towards target $\rightarrow$ Press `F` to build a dirt tile (requires iron).
  * Slots 4 & 5 (Stance triggers) $\rightarrow$ Press `F` to change combat stances.
* **Settings Panel**: Press **`O`** to open zoom adjustments and save slots.
* **Base Camp Management**: Press **`T`** to manage rescued survivors.

### Combat Stances
1. **Stone Stance** (Slot 2): Heavy physical strikes dealing massive posture damage and knockbacks.
2. **Water Stance** (Slot 4): Orbital shield blades spin around you, slicing passing monsters.
3. **Wind Stance** (Slot 5): Shoots wind slash waves targeting the closest enemy unit.

---

## 💾 Save & Load Management
Open settings with **`O`** and click **SAVE** or **LOAD** on any of the 3 slots. Game progress is serialized to local JSON files (`save_slot_1.json` to `save_slot_3.json`).

---

## 📄 License
This repository is licensed under the [MIT License](LICENSE).
