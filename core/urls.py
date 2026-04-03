from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('post.urls'), name='post'),
    path('account/', include('account.urls'), name='account'),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Error handlers
handler403 = TemplateView.as_view(template_name='403.html')
handler404 = TemplateView.as_view(template_name='404.html')
handler500 = TemplateView.as_view(template_name='500.html')
