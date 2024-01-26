from django.shortcuts import render,redirect
from. forms import TeacherRegistrationForm
from django.views.generic import FormView,TemplateView,DetailView
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from. models import TeacherDetails
from student.models import TuitionReview

# Create your views here.
class TeacherRegisterView(FormView):
    template_name='apply_teacher.html'
    form_class = TeacherRegistrationForm
    success_url = reverse_lazy('signup')
    def post(self,request, *args, **kwargs):
        form=self.form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            user=form.save()
            token=default_token_generator.make_token(user)
            print('token :',token)
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            print('uid :',uid)
            confirm_link=f"http://127.0.0.1:8000/teacher/active/{uid}/{token}"
            # confirm_link=f"https://success-tuition.onrender.com/student/active/{uid}/{token}"
            email_subject="Confirm Your Email"
            email_body=render_to_string('confirm_mail.html',{'confirm_link': confirm_link})
            email=EmailMultiAlternatives(email_subject,"",to=[user.email])
            email.attach_alternative(email_body,'text/html')
            email.send()
            messages.success(request,"Check Your mail to confirm")
            return HttpResponseRedirect(self.get_success_url())
        else:
            # Add form errors to messages
            for _, error in form.errors.items():
                messages.warning(request, error)

            # Return the form with errors
            return self.form_invalid(form)
        
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['type']='Apply Teacher'
        return context
    

def ActiveTeacher(request,uid64,token):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user=User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        return redirect('confirm_teacher')
    else:
        return redirect('signup')
    
class TeacherApplicationConfirm(TemplateView):
    template_name='confirm_teacher.html'


class TeacherDetailsView(DetailView):
    model = TeacherDetails
    # pk_url_kwargs = 'id'
    template_name='teacher_details.html'
     
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['data']=TuitionReview.objects.filter(teacher_id=self.object.id)
        # context['data']=TuitionReview.objects.all()
        return context
