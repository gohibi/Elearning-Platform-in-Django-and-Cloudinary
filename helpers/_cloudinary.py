# settings.py
import cloudinary
from decouple import config

CLOUDINARY_NAME = config("CLOUDINARY_NAME" , default="")
CLOUDINARY_API_PUBLIC_KEY = config("CLOUDINARY_API_PUBLIC_KEY",default="")
CLOUDINARY_API_SECRET_KEY = config("CLOUDINARY_API_SECRET_KEY")

def cloudinary_init():   
    cloudinary.config( 
        cloud_name =CLOUDINARY_NAME , 
        api_key = CLOUDINARY_API_PUBLIC_KEY , 
        api_secret =CLOUDINARY_API_SECRET_KEY,
        secure=True
    )