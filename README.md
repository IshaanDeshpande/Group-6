## Running website in django server

Open repo in vs code and run this in the terminal:

Use Python 3.11 or 3.12 for the smoothest setup. If you use Python 3.14 on Windows, install from the current `requirements.txt` so pip picks a newer Pillow wheel.

cd C:\Users\popej\Group-6

.venv\Scripts\Activate.ps1

python manage.py runserver

Then, click the link it gives you to open the website dev server


 

## Running AI Chatbot Instructions:

Install Ollama from https://ollama.com

After installing ollama, open the vs code terminal and run: ollama pull llama3.1:8b

Then run ollama in the backround by running: ollama serve

# ResourceConnect

A web application developed as part of the **Computing 4 Good 2026** program at the **Colorado School of Mines**.

## Overview
ResourceConnect is a website with the goal of helping people experiencing homelessness find help, and helping people interested in helping with homelessness get involved. Our website currently has two main branches. The "get involved" branch is targeted towards users wanting to help with homelessness. Features include short/simple education regarding homelessness, a quiz to help get an idea of how the user wants to involve themself, and an AI chatbot to assist with learning about involvement. The 
"find resources" branch is targeted towards users experiencing homelessness. Features include a map to help locate resources that can be helpful, search for nearby resources, and suggest other helpful resource centers/search hubs.
This project is currently in the development phase. 


---

## Table of Contents

- [ResourceConnect](#ResourceConnect)
  - [Overview](#overview)
  - [Tech Stack](#tech-stack)
  - [Why This Stack](#why-this-stack)
  - [Recommended Developer Tools](#recommended-developer-tools)
  - [Project Structure](#project-structure)
  - [Local Development Setup](#local-development-setup)
  - [Environment Variables](#environment-variables)
  - [Running the App Locally](#running-the-app-locally)
  - [Testing](#testing)
  - [Debugging with VSCode](#debugging-with-vscode)
  - [Deployment](#deployment)
  - [Git Workflow](#git-workflow)
  - [Coding Standards](#coding-standards)
  - [Contributors](#contributors)

---

## Tech Stack


### Best beginner-friendly stack

| Layer | Recommendation | Why |
| --- | --- | --- |
| Frontend templates | **Django Templates** | Keeps frontend/backend connected without needing a separate React app |
| CSS framework | **Tailwind CSS + DaisyUI** | Modern, clean components without Bootstrap’s default look |
| Interactivity | **Alpine.js** | Lightweight JavaScript for dropdowns, modals, filters, toggles |
| Backend | **Django** | Clear structure, admin panel, authentication, forms, models |
| API layer | **Django REST Framework** | Optional at first, useful if the team later adds React/mobile/API features |
| Database | **Supabase Postgres** | Hosted PostgreSQL database with dashboard, auth/storage options if needed |
| Environment variables | **python-dotenv / django-environ** | Keeps secrets out of GitHub |
| Local development | **Python virtual environment + npm** | Simple and common |
| Deployment | **Render / Railway / [Fly.io](http://Fly.io)** for Django, **Supabase** for DB | Beginner-friendly deployment options |
| Code quality | **Ruff + Black** | Auto-formatting and linting for Python |
| Testing | **Pytest + pytest-django** or Django’s built-in tests | Keeps backend reliable |
| Debugging | **VSCode Python debugger** | Easy breakpoints and step-through debugging |



### Backend

- **Django**
  - Main backend framework
  - Handles routing, views, forms, authentication, admin dashboard, and server-side rendering
  - Documentation: https://docs.djangoproject.com/

- **Django REST Framework**
  - Optional API layer
  - Useful if the project later adds a React frontend, mobile app, or external API integrations
  - Documentation: https://www.django-rest-framework.org/

### Database

- **Supabase Postgres**
  - Hosted PostgreSQL database
  - Used as the main production database
  - Supabase dashboard can help inspect tables and data during development
  - Documentation: https://supabase.com/docs
  - PostgreSQL documentation: https://www.postgresql.org/docs/

### Frontend

- **Django Templates**
  - Server-rendered HTML templates
  - Keeps frontend and backend development simple and connected
  - Documentation: https://docs.djangoproject.com/en/stable/topics/templates/

- **HTML**
  - Page structure and semantic markup
  - MDN docs: https://developer.mozilla.org/en-US/docs/Web/HTML

- **CSS**
  - Styling and layout
  - MDN docs: https://developer.mozilla.org/en-US/docs/Web/CSS

- **Tailwind CSS**
  - Utility-first CSS framework
  - Allows fast styling without writing large custom CSS files
  - Documentation: https://tailwindcss.com/docs

- **DaisyUI**
  - Component library built on top of Tailwind CSS
  - Provides modern UI components without using Bootstrap
  - Documentation: https://daisyui.com/

- **Alpine.js**
  - Lightweight JavaScript framework for simple interactivity
  - Useful for dropdowns, modals, tabs, filters, and toggles
  - Documentation: https://alpinejs.dev/

### Optional Later Additions

The team should avoid adding these until the MVP is stable:

- **React**
  - Good for highly interactive frontend applications
  - Not required for the first version if using Django templates
  - Documentation: https://react.dev/

- **Next.js**
  - React framework for full-stack frontend applications
  - Not recommended for the first version because Django already handles backend routing and rendering
  - Documentation: https://nextjs.org/docs

- **HTMX**
  - Alternative lightweight option for dynamic server-rendered pages
  - Can be useful if the team wants interactivity without React
  - Documentation: https://htmx.org/docs/

---

## Why This Stack

This project is designed for a beginner-friendly development team while still using modern tools.

The recommended stack is:


**Django + Django Templates + Tailwind CSS + DaisyUI + Alpine.js + Supabase Postgres**



This keeps the project simple because:

- Django handles the backend, routing, views, forms, authentication, and templates.
- Supabase provides a hosted PostgreSQL database.
- Tailwind CSS and DaisyUI provide modern styling without Bootstrap.
- Alpine.js adds lightweight interactivity without needing React.
- The frontend and backend stay organized in one project.
- The team can add Django REST Framework later if an API becomes necessary.

---

## Recommended Developer Tools

Each developer should install:

- Python 3.11 or newer
- Node.js LTS
- Git
- VSCode
- PostgreSQL client tool, optional
  - TablePlus
  - DBeaver
  - pgAdmin
- Supabase account
- GitHub account

Recommended VSCode extensions:

- Python
- Django
- Pylance
- Ruff
- Black Formatter
- Tailwind CSS IntelliSense
- HTML CSS Support
- GitLens
- dotenv

---

## Project Structure

Recommended file structure:

```

project-root/

│

├── [README.md](http://README.md)

├── .gitignore

├── .env.example

├── requirements.txt

├── package.json

├── tailwind.config.js

├── postcss.config.js

│

├── [manage.py](http://manage.py)

│

├── config/

│   ├── **init**.py

│   ├── [settings.py](http://settings.py)

│   ├── [urls.py](http://urls.py)

│   ├── [asgi.py](http://asgi.py)

│   └── [wsgi.py](http://wsgi.py)

│

├── apps/

│   ├── core/

│   │   ├── **init**.py

│   │   ├── [views.py](http://views.py)

│   │   ├── [urls.py](http://urls.py)

│   │   ├── [models.py](http://models.py)

│   │   ├── [forms.py](http://forms.py)

│   │   ├── [admin.py](http://admin.py)

│   │   └── [tests.py](http://tests.py)

│   │

│   ├── resources/

│   │   ├── **init**.py

│   │   ├── [views.py](http://views.py)

│   │   ├── [urls.py](http://urls.py)

│   │   ├── [models.py](http://models.py)

│   │   ├── [forms.py](http://forms.py)

│   │   ├── [admin.py](http://admin.py)

│   │   └── [tests.py](http://tests.py)

│   │

│   ├── opportunities/

│   │   ├── **init**.py

│   │   ├── [views.py](http://views.py)

│   │   ├── [urls.py](http://urls.py)

│   │   ├── [models.py](http://models.py)

│   │   ├── [forms.py](http://forms.py)

│   │   ├── [admin.py](http://admin.py)

│   │   └── [tests.py](http://tests.py)

│   │

│   └── users/

│       ├── **init**.py

│       ├── [views.py](http://views.py)

│       ├── [urls.py](http://urls.py)

│       ├── [models.py](http://models.py)

│       ├── [forms.py](http://forms.py)

│       ├── [admin.py](http://admin.py)

│       └── [tests.py](http://tests.py)

│

├── templates/

│   ├── base.html

│   ├── home.html

│   ├── resources/

│   │   ├── list.html

│   │   └── detail.html

│   ├── opportunities/

│   │   ├── list.html

│   │   └── detail.html

│   └── users/

│       ├── login.html

│       └── register.html

│

├── static/

│   ├── src/

│   │   └── input.css

│   ├── css/

│   │   └── output.css

│   ├── js/

│   │   └── main.js

│   └── images/

│

├── media/

│

└── docs/

├── [planning.md](http://planning.md)

├── [user-research.md](http://user-research.md)

├── [data-model.md](http://data-model.md)

└── [deployment-notes.md](http://deployment-notes.md)

```

### Folder Purpose

| Folder | Purpose |
|---|---|
| `config/` | Main Django project settings and URLs |
| `apps/core/` | Homepage, static pages, shared views |
| `apps/resources/` | Support resource listings and details |
| `apps/opportunities/` | Volunteer, paid, donation, and community involvement opportunities |
| `apps/users/` | User accounts, login, registration, saved items |
| `templates/` | HTML templates |
| `static/` | CSS, JavaScript, images |
| `docs/` | Planning notes and technical documentation |
| `media/` | Uploaded files if needed |

---

## Local Development Setup

### 1. Clone the Repository

```

git clone <repository-url>

cd <repository-name>

```

### 2. Create a Python Virtual Environment

macOS/Linux:

```

python3 -m venv venv

source venv/bin/activate

```

Windows PowerShell:

```

python -m venv venv

[venvScriptsActivate.ps](http://venvScriptsActivate.ps)1

```

### 3. Install Python Dependencies

```

pip install -r requirements.txt

```

If `requirements.txt` has not been created yet, the starter dependencies may include:

```

pip install django djangorestframework psycopg2-binary python-dotenv django-environ gunicorn whitenoise

pip freeze > requirements.txt

```

Optional development tools:

```

pip install black ruff pytest pytest-django

pip freeze > requirements.txt

```

### 4. Install Frontend Dependencies

```

npm install

```

If `package.json` has not been created yet, initialize it:

```

npm init -y

npm install -D tailwindcss postcss autoprefixer

npm install daisyui alpinejs

npx tailwindcss init -p

```

---

## Environment Variables

Create a `.env` file in the project root.

Do not commit `.env` to GitHub.

Use `.env.example` to show required variables without exposing secrets.

Example `.env.example`:

```

# Django

SECRET_KEY=replace-this-with-a-secret-key

DEBUG=True

ALLOWED_HOSTS=[localhost](http://localhost),127.0.0.1

# Supabase Postgres Database

DATABASE_NAME=postgres

DATABASE_USER=postgres

DATABASE_PASSWORD=replace-this

DATABASE_HOST=[replace-this.supabase.co](http://replace-this.supabase.co)

DATABASE_PORT=5432

# Optional Supabase API values

SUPABASE_URL=https://replace-this.supabase.co

SUPABASE_ANON_KEY=replace-this

```

Free map stack for the resources map page, could replace with google mapsin the future:

1. The map UI uses Leaflet loaded from a CDN.
2. Base map tiles come from OpenStreetMap.
3. Resource markers come from the existing 211 Colorado integration.
4. No Google API key or billing setup is required.

Recommended `.gitignore` entries:

```

.env

venv/

**pycache**/

*.pyc

db.sqlite3

media/

staticfiles/

node_modules/

.DS_Store

.vscode/

```

---

## Running the App Locally

### 1. Activate Virtual Environment

macOS/Linux:

```

source venv/bin/activate

```

Windows PowerShell:

```

[venvScriptsActivate.ps](http://venvScriptsActivate.ps)1

```

### 2. Run Database Migrations

```

python [manage.py](http://manage.py) makemigrations

python [manage.py](http://manage.py) migrate

```

### 3. Create a Superuser

```

python [manage.py](http://manage.py) createsuperuser

```

### 4. Run the Django Development Server

```

python [manage.py](http://manage.py) runserver

```

Open the app at:

```

http://127.0.0.1:8000/

```

Open the Django admin at:

```

http://127.0.0.1:8000/admin/

```

### 5. Run Tailwind CSS Watcher

In a separate terminal:

```

npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch

```

---

## Testing

### Run Django Tests

```

python [manage.py](http://manage.py) test

```

### Optional: Run Pytest

If using `pytest` and `pytest-django`:

```

pytest

```

Recommended testing areas:

- Models
- Views
- Forms
- Resource filters
- Opportunity filters
- User authentication
- Saved items
- Submit-resource form validation

---

## Debugging with VSCode

### 1. Install Recommended Extensions

Install these VSCode extensions:

- Python
- Pylance
- Django
- Ruff
- Black Formatter
- Tailwind CSS IntelliSense
- dotenv

### 2. Select the Python Interpreter

In VSCode:

1. Open the command palette:
   - macOS: `Cmd + Shift + P`
   - Windows/Linux: `Ctrl + Shift + P`
2. Search for `Python: Select Interpreter`
3. Select the interpreter inside the project virtual environment:
   - macOS/Linux: `./venv/bin/python`
   - Windows: `.\venv\Scripts\python.exe`

### 3. Add VSCode Debug Configuration

Create this file:

```

.vscode/launch.json

```

Add:

```

{

"version": "0.2.0",

"configurations": [

{

"name": "Django: Run Server",

"type": "python",

"request": "launch",

"program": "${workspaceFolder}/[manage.py](http://manage.py)",

"args": ["runserver"],

"django": true,

"justMyCode": true

},

{

"name": "Django: Run Tests",

"type": "python",

"request": "launch",

"program": "${workspaceFolder}/[manage.py](http://manage.py)",

"args": ["test"],

"django": true,

"justMyCode": true

}

]

}

```

### 4. Use Breakpoints

To debug:

1. Open a Python file, such as `views.py`.
2. Click to the left of a line number to add a breakpoint.
3. Go to the Run and Debug panel in VSCode.
4. Select `Django: Run Server`.
5. Click the green play button.
6. Visit the page in the browser that triggers the code.

VSCode will pause at the breakpoint and allow you to inspect variables.

### 5. Debugging Django Templates

For template issues:

- Check the browser page source.
- Check the Django terminal output.
- Confirm the template path is correct.
- Confirm the view passes the correct context variables.
- Use simple temporary output in templates:

```

{{ variable_name }}

```

### 6. Debugging Tailwind CSS

If styles are not appearing:

- Confirm the Tailwind watcher is running.
- Confirm `output.css` is linked in `base.html`.
- Confirm template paths are included in `tailwind.config.js`.
- Restart the watcher after changing Tailwind config.

Example `tailwind.config.js` content paths:

```

module.exports = {

content: [

"./templates//*.html",

"./apps//*.html",

"./apps//*.py"

],

theme: {

extend: {},

},

plugins: [require("daisyui")],

}

```

---

## Deployment

Recommended beginner-friendly deployment:

- **Django app:** Render, Railway, or Fly.io
- **Database:** Supabase Postgres
- **Static files:** WhiteNoise for simple deployments
- **Environment variables:** Configured in the deployment platform dashboard

### Production Checklist

Before deploying:

- Set `DEBUG=False`
- Set a secure `SECRET_KEY`
- Configure `ALLOWED_HOSTS`
- Configure the Supabase database URL/settings
- Run migrations
- Collect static files
- Confirm static files load correctly
- Create a production admin user
- Test login, forms, and main pages

### Collect Static Files

```

python [manage.py](http://manage.py) collectstatic

```

### Example Production Commands

Build command:

```

pip install -r requirements.txt && python [manage.py](http://manage.py) collectstatic --noinput && python [manage.py](http://manage.py) migrate

```

Start command:

```

gunicorn config.wsgi:application

```

---

## Git Workflow

Recommended branch strategy:

```

main

dev

feature/<feature-name>

bugfix/<bug-name>

```

### Branch Examples

```

git checkout dev

git pull origin dev

git checkout -b feature/resource-cards

```

### Commit Message Examples

```

Add resource card component

Create opportunity list page

Fix navbar mobile layout

Update README setup steps

```

### Pull Request Checklist

Before opening a pull request:

- Code runs locally
- Tests pass
- No secrets are committed
- New files are organized in the correct folders
- README is updated if setup steps changed
- Screenshots are included for UI changes

---

## Coding Standards

### Python

Use clear and readable Python code.

Recommended tools:

```

black .

ruff check .

```

### HTML

Use semantic HTML where possible:

```

<header>

<main>

<section>

<article>

<footer>

```

### CSS

Prefer Tailwind utility classes for layout and styling.

Use custom CSS only when:

- Tailwind utilities are not enough
- A reusable style is needed
- The style improves readability

### JavaScript

Use Alpine.js for simple interactivity.

Avoid adding large JavaScript libraries unless the team agrees they are necessary.

---

## Accessibility

This project should be designed with accessibility in mind.

Important practices:

- Use readable color contrast
- Use semantic HTML
- Add alt text to images
- Make buttons and links keyboard-accessible
- Use clear labels on forms
- Avoid tiny text
- Make the layout mobile-friendly
- Do not rely only on color to communicate meaning

---

## Data and Safety Guidelines

Because this project may involve homelessness, housing instability, and social services, data must be handled carefully.

Guidelines:

- Do not collect unnecessary personal information.
- Do not require users to create an account to find support resources.
- Show when a resource was last verified.
- Avoid publishing unverified emergency information.
- Use respectful, person-centered language.
- Do not present the app as a replacement for emergency services or official Coordinated Entry systems.
- Include clear source links for resource information.

Recommended language:

- Use `people experiencing homelessness`
- Use `people experiencing housing instability`
- Use `support resources`
- Use `social services`
- Use `community engagement`
- Use `volunteer opportunities`
- Use `paid nonprofit roles`
- Avoid terms like `the homeless`, `vagrants`, or `welfare`

---

## Contributors

This project is part of the **Computing 4 Good 2026** program at the **Colorado School of Mines**.

### Development Team



| Name | Role | GitHub | Email |
|---|---|---|---|
| Vyomesh | project developer | Vyo-Par | vyomeshparasa2@gmail.com |
| Ishaan | project developer | IshaanDeshpande | ishaans.desh@gmail.com |
| Jackson | project developer | JacksonP882 | pope.jackso09@gmail.com |
| Vihaan | project developer | VihaanRav | ravishankarvihaan@outlook.com |

### Mentor / Advisor

| Name | Role | GitHub | Email |
|---|---|---|---|
| Mimi | mentor/template provider | mimi-rai | 22sumnima.rai@gmail.com |

---

## License


MIT License for open-source projects

---
.
