"""nlp_service URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin', admin.site.urls),
    path('policyService', include('matcher.urls')),
    path('package',include('word2vec.urls')),
    path('ocr2', include('ocr2.urls')),
    path('ocr',include('ocr.urls')),
    path('utils',include('someUtils.urls')),

    path('single',include('word2vec2.urls')),
    path('nlp/master', include('master.urls')),
    path('extractorService', include('extractor.urls')),
]








