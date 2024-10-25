from django.db import models
from django.contrib.auth.models import User
from main.models import Restaurant
# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    like_count = models.PositiveIntegerField(default=0)  
    comment_count = models.PositiveIntegerField(default=0)  
    share_count = models.PositiveIntegerField(default=0)  
    report_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.SET_NULL, null=True, blank=True)

class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Report(models.Model):
    ALASAN_LAPORAN = [
        ('Konten Tidak Pantas', 'Konten Tidak Pantas'),
        ('Spam atau Iklan', 'Spam atau Iklan'),
        ('Bahasa Kasar atau Menyinggung', 'Bahasa Kasar atau Menyinggung'),
        ('Misinformasi', 'Misinformasi'),
        ('Topik Tidak Relevan', 'Topik Tidak Relevan'),
    ]
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=50, choices=ALASAN_LAPORAN)
    created_at = models.DateTimeField(auto_now_add=True)