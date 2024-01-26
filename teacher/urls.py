from django.urls import path
from. import views

urlpatterns = [
    path('apply_teacher/',views.TeacherRegisterView.as_view(),name='apply_teacher'),
    path('active/<uid64>/<token>/',views.ActiveTeacher,name='active_teacher'),
    path('confirm_application/',views.TeacherApplicationConfirm.as_view(),name='confirm_teacher'),
    path('teacher_details/<int:pk>/',views.TeacherDetailsView.as_view(),name='teacher_detail'),
]

