// src/Combat/CombatManager.cs
using Raylib_cs;
using System.Numerics;
using Varius.Core;
using Varius.Entities;
using Varius.Audio;

namespace Varius.Combat;

public class Projectile
{
    public float X { get; set; }
    public float Y { get; set; }
    public float VX { get; set; }
    public float VY { get; set; }
    public int Damage { get; set; }
    public bool IsEnemy { get; set; }
    public bool Dead { get; set; }
    private float _lifetime = 3.5f;
    public Color Col { get; set; }

    public void Update(float dt, World.GameWorld world)
    {
        if (Dead) return;
        X += VX * dt;
        Y += VY * dt;
        _lifetime -= dt;
        if (_lifetime <= 0) { Dead = true; return; }
        int tx = (int)(X / Constants.TileSize);
        int ty = (int)(Y / Constants.TileSize);
        if (world.IsSolid(tx, ty)) Dead = true;
    }

    public void Draw(float camX, float camY, float zoom)
    {
        if (Dead) return;
        int sx = (int)(X * zoom - camX);
        int sy = (int)(Y * zoom - camY);
        int r = (int)(4 * zoom);
        Raylib.DrawCircle(sx, sy, r * 1.5f, new Color(Col.R, Col.G, Col.B, (byte)60));
        Raylib.DrawCircle(sx, sy, r, Col);
    }
}

public class DamageNumber
{
    public float X { get; set; }
    public float Y { get; set; }
    public int Amount { get; set; }
    public bool IsCrit { get; set; }
    private float _lifetime = 1.4f;
    private float _vy = -55f;

    public bool Update(float dt)
    {
        _vy += 120f * dt;
        Y += _vy * dt;
        _lifetime -= dt;
        return _lifetime <= 0;
    }

    public void Draw(float camX, float camY, float zoom)
    {
        float alpha = Math.Clamp(_lifetime / 1.4f, 0, 1);
        int sx = (int)(X * zoom - camX);
        int sy = (int)(Y * zoom - camY);
        var col = IsCrit ? new Color(255, 80, 30, (int)(alpha * 255)) : new Color(255, 240, 80, (int)(alpha * 255));
        int fs = IsCrit ? (int)(14 * zoom) : (int)(10 * zoom);
        Raylib.DrawText(IsCrit ? $"!{Amount}!" : Amount.ToString(), sx - 10, sy, Math.Clamp(fs, 8, 32), col);
    }
}

public class CombatManager
{
    private readonly List<Projectile> _projectiles = new();
    private readonly List<DamageNumber> _numbers = new();
    private float _swingCooldown;
    private float _subWeaponTimer;
    private readonly Random _rng = new();

    public List<Projectile> Projectiles => _projectiles;

    public void TriggerManualSwing(Player player)
    {
        if (_swingCooldown > 0) return;
        _swingCooldown = 0.35f / player.Stats.Haste;
        
        float speed = 340f;
        if (player.Stance == Stance.Wind) speed *= 1.25f;

        float cx = player.X + Player.W / 2f;
        float cy = player.Y + Player.H / 2f;
        float vx = player.Direction * speed;

        int baseDamage = CalculateDamage(player);

        // Character active boost: Billy Butcher Compound V Rush (+3x damage if low HP)
        if (player.CharDef.Name == "Billy Butcher" && player.Health < player.Stats.MaxHealth * 0.4f)
        {
            baseDamage *= 3;
        }

        // Character active: Zoro Santoryu (triples slashes)
        int count = 1;
        if (player.CharDef.Name == "Zoro")
        {
            count = 3;
        }

        for (int i = 0; i < count; i++)
        {
            float vyOffset = (i - (count - 1) / 2f) * 60f;
            SpawnProjectile(cx, cy, vx, vyOffset, baseDamage, false, new Color(200, 230, 255, 255));
        }
    }

    public void SpawnProjectile(float x, float y, float vx, float vy, int damage, bool isEnemy, Color col)
    {
        _projectiles.Add(new Projectile { X = x, Y = y, VX = vx, VY = vy, Damage = damage, IsEnemy = isEnemy, Col = col });
    }

    public void AddProjectile(Projectile p) => _projectiles.Add(p);

    public int CalculateDamage(Player player)
    {
        float dmg = player.Stats.BaseDmg;
        bool crit = (float)_rng.NextDouble() < player.Stats.CritRate;
        if (crit) dmg *= player.Stats.CritDmg;
        return (int)dmg;
    }

    public void SpawnDmgNumber(float x, float y, int amount, bool crit)
    {
        _numbers.Add(new DamageNumber { X = x, Y = y, Amount = amount, IsCrit = crit });
    }

    public void Update(float dt, Player player, World.GameWorld world, List<Mob> mobs, FXManager? fx = null)
    {
        if (_swingCooldown > 0) _swingCooldown -= dt;

        // Auto-firing sub-weapons (Vampire Survivors style)
        _subWeaponTimer += dt;
        if (_subWeaponTimer >= 3.0f)
        {
            _subWeaponTimer = 0f;
            TriggerSubWeapon(player, mobs);
        }

        foreach (var p in _projectiles) p.Update(dt, world);
        _projectiles.RemoveAll(p => p.Dead);

        foreach (var proj in _projectiles.ToList())
        {
            if (!proj.IsEnemy)
            {
                foreach (var mob in mobs.ToList())
                {
                    var mr = new Rectangle(mob.X * 1.5f, mob.Y * 1.5f, Mob.W * 1.5f, Mob.H * 1.5f);
                    if (Raylib.CheckCollisionPointRec(new Vector2(proj.X * 1.5f, proj.Y * 1.5f), mr))
                    {
                        bool crit = (float)_rng.NextDouble() < player.Stats.CritRate;
                        
                        // Walter White damage multiplier deep in caves
                        float dMult = 1.0f;
                        if (player.CharDef.Name == "Walter White" && player.Y > 30 * Constants.TileSize)
                        {
                            dMult = 1.35f;
                        }

                        int dmg = (int)(player.Stats.BaseDmg * dMult * (crit ? player.Stats.CritDmg : 1f));
                        mob.Health -= dmg;
                        mob.FlashTimer = 0.2f;

                        // Apply Stance/character status effects
                        if (player.Stance == Stance.Water || player.CharDef.Name == "Elsa")
                        {
                            mob.ApplyFreeze(3.5f);
                        }
                        else if (player.Stance == Stance.Stone)
                        {
                            mob.ApplyBurn(3.0f);
                        }
                        else if (player.Stance == Stance.Wind)
                        {
                            mob.ApplyBleed(4.0f);
                        }

                        // Increment Stance Charge on hit
                        player.StanceCharge = Math.Min(100f, player.StanceCharge + 8f);
                        SoundManager.Instance.Play("hit");

                        SpawnDmgNumber(mob.X, mob.Y - 5, dmg, crit);
                        fx?.SpawnHitImpact(mob.X + Mob.W / 2f, mob.Y + Mob.H / 2f, player.Stance, crit);
                        proj.Dead = true;
                        break;
                    }
                }
            }
            else
            {
                var pr = new Rectangle(player.X * 1.5f, player.Y * 1.5f, Player.W * 1.5f, Player.H * 1.5f);
                if (Raylib.CheckCollisionPointRec(new Vector2(proj.X * 1.5f, proj.Y * 1.5f), pr))
                {
                    int reduced = Math.Max(1, proj.Damage - player.Stats.Armor);
                    player.TakeDamage(reduced);
                    SoundManager.Instance.Play("damage");
                    SpawnDmgNumber(player.X, player.Y - 5, reduced, false);
                    fx?.SpawnHitImpact(player.X + Player.W / 2f, player.Y + Player.H / 2f, player.Stance, false);
                    proj.Dead = true;
                }
            }
        }

        _numbers.RemoveAll(n => n.Update(dt));
    }

    private void TriggerSubWeapon(Player player, List<Mob> mobs)
    {
        Mob? target = null;
        float minDist = 999999f;
        float px = player.X + Player.W / 2f;
        float py = player.Y + Player.H / 2f;
        foreach (var mob in mobs)
        {
            if (mob.Dead) continue;
            float dx = mob.X - px;
            float dy = mob.Y - py;
            float dist = MathF.Sqrt(dx * dx + dy * dy);
            if (dist < minDist)
            {
                minDist = dist;
                target = mob;
            }
        }

        float vx = player.Direction * 220f;
        float vy = 0f;
        if (target != null && minDist < 250f)
        {
            float dx = (target.X + Mob.W / 2f) - px;
            float dy = (target.Y + Mob.H / 2f) - py;
            if (minDist > 0)
            {
                vx = (dx / minDist) * 220f;
                vy = (dy / minDist) * 220f;
            }
        }

        int projectileCount = 1 + player.Level / 4;
        if (projectileCount > 3) projectileCount = 3;

        for (int i = 0; i < projectileCount; i++)
        {
            float angleOffset = (i - (projectileCount - 1) / 2f) * 0.25f;
            float cos = MathF.Cos(angleOffset);
            float sin = MathF.Sin(angleOffset);
            float rx = vx * cos - vy * sin;
            float ry = vx * sin + vy * cos;

            _projectiles.Add(new Projectile
            {
                X = px,
                Y = py,
                VX = rx,
                VY = ry,
                Damage = (int)(player.Stats.BaseDmg * 0.7f),
                IsEnemy = false,
                Col = new Color(100, 200, 255, 255)
            });
        }
    }

    public void Draw(float camX, float camY, float zoom)
    {
        foreach (var p in _projectiles) p.Draw(camX, camY, zoom);
        foreach (var n in _numbers) n.Draw(camX, camY, zoom);
    }
}
