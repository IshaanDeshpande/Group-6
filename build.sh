#!/bin/bash

# 1. Install Node dependencies and build Tailwind CSS
echo "Building Tailwind CSS..."
npm install
npm run build:css

# 2. Create and activate a Python virtual environment
echo "Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# 3. Install Python dependencies inside the venv
echo "Installing Python requirements..."
pip install --upgrade pip
pip install -r requirements.txt

# 4. Run Django collectstatic
echo "Collecting static files..."
python3 manage.py collectstatic --noinput