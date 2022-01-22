from django.contrib import admin
from .models import Post, Category, PostCategory, Author, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('post_header', 'id_author', 'categories', 'post_type', 'post_rating', 'post_created')
    list_filter = ('post_header', 'id_author')
    search_fields = ('post_header', 'post_text')

    def categories(self, obj):
        return "\n".join(obj.id_post_category.values_list('category_name', flat=True))

class CommentAdmin(admin.ModelAdmin):
    list_display = ('id_post', 'id_user', 'comment_text', 'comment_created', 'comment_rating')
    list_filter = ('id_post', 'comment_text')
    search_fields = ('id_post', 'comment_text')

class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('id_post', 'id_category')

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'author_rating')


# Register your models here.
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Comment, CommentAdmin)
