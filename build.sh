#!/bin/bash

# 1. Install Node dependencies and build Tailwind CSS
echo "Installing Node dependencies..."
npm install

echo "Building Tailwind CSS..."
npm run build:css

echo "Building Next.js..."
npm run build

# 2. Create and activate a Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 3. Install Python dependencies inside the venv
echo "Installing Python requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Run Django collectstatic (skip database checks)
echo "Collecting static files..."
python manage.py collectstatic --noinput --skip-checks