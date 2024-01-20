from django.contrib import admin
from. import models
# Register your models here.
class ClassAdmin(admin.ModelAdmin):
    prepopulated_fields={'slug':('class_name',)}
admin.site.register(models.StudentClass, ClassAdmin)
admin.site.register(models.Student)
admin.site.register(models.TuitionReview)