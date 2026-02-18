from django.contrib import admin
from .models import Todo, Category, Subtask


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)


class SubtaskInline(admin.TabularInline):
    model = Subtask
    extra = 1
    fields = ('title', 'completed', 'order')


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'priority', 'category', 'due_date', 'completed', 'created_at')
    list_filter = ('completed', 'priority', 'category', 'created_at')
    search_fields = ('title', 'description', 'notes')
    inlines = [SubtaskInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'completed')
        }),
        ('Organization', {
            'fields': ('priority', 'category', 'due_date')
        }),
        ('Additional Details', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )
