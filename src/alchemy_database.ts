# Run the Reapers daemon in a secure containerized environment where security checks are active
python src/future_reaper_protocol.py --dry-run

# Or execute directly with full sandboxing enabled (requires specific permissions and setup)
source <(cat > /tmp/reaper.sh << 'EOF')
#!/bin/bash
set -euo pipefail
export PYTHONPATH=/path/to/src:$PYTHONPATH
python3 src/future_reaper_protocol.py --dry-run
EOF

chmod +x /tmp/reaper.sh
/tmp/reaper.sh
