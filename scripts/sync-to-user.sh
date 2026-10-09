#!/usr/bin/env bash
# SPDX-License-Identifier: MIT
# Install this repository's copy of the skill into the user-level skills directory.
#
# The direction is one-way on purpose: git is the source of truth and ~/.agents is the
# installed copy. Edit here, commit, then run this. Never edit the installed copy.
#
# The repository's own machinery (.git, .gitignore, this script, and the .claude-plugin/
# manifests that package the skill for the Claude Code, Codex and Copilot marketplaces) is
# excluded, so the installed copy is SKILL.md, README.md, references/, scripts/ and the
# licence. The checkout directory is only a container; the installed directory is named from the
# `name:` field in SKILL.md, so renaming this folder cannot install the skill under the
# wrong name. Drift is reported by comparing content checksums, so timestamps never
# register as a difference.
#
# Usage: scripts/sync-to-user.sh [--dry-run]
set -euo pipefail

src="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
name="$(awk -F': *' '/^name:/{print $2; exit}' "${src}/SKILL.md" | tr -d '\r')"
[[ -n "$name" ]] || name="$(basename "$src")"
dest="${HOME}/.agents/skills/${name}"
sha="$(command -v shasum || command -v sha256sum)"

# A truncated release is a mistake, not a version of the skill.
empty="$(find "$src" -type f -size 0)"
if [[ -n "$empty" ]]; then
  echo "${name}: refusing to install, these files are empty:" >&2
  printf '%s\n' "$empty" >&2
  exit 1
fi

manifest() {
  (cd "$1" && find . -type f -not -path './.git/*' -not -path './.claude-plugin/*' \
    ! -name 'sync-to-user.sh' ! -name '.gitignore' -print0 \
    | sort -z | xargs -0 "$sha" -a 256 2>/dev/null || true)
}

if [[ -d "$dest" ]]; then
  drift="$(diff <(manifest "$src") <(manifest "$dest") || true)"
  if [[ -z "$drift" ]]; then
    echo "${name}: already in sync with ${dest}"
    exit 0
  fi
  if [[ "${1:-}" == "--dry-run" ]]; then
    echo "${name}: would update ${dest}"
    printf '%s\n' "$drift"
    exit 0
  fi
elif [[ "${1:-}" == "--dry-run" ]]; then
  echo "${name}: not installed at ${dest}"
  exit 0
fi

mkdir -p "$dest"
rsync -rlpt --delete --exclude '.git/' --exclude '.gitignore' --exclude 'sync-to-user.sh' \
  --exclude '.claude-plugin/' "${src}/" "${dest}/"
echo "${name}: installed to ${dest}"
