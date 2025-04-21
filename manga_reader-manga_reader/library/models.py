from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    published_date = models.DateField()
    isbn = models.CharField(max_length=13)
    description = models.TextField(blank=True, null=True, default="")
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    book = models.ForeignKey(Book, related_name='chapters', on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='chapters/pdfs/', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('book', 'number')
        ordering = ['number']

    def __str__(self):
        return f"Chapter {self.number}: {self.title}"

class ChapterImage(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='chapters/images/')

class Purchase(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.CharField(max_length=255)
    date_purchased = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user} - {self.book}"