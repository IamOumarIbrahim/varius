// src/Data/SaveSystem.cs
using System.Text.Json;
using System.Text.Json.Serialization;
using Varius.World;

namespace Varius.Data;

public class SaveData
{
    public float SurvivalTime { get; set; }
    public int Gold { get; set; }
    public int Iron { get; set; }
    public int ScholarPts { get; set; }
    public float Zoom { get; set; } = 1.5f;
    public List<NpcData> RescuedNpcs { get; set; } = new();
    public List<Structure> Structures { get; set; } = new();
    public PlayerSaveData? Player { get; set; }
    public int[][]? WorldGrid { get; set; }
    public List<MobSaveData> Mobs { get; set; } = new();
}

public class NpcData
{
    public string Name { get; set; } = "";
    public string Job { get; set; } = "Unassigned";
    public int Level { get; set; } = 1;
}

public class PlayerSaveData
{
    public float X { get; set; }
    public float Y { get; set; }
    public int Health { get; set; }
    public float Posture { get; set; }
    public string Stance { get; set; } = "STONE";
    public int ActiveSlot { get; set; }
    public int Level { get; set; } = 1;
    public int Xp { get; set; }
    public int XpToNext { get; set; } = 100;
    public int CharacterIndex { get; set; }
    public string CharName { get; set; } = "Hero";
    public List<ItemData> Inventory { get; set; } = new();
    public Dictionary<string, ItemData?> Equipped { get; set; } = new()
    {
        ["HELMET"] = null, ["RING"] = null, ["CAPE"] = null
    };
}

public class MobSaveData
{
    public float X { get; set; }
    public float Y { get; set; }
    public string Type { get; set; } = "SLIME";
    public int Health { get; set; }
    public float Posture { get; set; }
}

public class ItemData
{
    public string Name { get; set; } = "";
    public string Slot { get; set; } = "HELMET";
    public string Rarity { get; set; } = "COMMON";
    public Dictionary<string, float> Bonuses { get; set; } = new();
}

public static class SaveSystem
{
    private static readonly JsonSerializerOptions _opts = new()
    {
        WriteIndented = false,
        PropertyNamingPolicy = JsonNamingPolicy.CamelCase
    };

    public static void Save(SaveData data, int slot)
    {
        string path = $"save_slot_{slot}.json";
        string json = JsonSerializer.Serialize(data, _opts);
        File.WriteAllText(path, json);
    }

    public static SaveData? Load(int slot)
    {
        string path = $"save_slot_{slot}.json";
        if (!File.Exists(path)) return null;
        string json = File.ReadAllText(path);
        return JsonSerializer.Deserialize<SaveData>(json, _opts);
    }

    public static bool SlotExists(int slot) => File.Exists($"save_slot_{slot}.json");

    public static void Delete(int slot)
    {
        string path = $"save_slot_{slot}.json";
        if (File.Exists(path)) File.Delete(path);
    }
}
