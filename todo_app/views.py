from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Todo, Category, Subtask
from django.utils import timezone


def todo_list(request):
    """Display all todos with filtering"""
    todos = Todo.objects.all()
    
    # Filter by category
    category_filter = request.GET.get('category')
    if category_filter:
        todos = todos.filter(category_id=category_filter)
    
    # Filter by priority
    priority_filter = request.GET.get('priority')
    if priority_filter:
        todos = todos.filter(priority=priority_filter)
    
    # Filter by status
    status_filter = request.GET.get('status')
    if status_filter == 'active':
        todos = todos.filter(completed=False)
    elif status_filter == 'completed':
        todos = todos.filter(completed=True)
    
    categories = Category.objects.all()
    
    context = {
        'todos': todos,
        'categories': categories,
        'selected_category': category_filter,
        'selected_priority': priority_filter,
        'selected_status': status_filter,
    }
    return render(request, 'todo_app/todo_list.html', context)


def add_todo(request):
    """Add a new todo"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'medium')
        category_id = request.POST.get('category')
        due_date = request.POST.get('due_date')
        notes = request.POST.get('notes', '')
        
        if title:
            todo = Todo.objects.create(
                title=title,
                description=description,
                priority=priority,
                category_id=category_id if category_id else None,
                due_date=due_date if due_date else None,
                notes=notes
            )
            
            # Handle subtasks
            subtask_titles = request.POST.getlist('subtask_title[]')
            for idx, subtask_title in enumerate(subtask_titles):
                if subtask_title.strip():
                    Subtask.objects.create(
                        todo=todo,
                        title=subtask_title.strip(),
                        order=idx
                    )
            
        return redirect('todo_list')
    
    categories = Category.objects.all()
    return render(request, 'todo_app/add_todo.html', {'categories': categories})


def toggle_todo(request, todo_id):
    """Toggle todo completion status"""
    todo = get_object_or_404(Todo, id=todo_id)
    todo.completed = not todo.completed
    todo.save()
    return redirect('todo_list')


def delete_todo(request, todo_id):
    """Delete a todo"""
    todo = get_object_or_404(Todo, id=todo_id)
    if request.method == 'POST':
        todo.delete()
    return redirect('todo_list')


def edit_todo(request, todo_id):
    """Edit a todo"""
    todo = get_object_or_404(Todo, id=todo_id)
    
    if request.method == 'POST':
        todo.title = request.POST.get('title', todo.title)
        todo.description = request.POST.get('description', todo.description)
        todo.priority = request.POST.get('priority', todo.priority)
        todo.notes = request.POST.get('notes', todo.notes)
        
        category_id = request.POST.get('category')
        todo.category_id = category_id if category_id else None
        
        due_date = request.POST.get('due_date')
        todo.due_date = due_date if due_date else None
        
        todo.save()
        
        # Update existing subtasks
        existing_subtask_ids = request.POST.getlist('subtask_id[]')
        existing_subtask_titles = request.POST.getlist('existing_subtask_title[]')
        existing_subtask_completed = request.POST.getlist('existing_subtask_completed[]')
        
        for idx, subtask_id in enumerate(existing_subtask_ids):
            if subtask_id:
                subtask = Subtask.objects.filter(id=subtask_id, todo=todo).first()
                if subtask:
                    subtask.title = existing_subtask_titles[idx]
                    subtask.completed = str(subtask_id) in existing_subtask_completed
                    subtask.save()
        
        # Add new subtasks
        new_subtask_titles = request.POST.getlist('new_subtask_title[]')
        for idx, subtask_title in enumerate(new_subtask_titles):
            if subtask_title.strip():
                Subtask.objects.create(
                    todo=todo,
                    title=subtask_title.strip(),
                    order=len(existing_subtask_ids) + idx
                )
        
        return redirect('todo_list')
    
    categories = Category.objects.all()
    return render(request, 'todo_app/edit_todo.html', {
        'todo': todo,
        'categories': categories
    })


def toggle_subtask(request, subtask_id):
    """Toggle subtask completion"""
    if request.method == 'POST':
        subtask = get_object_or_404(Subtask, id=subtask_id)
        subtask.completed = not subtask.completed
        subtask.save()
        return JsonResponse({'success': True, 'completed': subtask.completed})
    return JsonResponse({'success': False})


def delete_subtask(request, subtask_id):
    """Delete a subtask"""
    if request.method == 'POST':
        subtask = get_object_or_404(Subtask, id=subtask_id)
        subtask.delete()
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


def manage_categories(request):
    """Manage categories"""
    if request.method == 'POST':
        name = request.POST.get('name')
        color = request.POST.get('color', '#667eea')
        if name:
            Category.objects.create(name=name, color=color)
        return redirect('manage_categories')
    
    categories = Category.objects.all()
    return render(request, 'todo_app/manage_categories.html', {'categories': categories})


def delete_category(request, category_id):
    """Delete a category"""
    if request.method == 'POST':
        category = get_object_or_404(Category, id=category_id)
        category.delete()
    return redirect('manage_categories')
