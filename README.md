# Django Todo App

A simple and elegant todo application built with Django and Python.

## Features

- ✅ Add new tasks with title and description
- ✅ Mark tasks as complete/incomplete
- ✅ Edit existing tasks
- ✅ Delete tasks
- ✅ Beautiful, responsive UI
- ✅ SQLite database (no setup required)

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Setup Instructions

### 1. Create a Virtual Environment

```bash
# Navigate to the project directory
cd todo_project

# Create virtual environment
python -m venv todo_env

# Activate the virtual environment
# On Windows:
todo_env\Scripts\activate

# On macOS/Linux:
source todo_env/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create a Superuser (Optional - for admin panel)

```bash
python manage.py createsuperuser
```

Follow the prompts to create your admin account.

### 5. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at: `http://127.0.0.1:8000/`

## Usage

### Main Todo List
- Visit `http://127.0.0.1:8000/` to see your todo list
- Click "Add New Task" to create a task
- Click "Mark Complete" to toggle task completion
- Click "Edit" to modify a task
- Click "Delete" to remove a task

### Admin Panel
- Visit `http://127.0.0.1:8000/admin/`
- Log in with your superuser credentials
- Manage todos from the admin interface

## Project Structure

```
todo_project/
│
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
│
├── todo_project/            # Project settings
│   ├── __init__.py
│   ├── settings.py          # Project configuration
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
│
└── todo_app/                # Todo application
    ├── __init__.py
    ├── admin.py             # Admin configuration
    ├── apps.py              # App configuration
    ├── models.py            # Database models
    ├── views.py             # View functions
    ├── urls.py              # App URL routing
    ├── tests.py             # Tests
    ├── migrations/          # Database migrations
    └── templates/           # HTML templates
        └── todo_app/
            ├── base.html
            ├── todo_list.html
            ├── add_todo.html
            └── edit_todo.html
```

## Testing

Run tests with:

```bash
python manage.py test
```

## Common Commands

```bash
# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run tests
python manage.py test

# Open Django shell
python manage.py shell
```

## Troubleshooting

### Port Already in Use
If port 8000 is already in use, run the server on a different port:
```bash
python manage.py runserver 8080
```

### Database Issues
If you encounter database issues, delete `db.sqlite3` and run migrations again:
```bash
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
```

### Virtual Environment Not Activating
Make sure you're in the correct directory and using the right command for your operating system.

## Next Steps

Some ideas to extend this app:
- Add user authentication (multi-user support)
- Add categories/tags for tasks
- Add due dates and reminders
- Add priority levels
- Add search functionality
- Add task filtering (all/active/completed)
- Deploy to a production server

## License

This project is open source and available for educational purposes.
