"""
KB Manager Autoload Test

This script checks if the Knowledge Base (KB) can automatically discover and
parse existing documents in the `data/` directory upon initialization.
"""
import sys
import os

# Add the project root to sys.path so we can import modules from src/
sys.path.append(os.path.abspath("."))
from src.utils.kb_manager import KBManager

# Initialize the KB Manager and display the status of loaded files.
kb = KBManager()
print(f"--- SamiX Knowledge Base Stats ---")
print(f"Total files detected: {len(kb.files)}")

for f in kb.files:
    print(f" - {f.filename:30} | Chunks: {f.chunks:3} | Indexed: {f.indexed}")
