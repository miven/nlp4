from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^tokenizer', views.DocTokenizerService.as_view()),
]