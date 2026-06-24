// src/Combat/CombatManager.cs
using Raylib_cs;
using System.Numerics;
using Varius.Core;
using Varius.Entities;

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
    private readonly Random _rng = new();

    public List<Projectile> Projectiles => _projectiles;

    public void TriggerManualSwing(Player player)
    {
        if (_swingCooldown > 0) return;
        _swingCooldown = 0.35f / player.Stats.Haste;
        float cx = player.X + Player.W / 2f;
        float cy = player.Y + Player.H / 2f;
        float speed = 340f;
        float vx = player.Direction * speed;
        SpawnProjectile(cx, cy, vx, 0, CalculateDamage(player), false, new Color(200, 230, 255, 255));
    }

    public void SpawnProjectile(float x, float y, float vx, float vy, int damage, bool isEnemy, Color col)
    {
        _projectiles.Add(new Projectile { X = x, Y = y, VX = vx, VY = vy, Damage = damage, IsEnemy = isEnemy, Col = col });
    }

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

    public void Update(float dt, Player player, World.GameWorld world, List<Mob> mobs)
    {
        if (_swingCooldown > 0) _swingCooldown -= dt;

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
                        int dmg = (int)(player.Stats.BaseDmg * (crit ? player.Stats.CritDmg : 1f));
                        mob.Health -= dmg;
                        mob.FlashTimer = 0.2f;
                        SpawnDmgNumber(mob.X, mob.Y - 5, dmg, crit);
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
                    SpawnDmgNumber(player.X, player.Y - 5, reduced, false);
                    proj.Dead = true;
                }
            }
        }

        _numbers.RemoveAll(n => n.Update(dt));
    }

    public void Draw(float camX, float camY, float zoom)
    {
        foreach (var p in _projectiles) p.Draw(camX, camY, zoom);
        foreach (var n in _numbers) n.Draw(camX, camY, zoom);
    }
}
