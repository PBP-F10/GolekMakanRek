from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Like, Report
from main.models import Restaurant
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
import json
from django.core.serializers import serialize
from django.core import serializers

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
from django.http import HttpResponse

def search_restaurants(request):
    query = request.GET.get('q', '')
    restaurants = Restaurant.objects.filter(nama__icontains=query).order_by('nama')[:10]
    results = [{'id': restaurant.id, 'nama': restaurant.nama} for restaurant in restaurants]
    return JsonResponse({'restaurants': results})

# def post_json(request):
#     data = Post.objects.all()
#     return HttpResponse(serialize("json", data), content_type="application/json")

# # View for all Comments
# def comment_json(request):
#     data = Comment.objects.all()
#     return HttpResponse(serialize("json", data), content_type="application/json")

# # View for all Likes
# def like_json(request):
#     data = Like.objects.all()
#     return HttpResponse(serialize("json", data), content_type="application/json")

# # View for all Reports
# def report_json(request):
#     data = Report.objects.all()
#     return HttpResponse(serialize("json", data), content_type="application/json")


######### FLUTTER ########
# @csrf_exempt
def post_json(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        data = serializers.serialize('json', posts)
        return HttpResponse(data, content_type="application/json")
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed."}, status=405)

def like_json(request):
    if request.method == 'GET':
        posts = Like.objects.all()
        data = serializers.serialize('json', posts)
        return HttpResponse(data, content_type="application/json")
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed."}, status=405)


def comment_json(request):
    if request.method == 'GET':
        posts = Comment.objects.all()
        data = serializers.serialize('json', posts)
        return HttpResponse(data, content_type="application/json")
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed."}, status=405)


def report_json(request):
    if request.method == 'GET':
        posts = Report.objects.all()
        data = serializers.serialize('json', posts)
        return HttpResponse(data, content_type="application/json")
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed."}, status=405)



def create_post_flutter(request):
    if request.method == 'POST':
        try:
            #             username = request.POST['username']
            # password = request.POST['password']
            # Parse JSON body
            # data = json.loads(request.body.decode('utf-8'))
            # restaurant_id = data.get('restaurant_id')
            # restaurant_id = request.POST.get('restaurant_id')
            restaurant_id = False
            text = request.POST.get('text')
            # image = request.FILES.get('image')
            image = None

            restaurant = None

            if restaurant_id:
                try:
                    restaurant = Restaurant.objects.get(id=restaurant_id)
                except Restaurant.DoesNotExist:
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Invalid restaurant selected.'
                    }, status=400)

            # Create the new post with or without the restaurant
            post = Post.objects.create(
                user=request.user,
                restaurant=restaurant,  # This will be None if no restaurant is selected
                text=text,
                image=image,
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Post created successfully.',
                'post': {
                    'id': post.id,
                    'user': post.user.id,
                    'text': post.text,
                    'restaurant': post.restaurant.nama if post.restaurant else None,
                    'created_at': post.created_at.isoformat()
                }
            }, status=200)
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'An error occurred: {str(e)}'
            }, status=500)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed.'
        }, status=405)