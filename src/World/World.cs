// src/World/World.cs
using Raylib_cs;
using System.Numerics;
using Varius.Core;

namespace Varius.World;

public struct Structure
{
    public int Tx, Ty;
    public string Type; // "HOUSE", "FORGE", "LIBRARY"
    public int Level;
}

public class GameWorld
{
    public int Width { get; }
    public int Height { get; }
    public int[,] Grid { get; set; }
    public List<Structure> Structures { get; set; } = new();

    private readonly Random _rng = new();

    // Cloud system
    private readonly List<(float x, float y, float speed, float w, float h)> _clouds = new();

    public GameWorld(int width = Constants.WorldWidth, int height = Constants.WorldHeight)
    {
        Width = width;
        Height = height;
        Grid = new int[width, height];
        for (int i = 0; i < 18; i++)
        {
            _clouds.Add((
                (float)_rng.NextDouble() * width * Constants.TileSize,
                (float)_rng.NextDouble() * 180 + 10,
                (float)_rng.NextDouble() * 14 + 6,
                (float)_rng.NextDouble() * 80 + 60,
                (float)_rng.NextDouble() * 22 + 22
            ));
        }
        Generate();
    }

    public void Generate()
    {
        // Surface heightmap
        var surf = new int[Width];
        for (int x = 0; x < Width; x++)
            surf[x] = (int)(Constants.SurfaceY + 4 * Math.Sin(x * 0.1) + 2 * Math.Sin(x * 0.03));

        for (int x = 0; x < Width; x++)
        for (int y = 0; y < Height; y++)
        {
            int sh = surf[x];
            if (y < sh) Grid[x, y] = Constants.TileAir;
            else if (y == sh) Grid[x, y] = Constants.TileGrass;
            else if (y > sh && y < sh + 5)
                Grid[x, y] = _rng.NextDouble() < 0.15 ? Constants.TileAir : Constants.TileDirt;
            else
            {
                if (_rng.NextDouble() < 0.46) Grid[x, y] = Constants.TileAir;
                else
                {
                    double r = _rng.NextDouble();
                    Grid[x, y] = r < 0.03 ? Constants.TileCoal :
                                 r < 0.05 ? Constants.TileIron :
                                 r < 0.06 ? Constants.TileGold : Constants.TileStone;
                }
            }
            if (y == Height - 1) Grid[x, y] = Constants.TileBedrock;
        }

        // Cellular automata cave smoothing
        var temp = (int[,])Grid.Clone();
        for (int pass = 0; pass < 4; pass++)
        {
            for (int x = 1; x < Width - 1; x++)
            for (int y = 15; y < Height - 1; y++)
            {
                int solids = 0;
                for (int dx = -1; dx <= 1; dx++)
                for (int dy = -1; dy <= 1; dy++)
                {
                    int nx = x + dx, ny = y + dy;
                    if (nx >= 0 && nx < Width && ny >= 0 && ny < Height)
                        if (temp[nx, ny] != Constants.TileAir && temp[nx, ny] != Constants.TileCage)
                            solids++;
                }
                if (temp[x, y] != Constants.TileAir && temp[x, y] != Constants.TileCage)
                    Grid[x, y] = solids >= 4 ? temp[x, y] : Constants.TileAir;
                else
                    Grid[x, y] = solids >= 5 ? (y > 30 ? Constants.TileStone : Constants.TileDirt) : Constants.TileAir;
            }
            temp = (int[,])Grid.Clone();
        }

        // Place cages
        int cages = 0;
        for (int tries = 0; tries < 150 && cages < 6; tries++)
        {
            int cx = _rng.Next(10, Width - 10);
            int cy = _rng.Next(35, Height - 5);
            if (Grid[cx, cy] == Constants.TileAir && Grid[cx, cy + 1] != Constants.TileAir)
            { Grid[cx, cy] = Constants.TileCage; cages++; }
        }
    }

    public void UpdateClouds(float dt)
    {
        float worldW = Width * Constants.TileSize;
        for (int i = 0; i < _clouds.Count; i++)
        {
            var c = _clouds[i];
            c.x += c.speed * dt;
            if (c.x > worldW) c.x = -c.w;
            _clouds[i] = c;
        }
    }

    public int GetTile(int tx, int ty)
    {
        if (tx < 0 || tx >= Width) return Constants.TileBedrock;
        if (ty < 0) return Constants.TileAir;
        if (ty >= Height) return Constants.TileBedrock;
        return Grid[tx, ty];
    }

    public void SetTile(int tx, int ty, int value)
    {
        if (tx >= 0 && tx < Width && ty >= 0 && ty < Height)
            if (Grid[tx, ty] != Constants.TileBedrock)
                Grid[tx, ty] = value;
    }

    public bool IsSolid(int tx, int ty)
    {
        int t = GetTile(tx, ty);
        return t != Constants.TileAir && t != Constants.TileCage && t != Constants.TileTorch;
    }

    public List<Rectangle> CheckTileCollision(Rectangle rect)
    {
        var result = new List<Rectangle>();
        int x0 = Math.Max(0, (int)(rect.X / Constants.TileSize));
        int x1 = Math.Min(Width, (int)((rect.X + rect.Width) / Constants.TileSize) + 1);
        int y0 = Math.Max(0, (int)(rect.Y / Constants.TileSize));
        int y1 = Math.Min(Height, (int)((rect.Y + rect.Height) / Constants.TileSize) + 1);
        for (int tx = x0; tx < x1; tx++)
        for (int ty = y0; ty < y1; ty++)
            if (IsSolid(tx, ty))
            {
                var tr = new Rectangle(tx * Constants.TileSize, ty * Constants.TileSize, Constants.TileSize, Constants.TileSize);
                if (Raylib.CheckCollisionRecs(rect, tr)) result.Add(tr);
            }
        return result;
    }

    public void Draw(float camX, float camY, float zoom)
    {
        int sw = Constants.ScreenWidth;
        int sh = Constants.ScreenHeight;
        int ts = (int)(Constants.TileSize * zoom);

        // Sky
        int skyLimitY = (int)((Constants.SurfaceY + 1) * Constants.TileSize * zoom - camY);
        if (skyLimitY > 0)
        {
            Raylib.DrawRectangle(0, 0, sw, Math.Min(sh, skyLimitY), new Color(100, 180, 240, 255));
            // Sun
            int sunX = (int)(100 * Constants.TileSize * zoom - camX * 0.3f);
            int sunY = (int)(8 * Constants.TileSize * zoom - camY * 0.3f);
            int sunR = (int)(36 * zoom);
            if (sunX > -sunR && sunX < sw + sunR && sunY > -sunR && sunY < sh + sunR)
            {
                Raylib.DrawCircle(sunX, sunY, sunR * 1.35f, new Color(255, 255, 210, 80));
                Raylib.DrawCircle(sunX, sunY, sunR * 1.15f, new Color(255, 245, 180, 120));
                Raylib.DrawCircle(sunX, sunY, sunR, new Color(255, 220, 60, 255));
                for (int ang = 0; ang < 360; ang += 40)
                {
                    float rad = ang * MathF.PI / 180f;
                    int x1 = (int)(sunX + MathF.Cos(rad) * sunR * 1.15f);
                    int y1 = (int)(sunY + MathF.Sin(rad) * sunR * 1.15f);
                    int x2 = (int)(sunX + MathF.Cos(rad) * sunR * 1.5f);
                    int y2 = (int)(sunY + MathF.Sin(rad) * sunR * 1.5f);
                    Raylib.DrawLine(x1, y1, x2, y2, new Color(255, 220, 60, 200));
                }
            }
            // Clouds
            foreach (var (cx, cy, _, cw, ch) in _clouds)
            {
                int dcx = (int)(cx * zoom - camX * 0.5f);
                int dcy = (int)(cy * zoom - camY * 0.5f);
                int dcw = (int)(cw * zoom);
                int dch = (int)(ch * zoom);
                if (dcx > -dcw && dcx < sw)
                {
                    Raylib.DrawEllipse(dcx + dcw / 2, dcy + dch / 2, dcw / 2f, dch / 2f, new Color(248, 252, 255, 255));
                    Raylib.DrawEllipse(dcx + dcw / 2 + (int)(6 * zoom), dcy + dch / 2 - (int)(3 * zoom), dcw * 0.38f, dch * 0.4f, new Color(255, 255, 255, 255));
                }
            }
        }

        // Tiles
        int startX = Math.Max(0, (int)(camX / ts));
        int endX = Math.Min(Width, (int)((camX + sw) / ts) + 1);
        int startY = Math.Max(0, (int)(camY / ts));
        int endY = Math.Min(Height, (int)((camY + sh) / ts) + 1);

        for (int tx = startX; tx < endX; tx++)
        for (int ty = startY; ty < endY; ty++)
        {
            int tile = Grid[tx, ty];
            if (tile == Constants.TileAir) continue;

            int dx = (int)(tx * ts - camX);
            int dy = (int)(ty * ts - camY);

            Color baseCol = tile switch
            {
                Constants.TileDirt     => new Color(110, 72, 42, 255),
                Constants.TileStone    => new Color(95, 95, 100, 255),
                Constants.TileIron     => new Color(140, 115, 90, 255),
                Constants.TileGold     => new Color(200, 175, 55, 255),
                Constants.TileCoal     => new Color(38, 38, 40, 255),
                Constants.TileGrass    => new Color(50, 155, 50, 255),
                Constants.TileBedrock  => new Color(18, 18, 20, 255),
                Constants.TileCage     => new Color(190, 150, 35, 255),
                Constants.TileTorch    => new Color(80, 55, 25, 255),
                _                      => Color.Magenta
            };

            Raylib.DrawRectangle(dx, dy, ts, ts, baseCol);

            // Tile edge shadow (right and bottom darker strip for depth)
            Raylib.DrawRectangle(dx + ts - 2, dy, 2, ts, new Color(0, 0, 0, 50));
            Raylib.DrawRectangle(dx, dy + ts - 2, ts, 2, new Color(0, 0, 0, 50));
            // Tile top/left highlight
            Raylib.DrawRectangle(dx, dy, ts, 1, new Color(255, 255, 255, 25));
            Raylib.DrawRectangle(dx, dy, 1, ts, new Color(255, 255, 255, 25));

            int ss = Math.Max(1, (int)(3 * zoom));

            switch (tile)
            {
                case Constants.TileGrass:
                    Raylib.DrawRectangle(dx, dy, ts, (int)(3 * zoom), new Color(90, 210, 60, 255));
                    Raylib.DrawRectangle(dx, dy, ts, 1, new Color(120, 240, 80, 255));
                    break;
                case Constants.TileCoal:
                    Raylib.DrawRectangle(dx + (int)(4 * zoom), dy + (int)(3 * zoom), ss + 1, ss + 1, new Color(5, 5, 5, 255));
                    Raylib.DrawRectangle(dx + (int)(9 * zoom), dy + (int)(9 * zoom), ss, ss, new Color(5, 5, 5, 255));
                    Raylib.DrawRectangle(dx + (int)(6 * zoom), dy + (int)(7 * zoom), ss - 1, ss - 1, new Color(20, 20, 20, 255));
                    break;
                case Constants.TileIron:
                    Raylib.DrawRectangle(dx + (int)(3 * zoom), dy + (int)(2 * zoom), ss + 1, ss + 1, new Color(230, 140, 70, 255));
                    Raylib.DrawRectangle(dx + (int)(9 * zoom), dy + (int)(9 * zoom), ss, ss, new Color(210, 120, 55, 255));
                    Raylib.DrawRectangle(dx + (int)(6 * zoom), dy + (int)(5 * zoom), ss - 1, ss - 1, new Color(200, 100, 40, 255));
                    break;
                case Constants.TileGold:
                    Raylib.DrawRectangle(dx + (int)(3 * zoom), dy + (int)(4 * zoom), ss + 2, ss + 2, new Color(255, 220, 10, 255));
                    Raylib.DrawRectangle(dx + (int)(9 * zoom), dy + (int)(2 * zoom), ss + 1, ss + 1, new Color(255, 210, 20, 255));
                    Raylib.DrawRectangle(dx + (int)(7 * zoom), dy + (int)(8 * zoom), ss, ss, new Color(240, 195, 10, 255));
                    // Gold sparkle
                    Raylib.DrawRectangle(dx + (int)(11 * zoom), dy + (int)(5 * zoom), 1, 1, new Color(255, 255, 200, 255));
                    break;
                case Constants.TileCage:
                    Raylib.DrawRectangleLines(dx, dy, ts, ts, new Color(120, 120, 130, 255));
                    for (int bar = 3; bar < 16; bar += 4)
                        Raylib.DrawLine(dx + (int)(bar * zoom), dy, dx + (int)(bar * zoom), dy + ts, new Color(140, 140, 150, 200));
                    Raylib.DrawCircle(dx + ts / 2, dy + ts / 2, (int)(3 * zoom), new Color(255, 220, 100, 255));
                    break;
                case Constants.TileTorch:
                    // Torch stick
                    Raylib.DrawRectangle(dx + ts / 2 - 1, dy + (int)(6 * zoom), 2, (int)(10 * zoom), new Color(100, 65, 30, 255));
                    // Animated flame using time
                    float flicker = MathF.Sin((float)Raylib.GetTime() * 12f + tx) * 1.5f;
                    Raylib.DrawCircle(dx + ts / 2 + (int)flicker, dy + (int)(4 * zoom), (int)(3.5f * zoom), new Color(255, 130, 20, 255));
                    Raylib.DrawCircle(dx + ts / 2 + (int)flicker, dy + (int)(4 * zoom), (int)(1.8f * zoom), new Color(255, 240, 100, 255));
                    break;
            }
        }

        // Draw structures
        foreach (var s in Structures)
        {
            int dx = (int)(s.Tx * ts - camX);
            int dy = (int)(s.Ty * ts - camY);
            int wp = (int)(48 * zoom);
            int hp = (int)(36 * zoom);
            if (dx < -wp || dx > sw) continue;

            switch (s.Type)
            {
                case "HOUSE":
                    // Log cabin walls
                    Raylib.DrawRectangle(dx, dy + (int)(10 * zoom), wp, hp - (int)(10 * zoom), new Color(130, 82, 38, 255));
                    // Roof polygon
                    var roofPts = new Vector2[]
                    {
                        new(dx - (int)(4 * zoom), dy + (int)(10 * zoom)),
                        new(dx + wp / 2, dy - (int)(5 * zoom)),
                        new(dx + wp + (int)(4 * zoom), dy + (int)(10 * zoom))
                    };
                    Raylib.DrawTriangle(roofPts[0], roofPts[1], roofPts[2], new Color(160, 38, 38, 255));
                    // Door
                    Raylib.DrawRectangle(dx + (int)(14 * zoom), dy + hp - (int)(16 * zoom), (int)(10 * zoom), (int)(16 * zoom), new Color(85, 48, 18, 255));
                    // Window with glow
                    Raylib.DrawRectangle(dx + (int)(28 * zoom), dy + (int)(14 * zoom), (int)(10 * zoom), (int)(8 * zoom), new Color(255, 220, 100, 255));
                    Raylib.DrawRectangleLines(dx + (int)(28 * zoom), dy + (int)(14 * zoom), (int)(10 * zoom), (int)(8 * zoom), new Color(55, 35, 15, 255));
                    break;

                case "FORGE":
                    // Stone body
                    Raylib.DrawRectangle(dx, dy + (int)(8 * zoom), wp, hp - (int)(8 * zoom), new Color(85, 85, 92, 255));
                    // Chimney
                    Raylib.DrawRectangle(dx + (int)(6 * zoom), dy - (int)(4 * zoom), (int)(10 * zoom), (int)(12 * zoom), new Color(65, 65, 70, 255));
                    // Fire opening
                    Raylib.DrawRectangle(dx + (int)(22 * zoom), dy + hp - (int)(19 * zoom), (int)(16 * zoom), (int)(19 * zoom), new Color(25, 25, 25, 255));
                    // Animated fire in forge
                    float fh = (8 + MathF.Sin((float)Raylib.GetTime() * 6f) * 3) * zoom;
                    Raylib.DrawRectangle(dx + (int)(25 * zoom), (int)(dy + hp - fh), (int)(10 * zoom), (int)fh, new Color(255, 140, 0, 255));
                    Raylib.DrawRectangle(dx + (int)(28 * zoom), (int)(dy + hp - fh * 0.6f), (int)(4 * zoom), (int)(fh * 0.6f), new Color(255, 230, 50, 255));
                    // Anvil
                    Raylib.DrawRectangle(dx + (int)(4 * zoom), dy + hp - (int)(10 * zoom), (int)(14 * zoom), (int)(6 * zoom), new Color(45, 45, 50, 255));
                    Raylib.DrawRectangle(dx + (int)(7 * zoom), dy + hp - (int)(4 * zoom), (int)(8 * zoom), (int)(4 * zoom), new Color(40, 40, 45, 255));
                    break;

                case "LIBRARY":
                    // Wooden walls
                    Raylib.DrawRectangle(dx, dy + (int)(10 * zoom), wp, hp - (int)(10 * zoom), new Color(195, 155, 105, 255));
                    // Blue roof
                    var libRoof = new Vector2[]
                    {
                        new(dx - (int)(2 * zoom), dy + (int)(10 * zoom)),
                        new(dx + wp / 2, dy - (int)(2 * zoom)),
                        new(dx + wp + (int)(2 * zoom), dy + (int)(10 * zoom))
                    };
                    Raylib.DrawTriangle(libRoof[0], libRoof[1], libRoof[2], new Color(38, 75, 145, 255));
                    // Books window
                    Raylib.DrawRectangle(dx + (int)(8 * zoom), dy + (int)(14 * zoom), (int)(18 * zoom), (int)(14 * zoom), new Color(75, 48, 28, 255));
                    for (int by = 16; by < 28; by += 4)
                        Raylib.DrawLine(dx + (int)(9 * zoom), dy + (int)(by * zoom), dx + (int)(24 * zoom), dy + (int)(by * zoom), new Color(215, 95, 45, 200));
                    // Scroll sign
                    Raylib.DrawRectangle(dx + (int)(28 * zoom), dy + (int)(14 * zoom), (int)(12 * zoom), (int)(7 * zoom), new Color(245, 220, 175, 255));
                    Raylib.DrawRectangleLines(dx + (int)(28 * zoom), dy + (int)(14 * zoom), (int)(12 * zoom), (int)(7 * zoom), new Color(0, 0, 0, 180));
                    break;
            }
        }
    }

    public void DrawLighting(float camX, float camY, float zoom,
        float playerWorldX, float playerWorldY,
        bool waterShieldActive, List<(float x, float y)> spitPositions)
    {
        int sw = Constants.ScreenWidth;
        int sh = Constants.ScreenHeight;
        int ts = (int)(Constants.TileSize * zoom);

        // Only apply darkness for cave area
        int skyLimit = (int)((Constants.SurfaceY + 1) * Constants.TileSize * zoom - camY);
        if (skyLimit >= sh) return; // fully in sky, no lighting needed

        // Draw black overlay on cave portion
        int caveTop = Math.Max(0, skyLimit);
        // Use layered alpha darkness
        Raylib.DrawRectangle(0, caveTop, sw, sh - caveTop, new Color(0, 0, 8, 210));

        // Player light
        float psx = playerWorldX * zoom - camX;
        float psy = playerWorldY * zoom - camY;
        int prad = (int)(165 * zoom);

        // Draw decreasing-opacity rings outward from player to simulate a soft light
        for (int ring = prad; ring > 0; ring -= Math.Max(1, prad / 30))
        {
            float alpha = 210f * (1f - (float)ring / prad);
            Raylib.DrawCircle((int)psx, (int)psy, ring, new Color(0, 0, 8, (int)(210 - alpha)));
        }
        // Fully clear center
        Raylib.DrawCircle((int)psx, (int)psy, (int)(40 * zoom), new Color(0, 0, 0, 0));

        // Torch lights
        int startX = Math.Max(0, (int)(camX / ts));
        int endX = Math.Min(Width, (int)((camX + sw) / ts) + 1);
        int startY = Math.Max(0, (int)(camY / ts));
        int endY = Math.Min(Height, (int)((camY + sh) / ts) + 1);

        for (int tx = startX; tx < endX; tx++)
        for (int ty = startY; ty < endY; ty++)
        {
            if (Grid[tx, ty] != Constants.TileTorch) continue;
            float trad = 90f * zoom;
            float flicker = MathF.Sin((float)Raylib.GetTime() * 10f + tx * 2.3f) * 6 * zoom;
            float tcx = tx * ts + ts / 2f - camX;
            float tcy = ty * ts + ts / 2f - camY;
            for (int ring = (int)(trad + flicker); ring > 0; ring -= Math.Max(1, (int)(trad / 20)))
            {
                float alpha = 200f * (1f - ring / (trad + flicker));
                Raylib.DrawCircle((int)tcx, (int)tcy, ring, new Color(0, 0, 8, (int)(200 - alpha)));
            }
        }

        // Water shield glow
        if (waterShieldActive)
        {
            for (int ring = prad + 60; ring > prad; ring -= 4)
            {
                float alpha = 60f * (1f - (float)(ring - prad) / 60f);
                Raylib.DrawCircle((int)psx, (int)psy, ring, new Color(0, 0, 8, (int)(60 - alpha)));
            }
        }
    }
}
