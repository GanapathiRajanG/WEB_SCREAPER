from django.contrib import admin
from .models import ScrapedData


@admin.register(ScrapedData)
class ScrapedDataAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'created_at', 'scraped_at')
    list_filter = ('created_at', 'scraped_at')
    search_fields = ('title', 'url', 'description')
    readonly_fields = ('created_at', 'scraped_at')

    fieldsets = (
        ('Metadata', {
            'fields': ('title', 'description', 'keywords', 'url', 'scraped_at', 'created_at')
        }),
        ('Content', {
            'fields': ('headings', 'bold_texts', 'important_paragraphs', 'images', 'links'),
            'classes': ('collapse',)
        }),
    )
