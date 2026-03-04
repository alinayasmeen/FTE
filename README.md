# FTE - Full Time AI Employee

> **Personal AI Employee** — An autonomous AI agent built with Qwen Code + Obsidian for 24/7 task processing.

## 🎯 Project Status

**✅ Bronze Tier Complete** — See [BRONZE_TIER_COMPLETE.md](./BRONZE_TIER_COMPLETE.md)

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   PERCEPTION    │────▶│    REASONING    │────▶│     ACTION      │
│                 │     │                 │     │                 │
│ File Watcher    │     │   Qwen Code     │     │ File Operations │
│                 │     │                 │     │ Dashboard Update│
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    OBSIDIAN VAULT (Memory)                      │
│  /Inbox → /Needs_Action → /Done                                 │
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
│   ├── Dashboard.md                   # Main dashboard
│   ├── Company_Handbook.md            # Rules & SOPs
│   ├── QUICKSTART.md                  # Quick start guide
│   ├── Inbox/                         # Drop folder for new files
│   ├── Needs_Action/                  # Files awaiting processing
│   ├── Done/                          # Completed tasks
│   ├── Pending_Approval/              # Awaiting human approval
│   ├── Approved/                      # Approved actions
│   ├── Skills/
│   │   └── file-processor.md          # Agent skill definition
│   └── ...
│
└── scripts/
    ├── filesystem_watcher.py          # Monitors Inbox for new files
    └── ralph_orchestrator.py          # Autonomous processing loop
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
# Start the combined orchestrator with Qwen integration
./scripts/start-automation.sh

# Or run directly:
python scripts/orchestrator.py \
  --vault-path /home/alina/Hackathon_4/FTE/AI_Employee_Vault \
  --watch \
  --interval 5
```

### 3. Test the Workflow

**Simple Mode (Auto-processing):**
1. Drop a file into `AI_Employee_Vault/Inbox/`
2. Orchestrator auto-creates action file in `Needs_Action/`
3. Orchestrator auto-processes and moves to `Done/`
4. Dashboard updates automatically

**Approval Workflow (HITL):**
1. Create approval file in `Pending_Approval/`
2. **You move it to** `Approved/`
3. Orchestrator auto-executes the approval
4. Creates accounting entry, logs to `Updates/`
5. Moves to `Done/`

### 4. Legacy Scripts (Still Available)

```bash
# File watcher only
python scripts/filesystem_watcher.py \
  --vault-path /home/alina/Hackathon_4/FTE/AI_Employee_Vault \
  --drop-folder /home/alina/Hackathon_4/FTE/AI_Employee_Vault/Inbox

# Ralph loop only
python scripts/ralph_orchestrator.py \
  --vault-path /home/alina/Hackathon_4/FTE/AI_Employee_Vault \
  --max-iterations 10

# Qwen integration only
python scripts/qwen_integration.py \
  --vault-path /home/alina/Hackathon_4/FTE/AI_Employee_Vault \
  --watch
```

---

## 🔄 Workflow

### **Automated Workflow (With Qwen Integration)**

```
1. Drop file in /Inbox
         │
         ▼
2. Orchestrator detects → creates action file in /Needs_Action
         │
         ▼
3. Orchestrator auto-processes → updates Dashboard
         │
         ▼
4. File moved to /Done
         │
         ▼
✅ COMPLETE (No manual intervention needed)
```

### **Approval Workflow (HITL)**

```
1. Create approval request in /Pending_Approval
         │
         ▼
2. 🙋 YOU review and move to /Approved
         │
         ▼
3. Orchestrator detects → auto-executes
         │
         ├──→ Creates accounting entry in /Accounting
         ├──→ Logs execution in /Updates
         └──→ Updates Dashboard
         │
         ▼
4. File moved to /Done (renamed COMPLETED_*)
         │
         ▼
✅ COMPLETE
```

### File Frontmatter Format

```yaml
---
type: file_drop|email|approval_request
from: Source
subject: Description
received: 2026-03-01T00:00:00Z
priority: high|medium|low
status: pending|completed
---
```

---

## 📋 Bronze Tier Features

| Component | Status | Description |
|-----------|--------|-------------|
| **Obsidian Vault** | ✅ | Dashboard, Company Handbook, folder structure |
| **File System Watcher** | ✅ | Monitors Inbox, creates action files |
| **Qwen Integration** | ✅ | Auto-processes Approved/ folder |
| **Combined Orchestrator** | ✅ | Full automation (Inbox → Done) |
| **Agent Skills** | ✅ | `file-processor.md` skill definition |
| **Ralph Loop** | ✅ | Autonomous processing orchestrator |
| **Accounting Integration** | ✅ | Auto-creates expense entries |
| **Weekly Briefings** | ✅ | Auto-generated reports |

---

## 🛠️ Scripts

### orchestrator.py (Recommended - Combined)

**Full automation with Qwen integration.** Monitors all folders and auto-processes.

**Features:**
- Inbox → Needs_Action (auto-create action files)
- Needs_Action → Done (auto-process tasks)
- Approved → Done (auto-execute approvals with accounting)
- Dashboard auto-updates
- Single script for full workflow

**Usage:**
```bash
# Watch mode (continuous)
python scripts/orchestrator.py --vault-path /path/to/vault --watch

# Single run
python scripts/orchestrator.py --vault-path /path/to/vault
```

### start-automation.sh (Easiest)

**One-command startup** for full automation.

```bash
./scripts/start-automation.sh
```

### qwen_integration.py (Approval Processor)

**Qwen integration for Approved/ folder.** Auto-executes approvals.

**Features:**
- Monitors Approved/ folder
- Auto-executes approved requests
- Creates accounting entries
- Logs to Updates/
- Moves to Done/

**Usage:**
```bash
python scripts/qwen_integration.py --vault-path /path/to/vault --watch
```

### filesystem_watcher.py (Legacy)

Monitors the Inbox folder for new files and creates actionable `.md` files in `Needs_Action`.

**Features:**
- Detects priority keywords (urgent, important, normal)
- Identifies file types (document, invoice, image)
- Tracks processed files to avoid duplicates
- Configurable check interval

### ralph_orchestrator.py (Legacy)

Manages autonomous processing iterations using the Ralph Wiggum Loop pattern.

**Features:**
- Creates state files for Qwen to process
- Checks completion criteria
- Updates Dashboard with activity
- Configurable max iterations

---

## 📚 Documentation

- **[Bronze Tier Report](./BRONZE_TIER_COMPLETE.md)** - Detailed completion checklist
- **[Quick Start](./AI_Employee_Vault/QUICKSTART.md)** - Step-by-step guide
- **[Company Handbook](./AI_Employee_Vault/Company_Handbook.md)** - Rules & SOPs
- **[Dashboard](./AI_Employee_Vault/Dashboard.md)** - Live status

---

## 🎯 Next Steps (Silver Tier)

- [ ] Gmail Watcher for email processing
- [ ] WhatsApp Watcher for message monitoring
- [ ] MCP server for sending emails
- [ ] Human-in-the-loop approval workflow
- [ ] Scheduled tasks via cron

---

## 📄 License

MIT License - Copyright (c) 2026 Hafiza Alina Yasmeen

---

*Built with Qwen Code + Obsidian + Python*
