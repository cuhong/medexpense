from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, Row, Column, Div
from django import forms

from expense.models import Claim, MedExpenseRelation, Expense, MedExpenseType


class ClaimCreateForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['relation', 'name']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["relation"].queryset = MedExpenseRelation.objects.filter(
            company__companyuser__user=self.request.user)

    helper = FormHelper()
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', '다음', css_class='btn-primary btn-block'))


class ExpenseCreateForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['expense_type', 'org_name', 'expense_amount', 'expense_file']
        widgets = {'expense_file': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)
        self.fields["expense_type"].queryset = MedExpenseType.objects.filter(
            company__companyuser__user=self.request.user)

    helper = FormHelper()
    helper.form_id = 'expenseForm'
    helper.form_method = 'POST'

