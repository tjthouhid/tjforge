#!/usr/bin/env bash
# tjforge detect: prints a compact fact sheet about the project in the current
# directory. Read-only. Output is for Claude to draft PROJECT-PROFILE.md from.
set -u

has() { [ -e "$1" ]; }
say() { printf '%s\n' "$*"; }
first() { for f in "$@"; do if has "$f"; then say "$f"; return 0; fi; done; return 1; }

say "== tjforge detect: $(pwd)"

say "-- git"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  say "repo: yes  branch: $(git branch --show-current 2>/dev/null)  commits: $(git rev-list --count HEAD 2>/dev/null || echo 0)"
  say "hooksPath: $(git config --get core.hooksPath || echo '(default)')"
  say "recent subjects:"; git log -5 --pretty='  %s' 2>/dev/null
else
  say "repo: no"
fi

say "-- contract files"
for f in docs/PROJECT-PROFILE.md DESIGN.md CLAUDE.md AGENTS.md README.md .claude/settings.json .claude/agents .githooks/commit-msg; do
  has "$f" && say "present: $f"
done

say "-- manifests"
found=0
for f in package.json pnpm-workspace.yaml turbo.json nx.json pyproject.toml requirements.txt go.mod Cargo.toml composer.json Gemfile pom.xml build.gradle build.gradle.kts pubspec.yaml Package.swift mix.exs deno.json bun.lockb pnpm-lock.yaml yarn.lock package-lock.json; do
  if has "$f"; then say "present: $f"; found=1; fi
done
[ "$found" = 0 ] && say "none (empty or unrecognised project)"

if has package.json; then
  say "-- package.json signals"
  for dep in next react vue nuxt svelte @sveltejs/kit astro solid-js @angular/core remix express fastify hono @nestjs/core \
             typescript tailwindcss styled-components @emotion/react @radix-ui shadcn @mui/material \
             gsap framer-motion motion lenis three \
             prisma drizzle-orm mongoose typeorm \
             vitest jest playwright cypress @testing-library \
             eslint prettier @biomejs/biome husky lint-staged storybook; do
    grep -q "\"$dep" package.json 2>/dev/null && printf '%s ' "$dep"
  done
  echo
  say "scripts: $(python3 -c 'import json;print(", ".join(json.load(open("package.json")).get("scripts",{}).keys()))' 2>/dev/null)"
fi

for f in pyproject.toml requirements.txt; do
  if has "$f"; then
    say "-- $f signals"
    for dep in django fastapi flask sqlalchemy pydantic pytest ruff black mypy pyright celery; do
      grep -qi "$dep" "$f" 2>/dev/null && printf '%s ' "$dep"
    done
    echo
  fi
done
has composer.json && { say "-- composer signals"; for dep in laravel/framework symfony livewire inertiajs pestphp phpunit laravel/pint; do grep -q "$dep" composer.json && printf '%s ' "$dep"; done; echo; }
has Gemfile && { say "-- Gemfile signals"; for dep in rails sinatra rspec rubocop sidekiq hotwire; do grep -q "$dep" Gemfile && printf '%s ' "$dep"; done; echo; }

say "-- tooling config"
for f in tsconfig.json .eslintrc .eslintrc.js .eslintrc.json .eslintrc.cjs eslint.config.js eslint.config.mjs .prettierrc .prettierrc.json prettier.config.js biome.json \
         ruff.toml .rubocop.yml .editorconfig .golangci.yml rustfmt.toml phpstan.neon pint.json \
         Dockerfile docker-compose.yml compose.yaml .github/workflows .gitlab-ci.yml vercel.json netlify.toml fly.toml \
         .env.example .husky; do
  has "$f" && say "present: $f"
done
has tsconfig.json && say "ts strict: $(grep -Eq '"strict"[[:space:]]*:[[:space:]]*true' tsconfig.json && echo yes || echo 'no/unknown')"

say "-- UI signals"
ui=0
for f in tailwind.config.js tailwind.config.ts tailwind.config.mjs components.json .storybook src/components app/components components \
         src/styles styles src/app app pages src/pages public index.html tokens.json design-tokens.json; do
  if has "$f"; then say "present: $f"; ui=1; fi
done
tok=$(grep -rlE -- '--(color|font|space|radius)[a-z0-9-]*:' --include='*.css' --include='*.scss' . 2>/dev/null | grep -v node_modules | head -3)
[ -n "$tok" ] && { say "css token files:"; say "$tok" | sed 's/^/  /'; ui=1; }
fonts=$(grep -rhoE 'fonts\.googleapis\.com/css2?\?family=[^"&'"'"' ]+' --include='*.html' --include='*.css' --include='*.tsx' --include='*.jsx' --include='*.vue' --include='*.astro' . 2>/dev/null | grep -v node_modules | sort -u | head -3)
[ -n "$fonts" ] && { say "google fonts:"; say "$fonts" | sed 's/^/  /'; }
has package.json && grep -qE '"(next|react|vue|nuxt|svelte|astro|solid-js|@angular/core|tailwindcss)"' package.json && ui=1
say "has UI:$([ "$ui" = 1 ] && echo likely || echo 'no signal')"

say "-- tests"
for d in tests test __tests__ spec e2e cypress playwright; do has "$d" && say "present: $d/"; done

say "-- top level"
ls -1A 2>/dev/null | grep -vE '^(node_modules|\.git|dist|build|\.next|vendor|target|\.venv|__pycache__)$' | head -40 | tr '\n' ' '
echo

say "-- files by extension (top 8)"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git ls-files 2>/dev/null
else
  find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/dist/*' -not -path '*/vendor/*' 2>/dev/null | head -5000
fi | awk -F. 'NF>1 {c[$NF]++} END {for (e in c) print c[e], e}' | sort -rn | head -8 | sed 's/^/  /'
