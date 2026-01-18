from django.contrib import admin
from django.urls import path, include
from users import views as user_views

urlpatterns = [
    
]


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),
    path('register/', user_views.register, name='register'),
    # path('login/', user_views.login_view, name='login'),
    # path('logout/', user_views.logout_view, name='logout'),
]
