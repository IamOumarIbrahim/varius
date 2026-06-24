// src/World/WeatherSystem.cs
using Raylib_cs;
using System;
using System.Collections.Generic;
using System.Numerics;
using Varius.Core;

namespace Varius.World;

public class WeatherSystem
{
    private struct WeatherParticle
    {
        public float X, Y;
        public float VX, VY;
        public Color Col;
        public float Size;
        public float Lifetime;
        public float MaxLifetime;
    }

    private readonly List<WeatherParticle> _particles = new();
    private readonly Random _rng = new();

    public void Update(float dt, float camX, float camY, BiomeType biome)
    {
        int spawnCount = biome switch
        {
            BiomeType.Surface => 3, // Rain
            BiomeType.Ice     => 2, // Snow
            BiomeType.Magma   => 2, // Embers
            BiomeType.Ruins   => 2, // Void sparkles
            _ => 0
        };

        // Render relative to viewport
        for (int i = 0; i < spawnCount; i++)
        {
            if (_particles.Count >= 300) break;

            float px = camX / 1.5f + _rng.Next(0, (int)(Constants.ScreenWidth / 1.5f));
            float py = biome switch
            {
                BiomeType.Magma => camY / 1.5f + Constants.ScreenHeight / 1.5f + 10,
                BiomeType.Ruins => camY / 1.5f + _rng.Next(0, (int)(Constants.ScreenHeight / 1.5f)),
                _ => camY / 1.5f - 10
            };

            float vx = 0, vy = 0;
            Color col = Color.White;
            float size = 2f;
            float lifetime = _rng.NextSingle() * 1.8f + 1.5f;

            switch (biome)
            {
                case BiomeType.Surface:
                    vx = -45f;
                    vy = 340f;
                    col = new Color(110, 170, 255, 130);
                    size = 1f + _rng.NextSingle() * 1f;
                    break;
                case BiomeType.Ice:
                    vx = (float)(_rng.NextDouble() * 20 - 10);
                    vy = 55f + _rng.NextSingle() * 25f;
                    col = new Color(230, 245, 255, 190);
                    size = 1.2f + _rng.NextSingle() * 1.8f;
                    break;
                case BiomeType.Magma:
                    vx = (float)(_rng.NextDouble() * 30 - 15);
                    vy = -35f - _rng.NextSingle() * 25f;
                    col = _rng.Next(2) == 0 ? new Color(255, 150, 20, 160) : new Color(255, 70, 10, 160);
                    size = 1.8f + _rng.NextSingle() * 2f;
                    break;
                case BiomeType.Ruins:
                    vx = (float)(_rng.NextDouble() * 30 - 15);
                    vy = (float)(_rng.NextDouble() * 30 - 15);
                    col = new Color(185, 70, 255, 140);
                    size = 1.4f + _rng.NextSingle() * 1.6f;
                    break;
            }

            _particles.Add(new WeatherParticle
            {
                X = px, Y = py,
                VX = vx, VY = vy,
                Col = col,
                Size = size,
                Lifetime = lifetime,
                MaxLifetime = lifetime
            });
        }

        for (int i = _particles.Count - 1; i >= 0; i--)
        {
            var p = _particles[i];
            p.Lifetime -= dt;
            if (p.Lifetime <= 0)
            {
                _particles.RemoveAt(i);
                continue;
            }

            p.X += p.VX * dt;
            p.Y += p.VY * dt;

            if (biome == BiomeType.Ice)
            {
                p.VX += MathF.Sin(p.Lifetime * 4f) * 12f * dt;
            }

            _particles[i] = p;
        }
    }

    public void Draw(float camX, float camY, float zoom)
    {
        foreach (var p in _particles)
        {
            float sx = p.X * zoom - camX;
            float sy = p.Y * zoom - camY;

            float pct = p.Lifetime / p.MaxLifetime;
            Color drawCol = new Color(p.Col.R, p.Col.G, p.Col.B, (byte)(p.Col.A * pct));

            if (p.VY > 200f) // Rain line
            {
                Raylib.DrawLineEx(new Vector2(sx, sy), new Vector2(sx + p.VX * 0.02f, sy + p.VY * 0.02f), p.Size * zoom, drawCol);
            }
            else
            {
                Raylib.DrawCircle((int)sx, (int)sy, p.Size * zoom, drawCol);
            }
        }
    }
}
