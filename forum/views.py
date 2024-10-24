from django.shortcuts import render, get_object_or_404
from .models import Post, Comment
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
import json
from django.http import JsonResponse
from random import sample
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def show_post(request):
    posts = Post.objects.all().order_by('-created_at')  # Mengambil semua postingan, diurutkan dari yang terbaru
    return render(request, 'show_post.html', {'posts': posts})


def add_post(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        image = request.FILES.get('image')
        user = User.objects.first()  # Menggunakan dummy user (pengguna pertama yang ditemukan di database)

        # Buat objek Post baru
        post = Post(user=user, text=text, image=image)
        post.save()

        return redirect('show_post')  # Kembali ke halaman daftar postingan setelah berhasil menambahkan

    return render(request, 'add_post.html')

