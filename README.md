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
  
// I attached requirements.txt file but packages like django-thumbnails or django-imagekit hasnt been used, there is no need to install it.  
    
# Other
Most of image urls are hidden, but still achievable using static path dispatcher. Thumbnails are generated only once when user visit an imagle isntance. I used a 'proxy' method to hide generated thumnails from other users.  
