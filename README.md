# hexocean
  
  
  
# Url 
http://seotest.patrykorganisciak.pl  
  
# User instances:  
user_basic 8BVAk5j9wkTnMeR  
user_premium 8BVAk5j9wkTnMeR  
user_enterprise 8BVAk5j9wkTnMeR  
  
  
# Requirements 
Pillow==8.2.0  
uuid==1.30  
djangorestframework==3.12.4  
Django==3.2.3  
  
// I attached requirements.txt file but packages like django-thumbnails or django-imagekit haven't been used, there is no need to install it.  
    
# Other
Thumbnails are generated only once when the user visits an image instance. I used a 'proxy' method to hide generated thumbnails from others users. 
