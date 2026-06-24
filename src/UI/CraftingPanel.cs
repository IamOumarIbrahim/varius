// src/UI/CraftingPanel.cs
// Upgradeable crafting station UI — opened with C key
using Raylib_cs;
using System.Numerics;
using Varius.Core;
using Varius.Entities;

namespace Varius.UI;

public record CraftingMaterial(string ResourceId, int Amount);

public record CraftingRecipe(
    string OutputName,
    string OutputDescription,
    CraftingMaterial[] Inputs,
    int MinLevel,
    string Category, // "TOOLS", "WEAPONS", "ARMOR", "SPECIAL"
    Color AccentColor
);

public class CraftingPanel
{
    private int _hoverIdx = -1;
    private int _categoryFilter = -1; // -1 = all
    private float _craftProgress;
    private int? _craftingRecipeIdx;
    private string? _statusMessage;
    private float _statusTimer;

    private static readonly string[] CategoryLabels = { "ALL", "TOOLS", "WEAPONS", "ARMOR", "SPECIAL" };

    // Resource inventory (string → count)
    public Dictionary<string, int> Resources { get; } = new()
    {
        [Constants.RES_IRON]  = 0,
        [Constants.RES_GOLD]  = 0,
        [Constants.RES_COAL]  = 0,
        [Constants.RES_FROST] = 0,
        [Constants.RES_EMBER] = 0,
        [Constants.RES_RUNIC] = 0,
    };

    public void AddResource(string id, int amount = 1)
    {
        if (Resources.ContainsKey(id)) Resources[id] += amount;
        else Resources[id] = amount;
    }

    // Full recipe list
    public static readonly CraftingRecipe[] AllRecipes = new CraftingRecipe[]
    {
        new("Golden Pickaxe", "Mines 2 tiles at once. +2 Mining Power.",
            new[] { new CraftingMaterial(Constants.RES_GOLD, 5), new CraftingMaterial(Constants.RES_IRON, 2) },
            3, "TOOLS", new Color((byte)255, (byte)215, (byte)20, (byte)255)),

        new("Iron Shield", "Grants +3 Armor permanently.",
            new[] { new CraftingMaterial(Constants.RES_IRON, 6) },
            2, "ARMOR", new Color((byte)180, (byte)180, (byte)200, (byte)255)),

        new("Frost Blade", "Your sword attacks slow enemies by 40% for 2s.",
            new[] { new CraftingMaterial(Constants.RES_FROST, 3), new CraftingMaterial(Constants.RES_IRON, 2) },
            5, "WEAPONS", new Color((byte)100, (byte)220, (byte)255, (byte)255)),

        new("Ember Cannon", "Fires a burning projectile dealing double damage.",
            new[] { new CraftingMaterial(Constants.RES_EMBER, 3), new CraftingMaterial(Constants.RES_IRON, 3) },
            7, "WEAPONS", new Color((byte)255, (byte)100, (byte)20, (byte)255)),

        new("Runic Amulet", "+25% XP gain from all sources.",
            new[] { new CraftingMaterial(Constants.RES_RUNIC, 2), new CraftingMaterial(Constants.RES_GOLD, 2) },
            6, "SPECIAL", new Color((byte)180, (byte)80, (byte)255, (byte)255)),

        new("Coal Torch Pack", "Grants 12 torches instantly.",
            new[] { new CraftingMaterial(Constants.RES_COAL, 4) },
            1, "TOOLS", new Color((byte)200, (byte)160, (byte)80, (byte)255)),

        new("Iron Sword", "+8 base damage. Upgrades the KATANA slot.",
            new[] { new CraftingMaterial(Constants.RES_IRON, 4), new CraftingMaterial(Constants.RES_COAL, 2) },
            2, "WEAPONS", new Color((byte)160, (byte)180, (byte)210, (byte)255)),

        new("Gold Ring", "+10% crit rate permanently.",
            new[] { new CraftingMaterial(Constants.RES_GOLD, 3) },
            4, "ARMOR", new Color((byte)255, (byte)200, (byte)40, (byte)255)),

        new("Frost Boots", "+20% movement speed in ice biome.",
            new[] { new CraftingMaterial(Constants.RES_FROST, 4), new CraftingMaterial(Constants.RES_IRON, 1) },
            5, "ARMOR", new Color((byte)140, (byte)220, (byte)255, (byte)255)),

        new("Rune Scroll", "Instantly grants 120 XP.",
            new[] { new CraftingMaterial(Constants.RES_RUNIC, 1), new CraftingMaterial(Constants.RES_COAL, 2) },
            3, "SPECIAL", new Color((byte)200, (byte)120, (byte)255, (byte)255)),

        new("Ember Armor", "+5 Armor. Immune to magma damage.",
            new[] { new CraftingMaterial(Constants.RES_EMBER, 5), new CraftingMaterial(Constants.RES_IRON, 4) },
            8, "ARMOR", new Color((byte)220, (byte)80, (byte)20, (byte)255)),

        new("Diamond Drill", "Mines 3 tiles at once. Instant coal/stone break.",
            new[] { new CraftingMaterial(Constants.RES_GOLD, 6), new CraftingMaterial(Constants.RES_FROST, 2), new CraftingMaterial(Constants.RES_EMBER, 2) },
            10, "TOOLS", new Color((byte)100, (byte)240, (byte)255, (byte)255)),
    };

    public void Update(float dt, Player player)
    {
        if (_statusTimer > 0) _statusTimer -= dt;
        if (_craftingRecipeIdx.HasValue)
        {
            _craftProgress += dt / 1.8f; // 1.8s craft time
            if (_craftProgress >= 1f)
            {
                _craftProgress = 0;
                ApplyCraftEffect(_craftingRecipeIdx.Value, player);
                _craftingRecipeIdx = null;
            }
        }
    }

    public void Draw(Player player)
    {
        int sw = Constants.ScreenWidth;
        int sh = Constants.ScreenHeight;

        // Overlay dim
        Raylib.DrawRectangle(0, 0, sw, sh, new Color((byte)0, (byte)0, (byte)0, (byte)165));

        int panW = 900, panH = 520;
        int px = sw / 2 - panW / 2, py = sh / 2 - panH / 2;

        // Panel background
        Raylib.DrawRectangle(px, py, panW, panH, new Color((byte)12, (byte)12, (byte)20, (byte)248));
        Raylib.DrawRectangleLines(px, py, panW, panH, new Color((byte)80, (byte)70, (byte)100, (byte)255));
        // Header accent line
        Raylib.DrawRectangle(px, py, panW, 3, new Color((byte)255, (byte)180, (byte)40, (byte)255));

        Raylib.DrawText("⚒ CRAFTING STATION", px + 18, py + 14, 20, new Color((byte)255, (byte)200, (byte)60, (byte)255));
        Raylib.DrawText("[ESC/C] Close  |  Click recipe to craft", px + 18, py + panH - 18, 8,
            new Color((byte)180, (byte)180, (byte)200, (byte)200));

        // ── Resources panel (right) ───────────────────────────────────────────
        int resX = px + panW - 200, resY = py + 48;
        Raylib.DrawRectangle(resX - 4, resY - 4, 196, 170, new Color((byte)18, (byte)18, (byte)28, (byte)220));
        Raylib.DrawRectangleLines(resX - 4, resY - 4, 196, 170, new Color((byte)60, (byte)60, (byte)80, (byte)200));
        Raylib.DrawText("RESOURCES", resX, resY, 10, new Color((byte)200, (byte)200, (byte)240, (byte)240));

        (string id, string label, Color col)[] resDisplay =
        {
            (Constants.RES_IRON,  "Iron",         new Color((byte)200, (byte)140, (byte)80, (byte)255)),
            (Constants.RES_GOLD,  "Gold",         new Color((byte)255, (byte)215, (byte)20, (byte)255)),
            (Constants.RES_COAL,  "Coal",         new Color((byte)140, (byte)140, (byte)150, (byte)255)),
            (Constants.RES_FROST, "Frost Crystal",new Color((byte)100, (byte)220, (byte)255, (byte)255)),
            (Constants.RES_EMBER, "Ember Stone",  new Color((byte)255, (byte)100, (byte)20, (byte)255)),
            (Constants.RES_RUNIC, "Runic Shard",  new Color((byte)180, (byte)80, (byte)255, (byte)255)),
        };
        for (int i = 0; i < resDisplay.Length; i++)
        {
            var (id, label, col) = resDisplay[i];
            int ry = resY + 18 + i * 22;
            int count = Resources.GetValueOrDefault(id, 0);
            Raylib.DrawRectangle(resX, ry, 12, 12, col);
            Raylib.DrawText(label, resX + 18, ry, 9, count > 0 ? col : new Color((byte)80, (byte)80, (byte)90, (byte)180));
            Raylib.DrawText($"x{count}", resX + 155, ry, 9, count > 0 ? Color.White : new Color((byte)70, (byte)70, (byte)80, (byte)180));
        }

        // Player level
        Raylib.DrawText($"Level: {player.Level}", resX, resY + 155, 9, new Color((byte)140, (byte)200, (byte)255, (byte)240));

        // ── Category tabs ──────────────────────────────────────────────────────
        int tabY = py + 48;
        for (int i = 0; i < CategoryLabels.Length; i++)
        {
            int tx = px + 12 + i * 100;
            bool active = _categoryFilter == (i - 1);
            var mouse = Raylib.GetMousePosition();
            bool hover = mouse.X >= tx && mouse.X < tx + 92 && mouse.Y >= tabY && mouse.Y < tabY + 24;
            Raylib.DrawRectangle(tx, tabY, 92, 24, active ? new Color((byte)50, (byte)45, (byte)28, (byte)240) : new Color((byte)22, (byte)22, (byte)32, (byte)200));
            Raylib.DrawRectangleLines(tx, tabY, 92, 24, active ? new Color((byte)255, (byte)180, (byte)40, (byte)255) : new Color((byte)60, (byte)60, (byte)80, (byte)180));
            Raylib.DrawText(CategoryLabels[i], tx + 8, tabY + 7, 9, active ? new Color((byte)255, (byte)200, (byte)60, (byte)255) : Color.White);
            if (hover && Raylib.IsMouseButtonPressed(MouseButton.Left))
                _categoryFilter = i - 1;
        }

        // ── Recipe list ────────────────────────────────────────────────────────
        int listX = px + 12, listY = py + 82;
        int cardW = panW - 230, cardH = 56;
        int visibleRecipes = (panH - 110) / (cardH + 4);

        var mouse2 = Raylib.GetMousePosition();
        _hoverIdx = -1;
        int shown = 0;

        for (int i = 0; i < AllRecipes.Length && shown < visibleRecipes; i++)
        {
            var recipe = AllRecipes[i];
            if (_categoryFilter >= 0 && recipe.Category != CategoryLabels[_categoryFilter + 1]) continue;

            int ry = listY + shown * (cardH + 4);
            bool hover = mouse2.X >= listX && mouse2.X < listX + cardW && mouse2.Y >= ry && mouse2.Y < ry + cardH;
            if (hover) _hoverIdx = i;

            bool canCraft = CanCraft(recipe) && player.Level >= recipe.MinLevel;
            bool crafting = _craftingRecipeIdx == i;

            // Card background
            var bgCol = hover ? new Color((byte)40, (byte)36, (byte)22, (byte)235) : new Color((byte)20, (byte)20, (byte)30, (byte)220);
            Raylib.DrawRectangle(listX, ry, cardW, cardH, bgCol);
            // Left accent bar
            Raylib.DrawRectangle(listX, ry, 4, cardH, canCraft ? recipe.AccentColor : new Color((byte)50, (byte)50, (byte)60, (byte)200));
            Raylib.DrawRectangleLines(listX, ry, cardW, cardH,
                hover ? recipe.AccentColor : new Color((byte)50, (byte)50, (byte)65, (byte)180));

            // Name
            var nameCol = canCraft ? Color.White : new Color((byte)100, (byte)100, (byte)110, (byte)200);
            Raylib.DrawText(recipe.OutputName, listX + 12, ry + 8, 12, nameCol);
            // Level requirement
            string lvlText = $"Lv.{recipe.MinLevel}+";
            var lvlCol = player.Level >= recipe.MinLevel
                ? new Color((byte)100, (byte)200, (byte)100, (byte)255)
                : new Color((byte)200, (byte)80, (byte)60, (byte)255);
            Raylib.DrawText(lvlText, listX + cardW - 60, ry + 8, 9, lvlCol);

            // Description
            Raylib.DrawText(recipe.OutputDescription, listX + 12, ry + 24, 8,
                new Color((byte)180, (byte)180, (byte)200, (byte)220));

            // Input costs
            int costX = listX + 12;
            int costY = ry + 38;
            foreach (var mat in recipe.Inputs)
            {
                int have = Resources.GetValueOrDefault(mat.ResourceId, 0);
                bool hasMat = have >= mat.Amount;
                var matCol = hasMat ? new Color((byte)100, (byte)220, (byte)100, (byte)255) : new Color((byte)220, (byte)80, (byte)60, (byte)255);
                string matLabel = mat.ResourceId.Replace("_", " ");
                string costText = $"{matLabel} x{mat.Amount}  ";
                Raylib.DrawText(costText, costX, costY, 8, matCol);
                costX += Raylib.MeasureText(costText, 8);
            }

            // Craft button / progress
            if (crafting)
            {
                int pbW = (int)((cardW - 16) * _craftProgress);
                Raylib.DrawRectangle(listX + 8, ry + cardH - 8, cardW - 16, 5, new Color((byte)30, (byte)30, (byte)45, (byte)200));
                Raylib.DrawRectangle(listX + 8, ry + cardH - 8, pbW, 5, recipe.AccentColor);
                Raylib.DrawText("CRAFTING...", listX + cardW - 90, ry + 8, 8, new Color((byte)255, (byte)200, (byte)60, (byte)255));
            }
            else if (hover && canCraft && !_craftingRecipeIdx.HasValue)
            {
                Raylib.DrawText("[CLICK] Craft", listX + cardW - 90, ry + 8, 8, new Color((byte)100, (byte)240, (byte)120, (byte)255));
                if (Raylib.IsMouseButtonPressed(MouseButton.Left))
                    StartCraft(i);
            }

            shown++;
        }

        // Status message
        if (_statusTimer > 0 && _statusMessage != null)
        {
            float alpha = _statusTimer / 2.5f;
            Raylib.DrawText(_statusMessage, px + panW / 2 - Raylib.MeasureText(_statusMessage, 14) / 2,
                py + panH / 2 - 10, 14,
                new Color((byte)100, (byte)255, (byte)130, (byte)(int)(alpha * 255)));
        }
    }

    public bool CanCraft(CraftingRecipe recipe)
    {
        foreach (var mat in recipe.Inputs)
            if (Resources.GetValueOrDefault(mat.ResourceId, 0) < mat.Amount) return false;
        return true;
    }

    private void StartCraft(int idx)
    {
        _craftingRecipeIdx = idx;
        _craftProgress = 0;
        // Deduct materials immediately
        foreach (var mat in AllRecipes[idx].Inputs)
            Resources[mat.ResourceId] = Math.Max(0, Resources.GetValueOrDefault(mat.ResourceId, 0) - mat.Amount);
    }

    private void ApplyCraftEffect(int idx, Player player)
    {
        var recipe = AllRecipes[idx];
        // Apply recipe effects
        switch (recipe.OutputName)
        {
            case "Golden Pickaxe":
                player.BaseStats.MiningPower += 2;
                player.RecalculateStats();
                break;
            case "Iron Shield":
                player.BaseStats.Armor += 3;
                player.RecalculateStats();
                break;
            case "Frost Blade":
                player.BaseStats.BaseDmg += 8;
                player.RecalculateStats();
                break;
            case "Ember Cannon":
                player.BaseStats.BaseDmg += 12;
                player.RecalculateStats();
                break;
            case "Runic Amulet":
                // Handled as passive bonus — mark in stats note (simplified: +20% dmg for now)
                player.BaseStats.BaseDmg *= 1.08f;
                player.RecalculateStats();
                break;
            case "Coal Torch Pack":
                // No stat change; just resource flavor
                break;
            case "Iron Sword":
                player.BaseStats.BaseDmg += 8;
                player.RecalculateStats();
                break;
            case "Gold Ring":
                player.BaseStats.CritRate = Math.Min(1f, player.BaseStats.CritRate + 0.10f);
                player.RecalculateStats();
                break;
            case "Frost Boots":
                player.BaseStats.MoveSpeedMult += 0.20f;
                player.RecalculateStats();
                break;
            case "Rune Scroll":
                player.AddXP(120);
                break;
            case "Ember Armor":
                player.BaseStats.Armor += 5;
                player.RecalculateStats();
                break;
            case "Diamond Drill":
                player.BaseStats.MiningPower += 3;
                player.RecalculateStats();
                break;
        }
        _statusMessage = $"✓ {recipe.OutputName} crafted!";
        _statusTimer = 2.5f;
    }
}
