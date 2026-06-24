// src/UI/Minimap.cs
// Minimap overlay + compass: shows explored tiles, player pos, ores, cages, bosses
using Raylib_cs;
using System.Numerics;
using Varius.Core;
using Varius.Entities;

namespace Varius.UI;

public class Minimap
{
    private readonly bool[,] _explored;
    private int _worldW;
    private int _worldH;

    // Map of important tiles to display even if not yet "explored"
    private readonly Dictionary<(int, int), Color> _markers = new();

    private const int MapW = 160;
    private const int MapH = 80;
    private const int MapX = Constants.ScreenWidth - MapW - 10;
    private const int MapY = 10;

    public Minimap(int worldW, int worldH)
    {
        _worldW = worldW;
        _worldH = worldH;
        _explored = new bool[worldW, worldH];
    }

    /// Call every frame: marks tiles within 12 tiles of player as explored
    public void Explore(float playerWorldX, float playerWorldY, int[,] grid)
    {
        int cx = (int)(playerWorldX / Constants.TileSize);
        int cy = (int)(playerWorldY / Constants.TileSize);
        int radius = 12;
        for (int dx = -radius; dx <= radius; dx++)
        for (int dy = -radius; dy <= radius; dy++)
        {
            int tx = cx + dx, ty = cy + dy;
            if (tx >= 0 && tx < _worldW && ty >= 0 && ty < _worldH)
                _explored[tx, ty] = true;
        }
    }

    public void Draw(float playerWorldX, float playerWorldY, int[,] grid,
        List<(float x, float y)> bossPositions)
    {
        // Semi-transparent background panel
        Raylib.DrawRectangle(MapX - 2, MapY - 2, MapW + 4, MapH + 4, new Color((byte)8, (byte)8, (byte)14, (byte)210));
        Raylib.DrawRectangleLines(MapX - 2, MapY - 2, MapW + 4, MapH + 4, new Color((byte)80, (byte)80, (byte)100, (byte)200));

        // Draw tile pixels
        float scaleX = (float)MapW / _worldW;
        float scaleY = (float)MapH / _worldH;

        for (int tx = 0; tx < _worldW; tx++)
        for (int ty = 0; ty < _worldH; ty++)
        {
            if (!_explored[tx, ty]) continue;
            int tile = grid[tx, ty];
            if (tile == Constants.TileAir) continue;

            int px = MapX + (int)(tx * scaleX);
            int py = MapY + (int)(ty * scaleY);
            int pw = Math.Max(1, (int)scaleX);
            int ph = Math.Max(1, (int)scaleY);

            Color col = tile switch
            {
                Constants.TileGrass        => new Color((byte)50, (byte)180, (byte)60, (byte)255),
                Constants.TileDirt         => new Color((byte)110, (byte)75, (byte)45, (byte)255),
                Constants.TileStone        => new Color((byte)90, (byte)90, (byte)95, (byte)255),
                Constants.TileIron         => new Color((byte)200, (byte)140, (byte)80, (byte)255),
                Constants.TileGold         => new Color((byte)255, (byte)210, (byte)20, (byte)255),
                Constants.TileCoal         => new Color((byte)35, (byte)35, (byte)38, (byte)255),
                Constants.TileBedrock      => new Color((byte)15, (byte)15, (byte)18, (byte)255),
                Constants.TileCage         => new Color((byte)60, (byte)220, (byte)200, (byte)255),
                Constants.TileTorch        => new Color((byte)255, (byte)180, (byte)50, (byte)255),
                // Biome tiles
                Constants.TileIce          => new Color((byte)140, (byte)210, (byte)255, (byte)255),
                Constants.TileObsidian     => new Color((byte)40, (byte)20, (byte)65, (byte)255),
                Constants.TileAncientBrick => new Color((byte)110, (byte)85, (byte)65, (byte)255),
                Constants.TileFrostCrystal => new Color((byte)100, (byte)230, (byte)255, (byte)255),
                Constants.TileEmberStone   => new Color((byte)220, (byte)70, (byte)10, (byte)255),
                Constants.TileRunicShard   => new Color((byte)155, (byte)70, (byte)230, (byte)255),
                Constants.TileBossChest    => new Color((byte)255, (byte)200, (byte)30, (byte)255),
                _ => new Color((byte)80, (byte)80, (byte)80, (byte)255)
            };
            Raylib.DrawRectangle(px, py, pw, ph, col);
        }

        // Boss positions — red pulsing dot
        float t = (float)Raylib.GetTime();
        foreach (var (bx, by) in bossPositions)
        {
            int tx = (int)(bx / Constants.TileSize);
            int ty = (int)(by / Constants.TileSize);
            if (tx >= 0 && tx < _worldW && ty >= 0 && ty < _worldH && _explored[tx, ty])
            {
                int px = MapX + (int)(tx * scaleX);
                int py = MapY + (int)(ty * scaleY);
                float pulse = 0.6f + 0.4f * MathF.Sin(t * 5f);
                Raylib.DrawCircle(px, py, (int)(3.5f * pulse), new Color((byte)255, (byte)30, (byte)30, (byte)230));
            }
        }

        // Player dot — bright green pulsing
        int ppx = MapX + (int)((playerWorldX / Constants.TileSize) * scaleX);
        int ppy = MapY + (int)((playerWorldY / Constants.TileSize) * scaleY);
        ppx = Math.Clamp(ppx, MapX + 2, MapX + MapW - 2);
        ppy = Math.Clamp(ppy, MapY + 2, MapY + MapH - 2);
        float playerPulse = 0.7f + 0.3f * MathF.Sin(t * 7f);
        Raylib.DrawCircle(ppx, ppy, (int)(3f * playerPulse), new Color((byte)60, (byte)255, (byte)100, (byte)255));
        Raylib.DrawCircle(ppx, ppy, 2, new Color((byte)255, (byte)255, (byte)255, (byte)255));

        // Biome depth indicators on right edge
        DrawBiomeMarker(MapY + (int)(Constants.BiomeIceStart * scaleY), "ICE", new Color((byte)140, (byte)210, (byte)255, (byte)200));
        DrawBiomeMarker(MapY + (int)(Constants.BiomeMagmaStart * scaleY), "MAGMA", new Color((byte)255, (byte)90, (byte)20, (byte)200));
        DrawBiomeMarker(MapY + (int)(Constants.BiomeRuinsStart * scaleY), "RUINS", new Color((byte)160, (byte)80, (byte)255, (byte)200));

        // Minimap label
        Raylib.DrawText("MAP", MapX + 2, MapY + MapH + 3, 7, new Color((byte)160, (byte)160, (byte)180, (byte)200));

        // ── Compass rose (surface direction) ────────────────────────────────
        DrawCompass(playerWorldY);
    }

    private static void DrawBiomeMarker(int y, string label, Color col)
    {
        y = Math.Clamp(y, MapY, MapY + MapH);
        Raylib.DrawLine(MapX, y, MapX + MapW, y, new Color(col.R, col.G, col.B, (byte)80));
        Raylib.DrawText(label, MapX + 2, y + 1, 6, col);
    }

    private static void DrawCompass(float playerWorldY)
    {
        // Small compass in top-left of minimap
        int cx = MapX + 14, cy = MapY + MapH - 16;
        float surfaceWorldY = Constants.SurfaceY * Constants.TileSize;
        float dy = surfaceWorldY - playerWorldY;
        float dist = MathF.Abs(dy);

        // North arrow (always pointing up, labelled with "↑SURF")
        Raylib.DrawCircle(cx, cy, 11, new Color((byte)10, (byte)10, (byte)18, (byte)200));
        Raylib.DrawCircleLines(cx, cy, 11, new Color((byte)80, (byte)80, (byte)100, (byte)200));
        Raylib.DrawLine(cx, cy + 8, cx, cy - 8, new Color((byte)80, (byte)200, (byte)120, (byte)240));
        Raylib.DrawLine(cx, cy - 8, cx - 3, cy - 3, new Color((byte)80, (byte)200, (byte)120, (byte)240));
        Raylib.DrawLine(cx, cy - 8, cx + 3, cy - 3, new Color((byte)80, (byte)200, (byte)120, (byte)240));
        Raylib.DrawText("N", cx - 3, cy - 22, 7, new Color((byte)80, (byte)200, (byte)120, (byte)220));
        // Depth indicator
        int depthTiles = (int)(playerWorldY / Constants.TileSize) - Constants.SurfaceY;
        string depthStr = depthTiles > 0 ? $"{depthTiles * Constants.TileSize / 10}m" : "SURF";
        Raylib.DrawText(depthStr, cx - Raylib.MeasureText(depthStr, 6) / 2, cy + 14, 6,
            new Color((byte)200, (byte)200, (byte)220, (byte)200));
    }
}
