"""bambu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth.models import User, Group
from AssetOptimizer import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^AssetOptimizer/', include('AssetOptimizer.urls')),
    url(r'^$',RedirectView.as_view(url='/AssetOptimizer/')),
    url(r'^userinfo', views.userinfo, name='userinfo'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = 'Asset Optimization'
admin.site.index_title = 'Asset Management'
admin.site.site_title = 'Asset Optimization Portal'
