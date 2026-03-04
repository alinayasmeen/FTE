# AI Employee Vault - Quick Start Guide

**WSL Native Setup**: Windows Obsidian + Ubuntu Python Scripts

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  WINDOWS (GUI)                    │  WSL/UBUNTU (Terminal)  │
│                                   │                         │
│  Obsidian App                     │  Python Scripts         │
│  \\wsl.localhost\Ubuntu\...       │  /home/alina/Hackathon_4│
│  - Opens vault via WSL path       │  - auto_workflow.py     │
│  - Real-time Dashboard updates    │  - Full automation      │
│  - View all folders               │  - Qwen integration     │
└─────────────────────────────────────────────────────────────┘
           │                                      │
           └────────── Same files! ───────────────┘
              (Direct WSL filesystem access)
```

---

## 🚀 Quick Start (Auto Workflow - Recommended)

### Step 1: Install Dependencies (Ubuntu/WSL)

```bash
cd /home/alina/Hackathon_4/FTE

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Open Vault in Obsidian (Windows)

**On Windows side:**

1. Open **Obsidian** app
2. Click **"Open folder as vault"**
3. Navigate to: `\\wsl.localhost\Ubuntu\home\alina\Hackathon_4\FTE\AI_Employee_Vault`
4. Click **"Open"**

> 💡 **Tip**: In Windows File Explorer, type `\\wsl.localhost\Ubuntu` in the address bar to browse WSL files!

Now you can see the Dashboard and all folders in Obsidian!

### Step 3: Start Auto Workflow (Ubuntu/WSL)

```bash
cd /home/alina/Hackathon_4/FTE
source .venv/bin/activate

# Start the complete auto workflow (watch mode)
python scripts/auto_workflow.py --watch
```

Keep this terminal running - it monitors all folders automatically!

### Step 4: Test the Complete Workflow

1. **Drop a file in Inbox/**:
   ```bash
   cat > AI_Employee_Vault/Inbox/TEST_Email_2026-03-03.md << 'EOF'
   ---
   type: email
   from: test@example.com
   subject: Test Email
   priority: high
   ---
   
   # Test Email
   
   This is a test email for workflow demo.
   EOF
   ```

2. **Watch Obsidian Dashboard** - It updates automatically!
   - Pending Approvals count increases
   - Recent Activity Log shows new entry
   - Last Activity timestamp updates

3. **Approve the Plan** (YOUR ONLY MANUAL STEP):
   ```bash
   mv AI_Employee_Vault/Pending_Approval/*.md AI_Employee_Vault/Approved/
   ```

4. **Watch Auto-Execution** in terminal:
   ```
   ✅ Detected approved file
   🎯 Created action
   ✅ Executed action
   💰 Created accounting entry
   📝 Logged in Updates/
   📊 Dashboard updated
   📦 Moved to Done/
   ```

5. **Check Obsidian** - All folders clean, Dashboard updated!

---

## 🔄 Complete Auto Workflow

```
1. 📥 Drop file in Inbox/
         │
         ▼
2. 🔄 Auto-detect → Dashboard updates (visible in Obsidian)
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
   ├── 📝 Execution Log → Updates/
   ├── 📊 Update Dashboard (live in Obsidian)
   └── 📦 Move to Done/
         │
         ▼
7. ✅ COMPLETE - All folders clean!
```

**You only do ONE thing:** Move file from `Pending_Approval/` to `Approved/`

---

## 📁 Vault Paths

| System | Path |
|--------|------|
| **Windows (Obsidian)** | `\\wsl.localhost\Ubuntu\home\alina\Hackathon_4\FTE\AI_Employee_Vault` |
| **WSL/Ubuntu (Scripts)** | `/home/alina/Hackathon_4/FTE/AI_Employee_Vault` |
| **Windows File Explorer** | `\\wsl.localhost\Ubuntu\home\alina\Hackathon_4\FTE\` |

---

## 📂 Folder Structure

```
/home/alina/Hackathon_4/FTE/AI_Employee_Vault/
│
├── Dashboard.md           # Main dashboard
├── Company_Handbook.md    # AI rules
├── QUICKSTART.md          # This guide
├── Inbox/                 # Drop files here
├── Needs_Action/          # Pending tasks
├── Done/                  # Completed
├── Pending_Approval/      # Awaiting approval
├── Approved/              # Approved actions
├── Plans/                 # Task plans
├── Briefings/             # Weekly reports
├── Accounting/            # Financial records
├── Files/                 # Attached files
├── Skills/                # Agent skills
└── Updates/               # Sync updates
```

---

## 🤖 Using Qwen Code

### Basic Commands

Ask Qwen to:
- "Process all files in Needs_Action"
- "What's in my Needs_Action folder?"
- "Create a weekly briefing from items in Done folder"
- "Update Dashboard.md with current status"

### Auto Workflow (Recommended - No Qwen Prompting Needed)

The auto workflow handles everything automatically:

```bash
cd /home/alina/Hackathon_4/FTE
source .venv/bin/activate

# Start continuous monitoring
python scripts/auto_workflow.py --watch
```

**You only approve:** Move files from `Pending_Approval/` to `Approved/`

### Ralph Wiggum Loop (Legacy Mode)

```bash
cd /home/alina/Hackathon_4/FTE
source .venv/bin/activate

python scripts/ralph_orchestrator.py --max-iterations 10
```

---

## 🔗 WSL Path Access from Windows

### Method 1: Direct in Obsidian
- Open Obsidian → "Open folder as vault"
- Type: `\\wsl.localhost\Ubuntu\home\alina\Hackathon_4\FTE\AI_Employee_Vault`

### Method 2: Via File Explorer
1. Open File Explorer
2. Type in address bar: `\\wsl.localhost\Ubuntu`
3. Navigate to `home\alina\Hackathon_4\FTE\AI_Employee_Vault`
4. Right-click → "Open with Obsidian"

### Method 3: Map Network Drive (Optional)
```
Drive: Z:
Path: \\wsl.localhost\Ubuntu\home\alina\Hackathon_4\FTE\AI_Employee_Vault
```
Then access via `Z:` in Windows!

---

## 📋 Bronze Tier Checklist

- [x] Obsidian vault at `\\wsl.localhost\Ubuntu\...\AI_Employee_Vault`
- [x] Dashboard.md created
- [x] Company_Handbook.md created
- [x] File System Watcher working
- [x] Agent Skill defined
- [x] Ralph Wiggum loop configured
- [ ] Test complete workflow

---

## 🔧 Troubleshooting

### Obsidian can't open vault
- Make sure path is `\\wsl.localhost\Ubuntu\home\alina\Hackathon_4\FTE\AI_Employee_Vault`
- Ensure WSL is running (`wsl` command works in PowerShell)
- Try restarting WSL: `wsl --shutdown` then reopen

### Watcher can't access vault
- Ensure folder exists: `ls /home/alina/Hackathon_4/FTE/AI_Employee_Vault`
- Check permissions: `chmod -R 755 /home/alina/Hackathon_4/FTE/AI_Employee_Vault`

### Files not syncing
- Windows and WSL access same physical files
- Refresh Obsidian (Ctrl+R) if changes don't appear
- Ensure WSL filesystem is mounted properly

---

## 📚 Next Steps (Silver Tier)

1. Gmail Watcher for email processing
2. WhatsApp Watcher for messages
3. MCP server for sending emails
4. Human-in-the-loop approval workflow

---

*Built for the Personal AI Employee Hackathon - Bronze Tier*
*WSL Native Setup: Windows Obsidian + Ubuntu Backend*
