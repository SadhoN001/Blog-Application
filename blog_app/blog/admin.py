from django.contrib import admin
from . models import Tag, Post, Comment
# Register your models here.

class TagAdmin(admin.ModelAdmin):
    list_display= ['name']
    
admin.site.register(Tag, TagAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display=['title', 'content', 'status', 'featured_img', 'created_at', 'updated_at', 'author' ]
    
admin.site.register(Post, PostAdmin)

class CommentAdmin(admin.ModelAdmin):
    list_display=('body', 'post', 'user', 'created_at', 'updated_at')
    
admin.site.register(Comment, CommentAdmin)