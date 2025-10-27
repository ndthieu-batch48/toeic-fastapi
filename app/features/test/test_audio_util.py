"""Audio file utilities for handling TOEIC test audio files"""

import os
from pathlib import Path
from typing import Optional


def get_audio_base_path() -> Path:
    """
    Get the base path for audio files.
    Expected structure: C:\\TOEIC_NEW\\DB\\media\\assets
    """
    # Get the project root (C:\TOEIC_NEW\toeic-fastapi)
    current_file = Path(__file__)
    project_root = current_file.parent.parent.parent
    
    # Navigate to C:\TOEIC_NEW\DB\media\assets
    audio_base_path = project_root.parent / "DB" / "media" / "assets"
    
    return audio_base_path


def resolve_audio_file_path(relative_audio_url: str) -> Optional[str]:  # Change to str
    """
    Convert relative audio URL to absolute file system path.
    
    Args:
        relative_audio_url: URL like "assets/Full_trial_test_-_Batch_1_2025/JIM_s_TOEIC_LC_TEST_05-_Part_1.mp3"
    
    Returns:
        Absolute path string to the audio file if it exists, None otherwise
    """
    if not relative_audio_url:
        return None
    
    # Remove 'assets/' prefix if present
    if relative_audio_url.startswith('assets/'):
        relative_path = relative_audio_url[7:]
    else:
        relative_path = relative_audio_url
    
    # Get base path and construct full path
    base_path = get_audio_base_path()
    full_path = base_path / relative_path
    
    # Check if file exists
    if full_path.exists() and full_path.is_file():
        return str(full_path)
    
    return None
