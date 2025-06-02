from django.db import models
from django.utils import timezone


class ScrapedData(models.Model):
    # Metadata fields
    title = models.CharField(max_length=500, blank=True)
    description = models.TextField(blank=True)
    keywords = models.TextField(blank=True)
    url = models.URLField(max_length=2000)
    scraped_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now)

    # Content fields stored as JSON
    headings = models.JSONField(default=list)  # List of {"text": str, "level": int}
    bold_texts = models.JSONField(default=list)  # List of strings
    important_paragraphs = models.JSONField(default=list)  # List of strings
    images = models.JSONField(default=list)  # List of {"src": str, "alt": str}
    links = models.JSONField(default=list)  # List of {"text": str, "href": str}

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Scraped Data"
        verbose_name_plural = "Scraped Data"

    def __str__(self):
        return f"{self.title or 'No Title'} - {self.url}"

    def get_content_dict(self):
        """Return content in the same format as the original Flask app"""
        return {
            "headings": self.headings,
            "bold_texts": self.bold_texts,
            "important_paragraphs": self.important_paragraphs,
            "images": self.images,
            "links": self.links
        }

    def get_metadata_dict(self):
        """Return metadata in the same format as the original Flask app"""
        return {
            "title": self.title,
            "description": self.description,
            "keywords": self.keywords,
            "url": self.url,
            "scraped_at": self.scraped_at
        }
