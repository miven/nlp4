from django.conf.urls import url
from . import views

urlpatterns = [

url(r'', views.Word2VecService.as_view()),
]
