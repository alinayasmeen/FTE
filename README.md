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

### 2. Start the File Watcher

```bash
python scripts/filesystem_watcher.py \
  --vault-path /home/alina/Hackathon_4/FTE/AI_Employee_Vault \
  --drop-folder /home/alina/Hackathon_4/FTE/AI_Employee_Vault/Inbox
```

### 3. Test the Workflow

1. Drop a file into `AI_Employee_Vault/Inbox/`
2. Watcher creates action file in `Needs_Action/`
3. Ask Qwen: *"Process all files in Needs_Action folder"*
4. Qwen processes, updates Dashboard, moves to Done

### 4. Run Autonomous Mode (Optional)

```bash
python scripts/ralph_orchestrator.py \
  --vault-path /home/alina/Hackathon_4/FTE/AI_Employee_Vault \
  --max-iterations 10
```

---

## 🔄 Workflow

```
1. Drop file in /Inbox
         │
         ▼
2. File Watcher detects → creates action file in /Needs_Action
         │
         ▼
3. Qwen Code processes the file
         │
         ▼
4. Actions taken, Dashboard updated
         │
         ▼
5. File moved to /Done
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
| **Qwen Code Integration** | ✅ | Reads/writes to vault, processes files |
| **Agent Skills** | ✅ | `file-processor.md` skill definition |
| **Ralph Loop** | ✅ | Autonomous processing orchestrator |

---

## 🛠️ Scripts

### filesystem_watcher.py

Monitors the Inbox folder for new files and creates actionable `.md` files in `Needs_Action`.

**Features:**
- Detects priority keywords (urgent, important, normal)
- Identifies file types (document, invoice, image)
- Tracks processed files to avoid duplicates
- Configurable check interval

### ralph_orchestrator.py

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
