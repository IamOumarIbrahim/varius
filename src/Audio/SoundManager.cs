// src/Audio/SoundManager.cs
// Programmatic sound synthesis — no audio files needed, generates beeps via Raylib AudioStream
using Raylib_cs;
using System;
using System.Collections.Generic;

namespace Varius.Audio;

public class SoundManager
{
    public static SoundManager Instance { get; } = new();

    private float _masterVolume = 0.6f;
    private float _sfxVolume = 0.8f;
    private bool _initialized = false;
    private readonly Dictionary<string, Sound> _sounds = new();

    public float MasterVolume
    {
        get => _masterVolume;
        set 
        { 
            _masterVolume = Math.Clamp(value, 0f, 1f); 
            UpdateVolumes();
        }
    }
    public float SfxVolume
    {
        get => _sfxVolume;
        set 
        { 
            _sfxVolume = Math.Clamp(value, 0f, 1f); 
            UpdateVolumes();
        }
    }

    private void UpdateVolumes()
    {
        if (!_initialized) return;
        float vol = _masterVolume * _sfxVolume;
        foreach (var sound in _sounds.Values)
        {
            Raylib.SetSoundVolume(sound, vol);
        }
    }

    private void EnsureInitialized()
    {
        if (_initialized) return;
        _initialized = true;
        try
        {
            Raylib.InitAudioDevice();
            LoadSynthSound("swing", GenerateWavData(150, 0.14f, "noise"));
            LoadSynthSound("hit", GenerateWavData(110, 0.16f, "square"));
            LoadSynthSound("mine", GenerateWavData(480, 0.08f, "sine"));
            LoadSynthSound("level", GenerateArpeggioWav());
            LoadSynthSound("damage", GenerateWavData(90, 0.22f, "square"));
            LoadSynthSound("build", GenerateSweepWav(130, 520, 0.20f));
            UpdateVolumes();
        }
        catch 
        {
            // Fail silently if audio device fails to initialize
        }
    }

    private unsafe void LoadSynthSound(string name, byte[] wavData)
    {
        fixed (byte* pData = wavData)
        {
            byte[] fileTypeBytes = System.Text.Encoding.UTF8.GetBytes(".wav\0");
            fixed (byte* pFileType = fileTypeBytes)
            {
                Wave wave = Raylib.LoadWaveFromMemory((sbyte*)pFileType, pData, wavData.Length);
                Sound sound = Raylib.LoadSoundFromWave(wave);
                Raylib.UnloadWave(wave);
                _sounds[name] = sound;
            }
        }
    }

    private byte[] GenerateWavData(int frequency, float duration, string type)
    {
        int sampleRate = 22050;
        int numSamples = (int)(sampleRate * duration);
        int subChunk2Size = numSamples * 2;
        int chunkSize = 36 + subChunk2Size;

        byte[] wav = new byte[44 + subChunk2Size];
        System.Text.Encoding.ASCII.GetBytes("RIFF").CopyTo(wav, 0);
        BitConverter.GetBytes(chunkSize).CopyTo(wav, 4);
        System.Text.Encoding.ASCII.GetBytes("WAVE").CopyTo(wav, 8);
        System.Text.Encoding.ASCII.GetBytes("fmt ").CopyTo(wav, 12);
        BitConverter.GetBytes(16).CopyTo(wav, 16);
        BitConverter.GetBytes((short)1).CopyTo(wav, 20);
        BitConverter.GetBytes((short)1).CopyTo(wav, 22);
        BitConverter.GetBytes(sampleRate).CopyTo(wav, 24);
        BitConverter.GetBytes(sampleRate * 2).CopyTo(wav, 28);
        BitConverter.GetBytes((short)2).CopyTo(wav, 32);
        BitConverter.GetBytes((short)16).CopyTo(wav, 34);
        System.Text.Encoding.ASCII.GetBytes("data").CopyTo(wav, 36);
        BitConverter.GetBytes(subChunk2Size).CopyTo(wav, 40);

        var rand = new Random();
        for (int i = 0; i < numSamples; i++)
        {
            float t = (float)i / sampleRate;
            float sample = 0;
            if (type == "sine")
                sample = MathF.Sin(2f * MathF.PI * frequency * t);
            else if (type == "square")
                sample = MathF.Sin(2f * MathF.PI * frequency * t) >= 0 ? 1f : -1f;
            else if (type == "noise")
                sample = (float)(rand.NextDouble() * 2.0 - 1.0);

            float fade = 1f - ((float)i / numSamples);
            sample *= fade;

            short pcmValue = (short)(sample * 16000f);
            BitConverter.GetBytes(pcmValue).CopyTo(wav, 44 + i * 2);
        }
        return wav;
    }

    private byte[] GenerateSweepWav(int startFreq, int endFreq, float duration)
    {
        int sampleRate = 22050;
        int numSamples = (int)(sampleRate * duration);
        int subChunk2Size = numSamples * 2;
        int chunkSize = 36 + subChunk2Size;

        byte[] wav = new byte[44 + subChunk2Size];
        System.Text.Encoding.ASCII.GetBytes("RIFF").CopyTo(wav, 0);
        BitConverter.GetBytes(chunkSize).CopyTo(wav, 4);
        System.Text.Encoding.ASCII.GetBytes("WAVE").CopyTo(wav, 8);
        System.Text.Encoding.ASCII.GetBytes("fmt ").CopyTo(wav, 12);
        BitConverter.GetBytes(16).CopyTo(wav, 16);
        BitConverter.GetBytes((short)1).CopyTo(wav, 20);
        BitConverter.GetBytes((short)1).CopyTo(wav, 22);
        BitConverter.GetBytes(sampleRate).CopyTo(wav, 24);
        BitConverter.GetBytes(sampleRate * 2).CopyTo(wav, 28);
        BitConverter.GetBytes((short)2).CopyTo(wav, 32);
        BitConverter.GetBytes((short)16).CopyTo(wav, 34);
        System.Text.Encoding.ASCII.GetBytes("data").CopyTo(wav, 36);
        BitConverter.GetBytes(subChunk2Size).CopyTo(wav, 40);

        for (int i = 0; i < numSamples; i++)
        {
            float t = (float)i / sampleRate;
            float progress = (float)i / numSamples;
            float freq = startFreq + (endFreq - startFreq) * progress;
            float sample = MathF.Sin(2f * MathF.PI * freq * t);

            float fade = 1f - progress;
            sample *= fade;

            short pcmValue = (short)(sample * 16000f);
            BitConverter.GetBytes(pcmValue).CopyTo(wav, 44 + i * 2);
        }
        return wav;
    }

    private byte[] GenerateArpeggioWav()
    {
        int sampleRate = 22050;
        float duration = 0.6f;
        int numSamples = (int)(sampleRate * duration);
        int subChunk2Size = numSamples * 2;
        int chunkSize = 36 + subChunk2Size;

        byte[] wav = new byte[44 + subChunk2Size];
        System.Text.Encoding.ASCII.GetBytes("RIFF").CopyTo(wav, 0);
        BitConverter.GetBytes(chunkSize).CopyTo(wav, 4);
        System.Text.Encoding.ASCII.GetBytes("WAVE").CopyTo(wav, 8);
        System.Text.Encoding.ASCII.GetBytes("fmt ").CopyTo(wav, 12);
        BitConverter.GetBytes(16).CopyTo(wav, 16);
        BitConverter.GetBytes((short)1).CopyTo(wav, 20);
        BitConverter.GetBytes((short)1).CopyTo(wav, 22);
        BitConverter.GetBytes(sampleRate).CopyTo(wav, 24);
        BitConverter.GetBytes(sampleRate * 2).CopyTo(wav, 28);
        BitConverter.GetBytes((short)2).CopyTo(wav, 32);
        BitConverter.GetBytes((short)16).CopyTo(wav, 34);
        System.Text.Encoding.ASCII.GetBytes("data").CopyTo(wav, 36);
        BitConverter.GetBytes(subChunk2Size).CopyTo(wav, 40);

        int[] notes = { 261, 329, 392, 523 };
        for (int i = 0; i < numSamples; i++)
        {
            float t = (float)i / sampleRate;
            float progress = (float)i / numSamples;
            int noteIndex = Math.Clamp((int)(progress * 4), 0, 3);
            float freq = notes[noteIndex];
            float sample = MathF.Sin(2f * MathF.PI * freq * t);

            float fade = progress > 0.8f ? 1f - (progress - 0.8f) / 0.2f : 1f;
            sample *= fade;

            short pcmValue = (short)(sample * 16000f);
            BitConverter.GetBytes(pcmValue).CopyTo(wav, 44 + i * 2);
        }
        return wav;
    }

    public void Play(string name)
    {
        EnsureInitialized();
        if (_sounds.TryGetValue(name, out var sound))
        {
            Raylib.PlaySound(sound);
        }
    }

    public void StartMusic() { }
    public void StopMusic() { }
    
    public void Update(float dt) { }

    public void Shutdown()
    {
        if (!_initialized) return;
        foreach (var sound in _sounds.Values)
        {
            Raylib.UnloadSound(sound);
        }
        _sounds.Clear();
        try
        {
            Raylib.CloseAudioDevice();
        }
        catch { }
        _initialized = false;
    }
}
