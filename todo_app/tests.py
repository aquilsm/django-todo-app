from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from .models import Todo, Category, Subtask


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name='Work',
            color='#3498db'
        )

    def test_category_creation(self):
        """Test category is created correctly"""
        self.assertEqual(self.category.name, 'Work')
        self.assertEqual(self.category.color, '#3498db')

    def test_category_str(self):
        """Test category string representation"""
        self.assertEqual(str(self.category), 'Work')


class TodoModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')
        self.todo = Todo.objects.create(
            title="Test Todo",
            description="Test Description",
            priority='high',
            category=self.category
        )

    def test_todo_creation(self):
        """Test todo is created with correct attributes"""
        self.assertEqual(self.todo.title, "Test Todo")
        self.assertEqual(self.todo.description, "Test Description")
        self.assertEqual(self.todo.priority, 'high')
        self.assertFalse(self.todo.completed)

    def test_todo_str(self):
        """Test todo string representation"""
        self.assertEqual(str(self.todo), "Test Todo")

    def test_priority_color(self):
        """Test priority color mapping"""
        high_todo = Todo.objects.create(title="High", priority='high')
        medium_todo = Todo.objects.create(title="Medium", priority='medium')
        low_todo = Todo.objects.create(title="Low", priority='low')
        
        self.assertEqual(high_todo.priority_color, '#e74c3c')
        self.assertEqual(medium_todo.priority_color, '#f39c12')
        self.assertEqual(low_todo.priority_color, '#3498db')

    def test_is_overdue(self):
        """Test overdue detection"""
        # Not overdue (future date)
        future_todo = Todo.objects.create(
            title="Future",
            due_date=timezone.now() + timedelta(days=1)
        )
        self.assertFalse(future_todo.is_overdue)
        
        # Overdue (past date)
        past_todo = Todo.objects.create(
            title="Past",
            due_date=timezone.now() - timedelta(days=1)
        )
        self.assertTrue(past_todo.is_overdue)
        
        # Completed (not overdue even if past)
        completed_todo = Todo.objects.create(
            title="Completed",
            due_date=timezone.now() - timedelta(days=1),
            completed=True
        )
        self.assertFalse(completed_todo.is_overdue)


class SubtaskModelTest(TestCase):
    def setUp(self):
        self.todo = Todo.objects.create(title="Parent Todo")
        self.subtask = Subtask.objects.create(
            todo=self.todo,
            title="Subtask 1",
            order=1
        )

    def test_subtask_creation(self):
        """Test subtask is created correctly"""
        self.assertEqual(self.subtask.title, "Subtask 1")
        self.assertEqual(self.subtask.todo, self.todo)
        self.assertFalse(self.subtask.completed)

    def test_subtask_str(self):
        """Test subtask string representation"""
        expected = f"{self.todo.title} - {self.subtask.title}"
        self.assertEqual(str(self.subtask), expected)


class TodoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category')
        self.todo = Todo.objects.create(
            title="Test Todo",
            description="Test Description",
            priority='medium',
            category=self.category
        )

    def test_todo_list_view(self):
        """Test todo list view returns 200"""
        response = self.client.get(reverse('todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Todo")

    def test_add_todo_view_get(self):
        """Test add todo GET request"""
        response = self.client.get(reverse('add_todo'))
        self.assertEqual(response.status_code, 200)

    def test_add_todo_view_post(self):
        """Test add todo POST request"""
        data = {
            'title': 'New Todo',
            'description': 'New Description',
            'priority': 'high',
            'category': self.category.id
        }
        response = self.client.post(reverse('add_todo'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Todo.objects.filter(title='New Todo').exists())

    def test_toggle_todo(self):
        """Test toggling todo completion"""
        self.assertFalse(self.todo.completed)
        response = self.client.post(reverse('toggle_todo', args=[self.todo.id]))
        self.todo.refresh_from_db()
        self.assertTrue(self.todo.completed)

    def test_delete_todo(self):
        """Test deleting todo"""
        response = self.client.post(reverse('delete_todo', args=[self.todo.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(id=self.todo.id).exists())

    def test_edit_todo_view_get(self):
        """Test edit todo GET request"""
        response = self.client.get(reverse('edit_todo', args=[self.todo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.todo.title)

    def test_edit_todo_view_post(self):
        """Test edit todo POST request"""
        data = {
            'title': 'Updated Todo',
            'description': 'Updated Description',
            'priority': 'low',
            'category': self.category.id
        }
        response = self.client.post(reverse('edit_todo', args=[self.todo.id]), data)
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Todo')

    def test_filter_by_category(self):
        """Test filtering todos by category"""
        response = self.client.get(reverse('todo_list') + f'?category={self.category.id}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.todo.title)

    def test_filter_by_priority(self):
        """Test filtering todos by priority"""
        response = self.client.get(reverse('todo_list') + '?priority=medium')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.todo.title)

    def test_filter_by_status(self):
        """Test filtering todos by status"""
        response = self.client.get(reverse('todo_list') + '?status=active')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.todo.title)


class CategoryViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Test Category', color='#000000')

    def test_manage_categories_view(self):
        """Test manage categories view"""
        response = self.client.get(reverse('manage_categories'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Category')

    def test_create_category(self):
        """Test creating a new category"""
        data = {
            'name': 'New Category',
            'color': '#ff0000'
        }
        response = self.client.post(reverse('manage_categories'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Category.objects.filter(name='New Category').exists())

    def test_delete_category(self):
        """Test deleting a category"""
        response = self.client.post(reverse('delete_category', args=[self.category.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Category.objects.filter(id=self.category.id).exists())


class SubtaskViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.todo = Todo.objects.create(title="Test Todo")
        self.subtask = Subtask.objects.create(
            todo=self.todo,
            title="Test Subtask"
        )

    def test_toggle_subtask(self):
        """Test toggling subtask completion"""
        self.assertFalse(self.subtask.completed)
        response = self.client.post(reverse('toggle_subtask', args=[self.subtask.id]))
        self.assertEqual(response.status_code, 200)
        self.subtask.refresh_from_db()
        self.assertTrue(self.subtask.completed)

    def test_delete_subtask(self):
        """Test deleting subtask"""
        response = self.client.post(reverse('delete_subtask', args=[self.subtask.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Subtask.objects.filter(id=self.subtask.id).exists())