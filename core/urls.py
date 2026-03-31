from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('post.urls'), name='post'),
    path('account/', include('account.urls'), name='account'),
]
