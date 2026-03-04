# FTE - Full Time AI Employee

> **Personal AI Employee** — An autonomous AI agent built with Qwen Code + Obsidian for 24/7 task processing with full financial tracking.

## 🎯 Project Status

**✅ Bronze Tier Complete** — See [BRONZE_TIER_COMPLETE.md](./BRONZE_TIER_COMPLETE.md)

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   PERCEPTION    │────▶│    REASONING    │────▶│     ACTION      │
│                 │     │                 │     │                 │
│ Auto Workflow   │     │   Qwen Code     │     │ File Operations │
│ (auto_workflow) │     │   (Optional)    │     │ Dashboard Update│
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OBSIDIAN VAULT (Memory)                      │
│  /Inbox → Plan → Pending_Approval → [YOU] → Approved → Done     │
│                          │                                      │
│                          ▼                                      │
│                   /Accounting (Revenue/Expenses)                │
│                   /Briefings (Weekly Reports)                   │
│                   /Updates (Execution Logs)                     │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
FTE/
├── README.md                          # This file
├── BRONZE_TIER_COMPLETE.md            # Bronze tier completion report
├── requirements.txt                   # Python dependencies
├── qwen-config.json                   # Qwen settings
│
├── AI_Employee_Vault/                 # Obsidian Vault
│   ├── Dashboard.md                   # Main dashboard with financial snapshot
│   ├── Company_Handbook.md            # Rules & SOPs
│   ├── QUICKSTART.md                  # Quick start guide
│   ├── Inbox/                         # Drop folder for new files
│   ├── Plans/                         # Auto-generated processing plans
│   ├── Pending_Approval/              # Awaiting your approval
│   ├── Approved/                      # Approved (auto-executes)
│   ├── Needs_Action/                  # Actions to execute
│   ├── Done/                          # Completed tasks
│   ├── Accounting/                    # Financial entries (Revenue/Expenses)
│   ├── Briefings/                     # Weekly reports
│   ├── Updates/                       # Execution logs
│   ├── Files/                         # Reference files
│   └── Skills/
│       └── file-processor.md          # Agent skill definition
│
└── scripts/
    ├── auto_workflow.py               # 🆕 Complete automation with financial tracking
    ├── filesystem_watcher.py          # Legacy: Monitors Inbox
    ├── ralph_orchestrator.py          # Legacy: Autonomous loop
    └── orchestrator.py                # Legacy: Combined script
```

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd /home/alina/Hackathon_4/FTE
pip install -r requirements.txt
```

### 2. Start Full Automation (Recommended)

```bash
# Start the auto workflow in watch mode
cd /home/alina/Hackathon_4/FTE
source .venv/bin/activate  # If using virtual environment

python scripts/auto_workflow.py --watch
```

### 3. Test the Complete Workflow

**Step 1: Drop a file in Inbox/**
```bash
cat > AI_Employee_Vault/Inbox/TEST_Payment_2026-03-04.md << 'EOF'
---
type: payment
from: customer@example.com
subject: Payment Received - £100.00
received: 2026-03-04T14:30:00Z
priority: high
amount: 100.00
currency: GBP
bank_charges: 2.50
net_amount: 97.50
---

# Payment Received

**Gross Amount:** £100.00 GBP
**Bank Charges:** £2.50 GBP
**Net Received:** £97.50 GBP
EOF
```

**Step 2: Watch Obsidian Dashboard Update**
- Plan automatically created in `Pending_Approval/`
- Dashboard shows "1 Pending Approval"

**Step 3: Approve (YOUR ONLY MANUAL STEP)**
```bash
# In Obsidian: Right-click file → Move to Approved/
# Or in terminal:
mv AI_Employee_Vault/Pending_Approval/*.md AI_Employee_Vault/Approved/
```

**Step 4: Watch Auto-Execution Complete!**
- ✅ Accounting entry created (Revenue: £100, Expenses: £2.50)
- ✅ Weekly Briefing updated
- ✅ Dashboard Financial Snapshot updated
- ✅ Execution log created
- ✅ Original file moved to Done/

---

## 🔄 Complete Auto Workflow

```
1. 📥 Drop file in Inbox/
         │
         ▼
2. 🔄 Auto-Detect → Dashboard Updated
         │
         ▼
3. 📋 Create Plan → Plans/
         │
         ▼
4. ⏳ Move to Pending_Approval/
         │
         ▼
5. 🙋 YOU: Move to Approved/ (ONLY MANUAL STEP)
         │
         ▼
6. ✅ Auto-Execute:
   ├── 🎯 Create Action → Needs_Action/
   ├── 💰 Accounting Entry → Accounting/
   │   ├── Revenue tracking (gross amount)
   │   ├── Expense tracking (bank charges, bills)
   │   └── Journal entries (Debit/Credit)
   ├── 📝 Execution Log → Updates/
   ├── 📊 Dashboard Update
   │   ├── Financial Snapshot (Revenue/Expenses/Net)
   │   └── Activity Log
   ├── 📰 Weekly Briefing → Briefings/
   │   ├── Transaction count
   │   ├── Revenue total
   │   ├── Expenses total
   │   └── Net calculation
   └── 📦 Move to Done/
         │
         ▼
7. ✅ COMPLETE - All folders clean!
```

**You only do ONE thing:** Move file from `Pending_Approval/` to `Approved/`

---

## 💰 Financial Tracking Features

### Supported Transaction Types

| Type | Description | Example |
|------|-------------|---------|
| **Revenue/Income** | Payments received from customers | ASDA payment, client invoices |
| **Expenses** | Bills and operating costs | K-Electric, maintenance, utilities |
| **Bank Charges** | Fees deducted from payments | Intermediary bank fees |

### Accounting Entry Format

```yaml
---
type: accounting_entry
entry_id: ACC-20260304-001
amount: 650.00
currency: GBP
transaction_type: Revenue  # or Expense
bank_charges: 5.00
net_amount: 645.00
---
```

### Journal Entry Example (Payment with Bank Charges)

| Account | Debit | Credit |
|---------|-------|--------|
| Bank/Cash (Net) | £645.00 | - |
| Bank Charges Expense | £5.00 | - |
| Revenue/Income | - | £650.00 |

### Dashboard Financial Snapshot

```markdown
## 💰 Financial Snapshot

| Period | Revenue | Expenses | Net |
|--------|---------|----------|-----|
| This Week | £650.00 | £5.00 | £645.00 |
| This Month | £650.00 | £5.00 | £645.00 |
```

---

## 📋 File Frontmatter Format

### Payment/Income Email
```yaml
---
type: payment
from: payments@asda.co.uk
subject: Payment Received - £650.00 GBP
received: 2026-03-04T14:30:00Z
priority: high
amount: 650.00
currency: GBP
bank_charges: 5.00
net_amount: 645.00
---
```

### Expense/Bill Email
```yaml
---
type: expense
from: billing@k-electric.com
subject: Electricity Bill - March 2026
received: 2026-03-04T10:00:00Z
priority: medium
amount: 150.00
currency: GBP
vendor: K-Electric
due_date: 2026-03-15
---
```

### Invoice
```yaml
---
type: invoice
from: supplier@example.com
invoice_number: INV-2026-001
received: 2026-03-04T09:00:00Z
priority: medium
amount: 250.00
currency: GBP
due_date: 2026-03-20
---
```

---

## 🛠️ Scripts

### auto_workflow.py (🆕 Recommended)

**Complete automation with full financial tracking.**

**Features:**
- ✅ Inbox monitoring and plan creation
- ✅ Approval workflow (Pending_Approval → Approved)
- ✅ Auto-execution after approval
- ✅ Accounting entries (Revenue & Expenses)
- ✅ Bank charges tracking
- ✅ Weekly briefings with financial summary
- ✅ Dashboard updates (Financial Snapshot)
- ✅ Execution logging

**Usage:**
```bash
# Watch mode (continuous monitoring)
python scripts/auto_workflow.py --watch

# Single run
python scripts/auto_workflow.py
```

### Legacy Scripts (Still Available)

| Script | Purpose | Status |
|--------|---------|--------|
| `orchestrator.py` | Combined workflow | 🟡 Legacy |
| `qwen_integration.py` | Approval processor | 🟡 Legacy |
| `filesystem_watcher.py` | Inbox monitor | 🟡 Legacy |
| `ralph_orchestrator.py` | Autonomous loop | 🟡 Legacy |

---

## 📊 Folder Usage

| Folder | Purpose | Auto-Cleaned |
|--------|---------|--------------|
| `Inbox/` | Drop new files here | ✅ Yes |
| `Plans/` | Temporary (plan creation) | ✅ Yes |
| `Pending_Approval/` | Awaiting your approval | ⏳ Until approved |
| `Approved/` | Approved plans | ✅ Yes |
| `Needs_Action/` | Actions to execute | ✅ Yes |
| `Done/` | Completed items | 📦 Archive |
| `Accounting/` | Financial entries | 📊 Keep |
| `Updates/` | Execution logs | 📊 Keep |
| `Briefings/` | Weekly reports | 📊 Keep |
| `Files/` | Reference copies | 📊 Keep |

---

## 📚 Documentation

- **[Bronze Tier Report](./BRONZE_TIER_COMPLETE.md)** - Detailed completion checklist
- **[Quick Start](./AI_Employee_Vault/QUICKSTART.md)** - Step-by-step guide (WSL setup)
- **[Company Handbook](./AI_Employee_Vault/Company_Handbook.md)** - Rules & SOPs
- **[Dashboard](./AI_Employee_Vault/Dashboard.md)** - Live status with financial snapshot
- **[Auto Workflow Guide](./scripts/AUTO_WORKFLOW_GUIDE.md)** - Detailed workflow docs

---

## 🎯 Next Steps (Silver Tier)

- [ ] Gmail Watcher for automatic email processing
- [ ] WhatsApp Watcher for message monitoring
- [ ] MCP server for sending emails automatically
- [ ] Scheduled tasks via cron
- [ ] Multi-currency support
- [ ] Financial reports (P&L, Balance Sheet)

---

## 🏆 Bronze Tier Achievements

| Feature | Status | Description |
|---------|--------|-------------|
| **Obsidian Vault** | ✅ | Dashboard, Handbook, folder structure |
| **Auto Workflow** | ✅ | Complete automation (Inbox → Done) |
| **Approval Workflow** | ✅ | Human-in-the-loop (Pending_Approval → Approved) |
| **Financial Tracking** | ✅ | Revenue, Expenses, Bank Charges |
| **Accounting Entries** | ✅ | Auto-created with journal entries |
| **Weekly Briefings** | ✅ | Auto-generated with transaction summary |
| **Dashboard Updates** | ✅ | Real-time Financial Snapshot |
| **Execution Logging** | ✅ | All actions logged in Updates/ |

---

## 📄 License

MIT License - Copyright (c) 2026 Hafiza Alina Yasmeen

---

*Built with Qwen Code + Obsidian + Python*
*Full Financial Tracking: Revenue, Expenses, Bank Charges*
