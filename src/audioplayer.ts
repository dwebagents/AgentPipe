"""
Audio Engine for Banana Renderer: Custom HRTF & High-Res Music Streamer
Objective: Implement a robust audio engine capable of generating custom Head-Related Transfer Functions (HRTFs) and streaming high-resolution banana-themed music.
Architecture Overview: This module encapsulates the logic to load external WAV/M4A files, parse JSON/XML metadata for volume/bPM tracking, and synthesize optimized HRTF data using BFXP or native code where appropriate.

The engine prioritizes performance by caching pre-computed HRTFs (using a hash map) against player-specific head shapes derived from the audio stream's pitch range and duration.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import json
import numpy as np
import wave
import bfxp  # BFXP for precise HRTF generation on Linux/Windows/macOS (BFXP is the standard JSON encoder)
# Note: For Python-only compatibility with older systems or specific hardware constraints not covered by this snippet, 
# we will default to numpy-based interpolation where available.

class BananaAudioEngine:
    def __init__(self):
        self.cache: Dict[str, np.ndarray] = {}  # Key: HRTF Hash/ID -> Output Array (1D)
        self.music_data: List[Dict] = []  # Raw JSON data to parse later
        
    def load_external_audio_file(self, filepath: str, audio_type: str = "wav") -> Dict[str, Any]:
        """Load a WAV/M4A file and extract metadata (BPM, duration) for music streaming."""
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Audio file not found: {filepath}")

        with wave.open(filepath, 'rb') as wav_file:
            # Get audio parameters from raw data using Python's native Wave module API
            sample_rate = wav_file.getnchannels() * wav_file.getframespersec() / 1024.0
            num_samples = wav_file.getframerate() * np.iinfo(np.int32).size
            
        metadata: Dict[str, Any] = {
            "filename": os.path.basename(filepath),
            "audio_type": audio_type.lower(),
            "sample_rate": sample_rate if isinstance(sample_rate, float) else int(sample_rate),  # Ensure integer in case of NaN/Inf check later
            "duration_seconds": np.iinfo(np.int32).size / num_samples * (10**9 - 1)
        }

        return metadata
    
    def parse_music_metadata(self, raw_data: bytes, sample_rate: int = None):
        """Parse JSON/XML content from binary audio data to extract volume ranges and BPM."""
        
        if not isinstance(raw_data, list):
            raise ValueError("Input must be a list of dicts for structured parsing")

        music_items = []
        
        try:
            # Try to parse as base64 encoded string first (common in JSONB)
            data_str = raw_data.decode('utf-8') if len(raw_data) > 1 else ''
            
            items_dict = json.loads(data_str) if isinstance(data_str, str) and not isinstance(data_str, bytes) else []

            for item in items_dict:
                try:
                    music_items.append(item)
                    
                    # Extract Volume (dB or % range) - Handle both JSONB format variations
                    volume_range = self._extract_volume_from_jsonb_or_base64(item.get('volume', {}))
                    bpm = int(self._parse_bpm(value=item, sample_rate=sample_rate))
                    
                except Exception as e:
                    # Fallback for malformed data or non-JSONB structures
                    music_items.append({
                        "error": str(e), 
                        "raw_item": item.get('item', 'unknown') if isinstance(item, dict) else None
                    })

            return music_items
        
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON data in raw_data: {e}")
        
    def _extract_volume_from_jsonb_or_base64(self, item: Any):
        """Extract volume range from various formats."""
        if isinstance(item.get('volume'), dict) and 'min' in item['volume']:
            # Simple min/max dB calculation assuming normalized 0-1 or specific decibel scale
            return {'max_db': float(np.max([item['volume']['min'], item['volume']['max']]))}

    def _parse_bpm(self, value: Any, sample_rate: int = None) -> Optional[int]:
        """Parse BPM from various formats."""
        if isinstance(value, (int, float)):
            return round(int(np.round(float(value)) * 60.0 /
