# AGENTS.md

## Project Identity

This is a Django + Vue pet supplies independent website project.

The site is positioned as a high-visual-quality pet supplies independent store for young overseas pet owners. It should feel like a modern pet and home lifestyle brand, not a wholesale catalog, discount shop, or generic marketplace storefront.

## Brand And Frontend Direction

- Target audience: young overseas pet owners, especially cat owners and small-dog owners who care about home aesthetics.
- Positioning: good-looking, practical, lightweight, non-food, non-medical pet lifestyle essentials.
- Core scenarios: feeding, grooming, walking, and giftable starter sets.
- Visual style: clean, gentle, warm, home-friendly, lifestyle-oriented.
- Avoid: wholesale-site styling, cluttered product grids, aggressive discounts, loud saturated colors, heavy gradients, childish cartoon styling, and random decorative effects.
- Prefer: soft neutral backgrounds, sage green, mist blue, warm beige, natural light feeling, rounded cards, restrained shadows, readable typography, and product scenes that feel suitable for a real home.

## Technical Stack

- Backend: Django
- Frontend: Vue + Vite
- Database: SQLite during local development
- Admin UI: Django Admin with Simple UI
- Frontend build output is served by Django from `frontend/dist`.

## Current Important Areas

- Django settings and routing: `config/`
- Main Django app: `core/`
- Vue frontend: `frontend/src/`
- Contact form API writes to the `contract` SQLite table.
- Project handoff log: `docs/CODEX_HANDOFF.md`

## Planning Source

The project planning documents live outside this repository in the Obsidian vault:

`C:\Users\Le\Downloads\pet-supplies-obsidian-vault\pet-supplies-obsidian-vault`

Key files:

- `01-项目战略\项目企划书.md`
- `02-品牌定位\品牌定位.md`
- `02-品牌定位\视觉风格.md`
- `05-独立站\网站结构.md`
- `05-独立站\首页文案框架.md`

When a task mentions the project plan, website positioning, brand direction, product strategy, or visual style, read the relevant Obsidian planning files before making frontend or product-direction changes.

## Working Rules

1. Before making changes, inspect the current project structure and relevant files.
2. Follow the existing code style and project shape.
3. Do not delete or replace existing functionality unless the user explicitly asks.
4. Keep Django Admin and the contact form data flow working.
5. When changing the Vue frontend, run `npm run build` from `frontend`.
6. When changing Django code or settings, run `python manage.py check`.
7. Every completed task must update `docs/CODEX_HANDOFF.md`.
8. Each final response should include:
   - Files changed
   - What was implemented
   - How it was tested
   - Suggested next step

## Local Commands

Start Django:

```powershell
.\.venv\Scripts\python.exe manage.py runserver 127.0.0.1:8000
```

Check Django:

```powershell
.\.venv\Scripts\python.exe manage.py check
```

Build Vue:

```powershell
cd frontend
npm run build
```
