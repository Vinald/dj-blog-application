from .models import Post


def session_processor(request):
    """
    Context processor to add session data to all templates.
    Provides recently viewed posts and other session info.
    Only show recently viewed posts to authenticated users.
    """
    context = {}

    # Only show recently viewed posts to authenticated users
    if request.user.is_authenticated:
        recently_viewed = request.session.get('recently_viewed', [])
        if recently_viewed:
            try:
                # Fetch the actual post objects in order
                recent_posts = []
                for post_id in recently_viewed:
                    post = Post.objects.get(id=post_id)
                    recent_posts.append(post)
                context['recently_viewed_posts'] = recent_posts
            except Post.DoesNotExist:
                context['recently_viewed_posts'] = []
        else:
            context['recently_viewed_posts'] = []
    else:
        context['recently_viewed_posts'] = []

    return context

