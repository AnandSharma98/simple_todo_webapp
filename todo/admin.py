from django.contrib import admin
from .models import Todo
# Register your models here.
class TodoAdmin(admin.ModelAdmin):  # this is to show that not editable field (completed) in the admin
    readonly_fields = ('created',)
admin.site.register(Todo, TodoAdmin)