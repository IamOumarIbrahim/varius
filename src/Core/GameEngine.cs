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
    private UIManager _ui = new();
    private SoundManager _audio = new();

    // Game session state
    private float _survivalTime;
    private int _gold;
    private int _iron;
    private float _zoom = 1.5f;
    private List<NpcData> _rescuedNpcs = new();
    private int _characterSelectHover = -1;
    private int _characterSelectScroll = 0;
    private string[]? _levelUpChoices;
    private readonly Random _rng = new();
    private bool[] _saveSlotExists = new bool[3];

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
            case GameState.GameOver:
                if (InputManager.Escape) _state = GameState.MainMenu;
                break;
        }
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
        _world.UpdateClouds(dt);

        // Toolbar slot selection
        int slotKey = InputManager.ToolbarSlot();
        if (slotKey >= 0) _player.ActiveSlot = slotKey;
        int wheelDelta = InputManager.MouseWheelDelta;
        if (wheelDelta != 0)
        {
            _player.ActiveSlot = (_player.ActiveSlot - wheelDelta + 6) % 6;
        }

        // Use key (mining / swinging)
        if (InputManager.Use) _player.HandleUseKey(_world, _combat);
        else _player.HandleUseKeyReleased();

        // Panel toggles
        if (InputManager.Inventory) { _state = GameState.Inventory; return; }
        if (InputManager.Settings) { _state = GameState.Settings; return; }
        if (InputManager.Escape) { _state = GameState.Paused; return; }

        // Ultimate stance
        if (InputManager.Ultimate) CycleSance();

        // Player update
        _player.Update(dt, _world, _mobManager);

        // Mob update
        _mobManager.Update(dt, _player, _world, _combat);

        // Combat update
        _combat.Update(dt, _player, _world, _mobManager.Mobs);

        // Death check
        if (_player.Health <= 0)
        {
            _state = GameState.GameOver;
            AutoSave();
            return;
        }

        // Level-up check
        if (_player.XP >= _player.XPToNext)
        {
            _player.AddXP(0); // trigger level-up event
        }
    }

    private void CycleSance()
    {
        if (_player == null) return;
        _player.Stance = _player.Stance switch
        {
            Stance.Stone => Stance.Water,
            Stance.Water => Stance.Wind,
            Stance.Wind  => Stance.Stone,
            _            => Stance.Stone
        };
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
        float camX = _player.CamX;
        float camY = _player.CamY;

        _world.Draw(camX, camY, zoom);
        _mobManager?.Draw(camX, camY, zoom);
        _player.Draw(camX, camY, zoom);
        _combat?.Draw(camX, camY, zoom);
        _world.DrawLighting(camX, camY, zoom, _player.X + Player.W / 2f, _player.Y + Player.H / 2f,
            _player.Stance == Stance.Water, new List<(float, float)>());
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
        _survivalTime = 0;
        _gold = 0;
        _iron = 0;

        _ui.Zoom = _zoom;
        _state = GameState.Playing;
    }

    private void OnMinedBlock(int tile)
    {
        switch (tile)
        {
            case Constants.TileGold:
                _gold += 2 + _rng.Next(3);
                _ui.AddNotification("+Gold!", new Color(255, 215, 40, 255), 0, Constants.ScreenHeight - 80);
                break;
            case Constants.TileIron:
                _iron += 1 + _rng.Next(2);
                _ui.AddNotification("+Iron!", new Color(200, 160, 100, 255), 0, Constants.ScreenHeight - 80);
                break;
            case Constants.TileCage:
                _ui.AddNotification("NPC Freed!", new Color(100, 255, 160, 255), 0, Constants.ScreenHeight - 80);
                _rescuedNpcs.Add(new NpcData { Name = "Villager", Job = "Unassigned" });
                // Drop a random item
                if (_player != null && _player.Inventory.Count < 16)
                {
                    var item = Item.GenerateRandom(_player.Level);
                    _player.Inventory.Add(item);
                    _ui.AddNotification($"Found: {item.Name}!", item.RarityColor, 0, Constants.ScreenHeight - 96);
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
        // Minimal save — just to record the session ended
        var save = new SaveData
        {
            SurvivalTime = _survivalTime,
            Gold = _gold,
            Iron = _iron,
            Zoom = _zoom,
            RescuedNpcs = _rescuedNpcs,
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
                CharName = _player.CharDef.Name
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
        }
        _mobManager = new MobManager();
        _combat = new CombatManager();
        _state = GameState.Playing;
    }
}
