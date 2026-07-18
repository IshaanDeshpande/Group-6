# SETUP GUIDE

Development setup guide for the Computing 4 Good 2026 project.

This document explains how to install the tools needed for local development, set up the project environment, follow the Git/GitHub workflow, and keep the Notion sprint board updated.

## Table of Contents

- [1. Required Tools](#1-required-tools)
- [2. macOS Setup](#2-macos-setup)
- [3. Windows Setup](#3-windows-setup)
- [4. Project Setup After Cloning](#4-project-setup-after-cloning)
- [5. Environment Variables](#5-environment-variables)
- [6. Running the Project Locally](#6-running-the-project-locally)
- [7. Version Control Best Practices](#7-version-control-best-practices)
- [8. Starting Your Personal Development Branch](#8-starting-your-personal-development-branch)
- [9. Pull Requests and Code Review](#9-pull-requests-and-code-review)
- [10. Notion Sprint Board Workflow](#10-notion-sprint-board-workflow)
- [11. Common Debugging Commands](#11-common-debugging-commands)
- [12. Troubleshooting](#12-troubleshooting)

---

## 1. Required Tools

Each developer should install the following tools before starting development.

### Git

Git is used for version control. It tracks code changes and allows team members to work on separate branches before merging work into the main project.

Official installation guide: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

Check if Git is installed:

```

git --version

```

---

### GitHub

GitHub hosts the remote repository. Team members will use GitHub to push branches, open pull requests, review code, and merge approved changes.

GitHub Docs: https://docs.github.com/

---

### VSCode

VSCode is the recommended code editor for this project. It supports Python, Django, Git, debugging, formatting, and extensions for frontend development.

Download VSCode: https://code.visualstudio.com/

Recommended VSCode extensions:

- Python
- Pylance
- Django
- Ruff
- Black Formatter
- Tailwind CSS IntelliSense
- dotenv
- GitLens

---

### Python

Python is required because the backend uses Django.

Download Python: https://www.python.org/downloads/

Check if Python is installed:

```

python --version

```

or:

```

python3 --version

```

Recommended version:

```

Python 3.11 or 3.12 recommended

```

If you choose Python 3.14 on Windows, make sure you install from the current `requirements.txt`. Older Pillow pins fail there because they do not provide usable prebuilt wheels.

---

### Django

Django is the backend web framework. It handles routing, views, templates, forms, database models, authentication, and the admin panel.

Django documentation: https://docs.djangoproject.com/

Django will be installed inside the project’s Python virtual environment.

---

### Supabase

Supabase provides the hosted PostgreSQL database for the project.

Supabase Docs: https://supabase.com/docs

Supabase is used for:

- hosted PostgreSQL database
- database dashboard
- project credentials
- possible future storage or authentication features

---

### PostgreSQL Driver

The Django app needs a PostgreSQL driver to connect to Supabase Postgres.

Recommended package:

```

psycopg2-binary

```

Package page: https://pypi.org/project/psycopg2-binary/

---

### Node.js and npm

Node.js and npm are used for frontend tooling, especially Tailwind CSS and DaisyUI.

Download Node.js: https://nodejs.org/

Check if Node.js and npm are installed:

```

node --version

npm --version

```

Recommended version:

```

Node.js LTS

```

---

### Tailwind CSS

Tailwind CSS is the main styling framework. It allows developers to write modern layouts quickly using utility classes.

Tailwind CSS Docs: https://tailwindcss.com/docs

---

### DaisyUI

DaisyUI is a component library built on Tailwind CSS. It provides buttons, cards, navbars, forms, modals, alerts, and other components without using Bootstrap.

DaisyUI Docs: https://daisyui.com/

---

### Alpine.js

Alpine.js is a lightweight frontend JavaScript framework. It is useful for simple interactivity such as dropdowns, modals, filters, toggles, and tabs.

Alpine.js Docs: https://alpinejs.dev/

---

## 2. macOS Setup

This section is for Mac developers.

### 2.1 Install Homebrew

Homebrew is a package manager for macOS. It makes it easier to install developer tools from the terminal.

Homebrew installation guide: https://brew.sh/

Install Homebrew:

```

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

```

Check Homebrew:

```

brew --version

```

---

### 2.2 Install Git

Git is used to clone the repository, create branches, commit changes, and push code to GitHub.

```

brew install git

git --version

```

Configure Git with your name and email:

```

git config --global user.name "Your Name"

git config --global user.email "you@example.com"

```

Check your Git config:

```

git config --global --list

```

---

### 2.3 Install Python

Python is needed to run Django.

```

brew install python

python3 --version

pip3 --version

```

---

### 2.4 Install Node.js

Node.js and npm are needed for Tailwind CSS, DaisyUI, and other frontend packages.

```

brew install node

node --version

npm --version

```

---

### 2.5 Install VSCode

Download VSCode from:

```

https://code.visualstudio.com/

```

Optional: install the `code` command so VSCode can open folders from the terminal.

In VSCode:

1. Open the Command Palette:
   - `Cmd + Shift + P`
2. Search:
   - `Shell Command: Install 'code' command in PATH`
3. Select it.

Then test:

```

code --version

```

---

### 2.6 Install Optional PostgreSQL Tools

These are optional but helpful for viewing and debugging database data.

Options:

- TablePlus: https://tableplus.com/
- DBeaver: https://dbeaver.io/
- pgAdmin: https://www.pgadmin.org/

---

## 3. Windows Setup

This section is for Windows developers.

### 3.1 Install Git for Windows

Git is used for version control and GitHub collaboration.

Download Git for Windows:

```

https://git-scm.com/download/win

```

After installing, check Git:

```

git --version

```

Configure Git:

```

git config --global [user.name](http://user.name) "Your Name"

git config --global [user.email](http://user.email) "[you@example.com](mailto:you@example.com)"

```

Check your Git config:

```

git config --global --list

```

---

### 3.2 Install Python

Python is needed to run Django.

Download Python:

```

https://www.python.org/downloads/windows/

```

During installation, check:

```

Add python.exe to PATH

```

Then verify:

```

python --version

pip --version

```

---

### 3.3 Install Node.js

Node.js and npm are needed for Tailwind CSS and frontend tooling.

Download Node.js LTS:

```

https://nodejs.org/

```

Then verify:

```

node --version

npm --version

```

---

### 3.4 Install VSCode

Download VSCode:

```

https://code.visualstudio.com/

```

Recommended extensions:

```

Python

Pylance

Django

Ruff

Black Formatter

Tailwind CSS IntelliSense

dotenv

GitLens

```

---

### 3.5 Install Optional PostgreSQL Tools

These are optional but helpful for viewing database data.

Options:

- TablePlus: https://tableplus.com/
- DBeaver: https://dbeaver.io/
- pgAdmin: https://www.pgadmin.org/

---

### 3.6 PowerShell Execution Policy

If Windows blocks virtual environment activation, run PowerShell as Administrator and use:

```

Set-ExecutionPolicy RemoteSigned

```

Then close and reopen PowerShell.

---

## 4. Project Setup After Cloning

Once the repository exists, clone it to your local machine.

```

git clone <repository-url>

cd <repository-name>

code .

```

---

### 4.1 Create a Python Virtual Environment

A virtual environment keeps Python packages for this project separate from other projects on your computer.

#### macOS

```

python3 -m venv venv

source venv/bin/activate

```

#### Windows PowerShell

```

python -m venv venv

[venvScriptsActivate.ps](http://venvScriptsActivate.ps)1

```

After activating, your terminal should show something like:

```

(venv)

```

---

### 4.2 Upgrade pip

`pip` is Python’s package installer.

#### macOS

```

python3 -m pip install --upgrade pip

```

#### Windows

```

python -m pip install --upgrade pip

```

---

### 4.3 Install Python Packages

Install the core backend packages:

Option 1: install everything from the `requirements.txt` file

```

pip install -r requirements.txt

```

Option 2: install through command line individually

```

pip install django djangorestframework psycopg2-binary python-dotenv django-environ gunicorn whitenoise

```

What these packages are for:

| Package | Purpose |
|---|---|
| `django` | Main backend framework |
| `djangorestframework` | Optional API layer for future frontend/API work |
| `psycopg2-binary` | Allows Django to connect to Supabase Postgres |
| `python-dotenv` | Loads environment variables from `.env` files |
| `django-environ` | Helps configure Django settings using environment variables |
| `gunicorn` | Production server used during deployment |
| `whitenoise` | Helps serve static files in production |

Install development tools:

```

pip install black ruff pytest pytest-django

```

What these are for:

| Package | Purpose |
|---|---|
| `black` | Formats Python code automatically |
| `ruff` | Checks Python code for linting issues |
| `pytest` | Testing framework |
| `pytest-django` | Django support for pytest |

Save installed packages:

```

pip freeze > requirements.txt

```

---

### 4.4 Install Frontend Packages

Initialize npm if the project does not already have `package.json`:

```

npm init -y

```

Install Tailwind CSS tools:

```

npm install -D tailwindcss postcss autoprefixer

```

Install DaisyUI and Alpine.js:

```

npm install daisyui alpinejs

```

Create Tailwind config files if they do not exist yet:

```

npm install tailwindcss

```

What these packages are for:

| Package | Purpose |
|---|---|
| `tailwindcss` | Main utility-first CSS framework |
| `postcss` | Processes CSS during builds |
| `autoprefixer` | Adds browser compatibility prefixes to CSS |
| `daisyui` | Tailwind component library |
| `alpinejs` | Lightweight frontend interactivity |

---

## 5. Environment Variables

Environment variables keep secrets and local settings out of the codebase.

Create a `.env` file in the project root:

```

touch .env

```

On Windows PowerShell:

```

New-Item .env

```

Example `.env`:

```

SECRET_KEY=replace-this-with-a-secret-key

DEBUG=True

ALLOWED_HOSTS=[localhost](http://localhost),127.0.0.1

DATABASE_NAME=postgres

DATABASE_USER=postgres

DATABASE_PASSWORD=replace-this

DATABASE_HOST=[replace-this.supabase.co](http://replace-this.supabase.co)

DATABASE_PORT=5432

SUPABASE_URL=https://replace-this.supabase.co

SUPABASE_ANON_KEY=replace-this

```

Find Resources map stack:

1. The map UI uses Leaflet loaded from a CDN.
2. Base map tiles come from OpenStreetMap.
3. Resource markers come from the existing 211 Colorado integration.
4. No Google API key or billing setup is required.

Important:

```

Never commit .env to GitHub.

```

Make sure `.gitignore` includes:

```

.env

venv/

**pycache**/

*.pyc

db.sqlite3

node_modules/

staticfiles/

media/

.DS_Store

.vscode/

```

The repo should include a safe `.env.example` file that lists required variables without real secret values.

---

## 6. Running the Project Locally

### 6.1 Activate the Virtual Environment

#### macOS

```

source venv/bin/activate

```

#### Windows PowerShell

```

venvScriptsActivate.ps

```

---

### 6.2 Run Database Migrations

Migrations create or update database tables.

```

python manage.py makemigrations

python manage.py migrate

```

---

### 6.3 Create a Django Admin User

This creates a local admin account for the Django admin dashboard.

```

python manage.py createsuperuser

```

---

### 6.4 Start the Django Server

```

python manage.py runserver

```

Open:

```

http://127.0.0.1:8000/

```

Django admin:

```

http://127.0.0.1:8000/admin/

```

---

### 6.5 Start the Tailwind Watcher

Open a second terminal and run:

```

npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch

```

This watches the frontend files and rebuilds the CSS when changes are made.

---

## 7. Version Control Best Practices

This workflow is based on the C4G Development Cycle Instructions.

Main source: [C4G Development Cycle Instructions](https://www.notion.so/3876e3a88fa680a2b164cea4a5f0ce64)

### Daily Git Loop

Before starting a task:

```

git switch main

git pull origin main

```

Create a new branch:

```

git switch -c task-##-short-description

```

Example:

```

git switch -c task-01-create-landing-page

```

While coding, check your changes often:

```

git status

git diff

```

Stage changes:

```

git add .

```

Or stage a specific file:

```

git add path/to/file

```

Commit changes:

```

git commit -m "Add landing page layout"

```

Push your branch:

```

git push origin task-01-create-landing-page

```

If this is the first push and Git suggests using `--set-upstream`, use:

```

git push -u origin task-01-create-landing-page

```

---

### Important Git Rules

Do:

- Pull from `main` before starting new work.
- Create one branch per task.
- Use clear branch names.
- Commit small checkpoints.
- Write meaningful commit messages.
- Push your branch regularly.
- Open a pull request when the work is ready.
- Ask for review before merging.

Do not:

- Commit directly to `main`.
- Commit `.env` files.
- Commit passwords, API keys, tokens, or database credentials.
- Mix unrelated tasks in one branch.
- Merge your own PR without review unless the team agrees.

---

### Helpful Git Commands

```

git status

git diff

git log --oneline

git branch

git switch main

git pull origin main

git switch -c task-##-description

git add .

git commit -m "Message"

git push origin branch-name

```

Undo local changes to a file:

```

git restore path/to/file

```

Delete a local branch after it is merged:

```

git branch -d branch-name

```

---

## 8. Starting Your Personal Development Branch

Each developer should work on a personal task branch instead of coding directly on `main`.

### Step 1: Pick a Task

Go to the Notion sprint board and choose a task.

Update the task:

- Assign yourself as the owner
- Move it to the correct status, such as `In Progress`
- Confirm the task description is clear
- Add any notes or questions before starting

### Step 2: Update Local Main

```

git switch main

git pull origin main

```

### Step 3: Create Your Branch

Use this naming pattern:

```

task-##-short-description

```

Examples:

```

git switch -c task-01-create-homepage

git switch -c task-02-resource-card-component

git switch -c task-03-add-navbar

```

### Step 4: Start Development

Open the project in VSCode:

```

code .

```

Run the app locally and test as you build.

### Step 5: Commit Work in Checkpoints

```

git status

git add .

git commit -m "Create homepage layout"

```

### Step 6: Push Your Branch

```

git push -u origin task-01-create-homepage

```

### Step 7: Keep Notion Updated

As you work, keep the sprint board updated:

- Status: `In Progress`
- Owner: your name
- Branch: your branch name, if there is a branch field
- Notes: blockers, questions, or implementation details
- PR link: add once the pull request is created

---

## 9. Pull Requests and Code Review

### 9.1 Create a Pull Request

After pushing your branch:

1. Go to GitHub.
2. Open the repository.
3. Click `Compare & pull request`, or go to:
   - `Pull requests`
   - `New pull request`
4. Set:
   - base: `main`
   - compare: your branch
5. Create the pull request.

### 9.2 Pull Request Title

The PR title should include the task number.

Example:

```

Task 01: Create homepage layout

```

### 9.3 Pull Request Description Template

Use this format:

```

## Summary

- Added ...
- Updated ...
- Fixed ...

## Testing

- [ ]  Ran the app locally
- [ ]  Checked page in browser
- [ ]  Ran tests, if applicable

## Screenshots

TODO: Add screenshots for frontend changes.

## Notes

TODO: Add questions, blockers, or follow-up items.

```

### 9.4 Request Review

After creating the PR:

- Add a reviewer on GitHub.
- Message the reviewer in the team communication channel.
- Add the reviewer to the related Notion sprint board task.
- Add the PR link to the Notion task.

### 9.5 Reviewing Code

Reviewers should:

- Open the PR.
- Go to the `Files changed` tab.
- Read through the changes.
- Leave at least one comment.
- Check that the code matches the task.
- Check that no secrets are committed.
- Confirm the app runs if needed.
- Approve or request changes.

### 9.6 Merging

Only merge when:

- The PR has been reviewed.
- Required changes are complete.
- The code runs locally.
- The branch is up to date with `main`.
- The related Notion task is ready to move forward.

After merging:

```

git switch main

git pull origin main

git branch -d branch-name

```

Then update the Notion task.

---

## 10. Notion Sprint Board Workflow

The sprint board is the source of truth for task tracking.

For every coding task:

### Before Coding

- Assign yourself to the task.
- Move the task to `In Progress`.
- Make sure the task has a clear description.
- Create a branch for the task.
- Add your branch name to the task if there is a field for it.

### During Development

- Add notes for blockers or decisions.
- Keep the status accurate.
- Ask questions early if requirements are unclear.

### When Opening a PR

- Move the task to `In Review`.
- Add the GitHub PR link.
- Add the reviewer.
- Message the reviewer.

### After Merge

- Move the task to `Done`.
- Confirm the branch was merged into `main`.
- Delete the local branch.
- Pull the latest `main`.

---

## 11. Common Debugging Commands

### Django

Check for Django issues:

```

python [manage.py](http://manage.py) check

```

Run migrations:

```

python [manage.py](http://manage.py) makemigrations

python [manage.py](http://manage.py) migrate

```

Start server:

```

python [manage.py](http://manage.py) runserver

```

Open Django shell:

```

python [manage.py](http://manage.py) shell

```

Create admin user:

```

python [manage.py](http://manage.py) createsuperuser

```

---

### Python Formatting and Linting

Format Python files:

```

black .

```

Check Python files:

```

ruff check .

```

---

### Tests

Run Django tests:

```

python [manage.py](http://manage.py) test

```

Run pytest if configured:

```

pytest

```

---

### Tailwind

Start Tailwind watcher:

```

npx tailwindcss -i ./static/src/input.css -o ./static/css/output.css --watch

```

If styles are missing:

- Confirm the watcher is running.
- Confirm `output.css` is linked in `base.html`.
- Confirm `tailwind.config.js` includes the correct template paths.
- Restart the watcher.

---

### Git

Check current branch and changes:

```

git status

git branch

```

See recent commits:

```

git log --oneline

```

See unstaged changes:

```

git diff

```

Pull latest main:

```

git switch main

git pull origin main

```

---

## 12. Troubleshooting

### Virtual Environment Will Not Activate on Windows

Run PowerShell as Administrator:

```

Set-ExecutionPolicy RemoteSigned

```

Then reopen PowerShell and try:

```

venvScriptsActivate.ps

```

---

### `python` Command Does Not Work

Try:

```

python3 --version

```

If that works, use `python3` instead of `python`.

On Windows, reinstall Python and make sure `Add python.exe to PATH` is selected.

---

### `pip` Command Does Not Work

Try:

```

python -m pip --version

```

or:

```

python3 -m pip --version

```

---

### `npm` Command Does Not Work

Make sure Node.js LTS is installed:

```

https://nodejs.org/

```

Then restart the terminal and run:

```

node --version

npm --version

```

---

### Django Cannot Connect to Supabase

Check:

- `.env` exists
- database credentials are correct
- Supabase project is active
- database host is correct
- password does not contain accidental spaces
- `psycopg2-binary` is installed
- Django settings are reading environment variables correctly

---

### Tailwind Styles Are Not Showing

Check:

- Tailwind watcher is running
- `static/css/output.css` exists
- `output.css` is linked in `base.html`
- HTML files are included in `tailwind.config.js`
- The browser cache is refreshed

---

### Merge Conflicts

If Git reports a merge conflict:

1. Open the conflicting files in VSCode.
2. Look for conflict markers:

```

<<<<<<< HEAD

current branch code

=======

incoming code

> >>>>>> main
> 

```

3. Choose the correct code.
4. Remove the conflict markers.
5. Save the file.
6. Stage and commit:

```

git add path/to/conflicted-file

git commit

```

If you need to cancel the merge:

```

git merge --abort

```

---

## Final Notes

Keep the project simple, organized, and easy for new developers to understand.

Good habits:

- Pull before starting work.
- Work on one task per branch.
- Commit small checkpoints.
- Keep the sprint board updated.
- Ask for review before merging.
- Never commit secrets.
- Test locally before opening a PR.

