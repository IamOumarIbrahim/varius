// src/Entities/Mob.cs
using Raylib_cs;
using System.Numerics;
using Varius.Core;

namespace Varius.Entities;

public enum MobType { Slime, Crawler, Bomber, Bat, Skeleton, Eyeball }

public class Mob
{
    public float X { get; set; }
    public float Y { get; set; }
    public float VX { get; set; }
    public float VY { get; set; }
    public int Health { get; set; }
    public int MaxHealth { get; set; }
    public float Posture { get; set; } = 60;
    public float MaxPosture { get; set; } = 60;
    public MobType Type { get; set; }
    public bool Dead => Health <= 0;
    public float FlashTimer { get; set; }
    private bool _onGround;
    private float _aiTimer;
    private float _spitTimer;
    private float _statusSecTimer;
    public const int W = 12;
    public const int H = 12;
    private float _slowTimer;
    private float _danceTimer;
    public float BurnTimer { get; set; }
    public float BleedTimer { get; set; }
    public float FreezeTimer { get; set; }

    public void ApplyBurn(float duration) => BurnTimer = Math.Max(BurnTimer, duration);
    public void ApplyBleed(float duration) => BleedTimer = Math.Max(BleedTimer, duration);
    public void ApplyFreeze(float duration) => FreezeTimer = Math.Max(FreezeTimer, duration);

    private static readonly Random _rng = new();

    public static Mob Spawn(float worldPxX, float worldPxY)
    {
        var type = (MobType)_rng.Next(6);
        return new Mob
        {
            X = worldPxX,
            Y = worldPxY,
            Type = type,
            Health = type switch
            {
                MobType.Skeleton => 55,
                MobType.Bomber   => 35,
                MobType.Eyeball  => 45,
                MobType.Bat      => 28,
                MobType.Crawler  => 40,
                _                => 30
            },
            MaxHealth = type switch
            {
                MobType.Skeleton => 55,
                MobType.Bomber   => 35,
                MobType.Eyeball  => 45,
                MobType.Bat      => 28,
                MobType.Crawler  => 40,
                _                => 30
            }
        };
    }

    public Rectangle GetRect() => new(X, Y, W, H);

    public void ApplySlow(float duration) => _slowTimer = duration;
    public void ApplyDance(float duration) => _danceTimer = duration;

    public List<Combat.Projectile> Update(float dt, float playerX, float playerY, World.GameWorld world)
    {
        var result = new List<Combat.Projectile>();
        if (Dead) return result;
        if (FlashTimer > 0) FlashTimer -= dt;
        if (_danceTimer > 0) { _danceTimer -= dt; }
        if (_slowTimer > 0) _slowTimer -= dt;
        if (BurnTimer > 0) BurnTimer -= dt;
        if (BleedTimer > 0) BleedTimer -= dt;
        if (FreezeTimer > 0) FreezeTimer -= dt;

        _statusSecTimer += dt;
        if (_statusSecTimer >= 0.25f)
        {
            _statusSecTimer -= 0.25f;
            if (BurnTimer > 0) Health -= 2;
            if (BleedTimer > 0) Health -= 3;
            if (_danceTimer > 0) Health -= 1;
        }

        if (_danceTimer > 0) return result; // Dancing mobs are stunned

        float speedMult = FreezeTimer > 0 ? 0.15f : (_slowTimer > 0 ? 0.35f : 1f);
        float baseSpeed = Type switch { MobType.Bat => 75f, MobType.Bomber => 55f, _ => 65f };
        float spd = baseSpeed * speedMult;

        _aiTimer += dt;

        float dx = playerX - X;
        float dy = playerY - Y;
        float dist = MathF.Sqrt(dx * dx + dy * dy);

        switch (Type)
        {
            case MobType.Bat:
                // Bats fly directly
                if (dist > 0)
                {
                    VX = (dx / dist) * spd;
                    VY = (dy / dist) * spd;
                }
                X += VX * dt;
                Y += VY * dt;
                return result;

            case MobType.Eyeball:
                // Eyeballs hover and spit
                if (dist > 0)
                {
                    VX += (dx / dist) * 80f * dt;
                    VY += (dy / dist) * 80f * dt;
                }
                float maxVel = 90f;
                if (VX > maxVel) VX = maxVel; if (VX < -maxVel) VX = -maxVel;
                if (VY > maxVel) VY = maxVel; if (VY < -maxVel) VY = -maxVel;
                X += VX * dt; Y += VY * dt;
                if (FreezeTimer <= 0)
                {
                    _spitTimer += dt;
                    if (_spitTimer >= 3.0f && dist < 180)
                    {
                        _spitTimer = 0;
                        float spd2 = 120f;
                        result.Add(new Combat.Projectile
                        {
                            X = X + W / 2f, Y = Y + H / 2f,
                            VX = dist > 0 ? (dx / dist) * spd2 : 0,
                            VY = dist > 0 ? (dy / dist) * spd2 : 0,
                            Damage = 8, IsEnemy = true, Col = new Color(140, 60, 220, 255)
                        });
                    }
                }
                return result;

            case MobType.Bomber:
                // Rush when close
                if (dist < 80)
                {
                    if (dist > 0) { VX = (dx / dist) * spd * 1.8f; VY = (dy / dist) * spd * 1.8f; }
                    X += VX * dt; Y += VY * dt;
                    Health -= 1; // Self-destruct counter
                }
                else goto default;
                return result;

            default:
                // Ground movement
                if (_aiTimer >= 0.6f)
                {
                    _aiTimer = 0;
                    VX = dx > 0 ? spd : -spd;
                }
                VY += Constants.Gravity * 0.6f * dt;
                if (VY > Constants.MaxFallSpeed * 0.6f) VY = Constants.MaxFallSpeed * 0.6f;
                if (_onGround && dy < -20) VY = Constants.JumpForce * 0.5f;

                X += VX * dt;
                var hcols = world.CheckTileCollision(GetRect());
                foreach (var c in hcols)
                {
                    if (VX > 0) { X = c.X - W; VX = 0; }
                    else if (VX < 0) { X = c.X + c.Width; VX = 0; }
                }

                Y += VY * dt;
                var vcols = world.CheckTileCollision(GetRect());
                _onGround = false;
                foreach (var c in vcols)
                {
                    if (VY > 0) { Y = c.Y - H; VY = 0; _onGround = true; }
                    else if (VY < 0) { Y = c.Y + c.Height; VY = 0; }
                }
                break;
        }
        return result;
    }

    public void Draw(float camX, float camY, float zoom)
    {
        if (Dead) return;
        float sx = X * zoom - camX;
        float sy = Y * zoom - camY;
        int sw = (int)(W * zoom);
        int sh = (int)(H * zoom);

        bool flash = FlashTimer > 0 || _danceTimer > 0;

        switch (Type)
        {
            case MobType.Slime:
                DrawSlime((int)sx, (int)sy, sw, sh, flash);
                break;
            case MobType.Crawler:
                DrawCrawler((int)sx, (int)sy, sw, sh, flash);
                break;
            case MobType.Bomber:
                DrawBomber((int)sx, (int)sy, sw, sh, flash);
                break;
            case MobType.Bat:
                DrawBat((int)sx, (int)sy, sw, sh, flash);
                break;
            case MobType.Skeleton:
                DrawSkeleton((int)sx, (int)sy, sw, sh, flash);
                break;
            case MobType.Eyeball:
                DrawEyeball((int)sx, (int)sy, sw, sh, flash);
                break;
        }

        // Status effect overlays
        if (FreezeTimer > 0)
        {
            Raylib.DrawRectangle((int)sx, (int)sy, sw, sh, new Color(80, 160, 255, 120));
        }
        else if (BurnTimer > 0)
        {
            Raylib.DrawRectangle((int)sx, (int)sy, sw, sh, new Color(255, 120, 30, 100));
        }
        else if (BleedTimer > 0)
        {
            Raylib.DrawRectangle((int)sx, (int)sy, sw, sh, new Color(200, 20, 20, 100));
        }

        // Health bar
        float hpPct = (float)Health / MaxHealth;
        Raylib.DrawRectangle((int)sx, (int)sy - (int)(5 * zoom), sw, (int)(3 * zoom), new Color(60, 0, 0, 200));
        Raylib.DrawRectangle((int)sx, (int)sy - (int)(5 * zoom), (int)(sw * hpPct), (int)(3 * zoom),
            hpPct > 0.5f ? new Color(50, 200, 50, 220) : new Color(220, 80, 30, 220));

        // Dance effect
        if (_danceTimer > 0)
        {
            float t = (float)Raylib.GetTime();
            for (int i = 0; i < 4; i++)
            {
                float ang = t * 4f + i * MathF.PI / 2f;
                int nx = (int)sx + sw / 2 + (int)(MathF.Cos(ang) * 8 * zoom);
                int ny = (int)sy + sh / 2 + (int)(MathF.Sin(ang) * 8 * zoom);
                Raylib.DrawCircle(nx, ny, (int)(2 * zoom), new Color(255, 100, 200, 200));
            }
        }
    }

    private static void DrawSlime(int sx, int sy, int sw, int sh, bool flash)
    {
        var body = flash ? new Color(255, 100, 100, 255) : new Color(50, 200, 100, 255);
        var outline = new Color(30, 140, 70, 255);
        var eye = new Color(255, 255, 255, 255);
        var pupil = new Color(0, 0, 0, 255);

        // Blob body (ellipse-ish)
        Raylib.DrawEllipse(sx + sw / 2, sy + sh * 3 / 4, sw * 0.5f, sh * 0.38f, outline);
        Raylib.DrawEllipse(sx + sw / 2, sy + sh * 3 / 4, sw * 0.44f, sh * 0.32f, body);
        // Head
        Raylib.DrawEllipse(sx + sw / 2, (int)(sy + sh * 0.45f), sw * 0.38f, sh * 0.38f, outline);
        Raylib.DrawEllipse(sx + sw / 2, (int)(sy + sh * 0.45f), sw * 0.32f, sh * 0.32f, body);
        // Eyes
        Raylib.DrawCircle(sx + sw / 2 - sw / 5, sy + sh / 4, sw * 0.09f, eye);
        Raylib.DrawCircle(sx + sw / 2 + sw / 5, sy + sh / 4, sw * 0.09f, eye);
        Raylib.DrawCircle(sx + sw / 2 - sw / 5 + 1, sy + sh / 4 + 1, sw * 0.055f, pupil);
        Raylib.DrawCircle(sx + sw / 2 + sw / 5 + 1, sy + sh / 4 + 1, sw * 0.055f, pupil);
        // Shine
        Raylib.DrawCircle(sx + sw / 2 - sw / 6, sy + (int)(sh * 0.3f), (int)(sw * 0.06f), new Color(255, 255, 255, 120));
    }

    private static void DrawCrawler(int sx, int sy, int sw, int sh, bool flash)
    {
        var body = flash ? new Color(255, 100, 100, 255) : new Color(180, 80, 20, 255);
        Raylib.DrawRectangle(sx, sy + sh / 3, sw, sh * 2 / 3, body);
        // Shell sheen
        Raylib.DrawRectangle(sx, sy + sh / 3, sw, sh / 6, new Color(220, 110, 40, 200));
        // Legs
        for (int i = 0; i < 3; i++)
        {
            int lx = sx + i * sw / 3;
            Raylib.DrawLine(lx + sw / 6, sy + sh * 2 / 3, lx, sy + sh, new Color(150, 60, 10, 255));
            Raylib.DrawLine(lx + sw * 2 / 3, sy + sh * 2 / 3, lx + sw, sy + sh, new Color(150, 60, 10, 255));
        }
        // Eyes
        Raylib.DrawCircle(sx + sw / 3, sy + sh / 3 + sh / 6, sw / 8, new Color(255, 50, 50, 255));
        Raylib.DrawCircle(sx + sw * 2 / 3, sy + sh / 3 + sh / 6, sw / 8, new Color(255, 50, 50, 255));
    }

    private static void DrawBomber(int sx, int sy, int sw, int sh, bool flash)
    {
        float t = (float)Raylib.GetTime();
        int pulse = flash ? 2 : (int)(MathF.Abs(MathF.Sin(t * 5)) * 3);
        var body = flash ? new Color(255, 100, 100, 255) : new Color(200, 60, 20, 255);
        // Body
        Raylib.DrawRectangle(sx - pulse, sy - pulse, sw + pulse * 2, sh + pulse * 2, body);
        // Stripes
        Raylib.DrawRectangle(sx, sy + sh / 4, sw, sh / 8, new Color(255, 220, 0, 200));
        Raylib.DrawRectangle(sx, sy + sh / 2, sw, sh / 8, new Color(255, 220, 0, 200));
        // Skull face
        Raylib.DrawCircle(sx + sw / 3, sy + sh / 3, sw / 6, new Color(255, 255, 255, 230));
        Raylib.DrawCircle(sx + sw * 2 / 3, sy + sh / 3, sw / 6, new Color(255, 255, 255, 230));
        Raylib.DrawRectangle(sx + sw / 4, sy + sh * 2 / 3, sw / 2, sh / 6, new Color(255, 255, 255, 200));
        // Fuse
        Raylib.DrawLine(sx + sw / 2, sy, sx + sw / 2, sy - sh / 2, new Color(140, 110, 60, 255));
        if (pulse > 1) Raylib.DrawCircle(sx + sw / 2, sy - sh / 2, sw / 8, new Color(255, 200, 50, 220));
    }

    private static void DrawBat(int sx, int sy, int sw, int sh, bool flash)
    {
        float t = (float)Raylib.GetTime();
        float wingFlap = MathF.Sin(t * 12f) * sh / 3f;
        var body = flash ? new Color(255, 100, 100, 255) : new Color(90, 40, 120, 255);
        var wing = flash ? new Color(255, 100, 100, 200) : new Color(70, 30, 100, 200);

        // Wings
        Raylib.DrawTriangle(
            new Vector2(sx + sw / 2, sy + sh / 2),
            new Vector2(sx - sw / 2, sy + (int)wingFlap),
            new Vector2(sx, sy + sh / 2 + sh / 4), wing);
        Raylib.DrawTriangle(
            new Vector2(sx + sw / 2, sy + sh / 2),
            new Vector2(sx + sw * 3 / 2, sy + (int)wingFlap),
            new Vector2(sx + sw, sy + sh / 2 + sh / 4), wing);
        // Body
        Raylib.DrawEllipse(sx + sw / 2, sy + sh / 2, sw * 0.3f, sh * 0.35f, body);
        // Eyes
        Raylib.DrawCircle(sx + sw / 3, sy + sh / 3, sw / 7, new Color(255, 50, 50, 255));
        Raylib.DrawCircle(sx + sw * 2 / 3, sy + sh / 3, sw / 7, new Color(255, 50, 50, 255));
        // Fangs
        Raylib.DrawLine(sx + sw / 3, sy + sh * 2 / 3, sx + sw / 3 + 1, sy + sh * 2 / 3 + sh / 6, new Color(255, 255, 255, 220));
        Raylib.DrawLine(sx + sw * 2 / 3, sy + sh * 2 / 3, sx + sw * 2 / 3 + 1, sy + sh * 2 / 3 + sh / 6, new Color(255, 255, 255, 220));
    }

    private static void DrawSkeleton(int sx, int sy, int sw, int sh, bool flash)
    {
        var bone = flash ? new Color(255, 100, 100, 255) : new Color(235, 225, 200, 255);
        var dark = new Color(60, 55, 50, 255);
        // Skull
        Raylib.DrawRectangle(sx + sw / 4, sy, sw / 2, sh / 3, bone);
        // Eye sockets
        Raylib.DrawRectangle(sx + sw / 4 + sw / 12, sy + sh / 12, sw / 7, sh / 9, dark);
        Raylib.DrawRectangle(sx + sw / 2 + sw / 12, sy + sh / 12, sw / 7, sh / 9, dark);
        // Jaw
        Raylib.DrawRectangle(sx + sw / 4 + sw / 8, sy + sh / 3 - sh / 12, sw / 4, sh / 10, bone);
        // Ribcage
        for (int rib = 0; rib < 3; rib++)
        {
            int ry = sy + sh / 3 + rib * sh / 8;
            Raylib.DrawLine(sx + sw / 3, ry, sx + sw * 2 / 3, ry, bone);
        }
        // Arms
        Raylib.DrawLine(sx + sw / 4, sy + sh / 3, sx, sy + sh * 2 / 3, bone);
        Raylib.DrawLine(sx + sw * 3 / 4, sy + sh / 3, sx + sw, sy + sh * 2 / 3, bone);
        // Legs
        Raylib.DrawLine(sx + sw / 3, sy + sh * 2 / 3, sx + sw / 4, sy + sh, bone);
        Raylib.DrawLine(sx + sw * 2 / 3, sy + sh * 2 / 3, sx + sw * 3 / 4, sy + sh, bone);
    }

    private static void DrawEyeball(int sx, int sy, int sw, int sh, bool flash)
    {
        float t = (float)Raylib.GetTime();
        var sclera = flash ? new Color(255, 100, 100, 255) : new Color(245, 240, 235, 255);
        Raylib.DrawCircle(sx + sw / 2, sy + sh / 2, sw * 0.42f, new Color(180, 60, 60, 255));
        Raylib.DrawCircle(sx + sw / 2, sy + sh / 2, sw * 0.36f, sclera);
        // Iris
        var irisCol = new Color(60, 160, 255, 255);
        int pupilOff = (int)(MathF.Sin(t * 1.8f) * sw * 0.1f);
        Raylib.DrawCircle(sx + sw / 2 + pupilOff, sy + sh / 2, sw * 0.2f, irisCol);
        // Pupil
        Raylib.DrawCircle(sx + sw / 2 + pupilOff, sy + sh / 2, sw * 0.12f, new Color(5, 5, 8, 255));
        // Shine
        Raylib.DrawCircle(sx + sw / 2 + pupilOff - sw / 10, sy + sh / 2 - sh / 10, sw / 14, new Color(255, 255, 255, 200));
        // Veins
        Raylib.DrawLine(sx + sw / 5, sy + sh / 4, sx + sw * 2 / 5, sy + sh / 3, new Color(220, 60, 60, 140));
        Raylib.DrawLine(sx + sw * 4 / 5, sy + sh / 4, sx + sw * 3 / 5, sy + sh / 3, new Color(220, 60, 60, 140));
    }
}

// Mob manager
public class MobManager
{
    private readonly List<Mob> _mobs = new();
    private float _spawnTimer;
    private float _spawnInterval = 4.5f;
    private readonly Random _rng = new();
    private float _difficultyTimer;
    public List<Mob> Mobs => _mobs;

    public void Update(float dt, Player player, World.GameWorld world, Combat.CombatManager combat, List<ItemDrop> drops, float timeOfDay)
    {
        _spawnTimer += dt;
        _difficultyTimer += dt;
        // Increase difficulty
        if (_difficultyTimer >= 60f) { _difficultyTimer = 0; _spawnInterval = Math.Max(1.2f, _spawnInterval - 0.3f); }

        bool isNight = timeOfDay < 5f || timeOfDay > 19f;
        float currentInterval = (isNight && player.Y < Constants.BiomeIceStart * Constants.TileSize) ? _spawnInterval * 0.35f : _spawnInterval;

        if (_spawnTimer >= currentInterval && _mobs.Count < 40)
        {
            _spawnTimer = 0;
            SpawnNearPlayer(player, world);
        }

        foreach (var mob in _mobs)
        {
            var projs = mob.Update(dt, player.X + Player.W / 2f, player.Y + Player.H / 2f, world);
            foreach (var p in projs) combat.Projectiles.Add(p);
        }

        // Melee: mob touching player
        var pr = player.GetRect();
        foreach (var mob in _mobs)
        {
            if (mob.Dead) continue;
            var mr = mob.GetRect();
            if (Raylib.CheckCollisionRecs(mr, pr))
            {
                player.TakeDamage(Math.Max(1, 6 - player.Stats.Armor));
            }
        }

        // Handle mob deaths and drops
        for (int i = _mobs.Count - 1; i >= 0; i--)
        {
            var mob = _mobs[i];
            if (mob.Dead)
            {
                player.AddXP(20 + _rng.Next(10));
                if (_rng.NextDouble() < 0.12)
                {
                    var item = Item.GenerateRandom(player.Level);
                    drops.Add(new ItemDrop(mob.X + Mob.W / 2f, mob.Y + Mob.H / 2f, item));
                }
                _mobs.RemoveAt(i);
            }
        }
    }

    private void SpawnNearPlayer(Player player, World.GameWorld world)
    {
        for (int tries = 0; tries < 20; tries++)
        {
            float offX = (_rng.NextSingle() - 0.5f) * 300;
            float offY = (_rng.NextSingle() - 0.5f) * 200;
            float wx = player.X + offX;
            float wy = player.Y + offY;
            int tx = (int)(wx / Constants.TileSize);
            int ty = (int)(wy / Constants.TileSize);
            if (tx < 1 || tx >= world.Width - 1 || ty < 1 || ty >= world.Height - 1) continue;
            if (world.GetTile(tx, ty) == Constants.TileAir && world.IsSolid(tx, ty + 1))
            {
                _mobs.Add(Mob.Spawn(wx, wy));
                return;
            }
        }
    }

    public void Draw(float camX, float camY, float zoom)
    {
        foreach (var mob in _mobs) mob.Draw(camX, camY, zoom);
    }
}
