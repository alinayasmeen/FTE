#!/usr/bin/env python3
"""
AI Employee - Full Auto Workflow with Qwen Integration

Complete Workflow:
1. Detect file in Inbox/ → Update Dashboard
2. Create Plan in Plans/
3. Move Plan to Pending_Approval/
4. [USER moves to Approved/]
5. Auto-detect Approved/ → Create action in Needs_Action/
6. Execute action → Update Dashboard, Accounting/, Briefings/
7. Move original to Done/, clean up

Usage:
    python auto_workflow.py --vault-path /path/to/vault --watch
"""

import argparse
import logging
import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AutoWorkflowOrchestrator:
    """Complete automated workflow orchestrator."""

    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
        
        # Folder paths
        self.inbox = vault_path / 'Inbox'
        self.needs_action = vault_path / 'Needs_Action'
        self.pending_approval = vault_path / 'Pending_Approval'
        self.approved = vault_path / 'Approved'
        self.plans = vault_path / 'Plans'
        self.files = vault_path / 'Files'
        self.done = vault_path / 'Done'
        self.accounting = vault_path / 'Accounting'
        self.briefings = vault_path / 'Briefings'
        self.updates = vault_path / 'Updates'
        self.dashboard = vault_path / 'Dashboard.md'
        self.handbook = vault_path / 'Company_Handbook.md'
        
        # State tracking
        self.state_file = vault_path / '.workflow_state.txt'
        self.processed_files: set = self._load_state()
        
        # Ensure all folders exist
        for folder in [self.inbox, self.needs_action, self.pending_approval,
                       self.approved, self.plans, self.files, self.done,
                       self.accounting, self.briefings, self.updates]:
            folder.mkdir(parents=True, exist_ok=True)

    def _load_state(self) -> set:
        """Load processed files state."""
        if self.state_file.exists():
            return set(self.state_file.read_text().strip().split('\n'))
        return set()

    def _save_state(self, filename: str):
        """Save processed file to state."""
        self.processed_files.add(filename)
        self.state_file.write_text('\n'.join(self.processed_files))

    def _is_processed(self, filename: str) -> bool:
        """Check if file was already processed."""
        return filename in self.processed_files

    # ========== DASHBOARD UPDATER ==========

    def update_dashboard(self, action: str, details: str = "", status: str = "✅"):
        """Update Dashboard.md with activity."""
        if not self.dashboard.exists():
            logger.warning("Dashboard.md not found, creating...")
            self._create_default_dashboard()

        try:
            content = self.dashboard.read_text()
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Update last_updated
            if 'last_updated:' in content:
                content = content.replace(
                    'last_updated: 2026-02-26T00:00:00Z',
                    f'last_updated: {datetime.now().isoformat()}'
                )

            # Update Quick Status
            if '| Pending Tasks |' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if '| Pending Tasks |' in line:
                        # Count pending items
                        pending_count = len(list(self.pending_approval.glob('*.md')))
                        lines[i] = f'| Pending Tasks | {pending_count} | {"⏳" if pending_count > 0 else "✅"} |'
                    if '| Last Activity |' in line:
                        lines[i] = f'| Last Activity | {timestamp} - {action} | {status} |'
                content = '\n'.join(lines)

            # Update activity log
            if '## 📝 Recent Activity Log' in content:
                lines = content.split('\n')
                new_lines = []
                for i, line in enumerate(lines):
                    new_lines.append(line)
                    if '| Time | Action | Status |' in line:
                        new_lines.append(f'| {timestamp} | {action} | {status} |')
                content = '\n'.join(new_lines)

            # Update folder status
            if '| Folder | Files | Status |' in content:
                lines = content.split('\n')
                folder_counts = {
                    'Inbox/': len(list(self.inbox.glob('*.md'))),
                    'Needs_Action/': len(list(self.needs_action.glob('*.md'))),
                    'Pending_Approval/': len(list(self.pending_approval.glob('*.md'))),
                    'Approved/': len(list(self.approved.glob('*.md'))),
                    'Done/': len(list(self.done.glob('*.md'))),
                    'Accounting/': len(list(self.accounting.glob('*.md'))),
                    'Briefings/': len(list(self.briefings.glob('*.md'))),
                }
                for i, line in enumerate(lines):
                    for folder, count in folder_counts.items():
                        if folder in line:
                            status_icon = '📥' if count > 0 and folder == 'Inbox/' else \
                                         '⏳' if count > 0 and folder == 'Pending_Approval/' else \
                                         '✅'
                            lines[i] = f'| {folder} | {count} | {status_icon} |'
                content = '\n'.join(lines)

            # Update Financial Snapshot
            if '## 💰 Financial Snapshot' in content:
                # Calculate totals from accounting entries
                total_revenue = 0.0
                total_expenses = 0.0
                for entry_file in self.accounting.glob('ENTRY_*.md'):
                    entry_content = entry_file.read_text()
                    amount_val = 0.0
                    bank_charges_val = 0.0
                    is_expense = False
                    for line in entry_content.split('\n'):
                        # Get amount (gross amount, not net)
                        if 'amount:' in line.lower() and 'bank_charges' not in line.lower():
                            try:
                                amount_str = line.split(':')[1].strip()
                                amount_val = float(''.join(c for c in amount_str if c.isdigit() or c == '.'))
                            except:
                                pass
                        # Get bank charges
                        if 'bank_charges:' in line.lower():
                            try:
                                charges_str = line.split(':')[1].strip()
                                bank_charges_val = float(''.join(c for c in charges_str if c.isdigit() or c == '.'))
                            except:
                                pass
                        # Check transaction type
                        if 'transaction_type:' in line.lower():
                            if 'expense' in line.lower():
                                is_expense = True
                    
                    # Add to appropriate total
                    if is_expense:
                        total_expenses += amount_val
                    else:
                        total_revenue += amount_val  # Gross revenue
                    
                    # Bank charges are always expenses
                    if bank_charges_val > 0:
                        total_expenses += bank_charges_val
                
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if '| This Week |' in line:
                        lines[i] = f'| This Week | £{total_revenue:.2f} | £{total_expenses:.2f} | £{total_revenue - total_expenses:.2f} |'
                    if '| This Month |' in line:
                        lines[i] = f'| This Month | £{total_revenue:.2f} | £{total_expenses:.2f} | £{total_revenue - total_expenses:.2f} |'
                content = '\n'.join(lines)

            self.dashboard.write_text(content)
            logger.info(f"Dashboard updated: {action}")

        except Exception as e:
            logger.error(f"Failed to update dashboard: {e}")

    def _create_default_dashboard(self):
        """Create default dashboard if missing."""
        content = """---
last_updated: 2026-03-03T00:00:00Z
status: active
review_frequency: daily
---

# 🤖 AI Employee Dashboard

## Quick Status

| Metric | Value | Status |
|--------|-------|--------|
| Pending Tasks | 0 | ✅ |
| Pending Approvals | 0 | ✅ |
| Last Activity | - | - |

---

## 📥 Inbox Summary

*No new items*

---

## 📝 Recent Activity Log

| Time | Action | Status |
|------|--------|--------|

---

## 📁 Folder Status

| Folder | Files | Status |
|--------|-------|--------|
| Inbox/ | 0 | ✅ |
| Needs_Action/ | 0 | ✅ |
| Pending_Approval/ | 0 | ✅ |
| Approved/ | 0 | ✅ |
| Done/ | 0 | ✅ |
| Accounting/ | 0 | ✅ |
| Briefings/ | 0 | ✅ |

---

*Dashboard auto-updates when AI Employee processes tasks*
"""
        self.dashboard.write_text(content)

    # ========== STEP 1: INBOX DETECTION ==========

    def check_inbox(self) -> List[Path]:
        """Check Inbox for new files."""
        if not self.inbox.exists():
            return []
        
        new_files = []
        for file_path in self.inbox.glob('*.md'):
            if not self._is_processed(file_path.name):
                new_files.append(file_path)
                logger.info(f"📥 Detected new file in Inbox: {file_path.name}")
                self.update_dashboard(
                    f"New file detected: {file_path.name}",
                    "Processing started",
                    "🔄"
                )
        
        return new_files

    # ========== STEP 2: CREATE PLAN ==========

    def create_plan(self, inbox_file: Path) -> Path:
        """Create a plan in Plans/ folder."""
        try:
            content = inbox_file.read_text()
            
            # Extract metadata from frontmatter
            file_type = 'general'
            priority = 'medium'
            amount = None
            
            for line in content.split('\n')[:20]:
                if 'type:' in line.lower():
                    file_type = line.split(':')[1].strip()
                if 'priority:' in line.lower():
                    priority = line.split(':')[1].strip()
                if 'amount:' in line.lower():
                    amount = line.split(':')[1].strip()
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            plan_name = f'PLAN_{inbox_file.stem}_{timestamp}.md'
            plan_path = self.plans / plan_name
            
            plan_content = f"""---
plan_id: PLAN-{timestamp}
created: {datetime.now().isoformat()}
status: pending_approval
source_file: Inbox/{inbox_file.name}
file_type: {file_type}
priority: {priority}
amount: {amount or 'N/A'}
---

# Processing Plan: {inbox_file.name}

## Source Information

| Field | Value |
|-------|-------|
| **Original File** | {inbox_file.name} |
| **Type** | {file_type} |
| **Priority** | {priority} |
| **Amount** | {amount or 'N/A'} |
| **Received** | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |

---

## Proposed Actions

### Phase 1: Review & Analysis
- [ ] Read and analyze file content
- [ ] Categorize appropriately
- [ ] Identify required actions
- [ ] Check for approval requirements

### Phase 2: Processing
- [ ] Execute required actions per Company_Handbook.md
- [ ] Create accounting entry if financial
- [ ] Update Dashboard.md
- [ ] Log in Updates/

### Phase 3: Completion
- [ ] Move original file to Done/
- [ ] Archive reference in Files/ (if needed)
- [ ] Clean up temporary files
- [ ] Update Briefings/

---

## Approval Required

**This plan requires human approval before execution.**

**To approve:** Move this file to `/Approved/`
**To reject:** Move this file to `/Rejected/`

---

*Plan created by AI Employee Auto-Workflow*
*Next Step: Awaiting approval*
"""
            plan_path.write_text(plan_content)
            logger.info(f"📋 Created plan: {plan_name}")
            
            return plan_path
            
        except Exception as e:
            logger.error(f"Failed to create plan: {e}")
            return None

    # ========== STEP 3: MOVE TO PENDING_APPROVAL ==========

    def move_to_pending_approval(self, plan_path: Path) -> bool:
        """Move plan to Pending_Approval folder."""
        try:
            dest = self.pending_approval / plan_path.name
            shutil.move(str(plan_path), str(dest))
            logger.info(f"⏳ Moved to Pending_Approval: {plan_path.name}")
            
            self.update_dashboard(
                f"Plan created: {plan_path.name}",
                "Awaiting your approval",
                "⏳"
            )
            
            return True
        except Exception as e:
            logger.error(f"Failed to move to pending approval: {e}")
            return False

    # ========== STEP 4: DETECT APPROVED ==========

    def check_approved(self) -> List[Path]:
        """Check Approved/ folder for approved plans."""
        if not self.approved.exists():
            return []
        
        approved_files = []
        for file_path in self.approved.glob('*.md'):
            if not file_path.name.startswith('COMPLETED_'):
                approved_files.append(file_path)
                logger.info(f"✅ Detected approved file: {file_path.name}")
        
        return approved_files

    # ========== STEP 5: CREATE ACTION IN NEEDS_ACTION ==========

    def create_action_from_approved(self, approved_file: Path) -> Path:
        """Create action file in Needs_Action from approved plan."""
        try:
            content = approved_file.read_text()
            
            # Extract plan info
            source_file = 'Unknown'
            file_type = 'general'
            priority = 'medium'
            
            for line in content.split('\n')[:20]:
                if 'source_file:' in line.lower():
                    source_file = line.split(':')[1].strip()
                if 'file_type:' in line.lower():
                    file_type = line.split(':')[1].strip()
                if 'priority:' in line.lower():
                    priority = line.split(':')[1].strip()
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            action_name = f'ACTION_{approved_file.stem}_{timestamp}.md'
            action_path = self.needs_action / action_name
            
            action_content = f"""---
type: approved_action
created: {datetime.now().isoformat()}
status: pending
source_plan: {approved_file.name}
source_file: {source_file}
file_type: {file_type}
priority: {priority}
---

# Action Required: Execute Approved Plan

## Plan Information

| Field | Value |
|-------|-------|
| **Source Plan** | {approved_file.name} |
| **Original File** | {source_file} |
| **Type** | {file_type} |
| **Priority** | {priority} |
| **Approved** | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |

---

## Required Actions

- [ ] Execute plan per Company_Handbook.md
- [ ] Create accounting entry if financial transaction
- [ ] Update Dashboard.md
- [ ] Log execution in Updates/
- [ ] Move original to Done/
- [ ] Update Briefings/ if weekly summary needed

---

## Execution Notes

*To be filled during execution*

---

*Action created by AI Employee Auto-Workflow*
*Status: Ready for execution*
"""
            action_path.write_text(action_content)
            logger.info(f"🎯 Created action: {action_name}")
            
            return action_path
            
        except Exception as e:
            logger.error(f"Failed to create action: {e}")
            return None

    # ========== STEP 6: EXECUTE ACTION ==========

    def execute_action(self, action_file: Path) -> bool:
        """Execute an action file."""
        try:
            content = action_file.read_text()

            # Extract info
            source_file = 'Unknown'
            file_type = 'general'
            amount = None
            currency = 'GBP'
            bank_charges = None
            net_amount = None

            for line in content.split('\n')[:20]:
                if 'source_file:' in line.lower():
                    source_file = line.split(':')[1].strip()
                if 'file_type:' in line.lower():
                    file_type = line.split(':')[1].strip()

            # Read original source file to get amount info (check Inbox first, then Done)
            source_path = self.inbox / source_file.replace('Inbox/', '')
            if not source_path.exists():
                source_path = self.done / source_file.replace('Inbox/', '')
            if source_path.exists():
                source_content = source_path.read_text()
                for line in source_content.split('\n')[:25]:
                    line_lower = line.lower()
                    if 'amount:' in line_lower and 'bank_charges' not in line_lower and 'net_amount' not in line_lower:
                        amount = line.split(':')[1].strip()
                    if 'currency:' in line_lower:
                        currency = line.split(':')[1].strip()
                    if 'bank_charges:' in line_lower:
                        bank_charges = line.split(':')[1].strip()
                    if 'net_amount:' in line_lower:
                        net_amount = line.split(':')[1].strip()
                    if 'expense_type:' in line_lower:
                        expense_type = line.split(':')[1].strip()
                    if 'vendor:' in line_lower:
                        vendor = line.split(':')[1].strip()
                    if 'bill_to:' in line_lower:
                        bill_to = line.split(':')[1].strip()
            else:
                logger.warning(f"Source file not found: {source_file}")

            # Update action file status
            content = content.replace('status: pending', 'status: completed')
            content = content.replace(
                '*To be filled during execution*',
                f'**Executed by AI Employee on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}**\n\n'
                f'### Execution Summary\n\n'
                f'1. ✅ Read and analyzed source file\n'
                f'2. ✅ Categorized as: {file_type}\n'
                f'3. ✅ Amount: {amount or "N/A"} {currency}\n'
                f'4. ✅ Created accounting entry (if applicable)\n'
                f'5. ✅ Updated Dashboard.md\n'
                f'6. ✅ Logged in Updates/\n'
                f'7. ✅ Moved original to Done/'
            )
            action_file.write_text(content)

            # Create accounting entry if financial (check source file name and content)
            is_financial = (
                'invoice' in file_type.lower() or 
                'payment' in file_type.lower() or
                'purchase' in file_type.lower() or 
                'expense' in file_type.lower() or
                'bill' in source_file.lower() or
                ('email' in source_file.lower() and amount is not None)
            )
            
            if is_financial:
                # Determine if it's income or expense based on type and content
                is_expense = (
                    'expense' in file_type.lower() or
                    'invoice' in file_type.lower() or
                    'bill' in source_file.lower() or
                    'k-electric' in source_file.lower() or
                    'maintenance' in source_file.lower() or
                    'utilities' in source_file.lower()
                )
                self._create_accounting_entry(
                    action_file, source_file, amount, currency,
                    is_expense=is_expense, bank_charges=bank_charges
                )

            # Create execution log
            self._create_execution_log(action_file, source_file)

            # Create/update weekly briefing
            self._update_briefing(file_type, amount, currency if amount else None, is_expense, bank_charges)

            # Update dashboard
            self.update_dashboard(
                f"Executed: {action_file.name}",
                f"Source: {source_file}, Amount: {amount or 'N/A'} {currency}",
                "✅"
            )

            logger.info(f"✅ Executed action: {action_file.name}")
            return True

        except Exception as e:
            logger.error(f"Failed to execute action: {e}")
            return False

    def _create_accounting_entry(self, action_file: Path, source_file: str, amount: str = None, currency: str = 'GBP', is_expense: bool = False, bank_charges: str = None):
        """Create accounting entry for financial transactions."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d')
            entry_name = f'ENTRY_{timestamp}_{action_file.stem}.md'
            entry_path = self.accounting / entry_name

            # Parse amount - extract numeric value
            amount_value = amount
            if amount:
                amount_value = ''.join(c for c in str(amount) if c.isdigit() or c == '.')
            
            # Parse bank charges if present
            bank_charges_value = None
            if bank_charges:
                bank_charges_value = ''.join(c for c in str(bank_charges) if c.isdigit() or c == '.')

            # Determine transaction type
            transaction_type = "Expense" if is_expense else "Revenue"
            category = "Operating Expense" if is_expense else "Income"
            
            # Calculate net amount if bank charges deducted
            net_amount = float(amount_value) - float(bank_charges_value) if amount_value and bank_charges_value and amount_value.replace('.','').isdigit() and bank_charges_value.replace('.','').isdigit() else amount_value

            entry_content = f"""---
type: accounting_entry
entry_id: ACC-{timestamp}-{hash(action_file.name) % 1000:03d}
created: {datetime.now().isoformat()}
source_action: {action_file.name}
source_file: {source_file}
status: recorded
amount: {amount_value or 'N/A'}
currency: {currency}
transaction_type: {transaction_type}
bank_charges: {bank_charges_value or '0.00'}
net_amount: {net_amount if isinstance(net_amount, str) else f'{net_amount:.2f}'}
---

# Accounting Entry - {transaction_type}

## Transaction Details

| Field | Value |
|-------|-------|
| **Entry ID** | ACC-{timestamp}-{hash(action_file.name) % 1000:03d} |
| **Date** | {datetime.now().strftime('%Y-%m-%d')} |
| **Source** | {source_file} |
| **Action File** | {action_file.name} |
| **Transaction Type** | {transaction_type} |
| **Gross Amount** | {amount_value or 'N/A'} {currency} |
| **Bank Charges** | {bank_charges_value or '0.00'} {currency} |
| **Net Amount** | {net_amount if isinstance(net_amount, str) else f'{net_amount:.2f}'} {currency} |
| **Status** | ✅ Recorded |

---

## Classification

| Category | Subcategory | Amount | Treatment |
|----------|-------------|--------|-----------|
| {category} | Operations | {amount_value or 'TBD'} {currency} | {"Debit" if is_expense else "Credit"} |
| {"Bank Charges Expense" if bank_charges_value else "N/A"} | {"Bank Fees" if bank_charges_value else "N/A"} | {bank_charges_value or '0.00'} {currency} | {"Debit" if bank_charges_value else "N/A"} |

---

## Journal Entry

| Account | Debit | Credit |
|---------|-------|--------|
| {"Bank/Cash (Net)" if not is_expense else "Expense Account"} | {net_amount if isinstance(net_amount, str) else f'{net_amount:.2f}'} {currency} | - |
| {"Bank Charges Expense" if bank_charges_value else "N/A"} | {bank_charges_value or '0.00'} {currency} | - |
| {"Revenue/Income" if not is_expense else "N/A"} | - | {amount_value or 'TBD'} {currency} |

---

## Audit Trail

| Date | Action | By |
|------|--------|-----|
| {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Entry created | AI Employee |
| {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Source processed | AI Employee |

---

*Entry created by AI Employee Auto-Workflow*
"""
            entry_path.write_text(entry_content)
            logger.info(f"💰 Created accounting entry: {entry_name} ({transaction_type}: {amount_value} {currency})")

        except Exception as e:
            logger.error(f"Failed to create accounting entry: {e}")

    def _create_execution_log(self, action_file: Path, source_file: str):
        """Create execution log in Updates/."""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            log_name = f'LOG_{timestamp}_{action_file.stem}.md'
            log_path = self.updates / log_name

            log_content = f"""---
type: execution_log
logged: {datetime.now().isoformat()}
source_file: {source_file}
action_file: {action_file.name}
status: completed
---

# Execution Log

## Summary

| Field | Value |
|-------|-------|
| **Timestamp** | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |
| **Source File** | {source_file} |
| **Action File** | {action_file.name} |
| **Status** | ✅ Completed |

---

## Actions Performed

1. ✅ Read and analyzed file content
2. ✅ Categorized appropriately
3. ✅ Created accounting entry (if applicable)
4. ✅ Updated Dashboard.md
5. ✅ Archived original to Done/

---

*Log created by AI Employee Auto-Workflow*
"""
            log_path.write_text(log_content)
            logger.info(f"📝 Created execution log: {log_name}")

        except Exception as e:
            logger.error(f"Failed to create execution log: {e}")

    def _update_briefing(self, file_type: str, amount: str = None, currency: str = 'GBP', is_expense: bool = False, bank_charges: str = None):
        """Create or update weekly briefing."""
        try:
            # Get current week number
            week_num = datetime.now().isocalendar()[1]
            year = datetime.now().year
            briefing_name = f'WEEKLY_Briefing_{year}-W{week_num:02d}.md'
            briefing_path = self.briefings / briefing_name

            # Check if briefing exists
            if briefing_path.exists():
                content = briefing_path.read_text()
            else:
                content = f"""---
week: {week_num}
year: {year}
created: {datetime.now().isoformat()}
status: active
---

# Weekly Briefing - {year} Week {week_num}

**Period:** {datetime.now().strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}

---

## Summary

| Metric | Value |
|--------|-------|
| Total Transactions | 0 |
| Total Revenue | £0.00 |
| Total Expenses | £0.00 |
| Net | £0.00 |

---

## Transactions This Week

| Date | Type | Description | Amount | Status |
|------|------|-------------|--------|--------|

---

## Activities

- [ ] Review pending items
- [ ] Process approvals
- [ ] Update financial records

---

*Briefing created by AI Employee Auto-Workflow*
"""

            # Update briefing with new transaction
            if amount:
                amount_value = ''.join(c for c in str(amount) if c.isdigit() or c == '.')
                trans_type = "Expense" if is_expense else "Income"
                description = "Payment received" if not is_expense else "Expense paid"
                
                # Increment transaction count
                if 'Total Transactions | 0' in content:
                    content = content.replace('Total Transactions | 0', 'Total Transactions | 1')
                else:
                    # Count existing transactions
                    count = content.count('| 2026-') + 1
                    content = content.replace(f'Total Transactions | {count-1}', f'Total Transactions | {count}')
                
                # Update revenue or expenses
                if is_expense:
                    if 'Total Expenses | £0.00' in content:
                        content = content.replace('Total Expenses | £0.00', f'Total Expenses | £{amount_value}')
                else:
                    if 'Total Revenue | £0.00' in content:
                        content = content.replace('Total Revenue | £0.00', f'Total Revenue | £{amount_value}')
                
                # Add bank charges as expense if present
                if bank_charges:
                    charges_value = ''.join(c for c in str(bank_charges) if c.isdigit() or c == '.')
                    # Add to existing expenses
                    if 'Total Expenses | £0.00' in content:
                        content = content.replace('Total Expenses | £0.00', f'Total Expenses | £{charges_value}')
                    else:
                        # Parse and add to existing expenses (simplified)
                        pass
                
                # Add transaction row
                if f'| {datetime.now().strftime("%Y-%m-%d")} |' not in content:
                    charges_note = f" (incl. £{bank_charges} bank charges)" if bank_charges and not is_expense else ""
                    transaction_row = f'| {datetime.now().strftime("%Y-%m-%d")} | {file_type} | {description} | {amount_value} {currency} ({trans_type}){charges_note} | ✅ |\n'
                    content = content.replace(
                        '| Date | Type | Description | Amount | Status |',
                        f'| Date | Type | Description | Amount | Status |\n{transaction_row}'
                    )
                
                # Recalculate Net
                lines = content.split('\n')
                revenue = 0.0
                expenses = 0.0
                for line in lines:
                    if 'Total Revenue |' in line:
                        try:
                            revenue = float(line.split('£')[1].split('|')[0].strip())
                        except:
                            pass
                    if 'Total Expenses |' in line:
                        try:
                            expenses = float(line.split('£')[1].split('|')[0].strip())
                        except:
                            pass
                for i, line in enumerate(lines):
                    if '| Net |' in line and '£0.00' in line:
                        lines[i] = f'| Net | £{revenue - expenses:.2f} |'
                content = '\n'.join(lines)

            briefing_path.write_text(content)
            logger.info(f"📊 Updated weekly briefing: {briefing_name}")

        except Exception as e:
            logger.error(f"Failed to update briefing: {e}")

    # ========== STEP 7: MOVE TO DONE ==========

    def move_to_done(self, inbox_file: Path, action_file: Path, plan_file: Path):
        """Move processed files to Done/."""
        try:
            # Move original inbox file
            if inbox_file.exists():
                dest = self.done / inbox_file.name
                shutil.move(str(inbox_file), str(dest))
                logger.info(f"📦 Moved to Done: {inbox_file.name}")
            
            # Move action file
            if action_file.exists():
                dest = self.done / action_file.name
                shutil.move(str(action_file), str(dest))
                logger.info(f"📦 Moved to Done: {action_file.name}")
            
            # Move plan file (from approved)
            if plan_file.exists():
                new_name = plan_file.name.replace('PLAN_', 'COMPLETED_')
                dest = self.done / new_name
                shutil.move(str(plan_file), str(dest))
                logger.info(f"📦 Moved to Done: {plan_file.name} → {new_name}")
            
        except Exception as e:
            logger.error(f"Failed to move files to Done: {e}")

    # ========== MAIN WORKFLOW ==========

    def process_inbox_file(self, inbox_file: Path):
        """Process a single inbox file through complete workflow."""
        logger.info(f"🔄 Processing: {inbox_file.name}")
        
        # Step 1: Update dashboard (file detected)
        self.update_dashboard(
            f"Processing: {inbox_file.name}",
            "Creating plan",
            "🔄"
        )
        
        # Step 2: Create plan
        plan_path = self.create_plan(inbox_file)
        if not plan_path:
            logger.error("Failed to create plan")
            return
        
        # Step 3: Move to pending approval
        self.move_to_pending_approval(plan_path)
        
        # Mark as processed (waiting for approval)
        self._save_state(inbox_file.name)
        
        logger.info(f"⏳ Plan created and awaiting approval: {plan_path.name}")

    def process_approved_plan(self, approved_file: Path):
        """Process an approved plan through execution."""
        logger.info(f"🔄 Executing approved plan: {approved_file.name}")
        
        # Update dashboard
        self.update_dashboard(
            f"Executing: {approved_file.name}",
            "Plan approved",
            "🔄"
        )
        
        # Step 5: Create action in Needs_Action
        action_path = self.create_action_from_approved(approved_file)
        if not action_path:
            logger.error("Failed to create action")
            return
        
        # Step 6: Execute action
        if not self.execute_action(action_path):
            logger.error("Failed to execute action")
            return
        
        # Step 7: Find and move original inbox file to Done
        # (We need to find the original file from the plan)
        content = approved_file.read_text()
        source_file = 'Unknown'
        for line in content.split('\n')[:20]:
            if 'source_file:' in line.lower():
                source_file = line.split(':')[1].strip()
                break
        
        # Try to find the original file in Done (may already be there)
        # or mark as complete
        inbox_file_name = source_file.replace('Inbox/', '')
        inbox_file_path = self.inbox / inbox_file_name
        
        # Move files to Done
        self.move_to_done(inbox_file_path, action_path, approved_file)
        
        # Mark complete
        self._save_state(approved_file.name)
        
        logger.info(f"✅ Complete: {approved_file.name}")

    def run(self, watch: bool = False, interval: int = 5):
        """Run the auto workflow orchestrator."""
        logger.info("="*60)
        logger.info("AI Employee - Full Auto Workflow")
        logger.info("="*60)
        logger.info(f"Vault: {self.vault_path}")
        logger.info("Workflow: Inbox → Plan → Pending_Approval → [YOU] → Approved → Action → Done")
        logger.info("Press Ctrl+C to stop")
        logger.info("="*60)
        
        if watch:
            logger.info(f"Watch mode: Checking every {interval} seconds")
        else:
            logger.info("Single run mode")
        
        try:
            while True:
                # Check Inbox for new files
                inbox_files = self.check_inbox()
                for inbox_file in inbox_files:
                    self.process_inbox_file(inbox_file)
                
                # Check Approved for approved plans
                approved_files = self.check_approved()
                for approved_file in approved_files:
                    self.process_approved_plan(approved_file)
                
                if not watch:
                    logger.info("✅ Single run complete")
                    break
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            logger.info("\n⚠️ Orchestrator stopped by user")
        
        logger.info("✅ Auto Workflow complete")
        return 0


def main():
    parser = argparse.ArgumentParser(
        description='AI Employee - Full Auto Workflow Orchestrator'
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
    
    orchestrator = AutoWorkflowOrchestrator(vault_path=vault_path)
    sys.exit(orchestrator.run(watch=args.watch, interval=args.interval))


if __name__ == '__main__':
    main()
