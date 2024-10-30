from django.contrib import admin
from courses.models import Course,Lesson
from django.utils.html import format_html
from cloudinary import CloudinaryImage


class LessonInline(admin.StackedInline):
    model = Lesson
    readonly_fields = ['public_id','updated']
    extra = 0
    
@admin.register(Course)
class AdminCourse(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = ["title","display_image","access","status"]
    list_filter =["status","access"]
    fields = ["public_id","title","description","status","image","access","display_image"]
    readonly_fields = ["public_id","display_image"]
    
    
    def display_image(self,obj,*args,**kwargs):
        url = obj.image_admin_url
        # cloudinary_id = str(obj.image)
        # cloudinary_html = CloudinaryImage(cloudinary_id).image(width=100 , height=100)
        # return format_html(cloudinary_html)
        # return cloudinary_id
        return format_html(f"<img src={url} />")
    display_image.short_description = "Current Image"


    
