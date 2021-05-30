from django.contrib import admin
from .models import *



class ImgAdmin(admin.ModelAdmin):
    fields = ["image", "name", "user"]


class ThumbAdmin(admin.ModelAdmin):
    fields = ["image", "name", "user", "parentt", "height"]

class FullImgAdmin(admin.ModelAdmin):
    fields = ["image", "name", "user"]


class AccountTierAdmin(admin.ModelAdmin):
    fields = ["name", "fetch_a_link_permission",  "original_img_permission"]


class SizesListAdmin(admin.ModelAdmin):
    fields = ["AccountTier", "Size"]


class SizeAdmin(admin.ModelAdmin):
    fields = ["height"]


class LinkAdmin(admin.ModelAdmin):
    fields = ["Image",  "seconds"]


class ProfileAdmin(admin.ModelAdmin):
    fields = ["user", "AccountTier"]


admin.site.register(Img, ImgAdmin)
admin.site.register(Thumb, ThumbAdmin)
admin.site.register(FullImg, FullImgAdmin)
admin.site.register(AccountTier, AccountTierAdmin)
admin.site.register(SizesList, SizesListAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(TmpLink, LinkAdmin)
admin.site.register(Profile, ProfileAdmin)

