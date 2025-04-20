#!/usr/bin/env bash
set -euo pipefail

# --- 1) Creazione venv ---
python3 -m venv venv

# --- 2) Install runtime deps ---
venv/bin/pip install --upgrade pip || true
venv/bin/pip install -r requirements.txt

# --- 3) Install dev deps (solo se richiesto) ---
if [[ "${1:-}" == "--dev" ]]; then
  echo "✅ Installing development dependencies..."
  venv/bin/pip install -r requirements-dev.txt
fi

# --- 4) Rilevazione shell corrente ---
parent_shell="$(ps -p "${PPID}" -o comm= 2>/dev/null || echo "")"
shell_name="$(basename "${parent_shell}")"

case "${shell_name}" in
fish)
  activate_cmd="source venv/bin/activate.fish"
  ;;
csh | tcsh)
  activate_cmd="source venv/bin/activate.csh"
  ;;
bash | zsh | ksh | dash | sh)
  activate_cmd="source venv/bin/activate"
  ;;
*)
  activate_cmd=""
  ;;
esac

# --- 5) Output istruzioni ---
cat <<EOF

🎉 Ambiente virtuale creato con successo!

EOF

if [[ -n "${activate_cmd}" ]]; then
  cat <<EOF
Per attivarlo (shell rilevata: ${shell_name}):
    ${activate_cmd}

EOF
else
  cat <<'EOF'
Non ho riconosciuto la tua shell.
Per attivarlo, esegui uno di questi comandi:
  • bash/zsh/ksh/dash:  source venv/bin/activate
  • fish:               source venv/bin/activate.fish
  • csh/tcsh:           source venv/bin/activate.csh

EOF
fi

cat <<'EOF'
Per disattivare l'ambiente (in qualsiasi shell):
    deactivate

---
Se vuoi includere anche le dipendenze di sviluppo, rilancia:
    ./setup.sh --dev
EOF
