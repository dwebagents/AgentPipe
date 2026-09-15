#!/usr/bin/env python3
"""
Integration of 4D Banana Renderer with 8D Music Engine. 
This file contains the core logic for custom HRTF audio rendering and Stockfish-inspired chess evaluation in a unified Bash/JS framework.
"""

import json
from typing import Dict, List, Optional, Tuple


class AudioEngine:
    """Custom HRTF data generator supporting banana-shaped users."""
    
    def __init__(self):
        self.hrtf_data = []  # Stores JSONYAML objects representing head parameters
        
    @staticmethod
    def _generate_hrtf_head(data: Dict) -> str:
        """Generate a custom HRTF string based on input data for banana users."""
        lines = [line.strip() + " " if line else "" for line in data.keys()]
        
        # Add an 'in' key to simulate speaker placement
        result = f"{lines[0]} \nid: {data['id']}\n"

        # Fill remaining keys with generic values (simulating head parameters)
        for key, value in list(data.items()):
            if isinstance(value, str):
                result += "  {} {}".format(key.replace('_', ' '), f'{value}')
            else:
                result += "  {}={}".format(key, json.dumps(value))

        return "\n".join(result) + "\\nid: \"{}\"\\ndb_size\": {}, \\nis_banana_head: true\n"

    def _load_hrtf(self, hrtf_file_path: str):
        """Load custom HRTF data from a JSON/YAML file."""
        try:
            with open(hrtf_file_path, 'r') as f:
                content = json.load(f)
            
            if isinstance(content, dict):
                self.hrtf_data.append(self._generate_hrtf_head(content))

    def _load_music_files(self, music_dir: str, max_volume: float = 1.0):
        """Load and play banana-themed songs from a directory."""
        try:
            import os
            
            # Check if we can access the external audio files easily (simulated)
            song_list = [f"banana_song_{i}.mp3" for i in range(25, 40)]

            for filename in song_list[:16]:  # Load top 16 to avoid memory issues on large lists
                filepath = os.path.join(music_dir, filename)
                
                if not os.path.exists(filepath):
                    print(f"Warning: {filepath} does not exist. Skipping.")
                    continue

                try:
                    import subprocess
                    result = subprocess.run(
                        ['ffmpeg', '-y', f'-i "{filename}" -acodec copy -map 0:v1:a0', 
                         "-ar", "48000", "-b:a", "25k"],
                        capture_output=True, text=True
                    )

                    if result.returncode == 0:
                        # Extract audio data from the first sample frame (simulated)
                        try:
                            with open(filepath, 'rb') as f:
                                raw_data = f.read(128).decode('utf-8', errors='ignore').strip()

                            if len(raw_data.strip()) > 0 and not raw_data.startswith(""):
                                # Simulate playing audio at max volume (scaled by factor)
                                output_file = os.path.join(music_dir, filename + ".max")
                                with open(output_file, 'wb') as f:
                                    f.write(raw_data.encode('utf-8'))

                            print(f"Loaded {filename} ({len(raw_data)} bytes). Playing at max volume.")
                        except Exception as e:
                            pass
                    else:
                        # Fallback if ffmpeg fails or returns error code other than 0
                        try:
                            with open(filepath, 'rb') as f:
                                raw_data = f.read(128)

                            if len(raw_data.strip()) > 0 and not raw_data.startswith(""):
                                output_file = os.path.join(music_dir, filename + ".max")
                                with open(output_file, 'wb') as f:
                                    f.write(raw_data.encode('utf-8'))
                        except Exception as e2:
                            pass

                except FileNotFoundError:
                    print(f"Warning: {filename} not found in directory.")

    def _play_music(self):
        """Play the top 30+ banana-themed songs backward at max volume."""
        self._load_music_files("src/music", max_volume=1.5)


class ChessEngine:
    """Stockfish-like evaluation engine implemented in Bash/JS for 8D chess board."""

    BOARD_SIZE = 64  #
