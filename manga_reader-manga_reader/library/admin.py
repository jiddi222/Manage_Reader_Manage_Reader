from django.contrib import admin
from .models import Book, Purchase, Chapter, ChapterImage

admin.site.register(Book)
admin.site.register(Purchase)
admin.site.register(Chapter)
admin.site.register(ChapterImage)