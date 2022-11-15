from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (MyUser, Student, NotesPTS, 
                    Intake, Observation, 
                    Support, OcupationalTherapy, 
                    SpeechTherapy, UsersData, Stream, 
                    ImplicitStrategy, ReviewMeetingNote)



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
                    'date_review', 'intake',
                    'level', 'name' )
class ImplicitStrategyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    pass

class ReviewMeetingNoteAdmin(admin.ModelAdmin):
    list_display = ('strategies', 'text_strategy', 'notes', 
                    'progress', 'user', 'stream', 'student')
    def strategies(self, obj):
        resp = "/ ".join([note.name for note in obj.strategy.all()])
        return resp

    def student(self, obj):
        return (obj.stream.student.first_name + ' '
                +  obj.stream.student.last_name)

admin.site.register(MyUser, UserAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(NotesPTS, NotesPTSAdmin)
admin.site.register(Intake, IntakeAdmin)
admin.site.register(Observation, ObservationAdmin)
admin.site.register(Support, SupportAdmin)
admin.site.register(OcupationalTherapy, OcupationalTherapyAdmin)
admin.site.register(SpeechTherapy, SpeechTherapyAdmin)
admin.site.register(UsersData, UsersDataAdmin)
admin.site.register(Stream, StreamAdmin)
admin.site.register(ImplicitStrategy, ImplicitStrategyAdmin)
admin.site.register(ReviewMeetingNote, ReviewMeetingNoteAdmin)
