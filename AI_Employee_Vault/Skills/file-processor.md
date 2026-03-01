# Agent Skill: File Processor

## Overview

This Agent Skill enables Qwen Code to process files dropped into the AI Employee vault's `/Needs_Action` folder. It follows the Bronze Tier requirements for the Personal AI Employee hackathon.

## Installation

Add this skill to your Qwen Code configuration by referencing this file or copying the skill definition to your `.qwen/skills/` directory.

## Skill Definition

```yaml
name: file-processor
description: Process files from the Needs_Action folder, categorize them, and move to Done when complete
version: 1.0.0
author: AI Employee Bronze Tier

capabilities:
  - Read files from Needs_Action folder
  - Categorize file type and priority
  - Extract content and metadata
  - Create action plans for multi-step tasks
  - Move completed items to Done folder
  - Update Dashboard.md with activity

triggers:
  - Files appear in /Needs_Action/FILE_*.md
  - Manual invocation via /process-files command

permissions:
  - Read: /Needs_Action/**
  - Write: /Needs_Action/**, /Done/**, /Dashboard.md
  - Execute: File operations only (no external API calls)
```

## Usage

### Automatic Processing

When the File System Watcher detects a new file, it creates an action file in `/Needs_Action/`. Qwen Code should:

1. Check `/Needs_Action/` for pending files
2. Read each `FILE_*.md` action file
3. Process according to priority and type
4. Move to `/Done/` with completion timestamp

### Manual Invocation

Ask Qwen to:
```
- "Process all files in /Needs_Action folder"
- "Process FILE_DOCUMENT_invoice_20260226.md"
- "Show me what's in Needs_Action"
```

## Processing Workflow

### Step 1: Read and Categorize

```
1. Read the action file metadata (frontmatter)
2. Identify file type and priority
3. Check Company_Handbook.md for relevant rules
```

### Step 2: Take Action

Based on file type:

| Type | Action |
|------|--------|
| document | Read, summarize, extract key points |
| invoice | Check amount, flag if > $500, log in Accounting |
| image | Describe content, extract any text |
| spreadsheet | Summarize data, identify trends |
| contract | Highlight key terms, flag for review |

### Step 3: Create Plan (if multi-step)

For complex tasks, create `Plans/PLAN_<filename>.md`:

```markdown
---
type: plan
created: 2026-02-26T10:00:00Z
status: in_progress
---

# Plan: Process [File Name]

## Steps

- [ ] Step 1: Review content
- [ ] Step 2: Extract key information
- [ ] Step 3: Take required action
- [ ] Step 4: Update Dashboard
- [ ] Step 5: Move to Done

## Notes

_Add progress notes here_
```

### Step 4: Update Dashboard

After processing, update `Dashboard.md`:

```markdown
## Recent Activity Log

| Time | Action | Status |
|------|--------|--------|
| 2026-02-26 10:00 | Processed FILE_DOCUMENT_invoice_001.md | ✅ |
```

### Step 5: Move to Done

Move the action file to `/Done/` with completion metadata:

```markdown
---
completed: 2026-02-26T10:05:00Z
processing_time: 5 minutes
---

[Original content preserved]
```

## Error Handling

### If file cannot be processed:

1. Add error note to the action file
2. Move to `/Needs_Action/Review_Required/`
3. Update Dashboard with alert
4. Log error details

### If approval needed:

1. Create approval request in `/Pending_Approval/`
2. Reference original action file
3. Wait for human to move to `/Approved/`
4. Process only after approval

## Examples

### Example 1: Processing an Invoice

```
Input: FILE_INVOICE_client123_20260226.md
- Amount: $350 (below $500 threshold)
- Action: Log in Accounting, mark as paid
- Output: Move to Done, update Dashboard
```

### Example 2: Processing a Contract

```
Input: FILE_CONTRACT_vendor_agreement_20260226.md
- Type: Legal document
- Action: Extract key terms, flag for human review
- Output: Create summary, move to Pending_Approval
```

## Integration with Other Skills

This skill works alongside:

- **email-processor**: For email-based file drops
- **approval-manager**: For items requiring human approval
- **dashboard-updater**: For maintaining Dashboard.md
- **weekly-briefing**: For including processed files in reports

## Testing

To test this skill:

1. Create a test file in `/Inbox/`
2. Wait for watcher to create action file
3. Run: `claude "Process all files in Needs_Action"`
4. Verify file moved to `/Done/`
5. Check Dashboard.md updated

---

*This skill is part of the Bronze Tier deliverables for the Personal AI Employee Hackathon*
