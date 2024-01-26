from django.shortcuts import render,get_object_or_404
from django.views.generic import CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from.forms import AddTuitionForm,EditTuitionForm,ApplyTuitionForm,ContactForm
from.models import Tuition,ApplyTuition
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from student.models import StudentClass

# Create your views here.
class AddTuitionView(LoginRequiredMixin,CreateView):
    template_name='superuser_form.html'
    model=Tuition
    form_class=AddTuitionForm
    success_url=reverse_lazy('home')
    def form_valid(self, form):
        return super().form_valid(form)
    
class EditTuitionView(LoginRequiredMixin,UpdateView):
    model=Tuition
    form_class=EditTuitionForm
    template_name='superuser_form.html'
    pk_url_kwarg='id'
    success_url=reverse_lazy('home')

class DeleteTuitionView(LoginRequiredMixin,DeleteView):
    model=Tuition
    template_name='delete.html'
    success_url=reverse_lazy('profile')
    pk_url_kwarg='id'


    
class ContactUsView(FormView):
    template_name = 'contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Thanks to reach us. Our support team will contact you soon. Disscuss there everything . Or You also can contuct us by the beside email and phone number')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        # Handle form errors
        for _, error in form.errors.items():
            messages.warning(self.request, error)
            return self.form_invalid(form)

         
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Tuition Apply"
        return context
        

class TuitionApplyView(FormView):
    template_name = 'apply_tuition.html'
    form_class = ApplyTuitionForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        apply_tuition = form.save(commit=False)
        apply_tuition.student = self.request.user
        apply_tuition.save()
        messages.success(self.request, 'Apply successful, wait for confirmation mail')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        # Handle form errors
        for _, error in form.errors.items():
            messages.warning(self.request, error)
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Contact Us"
        return context
