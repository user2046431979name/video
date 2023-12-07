from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/',SignUp.as_view(),name='signup'),
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('series/<int:id>',series,name='series'),
    path('video/<int:id>',detailVideo,name='video'),
    path('allvideo/',allVideos,name='all_videos'),
    path('contact/',contact,name='contact'),
    path('profile/',profile,name='profile'),


]

urlpatterns += static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)
