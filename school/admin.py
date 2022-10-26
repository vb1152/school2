from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (MyUser, Student, NotesPTS, 
                    Consern, Intake, Observation, 
                    Support, OcupationalTherapy, 
                    SpeechTherapy, UsersData, Stream)



# Register your models here.
class MyUserAdmin(admin.ModelAdmin):
    list_display = ('is_student', 'is_teacher', 'is_conselor')
    fields = list(UserAdmin.fieldsets)
    fields[0] = ('General', {'fields': ('username', 'password', 'is_sst', 'is_teacher', 'is_conselor')})
    UserAdmin.fieldsets = tuple(fields)


class StudentAdmin(admin.ModelAdmin):
    list_display = ('school_id', 'first_name', 'middle_name', 'last_name', 'teacher')

class NotesPTSAdmin(admin.ModelAdmin):
    pass

class ConsernAdmin(admin.ModelAdmin):
    pass

class IntakeAdmin(admin.ModelAdmin):
    pass

class ObservationAdmin(admin.ModelAdmin):
    pass

class SupportAdmin(admin.ModelAdmin):
    pass

class OcupationalTherapyAdmin(admin.ModelAdmin):
    pass

class SpeechTherapyAdmin(admin.ModelAdmin):
    pass

class UsersDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'person_id', 'grades')

class StreamAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'date_start', 
                    'date_review', 'concern', 'intake',
                    'level', 'status', 'observation', 'support', 'name' )

    pass


admin.site.register(MyUser, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(NotesPTS, NotesPTSAdmin)
admin.site.register(Consern, ConsernAdmin)
admin.site.register(Intake, IntakeAdmin)
admin.site.register(Observation, ObservationAdmin)
admin.site.register(Support, SupportAdmin)
admin.site.register(OcupationalTherapy, OcupationalTherapyAdmin)
admin.site.register(SpeechTherapy, SpeechTherapyAdmin)
admin.site.register(UsersData, UsersDataAdmin)
admin.site.register(Stream, StreamAdmin)
