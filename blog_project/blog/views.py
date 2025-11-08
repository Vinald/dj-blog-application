from django.shortcuts import render

POSTS = [
    {
        "author": "Alice",
        "title": "First Post",
        "content": "This is the first post.",
        "date_posted": "2024-01-01",
    },
    {
        "author": "Bob",
        "title": "Second Post",
        "content": "This is the second post.",
        "date_posted": "2024-01-02",
    },
    {
        "author": "Charlie",
        "title": "Third Post",
        "content": "This is the third post.",
        "date_posted": "2024-01-03",
    },
    {
        "author": "Diana",
        "title": "Fourth Post",
        "content": "This is the fourth post.",
        "date_posted": "2024-01-04",
    },
]


def home(request):
    context = {"posts": POSTS,
               'title': "Home"}
    return render(request, "blog/home.html", context)


def about(request):
    context = {'title': 'About'}
    return render(request, "blog/about.html", context)
