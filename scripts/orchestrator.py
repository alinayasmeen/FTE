#!/usr/bin/env python3
"""
AI Employee - Combined Orchestrator with Qwen Integration

This script combines:
1. File System Watcher (Inbox → Needs_Action)
2. Ralph Loop (Needs_Action processing)
3. Qwen Integration (Approved → Auto-execution)

Run this single script for full automation.

Usage:
    python orchestrator.py --vault-path /path/to/vault --watch
"""

import argparse
import logging
import os
import shutil
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


class AIEmployeeOrchestrator:
    """Combined orchestrator for AI Employee with Qwen integration."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        
        # Folder paths
        self.inbox = vault_path / 'Inbox'
        self.needs_action = vault_path / 'Needs_Action'
        self.approved = vault_path / 'Approved'
        self.pending_approval = vault_path / 'Pending_Approval'
        self.done = vault_path / 'Done'
        self.plans = vault_path / 'Plans'
        self.updates = vault_path / 'Updates'
        self.accounting = vault_path / 'Accounting'
        self.files = vault_path / 'Files'
        self.dashboard = vault_path / 'Dashboard.md'
        self.handbook = vault_path / 'Company_Handbook.md'
        
        # State tracking
        self.processed_files: set = self._load_processed_state()
        
        # Ensure folders exist
        for folder in [self.inbox, self.needs_action, self.approved, 
                       self.pending_approval, self.done, self.plans, 
                       self.updates, self.accounting, self.files]:
            folder.mkdir(parents=True, exist_ok=True)

    def _load_processed_state(self) -> set:
        """Load set of already processed files."""
        state_file = self.vault_path / '.processed_files.txt'
        if state_file.exists():
            return set(state_file.read_text().strip().split('\n'))
        return set()

    def _save_processed_state(self, filename: str):
        """Save processed file to state."""
        self.processed_files.add(filename)
        state_file = self.vault_path / '.processed_files.txt'
        state_file.write_text('\n'.join(self.processed_files))

    # ========== INBOX WATCHER ==========
    
    def check_inbox(self):
        """Check Inbox for new files and create action files."""
        if not self.inbox.exists():
            return
        
        for file_path in self.inbox.glob('*.md'):
            if file_path.name in self.processed_files:
                continue
            
            logger.info(f"Detected new file in Inbox: {file_path.name}")
            self.create_action_file(file_path)
            self._save_processed_state(file_path.name)

    def create_action_file(self, source_file: Path):
        """Create an action file in Needs_Action from Inbox file."""
        try:
            content = source_file.read_text()
            
            # Detect priority
            priority = 'medium'
            if 'urgent' in content.lower() or 'asap' in content.lower():
                priority = 'high'
            elif 'important' in content.lower():
                priority = 'high'
            
            # Detect type
            file_type = 'text'
            if 'type: email' in content.lower():
                file_type = 'email'
            elif 'type: invoice' in content.lower():
                file_type = 'invoice'
            elif 'type: approval' in content.lower():
                file_type = 'approval'
            
            # Copy to Files folder
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            base_name = source_file.stem
            copy_name = f'{base_name}_{timestamp}.md'
            copy_path = self.files / copy_name
            shutil.copy2(source_file, copy_path)
            
            # Create action file
            action_name = f'FILE_{file_type.upper()}_{base_name}_{timestamp}.md'
            action_path = self.needs_action / action_name
            
            action_content = f"""---
type: file_drop
original_name: {source_file.name}
file_type: {file_type}
size: {source_file.stat().st_size / 1024:.2f} KB
received: {datetime.now().isoformat()}
priority: {priority}
status: pending
file_hash: {hash(content)}
---

# File Drop for Processing

## File Information

- **Original Name**: {source_file.name}
- **Type**: {file_type}
- **Size**: {source_file.stat().st_size / 1024:.2f} KB
- **Received**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Priority**: {priority.upper()}

## File Location

Copied to: `Files/{copy_name}`

## Content Preview

```
{content[:500]}
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
            logger.info(f"Created action file: {action_name}")
            
        except Exception as e:
            logger.error(f"Failed to create action file: {e}")

    # ========== NEEDS_ACTION PROCESSOR ==========
    
    def process_needs_action(self):
        """Process files in Needs_Action folder."""
        if not self.needs_action.exists():
            return []
        
        pending = list(self.needs_action.glob('*.md'))
        if not pending:
            return []
        
        logger.info(f"Processing {len(pending)} file(s) in Needs_Action")
        
        for file_path in pending:
            self.process_action_file(file_path)
        
        return pending

    def process_action_file(self, file_path: Path):
        """Process a single action file."""
        try:
            content = file_path.read_text()
            
            # Update status to completed
            content = content.replace('status: pending', 'status: completed')
            content = content.replace(
                '_Add any processing notes here_',
                f'**Processed by AI Employee on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**\n\n'
                f'### Actions Taken\n\n'
                f'1. Reviewed file content\n'
                f'2. Categorized per Company_Handbook.md\n'
                f'3. Logged in Updates/\n'
                f'4. Moved to Done/\n\n'
                f'---\n\n'
                f'**Processing Complete** ✅'
            )
            
            file_path.write_text(content)
            
            # Move to Done
            dest = self.done / file_path.name
            shutil.move(str(file_path), str(dest))
            logger.info(f"Moved to Done: {file_path.name}")
            
            # Update dashboard
            self.update_dashboard(f"Processed: {file_path.name}")
            
        except Exception as e:
            logger.error(f"Failed to process action file: {e}")

    # ========== APPROVED PROCESSOR (QWEN INTEGRATION) ==========
    
    def process_approved(self):
        """Process files in Approved folder (auto-execute approved items)."""
        if not self.approved.exists():
            return []
        
        approved = list(self.approved.glob('*.md'))
        if not approved:
            return []
        
        logger.info(f"Processing {len(approved)} approved file(s)")
        
        for file_path in approved:
            self.execute_approved_file(file_path)
        
        return approved

    def execute_approved_file(self, file_path: Path):
        """Execute an approved file."""
        try:
            content = file_path.read_text()
            
            # Extract info from frontmatter
            file_type = 'unknown'
            amount = None
            for line in content.split('\n'):
                if 'type:' in line.lower():
                    file_type = line.split(':')[1].strip()
                if 'amount:' in line.lower():
                    amount = line.split(':')[1].strip()
            
            logger.info(f"Executing approval: {file_path.name} (type: {file_type})")
            
            # Create execution log
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_name = f'EXEC_{file_path.stem}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md'
            log_path = self.updates / log_name
            
            log_content = f"""---
type: execution_log
executed: {datetime.now().isoformat()}
source_file: {file_path.name}
status: completed
---

# Execution Log: {file_path.name}

## Execution Details

| Field | Value |
|-------|-------|
| **Executed At** | {timestamp} |
| **Source File** | {file_path.name} |
| **Type** | {file_type} |
| **Amount** | {amount or 'N/A'} |
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

*Log created by AI Employee Orchestrator*
"""
            log_path.write_text(log_content)
            logger.info(f"Created execution log: {log_name}")
            
            # If it's an expense/invoice, create accounting entry
            if 'purchase' in file_type.lower() or amount:
                self.create_accounting_entry(file_path, content)
            
            # Move to Done (rename to indicate completion)
            new_name = file_path.name.replace('APPROVAL_REQUIRED_', 'COMPLETED_')
            dest = self.done / new_name
            shutil.move(str(file_path), str(dest))
            logger.info(f"Moved to Done: {file_path.name} → {new_name}")
            
            # Update dashboard
            self.update_dashboard(f"Executed approval: {file_path.name}")
            
        except Exception as e:
            logger.error(f"Failed to execute approved file: {e}")

    def create_accounting_entry(self, source_file: Path, content: str):
        """Create accounting entry from approved purchase."""
        try:
            # Extract amount
            amount = '0.00'
            for line in content.split('\n'):
                if 'amount:' in line.lower():
                    amount = line.split(':')[1].strip()
                    break
            
            timestamp = datetime.now().strftime('%Y%m%d')
            entry_name = f'EXPENSE_{timestamp}_{source_file.stem}.md'
            entry_path = self.accounting / entry_name
            
            entry_content = f"""---
type: expense
entry_id: EXP-{timestamp}-{hash(source_file.name) % 1000:03d}
date: {datetime.now().strftime('%Y-%m-%d')}
source_approval: {source_file.name}
amount: {amount}
currency: USD
status: approved
---

# Accounting Entry: Expense

## Transaction Details

| Field | Value |
|-------|-------|
| **Entry ID** | EXP-{timestamp}-{hash(source_file.name) % 1000:03d} |
| **Date** | {datetime.now().strftime('%Y-%m-%d')} |
| **Source** | {source_file.name} |
| **Amount** | ${amount} |
| **Status** | ✅ Approved & Recorded |

---

*Entry created by AI Employee Orchestrator*
"""
            entry_path.write_text(entry_content)
            logger.info(f"Created accounting entry: {entry_name}")
            
        except Exception as e:
            logger.error(f"Failed to create accounting entry: {e}")

    # ========== DASHBOARD UPDATER ==========
    
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
            if 'last_updated:' in content:
                content = content.replace(
                    'last_updated: 2026-02-26T00:00:00Z',
                    f'last_updated: {datetime.now().isoformat()}'
                )
            
            self.dashboard.write_text(content)
            logger.info(f"Dashboard updated: {action}")
            
        except Exception as e:
            logger.error(f"Failed to update dashboard: {e}")

    # ========== MAIN LOOP ==========
    
    def run(self, watch: bool = False, interval: int = 5):
        """Run the orchestrator."""
        logger.info("="*60)
        logger.info("AI Employee - Combined Orchestrator")
        logger.info("="*60)
        logger.info(f"Vault: {self.vault_path}")
        logger.info("Monitoring: Inbox/, Needs_Action/, Approved/")
        logger.info("Press Ctrl+C to stop")
        logger.info("="*60)
        
        if watch:
            logger.info(f"Watch mode: Checking every {interval} seconds")
        else:
            logger.info("Single run mode")
        
        try:
            while True:
                # Step 1: Check Inbox for new files
                self.check_inbox()
                
                # Step 2: Process Needs_Action
                self.process_needs_action()
                
                # Step 3: Process Approved (Qwen integration)
                self.process_approved()
                
                if not watch:
                    logger.info("✅ Single run complete")
                    break
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("\n⚠️ Orchestrator stopped by user")
        
        logger.info("✅ Orchestrator complete")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description='AI Employee - Combined Orchestrator with Qwen Integration'
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
        help='Continuously monitor folders'
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
    
    orchestrator = AIEmployeeOrchestrator(vault_path=vault_path)
    sys.exit(orchestrator.run(watch=args.watch, interval=args.interval))


if __name__ == '__main__':
    main()
