# FTE - Full Time AI Employee

## Project Overview

**FTE** (Full Time Equivalent) is a hackathon project for building a **Personal AI Employee**—an autonomous AI agent that proactively manages personal and business affairs 24/7. The project leverages **Qwen Code** as the reasoning engine and **Obsidian** as the local-first dashboard/memory system.

### Core Architecture

The architecture follows a **Perception → Reasoning → Action** pattern:

| Layer | Component | Purpose |
|-------|-----------|---------|
| **Perception** | Python Watcher Scripts | Monitor Gmail, WhatsApp, filesystems for new events |
| **Reasoning** | Qwen Code | Analyze events, create plans, make decisions |
| **Action** | MCP Servers / File Operations | Execute external actions (email, browser, payments) |
| **Memory/GUI** | Obsidian Vault | Local Markdown-based dashboard and long-term memory |

### Key Concepts

- **Digital FTE**: An AI agent priced and managed like a human employee (168 hrs/week availability, 85-90% cost reduction vs. human)
- **Watchers**: Lightweight Python scripts that monitor external systems and create `.md` files in `/Needs_Action` folder
- **Ralph Wiggum Loop**: A Stop hook pattern that keeps Claude iterating until multi-step tasks are complete
- **Human-in-the-Loop (HITL)**: Sensitive actions require moving approval files from `/Pending_Approval` to `/Approved`
- **Monday Morning CEO Briefing**: Autonomous weekly audit generating revenue reports, bottleneck analysis, and proactive suggestions

### Tech Stack

| Component | Technology |
|-----------|------------|
| Reasoning Engine | Qwen Code |
| Dashboard/Memory | Obsidian (local Markdown) |
| Orchestration | Python 3.13+ |
| External Actions | MCP (Model Context Protocol) servers |
| Browser Automation | Playwright |
| Version Control | Git / GitHub Desktop |

## Directory Structure

```
FTE/
├── README.md                          # Project title
├── Personal AI Employee Hackathon 0_...md  # Comprehensive hackathon guide (1201 lines)
├── skills-lock.json                   # Tracks installed skills (browsing-with-playwright)
├── LICENSE                            # MIT License
├── .qwen/skills/                      # Qwen skills directory
│   └── browsing-with-playwright/      # Playwright automation skill
│       ├── SKILL.md
│       ├── references/playwright-tools.md
│       └── scripts/
│           ├── mcp-client.py
│           ├── start-server.sh
│           ├── stop-server.sh
│           └── verify.py
└── .git/
```

## Building and Running

### Prerequisites

| Software | Version | Purpose |
|----------|---------|---------|
| Claude Code | Active subscription | Primary reasoning engine |
| Obsidian | v1.10.10+ | Knowledge base & dashboard |
| Python | 3.13+ | Sentinel scripts & orchestration |
| Node.js | v24+ LTS | MCP servers & automation |
| GitHub Desktop | Latest | Version control |

### Setup Steps

1. **Create Obsidian Vault**: Name it `AI_Employee_Vault` with folders:
   - `/Inbox` - Raw incoming items
   - `/Needs_Action` - Items requiring processing
   - `/Done` - Completed tasks
   - `/Pending_Approval` - Awaiting human approval
   - `/Approved` - Approved actions ready for execution

2. **Verify Qwen Code** is available in your environment

3. **Set up Python project** (UV recommended):
   ```bash
   uv init
   uv add playwright watchdog google-api-python-client
   ```

4. **Install Node.js dependencies**:
   ```bash
   npm install -g @modelcontextprotocol/server-filesystem
   ```

5. **Configure Qwen** using `qwen-config.json`

### Running Watchers

Example File System Watcher:
```bash
python scripts/filesystem_watcher.py \
  --vault-path /home/alina/Hackathon_4/FTE/AI_Employee_Vault \
  --drop-folder /home/alina/Hackathon_4/FTE/AI_Employee_Vault/Inbox
```

### Starting Ralph Wiggum Loop

```bash
# Start autonomous processing loop
python scripts/ralph_orchestrator.py \
  --vault-path /home/alina/Hackathon_4/FTE/AI_Employee_Vault \
  --max-iterations 10
```

### Using Qwen Code

Ask Qwen to process files:
- "Process all files in /Needs_Action folder"
- "Follow Company_Handbook.md rules when processing"
- "Update Dashboard.md with current status"

## Development Conventions

### File Naming Conventions

- **Action Files**: `TYPE_Description_YYYY-MM-DD.md` (e.g., `EMAIL_ClientInquiry_2026-01-07.md`)
- **Approval Files**: `APPROVAL_REQUIRED_Action_Description.md`
- **Plans**: `Plan.md` or `Plans/ProjectName_Plan.md`
- **Briefings**: `YYYY-MM-DD_Day_Briefing.md`

### Markdown Frontmatter Schema

All action files use YAML frontmatter:
```yaml
---
type: email|whatsapp|file_drop|approval_request|payment
from: Sender Name
subject: Subject Line
received: 2026-01-07T10:30:00Z
priority: high|medium|low
status: pending|in_progress|completed
---
```

### Agent Skills

All AI functionality should be implemented as **Agent Skills**:
- Skills are reusable, composable functions
- Each skill handles a specific domain (email, payments, social media)
- Skills communicate via the Obsidian vault filesystem
- See `AI_Employee_Vault/Skills/file-processor.md` for the Bronze Tier skill

### Human-in-the-Loop Pattern

For sensitive actions (payments, sending messages):

1. Claude creates approval request in `/Pending_Approval/`
2. User reviews and moves file to `/Approved` or `/Rejected`
3. Orchestrator triggers MCP action only for approved items
4. Result logged and task moved to `/Done`

### Error Handling

- Watchers log errors but continue running
- Failed tasks remain in `/Needs_Action` with error notes
- Ralph Wiggum loop has max iterations to prevent infinite loops
- Graceful degradation: if one watcher fails, others continue

## Hackathon Tiers

| Tier | Time | Deliverables |
|------|------|--------------|
| **Bronze** | 8-12 hrs | Obsidian dashboard, 1 watcher, basic Claude integration |
| **Silver** | 20-30 hrs | 2+ watchers, MCP server, HITL workflow, scheduling |
| **Gold** | 40+ hrs | Full integration, Odoo accounting, multiple MCPs, weekly audit |
| **Platinum** | 60+ hrs | Cloud deployment, domain specialization, A2A upgrade |

## Key Resources

- **Hackathon Guide**: `Personal AI Employee Hackathon 0_ Building Autonomous FTEs in 2026.md` (full architectural blueprint)
- **Playwright Skill**: `.qwen/skills/browsing-with-playwright/` (browser automation)
- **Zoom Meetings**: Wednesdays 10:00 PM PKT (Research & Show Case)
- **YouTube**: [@panaversity](https://www.youtube.com/@panaversity)

## License

MIT License - Copyright (c) 2026 Hafiza Alina Yasmeen
