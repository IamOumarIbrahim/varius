// src/UI/UIManager.cs
using Raylib_cs;
using System.Numerics;
using Varius.Core;
using Varius.Entities;
using Varius.Data;
using Varius.World;

namespace Varius.UI;

public class UIManager
{
    // Floating loot notifications
    private readonly List<(string text, Color col, float lifetime, float x, float y)> _notifications = new();
    // Level up choices
    public string[]? LevelUpChoices { get; set; }
    // Settings state
    private float _masterVolume = 0.6f;
    private float _sfxVolume = 0.8f;
    private float _zoom = 1.5f;
    public float MasterVolume { get => _masterVolume; set => _masterVolume = value; }
    public float SfxVolume { get => _sfxVolume; set => _sfxVolume = value; }
    public float Zoom { get => _zoom; set => _zoom = value; }
    public bool GpuAccel { get; set; } = true;
    // Toolbar scroll
    private static readonly string[] SlotNames = { "PICKAXE", "KATANA", "BLOCK", "TORCH", "WATER", "WIND" };
    // Panel open state


    public void AddNotification(string text, Color col, float notifX, float notifY)
    {
        _notifications.Add((text, col, 2.2f, notifX, notifY));
    }

    public void Update(float dt)
    {
        for (int i = _notifications.Count - 1; i >= 0; i--)
        {
            var n = _notifications[i];
            n.lifetime -= dt;
            n.y -= 22f * dt;
            if (n.lifetime <= 0) _notifications.RemoveAt(i);
            else _notifications[i] = n;
        }
    }

    public void DrawHUD(Player player, float survivalTime)
    {
        int sw = Constants.ScreenWidth;
        int sh = Constants.ScreenHeight;

        // ── Health Bar (top left) ──────────────────────────────────────────
        float hpPct = (float)player.Health / player.Stats.MaxHealth;
        Raylib.DrawRectangle(15, 14, 186, 14, new Color(30, 8, 8, 210));
        Raylib.DrawRectangle(16, 15, 184, 12, new Color(55, 12, 12, 200));
        Raylib.DrawRectangle(16, 15, (int)(184 * hpPct), 12,
            hpPct > 0.5f ? new Color(50, 230, 80, 240) : hpPct > 0.25f ? new Color(255, 180, 30, 240) : new Color(240, 40, 40, 240));
        Raylib.DrawRectangleLines(15, 14, 186, 14, new Color(255, 255, 255, 80));
        Raylib.DrawText($"HP {player.Health}/{player.Stats.MaxHealth}", 22, 17, 8, Color.White);

        // ── Posture Bar ────────────────────────────────────────────────────
        float postPct = player.Posture / player.Stats.MaxPosture;
        Raylib.DrawRectangle(15, 30, 186, 8, new Color(25, 25, 8, 210));
        Raylib.DrawRectangle(16, 31, (int)(184 * postPct), 6, new Color(220, 220, 40, 230));
        Raylib.DrawRectangleLines(15, 30, 186, 8, new Color(255, 255, 255, 60));
        Raylib.DrawText($"PST {(int)(postPct * 100)}%", 22, 31, 7, new Color(220, 220, 140, 255));

        // ── XP Bar ────────────────────────────────────────────────────────
        float xpPct = (float)player.XP / player.XPToNext;
        Raylib.DrawRectangle(15, 40, 186, 5, new Color(10, 10, 40, 200));
        Raylib.DrawRectangle(15, 40, (int)(186 * xpPct), 5, new Color(80, 140, 255, 230));
        Raylib.DrawText($"LV{player.Level}  XP {player.XP}/{player.XPToNext}", 15, 47, 7, new Color(140, 200, 255, 255));

        // ── Survival Timer (top center) ────────────────────────────────────
        int min = (int)(survivalTime / 60), sec = (int)(survivalTime % 60);
        string timeStr = $"{min:00}:{sec:00}";
        Raylib.DrawText(timeStr, sw / 2 - Raylib.MeasureText(timeStr, 18) / 2, 12, 18, new Color(255, 230, 170, 255));

        // ── Stance indicator (top right) ────────────────────────────────────
        string stanceName = player.Stance.ToString().ToUpper() + " STANCE";
        Color stanceCol = player.Stance switch
        {
            Stance.Stone => new Color(200, 175, 130, 255),
            Stance.Water => new Color(60, 170, 255, 255),
            Stance.Wind  => new Color(100, 240, 160, 255),
            _            => Color.White
        };
        int stnW = Raylib.MeasureText(stanceName, 10);
        Raylib.DrawRectangle(sw - stnW - 22, 12, stnW + 16, 16, new Color(0, 0, 0, 140));
        Raylib.DrawText(stanceName, sw - stnW - 14, 16, 10, stanceCol);

        // ── Character name (top right below stance) ─────────────────────────
        string charName = player.CharDef.Name;
        int cnW = Raylib.MeasureText(charName, 9);
        Raylib.DrawText(charName, sw - cnW - 14, 31, 9, new Color(255, 215, 140, 200));

        // ── 6-slot Toolbar (bottom center) ─────────────────────────────────
        int slotSize = 46;
        int totalW = 6 * slotSize + 5 * 4;
        int tbX = sw / 2 - totalW / 2;
        int tbY = sh - slotSize - 10;

        for (int i = 0; i < 6; i++)
        {
            int slotX = tbX + i * (slotSize + 4);
            bool active = player.ActiveSlot == i;
            var bgCol = active ? new Color(60, 55, 45, 235) : new Color(20, 20, 20, 190);
            var borderCol = active ? new Color(255, 200, 60, 255) : new Color(80, 80, 80, 200);

            // Slot background
            Raylib.DrawRectangle(slotX, tbY, slotSize, slotSize, bgCol);
            Raylib.DrawRectangleLines(slotX, tbY, slotSize, slotSize, borderCol);

            // Inner highlight
            if (active)
            {
                Raylib.DrawRectangle(slotX + 1, tbY + 1, slotSize - 2, 3, new Color(255, 220, 100, 60));
            }

            // Tool icon (procedural)
            DrawToolIcon(slotX + 4, tbY + 4, slotSize - 8, SlotNames[i]);

            // Slot key label
            Raylib.DrawText((i + 1).ToString(), slotX + 3, tbY + slotSize - 10, 8, new Color(200, 200, 200, 180));

            // Slot tool name
            if (active)
            {
                string toolName = SlotNames[i];
                int tnW = Raylib.MeasureText(toolName, 7);
                Raylib.DrawText(toolName, slotX + slotSize / 2 - tnW / 2, tbY - 12, 7, new Color(255, 220, 100, 255));
            }
        }

        // ── Equipped items (bottom left) ────────────────────────────────────
        DrawEquippedItems(player, 15, sh - 160);

        // ── Floating notifications ──────────────────────────────────────────
        foreach (var n in _notifications)
        {
            float alpha = Math.Clamp(n.lifetime / 2.2f, 0, 1);
            int nx = sw / 2 - Raylib.MeasureText(n.text, 11) / 2;
            int notifAlpha = (int)(alpha * 255);
            Raylib.DrawText(n.text, nx, (int)n.y, 11, new Color(n.col.R, n.col.G, n.col.B, (byte)notifAlpha));
        }

        // ── Key hints (small bottom right) ──────────────────────────────────
        string hints = "[I]nv  [B]uild  [T]own  [O]pts";
        int hintW = Raylib.MeasureText(hints, 8);
        Raylib.DrawText(hints, sw - hintW - 12, sh - 14, 8, new Color(180, 180, 180, 160));
    }

    private static void DrawToolIcon(int x, int y, int size, string tool)
    {
        int cx = x + size / 2, cy = y + size / 2;
        switch (tool)
        {
            case "PICKAXE":
                Raylib.DrawLine(cx - size / 3, cy + size / 3, cx + size / 3, cy - size / 3, new Color(180, 180, 190, 255));
                Raylib.DrawRectangle(cx - size / 6, cy - size / 3, size / 5, size / 4, new Color(160, 100, 50, 255));
                break;
            case "KATANA":
                Raylib.DrawLine(cx - size / 3, cy + size / 3, cx + size / 3, cy - size / 3, new Color(200, 215, 240, 255));
                Raylib.DrawLine(cx - size / 4, cy + size / 4, cx - size / 3, cy + size / 3, new Color(120, 65, 20, 255));
                break;
            case "BLOCK":
                Raylib.DrawRectangle(cx - size / 4, cy - size / 4, size / 2, size / 2, new Color(110, 70, 40, 255));
                Raylib.DrawRectangleLines(cx - size / 4, cy - size / 4, size / 2, size / 2, new Color(180, 140, 90, 180));
                break;
            case "TORCH":
                Raylib.DrawRectangle(cx - 2, cy, 4, size / 3, new Color(100, 65, 30, 255));
                float flicker = MathF.Sin((float)Raylib.GetTime() * 10f) * 2f;
                Raylib.DrawCircle(cx + (int)flicker, cy - 2, size / 7, new Color(255, 140, 20, 255));
                Raylib.DrawCircle(cx + (int)flicker, cy - 2, size / 14, new Color(255, 240, 100, 255));
                break;
            case "WATER":
                Raylib.DrawCircle(cx, cy, size / 4, new Color(40, 100, 240, 200));
                Raylib.DrawRingLines(new Vector2(cx, cy), size / 6f, size / 4f, 180, 360, 16, new Color(100, 180, 255, 255));
                break;
            case "WIND":
                Raylib.DrawLine(cx - size / 3, cy - size / 8, cx + size / 3, cy - size / 8, new Color(100, 230, 160, 255));
                Raylib.DrawLine(cx - size / 3, cy + size / 8, cx + size / 4, cy + size / 8, new Color(80, 200, 140, 255));
                break;
        }
    }

    private static void DrawEquippedItems(Player player, int x, int y)
    {
        string[] labels = { "HEAD", "RING", "CAPE" };
        var slots = new[] { ItemSlot.Helmet, ItemSlot.Ring, ItemSlot.Cape };
        for (int i = 0; i < 3; i++)
        {
            var item = player.Equipped[slots[i]];
            int iy = y + i * 48;
            Raylib.DrawRectangle(x, iy, 130, 42, new Color(15, 15, 18, 190));
            Raylib.DrawRectangleLines(x, iy, 130, 42, new Color(80, 80, 90, 180));
            Raylib.DrawText(labels[i], x + 5, iy + 4, 8, new Color(160, 160, 180, 200));
            if (item != null)
            {
                Raylib.DrawRectangle(x + 4, iy + 14, 10, 10, item.RarityColor);
                Raylib.DrawText(item.Name.Length > 16 ? item.Name[..16] + ".." : item.Name, x + 18, iy + 15, 7, item.RarityColor);
            }
            else
            {
                Raylib.DrawText("(empty)", x + 18, iy + 15, 7, new Color(100, 100, 110, 200));
            }
        }
    }

    // ── Main Menu ────────────────────────────────────────────────────────────
    public int DrawMainMenu(bool[] slots)
    {
        int sw = Constants.ScreenWidth;
        int sh = Constants.ScreenHeight;
        float t = (float)Raylib.GetTime();

        // Background
        Raylib.DrawRectangle(0, 0, sw, sh, new Color(8, 8, 14, 255));

        // Animated stars
        for (int i = 0; i < 80; i++)
        {
            int sx2 = (i * 137 + 23) % sw;
            int sy2 = (i * 97 + 47) % sh;
            float twinkle = 0.5f + 0.5f * MathF.Sin(t * (0.5f + i * 0.08f) + i);
            Raylib.DrawPixel(sx2, sy2, new Color(255, 255, 255, (int)(twinkle * 200)));
        }

        // Logo "VARIUS" — big pixelized 3D-style title
        DrawVariusLogo(sw / 2, 140, t);

        // Subtitle
        string sub = "Cave Survivor";
        Raylib.DrawText(sub, sw / 2 - Raylib.MeasureText(sub, 16) / 2, 228, 16, new Color(200, 175, 120, 200));

        // ── Save slots ────────────────────────────────────────────────────────
        string[] options = { "NEW GAME", "CONTINUE", "SETTINGS", "QUIT" };
        string[] subtexts =
        {
            "Start a fresh adventure",
            slots[0] ? "Load save slot 1" : "No save found",
            "Audio, controls, display",
            "Exit to desktop"
        };
        int clicked = -1;
        int btnW = 320, btnH = 50, btnSpacY = 64;
        int btnStartY = 295;

        for (int i = 0; i < options.Length; i++)
        {
            int bx = sw / 2 - btnW / 2;
            int by = btnStartY + i * btnSpacY;
            var mouse = Raylib.GetMousePosition();
            bool hover = mouse.X >= bx && mouse.X < bx + btnW && mouse.Y >= by && mouse.Y < by + btnH;

            // Button glow on hover
            if (hover) Raylib.DrawRectangle(bx - 3, by - 3, btnW + 6, btnH + 6, new Color(255, 200, 60, 30));

            // Button body
            var btnBg = hover
                ? new Color(50, 44, 35, 235)
                : new Color(18, 18, 24, 215);
            Raylib.DrawRectangle(bx, by, btnW, btnH, btnBg);

            // Accent bar left
            Raylib.DrawRectangle(bx, by, 4, btnH, hover ? new Color(255, 200, 60, 255) : new Color(80, 80, 100, 200));
            Raylib.DrawRectangleLines(bx, by, btnW, btnH, hover ? new Color(255, 200, 60, 200) : new Color(60, 60, 80, 180));

            // Label
            int tw = Raylib.MeasureText(options[i], 16);
            var labelCol = i == 1 && !slots[0] ? new Color(100, 100, 110, 200) : (hover ? new Color(255, 215, 60, 255) : Color.White);
            Raylib.DrawText(options[i], bx + 18, by + 10, 16, labelCol);

            // Subtext
            Raylib.DrawText(subtexts[i], bx + 18, by + 30, 9, new Color(180, 180, 200, 180));

            if (hover && Raylib.IsMouseButtonPressed(MouseButton.Left))
                clicked = i;
        }

        // Version
        Raylib.DrawText("v beta0.3  |  C# + Raylib", 10, sh - 18, 9, new Color(100, 100, 120, 180));

        return clicked;
    }

    private static void DrawVariusLogo(int cx, int cy, float t)
    {
        // Each letter as thick 3D pixel blocks
        string logoText = "VARIUS";
        int letterSpacing = 62;
        int totalW = (logoText.Length - 1) * letterSpacing;
        int startX = cx - totalW / 2;
        int depth = 5;
        int fontSize = 56;

        // 3D shadow layer
        for (int d = depth; d > 0; d--)
        {
            var shadowCol = new Color((byte)(20 + d * 6), (byte)(16 + d * 4), (byte)(5 + d * 2), (byte)(180 + d * 8));
            Raylib.DrawText(logoText,
                startX - Raylib.MeasureText(logoText, fontSize) / 2 + d + (int)(MathF.Sin(t * 0.8f) * 2f),
                cy - fontSize / 2 + d,
                fontSize, shadowCol);
        }

        // Primary colored text (gradient per character)
        Color[] charCols =
        {
            new Color(255, 180, 30, 255),
            new Color(255, 140, 20, 255),
            new Color(255, 100, 20, 255),
            new Color(240, 80, 30, 255),
            new Color(255, 120, 20, 255),
            new Color(255, 175, 30, 255)
        };

        int lx = startX - Raylib.MeasureText(logoText, fontSize) / 2;
        for (int i = 0; i < logoText.Length; i++)
        {
            string letter = logoText[i].ToString();
            float bob = MathF.Sin(t * 2.2f + i * 0.7f) * 3.5f;
            var c = charCols[i];
            Raylib.DrawText(letter, lx + (int)(MathF.Sin(t * 0.8f + i) * 1.5f), cy - fontSize / 2 + (int)bob, fontSize, c);
            lx += Raylib.MeasureText(letter, fontSize) + 2;
        }
    }

    // ── Character Select ─────────────────────────────────────────────────────
    public int DrawCharacterSelect(ref int hoverIndex, ref int scrollOffset)
    {
        int sw = Constants.ScreenWidth;
        int sh = Constants.ScreenHeight;

        Raylib.DrawRectangle(0, 0, sw, sh, new Color(10, 10, 18, 255));
        Raylib.DrawText("SELECT CHARACTER", sw / 2 - Raylib.MeasureText("SELECT CHARACTER", 22) / 2, 18, 22, new Color(255, 215, 60, 255));
        Raylib.DrawText("[ESC] Back  |  Click to select  |  [Scroll] to navigate", sw / 2 - 200, sh - 20, 9, new Color(180, 180, 200, 200));

        int cols = 5, cardW = 128, cardH = 170, padX = 22, padY = 22;
        int totalW = cols * (cardW + padX) - padX;
        int gridX = sw / 2 - totalW / 2;
        int gridY = 62;

        var chars = CharactersDB.All;
        var mouse = Raylib.GetMousePosition();
        int selected = -1;

        int scroll = InputManager.MouseWheelDelta;
        if (scroll != 0) scrollOffset = Math.Clamp(scrollOffset - scroll, 0, Math.Max(0, (chars.Length / cols) * (cardH + padY) - sh + 120));

        hoverIndex = -1;

        // Draw group labels & cards
        int idx = 0;
        foreach (var (groupName, indices) in CharactersDB.Groups)
        {
            // Group label
            int row = idx / cols;
            int labelY = gridY + row * (cardH + padY) - scrollOffset - 18;
            if (labelY >= 50 && labelY < sh)
            {
                Raylib.DrawRectangle(gridX, labelY, totalW, 16, new Color(30, 25, 15, 160));
                Raylib.DrawText(groupName, gridX + 8, labelY + 2, 10, new Color(255, 200, 80, 255));
            }

            foreach (int charIdx in indices)
            {
                int col = idx % cols;
                row = idx / cols;
                int cx = gridX + col * (cardW + padX);
                int cy = gridY + row * (cardH + padY) - scrollOffset;
                if (cy < -cardH || cy > sh + 20) { idx++; continue; }

                var cdef = chars[charIdx];
                bool hover = mouse.X >= cx && mouse.X < cx + cardW && mouse.Y >= cy && mouse.Y < cy + cardH;
                if (hover) hoverIndex = charIdx;

                // Card background
                Raylib.DrawRectangle(cx, cy, cardW, cardH, new Color(18, 18, 26, 230));
                if (hover) Raylib.DrawRectangle(cx, cy, cardW, cardH, new Color(255, 200, 60, 25));
                Raylib.DrawRectangleLines(cx, cy, cardW, cardH, hover ? new Color(255, 200, 60, 220) : new Color(55, 55, 70, 200));

                // Origin tag
                string originShort = cdef.Origin.Length > 18 ? cdef.Origin[..18] : cdef.Origin;
                Raylib.DrawText(originShort, cx + 4, cy + 4, 7, new Color(140, 140, 180, 200));

                // Character preview sprite (centered)
                DrawCharacterPreviewSprite(cx + cardW / 2, cy + 56, cdef.Theme, 2.5f);

                // Name
                string name = cdef.Name;
                int nw = Raylib.MeasureText(name, 9);
                if (nw > cardW - 8) name = name[..(name.Length - 3)] + "..";
                Raylib.DrawText(name, cx + cardW / 2 - Raylib.MeasureText(name, 9) / 2, cy + 104, 9, new Color(255, 230, 160, 255));

                // Stats mini-bars
                DrawStatBars(cx + 6, cy + 118, cardW - 12, cdef.Stats);

                // Click
                if (hover && Raylib.IsMouseButtonPressed(MouseButton.Left))
                    selected = charIdx;

                idx++;
            }
        }

        // Right panel: details for hovered character
        if (hoverIndex >= 0)
        {
            var c = chars[hoverIndex];
            int px = sw - 290, py = 60;
            Raylib.DrawRectangle(px - 10, py - 10, 290, sh - py - 30, new Color(12, 12, 20, 230));
            Raylib.DrawRectangleLines(px - 10, py - 10, 290, sh - py - 30, new Color(60, 60, 80, 200));
            Raylib.DrawText(c.Name, px, py, 16, new Color(255, 215, 60, 255));
            Raylib.DrawText(c.Origin, px, py + 22, 10, new Color(180, 180, 220, 220));
            Raylib.DrawText("Weapon: " + c.StartingWeapon, px, py + 44, 9, new Color(200, 230, 200, 255));
            Raylib.DrawText("── ABILITY ──", px, py + 62, 9, new Color(255, 160, 40, 255));
            Raylib.DrawText(c.UniqueAbility.Name, px, py + 76, 10, new Color(255, 215, 120, 255));
            // Wrap ability description
            WrapText(c.UniqueAbility.Description, px, py + 92, 260, 8, new Color(210, 210, 240, 220), 14);
            Raylib.DrawText("── CRAFT BONUS ──", px, py + 160, 9, new Color(100, 220, 160, 255));
            WrapText(c.CraftingBonus, px, py + 175, 265, 8, new Color(180, 240, 200, 220), 14);
            // Stats
            Raylib.DrawText("── STATS ──", px, py + 240, 9, new Color(140, 180, 255, 255));
            DrawDetailedStats(px, py + 255, c.Stats);
        }

        return selected;
    }

    private static void DrawCharacterPreviewSprite(int cx, int cy, CharacterTheme theme, float scale)
    {
        int headW = (int)(8 * scale), headH = (int)(8 * scale);
        int torsoH = (int)(10 * scale), legsH = (int)(8 * scale);
        int w = (int)(14 * scale), h = (int)(26 * scale);
        int sx = cx - w / 2, sy = cy - h / 2;

        // Legs
        Raylib.DrawRectangle(sx + (int)(2 * scale), sy + headH + torsoH, (int)(4 * scale), legsH, theme.Pants);
        Raylib.DrawRectangle(sx + (int)(8 * scale), sy + headH + torsoH, (int)(4 * scale), legsH, theme.Pants);
        // Shoes
        var shoeCol = new Color((byte)Math.Max(0, theme.Pants.R - 30), (byte)Math.Max(0, theme.Pants.G - 30), (byte)Math.Max(0, theme.Pants.B - 30), (byte)255);
        Raylib.DrawRectangle(sx + (int)(1 * scale), sy + headH + torsoH + legsH - (int)(2 * scale), (int)(5 * scale), (int)(2 * scale), shoeCol);
        Raylib.DrawRectangle(sx + (int)(8 * scale), sy + headH + torsoH + legsH - (int)(2 * scale), (int)(5 * scale), (int)(2 * scale), shoeCol);
        // Torso
        Raylib.DrawRectangle(sx + (int)(1 * scale), sy + headH, (int)(12 * scale), torsoH, theme.Shirt);
        // Shirt top highlight
        Raylib.DrawRectangle(sx + (int)(2 * scale), sy + headH, (int)(10 * scale), 1, new Color(255, 255, 255, 40));
        // Arms
        int armW = (int)(3 * scale), armH = (int)(7 * scale);
        Raylib.DrawRectangle(sx, sy + headH, armW, armH, theme.Shirt);
        Raylib.DrawRectangle(sx + w - armW, sy + headH, armW, armH, theme.Shirt);
        // Hands
        Raylib.DrawRectangle(sx, sy + headH + armH - (int)(2 * scale), armW, (int)(2 * scale), theme.Skin);
        Raylib.DrawRectangle(sx + w - armW, sy + headH + armH - (int)(2 * scale), armW, (int)(2 * scale), theme.Skin);
        // Head
        int headOff = (w - headW) / 2;
        Raylib.DrawRectangle(sx + headOff, sy, headW, headH, theme.Skin);
        // Hair
        Raylib.DrawRectangle(sx + headOff, sy, headW, (int)(3 * scale), theme.Hair);
        // Eyes
        Raylib.DrawRectangle(sx + headOff + (int)(5 * scale), sy + (int)(2 * scale), (int)(2 * scale), (int)(2 * scale), theme.Eyes);
        // Eye highlight
        Raylib.DrawRectangle(sx + headOff + (int)(5 * scale), sy + (int)(2 * scale), 1, 1, new Color(255, 255, 255, 180));
        // Mouth
        Raylib.DrawRectangle(sx + headOff + (int)(2 * scale), sy + (int)(5 * scale), (int)(4 * scale), 1, new Color(180, 100, 100, 200));
        // Ponytail
        if (theme.HasPonytail)
            Raylib.DrawRectangle(sx + headOff - (int)(3 * scale), sy + (int)(1 * scale), (int)(3 * scale), (int)(6 * scale), theme.Hair);
        // Braids
        if (theme.HasBraids)
        {
            Raylib.DrawRectangle(sx + headOff - (int)(1 * scale), sy + headH - (int)(2 * scale), (int)(2 * scale), (int)(10 * scale), theme.Hair);
            Raylib.DrawRectangle(sx + headOff + headW - (int)(1 * scale), sy + headH - (int)(2 * scale), (int)(2 * scale), (int)(10 * scale), theme.Hair);
        }
        // Character outline
        Raylib.DrawRectangleLines(sx, sy, w, h, new Color(0, 0, 0, 100));
    }

    private static void DrawStatBars(int x, int y, int maxW, CharacterStats stats)
    {
        float maxHp = 200f, maxSpd = 1.6f, maxArm = 8f, maxMag = 5.5f;
        (string label, float val, float max, Color col)[] bars =
        {
            ("HP", stats.MaxHealth, maxHp, new Color(50, 220, 80, 255)),
            ("SP", stats.MoveSpeed, maxSpd, new Color(80, 180, 255, 255)),
            ("AR", stats.Armor, maxArm, new Color(220, 180, 80, 255)),
            ("MG", stats.MagnetRange, maxMag, new Color(180, 100, 255, 255))
        };
        int bh = 5;
        for (int i = 0; i < bars.Length; i++)
        {
            var (label, val, max, col) = bars[i];
            int by = y + i * (bh + 5);
            Raylib.DrawText(label, x, by - 1, 6, new Color(180, 180, 200, 200));
            Raylib.DrawRectangle(x + 14, by, maxW - 14, bh, new Color(30, 30, 40, 200));
            Raylib.DrawRectangle(x + 14, by, (int)((maxW - 14) * Math.Clamp(val / max, 0, 1)), bh, col);
        }
    }

    private static void DrawDetailedStats(int x, int y, CharacterStats stats)
    {
        var lines = new[]
        {
            ($"HP:          {stats.MaxHealth}", new Color(80, 240, 120, 255)),
            ($"Speed:    {stats.MoveSpeed:0.00}x", new Color(100, 180, 255, 255)),
            ($"Armor:     {stats.Armor}", new Color(255, 200, 80, 255)),
            ($"Magnet: {stats.MagnetRange:0.0}", new Color(200, 120, 255, 255))
        };
        for (int i = 0; i < lines.Length; i++)
            Raylib.DrawText(lines[i].Item1, x, y + i * 16, 10, lines[i].Item2);
    }

    // ── Level Up ─────────────────────────────────────────────────────────────
    public int DrawLevelUp(string[] choices)
    {
        int sw = Constants.ScreenWidth;
        int sh = Constants.ScreenHeight;

        // Dim overlay
        Raylib.DrawRectangle(0, 0, sw, sh, new Color(0, 0, 0, 150));

        // Panel
        int panW = 480, panH = 340;
        int px = sw / 2 - panW / 2, py = sh / 2 - panH / 2;
        Raylib.DrawRectangle(px, py, panW, panH, new Color(14, 14, 22, 240));
        Raylib.DrawRectangleLines(px, py, panW, panH, new Color(255, 200, 60, 220));

        Raylib.DrawText("LEVEL UP!", sw / 2 - Raylib.MeasureText("LEVEL UP!", 28) / 2, py + 18, 28, new Color(255, 200, 60, 255));
        Raylib.DrawText("Choose an upgrade:", sw / 2 - Raylib.MeasureText("Choose an upgrade:", 12) / 2, py + 56, 12, new Color(200, 200, 230, 230));

        var mouse = Raylib.GetMousePosition();
        int selected = -1;
        int btnH = 56, btnSpacY = 66;
        for (int i = 0; i < choices.Length; i++)
        {
            int bx = px + 24, by = py + 88 + i * btnSpacY;
            int bw = panW - 48;
            bool hover = mouse.X >= bx && mouse.X < bx + bw && mouse.Y >= by && mouse.Y < by + btnH;
            Raylib.DrawRectangle(bx, by, bw, btnH, hover ? new Color(50, 45, 30, 240) : new Color(22, 22, 30, 230));
            Raylib.DrawRectangle(bx, by, 4, btnH, new Color(255, 180, 40, 255));
            Raylib.DrawRectangleLines(bx, by, bw, btnH, hover ? new Color(255, 180, 40, 255) : new Color(60, 60, 80, 200));
            WrapText(choices[i], bx + 12, by + 10, bw - 20, 11, Color.White, 19);
            if (hover && Raylib.IsMouseButtonPressed(MouseButton.Left)) selected = i;
        }
        return selected;
    }

    // ── Inventory Panel ───────────────────────────────────────────────────────
    public void DrawInventory(Player player)
    {
        int sw = Constants.ScreenWidth;
        int sh = Constants.ScreenHeight;
        Raylib.DrawRectangle(0, 0, sw, sh, new Color(0, 0, 0, 160));

        int panW = 640, panH = 460;
        int px = sw / 2 - panW / 2, py = sh / 2 - panH / 2;
        Raylib.DrawRectangle(px, py, panW, panH, new Color(14, 14, 22, 245));
        Raylib.DrawRectangleLines(px, py, panW, panH, new Color(80, 80, 120, 255));
        Raylib.DrawText("INVENTORY", px + 14, py + 12, 18, new Color(255, 215, 60, 255));
        Raylib.DrawText("[ESC/I] Close  |  Click to equip", px + 14, py + panH - 18, 8, new Color(180, 180, 200, 200));

        // Equipped section
        Raylib.DrawText("Equipped", px + 14, py + 40, 10, new Color(200, 200, 240, 240));
        string[] slotLabels = { "HEAD", "RING", "CAPE" };
        var slots = new[] { ItemSlot.Helmet, ItemSlot.Ring, ItemSlot.Cape };
        var mouse = Raylib.GetMousePosition();
        for (int i = 0; i < 3; i++)
        {
            int ex = px + 14 + i * 140, ey = py + 56;
            var item = player.Equipped[slots[i]];
            bool hover = mouse.X >= ex && mouse.X < ex + 130 && mouse.Y >= ey && mouse.Y < ey + 46;
            Raylib.DrawRectangle(ex, ey, 130, 46, hover ? new Color(40, 35, 20, 240) : new Color(20, 20, 28, 230));
            Raylib.DrawRectangleLines(ex, ey, 130, 46, hover ? new Color(255, 180, 40, 255) : new Color(70, 70, 90, 200));
            Raylib.DrawText(slotLabels[i], ex + 5, ey + 4, 8, new Color(160, 160, 190, 200));
            if (item != null)
            {
                Raylib.DrawRectangle(ex + 4, ey + 16, 8, 8, item.RarityColor);
                Raylib.DrawText(item.Name.Length > 14 ? item.Name[..14] + ".." : item.Name, ex + 16, ey + 17, 7, item.RarityColor);
            }
            else { Raylib.DrawText("(empty)", ex + 8, ey + 17, 7, new Color(100, 100, 115, 200)); }
            if (hover && Raylib.IsMouseButtonPressed(MouseButton.Right))
                player.UnequipItem(slots[i]);
        }

        // Inventory grid
        int iStartY = py + 118;
        Raylib.DrawText($"Bag ({player.Inventory.Count}/16)", px + 14, iStartY - 14, 10, new Color(200, 200, 240, 240));
        int cols = 8, cardW = 74, cardH = 66, padX = 4, padY = 4;
        for (int i = 0; i < player.Inventory.Count; i++)
        {
            int col = i % cols, row = i / cols;
            int ix = px + 14 + col * (cardW + padX);
            int iy = iStartY + row * (cardH + padY);
            var item = player.Inventory[i];
            bool hover = mouse.X >= ix && mouse.X < ix + cardW && mouse.Y >= iy && mouse.Y < iy + cardH;
            Raylib.DrawRectangle(ix, iy, cardW, cardH, hover ? new Color(40, 35, 20, 240) : new Color(20, 20, 30, 230));
            Raylib.DrawRectangle(ix, iy, 3, cardH, item.RarityColor);
            Raylib.DrawRectangleLines(ix, iy, cardW, cardH, hover ? item.RarityColor : new Color(55, 55, 70, 200));
            Raylib.DrawRectangle(ix + 5, iy + 5, 16, 16, item.RarityColor);
            string shortName = item.Name.Length > 10 ? item.Name[..10] : item.Name;
            Raylib.DrawText(shortName, ix + 4, iy + 25, 7, new Color(220, 220, 255, 240));
            Raylib.DrawText(item.Rarity.ToString(), ix + 4, iy + 35, 6, item.RarityColor);
            // Bonuses
            int bl = 0;
            foreach (var (key, val) in item.Bonuses)
            {
                Raylib.DrawText($"+{val:0.#} {key}", ix + 4, iy + 45 + bl * 8, 6, new Color(180, 240, 180, 200));
                bl++;
            }
            if (hover && Raylib.IsMouseButtonPressed(MouseButton.Left))
                player.EquipItem(i);
        }
    }

    // ── Settings Panel ────────────────────────────────────────────────────────
    public void DrawSettings()
    {
        int sw = Constants.ScreenWidth;
        int sh = Constants.ScreenHeight;
        Raylib.DrawRectangle(0, 0, sw, sh, new Color(0, 0, 0, 160));

        int panW = 480, panH = 400;
        int px = sw / 2 - panW / 2, py = sh / 2 - panH / 2;
        Raylib.DrawRectangle(px, py, panW, panH, new Color(14, 14, 22, 245));
        Raylib.DrawRectangleLines(px, py, panW, panH, new Color(80, 80, 120, 255));
        Raylib.DrawText("SETTINGS", px + 14, py + 14, 18, new Color(255, 215, 60, 255));
        Raylib.DrawText("[ESC/O] Close", px + 14, py + panH - 18, 8, new Color(180, 180, 200, 200));

        var mouse = Raylib.GetMousePosition();

        // Volume sliders
        DrawSlider("Master Volume", px + 20, py + 60, panW - 40, ref _masterVolume, mouse);
        DrawSlider("SFX Volume", px + 20, py + 120, panW - 40, ref _sfxVolume, mouse);

        // Zoom slider
        DrawSlider("Zoom", px + 20, py + 180, panW - 40, ref _zoom, mouse, 1.0f, 3.0f);

        // GPU toggle
        int tx = px + 20, ty = py + 250;
        bool gpuHover = mouse.X >= tx && mouse.X < tx + panW - 40 && mouse.Y >= ty && mouse.Y < ty + 34;
        Raylib.DrawRectangle(tx, ty, panW - 40, 34, gpuHover ? new Color(40, 35, 20, 240) : new Color(20, 20, 30, 230));
        Raylib.DrawRectangleLines(tx, ty, panW - 40, 34, gpuHover ? new Color(255, 180, 40, 255) : new Color(60, 60, 80, 200));
        Raylib.DrawText("GPU Acceleration", tx + 8, ty + 10, 12, Color.White);
        Color btnCol = GpuAccel ? new Color(50, 220, 80, 255) : new Color(220, 60, 60, 255);
        Raylib.DrawRectangle(tx + panW - 72, ty + 7, 50, 20, btnCol);
        Raylib.DrawText(GpuAccel ? "ON" : "OFF", tx + panW - 68, ty + 10, 10, Color.White);
        if (gpuHover && Raylib.IsMouseButtonPressed(MouseButton.Left)) GpuAccel = !GpuAccel;

        // Fullscreen toggle
        ty = py + 298;
        bool fsHover = mouse.X >= tx && mouse.X < tx + panW - 40 && mouse.Y >= ty && mouse.Y < ty + 34;
        Raylib.DrawRectangle(tx, ty, panW - 40, 34, fsHover ? new Color(40, 35, 20, 240) : new Color(20, 20, 30, 230));
        Raylib.DrawRectangleLines(tx, ty, panW - 40, 34, fsHover ? new Color(255, 180, 40, 255) : new Color(60, 60, 80, 200));
        Raylib.DrawText("Fullscreen", tx + 8, ty + 10, 12, Color.White);
        bool isFS = Raylib.IsWindowFullscreen();
        Raylib.DrawRectangle(tx + panW - 72, ty + 7, 50, 20, isFS ? new Color(50, 220, 80, 255) : new Color(220, 60, 60, 255));
        Raylib.DrawText(isFS ? "ON" : "OFF", tx + panW - 68, ty + 10, 10, Color.White);
        if (fsHover && Raylib.IsMouseButtonPressed(MouseButton.Left)) Raylib.ToggleFullscreen();

        Raylib.DrawText("FPS", px + 14, py + panH - 34, 9, new Color(140, 140, 170, 200));
        Raylib.DrawText($"{Raylib.GetFPS()} fps", px + 50, py + panH - 34, 9, new Color(200, 240, 200, 255));
    }

    private static void DrawSlider(string label, int x, int y, int width, ref float value, Vector2 mouse, float min = 0f, float max = 1f)
    {
        Raylib.DrawText(label, x, y, 11, new Color(200, 200, 240, 240));
        int trackH = 8;
        int ty = y + 18;
        Raylib.DrawRectangle(x, ty, width, trackH, new Color(30, 30, 50, 220));
        float pct = (value - min) / (max - min);
        Raylib.DrawRectangle(x, ty, (int)(width * pct), trackH, new Color(255, 180, 40, 255));
        Raylib.DrawRectangleLines(x, ty, width, trackH, new Color(80, 80, 100, 200));
        int knobX = x + (int)(width * pct);
        Raylib.DrawCircle(knobX, ty + trackH / 2, 8, new Color(255, 200, 60, 255));
        Raylib.DrawText($"{value:0.00}", x + width + 8, y + 18, 9, new Color(200, 200, 240, 240));

        // Dragging
        if (Raylib.IsMouseButtonDown(MouseButton.Left)
            && mouse.X >= x - 10 && mouse.X <= x + width + 10
            && mouse.Y >= ty - 8 && mouse.Y <= ty + trackH + 8)
        {
            float np = Math.Clamp((mouse.X - x) / width, 0f, 1f);
            value = min + np * (max - min);
        }
    }

    // ── Game Over ─────────────────────────────────────────────────────────────
    public void DrawGameOver(float survivalTime, int kills)
    {
        int sw = Constants.ScreenWidth;
        int sh = Constants.ScreenHeight;
        Raylib.DrawRectangle(0, 0, sw, sh, new Color(0, 0, 0, 200));
        Raylib.DrawText("YOU DIED", sw / 2 - Raylib.MeasureText("YOU DIED", 44) / 2, sh / 2 - 100, 44, new Color(230, 40, 40, 255));
        string time = $"Survived: {(int)(survivalTime / 60):00}:{(int)(survivalTime % 60):00}";
        Raylib.DrawText(time, sw / 2 - Raylib.MeasureText(time, 16) / 2, sh / 2 - 30, 16, new Color(255, 215, 60, 255));
        Raylib.DrawText("Press [ESC] to return to main menu", sw / 2 - 200, sh / 2 + 20, 12, Color.White);
    }

    // ── Utilities ─────────────────────────────────────────────────────────────
    private static void WrapText(string text, int x, int y, int maxW, int fontSize, Color col, int lineH)
    {
        var words = text.Split(' ');
        string line = "";
        int ly = y;
        foreach (var word in words)
        {
            string testLine = (line == "" ? "" : line + " ") + word;
            if (Raylib.MeasureText(testLine, fontSize) > maxW)
            {
                Raylib.DrawText(line, x, ly, fontSize, col);
                line = word;
                ly += lineH;
            }
            else { line = testLine; }
        }
        if (line != "") Raylib.DrawText(line, x, ly, fontSize, col);
    }
}
