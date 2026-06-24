// src/Audio/SoundManager.cs
// Programmatic sound synthesis — no audio files needed, generates beeps via Raylib AudioStream
using Raylib_cs;
using System.Numerics;

namespace Varius.Audio;

public class SoundManager
{
    private float _masterVolume = 0.6f;
    private float _sfxVolume = 0.8f;
    private readonly Dictionary<string, float[]> _clips = new();

    public float MasterVolume
    {
        get => _masterVolume;
        set { _masterVolume = Math.Clamp(value, 0, 1); }
    }
    public float SfxVolume
    {
        get => _sfxVolume;
        set { _sfxVolume = Math.Clamp(value, 0, 1); }
    }

    public void Play(string name)
    {
        // Placeholder: In future version, generate audio buffers via Raylib AudioStream
        // For now, no audio output to keep dependencies minimal
    }

    public void StartMusic() { }
    public void StopMusic() { }
    public void Update(float dt) { }
}
