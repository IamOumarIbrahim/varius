import pygame
import array
import math
import random

class SoundManager:
    def __init__(self):
        self.sfx_volume = 0.5
        self.music_volume = 0.3
        
        # Audio generation constants
        self.sample_rate = 22050
        
        # Pre-generate sounds
        self.sounds = {}
        self.music_channel = None
        self.music_sound = None
        
        self.generate_all_sounds()

    def generate_all_sounds(self):
        self.sounds["swing"] = self.gen_swing()
        self.sounds["hit"] = self.gen_hit()
        self.sounds["parry"] = self.gen_parry()
        self.sounds["block"] = self.gen_block()
        self.sounds["mine"] = self.gen_mine()
        self.sounds["levelup"] = self.gen_levelup()
        self.sounds["click"] = self.gen_click()
        
        # Generate background loop
        self.music_sound = self.gen_music_loop()

    def set_sfx_volume(self, volume):
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)

    def set_music_volume(self, volume):
        self.music_volume = max(0.0, min(1.0, volume))
        if self.music_channel:
            self.music_channel.set_volume(self.music_volume)

    def play(self, name):
        if name in self.sounds:
            self.sounds[name].play()

    def start_music(self):
        if not pygame.mixer.get_init():
            return
        # Channel 0 reserved for music
        self.music_channel = pygame.mixer.Channel(0)
        self.music_channel.set_volume(self.music_volume)
        # Play music looping infinitely
        self.music_channel.play(self.music_sound, loops=-1)

    def stop_music(self):
        if self.music_channel:
            self.music_channel.stop()

    # --- SYNTHESIZERS ---
    
    def gen_swing(self):
        # Sweeping pitch from 500Hz down to 80Hz
        duration = 0.15
        num_samples = int(self.sample_rate * duration)
        buf = array.array('h', [0] * num_samples)
        
        for i in range(num_samples):
            t = float(i) / self.sample_rate
            # Logarithmic frequency sweep
            freq = 500.0 * (80.0 / 500.0) ** (t / duration)
            val = math.sin(2.0 * math.pi * freq * t)
            
            # Fade out envelope
            env = 1.0 - (i / num_samples)
            buf[i] = int(val * 32767 * self.sfx_volume * env)
            
        return pygame.mixer.Sound(buffer=buf)

    def gen_hit(self):
        # White noise burst (damage crunch)
        duration = 0.2
        num_samples = int(self.sample_rate * duration)
        buf = array.array('h', [0] * num_samples)
        
        for i in range(num_samples):
            t = float(i) / self.sample_rate
            # Random noise
            val = random.uniform(-1.0, 1.0)
            # Heavy decay envelope
            env = math.exp(-12.0 * t)
            buf[i] = int(val * 32767 * self.sfx_volume * env * 0.7)
            
        return pygame.mixer.Sound(buffer=buf)

    def gen_parry(self):
        # Metallic ring (sine wave chords)
        duration = 0.6
        num_samples = int(self.sample_rate * duration)
        buf = array.array('h', [0] * num_samples)
        
        # Combine frequencies to sound metallic
        f1 = 980.0
        f2 = 1250.0
        f3 = 1600.0
        
        for i in range(num_samples):
            t = float(i) / self.sample_rate
            val = 0.5 * math.sin(2.0 * math.pi * f1 * t) + \
                  0.3 * math.sin(2.0 * math.pi * f2 * t) + \
                  0.2 * math.sin(2.0 * math.pi * f3 * t)
                  
            # Exponential decay
            env = math.exp(-5.0 * t)
            
            # Small linear fade in (5ms) to prevent initial pop
            if i < 110:
                env *= (i / 110.0)
                
            buf[i] = int(val * 32767 * self.sfx_volume * env * 0.95)
            
        return pygame.mixer.Sound(buffer=buf)

    def gen_block(self):
        # Metallic clink (short metallic chime mixed with noise)
        duration = 0.08
        num_samples = int(self.sample_rate * duration)
        buf = array.array('h', [0] * num_samples)
        
        f1 = 1200.0
        f2 = 1800.0
        
        for i in range(num_samples):
            t = float(i) / self.sample_rate
            tone = 0.6 * math.sin(2.0 * math.pi * f1 * t) + 0.2 * math.sin(2.0 * math.pi * f2 * t)
            noise = 0.2 * random.uniform(-1.0, 1.0)
            val = tone + noise
            
            # Linear decay
            env = 1.0 - (i / num_samples)
            buf[i] = int(val * 32767 * self.sfx_volume * env * 0.8)
            
        return pygame.mixer.Sound(buffer=buf)

    def gen_mine(self):
        # Low pitch thud
        duration = 0.12
        num_samples = int(self.sample_rate * duration)
        buf = array.array('h', [0] * num_samples)
        
        for i in range(num_samples):
            t = float(i) / self.sample_rate
            # Sweeping pitch from 120Hz down to 60Hz
            freq = 120.0 - 60.0 * (t / duration)
            val = math.sin(2.0 * math.pi * freq * t)
            
            # Exponential decay
            env = math.exp(-10.0 * t)
            buf[i] = int(val * 32767 * self.sfx_volume * env * 0.9)
            
        return pygame.mixer.Sound(buffer=buf)

    def gen_levelup(self):
        # Ascending arpeggio (C5, E5, G5, C6)
        duration = 0.45
        num_samples = int(self.sample_rate * duration)
        buf = array.array('h', [0] * num_samples)
        
        # Tone definitions
        notes = [523.25, 659.25, 783.99, 1046.50]  # C5, E5, G5, C6
        note_len = num_samples // len(notes)
        
        for note_idx, freq in enumerate(notes):
            for i in range(note_len):
                idx = note_idx * note_len + i
                t = float(idx) / self.sample_rate
                val = math.sin(2.0 * math.pi * freq * t)
                
                # Soft envelope per note to make it floaty
                local_t = float(i) / note_len
                env = math.sin(math.pi * local_t)  # Bell curve shape
                
                buf[idx] = int(val * 32767 * self.sfx_volume * env * 0.75)
                
        return pygame.mixer.Sound(buffer=buf)

    def gen_click(self):
        # Two clean chime notes
        duration = 0.16
        num_samples = int(self.sample_rate * duration)
        buf = array.array('h', [0] * num_samples)
        
        notes = [587.33, 783.99] # D5, G5
        note_len = num_samples // len(notes)
        
        for note_idx, freq in enumerate(notes):
            for i in range(note_len):
                idx = note_idx * note_len + i
                t = float(idx) / self.sample_rate
                val = math.sin(2.0 * math.pi * freq * t)
                
                # Decay envelope per note
                env = 1.0 - (float(i) / note_len)
                buf[idx] = int(val * 32767 * self.sfx_volume * env * 0.6)
                
        return pygame.mixer.Sound(buffer=buf)

    def gen_music_loop(self):
        # 8-second soothing synth melody loop
        duration = 8.0
        num_samples = int(self.sample_rate * duration)
        buf = array.array('h', [0] * num_samples)
        
        # Chord progression: Am (A3, C4, E4), F (F3, A3, C4), C (C3, E3, G3), G (G3, B3, D4)
        # Each chord lasts 2.0 seconds
        chord_freqs = [
            [220.00, 261.63, 329.63], # Am (A3, C4, E4)
            [174.61, 220.00, 261.63], # F (F3, A3, C4)
            [130.81, 164.81, 196.00], # C (C3, E3, G3)
            [196.00, 246.94, 293.66], # G (G3, B3, D4)
        ]
        
        chord_duration = 2.0
        samples_per_chord = int(self.sample_rate * chord_duration)
        
        for c_idx in range(4):
            ch_notes = chord_freqs[c_idx]
            offset = c_idx * samples_per_chord
            
            # We arpeggiate the notes in the chord: 4 notes per chord (each 0.5s)
            for note_step in range(4):
                note_freq = ch_notes[note_step % len(ch_notes)]
                step_offset = offset + int(note_step * 0.5 * self.sample_rate)
                step_samples = int(0.5 * self.sample_rate)
                
                for i in range(step_samples):
                    idx = step_offset + i
                    if idx >= num_samples:
                        break
                    
                    t = float(idx) / self.sample_rate
                    # Soft sine wave arpeggio
                    val = 0.55 * math.sin(2.0 * math.pi * note_freq * t)
                    
                    # Add a very soft octave harmonizer
                    val += 0.20 * math.sin(2.0 * math.pi * (note_freq * 2.0) * t)
                    
                    # Envelope per note (soft bell shape)
                    local_t = float(i) / step_samples
                    env = math.sin(math.pi * local_t)
                    
                    # Overall fade for chord bounds to prevent seams
                    chord_progress = float(note_step * 0.5 + local_t * 0.5) / chord_duration
                    seam_env = math.sin(math.pi * chord_progress)
                    
                    buf[idx] = int(val * 32767 * self.music_volume * env * seam_env * 0.35)
                    
        return pygame.mixer.Sound(buffer=buf)
