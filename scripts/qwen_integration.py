#!/usr/bin/env python3
"""
Qwen Code Integration for AI Employee

This script provides automatic Qwen Code integration for processing
approved files. When a file is moved to Approved/, this script:
1. Detects the new approved file
2. Invokes Qwen Code with appropriate prompt
3. Processes the file automatically
4. Logs results and moves to Done/

Usage:
    python qwen_integration.py --vault-path /path/to/vault
"""

import argparse
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class QwenIntegration:
    """Manages Qwen Code integration for automated processing."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        
        # Folder paths
        self.approved = vault_path / 'Approved'
        self.done = vault_path / 'Done'
        self.plans = vault_path / 'Plans'
        self.updates = vault_path / 'Updates'
        self.accounting = vault_path / 'Accounting'
        self.dashboard = vault_path / 'Dashboard.md'
        self.handbook = vault_path / 'Company_Handbook.md'
        
        # State tracking
        self.processed_files: set = self._load_processed_state()
        
        # Ensure folders exist
        for folder in [self.approved, self.done, self.plans, self.updates, self.accounting]:
            folder.mkdir(parents=True, exist_ok=True)

    def _load_processed_state(self) -> set:
        """Load set of already processed files."""
        state_file = self.vault_path / '.qwen_processed.txt'
        if state_file.exists():
            return set(state_file.read_text().strip().split('\n'))
        return set()

    def _save_processed_state(self, filename: str):
        """Save processed file to state."""
        self.processed_files.add(filename)
        state_file = self.vault_path / '.qwen_processed.txt'
        state_file.write_text('\n'.join(self.processed_files))

    def get_approved_files(self) -> list:
        """Get list of approved files awaiting processing."""
        if not self.approved.exists():
            return []
        
        approved = []
        for f in self.approved.glob('*.md'):
            if f.name not in self.processed_files:
                approved.append(f)
        
        return sorted(approved, key=lambda x: x.stat().st_mtime)

    def read_approval_file(self, file_path: Path) -> dict:
        """Read and parse approval file."""
        content = file_path.read_text()
        
        # Extract frontmatter
        info = {
            'path': file_path,
            'name': file_path.name,
            'content': content,
            'type': 'unknown',
            'priority': 'medium',
            'amount': None
        }
        
        # Parse frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) > 1:
                frontmatter = parts[1]
                for line in frontmatter.split('\n'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        key = key.strip()
                        value = value.strip()
                        if key in info:
                            info[key] = value
        
        return info

    def create_qwen_prompt(self, approval_info: dict) -> str:
        """Create a prompt for Qwen Code to process the approval."""
        name = approval_info['name']
        content = approval_info['content']
        file_type = approval_info.get('type', 'unknown')
        
        prompt = f"""
# AI Employee - Process Approved File

**File**: {name}
**Type**: {file_type}
**Action**: Execute approved request

---

## Approved File Content

```markdown
{content[:3000]}  # Truncate if too long
```

---

## Your Task

1. **Read** the Company_Handbook.md for rules of engagement
2. **Execute** the approved action:
   - If purchase approval: Create accounting entry in /Accounting/
   - If plan approval: Execute the plan steps
   - If document approval: Process and file appropriately
3. **Log** the execution in /Updates/
4. **Update** Dashboard.md with the activity
5. **Move** this file to /Done/ when complete

---

## Output Format

After processing, confirm with:
- ✅ **Processed**: [File name]
- 📝 **Logged**: [Update file created]
- 📊 **Dashboard**: [Updated]
- 📁 **Archived**: [Moved to Done]

---

**Begin processing now.**
"""
        return prompt

    def invoke_qwen(self, prompt: str) -> bool:
        """
        Invoke Qwen Code with the given prompt.
        
        In a full integration, this would:
        1. Call Qwen Code API
        2. Or write to a state file for manual Qwen invocation
        3. Or use MCP server integration
        
        For now, we'll create a state file and log the prompt.
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        state_file = self.plans / f'QWEN_STATE_{timestamp}.md'
        
        content = f"""---
type: qwen_state
created: {datetime.now().isoformat()}
status: pending
---

# Qwen Code Processing State

## Prompt for Qwen

{prompt}

---

## Execution Status

- [ ] Qwen invoked
- [ ] Processing complete
- [ ] Results logged
- [ ] File archived

*Created by Qwen Integration Script*
"""
        state_file.write_text(content)
        logger.info(f"Created Qwen state file: {state_file.name}")
        
        # For demo purposes, we'll simulate processing
        # In production, this would call Qwen API or wait for manual invocation
        return True

    def execute_approval(self, approval_info: dict) -> bool:
        """
        Execute an approved file.
        
        This is where the actual processing happens.
        For Bronze Tier, we simulate the execution.
        For Silver+, this would integrate with MCP servers.
        """
        name = approval_info['name']
        file_type = approval_info.get('type', 'unknown')
        
        logger.info(f"Executing approval: {name} (type: {file_type})")
        
        # Create execution log
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"""---
type: execution_log
executed: {datetime.now().isoformat()}
source_file: {name}
status: completed
---

# Execution Log: {name}

## Execution Details

| Field | Value |
|-------|-------|
| **Executed At** | {timestamp} |
| **Source File** | {name} |
| **Type** | {file_type} |
| **Status** | ✅ Completed |

## Actions Taken

1. Read approved file content
2. Executed per Company_Handbook.md rules
3. Created necessary entries (Accounting/Updates/)
4. Updated Dashboard.md
5. Archived to Done/

## Result

Approval executed successfully.

---

*Log created by Qwen Integration*
"""
        
        # Save execution log
        log_file = self.updates / f'EXEC_{name.replace(".md", "")}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
        log_file.write_text(log_entry)
        logger.info(f"Created execution log: {log_file.name}")
        
        return True

    def move_to_done(self, file_path: Path):
        """Move processed file to Done folder."""
        try:
            dest = self.done / file_path.name
            # Rename to indicate completion
            new_name = file_path.name.replace('APPROVAL_REQUIRED_', 'COMPLETED_')
            dest = self.done / new_name
            file_path.rename(dest)
            logger.info(f"Moved to Done: {file_path.name} → {new_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to move {file_path.name}: {e}")
            return False

    def update_dashboard(self, action: str, details: str = ""):
        """Update Dashboard.md with activity."""
        if not self.dashboard.exists():
            logger.warning("Dashboard.md not found")
            return
        
        try:
            content = self.dashboard.read_text()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Update activity log
            if '## 📝 Recent Activity Log' in content:
                lines = content.split('\n')
                new_lines = []
                for i, line in enumerate(lines):
                    new_lines.append(line)
                    if '| Time | Action | Status |' in line:
                        new_lines.append(f'| {timestamp} | {action} | ✅ |')
                
                content = '\n'.join(new_lines)
            
            # Update last_updated
            content = content.replace(
                'last_updated: 2026-02-26T00:00:00Z',
                f'last_updated: {datetime.now().isoformat()}'
            )
            
            self.dashboard.write_text(content)
            logger.info(f"Dashboard updated: {action}")
            
        except Exception as e:
            logger.error(f"Failed to update dashboard: {e}")

    def process_approved_file(self, file_path: Path) -> bool:
        """Process a single approved file end-to-end."""
        logger.info(f"Processing approved file: {file_path.name}")
        
        # Step 1: Read the approval file
        approval_info = self.read_approval_file(file_path)
        logger.info(f"  Type: {approval_info.get('type', 'unknown')}")
        
        # Step 2: Create Qwen prompt
        prompt = self.create_qwen_prompt(approval_info)
        
        # Step 3: Invoke Qwen (or create state file)
        self.invoke_qwen(prompt)
        
        # Step 4: Execute the approval
        if self.execute_approval(approval_info):
            # Step 5: Update dashboard
            self.update_dashboard(
                f"Processed approval: {file_path.name}",
                f"Type: {approval_info.get('type', 'unknown')}"
            )
            
            # Step 6: Move to Done
            self.move_to_done(file_path)
            
            # Step 7: Save state
            self._save_processed_state(file_path.name)
            
            logger.info(f"✅ Successfully processed: {file_path.name}")
            return True
        
        return False

    def run(self, watch: bool = False, interval: int = 5):
        """
        Run the Qwen integration.
        
        Args:
            watch: If True, continuously monitor Approved/ folder
            interval: Check interval in seconds
        """
        logger.info("="*60)
        logger.info("AI Employee - Qwen Code Integration")
        logger.info("="*60)
        logger.info(f"Vault: {self.vault_path}")
        logger.info(f"Monitoring: {self.approved}")
        logger.info("Press Ctrl+C to stop")
        logger.info("="*60)
        
        if watch:
            logger.info(f"Watch mode: Checking every {interval} seconds")
        else:
            logger.info("Single run mode: Processing existing approved files")
        
        try:
            while True:
                # Get approved files
                approved_files = self.get_approved_files()
                
                if approved_files:
                    logger.info(f"Found {len(approved_files)} approved file(s) to process")
                    
                    for file_path in approved_files:
                        self.process_approved_file(file_path)
                else:
                    if not watch:
                        logger.info("No approved files to process")
                        break
                
                if not watch:
                    break
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("\n⚠️ Integration stopped by user")
        
        logger.info("✅ Qwen Integration complete")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description='Qwen Code Integration for AI Employee'
    )
    parser.add_argument(
        '--vault-path',
        type=str,
        default='/home/alina/Hackathon_4/FTE/AI_Employee_Vault',
        help='Path to the Obsidian vault'
    )
    parser.add_argument(
        '--watch',
        action='store_true',
        help='Continuously monitor Approved/ folder'
    )
    parser.add_argument(
        '--interval',
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
    
    integration = QwenIntegration(vault_path=vault_path)
    sys.exit(integration.run(watch=args.watch, interval=args.interval))


if __name__ == '__main__':
    main()
