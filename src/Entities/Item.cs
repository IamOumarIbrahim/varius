// src/Entities/Item.cs
using Raylib_cs;

namespace Varius.Entities;

public enum ItemSlot { Helmet, Ring, Cape }
public enum ItemRarity { Common, Rare, Epic, Legendary }

public class Item
{
    public string Name { get; set; } = "";
    public ItemSlot Slot { get; set; }
    public ItemRarity Rarity { get; set; }
    public Dictionary<string, float> Bonuses { get; set; } = new();

    public Color RarityColor => Rarity switch
    {
        ItemRarity.Common    => new Color(220, 220, 220, 255),
        ItemRarity.Rare      => new Color(50, 150, 255, 255),
        ItemRarity.Epic      => new Color(160, 50, 240, 255),
        ItemRarity.Legendary => new Color(255, 140, 0, 255),
        _                    => Color.White
    };

    private static readonly Random _rng = new();
    private static readonly string[] Prefixes = { "Mythic", "Ancient", "Steel", "Crimson", "Shadow", "Golden", "Rusty", "Arcane" };

    public static Item GenerateRandom(int playerLevel)
    {
        var slot = (ItemSlot)_rng.Next(3);
        double roll = _rng.NextDouble();
        var rarity = roll < 0.60 ? ItemRarity.Common :
                     roll < 0.85 ? ItemRarity.Rare :
                     roll < 0.97 ? ItemRarity.Epic :
                                   ItemRarity.Legendary;

        float mult = rarity switch
        {
            ItemRarity.Common    => 1.0f,
            ItemRarity.Rare      => 1.6f,
            ItemRarity.Epic      => 2.4f,
            ItemRarity.Legendary => 3.8f,
            _                    => 1.0f
        };

        string[] suffixes = slot switch
        {
            ItemSlot.Helmet => new[] { "Crown", "Great Helm", "Visor", "Cap" },
            ItemSlot.Ring   => new[] { "Ring", "Band", "Signet", "Loop" },
            _               => new[] { "Cape", "Cloak", "Mantle", "Shroud" }
        };
        string modifier = slot switch
        {
            ItemSlot.Helmet => "of Vitality",
            ItemSlot.Ring   => "of Critical Eye",
            _               => "of Swiftness"
        };

        string name = $"{Prefixes[_rng.Next(Prefixes.Length)]} {suffixes[_rng.Next(suffixes.Length)]} {modifier}";

        var bonuses = new Dictionary<string, float>();
        switch (slot)
        {
            case ItemSlot.Helmet:
                bonuses["MaxHealth"] = (int)((_rng.Next(10, 20)) * mult);
                if (rarity >= ItemRarity.Rare) bonuses["Armor"] = (int)(_rng.Next(1, 3) * (mult / 1.5f));
                break;
            case ItemSlot.Ring:
                bonuses["CritRate"] = MathF.Round(_rng.NextSingle() * 0.03f * mult + 0.02f, 3);
                if (rarity >= ItemRarity.Epic) bonuses["CritDmg"] = MathF.Round(_rng.NextSingle() * 0.07f * mult + 0.08f, 2);
                break;
            case ItemSlot.Cape:
                bonuses["MoveSpeedMult"] = MathF.Round(_rng.NextSingle() * 0.04f * mult + 0.04f, 2);
                if (rarity >= ItemRarity.Rare) bonuses["MagnetRange"] = MathF.Round(_rng.NextSingle() * 0.7f * mult + 0.5f, 1);
                break;
        }

        return new Item { Name = name, Slot = slot, Rarity = rarity, Bonuses = bonuses };
    }
}

public class ItemDrop
{
    public float X { get; set; }
    public float Y { get; set; }
    public Item Item { get; }
    private float _vy;
    private bool _magnetized;
    public float Lifetime { get; private set; } = 16f;
    private const float Radius = 6f;

    public ItemDrop(float x, float y, Item item)
    {
        X = x;
        Y = y;
        Item = item;
    }

    public bool Update(float dt, float playerX, float playerY, float playerW, float playerH,
        float magnetRange, World.GameWorld world)
    {
        Lifetime -= dt;
        float px = playerX + playerW / 2, py = playerY + playerH / 2;
        float dx = px - X, dy = py - Y;
        float dist = MathF.Sqrt(dx * dx + dy * dy);

        if (dist < magnetRange * 16 + 24) _magnetized = true;

        if (_magnetized && dist > 0.5f)
        {
            float spd = 300f;
            X += dx / dist * spd * dt;
            Y += dy / dist * spd * dt;
        }
        else if (!_magnetized)
        {
            _vy += 620f * dt;
            if (_vy > 300f) _vy = 300f;
            Y += _vy * dt;
            var rect = new Rectangle(X - Radius, Y - Radius, Radius * 2, Radius * 2);
            var cols = world.CheckTileCollision(rect);
            if (cols.Count > 0) { Y = cols[0].Y - Radius; _vy = 0; }
        }

        // Check player pickup
        float pdx = X - px, pdy = Y - py;
        return MathF.Sqrt(pdx * pdx + pdy * pdy) < 14f;
    }

    public void Draw(float camX, float camY, float zoom)
    {
        int sx = (int)(X * zoom - camX);
        int sy = (int)(Y * zoom - camY);
        int r = (int)(Radius * zoom);

        // Glowing border
        Raylib.DrawCircle(sx, sy, r + 2, new Color(Item.RarityColor.R, Item.RarityColor.G, Item.RarityColor.B, (byte)80));
        Raylib.DrawRectangle(sx - r, sy - r, r * 2, r * 2, Item.RarityColor);
        Raylib.DrawRectangleLines(sx - r, sy - r, r * 2, r * 2, new Color((byte)25, (byte)25, (byte)25, (byte)255));
        Raylib.DrawLine(sx - r + 1, sy, sx + r - 1, sy, new Color((byte)255, (byte)215, (byte)0, (byte)180));
    }
}
