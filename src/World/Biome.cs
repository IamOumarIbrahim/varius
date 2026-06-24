// src/World/Biome.cs
using Raylib_cs;
using Varius.Core;

namespace Varius.World;

public enum BiomeType { Surface, Ice, Magma, Ruins }

public static class BiomeHelper
{
    public static BiomeType GetBiome(int tileY)
    {
        if (tileY < Constants.BiomeIceStart)   return BiomeType.Surface;
        if (tileY < Constants.BiomeMagmaStart) return BiomeType.Ice;
        if (tileY < Constants.BiomeRuinsStart) return BiomeType.Magma;
        return BiomeType.Ruins;
    }

    /// Background gradient colours for the cave section at a given camera Y (world pixels)
    public static Color GetCaveBgColor(float worldY)
    {
        float tileY = worldY / Constants.TileSize;
        if (tileY < Constants.BiomeIceStart)   return new Color(15, 18, 30, 255);
        if (tileY < Constants.BiomeMagmaStart) return new Color(8, 22, 45, 255);
        if (tileY < Constants.BiomeRuinsStart) return new Color(35, 10, 8, 255);
        return new Color(12, 8, 22, 255);
    }

    /// Ambient/fog overlay colour for cave lighting per biome
    public static Color GetAmbientColor(BiomeType b) => b switch
    {
        BiomeType.Ice   => new Color(20, 60, 120, 195),
        BiomeType.Magma => new Color(80, 20, 5, 210),
        BiomeType.Ruins => new Color(30, 10, 55, 200),
        _               => new Color(0, 0, 8, 210)
    };

    /// Player light radius in world-space tiles, smaller deeper
    public static float GetLightRadius(BiomeType b) => b switch
    {
        BiomeType.Surface => 10.5f,
        BiomeType.Ice     => 9.0f,
        BiomeType.Magma   => 8.0f,
        BiomeType.Ruins   => 7.5f,
        _                 => 10.5f
    };

    public static Color GetTileColor(int tile) => tile switch
    {
        Constants.TileIce          => new Color(160, 220, 255, 255),
        Constants.TileObsidian     => new Color(30, 18, 55, 255),
        Constants.TileAncientBrick => new Color(120, 95, 70, 255),
        Constants.TileRuinsRune    => new Color(80, 55, 100, 255),
        Constants.TileFrostCrystal => new Color(100, 210, 255, 255),
        Constants.TileEmberStone   => new Color(210, 80, 20, 255),
        Constants.TileRunicShard   => new Color(160, 80, 240, 255),
        Constants.TileBossChest    => new Color(200, 170, 30, 255),
        Constants.TileBossArenaFloor => new Color(85, 65, 90, 255),
        _ => Color.Magenta
    };

    /// Which ore/resource drop a mined tile yields
    public static string? GetResourceDrop(int tile) => tile switch
    {
        Constants.TileIron         => Constants.RES_IRON,
        Constants.TileGold         => Constants.RES_GOLD,
        Constants.TileCoal         => Constants.RES_COAL,
        Constants.TileFrostCrystal => Constants.RES_FROST,
        Constants.TileEmberStone   => Constants.RES_EMBER,
        Constants.TileRunicShard   => Constants.RES_RUNIC,
        _                          => null
    };

    /// What world tile IDs count as biome "stone" for generation
    public static int GetBiomeStone(int tileY)
    {
        return GetBiome(tileY) switch
        {
            BiomeType.Ice   => Constants.TileIce,
            BiomeType.Magma => Constants.TileObsidian,
            BiomeType.Ruins => Constants.TileAncientBrick,
            _               => Constants.TileStone
        };
    }

    /// Ore probability table per biome
    public static int GetRandomOre(int tileY, Random rng)
    {
        double r = rng.NextDouble();
        return GetBiome(tileY) switch
        {
            BiomeType.Ice => r < 0.04 ? Constants.TileFrostCrystal :
                             r < 0.06 ? Constants.TileIron :
                             r < 0.07 ? Constants.TileCoal : Constants.TileIce,
            BiomeType.Magma => r < 0.05 ? Constants.TileEmberStone :
                               r < 0.07 ? Constants.TileGold :
                               r < 0.09 ? Constants.TileIron : Constants.TileObsidian,
            BiomeType.Ruins => r < 0.04 ? Constants.TileRunicShard :
                               r < 0.07 ? Constants.TileGold :
                               r < 0.09 ? Constants.TileIron : Constants.TileAncientBrick,
            _ => r < 0.03 ? Constants.TileCoal :
                 r < 0.05 ? Constants.TileIron :
                 r < 0.06 ? Constants.TileGold : Constants.TileStone
        };
    }

    /// True if this tile is solid for collision purposes
    public static bool IsBiomeSolid(int tile) =>
        tile == Constants.TileIce || tile == Constants.TileObsidian ||
        tile == Constants.TileAncientBrick || tile == Constants.TileRuinsRune ||
        tile == Constants.TileBossArenaFloor;
}

/// Particle effects for biome ambiance (magma drips, frost particles, rune glows)
public class BiomeParticle
{
    public float X { get; set; }
    public float Y { get; set; }
    public float VX { get; set; }
    public float VY { get; set; }
    public float Life { get; set; }
    public float MaxLife { get; set; }
    public Color Col { get; set; }
    public float Size { get; set; }
    public string Kind { get; set; } = "SPARK";

    public bool Update(float dt)
    {
        VY += 60f * dt;
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
        Raylib.DrawCircle(sx, sy, r, new Color(Col.R, Col.G, Col.B, (byte)(alpha * Col.A)));
    }
}

public class BiomeParticleSystem
{
    private readonly List<BiomeParticle> _particles = new();
    private float _spawnTimer;
    private readonly Random _rng = new();

    public void Update(float dt, float playerX, float playerY, int[,] grid, int worldW, int worldH)
    {
        _spawnTimer += dt;
        if (_spawnTimer >= 0.18f)
        {
            _spawnTimer = 0;
            TrySpawnAmbient(playerX, playerY, grid, worldW, worldH);
        }
        _particles.RemoveAll(p => p.Update(dt));
    }

    private void TrySpawnAmbient(float px, float py, int[,] grid, int worldW, int worldH)
    {
        int cx = (int)(px / Constants.TileSize);
        int cy = (int)(py / Constants.TileSize);
        for (int attempt = 0; attempt < 4; attempt++)
        {
            int tx = cx + _rng.Next(-12, 13);
            int ty = cy + _rng.Next(-8, 9);
            if (tx < 0 || tx >= worldW || ty < 0 || ty >= worldH) continue;
            int tile = grid[tx, ty];
            BiomeType biome = BiomeHelper.GetBiome(ty);

            switch (biome)
            {
                case BiomeType.Magma when tile == Constants.TileAir:
                    // Upward heat shimmer / ember float
                    if (ty + 1 < worldH && grid[tx, ty + 1] == Constants.TileObsidian)
                    {
                        _particles.Add(new BiomeParticle
                        {
                            X = tx * Constants.TileSize + _rng.NextSingle() * Constants.TileSize,
                            Y = ty * Constants.TileSize,
                            VX = (_rng.NextSingle() - 0.5f) * 12f,
                            VY = -(_rng.NextSingle() * 25f + 10f),
                            Life = 1.4f, MaxLife = 1.4f,
                            Col = new Color((byte)255, (byte)_rng.Next(60, 140), (byte)0, (byte)200),
                            Size = _rng.NextSingle() * 1.2f + 0.5f,
                            Kind = "EMBER"
                        });
                    }
                    break;

                case BiomeType.Ice when tile == Constants.TileAir:
                    // Falling frost sparkles
                    if (ty > 0 && grid[tx, ty - 1] == Constants.TileIce)
                    {
                        _particles.Add(new BiomeParticle
                        {
                            X = tx * Constants.TileSize + _rng.NextSingle() * Constants.TileSize,
                            Y = ty * Constants.TileSize,
                            VX = (_rng.NextSingle() - 0.5f) * 6f,
                            VY = _rng.NextSingle() * 10f + 5f,
                            Life = 1.8f, MaxLife = 1.8f,
                            Col = new Color((byte)180, (byte)230, (byte)255, (byte)200),
                            Size = _rng.NextSingle() * 0.8f + 0.3f,
                            Kind = "FROST"
                        });
                    }
                    break;

                case BiomeType.Ruins when tile == Constants.TileRuinsRune:
                    // Rune glow pulse
                    _particles.Add(new BiomeParticle
                    {
                        X = tx * Constants.TileSize + Constants.TileSize / 2f,
                        Y = ty * Constants.TileSize + Constants.TileSize / 2f,
                        VX = (_rng.NextSingle() - 0.5f) * 8f,
                        VY = -(_rng.NextSingle() * 15f),
                        Life = 1.0f, MaxLife = 1.0f,
                        Col = new Color((byte)180, (byte)80, (byte)255, (byte)180),
                        Size = _rng.NextSingle() * 1.5f + 0.5f,
                        Kind = "RUNE"
                    });
                    break;
            }
        }
    }

    public void Draw(float camX, float camY, float zoom)
    {
        foreach (var p in _particles)
            p.Draw(camX, camY, zoom);
    }
}
