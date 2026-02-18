from django.test import TestCase
from .models import Todo


class TodoModelTest(TestCase):
    def setUp(self):
        Todo.objects.create(title="Test Todo", description="Test Description")

    def test_todo_creation(self):
        todo = Todo.objects.get(title="Test Todo")
        self.assertEqual(todo.description, "Test Description")
        self.assertFalse(todo.completed)
