from django.contrib import admin
from .models import Post
@admin.register(Post)
class Postadmin(admin.ModelAdmin):
    list_display = [
        'title',
        'slug',
        'author',
        'published',
        'status'
    ]
    list_filter = ['status', 'created', 'published', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'published'
    ordering = ['status', 'published']
    show_facets = admin.ShowFacets.ALWAYS
# Register your models here.
