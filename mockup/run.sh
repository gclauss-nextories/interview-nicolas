#!/usr/bin/env bash
# Installe, construit et sert la maquette sur http://localhost:${PORT:-3001}/vente-de-leads.
set -euo pipefail

cd "$(dirname "$0")"

# Charge la version de Node de .nvmrc quand nvm est installé.
if [ -s "${NVM_DIR:-$HOME/.nvm}/nvm.sh" ]; then
  . "${NVM_DIR:-$HOME/.nvm}/nvm.sh"
  nvm install >/dev/null
  nvm use >/dev/null
fi

if ! command -v node >/dev/null; then
  echo "Node.js 20 ou plus récent est requis." >&2
  exit 1
fi

[ -d node_modules ] || npm install
npm run build

export PORT="${PORT:-3001}"
echo "Maquette disponible sur http://localhost:${PORT}/vente-de-leads"
node .output/server/index.mjs
