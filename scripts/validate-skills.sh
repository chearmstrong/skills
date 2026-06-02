#!/usr/bin/env bash
#
# Validate Agent Skill directories with skills-ref.
#
# Usage:
#   ./scripts/validate-skills.sh
#   ./scripts/validate-skills.sh skills/review-pr
#
# Paths are resolved from the repository root, regardless of the current
# working directory. With no argument, validates every skill directory directly
# under skills/. With an argument, validates either that individual skill
# directory or every skill directory directly under the provided bundle
# directory.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="${1:-skills}"

cd "$repo_root"

if [[ "${target}" == "-h" || "${target}" == "--help" ]]; then
  sed -n '2,/^set -euo pipefail/p' "$0" | sed '$d; s/^# \{0,1\}//'
  exit 0
fi

if [[ ! -d "$target" ]]; then
  echo "Skill path does not exist: $target" >&2
  exit 1
fi

if [[ -f "$target/SKILL.md" ]]; then
  npx --yes skills-ref validate "$target"
  exit 0
fi

found=0
status=0

while IFS= read -r skill_file; do
  found=1
  skill_dir="$(dirname "$skill_file")"
  echo "Validating $skill_dir"
  if ! npx --yes skills-ref validate "$skill_dir"; then
    status=1
  fi
done < <(find "$target" -mindepth 2 -maxdepth 2 -type f -name SKILL.md | sort)

if [[ "$found" -eq 0 ]]; then
  echo "No skill directories found under: $target" >&2
  exit 1
fi

exit "$status"
