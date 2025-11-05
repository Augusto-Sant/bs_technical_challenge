**Install & Run**
```bash
uv sync
npm install
uv run python manage.py migrate
````

populate data for orders and products using scripts or just products
```bash
uv run python manage.py import_products
```

**Start server**

```bash
npm run build-theme
uv run python manage.py runserver
```
