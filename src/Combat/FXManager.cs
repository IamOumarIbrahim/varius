// src/Combat/FXManager.cs
// Screen shake, slash trails, spark/impact particles, blood splats
using Raylib_cs;
using System.Numerics;
using Varius.Core;
using Varius.Entities;

namespace Varius.Combat;

// ── Screen Shake ──────────────────────────────────────────────────────────────
public class ScreenShake
{
    private float _duration;
    private float _intensity;
    private readonly Random _rng = new();

    public bool Active => _duration > 0;

    public void Trigger(float intensity, float duration)
    {
        // Only escalate, never weaken an active shake
        if (intensity >= _intensity)
        {
            _intensity = intensity;
            _duration = duration;
        }
    }

    /// Returns a camera offset to apply this frame
    public (float dx, float dy) Update(float dt)
    {
        if (_duration <= 0) return (0, 0);
        _duration -= dt;
        float t = _duration > 0 ? _intensity * (_duration / 0.3f) : 0;
        t = Math.Min(t, _intensity);
        float dx = (_rng.NextSingle() - 0.5f) * 2f * t;
        float dy = (_rng.NextSingle() - 0.5f) * 2f * t;
        return (dx, dy);
    }
}

// ── Slash Trail ───────────────────────────────────────────────────────────────
public class SlashTrail
{
    private record TrailPoint(float X, float Y, float Life, Color Col);
    private readonly List<TrailPoint> _points = new();
    private readonly List<(Vector2 a, Vector2 b, float life, float maxLife, Color col)> _arcs = new();

    public void SpawnSwingArc(float worldX, float worldY, int direction, Stance stance)
    {
        Color col = stance switch
        {
            Stance.Water => new Color((byte)60, (byte)160, (byte)255, (byte)200),
            Stance.Wind  => new Color((byte)80, (byte)240, (byte)130, (byte)200),
            _            => new Color((byte)255, (byte)220, (byte)60, (byte)200)
        };
        // Arc anchored at player center, sweeping outward
        float arcLen = 52f;
        float baseAng = direction == 1 ? -30f : 210f;
        float endAng = direction == 1 ? 30f : 150f;
        for (float ang = baseAng; ang <= endAng; ang += 8f)
        {
            float rad = ang * MathF.PI / 180f;
            float px = worldX + MathF.Cos(rad) * arcLen;
            float py = worldY + MathF.Sin(rad) * arcLen;
            _points.Add(new TrailPoint(px, py, 0.22f, col));
        }
    }

    public void SpawnProjectileTrail(float worldX, float worldY, Color col)
    {
        _points.Add(new TrailPoint(worldX, worldY, 0.14f, col));
    }

    public void Update(float dt)
    {
        for (int i = _points.Count - 1; i >= 0; i--)
        {
            var p = _points[i];
            if (p.Life - dt <= 0) _points.RemoveAt(i);
            else _points[i] = p with { Life = p.Life - dt };
        }
    }

    public void Draw(float camX, float camY, float zoom)
    {
        foreach (var p in _points)
        {
            int sx = (int)(p.X * zoom - camX);
            int sy = (int)(p.Y * zoom - camY);
            float alpha = p.Life / 0.22f;
            Raylib.DrawCircle(sx, sy, (int)(2.5f * zoom), new Color(p.Col.R, p.Col.G, p.Col.B, (byte)(alpha * p.Col.A)));
        }
    }
}

// ── Spark / Impact Particles ──────────────────────────────────────────────────
public class FXParticle
{
    public float X { get; set; }
    public float Y { get; set; }
    public float VX { get; set; }
    public float VY { get; set; }
    public float Life { get; set; }
    public float MaxLife { get; set; }
    public Color Col { get; set; }
    public float Size { get; set; }

    public bool Update(float dt)
    {
        VY += 320f * dt;  // gravity on sparks
        X += VX * dt;
        Y += VY * dt;
        Life -= dt;
        return Life <= 0;
    }

    public void Draw(float camX, float camY, float zoom)
    {
        float alpha = Math.Clamp(Life / MaxLife, 0, 1);
        int sx = (int)(X * zoom - camX);
        int sy = (int)(Y * zoom - camY);
        int r = (int)(Size * zoom);
        if (r < 1) r = 1;
        Raylib.DrawCircle(sx, sy, r, new Color(Col.R, Col.G, Col.B, (byte)(alpha * 255)));
    }
}

public class FXManager
{
    public ScreenShake Shake { get; } = new();
    public SlashTrail Trails { get; } = new();
    private readonly List<FXParticle> _particles = new();
    private readonly Random _rng = new();

    // ── Spawners ──────────────────────────────────────────────────────────────
    public void SpawnHitImpact(float worldX, float worldY, Stance stance, bool isCrit)
    {
        // Screen shake
        float intensity = isCrit ? 6.5f : 2.8f;
        float dur = isCrit ? 0.22f : 0.12f;
        Shake.Trigger(intensity, dur);

        // Sparks
        int count = isCrit ? 14 : 7;
        Color col = stance switch
        {
            Stance.Water => new Color((byte)80, (byte)180, (byte)255, (byte)255),
            Stance.Wind  => new Color((byte)100, (byte)255, (byte)150, (byte)255),
            _            => new Color((byte)255, (byte)220, (byte)80, (byte)255)
        };

        for (int i = 0; i < count; i++)
        {
            float angle = _rng.NextSingle() * MathF.PI * 2f;
            float speed = _rng.NextSingle() * 80f + (isCrit ? 60f : 30f);
            _particles.Add(new FXParticle
            {
                X = worldX, Y = worldY,
                VX = MathF.Cos(angle) * speed,
                VY = MathF.Sin(angle) * speed - 20f,
                Life = isCrit ? 0.55f : 0.38f,
                MaxLife = isCrit ? 0.55f : 0.38f,
                Col = col,
                Size = isCrit ? 1.8f : 1.1f
            });
        }

        // White flash particle at impact point
        _particles.Add(new FXParticle
        {
            X = worldX, Y = worldY,
            VX = 0, VY = 0,
            Life = 0.09f, MaxLife = 0.09f,
            Col = new Color((byte)255, (byte)255, (byte)255, (byte)255),
            Size = isCrit ? 4f : 2.5f
        });
    }

    public void SpawnParryBurst(float worldX, float worldY)
    {
        Shake.Trigger(4f, 0.18f);
        // Ring of blue-white sparks
        for (int i = 0; i < 16; i++)
        {
            float angle = i * MathF.PI * 2f / 16f;
            float speed = 90f + _rng.NextSingle() * 40f;
            _particles.Add(new FXParticle
            {
                X = worldX, Y = worldY,
                VX = MathF.Cos(angle) * speed,
                VY = MathF.Sin(angle) * speed,
                Life = 0.5f, MaxLife = 0.5f,
                Col = new Color((byte)100, (byte)200, (byte)255, (byte)255),
                Size = 1.4f
            });
        }
    }

    public void SpawnMineImpact(float worldX, float worldY, int tileType)
    {
        Shake.Trigger(1.5f, 0.08f);
        Color col = tileType switch
        {
            Constants.TileGold         => new Color((byte)255, (byte)200, (byte)40, (byte)255),
            Constants.TileIron         => new Color((byte)200, (byte)140, (byte)80, (byte)255),
            Constants.TileFrostCrystal => new Color((byte)160, (byte)230, (byte)255, (byte)255),
            Constants.TileEmberStone   => new Color((byte)255, (byte)100, (byte)20, (byte)255),
            Constants.TileRunicShard   => new Color((byte)180, (byte)80, (byte)255, (byte)255),
            _                          => new Color((byte)160, (byte)140, (byte)100, (byte)255)
        };
        for (int i = 0; i < 6; i++)
        {
            float angle = _rng.NextSingle() * MathF.PI * 2f;
            float speed = _rng.NextSingle() * 45f + 20f;
            _particles.Add(new FXParticle
            {
                X = worldX, Y = worldY,
                VX = MathF.Cos(angle) * speed,
                VY = MathF.Sin(angle) * speed - 30f,
                Life = 0.45f, MaxLife = 0.45f,
                Col = col,
                Size = 1.0f
            });
        }
    }

    public void SpawnBiomeSpark(float worldX, float worldY, Color col)
    {
        _particles.Add(new FXParticle
        {
            X = worldX, Y = worldY,
            VX = (_rng.NextSingle() - 0.5f) * 40f,
            VY = -(_rng.NextSingle() * 30f + 10f),
            Life = 0.7f, MaxLife = 0.7f,
            Col = col,
            Size = 0.9f
        });
    }

    // ── Update & Draw ─────────────────────────────────────────────────────────
    public void Update(float dt)
    {
        Trails.Update(dt);
        _particles.RemoveAll(p => p.Update(dt));
    }

    public void Draw(float camX, float camY, float zoom)
    {
        Trails.Draw(camX, camY, zoom);
        foreach (var p in _particles)
            p.Draw(camX, camY, zoom);
    }
}
