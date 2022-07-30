from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MyUser, Student, NotesPTS, Consern, Intake


# Register your models here.
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('is_student', 'is_teacher', 'is_conselor')
    fields = list(UserAdmin.fieldsets)
    fields[0] = ('General', {'fields': ('username', 'password', 'is_sst', 'is_teacher', 'is_conselor')})
    UserAdmin.fieldsets = tuple(fields)


class StudentAdmin(admin.ModelAdmin):
    pass

class NotesPTSAdmin(admin.ModelAdmin):
    pass

class ConsernAdmin(admin.ModelAdmin):
    pass

class IntakeAdmin(admin.ModelAdmin):
    pass

admin.site.register(MyUser, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(NotesPTS, NotesPTSAdmin)
admin.site.register(Consern, ConsernAdmin)
admin.site.register(Intake, IntakeAdmin)


