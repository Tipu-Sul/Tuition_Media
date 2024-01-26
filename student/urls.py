from django.urls import path
from. import views

urlpatterns = [
    path('signup/',views.StudentRegisterView.as_view(),name='signup'),
    path('active/<uid64>/<token>/',views.ActiveStudent,name='activate'),
    path('login/',views.StudentLoginView.as_view(),name='login'),
    path('profile/',views.StudentProfileView.as_view(),name='profile'),
    path('update_profile/',views.StudentUpdateView.as_view(),name='update'),
    path('tuition/',views.TuitionView.as_view(),name='tuition'),
    path('category/<slug:category_slug>/', views.TuitionView.as_view(),name='class_wise_home'),
    # path('apply_tuition/',views.TuitionApplyView.as_view(),name='apply'),
    path('logout/',views.StudentLogout,name='logout'),
    path('update_password/',views.PasswordUpdateView,name='update_password'),
    path('review_tuition/<int:id>',views.TuitionReviewView,name='review'),
]
