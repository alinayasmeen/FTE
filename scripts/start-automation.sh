#!/bin/bash
# AI Employee - Start Full Automation
# This script starts the combined orchestrator with Qwen integration

VAULT_PATH="/home/alina/Hackathon_4/FTE/AI_Employee_Vault"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========================================"
echo "AI Employee - Full Automation"
echo "========================================"
echo ""
echo "Vault: $VAULT_PATH"
echo "Mode: Continuous Watch"
echo ""
echo "Monitoring:"
echo "  📁 Inbox/           → Auto-create action files"
echo "  📁 Needs_Action/    → Auto-process tasks"
echo "  📁 Approved/        → Auto-execute approvals"
echo ""
echo "Press Ctrl+C to stop"
echo "========================================"
echo ""

# Activate virtual environment if exists
if [ -d "$SCRIPT_DIR/../.venv" ]; then
    source "$SCRIPT_DIR/../.venv/bin/activate"
fi

# Run the combined orchestrator
python3 "$SCRIPT_DIR/orchestrator.py" \
    --vault-path "$VAULT_PATH" \
    --watch \
    --interval 5
