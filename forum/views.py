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
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

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
        likes = Like.objects.all()
        data = serializers.serialize('json', likes)
        return HttpResponse(data, content_type="application/json")
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed."}, status=405)


def comment_json(request):
    if request.method == 'GET':
        comments = Comment.objects.all()
        data = serializers.serialize('json', comments)
        return HttpResponse(data, content_type="application/json")
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed."}, status=405)


def report_json(request):
    if request.method == 'GET':
        reports = Report.objects.all()
        data = serializers.serialize('json', reports)
        return HttpResponse(data, content_type="application/json")
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed."}, status=405)


def restaurant_json(request):
    if request.method == 'GET':
        restaurants = Restaurant.objects.all()
        data = serializers.serialize('json', restaurants)
        return HttpResponse(data, content_type="application/json")
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed."}, status=405)


@csrf_exempt
def create_post_flutter(request):
    print("Masuk")
    if request.method == 'POST':
        try:
            text = request.POST.get('text')
            restaurant_id = request.POST.get('restaurant_id')

            # Validasi atau cari instance Restaurant
            restaurant = None
            if restaurant_id:
                try:
                    restaurant = Restaurant.objects.get(id=restaurant_id)
                except Restaurant.DoesNotExist:
                    print(f"Restaurant with id {restaurant_id} not found. Proceeding without restaurant.")

            # Buat Post baru
            default_user, _ = User.objects.get_or_create(id=999, defaults={'username': 'default_user'})
            user = request.user if request.user.is_authenticated else default_user
            print('User ', user)
            post = Post.objects.create(
                user=user,
                text=text,
                restaurant=restaurant  # Bisa None jika tidak ditemukan
            )

            # Response JSON
            return JsonResponse({
                'status': 'success',
                'message': 'Post created successfully.',
                'post': {
                    'id': post.id,
                    'text': post.text,
                    'restaurant': restaurant.nama if restaurant else None,
                    'created_at': post.created_at.isoformat(),
                }
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e),
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed.'
    }, status=405)

@csrf_exempt
def like_post_flutter(request):
    """
    Menerima POST dengan body:
      {
        'post_id': <ID dari Post>
      }
    Mengembalikan JSON:
      {
        'status': 'success',
        'liked': True/False,
        'like_count': <updated like count>
      }
    """
    if request.method == 'POST':
        try:
            # Dapatkan data. Flutter biasanya mengirim lewat request.body atau request.POST
            data = request.POST or json.loads(request.body)
            post_id = data.get('post_id')

            if not post_id:
                return JsonResponse({
                    'status': 'error',
                    'message': 'post_id is required'
                }, status=400)

            post = get_object_or_404(Post, id=post_id)

            # Jika user tidak login, gunakan default_user
            if request.user.is_authenticated:
                current_user = request.user
            else:
                # fallback user default
                default_user, _ = User.objects.get_or_create(
                    id=999, 
                    defaults={'username': 'default_user'}
                )
                current_user = default_user

            # Cek apakah user sudah pernah like
            liked_obj = Like.objects.filter(post=post, user=current_user).first()

            if liked_obj:
                # Sudah like -> un-like
                liked_obj.delete()
                liked = False
            else:
                # Belum like -> tambahkan
                Like.objects.create(post=post, user=current_user)
                liked = True

            # Hitung jumlah like terbaru
            like_count = Like.objects.filter(post=post).count()

            return JsonResponse({
                'status': 'success',
                'liked': liked,
                'like_count': like_count
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed'
        }, status=405)

@csrf_exempt
def comment_post_flutter(request):
    """
    Menerima POST dengan body:
      {
        'post_id': <ID dari Post>,
        'comment': <Isi komentar>
      }
    Mengembalikan JSON:
      {
        'status': 'success',
        'username': <username atau 'default_user'>,
        'comment': <isi komentar>,
        'post_id': <ID post>,
        'comment_count': <comment count baru>
      }
    """
    if request.method == 'POST':
        try:
            data = request.POST
            post_id = data.get('post_id')
            comment_text = data.get('comment')

            if not post_id or not comment_text:
                return JsonResponse({
                    'status': 'error',
                    'message': 'post_id and comment are required'
                }, status=400)

            post = get_object_or_404(Post, id=post_id)

            # Jika user tidak login, gunakan default_user
            if request.user.is_authenticated:
                current_user = request.user
            else:
                default_user, _ = User.objects.get_or_create(
                    id=999, 
                    defaults={'username': 'default_user'}
                )
                current_user = default_user

            # Buat komentar baru
            comment = Comment.objects.create(
                post=post,
                user=current_user,
                text=comment_text
            )

            # Hitung comment terbaru
            comment_count = Comment.objects.filter(post=post).count()

            return JsonResponse({
                'status': 'success',
                 'comment': {
                'model': 'forum.comment',
                'pk': comment.id,
                'fields': {
                    'post': post.id,
                    'user': current_user.id,
                    'text': comment.text,
                    'created_at': comment.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
                }
            },
            'comment_count': comment_count
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed'
        }, status=405)


# -------------------------------------------
# REPORT POST (Flutter)
# -------------------------------------------
@csrf_exempt
def report_post_flutter(request):
    """
    Menerima POST dengan body:
      {
        'post_id': <ID dari Post>,
        'reason': <Alasan report>
      }
    Mengembalikan JSON:
      {
        'status': 'success',
        'message': 'Postingan telah dilaporkan.'
      }
    """
    if request.method == 'POST':
        try:
            data = request.POST or json.loads(request.body)
            post_id = data.get('post_id')
            reason = data.get('reason')

            if not post_id or not reason:
                return JsonResponse({
                    'status': 'error',
                    'message': 'post_id and reason are required'
                }, status=400)

            post = get_object_or_404(Post, id=post_id)

            # Jika user tidak login, gunakan default_user
            if request.user.is_authenticated:
                current_user = request.user
            else:
                default_user, _ = User.objects.get_or_create(
                    id=999, 
                    defaults={'username': 'default_user'}
                )
                current_user = default_user

            # Buat laporan
            Report.objects.create(
                post=post,
                reported_by=current_user,
                reason=reason
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Postingan telah dilaporkan.'
            })

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Method not allowed'
        }, status=405)


def get_all_users(request):
    """
    Returns a list of all users with their IDs and usernames.
    """
    if request.method == 'GET':

        users = User.objects.all()
        user_data = [
            {
                'id': user.id,
                'username': user.username,
            }
            for user in users
        ]
        return JsonResponse({'users': user_data}, status=200)

def get_all_users(request):
    """
    Returns a list of all users with their IDs and usernames.
    """
    if request.method == 'GET':

        users = User.objects.all()
        user_data = [
            {
                'id': user.id,
                'username': user.username,
            }
            for user in users
        ]
        return JsonResponse({'users': user_data}, status=200)

# def get_all_users(request):
#     if request.method == 'GET':
#         users = User.objects.all()
#         data = serializers.serialize('json', users)
#         return HttpResponse(data, content_type="application/json")
#     else:
#         return JsonResponse({"status": "error", "message": "Method not allowed."}, status=405)
@csrf_exempt
def edit_comment_flutter(request):
    if request.method == "POST":
        comment_id = request.POST.get("comment_id")
        new_text = request.POST.get("text")

        if not comment_id or not new_text:
            return JsonResponse({"status": "error", "message": "Invalid input."})

        # Get the comment
        comment = get_object_or_404(Comment, pk=comment_id)

        # Check if the logged-in user is the owner of the comment
        if comment.user != request.user:
            return JsonResponse({"status": "error", "message": "Unauthorized."})

        # Update the comment
        comment.text = new_text
        comment.save()

        return JsonResponse({
            "status": "success",
            "message": "Comment updated successfully.",
            "new_comment": {
                "id": comment.id,
                "text": comment.text,
                "post": comment.post.id,
                "user": comment.user.id,
            },
        })

    return JsonResponse({"status": "error", "message": "Invalid request method."})

@csrf_exempt
def delete_post_flutter(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")

        if not post_id:
            return JsonResponse({"status": "error", "message": "Post ID is required."})

        # Get the post
        post = get_object_or_404(Post, pk=post_id)

        # Check if the logged-in user is the owner of the post
        if post.user != request.user:
            return JsonResponse({"status": "error", "message": "Unauthorized."})

        # Delete the post
        post.delete()

        return JsonResponse({"status": "success", "message": "Post deleted successfully."})

    return JsonResponse({"status": "error", "message": "Invalid request method."})

@csrf_exempt
def like_post_flutter(request):
    if request.method == 'POST':
        try:
            # Log the incoming request body for debugging
            print(f"Request Body: {request.body}")

            # Attempt to parse the JSON data
            # data = json.loads(request.body)
            post_id = request.POST.get('post_id')
            
            # Ensure user is authenticated
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"status": "error", "message": "User not authenticated."}, status=401)

            # Validate post ID
            try:
                post = Post.objects.get(pk=post_id)
            except Post.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Post not found."}, status=404)

            # Handle the like toggle logic
            like, created = Like.objects.get_or_create(post=post, user=user)
            if not created:
                like.delete()
                liked = False
            else:
                liked = True

            return JsonResponse({
                "status": "success",
                "liked": liked,
                "like_count": post.likes.count()
            })

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON payload."}, status=400)
        except Exception as e:
            return JsonResponse({"status": "error", "message": f"Unexpected error: {str(e)}"}, status=500)
    else:
        return JsonResponse({"status": "error", "message": "Method not allowed."}, status=405)