from django.contrib import admin
from quiz.models.custom_user import * 
from quiz.models.quiz import * 
from django.contrib.auth.admin import UserAdmin 


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'role', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email', 'role')
    list_editable = ('role', 'is_staff', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password', 'role')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )


class AnswerInline(admin.TabularInline):
    model = Answer 
    extra = 4 


class QuestionInline(admin.TabularInline):
    model = Question 
    extra = 15 
    inlines = [AnswerInline]


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ('title',)


class ResultDetailInline(admin.TabularInline):
    model = ResultDetail 
    extra = 1


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    inlines = [ResultDetailInline]
    search_fields = ['exam',]