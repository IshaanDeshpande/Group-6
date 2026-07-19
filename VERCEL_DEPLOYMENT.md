# Vercel Deployment Guide (Django)

This project is a Django app with server-rendered templates. It must be deployed as a Python app, not a static site and not a Next.js app.

## 1. Repo Requirements (already set)

- Entry function: [api/index.py](api/index.py)
- Django WSGI app: [config/wsgi.py](config/wsgi.py)
- Vercel config: [vercel.json](vercel.json)
- Ignore Next build artifacts: [.vercelignore](.vercelignore)

## 2. Vercel Project Settings

In Vercel, open the project and set:

1. Root Directory: repository root (folder containing manage.py)
2. Framework Preset: Other
3. Build Command:
   npm install && npm run build:css && python manage.py collectstatic --noinput
4. Install Command: leave default
5. Output Directory: leave empty

## 3. Environment Variables

Set these in Vercel Project -> Settings -> Environment Variables:

Required:
- SECRET_KEY = a strong random string
- DEBUG = False
- ALLOWED_HOSTS = .vercel.app
- CSRF_TRUSTED_ORIGINS = https://<your-project>.vercel.app

Database (if using Postgres/Supabase):
- DB_ENGINE = django.db.backends.postgresql
- DB_NAME = <db name>
- DB_USER = <db user>
- DB_PASSWORD = <db password>
- DB_HOST = <db host>
- DB_PORT = 5432

Notes:
- Settings also accept DATABASE_* names for compatibility.
- If you do not provide DB_* or DATABASE_* values, Django falls back to local sqlite settings.

Optional:
- CORS_ALLOWED_ORIGINS = https://<your-project>.vercel.app
- AI_API_KEY, AI_API_URL, AI_MODEL

## 4. Deploy

1. Push latest changes to the branch connected to Vercel.
2. Trigger a new deployment (do not retry an old deployment).
3. Wait for build completion.

## 5. Verify URLs

After deploy, test these directly:

- /
- /get-involved/
- /resources/
- /users/signup/

Expected: all routes render Django templates with CSS.

## 6. If You See "Cannot GET /get-involved/"

That means Vercel is still serving static/Next runtime instead of Django.

Check again:

1. Framework Preset is Other
2. Root Directory points to the Django repo root
3. Latest commit includes [vercel.json](vercel.json)
4. Deployment is new, not retried from old config

## 7. Local Testing Reminder

Do not use Live Server for this project. Live Server only serves static files and cannot render Django routes/templates.

Use Django dev server instead:

python manage.py runserver
