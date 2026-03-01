#!/usr/bin/env python3
"""
Ralph Wiggum Loop Orchestrator for AI Employee - Bronze Tier

This script manages the autonomous processing loop, keeping Qwen Code
working until all tasks in Needs_Action are complete.

Based on the Ralph Wiggum pattern (adapted for Qwen Code).

Usage:
    python ralph_orchestrator.py --vault-path /path/to/vault --max-iterations 10
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


class RalphOrchestrator:
    """Manages the Ralph Wiggum autonomous processing loop."""

    def __init__(
        self,
        vault_path: Path,
        max_iterations: int = 10,
        check_interval: int = 2
    ):
        self.vault_path = vault_path
        self.max_iterations = max_iterations
        self.check_interval = check_interval

        # Folder paths
        self.needs_action = vault_path / 'Needs_Action'
        self.done = vault_path / 'Done'
        self.plans = vault_path / 'Plans'
        self.pending_approval = vault_path / 'Pending_Approval'
        self.dashboard = vault_path / 'Dashboard.md'

        # State tracking
        self.state_file = vault_path / '.ralph_state.txt'
        self.current_iteration = 0
        self.pending_tasks: list = []

        # Ensure folders exist
        for folder in [self.needs_action, self.done, self.plans, self.pending_approval]:
            folder.mkdir(parents=True, exist_ok=True)

    def get_pending_tasks(self) -> list:
        """Get list of pending task files."""
        if not self.needs_action.exists():
            return []

        pending = []
        for f in self.needs_action.glob('*.md'):
            # Skip files that are being processed
            if f.name.startswith('~'):
                continue
            pending.append(f)

        return sorted(pending, key=lambda x: x.stat().st_mtime)

    def get_task_priority(self, task_file: Path) -> str:
        """Extract priority from task file frontmatter."""
        try:
            content = task_file.read_text()
            if 'priority: high' in content.lower():
                return 'high'
            elif 'priority: medium' in content.lower():
                return 'medium'
            return 'low'
        except Exception:
            return 'unknown'

    def create_state_file(self, prompt: str) -> Path:
        """Create a state file for Claude to process."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        state_file = self.plans / f'RALPH_STATE_{timestamp}.md'

        content = f"""---
type: ralph_state
created: {datetime.now().isoformat()}
iteration: {self.current_iteration}
status: pending
---

# Ralph Wiggum Processing State

## Current Prompt

{prompt}

## Pending Tasks

{chr(10).join(f'- {t.name}' for t in self.pending_tasks)}

## Instructions for Claude

1. Read Company_Handbook.md for rules of engagement
2. Process tasks in priority order (high → medium → low)
3. For each task:
   - Read the action file
   - Take appropriate action
   - Update Dashboard.md
   - Move completed task to /Done
4. When all tasks are complete, output: <promise>TASK_COMPLETE</promise>
5. If more iterations needed, explain what remains

## Completion Criteria

- All files moved from /Needs_Action to /Done
- Dashboard.md updated with activity
- Any approval requests moved to /Pending_Approval
"""

        state_file.write_text(content)
        return state_file

    def check_completion(self) -> Tuple[bool, str]:
        """
        Check if the task is complete.

        Returns:
            Tuple of (is_complete, reason)
        """
        pending = self.get_pending_tasks()

        if not pending:
            return True, "All tasks processed - Needs_Action is empty"

        # Check for approval requests (these don't block completion)
        approval_count = len(list(self.pending_approval.glob('*.md')))

        return False, f"{len(pending)} tasks pending, {approval_count} awaiting approval"

    def update_dashboard(self, action: str, details: str = ""):
        """Update the Dashboard.md with recent activity."""
        if not self.dashboard.exists():
            logger.warning("Dashboard.md not found")
            return

        try:
            content = self.dashboard.read_text()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Find the activity log section and add entry
            if '## 📝 Recent Activity Log' in content:
                lines = content.split('\n')
                new_lines = []
                for i, line in enumerate(lines):
                    new_lines.append(line)
                    if '| Time | Action | Status |' in line:
                        # Add new entry after header
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

    def move_to_done(self, task_file: Path):
        """Move a completed task file to the Done folder."""
        try:
            dest = self.done / task_file.name
            shutil.move(str(task_file), str(dest))
            logger.info(f"Moved to Done: {task_file.name}")
            return True
        except Exception as e:
            logger.error(f"Failed to move {task_file.name}: {e}")
            return False

    def run_iteration(self, prompt: str) -> bool:
        """
        Run one iteration of the Ralph loop.

        Returns:
            True if should continue, False if complete
        """
        self.current_iteration += 1
        logger.info(f"{'='*60}")
        logger.info(f"Ralph Loop - Iteration {self.current_iteration}/{self.max_iterations}")
        logger.info(f"{'='*60}")

        # Get pending tasks
        self.pending_tasks = self.get_pending_tasks()

        if not self.pending_tasks:
            logger.info("No pending tasks - loop complete!")
            self.update_dashboard("Ralph loop completed", "All tasks processed")
            return False

        # Log task summary
        high_priority = [t for t in self.pending_tasks if self.get_task_priority(t) == 'high']
        logger.info(f"Pending tasks: {len(self.pending_tasks)} ({len(high_priority)} high priority)")

        # Create state file for Claude
        state_file = self.create_state_file(prompt)
        logger.info(f"Created state file: {state_file.name}")

        # Output the prompt for Qwen
        print("\n" + "="*60)
        print(f"QWEN PROMPT - Iteration {self.current_iteration}")
        print("="*60)
        print(f"""
🤖 AI Employee - Process Pending Tasks

**Current State**: {len(self.pending_tasks)} tasks in /Needs_Action

**Your Task**:
1. Read /Company_Handbook.md for rules
2. Process tasks from /Needs_Action in priority order
3. For each task:
   - Review the action file
   - Take appropriate action per Company_Handbook.md
   - Update Dashboard.md
   - Move completed items to /Done

**Pending Files**:
{chr(10).join(f'  - {t.name} ({self.get_task_priority(t)} priority)' for t in self.pending_tasks)}

**Completion**: When all tasks are processed, output: <promise>TASK_COMPLETE</promise>

---
State file: {state_file}
""")
        print("="*60 + "\n")

        return True

    def run(self, initial_prompt: str = "Process all files in /Needs_Action"):
        """Run the full Ralph loop."""
        logger.info("="*60)
        logger.info("AI Employee - Ralph Wiggum Loop Orchestrator")
        logger.info("="*60)
        logger.info(f"Vault: {self.vault_path}")
        logger.info(f"Max Iterations: {self.max_iterations}")
        logger.info("Press Ctrl+C to stop")
        logger.info("="*60)

        try:
            while self.current_iteration < self.max_iterations:
                should_continue = self.run_iteration(initial_prompt)

                if not should_continue:
                    logger.info("✅ Loop completed successfully!")
                    return 0

                # In a real implementation, this would invoke Qwen here
                # For now, we wait for manual Qwen invocation
                logger.info("Waiting for Qwen to process... (invoke manually or integrate)")
                logger.info("After Qwen processes, re-run this script to continue")

                # For demo purposes, break after first iteration
                # In production, this would integrate with Claude Code API
                break

        except KeyboardInterrupt:
            logger.info("\n⚠️ Loop interrupted by user")
            return 1

        logger.info(f"Loop ended after {self.current_iteration} iterations")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description='Ralph Wiggum Loop Orchestrator for AI Employee'
    )
    parser.add_argument(
        '--vault-path',
        type=str,
        default='/home/alina/Hackathon_4/FTE/AI_Employee_Vault',
        help='Path to the Obsidian vault (default: /home/alina/Hackathon_4/FTE/AI_Employee_Vault)'
    )
    parser.add_argument(
        '--max-iterations',
        type=int,
        default=10,
        help='Maximum number of iterations (default: 10)'
    )
    parser.add_argument(
        '--prompt',
        type=str,
        default='Process all files in /Needs_Action',
        help='Initial processing prompt'
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

    orchestrator = RalphOrchestrator(
        vault_path=vault_path,
        max_iterations=args.max_iterations
    )

    sys.exit(orchestrator.run(args.prompt))


if __name__ == '__main__':
    main()
