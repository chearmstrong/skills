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
# directory. If npx cannot fetch skills-ref because npm registry access is
# unavailable, falls back to the local portable validator when installed at
# ~/.agents/skills/skill-maintenance/scripts/validate_skills.py.
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
target="${1:-skills}"
fallback_validator="${SKILLS_FALLBACK_VALIDATOR:-$HOME/.agents/skills/skill-maintenance/scripts/validate_skills.py}"

cd "$repo_root"

if [[ "${target}" == "-h" || "${target}" == "--help" ]]; then
  sed -n '2,/^set -euo pipefail/p' "$0" | sed '$d; s/^# \{0,1\}//'
  exit 0
fi

if [[ ! -d "$target" ]]; then
  echo "Skill path does not exist: $target" >&2
  exit 1
fi

skill_dirs=()

if [[ -f "$target/SKILL.md" ]]; then
  skill_dirs=("$target")
else
  while IFS= read -r skill_file; do
    skill_dirs+=("$(dirname "$skill_file")")
  done < <(find "$target" -mindepth 2 -maxdepth 2 -type f -name SKILL.md | sort)
fi

if [[ "${#skill_dirs[@]}" -eq 0 ]]; then
  echo "No skill directories found under: $target" >&2
  exit 1
fi

is_npm_network_error() {
  local output="$1"

  [[ "$output" == *"ENOTFOUND"* ]] ||
    [[ "$output" == *"EAI_AGAIN"* ]] ||
    [[ "$output" == *"ECONNRESET"* ]] ||
    [[ "$output" == *"ETIMEDOUT"* ]] ||
    [[ "$output" == *"getaddrinfo"* ]] ||
    [[ "$output" == *"registry.npmjs.org"* ]] ||
    [[ "$output" == *"npm error network"* ]]
}

run_fallback_validator() {
  if [[ ! -f "$fallback_validator" ]]; then
    echo "skills-ref could not be fetched from npm, and no fallback validator was found at: $fallback_validator" >&2
    echo "Install skills-ref, allow npm registry access, or set SKILLS_FALLBACK_VALIDATOR to a local validate_skills.py path." >&2
    return 1
  fi

  echo "skills-ref unavailable because npm registry access failed." >&2
  echo "Falling back to local portable skill validation: $fallback_validator" >&2
  python3 "$fallback_validator" --fallback-only "${skill_dirs[@]}"
}

if [[ -x "$repo_root/node_modules/.bin/skills-ref" ]]; then
  skills_ref=( "$repo_root/node_modules/.bin/skills-ref" "validate" )
  using_npx=0
elif command -v skills-ref >/dev/null 2>&1; then
  skills_ref=( "skills-ref" "validate" )
  using_npx=0
else
  skills_ref=( "npx" "--yes" "skills-ref" "validate" )
  using_npx=1
fi

status=0

for skill_dir in "${skill_dirs[@]}"; do
  echo "Validating $skill_dir"
  output="$("${skills_ref[@]}" "$skill_dir" 2>&1)" || {
    command_status=$?
    if [[ "$using_npx" -eq 1 ]] && is_npm_network_error "$output"; then
      run_fallback_validator
      exit $?
    fi

    printf '%s\n' "$output" >&2
    status="$command_status"
    continue
  }

  printf '%s\n' "$output"
done

exit "$status"
