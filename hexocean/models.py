from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User

class Img(models.Model):
    from .validators import validate_file_extension
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="imgs", validators=[validate_file_extension])
    name = models.CharField(max_length=256)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return "/imgs/%i/" % self.id


class FullImg(Img):
    def __str__(self):
        return str(self.name)
    def get_absolute_url(self):
        return "/f_imgs/%i/" % self.id


class Thumb(Img):
    parentt = models.ForeignKey('Img', on_delete=models.CASCADE, null=True, blank=True, related_name="parent")
    height = models.IntegerField(null=True,  blank=True)
    def __str__(self):
        return str(self.name) + "_" + str(self.height)

    def get_absolute_url(self):
        return "/thumbs/%i/" % self.id


class AccountTier(models.Model):
    name = models.CharField(max_length=256)
    fetch_a_link_permission = models.BooleanField(default=False)
    original_img_permission = models.BooleanField(default=False)
    def __str__(self):
        return str(self.name)


class SizesList(models.Model):
    AccountTier = models.ForeignKey('AccountTier', on_delete=models.CASCADE)
    Size = models.ForeignKey('Size', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.AccountTier) + " " + str(self.Size)


class Size(models.Model):
    height = models.IntegerField(default=200,  validators=[MinValueValidator(50), MaxValueValidator(3000)])
    def __str__(self):
        return str(self.height)


class Link(models.Model):
    import uuid as uuid
    Image = models.ForeignKey("Img",  on_delete=models.CASCADE)
    data_add = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return str(self.Image.name)


class TmpLink(Link):
    seconds = models.IntegerField(default=300, validators=[MinValueValidator(300), MaxValueValidator(3000)])

    def __str__(self):
        return "tmp_" + str(self.Image.name)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    AccountTier = models.ForeignKey('AccountTier', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user.__str__())


from django.db.models.signals import post_save
from django.dispatch import receiver
# create and save profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        basic_tier = AccountTier.objects.get(name="Basic")
        Profile.objects.create(user=instance, AccountTier=basic_tier)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.profile:
        instance.profile.save()