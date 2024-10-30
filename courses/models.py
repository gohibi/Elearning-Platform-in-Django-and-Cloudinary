import uuid
from django.db import models
import helpers
from cloudinary.models import CloudinaryField
from django.utils.text import slugify

# Create your models here.
helpers.cloudinary_init()

def generate_public_id(instance,*args,**kwargs):
    title = instance.title
    unique_id = str(uuid.uuid4()).replace("-","")
    if not title:
        return unique_id
    slug = slugify(title)
    unique_id_short = unique_id[:5]
    return f"{slug}-{unique_id_short}"

# def get_public_id_prefix(instance,*args,**kwargs):
#     title = instance.title
#     if title:
#         slug = slugify(title)
#         unique_id = str(uuid.uuid4()).replace("-","")[:5]
#         return f"courses/{slug}-{unique_id  }"
#     if instance.id:
#         return f"courses/{instance.id}"
#     return "courses"
def get_public_id_prefix(instance,*args,**kwargs):
    if hasattr(instance,"path"):
        path = instance.path
        if path.startswith("/"):
            path = path[1:]
        if path.endswith("/"):
            path = path[:-1]
        return path
    public_id = instance.public_id
    model_class = instance.__class__
    model_name = model_class.__name__
    model_name_slug = slugify(model_name)
    if not public_id:
        return f"{model_name_slug}"
    return f"{model_name_slug}/{public_id}"
  

# def get_display_name(instance,*args,**kwargs):
#     title = instance.title
#     if title:
#         return title
#     return "Course upload"
def get_display_name(instance,*args,**kwargs):
    if hasattr(instance,'get_display_name'):
        return instance.get_display_name()
    elif hasattr(instance,'title'):
        return instance.title
    model_class = instance.__class__
    model_name = model_class.__name__
    return f"{model_name} Upload"

# get_thumbnail_display_name = lambda instance:get_display_name(instance,is_thumbanil=True)

def handle_upload(instance, filename):
    return f"{filename}"

class StatusPublish(models.TextChoices):
    PUBLISHED = "pub","Published"
    COMING_SOOM = "soon","Coming Soon"
    DRAFT = "draft","Draft"
    
class AccessREquirement(models.TextChoices):
    ANYONE = "any","Anyone"
    EMAIL_REQUIRED = "email_required","Email required"


    
class Course(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4(),unique=True)
    public_id = models.CharField(max_length=150,blank=True, null=True)
    image = CloudinaryField(
        'image',
        null=True,
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=["course","thumbnail"]
        )
    access = models.CharField(
        max_length=15,
        choices=AccessREquirement.choices,
        default=AccessREquirement.EMAIL_REQUIRED
        )
    status = models.CharField(
        max_length=10,
        choices=StatusPublish.choices,
        default=StatusPublish.DRAFT
        )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def save(self,*args,**kwargs):
        if self.public_id=="" or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args,**kwargs)
        
    def get_display_name(self):
        return f"{self.title} - Course"
    
    def get_absolute_url(self):
        return self.path
    
    @property
    def path(self):
        return f"/courses/{self.public_id}"
    
    def __str__(self):
        return f"{self.title}"
    
    @property
    def is_published(self):
        return self.status == StatusPublish.PUBLISHED
    
    @property
    def image_admin_url(self):
        if not self.image:
            return ""
        images_options ={
            "width":200
        }
        url =self.image.build_url(**images_options)
        return url
    
    def get_image_thumbnail(self, as_html=False, width=500):
        if not self.image:
            return ""
        image_options ={
            "width":width
        }
         
        if as_html:
            return self.image.image(**image_options)
        
        url =self.image.build_url(**image_options)
        return url 
    
    def get_image_detail(self, as_html=False, width=750):
        if not self.image:
            return ""
        image_options ={
            "width":width
        }
         
        if as_html:
            return self.image.image(**image_options)
        
        url =self.image.build_url(**image_options)
        return url 
    

class Lesson(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=150,blank=True, null=True)
    thumbnail = CloudinaryField(
        "image", 
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        tags=['image','thumbnail','lesson'],
        blank=True,
        null=True)
    video = CloudinaryField(
        "video",
        public_id_prefix=get_public_id_prefix,
        display_name=get_display_name,
        blank=True, 
        null=True,
        tags=['video','lesson'],
        resource_type="video")
    
    order = models.IntegerField(default=0)
    status = models.CharField(max_length=10,choices=StatusPublish.choices,default=StatusPublish.DRAFT)
    can_preview = models.BooleanField(default=False ,
        help_text="If user does not have access to course, can they see this ?")
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)   
    
    class Meta:
        ordering = ['order','-updated']
        
        
    def save(self,*args,**kwargs):
        if self.public_id=="" or self.public_id is None:
            self.public_id = generate_public_id(self)
        super().save(*args,**kwargs) 
        
    @property
    def path(self):
        course_path = self.course.path
        if course_path.endswith("/"):
            course_path = course_path[:-1]
        return f"{course_path}/lessons/{self.public_id}"
    
    def get_display_name(self):
        return f"{self.title} - {self.course.get_display_name()}"
        