#!/usr/bin/env python3
"""
File System Watcher for AI Employee - Bronze Tier

This watcher monitors a drop folder for new files and creates
actionable .md files in the Needs_Action folder for Qwen to process.

Usage:
    python filesystem_watcher.py --vault-path /path/to/vault --drop-folder /path/to/drop

Requirements:
    pip install watchdog
"""

import argparse
import hashlib
import logging
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DropFolderHandler(FileSystemEventHandler):
    """Handles file creation events in the drop folder."""

    def __init__(self, vault_path: Path, processed_file: Path):
        super().__init__()
        self.vault_path = vault_path
        self.needs_action = vault_path / 'Needs_Action'
        self.processed_file = processed_file
        self.processed_hashes: set = set()

        # Ensure Needs_Action folder exists
        self.needs_action.mkdir(parents=True, exist_ok=True)

        # Load previously processed file hashes
        self._load_processed_hashes()

    def _load_processed_hashes(self):
        """Load hashes of already processed files to avoid duplicates."""
        if self.processed_file.exists():
            content = self.processed_file.read_text()
            self.processed_hashes = set(line.strip() for line in content.splitlines() if line.strip())
            logger.info(f"Loaded {len(self.processed_hashes)} previously processed file hashes")

    def _save_hash(self, file_hash: str):
        """Save a file hash to the processed list."""
        self.processed_hashes.add(file_hash)
        with open(self.processed_file, 'a') as f:
            f.write(f"{file_hash}\n")

    def _calculate_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _get_file_size(self, size_bytes: int) -> str:
        """Convert bytes to human-readable format."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.2f} TB"

    def _detect_priority(self, filename: str, content: str = "") -> str:
        """Detect priority based on filename and content."""
        filename_lower = filename.lower()
        content_lower = content.lower()

        # High priority keywords
        high_priority = ['urgent', 'asap', 'emergency', 'invoice', 'payment', 'deadline']
        for keyword in high_priority:
            if keyword in filename_lower or keyword in content_lower:
                return 'high'

        # Medium priority keywords
        medium_priority = ['important', 'review', 'action required', 'follow up']
        for keyword in medium_priority:
            if keyword in filename_lower or keyword in content_lower:
                return 'medium'

        return 'low'

    def _detect_type(self, filename: str) -> str:
        """Detect the type of file based on extension and name."""
        filename_lower = filename.lower()

        if filename_lower.endswith(('.pdf', '.doc', '.docx')):
            return 'document'
        elif filename_lower.endswith(('.txt', '.md')):
            return 'text'
        elif filename_lower.endswith(('.jpg', '.jpeg', '.png', '.gif')):
            return 'image'
        elif filename_lower.endswith(('.xls', '.xlsx', '.csv')):
            return 'spreadsheet'
        elif 'invoice' in filename_lower:
            return 'invoice'
        elif 'contract' in filename_lower:
            return 'contract'
        else:
            return 'file'

    def on_created(self, event):
        """Handle file creation events."""
        if event.is_directory:
            return

        source_path = Path(event.src_path)
        logger.info(f"New file detected: {source_path.name}")

        # Wait a moment for file to be fully written
        time.sleep(0.5)

        try:
            # Calculate hash to check if already processed
            file_hash = self._calculate_hash(source_path)
            if file_hash in self.processed_hashes:
                logger.debug(f"File already processed: {source_path.name}")
                return

            # Read content if text file
            content = ""
            if source_path.suffix.lower() in ['.txt', '.md', '.csv']:
                try:
                    content = source_path.read_text()
                except Exception as e:
                    logger.warning(f"Could not read text content: {e}")

            # Create action file
            action_file = self.create_action_file(source_path, content, file_hash)
            logger.info(f"Created action file: {action_file}")

            # Save hash
            self._save_hash(file_hash)

        except Exception as e:
            logger.error(f"Error processing file {source_path.name}: {e}")

    def create_action_file(self, source: Path, content: str, file_hash: str) -> Path:
        """Create a .md action file in Needs_Action folder."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_type = self._detect_type(source.name)
        priority = self._detect_priority(source.name, content)

        # Generate unique filename
        safe_name = source.stem.replace(' ', '_').replace('-', '_')
        action_filename = f"FILE_{file_type.upper()}_{safe_name}_{timestamp}.md"
        action_path = self.needs_action / action_filename

        # Copy original file to vault
        files_folder = self.vault_path / 'Files'
        files_folder.mkdir(parents=True, exist_ok=True)
        copied_file = files_folder / f"{safe_name}_{timestamp}{source.suffix}"
        shutil.copy2(source, copied_file)

        # Create markdown action file
        action_content = f"""---
type: file_drop
original_name: {source.name}
file_type: {file_type}
size: {self._get_file_size(source.stat().st_size)}
received: {datetime.now().isoformat()}
priority: {priority}
status: pending
file_hash: {file_hash}
---

# File Drop for Processing

## File Information

- **Original Name**: {source.name}
- **Type**: {file_type}
- **Size**: {self._get_file_size(source.stat().st_size)}
- **Received**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Priority**: {priority.upper()}

## File Location

Copied to: `Files/{copied_file.name}`

## Content Preview

```
{content[:500] if content else "(Binary file - no preview available)"}
```

## Required Actions

- [ ] Review file content
- [ ] Categorize and tag appropriately
- [ ] Take necessary action or file for reference
- [ ] Move to /Done when complete

## Notes

_Add any processing notes here_
"""

        action_path.write_text(action_content)
        return action_path


def main():
    parser = argparse.ArgumentParser(description='File System Watcher for AI Employee')
    parser.add_argument(
        '--vault-path',
        type=str,
        default='/home/alina/Hackathon_4/FTE/AI_Employee_Vault',
        help='Path to the Obsidian vault (default: /home/alina/Hackathon_4/FTE/AI_Employee_Vault)'
    )
    parser.add_argument(
        '--drop-folder',
        type=str,
        default=None,
        help='Path to the drop folder (default: vault_path/Inbox)'
    )
    parser.add_argument(
        '--check-interval',
        type=int,
        default=5,
        help='Check interval in seconds (default: 5)'
    )
    parser.add_argument(
        '--log-level',
        type=str,
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        help='Logging level'
    )

    args = parser.parse_args()

    # Set log level
    logger.setLevel(getattr(logging, args.log_level.upper()))

    vault_path = Path(args.vault_path).resolve()
    if not vault_path.exists():
        logger.error(f"Vault path does not exist: {vault_path}")
        sys.exit(1)

    drop_folder = Path(args.drop_folder).resolve() if args.drop_folder else vault_path / 'Inbox'
    drop_folder.mkdir(parents=True, exist_ok=True)

    processed_file = vault_path / '.processed_files.txt'

    logger.info("=" * 60)
    logger.info("AI Employee - File System Watcher (Bronze Tier)")
    logger.info("=" * 60)
    logger.info(f"Vault Path: {vault_path}")
    logger.info(f"Drop Folder: {drop_folder}")
    logger.info(f"Check Interval: {args.check_interval}s")
    logger.info("Press Ctrl+C to stop")
    logger.info("=" * 60)

    # Create event handler and observer
    event_handler = DropFolderHandler(vault_path, processed_file)
    observer = Observer()
    observer.schedule(event_handler, str(drop_folder), recursive=False)

    # Start watching
    observer.start()
    logger.info("Watcher started - monitoring for new files...")

    try:
        while True:
            time.sleep(args.check_interval)
    except KeyboardInterrupt:
        logger.info("\nStopping watcher...")
        observer.stop()

    observer.join()
    logger.info("Watcher stopped")


if __name__ == '__main__':
    main()
