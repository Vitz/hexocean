from django.contrib.auth.models import User, Group
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone
from rest_framework import serializers
from .models import *


class LinkSerializer(serializers.ModelSerializer):
    expired = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()

    class Meta:
        model = TmpLink
        fields = ['pk', 'Image',  'seconds',  'link', 'expired']

    def get_expired(self, obj):
        t_add = obj.data_add
        t_now = timezone.localtime()
        sec = (t_now - t_add).seconds
        return sec > obj.seconds


    def get_link(self, obj):
        from django.urls import reverse
        from django.contrib.sites.models import Site
        domain = Site.objects.get_current().domain
        tmp_url = reverse('get_temp_url', args=(obj.uuid,))
        url = 'http://{domain}{path}'.format(domain=domain, path=tmp_url)
        return url


class ThumbSerializer(serializers.ModelSerializer):
    class Meta:
        model = Thumb
        fields = ['name', 'image']


class ImagesSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()

    def get_details(self, obj):
        obj_url = obj.get_absolute_url()
        return self.context["request"].build_absolute_uri(obj_url)

    class Meta:
        model = FullImg
        fields = ['pk', 'name', 'details']


class CreateImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullImg
        fields = ['image', 'name']


class SingleImageSerializer(serializers.ModelSerializer):
    thumbs = serializers.SerializerMethodField('thumbs_urls')
    full_img = serializers.SerializerMethodField('full_img_url')

    def thumbs_urls(self, item):
        from django.urls import reverse
        from django.contrib.sites.models import Site
        domain = Site.objects.get_current().domain

        owner = item.user
        profile = Profile.objects.get(user=owner)
        tier = profile.AccountTier
        s_lists = SizesList.objects.filter(AccountTier=tier)
        urls = {}
        for size_list in s_lists:
            img = self.get_thumb(item, size_list.Size.height)
            link_obj = self.get_url(img)
            link_url = reverse('get_thumb_url', args=(link_obj.uuid,))
            full_url = 'http://{domain}{path}'.format(domain=domain, path=link_url)
            urls[size_list.Size.height] = full_url
        return urls

    def full_img_url(self, item:Img):
        owner = item.user
        profile = Profile.objects.get(user=owner)
        tier = profile.AccountTier
        if tier.original_img_permission:
            ss_url = item.image.url
            from django.contrib.sites.models import Site
            domain = Site.objects.get_current().domain
            url = 'http://{domain}{path}'.format(domain=domain, path=ss_url)
            return url
        else:
            return "Upgrade your account"

    class Meta:
            model = FullImg
            fields = ['name', 'thumbs', 'full_img']


    def resize(self, item:Img, height):
        from PIL import Image
        from io import BytesIO, StringIO
        image = Image.open(item.image)
        old_w, old_h = image.size
        new_size = int(old_w/(old_h/int(height))), int(height)
        name = str(height) + "_" + item.name + ".JPEG"

        im = Image.open(item.image)
        tempfile = im.convert('RGB')
        tempfile = tempfile.resize(new_size, Image.ANTIALIAS)
        tempfile_io = BytesIO()
        tempfile.save(tempfile_io, format='JPEG')
        image_file = InMemoryUploadedFile(tempfile_io, None, name, 'image/jpeg', tempfile_io.__sizeof__(), None)
        th = Thumb(user=item.user)
        th.image.save(name, image_file)
        th.name = name
        th.height = height
        th.parentt = item
        th.save()
        return th


    def get_thumb(self, item, height):
        try:
            img = Thumb.objects.get(parentt=item, height=height)
            return img
        except:
            return self.resize(item, height)

    def get_url(self, img):
        try:
            return Link.objects.get(Image=img)
        except:
            link = Link(Image=img)
            link.save()
            return link



