// src/Core/InputManager.cs
using Raylib_cs;
using System.Numerics;

namespace Varius.Core;

public static class InputManager
{
    public static bool Left => Raylib.IsKeyDown(KeyboardKey.A) || Raylib.IsKeyDown(KeyboardKey.Left);
    public static bool Right => Raylib.IsKeyDown(KeyboardKey.D) || Raylib.IsKeyDown(KeyboardKey.Right);
    public static bool Up => Raylib.IsKeyDown(KeyboardKey.W) || Raylib.IsKeyDown(KeyboardKey.Up);
    public static bool Down => Raylib.IsKeyDown(KeyboardKey.S) || Raylib.IsKeyDown(KeyboardKey.Down);
    public static bool Jump => Raylib.IsKeyPressed(KeyboardKey.Space);
    public static bool Use => Raylib.IsKeyPressed(KeyboardKey.F);
    public static bool Block => Raylib.IsKeyDown(KeyboardKey.LeftShift) || Raylib.IsKeyDown(KeyboardKey.RightShift);
    public static bool Ultimate => Raylib.IsKeyPressed(KeyboardKey.Q) || Raylib.IsKeyPressed(KeyboardKey.E);
    public static bool Inventory => Raylib.IsKeyPressed(KeyboardKey.I);
    public static bool Camp => Raylib.IsKeyPressed(KeyboardKey.B);
    public static bool Town => Raylib.IsKeyPressed(KeyboardKey.T);
    public static bool Settings => Raylib.IsKeyPressed(KeyboardKey.O);
    public static bool Escape => Raylib.IsKeyPressed(KeyboardKey.Escape);
    public static bool Enter => Raylib.IsKeyPressed(KeyboardKey.Enter);

    public static int ToolbarSlot()
    {
        if (Raylib.IsKeyPressed(KeyboardKey.One)) return 0;
        if (Raylib.IsKeyPressed(KeyboardKey.Two)) return 1;
        if (Raylib.IsKeyPressed(KeyboardKey.Three)) return 2;
        if (Raylib.IsKeyPressed(KeyboardKey.Four)) return 3;
        if (Raylib.IsKeyPressed(KeyboardKey.Five)) return 4;
        if (Raylib.IsKeyPressed(KeyboardKey.Six)) return 5;
        return -1;
    }

    public static Vector2 MousePosition => Raylib.GetMousePosition();
    public static bool MouseLeft => Raylib.IsMouseButtonPressed(MouseButton.Left);
    public static bool MouseRight => Raylib.IsMouseButtonPressed(MouseButton.Right);
    public static int MouseWheelDelta => (int)Raylib.GetMouseWheelMove();

    // Direction based on held movement keys
    public static (int dx, int dy) GetActionDirection()
    {
        int dx = 0, dy = 0;
        if (Raylib.IsKeyDown(KeyboardKey.A) || Raylib.IsKeyDown(KeyboardKey.Left)) dx = -1;
        else if (Raylib.IsKeyDown(KeyboardKey.D) || Raylib.IsKeyDown(KeyboardKey.Right)) dx = 1;
        if (Raylib.IsKeyDown(KeyboardKey.W) || Raylib.IsKeyDown(KeyboardKey.Up)) dy = -1;
        else if (Raylib.IsKeyDown(KeyboardKey.S) || Raylib.IsKeyDown(KeyboardKey.Down)) dy = 1;
        return (dx, dy);
    }
}
