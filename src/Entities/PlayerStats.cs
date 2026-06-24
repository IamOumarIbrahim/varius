// src/Entities/PlayerStats.cs
namespace Varius.Entities;

public class PlayerStats
{
    public int MaxHealth { get; set; } = 100;
    public int MaxPosture { get; set; } = 100;
    public float BaseDmg { get; set; } = 22f;
    public float CritRate { get; set; } = 0.10f;
    public float CritDmg { get; set; } = 1.5f;
    public float Haste { get; set; } = 1.0f;
    public int MiningPower { get; set; } = 1;
    public float ParryWindowMs { get; set; } = 200f;
    public float MoveSpeedMult { get; set; } = 1.0f;
    public float MagnetRange { get; set; } = 3.0f;
    public int Armor { get; set; } = 0;

    public PlayerStats Clone() => (PlayerStats)MemberwiseClone();

    public void ApplyItemBonuses(Item item)
    {
        foreach (var (key, val) in item.Bonuses)
        {
            switch (key)
            {
                case "MaxHealth":     MaxHealth += (int)val; break;
                case "Armor":         Armor += (int)val; break;
                case "CritRate":      CritRate = Math.Min(1f, CritRate + val); break;
                case "CritDmg":       CritDmg += val; break;
                case "MoveSpeedMult": MoveSpeedMult += val; break;
                case "MagnetRange":   MagnetRange += val; break;
                case "Haste":         Haste += val; break;
            }
        }
    }
}
