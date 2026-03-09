
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('accounts/', include('accounts.urls')),
    path('community/', include('community.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
