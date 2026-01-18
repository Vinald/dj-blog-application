from django.contrib import admin
from .models import Post


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "content", "date_posted")
    search_fields = ("title", "content", "author")
    list_filter = ("date_posted", "author")


admin.site.register(Post, PostAdmin)
