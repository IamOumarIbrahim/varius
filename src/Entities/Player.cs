// src/Entities/Player.cs
using Raylib_cs;
using System.Numerics;
using Varius.Core;
using Varius.Data;

namespace Varius.Entities;

public enum Stance { Stone, Water, Wind }

public class Player
{
    // Position & physics
    public float X { get; set; }
    public float Y { get; set; }
    public float VX { get; set; }
    public float VY { get; set; }
    public bool OnGround { get; set; }
    public int Direction { get; set; } = 1; // 1=right, -1=left

    // Dimensions (unscaled, in world pixels)
    public const int W = Constants.PlayerWidth;
    public const int H = Constants.PlayerHeight;

    // Stats & progression
    public PlayerStats BaseStats { get; private set; } = new();
    public PlayerStats Stats { get; private set; } = new();
    public int Health { get; set; }
    public float Posture { get; set; }
    public int Level { get; set; } = 1;
    public int XP { get; set; }
    public int XPToNext { get; set; } = 100;

    // Stance & toolbar
    public Stance Stance { get; set; } = Stance.Stone;
    public string[] Toolbar { get; } = { "PICKAXE", "KATANA", "BLOCK", "TORCH", "WATER", "WIND" };
    public int ActiveSlot { get; set; }

    // Character identity
    public int CharacterIndex { get; set; }
    public CharacterDef CharDef { get; private set; }

    // Inventory & equipment
    public List<Item> Inventory { get; set; } = new();
    public Dictionary<ItemSlot, Item?> Equipped { get; set; } = new()
        { [ItemSlot.Helmet] = null, [ItemSlot.Ring] = null, [ItemSlot.Cape] = null };

    // Animation / interaction
    public bool IsMining { get; set; }
    public float MineTimer { get; set; }
    public (int tx, int ty)? MineTarget { get; set; }
    public bool IsSwinging { get; set; }
    public float SwingTimer { get; set; }
    public float FlashTimer { get; set; }

    // Camera
    public float CamX { get; set; }
    public float CamY { get; set; }

    // Character-specific timers
    private float _shockwaveTimer;

    public Player(int characterIndex, float startX, float startY)
    {
        CharacterIndex = characterIndex;
        CharDef = CharactersDB.All[characterIndex];
        X = startX;
        Y = startY;

        // Apply character base stats
        BaseStats.MaxHealth = CharDef.Stats.MaxHealth;
        BaseStats.MoveSpeedMult = CharDef.Stats.MoveSpeed;
        BaseStats.Armor = CharDef.Stats.Armor;
        BaseStats.MagnetRange = CharDef.Stats.MagnetRange;

        RecalculateStats();
        Health = Stats.MaxHealth;
        Posture = Stats.MaxPosture;
    }

    public void RecalculateStats()
    {
        Stats = BaseStats.Clone();
        foreach (var item in Equipped.Values)
            if (item != null) Stats.ApplyItemBonuses(item);
    }

    public Rectangle GetRect() => new(X, Y, W, H);

    public void Update(float dt, World.GameWorld world, object? mobManager = null)
    {
        // Gravity
        VY += Constants.Gravity * dt;
        if (VY > Constants.MaxFallSpeed) VY = Constants.MaxFallSpeed;

        // Posture recovery
        if (Posture < Stats.MaxPosture)
            Posture = MathF.Min(Posture + 18f * dt, Stats.MaxPosture);

        if (FlashTimer > 0) FlashTimer -= dt;
        if (SwingTimer > 0) { SwingTimer -= dt; if (SwingTimer <= 0) IsSwinging = false; }

        // Character passive
        switch (CharDef.Name)
        {
            case "Deadpool":
                Health = (int)MathF.Min(Health + Stats.MaxHealth * 0.03f * dt, Stats.MaxHealth);
                break;
            case "Wednesday Addams":
                _shockwaveTimer += dt;
                if (_shockwaveTimer >= 8f) { _shockwaveTimer = 0; /* shockwave event handled in engine */ }
                break;
        }

        // Movement
        float speed = Constants.WalkSpeed * Stats.MoveSpeedMult;
        if (Stance == Stance.Wind) speed *= 1.22f;
        VX = 0;
        if (InputManager.Left)  { VX = -speed; Direction = -1; }
        if (InputManager.Right) { VX =  speed; Direction =  1; }
        if (InputManager.Jump && OnGround) { VY = Constants.JumpForce; OnGround = false; }

        // Horizontal collision
        X += VX * dt;
        var cols = world.CheckTileCollision(GetRect());
        foreach (var c in cols)
        {
            if (VX > 0) X = c.X - W;
            else if (VX < 0) X = c.X + c.Width;
        }

        // Vertical collision
        Y += VY * dt;
        cols = world.CheckTileCollision(GetRect());
        OnGround = false;
        foreach (var c in cols)
        {
            if (VY > 0) { Y = c.Y - H; VY = 0; OnGround = true; }
            else if (VY < 0) { Y = c.Y + c.Height; VY = 0; }
        }

        // Mining tick
        if (IsMining && MineTarget.HasValue)
        {
            MineTimer += dt;
            float mineSpeed = 0.28f / Stats.MiningPower;
            if (MineTimer >= mineSpeed) { MineTimer = 0; CompleteMining(world); }
        }

        // Camera tracking
        float targetCamX = X * 1.5f - Constants.ScreenWidth / 2f;
        float targetCamY = Y * 1.5f - Constants.ScreenHeight / 2f;
        float smooth = Constants.CameraSmooth * dt;
        CamX += (targetCamX - CamX) * smooth;
        CamY += (targetCamY - CamY) * smooth;
        float maxCamX = world.Width * Constants.TileSize * 1.5f - Constants.ScreenWidth;
        float maxCamY = world.Height * Constants.TileSize * 1.5f - Constants.ScreenHeight;
        CamX = Math.Clamp(CamX, 0, Math.Max(0, maxCamX));
        CamY = Math.Clamp(CamY, 0, Math.Max(0, maxCamY));
    }

    public void HandleUseKey(World.GameWorld world, Combat.CombatManager combat)
    {
        var (adx, ady) = InputManager.GetActionDirection();
        if (adx == 0 && ady == 0) adx = Direction;

        int ptx = (int)((X + W / 2f) / Constants.TileSize);
        int pty = (int)((Y + H / 2f) / Constants.TileSize);
        int tx = ptx + adx;
        int ty = ady == -1 ? (int)(Y / Constants.TileSize) - 1 :
                 ady ==  1 ? (int)((Y + H) / Constants.TileSize) :
                             (int)((Y + H / 2f) / Constants.TileSize);

        string tool = Toolbar[ActiveSlot];
        switch (tool)
        {
            case "PICKAXE":
                if (world.GetTile(tx, ty) != Constants.TileAir)
                {
                    IsMining = true; MineTarget = (tx, ty); MineTimer = 0;
                    IsSwinging = true; SwingTimer = 0.22f;
                }
                break;
            case "KATANA":
                if (adx != 0) Direction = adx;
                IsSwinging = true; SwingTimer = 0.28f;
                combat.TriggerManualSwing(this);
                break;
            case "BLOCK":
                var placed = new Rectangle(tx * 16, ty * 16, 16, 16);
                if (world.GetTile(tx, ty) == Constants.TileAir && !Raylib.CheckCollisionRecs(GetRect(), placed))
                {
                    world.SetTile(tx, ty, Constants.TileDirt);
                    IsSwinging = true; SwingTimer = 0.15f;
                }
                break;
            case "TORCH":
                if (world.GetTile(tx, ty) == Constants.TileAir)
                {
                    world.SetTile(tx, ty, Constants.TileTorch);
                    IsSwinging = true; SwingTimer = 0.15f;
                }
                break;
            case "WATER":
                Stance = Stance.Water;
                IsSwinging = true; SwingTimer = 0.15f;
                break;
            case "WIND":
                Stance = Stance.Wind;
                IsSwinging = true; SwingTimer = 0.15f;
                break;
        }
    }

    public void HandleUseKeyReleased() { IsMining = false; MineTarget = null; }

    private void CompleteMining(World.GameWorld world)
    {
        if (!MineTarget.HasValue) return;
        var (tx, ty) = MineTarget.Value;
        int tile = world.GetTile(tx, ty);
        if (tile == Constants.TileCage)
        {
            world.SetTile(tx, ty, Constants.TileAir);
            OnMineBlock?.Invoke(tile);
        }
        else if (tile != Constants.TileAir)
        {
            world.SetTile(tx, ty, Constants.TileAir);
            OnMineBlock?.Invoke(tile);
        }
        IsMining = false; MineTarget = null;
    }

    public Action<int>? OnMineBlock { get; set; }

    public void TakeDamage(int amount)
    {
        if (FlashTimer > 0) return;
        Health -= amount;
        if (Health < 0) Health = 0;
        FlashTimer = 0.3f;
    }

    public void AddXP(int amount)
    {
        XP += amount;
        if (XP >= XPToNext) { XP -= XPToNext; Level++; XPToNext = (int)(XPToNext * 1.3f); OnLevelUp?.Invoke(); }
    }

    public Action? OnLevelUp { get; set; }

    public void EquipItem(int inventoryIndex)
    {
        if (inventoryIndex < 0 || inventoryIndex >= Inventory.Count) return;
        var item = Inventory[inventoryIndex];
        var slotKey = item.Slot;
        var current = Equipped[slotKey];
        Equipped[slotKey] = item;
        if (current != null) Inventory[inventoryIndex] = current;
        else Inventory.RemoveAt(inventoryIndex);
        int oldMax = Stats.MaxHealth;
        RecalculateStats();
        Health = Math.Clamp(Health + (Stats.MaxHealth - oldMax), 1, Stats.MaxHealth);
    }

    public void UnequipItem(ItemSlot slot)
    {
        var item = Equipped[slot];
        if (item == null || Inventory.Count >= 16) return;
        Inventory.Add(item);
        Equipped[slot] = null;
        RecalculateStats();
    }

    public void Draw(float camX, float camY, float zoom)
    {
        float sx = X * zoom - camX;
        float sy = Y * zoom - camY;
        DrawDetailedSprite((int)sx, (int)sy, zoom);
        DrawWeapon((int)sx, (int)sy, zoom);
        if (IsSwinging) DrawSwingArc((int)sx, (int)sy, zoom);
        if (IsMining && MineTarget.HasValue) DrawMiningCracks(camX, camY, zoom);
    }

    private void DrawDetailedSprite(int sx, int sy, float zoom)
    {
        var theme = CharDef.Theme;
        bool flash = FlashTimer > 0;
        var skinCol = flash ? new Color(255, 80, 80, 255) : theme.Skin;
        var hairCol = flash ? new Color(255, 80, 80, 255) : theme.Hair;
        var shirtCol = flash ? new Color(255, 80, 80, 255) : theme.Shirt;
        var pantsCol = flash ? new Color(255, 80, 80, 255) : theme.Pants;

        int w = (int)(W * zoom);
        int h = (int)(H * zoom);

        // Body proportions: head = 8px, torso = 10px, legs = 8px (at 16px tile scale)
        int headH = (int)(8 * zoom);
        int torsoH = (int)(10 * zoom);
        int legsH = (int)(8 * zoom);
        int headW = (int)(8 * zoom);
        int headOff = (w - headW) / 2;

        // ── LEGS ──────────────────────────────────────────────
        // Left leg
        Raylib.DrawRectangle(sx + (int)(2 * zoom), sy + headH + torsoH, (int)(4 * zoom), legsH, pantsCol);
        // Right leg
        Raylib.DrawRectangle(sx + w - (int)(6 * zoom), sy + headH + torsoH, (int)(4 * zoom), legsH, pantsCol);
        // Leg shadow lines
        Raylib.DrawRectangle(sx + (int)(2 * zoom), sy + headH + torsoH, 1, legsH, new Color(0, 0, 0, 60));
        Raylib.DrawRectangle(sx + w - (int)(6 * zoom) + (int)(3 * zoom), sy + headH + torsoH, 1, legsH, new Color(0, 0, 0, 60));
        // Shoes (slightly darker)
        var shoeCol = new Color(Math.Max(0, pantsCol.R - 30), Math.Max(0, pantsCol.G - 30), Math.Max(0, pantsCol.B - 30), 255);
        Raylib.DrawRectangle(sx + (int)(1 * zoom), sy + headH + torsoH + legsH - (int)(2 * zoom), (int)(5 * zoom), (int)(2 * zoom), shoeCol);
        Raylib.DrawRectangle(sx + w - (int)(6 * zoom) - 1, sy + headH + torsoH + legsH - (int)(2 * zoom), (int)(5 * zoom), (int)(2 * zoom), shoeCol);

        // ── TORSO ─────────────────────────────────────────────
        Raylib.DrawRectangle(sx + (int)(1 * zoom), sy + headH, w - (int)(2 * zoom), torsoH, shirtCol);
        // Shirt shading: darker left third
        Raylib.DrawRectangle(sx + (int)(1 * zoom), sy + headH, (int)(2 * zoom), torsoH, new Color(0, 0, 0, 40));
        // Shirt highlight: lighter strip top
        Raylib.DrawRectangle(sx + (int)(2 * zoom), sy + headH, w - (int)(4 * zoom), 1, new Color(255, 255, 255, 40));
        // Belt line at bottom of torso
        Raylib.DrawRectangle(sx + (int)(1 * zoom), sy + headH + torsoH - (int)(2 * zoom), w - (int)(2 * zoom), (int)(2 * zoom),
            new Color(Math.Max(0, pantsCol.R - 20), Math.Max(0, pantsCol.G - 20), Math.Max(0, pantsCol.B - 20), 255));

        // Arms
        int armW = (int)(3 * zoom), armH = (int)(7 * zoom);
        int armY = sy + headH + (int)(1 * zoom);
        Raylib.DrawRectangle(sx, armY, armW, armH, shirtCol);
        Raylib.DrawRectangle(sx + w - armW, armY, armW, armH, shirtCol);
        // Hands
        Raylib.DrawRectangle(sx, armY + armH - (int)(2 * zoom), armW, (int)(2 * zoom), skinCol);
        Raylib.DrawRectangle(sx + w - armW, armY + armH - (int)(2 * zoom), armW, (int)(2 * zoom), skinCol);

        // ── HEAD ──────────────────────────────────────────────
        // Head base (skin)
        Raylib.DrawRectangle(sx + headOff, sy, headW, headH, skinCol);
        // Skull top darker tint
        Raylib.DrawRectangle(sx + headOff, sy, headW, (int)(2 * zoom), new Color(0, 0, 0, 20));
        // Face: eyes
        var eyeCol = flash ? Color.White : theme.Eyes;
        int eyeY = sy + (int)(2 * zoom);
        int leftEyeX = Direction == 1 ? sx + headOff + (int)(5 * zoom) : sx + headOff + (int)(1 * zoom);
        int rightEyeX = Direction == 1 ? sx + headOff + (int)(1 * zoom) : sx + headOff + (int)(5 * zoom);
        Raylib.DrawRectangle(leftEyeX, eyeY, (int)(2 * zoom), (int)(2 * zoom), eyeCol);
        // Eye white highlight
        Raylib.DrawRectangle(leftEyeX + (int)(0.5f * zoom), eyeY, 1, 1, new Color(255, 255, 255, 180));
        // Mouth (small smile)
        Raylib.DrawRectangle(sx + headOff + (int)(2 * zoom), sy + (int)(5 * zoom), (int)(4 * zoom), 1, new Color(180, 100, 100, 200));

        // Hair
        Raylib.DrawRectangle(sx + headOff, sy, headW, (int)(3 * zoom), hairCol);
        // Hair highlight
        Raylib.DrawRectangle(sx + headOff + (int)(1 * zoom), sy, (int)(3 * zoom), 1, new Color(255, 255, 255, 60));

        // Hair style extras
        if (theme.HasPonytail)
        {
            int ptailX = Direction == 1 ? sx + headOff - (int)(3 * zoom) : sx + headOff + headW;
            Raylib.DrawRectangle(ptailX, sy + (int)(1 * zoom), (int)(3 * zoom), (int)(6 * zoom), hairCol);
        }
        if (theme.HasBraids)
        {
            Raylib.DrawRectangle(sx + headOff - (int)(1 * zoom), sy + headH - (int)(2 * zoom), (int)(2 * zoom), (int)(10 * zoom), hairCol);
            Raylib.DrawRectangle(sx + headOff + headW - (int)(1 * zoom), sy + headH - (int)(2 * zoom), (int)(2 * zoom), (int)(10 * zoom), hairCol);
        }

        // Stance indicator aura around character
        Color stanceAura = Stance switch
        {
            Stance.Stone => new Color(180, 150, 100, 35),
            Stance.Water => new Color(50, 150, 255, 35),
            Stance.Wind  => new Color(100, 230, 150, 35),
            _            => Color.Blank
        };
        if (stanceAura.A > 0)
            Raylib.DrawRectangle(sx - (int)(2 * zoom), sy - (int)(2 * zoom), w + (int)(4 * zoom), h + (int)(4 * zoom), stanceAura);

        // Character outline (1px dark border)
        Raylib.DrawRectangleLines(sx, sy, w, h, new Color(0, 0, 0, 120));
    }

    private void DrawWeapon(int sx, int sy, float zoom)
    {
        var theme = CharDef.Theme;
        int bx = Direction == 1 ? sx + (int)(13 * zoom) : sx - (int)(5 * zoom);
        var swordCol = theme.HasLightsaber && theme.SaberColor.HasValue
            ? theme.SaberColor.Value
            : new Color(200, 200, 210, 255);
        var hiltCol = new Color(130, 65, 15, 255);

        switch (Stance)
        {
            case Stance.Stone:
                Raylib.DrawLine(bx, sy + (int)(12 * zoom), bx, sy + (int)(8 * zoom), hiltCol);
                Raylib.DrawLine(bx, sy + (int)(8 * zoom), bx + (int)(5 * Direction * zoom), sy - (int)(3 * zoom), swordCol);
                Raylib.DrawLine(bx, sy + (int)(8 * zoom), bx + (int)(5 * Direction * zoom), sy - (int)(3 * zoom), new Color(255, 255, 255, 60));
                break;
            case Stance.Water:
                Raylib.DrawLine(bx, sy + (int)(14 * zoom), bx + (int)(3 * Direction * zoom), sy + (int)(14 * zoom), hiltCol);
                Raylib.DrawLine(bx + (int)(3 * Direction * zoom), sy + (int)(14 * zoom), bx + (int)(13 * Direction * zoom), sy + (int)(12 * zoom), swordCol);
                break;
            case Stance.Wind:
                Raylib.DrawLine(bx, sy + (int)(10 * zoom), bx + (int)(2 * Direction * zoom), sy + (int)(9 * zoom), hiltCol);
                Raylib.DrawLine(bx + (int)(2 * Direction * zoom), sy + (int)(9 * zoom), bx + (int)(15 * Direction * zoom), sy + (int)(3 * zoom), swordCol);
                break;
        }
    }

    private void DrawSwingArc(int sx, int sy, float zoom)
    {
        var col = Toolbar[ActiveSlot] switch
        {
            "PICKAXE" => new Color(200, 200, 225, 160),
            "BLOCK"   => new Color(140, 100, 75, 140),
            _         => new Color(255, 255, 255, 180)
        };
        int arcSize = (int)(40 * zoom);
        int arcX = Direction == 1 ? sx + (int)(W * zoom) - (int)(4 * zoom) : sx - (int)(22 * zoom);
        Raylib.DrawRingLines(new Vector2(arcX, sy - (int)(6 * zoom)), arcSize * 0.35f, arcSize * 0.45f, -60, 60, 16, col);
    }

    private void DrawMiningCracks(float camX, float camY, float zoom)
    {
        if (!MineTarget.HasValue) return;
        var (tx, ty) = MineTarget.Value;
        int ts = (int)(Constants.TileSize * zoom);
        int mdx = (int)(tx * ts - camX);
        int mdy = (int)(ty * ts - camY);
        Raylib.DrawLine(mdx + (int)(2 * zoom), mdy + (int)(2 * zoom), mdx + ts - (int)(2 * zoom), mdy + ts - (int)(2 * zoom), new Color(255, 255, 255, 180));
        Raylib.DrawLine(mdx + ts - (int)(2 * zoom), mdy + (int)(2 * zoom), mdx + (int)(2 * zoom), mdy + ts - (int)(2 * zoom), new Color(255, 255, 255, 180));
        // Progress overlay
        float prog = MineTimer / (0.28f / Stats.MiningPower);
        Raylib.DrawRectangle(mdx, mdy + ts - 3, (int)(ts * prog), 3, new Color(255, 200, 50, 200));
    }
}
