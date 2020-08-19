from django.conf.urls import url
from . import views
'''
建立用个utils包,包括许多github上提供的nlp算法,可以根据需要继承到这个django里面.
'''
urlpatterns = [
    url(r'', views.DocTokenizerService.as_view()),
]