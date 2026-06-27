# Backend Requirements for Pet Supplies Store

This document describes backend updates needed by the Vue frontend for the pet supplies independent website.

## Current Frontend Context

- Project type: Django backend + Vue frontend.
- Website positioning: overseas pet supplies independent store for young pet owners.
- Current frontend pages: 首页, 产品, 产品详情, 工厂, 定制, 联系, About, FAQ, Shipping, Return.
- Existing real API: `POST /api/contracts/` writes contact form data into SQLite table `contract`.
- Current product, review, collection, and newsletter data are frontend mock data.

## Priority 1: Product Catalog API

The frontend needs real product data to replace mock products in `frontend/src/App.vue`.

### Suggested Model: Product

Fields:

- `id`
- `slug`
- `name`
- `category`
- `price`
- `currency`
- `tag`
- `short_description`
- `description`
- `image`
- `gallery`
- `material`
- `care`
- `fit`
- `is_best_seller`
- `is_active`
- `sort_order`
- `created_at`
- `updated_at`

### Suggested API

- `GET /api/products/`
  - Returns active product list.
  - Supports optional filters: `category`, `is_best_seller`.

- `GET /api/products/<slug>/`
  - Returns product detail.

### Frontend Usage

- 首页 Best Sellers 区读取 `GET /api/products/?is_best_seller=true`
- 产品列表页读取 `GET /api/products/`
- 产品详情页读取 `GET /api/products/<slug>/`

## Priority 2: Collection API

The frontend has four main collections:

- Feeding
- Grooming
- Walking
- Gift Sets

### Suggested Model: Collection

Fields:

- `id`
- `slug`
- `name`
- `title`
- `description`
- `image`
- `sort_order`
- `is_active`

### Suggested API

- `GET /api/collections/`
- `GET /api/collections/<slug>/`

## Priority 3: Reviews / Testimonials API

The homepage currently uses mock customer reviews.

### Suggested Model: Testimonial

Fields:

- `id`
- `quote`
- `name`
- `profile`
- `rating`
- `is_active`
- `sort_order`

### Suggested API

- `GET /api/testimonials/`

## Priority 4: Newsletter API

The newsletter block is currently frontend-only.

### Suggested Model: NewsletterSubscriber

Fields:

- `id`
- `email`
- `source`
- `created_at`

### Suggested API

- `POST /api/newsletter/`

Request body:

```json
{
  "email": "you@example.com",
  "source": "homepage"
}
```

Expected response:

```json
{
  "success": true,
  "message": "Subscribed successfully."
}
```

## Priority 5: Editable Site Content

To avoid hardcoding policy and brand pages in Vue, add editable backend content for:

- About
- FAQ
- Shipping
- Return

### Suggested Model: SitePage

Fields:

- `id`
- `slug`
- `title`
- `subtitle`
- `content`
- `is_active`
- `updated_at`

### Suggested API

- `GET /api/pages/<slug>/`

Suggested slugs:

- `about`
- `faq`
- `shipping`
- `return`

## Priority 6: Admin Menu

Add Django Admin / Simple UI menus for:

- 产品管理
  - 产品列表
  - 产品分类
- 内容管理
  - 首页评价
  - Newsletter 订阅
  - 页面内容
- 联系表单
  - 保留当前已有菜单和数据查询能力

## Compatibility Requirements

- Do not break current `POST /api/contracts/`.
- Do not rename existing `contract` table unless a migration plan is provided.
- Keep SQLite usable for local development.
- API responses should be JSON.
- Add CORS only if frontend and backend are later served on different ports.
- Add seed data or fixtures for local frontend testing if possible.

## Suggested Implementation Order

1. Add `Product` and `Collection` models, migrations, admin registration, and list APIs.
2. Add `Testimonial` model and homepage API.
3. Add `NewsletterSubscriber` model and submit API.
4. Add `SitePage` model and API for About / FAQ / Shipping / Return.
5. Add Simple UI menu entries for the new backend sections.
6. Run migrations and create initial seed data.

## Frontend Follow-up After Backend Update

After backend APIs are ready, frontend should:

- Replace mock `products` with `GET /api/products/`.
- Replace mock `collections` with `GET /api/collections/`.
- Replace mock `reviews` with `GET /api/testimonials/`.
- Connect newsletter form to `POST /api/newsletter/`.
- Load About / FAQ / Shipping / Return content from `GET /api/pages/<slug>/`.
