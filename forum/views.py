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
from .models import Post, Like, Report
from main.models import Restaurant, Food
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.shortcuts import render, redirect
from .models import Post, Restaurant
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Post
from main.models import Restaurant
from django.contrib.auth.decorators import login_required
def show_post(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    user_liked_posts = []
    if request.user.is_authenticated:
        user_liked_posts = Like.objects.filter(user=request.user).values_list('post_id', flat=True)

    context = {
        'page_obj': page_obj,
        'user_liked_posts': user_liked_posts,
    }
    return render(request, 'show_post.html', context)



@login_required
def add_post(request):
    if request.method == 'POST':
        user = User.objects.get(username='Kaindra')

        restaurant_id = request.POST.get('restaurant_id')
        restaurant_name = request.POST.get('restaurant_name')
        text = request.POST.get('text')
        image = request.FILES.get('image')

        # Validate the restaurant selection
        if restaurant_id:
            try:
                restaurant = Restaurant.objects.get(id=restaurant_id)
            except Restaurant.DoesNotExist:
                # Handle the case where the restaurant ID is invalid
                return render(request, 'add_post.html', {'error': 'Invalid restaurant selected.'})
        else:
            # Handle the case where no restaurant is selected
            return render(request, 'add_post.html', {'error': 'Please select a restaurant from the list.'})

        # Create the new post
        post = Post.objects.create(
            user=user,
            restaurant=restaurant,
            text=text,
            image=image,
        )

        return redirect(reverse('forum:show_post'))  # Adjust the URL name as per your urls.py
    else:
        return render(request, 'add_post.html')


# forum/views.py
from django.http import JsonResponse

@require_POST
def like_post(request):
    data = json.loads(request.body)
    post_id = data.get('post_id')
    post = get_object_or_404(Post, id=post_id)

    user = User.objects.get(username='Kaindra')
    if not user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'User not authenticated'})

    liked = Like.objects.filter(post=post, user=user).exists()

    if liked:
        # Remove the like
        Like.objects.filter(post=post, user=user).delete()
        liked = False
    else:
        # Add a like
        Like.objects.create(post=post, user=user)
        liked = True

    return JsonResponse({'success': True, 'liked': liked})


def comment_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get('post_id')
        comment_text = data.get('comment')
        user = User.objects.get(username='tes')  # Use the first user as the commenter

        if post_id and comment_text:
            post = get_object_or_404(Post, id=post_id)
            comment = Comment.objects.create(post=post, user=user, text=comment_text)
            return JsonResponse({'success': True, 'username': user.username, 'comment': comment.text})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

def report_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get('post_id')
        reason = data.get('reason')
        user = request.user if request.user.is_authenticated else None

        # Pastikan pengguna terautentikasi
        if user is None:
            return JsonResponse({'success': False, 'error': 'Pengguna harus login untuk melaporkan postingan.'})

        # Ambil postingan yang akan dilaporkan
        post = get_object_or_404(Post, id=post_id)

        # Buat laporan baru
        Report.objects.create(post=post, reported_by=user, reason=reason)

        # Kembalikan respons berhasil
        return JsonResponse({'success': True, 'message': 'Postingan telah dilaporkan.'})
    
    return JsonResponse({'success': False, 'error': 'Metode permintaan tidak valid'})



@require_GET
def search_restaurants(request):
    query = request.GET.get('q', '')
    restaurants = Restaurant.objects.filter(nama__icontains=query).order_by('nama')[:10]
    results = []
    for restaurant in restaurants:
        results.append({'id': restaurant.id, 'nama': restaurant.nama})
    return JsonResponse({'restaurants': results})
