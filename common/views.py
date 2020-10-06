import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import View

from common.forms import ProtectedFileForm
from common.models import ProtectedFile


class PassRequestToFormViewMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs


class ProtectedFileView(LoginRequiredMixin, View):
    def get(self, request):
        pf = get_object_or_404(ProtectedFile, id=request.GET.get('pf_id', None))
        return HttpResponseRedirect(pf.file.url)

    def post(self, request):
        form = ProtectedFileForm(request.POST, request.FILES)
        if form.is_valid():
            pf = form.save()
            pf.refresh_from_db()
            data = {"id": str(pf.id), "url": pf.file.url}
            rd = {"result": True, "data": data}
        else:
            rd = {"result": False, "errors": form.errors}
        return HttpResponse(json.dumps(rd), content_type='application/json')
