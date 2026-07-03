# Grocery Project

This is a Django grocery ordering app.

## Deployment

### Local development

1. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

2. Run migrations:
   ```bash
   python manage.py migrate
   ```

3. Collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```

4. Start web server:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

### PythonAnywhere deployment

1. Create a new web app in PythonAnywhere using the manual configuration option.
2. In the Bash console, clone or upload this project and install requirements:
   ```bash
   cd ~/<your-pythonanywhere-username>/grocery_project
   pip install -r requirements.txt
   ```
3. Set these environment variables in the PythonAnywhere Web tab:
   - `DJANGO_SECRET_KEY=<strong-secret>`
   - `DJANGO_DEBUG=False`
   - `DJANGO_ALLOWED_HOSTS=<your-username>.pythonanywhere.com,localhost,127.0.0.1`
   - `DJANGO_CSRF_TRUSTED_ORIGINS=https://<your-username>.pythonanywhere.com`
4. Run database migrations:
   ```bash
   python manage.py migrate
   ```
5. Collect static files:
   ```bash
   python manage.py collectstatic --noinput
   ```
6. Point the PythonAnywhere WSGI file to:
   ```python
   from grocery.wsgi import application
   ```

## Environment variables

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG` (True/False)
- `DJANGO_ALLOWED_HOSTS` (comma-separated)
- `DJANGO_CSRF_TRUSTED_ORIGINS` (comma-separated)
