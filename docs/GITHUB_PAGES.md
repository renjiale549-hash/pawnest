# GitHub Pages Frontend Deployment

This project can publish the Vue frontend to the free GitHub Pages URL:

```text
https://renjiale549-hash.github.io/pawnest/
```

GitHub Pages can only host the static Vue build. It cannot run Django, SQLite, PostgreSQL, Django Admin, email sending, inquiry saving, or order saving.

## What Works On GitHub Pages

- Home page
- Product UI with fallback products if the API is unavailable
- Product detail UI
- Cart UI stored in the browser with `localStorage`
- Checkout page UI
- Contact/inquiry form UI

## What Needs A Backend

- `GET /api/products/`
- `POST /api/contracts/`
- `POST /api/orders/`
- `POST /api/newsletter/`
- Django Admin
- Database storage
- Email notifications

To make those work later, deploy Django separately and point the frontend API calls to that backend.

## Build Locally For Django

The default local build still uses `/static/` because Django serves `frontend/dist`:

```powershell
cd frontend
npm run build
```

## Test GitHub Pages Build Locally

```powershell
cd frontend
$env:VITE_BASE_PATH="/pawnest/"
npm run build
```

The generated `frontend/dist/index.html` should reference assets under `/pawnest/assets/...`.

## GitHub Pages Setup

After pushing this repository to GitHub:

1. Open `https://github.com/renjiale549-hash/pawnest`.
2. Go to `Settings`.
3. Go to `Pages`.
4. Under `Build and deployment`, set `Source` to `GitHub Actions`.
5. Push to the `main` branch.
6. Open the `Actions` tab and wait for `Deploy frontend to GitHub Pages` to finish.
7. Visit:

```text
https://renjiale549-hash.github.io/pawnest/
```

## Routing Note

The current Vue frontend does not use Vue Router history mode. It switches sections with local component state, so GitHub Pages refresh 404 issues are avoided for the current site.
