# Quick Start Guide - ResourceConnect

Important: This is a Django app. Use Django's dev server for local testing. Do not use VS Code Live Server for app routes, because it serves static files only.

## Prerequisites
- Python 3.11 or 3.12 recommended; Python 3.14 also works with the current requirements
- Node.js LTS
- PostgreSQL (or update `.env` to use SQLite for local dev)

## Setup Steps

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Install Frontend Dependencies
```bash
npm install
```

### 4. Create `.env` file (already created)
The `.env` file is configured for local PostgreSQL. For SQLite development:
```
DEBUG=True
SECRET_KEY=django-insecure-dev-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1
```

And update `config/settings.py` to use SQLite:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 5. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Build Tailwind CSS
```bash
npm run build:css
```

### 8. Run Development Server
In one terminal:
```bash
python manage.py runserver
```

In another terminal, watch Tailwind CSS:
```bash
npm run watch:css
```

### 9. Open Browser
Visit: http://127.0.0.1:8000/

Admin panel: http://127.0.0.1:8000/admin/

## Project Structure
```
Group-6/
├── config/                 # Django settings, urls, wsgi
├── apps/
│   ├── core/              # Homepage and static pages
│   ├── resources/         # Resource listings
│   ├── opportunities/     # Volunteer/donation opportunities
│   └── users/             # User accounts
├── templates/             # HTML templates
├── static/
│   ├── css/               # Generated Tailwind output
│   ├── src/               # Input CSS
│   └── js/                # JavaScript files
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Next Steps
- Implement Resource model and views
- Create "Get Involved" page
- Set up map integration for resource finder
- Add user authentication
- Connect to Supabase for production database

## Deployment
- Vercel deployment instructions are in [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)
