from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Like, Report
from main.models import Restaurant
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
import json

def show_post(request):
    posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(posts, 5)  # Show 5 posts per page
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

@login_required(login_url='/login/')
def add_post(request):
    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant_id')
        text = request.POST.get('text')
        image = request.FILES.get('image')

        restaurant = None

        if restaurant_id:
            try:
                restaurant = Restaurant.objects.get(id=restaurant_id)
            except Restaurant.DoesNotExist:
                return render(request, 'add_post.html', {'error': 'Invalid restaurant selected.'})

        # Create the new post with or without the restaurant
        post = Post.objects.create(
            user=request.user,
            restaurant=restaurant,  # This will be None if no restaurant is selected
            text=text,
            image=image,
        )

        return redirect(reverse('forum:show_post'))
    else:
        return render(request, 'add_post.html')


@require_POST
@login_required(login_url='/login/')
def like_post(request):
    data = json.loads(request.body)
    post_id = data.get('post_id')
    post = get_object_or_404(Post, id=post_id)

    liked = Like.objects.filter(post=post, user=request.user).exists()

    if liked:
        # Remove the like
        Like.objects.filter(post=post, user=request.user).delete()
        liked = False
    else:
        # Add a like
        Like.objects.create(post=post, user=request.user)
        liked = True

    return JsonResponse({'success': True, 'liked': liked})

@login_required(login_url='/login/')
def comment_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get('post_id')
        comment_text = data.get('comment')

        if post_id and comment_text:
            post = get_object_or_404(Post, id=post_id)
            comment = Comment.objects.create(post=post, user=request.user, text=comment_text)
            return JsonResponse({'success': True, 'username': request.user.username, 'comment': comment.text})

    return JsonResponse({'success': False, 'error': 'Invalid request'})

@login_required(login_url='/login/')
def report_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get('post_id')
        reason = data.get('reason')

        # Get the post to be reported
        post = get_object_or_404(Post, id=post_id)

        # Create a new report
        Report.objects.create(post=post, reported_by=request.user, reason=reason)

        # Return success response
        return JsonResponse({'success': True, 'message': 'Postingan telah dilaporkan.'})
    
    return JsonResponse({'success': False, 'error': 'Metode permintaan tidak valid'})

def search_restaurants(request):
    query = request.GET.get('q', '')
    restaurants = Restaurant.objects.filter(nama__icontains=query).order_by('nama')[:10]
    results = [{'id': restaurant.id, 'nama': restaurant.nama} for restaurant in restaurants]
    return JsonResponse({'restaurants': results})
