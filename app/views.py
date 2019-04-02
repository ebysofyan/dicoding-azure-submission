"""
app.views
"""
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, FormView

from .forms import ProgrammingForm
from .models import Programming

# Create your views here.


class ProgrammingView(FormView):
    """ProgrammingView"""
    template_name = 'index.html'
    form_class = ProgrammingForm

    def get_context_data(self, **kwargs):
        ctx = super(ProgrammingView, self).get_context_data(**kwargs)
        ctx['list'] = Programming.objects.all()
        return ctx

    def form_valid(self, form):
        messages.success(self.request, "New Programming language added", extra_tags='success')
        form.save()
        return redirect('index:view')

    def form_invalid(self, form):
        err = {}
        for k, val in form.errors.items():
            err[k] = ', '.join(val)

        messages.error(self.request, err, extra_tags='danger')
        return redirect('index:view')


class ProgrammingDeleteView(DeleteView):
    """
    ProgrammingDeletView
    """
    model = Programming
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('index:view')

    def get(self, *args, **kwargs):
        """get request"""
        return self.post(*args, **kwargs)
