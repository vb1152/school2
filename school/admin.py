from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Student


# Register your models here.
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('is_student', 'is_teacher', 'is_conselor')
    fields = list(UserAdmin.fieldsets)
    fields[0] = ('General', {'fields': ('username', 'password', 'is_sst', 'is_teacher', 'is_conselor')})
    UserAdmin.fieldsets = tuple(fields)


class StudentAdmin(admin.ModelAdmin):
    pass


admin.site.register(MyUser, UserAdmin)
admin.site.register(Student, StudentAdmin)