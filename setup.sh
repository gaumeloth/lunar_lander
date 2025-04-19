#!/usr/bin/env bash
set -euo pipefail

# 1) Crea venv e installa dipendenze
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# 2) Rileva la shell padre del processo
parent_shell="$(ps -p "${PPID}" -o comm= 2>/dev/null || echo "")"
shell_name="$(basename "${parent_shell}")"

# 3) Scegli il comando di attivazione
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

# 4) Messaggio all’utente
cat <<EOF

🎉 Ambiente virtuale creato con successo!

EOF

if [[ -n "${activate_cmd}" ]]; then
  cat <<EOF
Per attivarlo (hai rilevato: ${shell_name}):
    ${activate_cmd}

EOF
else
  cat <<'EOF'
Non sono riuscito a riconoscere automaticamente la tua shell:
  • Bash/Zsh/Ksh/Dash:   source venv/bin/activate
  • Fish:                 source venv/bin/activate.fish
  • Csh/Tcsh:             source venv/bin/activate.csh

EOF
fi

cat <<'EOF'
Per disattivare l'ambiente (in qualsiasi shell):
    deactivate

Buon lavoro con il tuo Lunar Lander! 🚀
EOF
