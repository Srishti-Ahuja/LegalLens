from django.urls import path
from .views import UploadView, ChatView, CompareView

urlpatterns = [
    path('upload/', UploadView.as_view(), name='api-upload'),
    path('chat/', ChatView.as_view(), name='api-chat'),
    path('compare/', CompareView.as_view(), name='api-compare'),
]
