from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Post title',
        })
    )
    slug = forms.SlugField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'post-slug-url',
            'help_text': 'URL-friendly version of the title'
        })
    )
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Write your post content here...',
            'rows': 8,
        })
    )

    class Meta:
        model = Post
        fields = ['title', 'slug', 'content']

    def clean_slug(self):
        slug = self.cleaned_data.get('slug')
        if Post.objects.filter(slug=slug).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This slug is already in use. Please use a different one.')
        return slug

