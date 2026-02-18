# Quick Start Guide - Django Todo App

## Get Started in 5 Minutes! 🚀

### Step 1: Navigate to the project
```bash
cd todo_project
```

### Step 2: Create and activate virtual environment
**Windows:**
```bash
python -m venv todo_env
todo_env\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv todo_env
source todo_env/bin/activate
```

### Step 3: Install Django
```bash
pip install -r requirements.txt
```

### Step 4: Setup database
```bash
python manage.py migrate
```

### Step 5: Run the app!
```bash
python manage.py runserver
```

### Step 6: Open in browser
Visit: **http://127.0.0.1:8000/**

That's it! Start adding your todos! 📝

---

## Optional: Create Admin Account

```bash
python manage.py createsuperuser
```

Then visit **http://127.0.0.1:8000/admin/** to manage todos from admin panel.

---

## Need Help?
Check the full README.md for detailed instructions and troubleshooting!
