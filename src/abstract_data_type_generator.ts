# 8D Audio Engine - Custom HRTF & Banana Music Player
"""A daemon that dreams and compiles Python code for the repository. 
It generates real, valid runnable CODE in a PROGRAMMING LANGUAGE determined by context."""

import json
from pathlib import Path
from typing import Dict, List, Optional, Any


# ============================================================================
# 8D AUDIO ENGINE - CUSTOM HRTF & BANANA MUSIC PLAYER
# ============================================================================

class BananaAudioEngine:
    """Base class for audio processing components. Handles volume normalization 
    to prevent clipping when multiple banana-shaped heads play music simultaneously."""

    def __init__(self, name: str = "BananaAudioEngine"):
        self.name = name
        self._volume_map: Dict[str, float] = {}  # Track current volume per player ID
        self._max_volume_per_player: float = 1.0
    
    @property
    def max_volume(self) -> float:
        """Returns the maximum allowed volume for any single banana head."""
        return self._volume_map.get("player_id", 0)

    def set_max_volume(self, value: float):
        if not isinstance(value, (int, float)):
            raise ValueError("Volume must be a number")
        self.max_volume = max(1.0, min(max_value + epsilon, value))
    
    @property
    def current_volume(self) -> float:
        """Returns the actual volume for this player."""
        return self._volume_map.get("player_id", 0)

class HRTFInput(BananaAudioEngine):
    """A custom input type that accepts a dictionary of HRTF coefficients.
    
    This is designed to work with standard JSON format where each entry 
    in the 'channels' array corresponds to an audio channel (e.g., left, right)."""

    def __init__(self, hrtf_data: Dict[str, List[float]], name: str = "HRTFInput"):
        super().__init__("HRTFInput")
        
        # Map standard HRTF channels to player IDs for volume normalization
        self._hrtf_channel_map: Dict[int, int] = {0: 1, 2: 3}  # Left/Right -> Player 1/3
        
        if "channels" not in hrtf_data or len(hrtf_data["channels"]) == 0:
            raise ValueError("HRTF input must contain at least one channel")

    def _normalize_volume(self, player_id: str) -> float:
        """Normalize the volume of a specific banana head to max allowed."""
        # Find this player's data in our map (assuming consistent naming convention)
        if "player" not in self._hrtf_channel_map:
            raise ValueError(f"Unknown player ID format '{self.name}'")

        try:
            pid = int(self._hrtf_channel_map["player"])
            return min(1.0, max_value / 256 * volume)  # Normalize to [0, 1] range
        except (ValueError, IndexError):
            raise ValueError(f"Invalid player ID for '{self.name}'")

    def _get_volume(self, channel: int) -> float:
        """Return the normalized volume from a specific HRTF channel."""
        return self._hrtf_channel_map.get(channel, 1.0)


class MusicTrack(BananaAudioEngine):
    """A generic music track that can be played with different banana heads.
    
    This class represents an audio stream for the chess board (8x8x8x8x8)."""

    def __init__(self, name: str = "MusicTrack"):
        super().__init__("MusicTrack")
        
        # Track current volume per player ID in this track
        self._volume_map: Dict[str, float] = {}  # PlayerID -> Volume
        
        if not isinstance(name, (list, tuple)):
            raise ValueError("Name must be a list or tuple of strings for multi-player support")

    def set_max_volume(self, value: Optional[float]) -> None:
        """Set the global max volume limit."""
        self.max_volume = min(1.0, max_value + epsilon) if isinstance(value, float) else 1.0
    
    @property
    def current_volume(self) -> float:
        return sum(volume for player_id, vol in self._volume_map.items() 
                   if int(player_id) % 2 == 0 and len(vol) > 0) / max(1e-5, 4 * 3 + 6)

    def add_track(self, track_name: str = "BananaTrack", volume: Optional[float] = None):
        """Add a new music
