# 🚀 UPGRADE INSTRUCTIONS - Adding New Features

## ⚠️ IMPORTANT: Follow these steps to upgrade your existing todo app

### Step 1: Stop the server
Press `Ctrl+C` in your terminal to stop the Django development server.

### Step 2: Replace all files
Copy all the new files from the updated project folder, replacing the old ones:
- Copy all files from `todo_app/` folder
- Copy all files from `todo_project/` folder

### Step 3: Create and Apply Migrations
```bash
# Create new migrations for the updated models
python manage.py makemigrations

# Apply the migrations to update the database
python manage.py migrate
```

### Step 4: Create some default categories (optional)
```bash
python manage.py shell
```

Then in the Python shell:
```python
from todo_app.models import Category

# Create some default categories
Category.objects.create(name='Work', color='#3498db')
Category.objects.create(name='Personal', color='#e74c3c')
Category.objects.create(name='Shopping', color='#f39c12')
Category.objects.create(name='Health', color='#27ae60')

# Exit the shell
exit()
```

### Step 5: Start the server
```bash
python manage.py runserver
```

### Step 6: Visit the app
Go to http://127.0.0.1:8000/ and enjoy your new features!

---

## 🎉 New Features Available

### ✅ Priority Levels
- High, Medium, and Low priorities
- Color-coded badges
- Filter tasks by priority

### 🏷️ Categories/Tags
- Create custom categories
- Assign categories to tasks
- Filter by category
- Color-coded category badges
- Manage categories from the Categories page

### 📅 Due Dates
- Set due dates and times for tasks
- Visual overdue indicators
- See which tasks need attention

### ☑️ Subtasks
- Break down tasks into smaller subtasks
- Check off subtasks as you complete them
- Track progress on complex tasks

### 📝 Notes
- Add detailed notes to any task
- Expandable notes section
- Keep all task-related information in one place

### 🔍 Filtering
- Filter by category, priority, or status
- View only active or completed tasks
- Clear all filters with one click

---

## 📊 Your Existing Data

Don't worry! Your existing tasks are safe:
- All existing tasks will keep their data
- New fields will have default values:
  - Priority: Medium
  - Category: None
  - Due Date: None
  - Notes: Empty
  - No subtasks initially

You can edit your existing tasks to add these new features!

---

## 🆘 Troubleshooting

### Migration Issues
If you get migration errors:
```bash
# Delete the database (you'll lose data!)
rm db.sqlite3

# Delete old migrations
rm todo_app/migrations/0*.py

# Create fresh migrations
python manage.py makemigrations
python manage.py migrate
```

### Module Import Errors
Make sure you've replaced ALL files, especially:
- `todo_app/models.py`
- `todo_app/views.py`
- `todo_app/urls.py`
- `todo_app/admin.py`

### CSRF Token Errors
If you get CSRF errors with subtasks, make sure:
1. You're using the correct template files
2. The server is running
3. You've cleared your browser cache

---

## 🎨 Next Steps

Try out the new features:
1. Create some categories (Work, Personal, etc.)
2. Add a task with a due date
3. Set priorities on your tasks
4. Break down a complex task into subtasks
5. Add notes with additional details
6. Use filters to focus on specific tasks

Enjoy your enhanced todo app! 🎉
