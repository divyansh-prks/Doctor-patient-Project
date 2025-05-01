from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('div/', views.home),
    path('voice-to-text/', views.voice_to_text),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


