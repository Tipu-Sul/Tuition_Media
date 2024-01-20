
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login,logout,update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from. forms import StudentRegistrationForm,StudentUpdateForm,TuitionReviewForm
from django.views.generic import TemplateView,ListView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives,EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.views import View
from django.contrib.auth.forms import PasswordChangeForm
from tuition.models import ApplyTuition,Tuition
from. models import StudentClass,Student,TuitionReview

# Create your views here.
class Homeview(TemplateView):
    template_name="home.html"
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        class_slug=self.kwargs.get('category_slug') 
        data=Tuition.objects.all()
        class_category=StudentClass.objects.all()

        if class_slug:
            category=get_object_or_404(StudentClass,slug=class_slug)
            data=data.filter(name=category)
        context['data']=data
        context['data2']=class_category
        context['data3']=TuitionReview.objects.all()
        return context
    
def home(request,category_slug=None):
    data=Tuition.objects.all()
    if category_slug is not None:
        category=StudentClass.objects.get(slug=category_slug)
        data=Tuition.objects.filter(name=category)
    book_ctg=StudentClass.objects.all()
    return render(request,'home.html',{'data':data, 'data2':book_ctg})

    
class StudentRegisterView(FormView):
    template_name='signup.html'
    form_class = StudentRegistrationForm
    success_url = reverse_lazy('signup')
    def post(self,request, *args, **kwargs):
        form=self.form_class(data=request.POST, files=request.FILES)
        if form.is_valid():
            user=form.save()
            token=default_token_generator.make_token(user)
            print('token :',token)
            uid=urlsafe_base64_encode(force_bytes(user.pk))
            print('uid :',uid)
            confirm_link=f"http://127.0.0.1:8000/student/active/{uid}/{token}"
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
        context['type']='SignUp'
        return context

def ActiveStudent(request,uid64,token):
    try:
        uid=urlsafe_base64_decode(uid64).decode()
        user=User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError,User.DoesNotExist):
        user=None
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active=True
        user.save()
        return redirect('login')
    else:
        return redirect('signup')

class StudentLoginView(LoginView):
    template_name='signup.html'
    def get_success_url(self):
        messages.success(self.request,'Login Successfully')
        return '/student/profile/'
        # return super().get_success_url('profile')
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['type']='Login'
        return context

@login_required
def StudentLogout(request):
    if request.user.is_authenticated:
        messages.success(request,'You are logged out successfully')
        logout(request)
        return redirect('login')
    
class StudentProfileView(LoginRequiredMixin,ListView):
    model=Tuition
    def get_template_names(self):
        if self.request.user.is_superuser:
            template_name="superuser.html" 
            return template_name   
        else:
            template_name='profile.html'
            return template_name
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["data"] = Student.objects.filter(user=self.request.user)
        context["data2"] = ApplyTuition.objects.filter(student=self.request.user)
        if self.request.user.is_superuser:
            context["data_3"] = Tuition.objects.all()
        return context
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Tuition.objects.all()
     
        else:
            return Student.objects.filter(user=self.request.user)


class StudentUpdateView(LoginRequiredMixin,View):
    template_name='signup.html'
    def get(self, request):
        form=StudentUpdateForm(instance=request.user)
        return render(request,self.template_name,{'form':form})
    
    def post(self, request):
        form=StudentUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(self.request,'Account update successfully')
        return redirect('profile')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "User Update"
        return context

@login_required
def PasswordUpdateView(request):
    if request.method =='POST':
        form=PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save() 
            update_session_auth_hash(request,form.user)
            messages.success(request,'Password update successfully') 
            return redirect('profile')
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request,'signup.html',{'form':form,'type':'PasswordChange'})




@login_required
def TuitionReviewView(request,id):
    subject=Tuition.objects.get(pk=id)
    if request.method == 'POST':
        form=TuitionReviewForm(request.POST)
        if form.is_valid():
            text=form.cleaned_data['body']
            star=form.cleaned_data['star']
            review=TuitionReview.objects.create(
                tuition=subject,
                name=request.user.first_name,
                email=request.user.email,
                body=text,
                star=star,
            )
            review.save()
            messages.success(request,'Review successfull')
            return redirect('profile')
    else:
        form=TuitionReviewForm()
    return render(request,'signup.html',{'form':form,'type':'Review'})

