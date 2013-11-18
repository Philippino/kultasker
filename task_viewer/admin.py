from django.contrib import admin
from task_viewer.models import Check, Date, Result, Task

admin.site.register(Check)
admin.site.register(Date)
admin.site.register(Result)
admin.site.register(Task)
