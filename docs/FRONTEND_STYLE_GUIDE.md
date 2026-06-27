# Frontend Style Guide

## Skill Source

Installed UI/UX skill:

- `.codex/skills/ui-ux-pro-max`

The skill was installed with:

```powershell
npm install -g uipro-cli
uipro init --ai codex
```

The generated skill is project-local. Future Codex sessions should read `.codex/skills/ui-ux-pro-max/SKILL.md` when doing UI/UX work.

## Design System Direction

Based on `ui-ux-pro-max` design-system search for:

`ecommerce pet supplies lifestyle home-friendly gentle modern`

Recommended base logic:

- Pattern: Social Proof-Focused + Trust
- Style: Accessible & Ethical
- Typography: Varela Round for headings, Nunito Sans for body
- Effects: visible focus rings, responsive design, reduced motion support, 44px touch targets

## Project-Specific Override

The skill suggested a more saturated orange/blue palette. For this project, use the Obsidian planning documents as the stronger source of truth and keep the palette softer:

- Milk white: `#FAF6ED`
- Soft gray: `#E7E3DA`
- Sage green: `#A8BE9B`
- Mist blue: `#B8D7DF`
- Warm beige: `#F1D8B6`
- Charcoal: `#243029`

## Brand Feel

The frontend should feel like:

- A pet and home lifestyle brand
- Clean, gentle, modern, useful, home-friendly
- Suitable for young overseas pet owners
- Especially relevant to cat owners and small-dog owners

Avoid:

- Wholesale site styling
- Cheap marketplace styling
- Heavy discount banners
- Loud red or purple color schemes
- Overly childish pet graphics
- Decorative animations that distract from shopping

## Page Structure

Homepage:

1. Hero
2. Feeding / Grooming / Walking / Gift Sets categories
3. Best Sellers
4. Brand value section
5. Customer reviews
6. Newsletter

Product listing:

- Use mock products until real product data exists.
- Product cards must show category, title, price, short benefit, and a details action.

Product detail:

- Title and price
- Core benefits
- Materials
- Cleaning/care
- Shipping note
- Related recommendation

Support pages:

- About
- FAQ
- Shipping
- Return

## Interaction Rules

- Use 150-300ms transitions.
- Use hover feedback without layout shift.
- Respect `prefers-reduced-motion`.
- Avoid horizontal scrolling on mobile.
- Keep inputs labeled.
- Keep focus states visible.

