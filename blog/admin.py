from django.contrib import admin
from .models import Category, Tag, Post


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_time', 'modified_time', 'category', 'author')
    ordering = ('id',)
    fields = ['title', 'body', 'excerpt', 'category', 'tags']

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)



