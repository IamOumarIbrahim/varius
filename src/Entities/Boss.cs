// src/Entities/Boss.cs
// Mini-boss arenas: GiantSlime, ShadowWraith, MagmaGolem
using Raylib_cs;
using System.Numerics;
using Varius.Core;

namespace Varius.Entities;

public enum BossType { GiantSlime, ShadowWraith, MagmaGolem }

public class Boss
{
    public float X { get; set; }
    public float Y { get; set; }
    public float VX { get; set; }
    public float VY { get; set; }
    public int Health { get; set; }
    public int MaxHealth { get; set; }
    public float Posture { get; set; }
    public float MaxPosture { get; set; } = 200f;
    public BossType Type { get; set; }
    public bool Dead => Health <= 0;
    public float FlashTimer { get; set; }
    public bool Enraged { get; private set; }

    // Arena
    public int ArenaTx { get; set; }
    public int ArenaTy { get; set; }

    // AI state
    private float _phaseTimer;
    private float _attackTimer;
    private float _jumpTimer;
    private int _phase = 1;
    private bool _onGround;
    private readonly Random _rng = new();

    public const int W = 36;
    public const int H = 36;

    public static Boss Spawn(BossType type, float x, float y)
    {
        return new Boss
        {
            X = x, Y = y, Type = type,
            Health = type switch
            {
                BossType.GiantSlime   => 450,
                BossType.ShadowWraith => 360,
                BossType.MagmaGolem   => 550,
                _ => 400
            },
            MaxHealth = type switch
            {
                BossType.GiantSlime   => 450,
                BossType.ShadowWraith => 360,
                BossType.MagmaGolem   => 550,
                _ => 400
            }
        };
    }

    public List<Combat.Projectile> Update(float dt, float playerX, float playerY, World.GameWorld world)
    {
        var projs = new List<Combat.Projectile>();
        if (Dead) return projs;

        if (FlashTimer > 0) FlashTimer -= dt;
        Posture = Math.Min(Posture + 10f * dt, MaxPosture);
        _phaseTimer += dt;
        _attackTimer += dt;

        // Enrage at 30%
        if (!Enraged && Health < MaxHealth * 0.3f)
        {
            Enraged = true;
        }

        float speedMult = Enraged ? 1.6f : 1.0f;
        float dx = playerX - (X + W / 2f);
        float dy = playerY - (Y + H / 2f);
        float dist = MathF.Sqrt(dx * dx + dy * dy);

        switch (Type)
        {
            case BossType.GiantSlime:
                UpdateGiantSlime(dt, dx, dy, dist, speedMult, projs);
                break;
            case BossType.ShadowWraith:
                UpdateShadowWraith(dt, dx, dy, dist, speedMult, projs);
                break;
            case BossType.MagmaGolem:
                UpdateMagmaGolem(dt, dx, dy, dist, speedMult, projs);
                break;
        }

        // Ground physics (not for wraith)
        if (Type != BossType.ShadowWraith)
        {
            VY += Constants.Gravity * 0.7f * dt;
            if (VY > Constants.MaxFallSpeed) VY = Constants.MaxFallSpeed;
            X += VX * dt;
            var hcols = world.CheckTileCollision(new Rectangle(X, Y, W, H));
            foreach (var c in hcols)
            {
                if (VX > 0) { X = c.X - W; VX = 0; }
                else if (VX < 0) { X = c.X + c.Width; VX = 0; }
            }
            Y += VY * dt;
            var vcols = world.CheckTileCollision(new Rectangle(X, Y, W, H));
            _onGround = false;
            foreach (var c in vcols)
            {
                if (VY > 0) { Y = c.Y - H; VY = 0; _onGround = true; }
                else if (VY < 0) { Y = c.Y + c.Height; VY = 0; }
            }
        }

        return projs;
    }

    private void UpdateGiantSlime(float dt, float dx, float dy, float dist, float speedMult,
        List<Combat.Projectile> projs)
    {
        // Hop toward player
        _jumpTimer += dt;
        if (_onGround && _jumpTimer >= (Enraged ? 0.9f : 1.8f))
        {
            _jumpTimer = 0;
            float hopDir = dx > 0 ? 1f : -1f;
            VX = hopDir * (95f + 25f * speedMult);
            VY = Constants.JumpForce * 0.65f;
        }

        // Every 4s: slam attack — spit 4 projectiles in cross
        if (_attackTimer >= (Enraged ? 2.5f : 4.5f) && dist < 180)
        {
            _attackTimer = 0;
            for (int i = 0; i < (Enraged ? 6 : 4); i++)
            {
                float ang = i * MathF.PI * 2f / (Enraged ? 6f : 4f);
                projs.Add(new Combat.Projectile
                {
                    X = X + W / 2f, Y = Y + H / 2f,
                    VX = MathF.Cos(ang) * 90f,
                    VY = MathF.Sin(ang) * 90f,
                    Damage = 12, IsEnemy = true,
                    Col = new Color((byte)60, (byte)210, (byte)100, (byte)255)
                });
            }
        }
    }

    private void UpdateShadowWraith(float dt, float dx, float dy, float dist, float speedMult,
        List<Combat.Projectile> projs)
    {
        // Ethereal float — no gravity, drift toward player
        float spd = (55f + 20f * speedMult) * dt;
        if (dist > 0)
        {
            X += (dx / dist) * spd;
            Y += (dy / dist) * spd;
        }

        // Phase teleport every 6s
        _phaseTimer += dt;
        if (_phaseTimer >= (Enraged ? 3.5f : 6.5f))
        {
            _phaseTimer = 0;
            // Teleport slightly around player
            X = dx > 0 ? X - _rng.NextSingle() * 60f - 30f : X + _rng.NextSingle() * 60f + 30f;
            Y = Y + (_rng.NextSingle() - 0.5f) * 40f;
        }

        // Dark bolt volley
        if (_attackTimer >= (Enraged ? 1.8f : 3.2f) && dist < 220)
        {
            _attackTimer = 0;
            int count = Enraged ? 5 : 3;
            for (int i = 0; i < count; i++)
            {
                float spread = (i - count / 2f) * 0.2f;
                float baseAng = dist > 0 ? MathF.Atan2(dy, dx) : 0f;
                float ang = baseAng + spread;
                projs.Add(new Combat.Projectile
                {
                    X = X + W / 2f, Y = Y + H / 2f,
                    VX = MathF.Cos(ang) * 115f,
                    VY = MathF.Sin(ang) * 115f,
                    Damage = 10, IsEnemy = true,
                    Col = new Color((byte)120, (byte)40, (byte)200, (byte)255)
                });
            }
        }
    }

    private void UpdateMagmaGolem(float dt, float dx, float dy, float dist, float speedMult,
        List<Combat.Projectile> projs)
    {
        // Slow stomp toward player
        if (_onGround)
            VX = dx > 0 ? 60f * speedMult : -60f * speedMult;

        // Rock throw
        if (_attackTimer >= (Enraged ? 2.0f : 3.8f) && dist < 250)
        {
            _attackTimer = 0;
            float ang = dist > 0 ? MathF.Atan2(dy, dx) : 0f;
            // Lob arc
            projs.Add(new Combat.Projectile
            {
                X = X + W / 2f, Y = Y,
                VX = MathF.Cos(ang) * 130f,
                VY = -110f,
                Damage = 18, IsEnemy = true,
                Col = new Color((byte)220, (byte)80, (byte)20, (byte)255)
            });

            if (Enraged)
            {
                // Also spit ember spread
                for (int i = -2; i <= 2; i++)
                {
                    projs.Add(new Combat.Projectile
                    {
                        X = X + W / 2f, Y = Y + H / 2f,
                        VX = i * 40f,
                        VY = -80f,
                        Damage = 9, IsEnemy = true,
                        Col = new Color((byte)255, (byte)120, (byte)20, (byte)255)
                    });
                }
            }
        }
    }

    public Rectangle GetRect() => new(X, Y, W, H);

    public void Draw(float camX, float camY, float zoom)
    {
        if (Dead) return;
        float sx = X * zoom - camX;
        float sy = Y * zoom - camY;
        int sw = (int)(W * zoom);
        int sh = (int)(H * zoom);

        switch (Type)
        {
            case BossType.GiantSlime:   DrawGiantSlime((int)sx, (int)sy, sw, sh); break;
            case BossType.ShadowWraith: DrawShadowWraith((int)sx, (int)sy, sw, sh); break;
            case BossType.MagmaGolem:   DrawMagmaGolem((int)sx, (int)sy, sw, sh); break;
        }

        // Health bar (wide, above boss)
        float hpPct = (float)Health / MaxHealth;
        int barW = sw + (int)(24 * zoom);
        int barX = (int)sx - (int)(12 * zoom);
        int barY = (int)sy - (int)(12 * zoom);
        Raylib.DrawRectangle(barX, barY, barW, (int)(6 * zoom), new Color((byte)40, (byte)5, (byte)5, (byte)220));
        Raylib.DrawRectangle(barX, barY, (int)(barW * hpPct), (int)(6 * zoom),
            Enraged ? new Color((byte)255, (byte)40, (byte)40, (byte)255) : new Color((byte)200, (byte)60, (byte)60, (byte)255));
        Raylib.DrawRectangleLines(barX, barY, barW, (int)(6 * zoom), new Color((byte)255, (byte)255, (byte)255, (byte)100));

        // Boss name tag
        string bossName = Type switch
        {
            BossType.GiantSlime   => Enraged ? "!ENRAGED SLIME KING!" : "Slime King",
            BossType.ShadowWraith => Enraged ? "!ENRAGED SHADOW WRAITH!" : "Shadow Wraith",
            BossType.MagmaGolem   => Enraged ? "!ENRAGED MAGMA GOLEM!" : "Magma Golem",
            _ => "Boss"
        };
        var nameCol = Enraged ? new Color((byte)255, (byte)60, (byte)60, (byte)255) : new Color((byte)255, (byte)215, (byte)60, (byte)255);
        int nameW = Raylib.MeasureText(bossName, 10);
        Raylib.DrawText(bossName, (int)sx + sw / 2 - nameW / 2, barY - 14, 10, nameCol);
    }

    private void DrawGiantSlime(int sx, int sy, int sw, int sh)
    {
        float t = (float)Raylib.GetTime();
        bool flash = FlashTimer > 0;
        var body = flash ? new Color((byte)255, (byte)100, (byte)100, (byte)255)
                        : (Enraged ? new Color((byte)255, (byte)60, (byte)80, (byte)255) : new Color((byte)50, (byte)210, (byte)110, (byte)255));
        var outline = Enraged ? new Color((byte)200, (byte)30, (byte)50, (byte)255) : new Color((byte)30, (byte)150, (byte)70, (byte)255);

        float squish = MathF.Sin(t * 6f) * 2f * (float)zoom; // bounce
        float z = _onGround ? 1f : (float)sw;

        Raylib.DrawEllipse(sx + sw / 2, (int)(sy + sh * 3 / 4), sw * 0.52f, sh * 0.35f, outline);
        Raylib.DrawEllipse(sx + sw / 2, (int)(sy + sh * 3 / 4), sw * 0.44f, sh * 0.29f, body);
        Raylib.DrawEllipse(sx + sw / 2, (int)(sy + sh * 0.42f), sw * 0.4f + (int)squish, sh * 0.4f - (int)squish, outline);
        Raylib.DrawEllipse(sx + sw / 2, (int)(sy + sh * 0.42f), sw * 0.33f + (int)squish, sh * 0.33f - (int)squish, body);

        // Big eyes
        Raylib.DrawCircle(sx + sw / 2 - sw / 5, sy + sh / 3, sw / 9, new Color((byte)255, (byte)255, (byte)255, (byte)255));
        Raylib.DrawCircle(sx + sw / 2 + sw / 5, sy + sh / 3, sw / 9, new Color((byte)255, (byte)255, (byte)255, (byte)255));
        var pupilCol = Enraged ? new Color((byte)255, (byte)30, (byte)30, (byte)255) : new Color((byte)0, (byte)0, (byte)0, (byte)255);
        Raylib.DrawCircle(sx + sw / 2 - sw / 5 + 1, sy + sh / 3 + 1, sw / 16, pupilCol);
        Raylib.DrawCircle(sx + sw / 2 + sw / 5 + 1, sy + sh / 3 + 1, sw / 16, pupilCol);
        // Crown detail for boss
        for (int i = 0; i < 5; i++)
        {
            float ang = -60f + i * 30f;
            float rad = ang * MathF.PI / 180f;
            int cx = sx + sw / 2 + (int)(MathF.Cos(rad) * sw * 0.36f);
            int cy = sy + (int)(sh * 0.1f) + (int)(MathF.Sin(rad) * sh * 0.1f);
            Raylib.DrawCircle(cx, cy, sw / 14, new Color((byte)255, (byte)215, (byte)0, (byte)220));
        }
    }

    private float zoom => 1.5f; // approximation for draw helpers

    private void DrawShadowWraith(int sx, int sy, int sw, int sh)
    {
        float t = (float)Raylib.GetTime();
        bool flash = FlashTimer > 0;
        var shroud = flash ? new Color((byte)255, (byte)100, (byte)100, (byte)200)
                          : (Enraged ? new Color((byte)180, (byte)30, (byte)255, (byte)200)
                                     : new Color((byte)60, (byte)20, (byte)100, (byte)200));
        // Swirling dark robe — animated circles
        for (int ring = 0; ring < 4; ring++)
        {
            float rOff = ring * 0.06f;
            float ang = t * (2.2f + ring * 0.5f) + rOff;
            int rx = sx + sw / 2 + (int)(MathF.Cos(ang) * sw * 0.18f * ring);
            int ry = sy + sh / 2 + (int)(MathF.Sin(ang * 0.7f) * sh * 0.12f * ring);
            float radius = sw * (0.42f - ring * 0.06f);
            Raylib.DrawCircle(rx, ry, radius, new Color(shroud.R, shroud.G, shroud.B, (byte)(shroud.A - ring * 30)));
        }
        // Glowing eyes
        float eyeGlow = 0.7f + 0.3f * MathF.Sin(t * 4f);
        var eyeCol = Enraged
            ? new Color((byte)255, (byte)(int)(eyeGlow * 60), (byte)(int)(eyeGlow * 30), (byte)255)
            : new Color((byte)(int)(eyeGlow * 160), (byte)(int)(eyeGlow * 40), (byte)255, (byte)255);
        Raylib.DrawCircle(sx + sw / 3, sy + sh / 3, sw / 10, eyeCol);
        Raylib.DrawCircle(sx + sw * 2 / 3, sy + sh / 3, sw / 10, eyeCol);
        // Scythe suggestion
        Raylib.DrawLine(sx + sw * 3 / 4, sy + sh / 4, sx + sw + sw / 4, sy - sh / 4, new Color((byte)80, (byte)20, (byte)140, (byte)200));
        Raylib.DrawLine(sx + sw + sw / 4, sy - sh / 4, sx + sw + sw / 4 - sw / 3, sy - sh / 4 + sh / 3, new Color((byte)100, (byte)40, (byte)180, (byte)200));
    }

    private void DrawMagmaGolem(int sx, int sy, int sw, int sh)
    {
        float t = (float)Raylib.GetTime();
        bool flash = FlashTimer > 0;
        var body = flash ? new Color((byte)255, (byte)100, (byte)100, (byte)255)
                        : new Color((byte)80, (byte)60, (byte)55, (byte)255);
        var lava = Enraged
            ? new Color((byte)255, (byte)(int)(80 + 60 * MathF.Sin(t * 8)), (byte)20, (byte)255)
            : new Color((byte)255, (byte)(int)(60 + 40 * MathF.Sin(t * 5)), (byte)20, (byte)220);

        // Stone body
        Raylib.DrawRectangle(sx + sw / 6, sy + sh / 4, sw * 2 / 3, sh * 3 / 4, body);
        Raylib.DrawRectangle(sx + sw / 4, sy, sw / 2, sh / 2, body);
        // Lava cracks
        Raylib.DrawRectangle(sx + sw / 4, sy + sh / 3, sw / 12, sh / 3, lava);
        Raylib.DrawRectangle(sx + sw / 2, sy + sh / 4, sw / 10, sh / 2, lava);
        Raylib.DrawRectangle(sx + sw * 2 / 3, sy + sh * 2 / 5, sw / 10, sh / 4, lava);
        // Eyes — lava glow
        Raylib.DrawCircle(sx + sw / 3, sy + sh / 4, sw / 8, lava);
        Raylib.DrawCircle(sx + sw * 2 / 3, sy + sh / 4, sw / 8, lava);
        // Fists
        Raylib.DrawRectangle(sx - sw / 5, sy + sh / 3, sw / 5, sh / 4, body);
        Raylib.DrawRectangle(sx + sw, sy + sh / 3, sw / 5, sh / 4, body);
        // Knuckle lava
        Raylib.DrawRectangle(sx - sw / 5, sy + sh / 3, sw / 10, sh / 8, lava);
        Raylib.DrawRectangle(sx + sw + sw / 10, sy + sh / 3, sw / 10, sh / 8, lava);
    }
}

/// Boss arena: a room carved into the cave with a floor, walls, and a locked chest
public class BossArena
{
    public int Tx { get; set; }
    public int Ty { get; set; }
    public int W { get; set; } = 14;
    public int H { get; set; } = 8;
    public BossType BossType { get; set; }
    public Boss? BossRef { get; set; }
    public bool Cleared { get; set; }
    public bool ChestSpawned { get; set; }

    public static BossArena CarveInto(World.GameWorld world, int tx, int ty, BossType btype)
    {
        int w = 14, h = 8;
        // Carve air interior
        for (int x = tx + 1; x < tx + w - 1; x++)
        for (int y = ty + 1; y < ty + h - 1; y++)
            world.SetTile(x, y, Constants.TileAir);

        // Place stone floor
        for (int x = tx; x < tx + w; x++)
            world.SetTile(x, ty + h - 1, Constants.TileBossArenaFloor);

        // Place pillar decorations
        world.SetTile(tx + 2, ty + h - 2, Constants.TileAncientBrick);
        world.SetTile(tx + w - 3, ty + h - 2, Constants.TileAncientBrick);

        // Place chest on the far right of the arena
        world.SetTile(tx + w - 2, ty + h - 2, Constants.TileBossChest);

        // Spawn boss in center
        float bx = (tx + w / 2) * Constants.TileSize - Boss.W / 2f;
        float by = (ty + h - 2) * Constants.TileSize - Boss.H;
        var boss = Boss.Spawn(btype, bx, by);
        boss.ArenaTx = tx;
        boss.ArenaTy = ty;

        return new BossArena
        {
            Tx = tx, Ty = ty, W = w, H = h,
            BossType = btype, BossRef = boss
        };
    }
}

/// Manages all active bosses and arenas
public class BossManager
{
    public List<BossArena> Arenas { get; } = new();
    private readonly Random _rng = new();
    private float _spawnTimer = 45f; // first arena after 45s

    public void GenerateArenas(World.GameWorld world)
    {
        BossType[] types = { BossType.ShadowWraith, BossType.GiantSlime, BossType.MagmaGolem };
        int[] depths = { Constants.BiomeIceStart + 4, Constants.BiomeMagmaStart + 4, Constants.BiomeRuinsStart + 4 };

        for (int i = 0; i < 3; i++)
        {
            // Find a good spot at the target depth
            int targetY = depths[i];
            for (int tries = 0; tries < 50; tries++)
            {
                int tx = _rng.Next(20, world.Width - 34);
                bool valid = true;
                // Make sure there's enough space
                for (int x = tx; x < tx + 16 && valid; x++)
                for (int y = targetY; y < targetY + 10 && valid; y++)
                    if (world.GetTile(x, y) == Constants.TileBedrock) valid = false;

                if (valid)
                {
                    var arena = BossArena.CarveInto(world, tx, targetY, types[i]);
                    Arenas.Add(arena);
                    break;
                }
            }
        }
    }

    public List<Combat.Projectile> Update(float dt, Player player, World.GameWorld world,
        Combat.FXManager fx)
    {
        var projs = new List<Combat.Projectile>();
        foreach (var arena in Arenas)
        {
            if (arena.Cleared || arena.BossRef == null) continue;
            var boss = arena.BossRef;
            var newProjs = boss.Update(dt, player.X + Player.W / 2f, player.Y + Player.H / 2f, world);
            projs.AddRange(newProjs);

            // Boss-player melee
            var br = boss.GetRect();
            var pr = player.GetRect();
            if (Raylib.CheckCollisionRecs(br, pr))
                player.TakeDamage(Math.Max(1, 15 - player.Stats.Armor));

            // Boss death
            if (boss.Dead)
            {
                arena.Cleared = true;
                player.AddXP(250);
                // Spawn Boss Chest tile in the world
                int btx = (int)((boss.X + Boss.W / 2f) / Constants.TileSize);
                int bty = (int)((boss.Y + Boss.H / 2f) / Constants.TileSize);
                world.SetTile(btx, bty, Constants.TileBossChest);
                fx.Shake.Trigger(10f, 0.4f);
            }
        }
        return projs;
    }

    public void TryDamage(Boss boss, int damage, Player player, Combat.FXManager fx)
    {
        if (boss.Dead) return;
        bool crit = (float)new Random().NextDouble() < player.Stats.CritRate;
        int dmg = (int)(damage * (crit ? player.Stats.CritDmg : 1f));
        boss.Health -= dmg;
        boss.FlashTimer = 0.18f;
        fx.SpawnHitImpact(boss.X + Boss.W / 2f, boss.Y + Boss.H / 2f, player.Stance, crit);
    }

    public void Draw(float camX, float camY, float zoom)
    {
        foreach (var arena in Arenas)
            arena.BossRef?.Draw(camX, camY, zoom);
    }
}
