from django.urls import path
from. import views

urlpatterns = [
    path('add_tuition/', views.AddTuitionView.as_view(),name='add_tuition'),
    path('edit_tuition/<int:id>/', views.EditTuitionView.as_view(),name='edit_tuition'),
    path('delete_tuition/<int:id>/', views.DeleteTuitionView.as_view(),name='delete_tuition'),
    path('apply_tuition/',views.TuitionApplyView.as_view(),name='apply'),
]
