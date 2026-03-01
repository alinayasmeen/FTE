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
│  - Opens vault via WSL path       │  - filesystem_watcher.py│
│  - Full access to Linux files     │  - ralph_orchestrator.py│
│                                   │  - Qwen Code integration│
└─────────────────────────────────────────────────────────────┘
           │                                      │
           └────────── Same files! ───────────────┘
              (Direct WSL filesystem access)
```

---

## 🚀 Quick Start (Bronze Tier)

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

Now you can see all files in Obsidian!

### Step 3: Start the File Watcher (Ubuntu/WSL)

```bash
cd /home/alina/Hackathon_4/FTE
source .venv/bin/activate

# Run watcher (uses default path)
python scripts/filesystem_watcher.py
```

Keep this terminal running - it watches for new files!

### Step 4: Test the System

1. **Drop a test file** into the Inbox:
   ```bash
   echo "Test document for processing" > /home/alina/Hackathon_4/FTE/AI_Employee_Vault/Inbox/test.txt
   ```

2. **Wait 5 seconds** - watcher creates action file in `Needs_Action/`

3. **Open Obsidian** - you'll see the new file instantly!

4. **Ask Qwen Code** to process:
   ```
   "Process all files in Needs_Action folder"
   ```

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

### Ralph Wiggum Loop (Autonomous Mode)

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
