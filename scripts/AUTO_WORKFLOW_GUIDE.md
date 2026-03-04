# 🚀 Auto Workflow - Quick Start Guide

## Complete Automated Workflow

This is the **recommended workflow** for the AI Employee system with full Qwen integration.

---

## 📋 Workflow Overview

```
📥 Inbox/
    │
    ▼ (File dropped)
🔄 Auto-Detect → 📊 Dashboard Updated
    │
    ▼
📋 Create Plan → Plans/
    │
    ▼
⏳ Move to Pending_Approval/
    │
    ▼
🙋 YOU: Move to Approved/
    │
    ▼
✅ Auto-Execute:
   ├── 🎯 Create Action → Needs_Action/
   ├── 💰 Create Entry → Accounting/
   ├── 📝 Log → Updates/
   ├── 📊 Update Dashboard
   └── 📦 Move to Done/
```

**You only need to do ONE thing:** Move file from `Pending_Approval/` to `Approved/`

---

## 🎯 Quick Start

### 1. Start the Auto Workflow

```bash
cd /home/alina/Hackathon_4/FTE

# Start in watch mode (continuous monitoring)
python scripts/auto_workflow.py --vault-path /home/alina/Hackathon_4/FTE/AI_Employee_Vault --watch
```

### 2. Drop a File in Inbox

```bash
# Example: Create a test file
cat > AI_Employee_Vault/Inbox/TEST_Email_2026-03-03.md << 'EOF'
---
type: email
from: test@example.com
subject: Test Email
priority: high
---

# Test Email Content

This is a test email for workflow demonstration.
EOF
```

### 3. Watch the Magic Happen

**Terminal output:**
```
INFO - 📥 Detected new file in Inbox: TEST_Email_2026-03-03.md
INFO - 📊 Dashboard updated: New file detected
INFO - 📋 Created plan: PLAN_TEST_Email_2026-03-03_20260303_190000.md
INFO - ⏳ Moved to Pending_Approval: PLAN_TEST_Email_...md
```

### 4. Approve the Plan

**You move the file:**
```bash
mv AI_Employee_Vault/Pending_Approval/PLAN_*.md \
   AI_Employee_Vault/Approved/
```

### 5. Watch Auto-Execution

**Terminal output:**
```
INFO - ✅ Detected approved file: PLAN_TEST_Email_...md
INFO - 🎯 Created action: ACTION_PLAN_...md
INFO - ✅ Executed action
INFO - 📝 Created execution log: LOG_...md
INFO - 📊 Dashboard updated: Executed
INFO - 📦 Moved to Done: TEST_Email_2026-03-03.md
```

### 6. Check Results

```bash
# All folders clean!
ls AI_Employee_Vault/Inbox/           # Empty ✅
ls AI_Employee_Vault/Needs_Action/    # Empty ✅
ls AI_Employee_Vault/Pending_Approval/ # Empty ✅
ls AI_Employee_Vault/Approved/        # Empty ✅

# Results in Done/
ls AI_Employee_Vault/Done/

# Accounting entry created
ls AI_Employee_Vault/Accounting/

# Execution log created
ls AI_Employee_Vault/Updates/

# Dashboard updated
cat AI_Employee_Vault/Dashboard.md
```

---

## 📁 Folder Usage

| Folder | Purpose | Auto-Cleaned |
|--------|---------|--------------|
| `Inbox/` | Drop new files here | ✅ Yes |
| `Plans/` | Temporary (plan creation) | ✅ Yes |
| `Pending_Approval/` | Awaiting your approval | ⏳ Until you approve |
| `Approved/` | Approved plans | ✅ Yes |
| `Needs_Action/` | Actions to execute | ✅ Yes |
| `Done/` | Completed items | 📦 Archive |
| `Accounting/` | Financial entries | 📊 Keep |
| `Updates/` | Execution logs | 📊 Keep |
| `Briefings/` | Weekly reports | 📊 Keep |
| `Files/` | Reference copies | 📊 Keep |

---

## 🔧 Command Reference

### Start Auto Workflow

```bash
# Watch mode (recommended)
python scripts/auto_workflow.py \
  --vault-path /home/alina/Hackathon_4/FTE/AI_Employee_Vault \
  --watch

# Single run (test)
python scripts/auto_workflow.py \
  --vault-path /home/alina/Hackathon_4/FTE/AI_Employee_Vault
```

### Check Status

```bash
# Show all folder counts
echo "Inbox: $(ls -1 AI_Employee_Vault/Inbox/*.md 2>/dev/null | wc -l)"
echo "Pending: $(ls -1 AI_Employee_Vault/Pending_Approval/*.md 2>/dev/null | wc -l)"
echo "Approved: $(ls -1 AI_Employee_Vault/Approved/*.md 2>/dev/null | wc -l)"
echo "Done: $(ls -1 AI_Employee_Vault/Done/*.md 2>/dev/null | wc -l)"
```

### View Dashboard

```bash
cat AI_Employee_Vault/Dashboard.md
```

---

## 🎬 Demo Video Script

### Scene 1: Start Workflow (0:00-1:00)
```bash
# Show terminal
python scripts/auto_workflow.py --vault-path ... --watch

# Explain: "This monitors all folders automatically"
```

### Scene 2: Drop File (1:00-2:00)
```bash
# Drop file in Inbox
# Show dashboard updating in real-time
cat AI_Employee_Vault/Dashboard.md
```

### Scene 3: Plan Creation (2:00-3:00)
```bash
# Show plan created in Pending_Approval
ls AI_Employee_Vault/Pending_Approval/
cat AI_Employee_Vault/Pending_Approval/PLAN_*.md
```

### Scene 4: Approval (3:00-4:00)
```bash
# YOU move file to Approved
mv AI_Employee_Vault/Pending_Approval/PLAN_*.md \
   AI_Employee_Vault/Approved/

# Explain: "This is the only manual step"
```

### Scene 5: Auto-Execution (4:00-6:00)
```bash
# Show terminal output
# Show accounting entry created
cat AI_Employee_Vault/Accounting/ENTRY_*.md

# Show execution log
cat AI_Employee_Vault/Updates/LOG_*.md
```

### Scene 6: Clean Folders (6:00-7:00)
```bash
# Show all folders clean
ls AI_Employee_Vault/Inbox/
ls AI_Employee_Vault/Needs_Action/
ls AI_Employee_Vault/Pending_Approval/

# Show Done folder
ls AI_Employee_Vault/Done/
```

### Scene 7: Final Dashboard (7:00-8:00)
```bash
cat AI_Employee_Vault/Dashboard.md

# Explain: "Everything automated, everything tracked"
```

---

## 💡 Tips

1. **Always run in watch mode** for real-time automation
2. **Check Pending_Approval/** regularly for items needing your approval
3. **Review Dashboard.md** for current status
4. **Keep Done/** folder for audit trail
5. **Review Accounting/** and **Updates/** for financial tracking

---

## 🐛 Troubleshooting

### File not detected in Inbox
- Ensure file has `.md` extension
- Check file wasn't already processed (check `.workflow_state.txt`)
- Restart orchestrator

### Plan not moving to Approved
- You need to manually move it from `Pending_Approval/` to `Approved/`
- The system waits for your approval

### Accounting entry not created
- Ensure file has financial keywords (invoice, purchase, amount)
- Check `Accounting/` folder for entries

### Dashboard not updating
- Check `Dashboard.md` exists
- Ensure write permissions on vault folder

---

## 📚 More Documentation

- [Main README](../README.md) - Project overview
- [Company Handbook](../AI_Employee_Vault/Company_Handbook.md) - Rules & SOPs
- [Bronze Tier Report](../BRONZE_TIER_COMPLETE.md) - Completion checklist

---

*Auto Workflow - Full Automation with Human-in-the-Loop*
*Created: 2026-03-03*
