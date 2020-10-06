from django.contrib import admin
from django.db.models import Count

from expense.models import Claim, Expense, MedExpenseRelation, MedExpenseType


class MedExpenseRelationInline(admin.TabularInline):
    model = MedExpenseRelation


class MedExpenseTypeInline(admin.TabularInline):
    model = MedExpenseType


class ExpenseAdmin(admin.TabularInline):
    model = Expense
    fields = ['serial', 'status', 'expense_type', 'org_name', 'expense_amount', 'expense_file']
    readonly_fields = ['serial']


@admin.register(Claim)
class ClaimAdmin(admin.ModelAdmin):
    class Meta:
        model = Claim

    list_display = ['serial', 'get_company', 'user', 'manager', 'get_expense_count', 'status']
    list_filter = ['manager', 'status']
    search_fields = ['user__name', 'manager__user']
    readonly_fields = ['id', 'serial']
    autocomplete_fields = ['user', 'manager']
    inlines = [ExpenseAdmin]

    def get_queryset(self, request):
        qs = super().get_queryset(request).select_related(
            'user', 'user__companyuser', 'manager'
        ).annotate(
            expense_count=Count('expense')
        )
        return qs

    def get_company(self, obj):
        return obj.user.companyuser.company.name

    def get_expense_count(self, obj):
        return obj.expense_count

    get_company.short_description = '회사'
    get_expense_count.short_description = '진료비건'
