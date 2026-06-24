// src/Core/GameEngine.cs
using Raylib_cs;
using System.Numerics;
using Varius.Audio;
using Varius.Combat;
using Varius.Data;
using Varius.Entities;
using Varius.UI;
using Varius.World;

namespace Varius.Core;

public class GameEngine
{
    private GameState _state = GameState.MainMenu;

    // Systems
    private GameWorld? _world;
    private Player? _player;
    private MobManager? _mobManager;
    private CombatManager? _combat;
    private FXManager _fx = new();
    private BossManager? _bossMgr;
    private Minimap? _minimap;
    private CraftingPanel _crafting = new();
    private UIManager _ui = new();
    private SoundManager _audio = new();
    private readonly WeatherSystem _weather = new();
    private readonly List<ItemDrop> _itemDrops = new();

    // Game session state
    private float _survivalTime;
    private float _timeOfDay = 12f;
    private int _gold;
    private int _iron;
    private float _zoom = 1.5f;
    private List<NpcData> _rescuedNpcs = new();
    private Vector2? _shadowClonePos;
    private float _shadowCloneTimer;
    private float _cloneAttackTimer;
    private int _characterSelectHover = -1;
    private int _characterSelectScroll = 0;
    private string[]? _levelUpChoices;
    private readonly Random _rng = new();
    private bool[] _saveSlotExists = new bool[3];
    private bool _showCrafting;

    // Level-up upgrade pool
    private static readonly string[] UpgradePool = {
        "+25 Max Health — Your max HP increases permanently.",
        "+15% Attack Damage — All attacks deal more damage.",
        "+10% Move Speed — You move faster.",
        "+1 Mining Power — Mine tiles faster.",
        "+5% Crit Chance — Land more critical hits.",
        "+0.3x Crit Damage — Critical hits hit harder.",
        "+0.8 Magnet Range — Items are attracted from farther away.",
        "+1 Armor — Reduce incoming damage by 1.",
        "+0.2 Attack Speed (Haste) — Faster swings.",
    };

    public void Run()
    {
        Raylib.InitWindow(Constants.ScreenWidth, Constants.ScreenHeight, Constants.Title);
        Raylib.SetTargetFPS(Constants.TargetFPS);
        Raylib.SetWindowState(ConfigFlags.ResizableWindow);

        // Check save slots
        for (int i = 0; i < 3; i++)
            _saveSlotExists[i] = SaveSystem.SlotExists(i);

        while (!Raylib.WindowShouldClose())
        {
            float dt = Raylib.GetFrameTime();
            dt = Math.Min(dt, 0.05f); // cap dt to avoid huge physics steps

            Update(dt);

            Raylib.BeginDrawing();
            Raylib.ClearBackground(new Color(8, 8, 14, 255));
            Draw();
            Raylib.EndDrawing();
        }

        _audio.Shutdown();
        Raylib.CloseWindow();
    }

    private void Update(float dt)
    {
        _audio.Update(dt);
        _ui.Update(dt);

        switch (_state)
        {
            case GameState.MainMenu:
                UpdateMainMenu();
                break;
            case GameState.CharacterSelect:
                UpdateCharacterSelect();
                break;
            case GameState.Playing:
                UpdatePlaying(dt);
                break;
            case GameState.Paused:
                if (InputManager.Escape) _state = GameState.Playing;
                break;
            case GameState.LevelUp:
                UpdateLevelUp();
                break;
            case GameState.Settings:
                UpdateSettings();
                break;
            case GameState.Inventory:
                if (InputManager.Inventory || InputManager.Escape)
                    _state = GameState.Playing;
                break;
            case GameState.Town:
                UpdateTown();
                break;
            case GameState.CampBuild:
                UpdateCampBuild();
                break;
            case GameState.GameOver:
                if (InputManager.Escape) _state = GameState.MainMenu;
                break;
        }
    }

    private void UpdateTown()
    {
        if (InputManager.Escape || InputManager.Town)
            _state = GameState.Playing;
    }

    private void UpdateCampBuild()
    {
        if (InputManager.Escape || InputManager.Camp)
            _state = GameState.Playing;
    }

    private void UpdateMainMenu()
    {
        // No logic here — handled in Draw via click returns
    }

    private void UpdateCharacterSelect()
    {
        if (InputManager.Escape)
            _state = GameState.MainMenu;
    }

    private void UpdatePlaying(float dt)
    {
        if (_player == null || _world == null || _mobManager == null || _combat == null) return;

        _survivalTime += dt;
        _timeOfDay += dt * 0.15f;
        if (_timeOfDay >= 24f) _timeOfDay -= 24f;
        _world.UpdateClouds(dt);
        _fx.Update(dt);

        // Toolbar slot selection
        int slotKey = InputManager.ToolbarSlot();
        if (slotKey >= 0) _player.ActiveSlot = slotKey;
        int wheelDelta = InputManager.MouseWheelDelta;
        if (wheelDelta != 0)
            _player.ActiveSlot = (_player.ActiveSlot - wheelDelta + 6) % 6;

        // Use key (mining / swinging) — triggers FX and sound
        if (InputManager.Use)
        {
            bool swung = _player.HandleUseKey(_world, _combat);
            if (swung)
            {
                _fx.Trails.SpawnSwingArc(_player.X + Player.W / 2f, _player.Y + Player.H / 2f,
                    _player.Direction, _player.Stance);
                if (_player.Toolbar[_player.ActiveSlot] == "PICKAXE")
                {
                    _audio.Play("mine");
                }
                else
                {
                    _audio.Play("swing");
                }
            }
        }
        else _player.HandleUseKeyReleased();

        // Panel toggles
        if (InputManager.Inventory) { _state = GameState.Inventory; return; }
        if (InputManager.Settings)  { _state = GameState.Settings; return; }
        if (InputManager.Escape)    { _state = GameState.Paused; return; }
        if (Raylib.IsKeyPressed(KeyboardKey.C)) { _showCrafting = !_showCrafting; }
        if (InputManager.Camp)      { _state = GameState.CampBuild; return; }
        if (InputManager.Town)
        {
            if (IsNearAnyStructure())
            {
                _state = GameState.Town;
            }
            else
            {
                _ui.AddNotification("Must be near a colony structure!", Color.Orange, 0, Constants.ScreenHeight - 80);
            }
            return;
        }

        // Ultimate stance
        if (InputManager.Ultimate) CycleSance();

        // Player update
        _player.Update(dt, _world, _mobManager);

        // Character active/passive ticks
        UpdateCharacterAbilityEffects();

        // Mob update
        _mobManager.Update(dt, _player, _world, _combat, _itemDrops, _timeOfDay);

        // Update item drops
        for (int i = _itemDrops.Count - 1; i >= 0; i--)
        {
            var drop = _itemDrops[i];
            bool pickedUp = drop.Update(dt, _player.X, _player.Y, Player.W, Player.H, _player.Stats.MagnetRange, _world);
            if (pickedUp)
            {
                _itemDrops.RemoveAt(i);
                if (_player.Inventory.Count < 16)
                {
                    _player.Inventory.Add(drop.Item);
                    _ui.AddNotification($"Looted: {drop.Item.Name}!", drop.Item.RarityColor, 0, Constants.ScreenHeight - 96);
                }
            }
            else if (drop.Lifetime <= 0)
            {
                _itemDrops.RemoveAt(i);
            }
        }

        // Combat update — hook into FX for hit impacts
        _combat.Update(dt, _player, _world, _mobManager.Mobs, _fx);

        // Boss update
        if (_bossMgr != null)
        {
            var bossProjs = _bossMgr.Update(dt, _player, _world, _fx);
            foreach (var p in bossProjs) _combat.AddProjectile(p);
        }

        // Biome ambient particles
        _world.BiomeParticles.Update(dt, _player.X, _player.Y, _world.Grid, _world.Width, _world.Height);

        // Weather update
        _weather.Update(dt, _player.CamX, _player.CamY, BiomeHelper.GetBiome((int)(_player.Y / Constants.TileSize)));

        // Minimap fog exploration
        _minimap?.Explore(_player.X, _player.Y, _world.Grid);

        // Crafting update
        if (_showCrafting) _crafting.Update(dt, _player);

        // Death check
        if (_player.Health <= 0)
        {
            _state = GameState.GameOver;
            AutoSave();
            return;
        }

        // Level-up check
        if (_player.XP >= _player.XPToNext)
            _player.AddXP(0);
    }

    private bool IsNearAnyStructure()
    {
        if (_player == null || _world == null) return false;
        float px = _player.X;
        float py = _player.Y;
        foreach (var s in _world.Structures)
        {
            float sx = s.Tx * Constants.TileSize;
            float sy = s.Ty * Constants.TileSize;
            float dx = px - sx;
            float dy = py - sy;
            if (MathF.Sqrt(dx * dx + dy * dy) < 120f) return true;
        }
        return false;
    }

    private void UpdateCharacterAbilityEffects()
    {
        if (_player == null || _mobManager == null || _fx == null || _world == null) return;
        float dt = Raylib.GetFrameTime();

        if (_player.TriggerShockwave)
        {
            _player.TriggerShockwave = false;
            _fx.Shake.Trigger(7f, 0.35f);
            _audio.Play("damage");
            float radius = 180f;
            foreach (var mob in _mobManager.Mobs)
            {
                if (mob.Dead) continue;
                float dx = mob.X - _player.X;
                float dy = mob.Y - _player.Y;
                float dist = MathF.Sqrt(dx * dx + dy * dy);
                if (dist <= radius)
                {
                    mob.Health -= 15;
                    mob.ApplySlow(4.0f);
                    _fx.SpawnHitImpact(mob.X + Mob.W / 2f, mob.Y + Mob.H / 2f, Stance.Wind, false);
                }
            }
            _ui.AddNotification("Wednesday's Cello Shockwave!", Color.Purple, 0, Constants.ScreenHeight - 110);
        }

        if (_player.TriggerLightning)
        {
            _player.TriggerLightning = false;
            Mob? closest = null;
            float minDist = 999999f;
            foreach (var mob in _mobManager.Mobs)
            {
                if (mob.Dead) continue;
                float dx = mob.X - _player.X;
                float dy = mob.Y - _player.Y;
                float dist = MathF.Sqrt(dx * dx + dy * dy);
                if (dist < minDist) { minDist = dist; closest = mob; }
            }

            if (closest != null)
            {
                _audio.Play("hit");
                _fx.Shake.Trigger(6f, 0.25f);
                closest.Health -= 35;
                closest.FlashTimer = 0.25f;
                _fx.SpawnHitImpact(closest.X + Mob.W / 2f, closest.Y + Mob.H / 2f, Stance.Water, true);
                
                foreach (var mob in _mobManager.Mobs)
                {
                    if (mob == closest || mob.Dead) continue;
                    float dx = mob.X - closest.X;
                    float dy = mob.Y - closest.Y;
                    float dist = MathF.Sqrt(dx * dx + dy * dy);
                    if (dist < 80f)
                    {
                        mob.Health -= 18;
                        mob.FlashTimer = 0.2f;
                    }
                }
                _ui.AddNotification("Thor's Lightning Strike!", Color.SkyBlue, 0, Constants.ScreenHeight - 110);
            }
        }

        if (_player.TriggerFreeze)
        {
            _player.TriggerFreeze = false;
            _audio.Play("mine");
            _fx.Shake.Trigger(4f, 0.4f);
            foreach (var mob in _mobManager.Mobs)
            {
                if (mob.Dead) continue;
                float sx = mob.X * _zoom - _player.CamX;
                float sy = mob.Y * _zoom - _player.CamY;
                if (sx >= 0 && sx < Constants.ScreenWidth && sy >= 0 && sy < Constants.ScreenHeight)
                {
                    mob.ApplySlow(5f);
                    mob.Health -= 8;
                    mob.FlashTimer = 0.3f;
                }
            }
            _ui.AddNotification("Gojo's Infinity Domain Freeze!", Color.DarkBlue, 0, Constants.ScreenHeight - 110);
        }

        if (_player.TriggerConcert)
        {
            _player.TriggerConcert = false;
            _audio.Play("level");
            float px = _player.X + Player.W / 2f;
            float py = _player.Y + Player.H / 2f;
            foreach (var mob in _mobManager.Mobs)
            {
                if (mob.Dead) continue;
                float dx = mob.X - px;
                float dy = mob.Y - py;
                float dist = MathF.Sqrt(dx * dx + dy * dy);
                if (dist < 220f)
                {
                    if (dist > 20f)
                    {
                        mob.X -= (dx / dist) * 45f;
                        mob.Y -= (dy / dist) * 45f;
                    }
                    mob.Health -= 12;
                    mob.FlashTimer = 0.2f;
                }
            }
            _ui.AddNotification("Miku's Concert Pull!", Color.Green, 0, Constants.ScreenHeight - 110);
        }

        if (_player.TriggerWatsonHeal)
        {
            _player.TriggerWatsonHeal = false;
            _audio.Play("level");
            _ui.AddNotification("Watson: Field Medicine!", Color.Green, 0, Constants.ScreenHeight - 110);
        }

        if (_player.TriggerStanceBlast)
        {
            _player.TriggerStanceBlast = false;
            _audio.Play("hit");
            _fx.Shake.Trigger(8f, 0.3f);
            float radius = 160f;
            foreach (var mob in _mobManager.Mobs)
            {
                if (mob.Dead) continue;
                float dx = mob.X - _player.X;
                float dy = mob.Y - _player.Y;
                float dist = MathF.Sqrt(dx * dx + dy * dy);
                if (dist <= radius)
                {
                    mob.Health -= 28;
                    mob.FlashTimer = 0.3f;
                    if (dist > 0)
                    {
                        mob.VX = (dx / dist) * 200f;
                        mob.VY = -120f;
                    }
                }
            }
            _ui.AddNotification("STANCE BLAST!", Color.Orange, 0, Constants.ScreenHeight - 110);
        }

        if (_player.TriggerClone)
        {
            _player.TriggerClone = false;
            _shadowClonePos = new Vector2(_player.X - 32, _player.Y);
            _shadowCloneTimer = 12f;
            _cloneAttackTimer = 0f;
            _audio.Play("level");
            _ui.AddNotification("Shadow Clone Jutsu!", Color.Orange, 0, Constants.ScreenHeight - 110);
        }

        if (_player.TriggerDiva)
        {
            _player.TriggerDiva = false;
            _audio.Play("level");
            _fx.Shake.Trigger(5f, 0.3f);
            float radius = 220f;
            foreach (var mob in _mobManager.Mobs)
            {
                if (mob.Dead) continue;
                float dx = mob.X - _player.X;
                float dy = mob.Y - _player.Y;
                float dist = MathF.Sqrt(dx * dx + dy * dy);
                if (dist <= radius)
                {
                    mob.Health -= 20;
                    mob.ApplySlow(5.0f);
                    _fx.SpawnHitImpact(mob.X + Mob.W / 2f, mob.Y + Mob.H / 2f, Stance.Wind, true);
                }
            }
            _ui.AddNotification($"{_player.CharDef.Name}'s Pop Diva Encore!", new Color(255, 105, 180, 255), 0, Constants.ScreenHeight - 110);
        }

        if (_player.TriggerDeadEye)
        {
            _player.TriggerDeadEye = false;
            _audio.Play("mine");
            _ui.AddNotification("Dead Eye Bullet Storm!", Color.Red, 0, Constants.ScreenHeight - 110);

            int count = 0;
            foreach (var mob in _mobManager.Mobs)
            {
                if (mob.Dead) continue;
                float dx = mob.X - _player.X;
                float dy = mob.Y - _player.Y;
                float dist = MathF.Sqrt(dx * dx + dy * dy);
                if (dist < 300f)
                {
                    float vx = (dx / dist) * 450f;
                    float vy = (dy / dist) * 450f;
                    _combat.SpawnProjectile(_player.X + Player.W / 2f, _player.Y + Player.H / 2f, vx, vy, (int)(_player.Stats.BaseDmg * 1.5f), false, Color.Yellow);
                    count++;
                    if (count >= 3) break;
                }
            }
            if (count > 0) _audio.Play("hit");
        }

        // Update Naruto Shadow Clone
        if (_shadowCloneTimer > 0 && _shadowClonePos.HasValue)
        {
            _shadowCloneTimer -= dt;
            if (_shadowCloneTimer <= 0)
            {
                _shadowClonePos = null;
            }
            else
            {
                float cX = _shadowClonePos.Value.X;
                float cY = _shadowClonePos.Value.Y;
                float dx = _player.X - cX;
                float dy = _player.Y - cY;
                float dist = MathF.Sqrt(dx * dx + dy * dy);
                if (dist > 30f)
                {
                    cX += (dx / dist) * 160f * dt;
                    cY += (dy / dist) * 160f * dt;
                    _shadowClonePos = new Vector2(cX, cY);
                }

                _cloneAttackTimer += dt;
                if (_cloneAttackTimer >= 1.2f)
                {
                    _cloneAttackTimer = 0f;
                    Mob? target = null;
                    float minDist = 99999f;
                    foreach (var mob in _mobManager.Mobs)
                    {
                        if (mob.Dead) continue;
                        float mdx = mob.X - cX;
                        float mdy = mob.Y - cY;
                        float mdist = MathF.Sqrt(mdx * mdx + mdy * mdy);
                        if (mdist < minDist) { minDist = mdist; target = mob; }
                    }
                    if (target != null && minDist < 200f)
                    {
                        float vx = ((target.X - cX) / minDist) * 260f;
                        float vy = ((target.Y - cY) / minDist) * 260f;
                        _combat.SpawnProjectile(cX, cY, vx, vy, (int)(_player.Stats.BaseDmg * 0.8f), false, new Color(130, 200, 255, 255));
                        _audio.Play("swing");
                    }
                }
            }
        }
    }

    private void BuildStructure(string type)
    {
        if (_player == null || _world == null) return;
        
        int ironCost = type switch { "HOUSE" => 10, "FORGE" => 15, "LIBRARY" => 8, _ => 999 };
        int goldCost = type switch { "HOUSE" => 20, "FORGE" => 30, "LIBRARY" => 50, _ => 999 };
        int coalCost = type switch { "FORGE" => 10, _ => 0 };
        int runicCost = type switch { "LIBRARY" => 3, _ => 0 };

        if (_iron < ironCost || _gold < goldCost || _crafting.Resources[Constants.RES_COAL] < coalCost || _crafting.Resources[Constants.RES_RUNIC] < runicCost)
        {
            _ui.AddNotification("Not enough materials!", Color.Red, 0, Constants.ScreenHeight - 80);
            return;
        }

        int ptx = (int)((_player.X + Player.W / 2f) / Constants.TileSize);
        int pty = (int)((_player.Y + Player.H) / Constants.TileSize);
        
        if (pty > Constants.SurfaceY + 2)
        {
            _ui.AddNotification("Can only build camps on surface!", Color.Red, 0, Constants.ScreenHeight - 80);
            return;
        }

        _iron -= ironCost;
        _gold -= goldCost;
        if (coalCost > 0) _crafting.Resources[Constants.RES_COAL] -= coalCost;
        if (runicCost > 0) _crafting.Resources[Constants.RES_RUNIC] -= runicCost;

        _world.Structures.Add(new Structure
        {
            Tx = ptx - 1,
            Ty = pty - 3,
            Type = type,
            Level = 1
        });

        _audio.Play("build");
        _ui.AddNotification($"{type} constructed!", Color.Green, 0, Constants.ScreenHeight - 80);
    }

    private void CycleSance()
    {
        if (_player == null) return;

        if (_player.StanceCharge >= 100f)
        {
            _player.StanceCharge = 0f;
            _player.TriggerStanceBlast = true;
        }

        _player.Stance = _player.Stance switch
        {
            Stance.Stone => Stance.Water,
            Stance.Water => Stance.Wind,
            Stance.Wind  => Stance.Stone,
            _            => Stance.Stone
        };
        _player.RecalculateStats();
    }

    private void UpdateLevelUp()
    {
        if (_levelUpChoices == null) return;
        // Handled in draw with click return
    }

    private void UpdateSettings()
    {
        if (InputManager.Settings || InputManager.Escape)
        {
            _zoom = _ui.Zoom;
            _state = _player == null ? GameState.MainMenu : GameState.Playing;
        }
    }

    private void Draw()
    {
        switch (_state)
        {
            case GameState.MainMenu:
                int menuResult = _ui.DrawMainMenu(_saveSlotExists);
                if (menuResult == 0) _state = GameState.CharacterSelect;
                else if (menuResult == 1) LoadGame(0);
                else if (menuResult == 2) { _ui.Zoom = _zoom; _state = GameState.Settings; }
                else if (menuResult == 3) Raylib.CloseWindow();
                break;

            case GameState.CharacterSelect:
                int charSelected = _ui.DrawCharacterSelect(ref _characterSelectHover, ref _characterSelectScroll);
                if (charSelected >= 0) StartNewGame(charSelected);
                if (InputManager.Escape) _state = GameState.MainMenu;
                break;

            case GameState.Playing:
                DrawPlayingScene();
                _ui.DrawHUD(_player!, _survivalTime);
                break;

            case GameState.Paused:
                DrawPlayingScene();
                DrawPauseOverlay();
                break;

            case GameState.LevelUp:
                DrawPlayingScene();
                if (_levelUpChoices != null)
                {
                    int chosen = _ui.DrawLevelUp(_levelUpChoices);
                    if (chosen >= 0)
                    {
                        ApplyLevelUpChoice(chosen);
                        _levelUpChoices = null;
                        _state = GameState.Playing;
                    }
                }
                break;

            case GameState.Settings:
                if (_player != null) DrawPlayingScene();
                _ui.DrawSettings();
                break;

            case GameState.Inventory:
                DrawPlayingScene();
                _ui.DrawInventory(_player!);
                break;

            case GameState.Town:
                DrawPlayingScene();
                _ui.DrawTown(_rescuedNpcs, ref _gold, ref _iron, _player!, _crafting);
                break;

            case GameState.CampBuild:
                DrawPlayingScene();
                string? structureToBuild = _ui.DrawCampBuild(_gold, _iron, _crafting);
                if (structureToBuild != null)
                {
                    BuildStructure(structureToBuild);
                    _state = GameState.Playing;
                }
                break;

            case GameState.GameOver:
                DrawPlayingScene();
                _ui.DrawGameOver(_survivalTime, 0);
                break;
        }
    }

    private void DrawPlayingScene()
    {
        if (_world == null || _player == null) return;
        float zoom = _zoom;

        // Apply camera shake offset
        var (shakeX, shakeY) = _fx.Shake.Update(0f); // called without dt since Update() already ran
        float camX = _player.CamX + shakeX;
        float camY = _player.CamY + shakeY;

        _world.Draw(camX, camY, zoom, _timeOfDay);
        _world.BiomeParticles.Draw(camX, camY, zoom);

        // Draw item drops
        foreach (var drop in _itemDrops)
            drop.Draw(camX, camY, zoom);

        _mobManager?.Draw(camX, camY, zoom);
        _bossMgr?.Draw(camX, camY, zoom);
        if (_shadowCloneTimer > 0 && _shadowClonePos.HasValue)
        {
            float sx = _shadowClonePos.Value.X * zoom - camX;
            float sy = _shadowClonePos.Value.Y * zoom - camY;
            Raylib.DrawRectangle((int)sx, (int)sy, (int)(Player.W * zoom), (int)(Player.H * zoom), new Color(80, 160, 255, 140));
            Raylib.DrawRectangleLines((int)sx, (int)sy, (int)(Player.W * zoom), (int)(Player.H * zoom), new Color(150, 220, 255, 200));
        }
        _player.Draw(camX, camY, zoom);
        _combat?.Draw(camX, camY, zoom);
        _fx.Draw(camX, camY, zoom);
        _world.DrawLighting(camX, camY, zoom, _player.X + Player.W / 2f, _player.Y + Player.H / 2f,
            _player.Stance == Stance.Water, new List<(float, float)>(), _timeOfDay);

        // Weather render
        _weather.Draw(camX, camY, zoom);

        // Minimap overlay (top-right)
        if (_minimap != null)
        {
            var bossPositions = new List<(float, float)>();
            if (_bossMgr != null)
                foreach (var arena in _bossMgr.Arenas)
                    if (!arena.Cleared && arena.BossRef != null)
                        bossPositions.Add((arena.BossRef.X, arena.BossRef.Y));
            _minimap.Draw(_player.X, _player.Y, _world.Grid, bossPositions);
        }

        // Crafting panel overlay
        if (_showCrafting) _crafting.Draw(_player);
    }

    private void DrawPauseOverlay()
    {
        int sw = Constants.ScreenWidth;
        int sh = Constants.ScreenHeight;
        Raylib.DrawRectangle(0, 0, sw, sh, new Color(0, 0, 0, 130));
        Raylib.DrawText("PAUSED", sw / 2 - Raylib.MeasureText("PAUSED", 40) / 2, sh / 2 - 50, 40, new Color(255, 215, 60, 255));
        Raylib.DrawText("[ESC] Resume  |  [I] Inventory  |  [O] Settings", sw / 2 - 200, sh / 2 + 20, 12, Color.White);
    }

    private void StartNewGame(int characterIndex)
    {
        _world = new GameWorld();
        // Find surface Y for player spawn
        int spawnX = Constants.WorldWidth / 2;
        int spawnY = Constants.SurfaceY - 2;
        float startX = spawnX * Constants.TileSize;
        float startY = spawnY * Constants.TileSize;

        _player = new Player(characterIndex, startX, startY);
        _player.OnMineBlock += OnMinedBlock;
        _player.OnLevelUp += OnLevelUp;

        _mobManager = new MobManager();
        _combat = new CombatManager();
        _fx = new FXManager();
        _crafting = new CraftingPanel();
        _bossMgr = new BossManager();
        _bossMgr.GenerateArenas(_world);
        _minimap = new Minimap(_world.Width, _world.Height);
        _survivalTime = 0;
        _gold = 0;
        _iron = 0;
        _itemDrops.Clear();

        _ui.Zoom = _zoom;
        _state = GameState.Playing;
    }

    private void OnMinedBlock(int tile)
    {
        string? resource = BiomeHelper.GetResourceDrop(tile);
        if (resource != null)
        {
            int amt = _rng.Next(1, 3);
            _crafting.AddResource(resource, amt);
        }

        switch (tile)
        {
            case Constants.TileGold:
                _gold += 2 + _rng.Next(3);
                _ui.AddNotification("+Gold!", new Color((byte)255, (byte)215, (byte)40, (byte)255), 0, Constants.ScreenHeight - 80);
                if (_player != null) _fx.SpawnMineImpact(_player.X + Player.W / 2f, _player.Y, Constants.TileGold);
                break;
            case Constants.TileIron:
                _iron += 1 + _rng.Next(2);
                _ui.AddNotification("+Iron!", new Color((byte)200, (byte)160, (byte)100, (byte)255), 0, Constants.ScreenHeight - 80);
                if (_player != null) _fx.SpawnMineImpact(_player.X + Player.W / 2f, _player.Y, Constants.TileIron);
                break;
            case Constants.TileFrostCrystal:
                _ui.AddNotification("+Frost Crystal!", new Color((byte)100, (byte)220, (byte)255, (byte)255), 0, Constants.ScreenHeight - 80);
                if (_player != null) _fx.SpawnMineImpact(_player.X + Player.W / 2f, _player.Y, Constants.TileFrostCrystal);
                break;
            case Constants.TileEmberStone:
                _ui.AddNotification("+Ember Stone!", new Color((byte)255, (byte)100, (byte)20, (byte)255), 0, Constants.ScreenHeight - 80);
                if (_player != null) _fx.SpawnMineImpact(_player.X + Player.W / 2f, _player.Y, Constants.TileEmberStone);
                break;
            case Constants.TileRunicShard:
                _ui.AddNotification("+Runic Shard!", new Color((byte)180, (byte)80, (byte)255, (byte)255), 0, Constants.ScreenHeight - 80);
                if (_player != null) _fx.SpawnMineImpact(_player.X + Player.W / 2f, _player.Y, Constants.TileRunicShard);
                break;
            case Constants.TileCage:
                _ui.AddNotification("NPC Freed!", new Color((byte)100, (byte)255, (byte)160, (byte)255), 0, Constants.ScreenHeight - 80);
                _rescuedNpcs.Add(new NpcData { Name = "Villager", Job = "Unassigned" });
                if (_player != null && _player.Inventory.Count < 16)
                {
                    var item = Item.GenerateRandom(_player.Level);
                    _player.Inventory.Add(item);
                    _ui.AddNotification($"Found: {item.Name}!", item.RarityColor, 0, Constants.ScreenHeight - 96);
                }
                break;
            case Constants.TileBossChest:
                _ui.AddNotification("BOSS CHEST OPENED!", new Color((byte)255, (byte)215, (byte)60, (byte)255), 0, Constants.ScreenHeight - 80);
                if (_player != null)
                {
                    var item = Item.GenerateLegendary(_player.Level + 4);
                    if (_player.Inventory.Count < 16)
                    {
                        _player.Inventory.Add(item);
                        _ui.AddNotification($"Looted: {item.Name}!", item.RarityColor, 0, Constants.ScreenHeight - 96);
                    }
                    else
                    {
                        _itemDrops.Add(new ItemDrop(_player.X, _player.Y, item));
                        _ui.AddNotification("Inventory full! Item dropped on ground.", Color.Orange, 0, Constants.ScreenHeight - 96);
                    }
                    _fx.SpawnMineImpact(_player.X + Player.W / 2f, _player.Y, Constants.TileBossChest);
                }
                break;
        }
    }

    private void OnLevelUp()
    {
        // Pick 3 random upgrades
        var pool = new List<string>(UpgradePool);
        var choices = new string[3];
        for (int i = 0; i < 3; i++)
        {
            int idx = _rng.Next(pool.Count);
            choices[i] = pool[idx];
            pool.RemoveAt(idx);
        }
        _levelUpChoices = choices;
        _state = GameState.LevelUp;
    }

    private void ApplyLevelUpChoice(int choice)
    {
        if (_player == null || _levelUpChoices == null) return;
        string text = _levelUpChoices[choice];
        if (text.Contains("Max Health"))        { _player.BaseStats.MaxHealth += 25; _player.RecalculateStats(); _player.Health = _player.Stats.MaxHealth; }
        else if (text.Contains("Attack Damage")) _player.BaseStats.BaseDmg *= 1.15f;
        else if (text.Contains("Move Speed"))    _player.BaseStats.MoveSpeedMult += 0.10f;
        else if (text.Contains("Mining Power"))  _player.BaseStats.MiningPower += 1;
        else if (text.Contains("Crit Chance"))   _player.BaseStats.CritRate += 0.05f;
        else if (text.Contains("Crit Damage"))   _player.BaseStats.CritDmg += 0.3f;
        else if (text.Contains("Magnet"))        _player.BaseStats.MagnetRange += 0.8f;
        else if (text.Contains("Armor"))         _player.BaseStats.Armor += 1;
        else if (text.Contains("Haste"))         _player.BaseStats.Haste += 0.2f;
        _player.RecalculateStats();
    }

    private void AutoSave()
    {
        if (_player == null || _world == null) return;

        var inventoryData = new List<ItemData>();
        foreach (var item in _player.Inventory)
            inventoryData.Add(Item.ToData(item));

        var equippedData = new Dictionary<string, ItemData?>();
        foreach (var kvp in _player.Equipped)
            equippedData[kvp.Key.ToString().ToUpper()] = kvp.Value != null ? Item.ToData(kvp.Value) : null;

        int[][] gridArray = new int[_world.Width][];
        for (int x = 0; x < _world.Width; x++)
        {
            gridArray[x] = new int[_world.Height];
            for (int y = 0; y < _world.Height; y++)
            {
                gridArray[x][y] = _world.Grid[x, y];
            }
        }

        var save = new SaveData
        {
            SurvivalTime = _survivalTime,
            Gold = _gold,
            Iron = _iron,
            Zoom = _zoom,
            RescuedNpcs = _rescuedNpcs,
            Structures = _world.Structures,
            WorldGrid = gridArray,
            Player = new PlayerSaveData
            {
                X = _player.X, Y = _player.Y,
                Health = _player.Health,
                Posture = _player.Posture,
                Stance = _player.Stance.ToString(),
                ActiveSlot = _player.ActiveSlot,
                Level = _player.Level,
                Xp = _player.XP,
                XpToNext = _player.XPToNext,
                CharacterIndex = _player.CharacterIndex,
                CharName = _player.CharDef.Name,
                Inventory = inventoryData,
                Equipped = equippedData
            }
        };
        SaveSystem.Save(save, 0);
        _saveSlotExists[0] = true;
    }

    private void LoadGame(int slot)
    {
        var save = SaveSystem.Load(slot);
        if (save == null) { _state = GameState.CharacterSelect; return; }
        _survivalTime = save.SurvivalTime;
        _gold = save.Gold;
        _iron = save.Iron;
        _zoom = save.Zoom;
        _rescuedNpcs = save.RescuedNpcs;
        _world = new GameWorld();

        if (save.WorldGrid != null)
        {
            for (int x = 0; x < _world.Width && x < save.WorldGrid.Length; x++)
            {
                if (save.WorldGrid[x] == null) continue;
                for (int y = 0; y < _world.Height && y < save.WorldGrid[x].Length; y++)
                {
                    _world.Grid[x, y] = save.WorldGrid[x][y];
                }
            }
        }
        _world.Structures = save.Structures ?? new();

        int charIdx = save.Player?.CharacterIndex ?? 0;
        _player = new Player(charIdx, save.Player?.X ?? 0, save.Player?.Y ?? 0);
        _player.OnMineBlock += OnMinedBlock;
        _player.OnLevelUp += OnLevelUp;

        if (save.Player != null)
        {
            _player.Health = save.Player.Health;
            _player.Level = save.Player.Level;
            _player.XP = save.Player.Xp;
            _player.XPToNext = save.Player.XpToNext;

            if (Enum.TryParse<Stance>(save.Player.Stance, true, out var stance))
                _player.Stance = stance;

            _player.ActiveSlot = save.Player.ActiveSlot;

            _player.Inventory.Clear();
            if (save.Player.Inventory != null)
            {
                foreach (var itemData in save.Player.Inventory)
                    _player.Inventory.Add(Item.FromData(itemData));
            }

            if (save.Player.Equipped != null)
            {
                foreach (var kvp in save.Player.Equipped)
                {
                    if (Enum.TryParse<ItemSlot>(kvp.Key, true, out var slotKey))
                        _player.Equipped[slotKey] = kvp.Value != null ? Item.FromData(kvp.Value) : null;
                }
            }
            _player.RecalculateStats();
        }

        _itemDrops.Clear();
        _mobManager = new MobManager();
        _combat = new CombatManager();
        _state = GameState.Playing;
    }
}
