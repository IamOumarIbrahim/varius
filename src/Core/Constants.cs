// src/Core/Constants.cs
namespace Varius.Core;

public static class Constants
{
    public const int ScreenWidth = 1280;
    public const int ScreenHeight = 768;
    public const string Title = "Varius - Cave Survivor";
    public const int TargetFPS = 165;

    // World
    public const int TileSize = 16;
    public const int WorldWidth = 200;
    public const int WorldHeight = 100;
    public const int SurfaceY = 25;  // tiles — sky above, caves below

    // Player
    public const int PlayerWidth = 14;
    public const int PlayerHeight = 26;
    public const float Gravity = 900f;
    public const float MaxFallSpeed = 520f;
    public const float JumpForce = -320f;
    public const float WalkSpeed = 185f;
    
    // Camera smooth factor
    public const float CameraSmooth = 8.0f;

    // Tile IDs
    public const int TileAir = 0;
    public const int TileDirt = 1;
    public const int TileStone = 2;
    public const int TileIron = 3;
    public const int TileGold = 4;
    public const int TileCoal = 5;
    public const int TileGrass = 6;
    public const int TileBedrock = 7;
    public const int TileCage = 10;
    public const int TileTorch = 15;
}
