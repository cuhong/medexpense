from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from account.forms import UserChangeForm, UserCreationForm
from account.models import Company, CompanyUser, Manager
from expense.admin import MedExpenseRelationInline, MedExpenseTypeInline

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = (
        'email', 'name', 'cellphone', 'is_admin', 'registered_at'
    )
    ordering = ('-registered_at',)
    search_fields = ['email', 'name', 'cellphone']
    list_filter = ['is_admin']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'cellphone',)}),
        ('Permissions', {'fields': ('is_admin', 'is_superuser', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'cellphone', 'password1', 'password2'),
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


class CompanyUserInline(admin.TabularInline):
    model = CompanyUser
    fields = ['user', 'is_admin']


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    inlines = [CompanyUserInline, MedExpenseRelationInline, MedExpenseTypeInline]

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ['user']
    search_fields = ['user__name']


@admin.register(CompanyUser)
class CompanyUserAdmin(admin.ModelAdmin):
    list_display = ['company', 'user', 'is_admin', 'registered_at']