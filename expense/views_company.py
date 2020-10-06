import json

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView, ListView, CreateView

from account.models import CompanyUser
from common.views import PassRequestToFormViewMixin
from expense.forms import ClaimCreateForm, ExpenseCreateForm
from expense.models import Claim, Expense


class CompanyUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return CompanyUser.objects.filter(user=self.request.user).exists()

    def get_login_url(self):
        if not self.request.user.is_authenticated:
            return super().get_login_url()
        else:
            return ''


class UserIndexView(CompanyUserMixin, ListView):
    model = Claim
    template_name = 'company_user/index.html'
    paginate_by = 20
    context_object_name = 'claim_list'

    def get_queryset(self):
        qs = super().get_queryset().values(
            'id', 'registered_at', 'status', 'user__name', 'user__companyuser__company__name', 'manager__name',
            'relation__name', 'name', 'serial'
        ).filter(user=self.request.user)
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        ctxt = super().get_context_data(object_list=object_list, **kwargs)
        ctxt['claim_status_choices'] = Claim.CLAIM_STATUS
        return ctxt


class ClaimCreateView(PassRequestToFormViewMixin, CompanyUserMixin, CreateView):
    model = Claim
    form_class = ClaimCreateForm
    template_name = 'company_user/claim_create.html'
    context_object_name = 'claim'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        url = reverse('company:claim_detail', args=[self.object.id])
        return url


class ClaimDetailView(CompanyUserMixin, ListView):
    model = Expense
    template_name = 'company_user/claim_detail.html'
    paginate_by = 20
    context_object_name = 'expense_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['claim'] = Claim.objects.values(
            'relation__name', 'name', 'manager__name', 'status', 'registered_at','serial'
        ).get(Q(user=self.request.user) & Q(id=self.kwargs['claim_id']))
        context['claim_status_choices'] = Claim.CLAIM_STATUS
        context['expense_status_choices'] = Expense.CLAIM_STATUS
        context['expense_form'] = ExpenseCreateForm(**{'request': self.request})
        return context

    def get_queryset(self):
        claim_id = self.kwargs['claim_id']
        qs = super().get_queryset().filter(
            Q(claim__user=self.request.user) & Q(claim_id=claim_id)
        )
        return qs

    def post(self, request, claim_id):
        form = ExpenseCreateForm(self.request.POST, **{'request': self.request})
        if form.is_valid():
            expense = form.save(commit=False)
            expense.claim_id = claim_id
            expense.save()
            rd = {"result": True}
        else:
            rd = {"result": False, "error": form.errors}
        return HttpResponse(json.dumps(rd), content_type='application/json')
