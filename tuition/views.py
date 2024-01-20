from django.shortcuts import render,get_object_or_404
from django.views.generic import CreateView,UpdateView,DeleteView,FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from.forms import AddTuitionForm,EditTuitionForm,ApplyTuitionForm
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

# class TuitionApplyView(FormView):
#     template_name='apply_tuition.html'
#     model=ApplyTuition
#     form_class = ApplyTuitionForm
#     success_url = reverse_lazy('profile')
    
#     def get(self,request, *args, **kwargs):
#         form=self.form_class()
#         return render(request,self.template_name,{'form':form})
    
#     def post(self,request, *args, **kwargs):
#         form=self.form_class(request.POST)
#         if form.is_valid():
#             form.save(commit=False)
#             student_class_value=form.cleaned_data['student_class']
#             student_class_instance = get_object_or_404(StudentClass, class_name=student_class_value)
#             apply=ApplyTuition.objects.create(
#                 student=self.request.user,
#                 class_name=student_class_instance,
#                 )
#             form.save()
#             apply.save()
#             messages.success(request,'Apply sucessfull,wait for confirmation mail')
#             return HttpResponseRedirect(self.get_success_url())
#         else:
#             for _, error in form.errors.items():
#                 messages.warning(request, error)
#             return self.form_invalid(form)
        
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["type"] = "Tuition Apply"
#         return context
    
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
        context["type"] = "Tuition Apply"
        return context
        


