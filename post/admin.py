from django.contrib import admin
from .models import Post, Tag, Comment


class CommentInline(admin.TabularInline):
    """Inline admin for comments within post admin."""
    model = Comment
    extra = 1
    fields = ('author', 'content', 'created_at')
    readonly_fields = ('author', 'created_at')


class PostAdmin(admin.ModelAdmin):
    """Admin class for Post model."""
    list_display = ('title', 'author', 'created_at', 'tag_list', 'comment_count')
    list_filter = ('created_at', 'tags')
    search_fields = ('title', 'content', 'author__username')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    inlines = [CommentInline]
    fieldsets = (
        ('Post Information', {
            'fields': ('title', 'slug', 'content', 'image')
        }),
        ('Metadata', {
            'fields': ('author', 'tags', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

    def tag_list(self, obj):
        """Display tags in list view."""
        return ', '.join([tag.title for tag in obj.tags.all()])

    tag_list.short_description = 'Tags'

    def comment_count(self, obj):
        """Display comment count in list view."""
        return obj.comments.count()

    comment_count.short_description = 'Comments'


class TagAdmin(admin.ModelAdmin):
    """Admin class for Tag model."""
    list_display = ('title', 'post_count')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title',)

    def post_count(self, obj):
        """Display number of posts with this tag."""
        return obj.posts.count()

    post_count.short_description = 'Posts'


class CommentAdmin(admin.ModelAdmin):
    """Admin class for Comment model."""
    list_display = ('author', 'post', 'created_at', 'preview')
    list_filter = ('created_at', 'post')
    search_fields = ('author__username', 'content', 'post__title')
    readonly_fields = ('created_at', 'updated_at', 'author')
    fieldsets = (
        ('Comment Information', {
            'fields': ('post', 'author', 'content')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def preview(self, obj):
        """Display preview of comment content."""
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content

    preview.short_description = 'Content Preview'

    def save_model(self, request, obj, form, change):
        """Automatically set author to current user."""
        if not change:  # Only on creation
            obj.author = request.user
        super().save_model(request, obj, form, change)


# Register models
admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
