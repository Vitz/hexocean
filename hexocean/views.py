from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response

from .serializers import *
from .models import *


def get_temp_url(request, uuid):
    from .models import TmpLink
    link = TmpLink.objects.get(uuid=uuid)
    t_add = link.data_add
    t_now = timezone.localtime()
    sec = (t_now - t_add).seconds
    expired = sec > link.seconds
    if not expired:
        return HttpResponse(link.Image.image, content_type="image/png")
    else:
        from rest_framework import status
        return Response({"error": "Expired"}, status=status.HTTP_423_LOCKED)


def get_thumb_url(request, uuid):
    from .models import Link
    link = Link.objects.get(uuid=uuid)
    if request.user == link.Image.user:
        return HttpResponse(link.Image.image, content_type="image/png")
    else:
        from django.http import HttpResponseForbidden
        return HttpResponseForbidden()


class LinkViewSet(viewsets.ModelViewSet):
    serializer_class = LinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        own_imgs = Img.objects.filter(user=self.request.user)
        return TmpLink.objects.filter(Image__in=own_imgs)

    def retrieve(self, request, *args, **kwargs):
        tmp_link = get_object_or_404(TmpLink, pk=kwargs['pk'])
        if tmp_link.Image.user == request.user:
            serializer = LinkSerializer(tmp_link)
            return Response(serializer.data)
        else:
            from rest_framework import status
            return Response({"error": "No permission, upgrade your account"}, status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        from rest_framework import status
        from rest_framework.response import Response

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = self.request.user
        profile = get_object_or_404(Profile, user=user)

        if profile.AccountTier.fetch_a_link_permission or user.is_superuser:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response({"error": "No permission, upgrade your account"}, status=status.HTTP_401_UNAUTHORIZED)

    def perform_create(self, serializer):
        serializer.save()


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = ImagesSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateImageSerializer
        elif self.action == 'retrieve':
            return SingleImageSerializer
        else:
            return self.serializer_class

    def get_queryset(self):
        return FullImg.objects.filter(user=self.request.user)

    def retrieve(self, request, pk):
        queryset = FullImg.objects.filter(user=self.request.user)
        image = get_object_or_404(queryset, pk=pk)
        serializer = SingleImageSerializer(image)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = CreateImageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        res = self.perform_create(serializer)
        from django.contrib.sites.models import Site
        domain = Site.objects.get_current().domain
        tmp_url = res.get_absolute_url()
        url = 'http://{domain}{path}'.format(domain=domain, path=tmp_url)
        return Response({"url":url})

    def perform_create(self, serializer):
        user = self.request.user
        return serializer.save(user=user)


class ThumbViewSet(viewsets.ModelViewSet):
    serializer_class = ThumbSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Thumb.objects.all()


