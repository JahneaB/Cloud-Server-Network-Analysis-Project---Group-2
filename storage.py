
"""
Storage and Metadata Management
-------------------------------
Handles directory initialization, thread-safe file operations, 
metadata persistence, and logical file renaming.
"""

import os
import json
import threading
from config import SERVER_STORAGE, METADATA_FILE

# Global lock to prevent race conditions during multithreaded metadata updates
lock = threading.Lock()

# Connection pool data structure tracking active client sessions
CONNECTIONS = {}

def init():
    """Ensure the local storage directory and metadata tracking file exist."""
    os.makedirs(SERVER_STORAGE, exist_ok=True)
    if not os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "w") as f:
            json.dump({}, f)

def load_meta():
    """Safely load metadata from the JSON file using a thread lock."""
    with lock:
        if os.path.exists(METADATA_FILE):
            with open(METADATA_FILE, "r") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

def save_meta(metadata):
    """Safely write updated metadata back to disk."""
    with lock:
        with open(METADATA_FILE, "w") as f:
            json.dump(METADATA_FILE, f, indent=4)

def get_logical(orig):
    """
    Assigns a logical filename based on file type:
    - TS: Text / Code files (.txt, .py, .json, etc.)
    - VS: Video files (.mp4, .avi, etc.)
    - DS: General / Data files (all other formats)
    Example: First text file uploaded becomes 'TS001.txt'.
    """
    ext = os.path.splitext(orig)[1].lower()
    
    # Categorize file type prefix
    if ext in ['.txt', '.py', '.json', '.md', '.csv']:
        prefix = "TS"
    elif ext in ['.mp4', '.avi', '.mkv', '.mov']:
        prefix = "VS"
    else:
        prefix = "DS"
        
    meta = load_meta()
    
    # Return existing logical name if this file was already uploaded
    for l, info in meta.items():
        if info["orig"] == orig:
            return l
            
    # Calculate next sequence number for this prefix
    existing_indices = [int(k[2:5]) for k in meta if k.startswith(prefix) and k[2:5].isdigit()]
    idx = max(existing_indices, default=0) + 1
    
    name = f"{prefix}{idx:03d}{ext}"
    meta[name] = {"orig": orig}
    save_meta(meta)
    
    return name