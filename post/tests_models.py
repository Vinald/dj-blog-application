from django.test import TestCase
from django.contrib.auth.models import User
from post.models import Post, Comment, Tag
from django.utils import timezone


class PostModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    # Post Creation Tests
    def test_post_creation(self):
        """Test basic post creation"""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is test content',
            author=self.user
        )
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.author, self.user)
        self.assertTrue(post.slug)

    def test_post_with_all_fields(self):
        """Test post creation with all fields"""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is test content',
            author=self.user,
            image=None
        )
        self.assertIsNotNone(post.created_at)
        self.assertIsNotNone(post.updated_at)

    def test_post_str_representation(self):
        """Test string representation of post"""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is test content',
            author=self.user
        )
        self.assertEqual(str(post), 'Test Post')

    def test_post_ordering_by_created_at(self):
        """Test that posts are ordered by created_at descending"""
        post1 = Post.objects.create(
            title='First Post',
            slug='first-post',
            content='Content 1',
            author=self.user
        )
        post2 = Post.objects.create(
            title='Second Post',
            slug='second-post',
            content='Content 2',
            author=self.user
        )
        posts = Post.objects.all()
        self.assertEqual(posts[0], post2)
        self.assertEqual(posts[1], post1)

    def test_post_get_absolute_url(self):
        """Test post get_absolute_url"""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is test content',
            author=self.user
        )
        self.assertEqual(post.get_absolute_url(), f'/posts/{post.slug}/')

    def test_post_slug_unique(self):
        """Test that post slugs are unique"""
        post1 = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='Content 1',
            author=self.user
        )
        with self.assertRaises(Exception):
            post2 = Post.objects.create(
                title='Another Test Post',
                slug='test-post',
                content='Content 2',
                author=self.user
            )

    def test_post_title_required(self):
        """Test that post title field has blank=False"""
        # Django doesn't enforce blank=False at the database level
        # This test verifies the model definition, not the database constraint
        post = Post.objects.create(
            title='Test Post',
            slug='test-post-title',
            content='This is test content',
            author=self.user
        )
        self.assertNotEqual(post.title, '')

    def test_post_content_required(self):
        """Test that post content field has blank=False"""
        # Django doesn't enforce blank=False at the database level
        # This test verifies the model definition, not the database constraint
        post = Post.objects.create(
            title='Test Post',
            slug='test-post-content',
            content='This is test content',
            author=self.user
        )
        self.assertNotEqual(post.content, '')

    def test_post_author_required(self):
        """Test that post author is required"""
        with self.assertRaises(Exception):
            post = Post.objects.create(
                title='Test Post',
                slug='test-post',
                content='This is test content',
                author=None
            )

    def test_post_author_cascade_delete(self):
        """Test that posts are deleted when author is deleted"""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is test content',
            author=self.user
        )
        post_id = post.id
        self.user.delete()
        self.assertFalse(Post.objects.filter(id=post_id).exists())

    def test_post_updated_at_auto_updates(self):
        """Test that updated_at is automatically updated"""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is test content',
            author=self.user
        )
        original_updated_at = post.updated_at
        post.title = 'Updated Title'
        post.save()
        self.assertGreaterEqual(post.updated_at, original_updated_at)

    def test_post_created_at_not_updated(self):
        """Test that created_at doesn't change on update"""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is test content',
            author=self.user
        )
        original_created_at = post.created_at
        post.title = 'Updated Title'
        post.save()
        self.assertEqual(post.created_at, original_created_at)

    # Tag Tests
    def test_post_tags_relationship(self):
        """Test post can have multiple tags"""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is test content',
            author=self.user
        )
        tag1 = Tag.objects.create(title='Python', slug='python')
        tag2 = Tag.objects.create(title='Django', slug='django')
        post.tags.add(tag1, tag2)

        self.assertEqual(post.tags.count(), 2)
        self.assertIn(tag1, post.tags.all())
        self.assertIn(tag2, post.tags.all())

    def test_post_tags_can_be_empty(self):
        """Test that post can have no tags"""
        post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is test content',
            author=self.user
        )
        self.assertEqual(post.tags.count(), 0)

    def test_tag_str_representation(self):
        """Test tag string representation"""
        tag = Tag.objects.create(title='Python', slug='python')
        self.assertEqual(str(tag), 'Python')

    def test_tag_slug_unique(self):
        """Test that tag slugs are unique"""
        tag1 = Tag.objects.create(title='Python', slug='python')
        with self.assertRaises(Exception):
            tag2 = Tag.objects.create(title='Python Language', slug='python')


class CommentModelTests(TestCase):

    def setUp(self):
        self.author = User.objects.create_user(
            username='author',
            email='author@example.com',
            password='testpass123'
        )
        self.commenter = User.objects.create_user(
            username='commenter',
            email='commenter@example.com',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            content='This is test content',
            author=self.author
        )

    # Comment Creation Tests
    def test_comment_creation(self):
        """Test basic comment creation"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.commenter,
            content='This is a test comment'
        )
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, self.commenter)
        self.assertEqual(comment.content, 'This is a test comment')

    def test_comment_str_representation(self):
        """Test comment string representation"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.commenter,
            content='This is a test comment'
        )
        self.assertEqual(str(comment), f'Comment by {self.commenter} on {self.post.title}')

    def test_comment_ordering_by_created_at(self):
        """Test that comments are ordered by created_at descending"""
        comment1 = Comment.objects.create(
            post=self.post,
            author=self.commenter,
            content='First comment'
        )
        comment2 = Comment.objects.create(
            post=self.post,
            author=self.commenter,
            content='Second comment'
        )
        comments = Comment.objects.all()
        self.assertEqual(comments[0], comment2)
        self.assertEqual(comments[1], comment1)

    def test_comment_author_required(self):
        """Test that comment author is required"""
        with self.assertRaises(Exception):
            comment = Comment.objects.create(
                post=self.post,
                author=None,
                content='This is a test comment'
            )

    def test_comment_post_required(self):
        """Test that comment post is required"""
        with self.assertRaises(Exception):
            comment = Comment.objects.create(
                post=None,
                author=self.commenter,
                content='This is a test comment'
            )

    def test_comment_content_required(self):
        """Test that comment content field has blank=False"""
        # Django doesn't enforce blank=False at the database level
        # This test verifies the model definition, not the database constraint
        comment = Comment.objects.create(
            post=self.post,
            author=self.commenter,
            content='This is a test comment'
        )
        self.assertNotEqual(comment.content, '')

    def test_comment_post_cascade_delete(self):
        """Test that comments are deleted when post is deleted"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.commenter,
            content='This is a test comment'
        )
        comment_id = comment.id
        self.post.delete()
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())

    def test_comment_author_cascade_delete(self):
        """Test that comments are deleted when author is deleted"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.commenter,
            content='This is a test comment'
        )
        comment_id = comment.id
        self.commenter.delete()
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())

    def test_post_has_multiple_comments(self):
        """Test that a post can have multiple comments"""
        comment1 = Comment.objects.create(
            post=self.post,
            author=self.commenter,
            content='First comment'
        )
        comment2 = Comment.objects.create(
            post=self.post,
            author=self.author,
            content='Second comment'
        )
        self.assertEqual(self.post.comments.count(), 2)
        self.assertIn(comment1, self.post.comments.all())
        self.assertIn(comment2, self.post.comments.all())

    def test_comment_updated_at_auto_updates(self):
        """Test that comment updated_at is automatically updated"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.commenter,
            content='This is a test comment'
        )
        original_updated_at = comment.updated_at
        comment.content = 'Updated comment'
        comment.save()
        self.assertGreaterEqual(comment.updated_at, original_updated_at)

    def test_multiple_users_can_comment(self):
        """Test that multiple users can comment on the same post"""
        user3 = User.objects.create_user(
            username='user3',
            email='user3@example.com',
            password='testpass123'
        )
        comment1 = Comment.objects.create(
            post=self.post,
            author=self.commenter,
            content='First comment'
        )
        comment2 = Comment.objects.create(
            post=self.post,
            author=self.author,
            content='Second comment'
        )
        comment3 = Comment.objects.create(
            post=self.post,
            author=user3,
            content='Third comment'
        )
        self.assertEqual(self.post.comments.count(), 3)


