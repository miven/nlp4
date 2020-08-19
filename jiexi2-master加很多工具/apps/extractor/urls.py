from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'extractor',views.PolicyExtractorService.as_view()),
]
