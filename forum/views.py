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
from .models import Post, Like

from django.contrib.auth.models import User
def show_post(request):
    posts = Post.objects.all().order_by('-created_at')
    
    # Get the first user in the database as the default user
    user = User.objects.first()
    
    # Get a list of post IDs liked by the user
    user_liked_posts = Like.objects.filter(user=user).values_list('post_id', flat=True)

    return render(request, 'show_post.html', {'posts': posts, 'user_liked_posts': user_liked_posts})

def add_post(request):
    if request.method == 'POST':
        text = request.POST.get('text')
        image = request.FILES.get('image')
        user = User.objects.first()  # Use the first user in the database for testing

        # Create a new Post object
        post = Post(user=user, text=text, image=image)
        post.save()

        return redirect('forum:show_post')  # Redirect to 'show_post' after saving the post

    return render(request, 'add_post.html')


# forum/views.py
from django.http import JsonResponse

def like_post(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get('post_id')
        post = get_object_or_404(Post, id=post_id)

        # Use a global user for development if the user is not authenticated
        user = request.user if request.user.is_authenticated else User.objects.first()

        # Check if the global user has already liked the post
        liked = Like.objects.filter(post=post, user=user).exists()

        if liked:
            # If already liked, remove the like
            Like.objects.filter(post=post, user=user).delete()
            post.like_count = max(post.like_count - 1, 0)
            liked = False
        else:
            # If not liked, add a new like
            Like.objects.create(post=post, user=user)
            post.like_count += 1
            liked = True

        # Save the updated like count
        post.save()

        # Return the updated like count
        return JsonResponse({'success': True, 'like_count': post.like_count, 'liked': liked})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

from django.http import JsonResponse

def post_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        post_id = data.get('post_id')
        comment_text = data.get('comment')
        user = User.objects.first()  # Use the first user as the commenter

        if post_id and comment_text:
            post = get_object_or_404(Post, id=post_id)
            comment = Comment.objects.create(post=post, user=user, text=comment_text)
            return JsonResponse({'success': True, 'username': user.username, 'comment': comment.text})

    return JsonResponse({'success': False, 'error': 'Invalid request'})
