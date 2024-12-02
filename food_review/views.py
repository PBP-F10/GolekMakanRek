from .models                            import *
from .forms                             import *
from django.shortcuts                   import render, get_object_or_404
from django.http                        import JsonResponse
from django.contrib.auth.decorators     import login_required
from main.models                        import *
from django.utils                       import timezone
from django.http                        import JsonResponse
from django.contrib.auth.decorators     import login_required
from django.views.decorators.http       import require_http_methods
import logging
import json

TIME_ZONE = 'Asia/Jakarta'
USE_TZ = True
logger = logging.getLogger(__name__)

def restaurant_preview(request):
    restaurants = Restaurant.objects.all()  
    return render(request, 'show_detail.html', {'restaurants': restaurants})

def restaurant_detail(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    restaurant_foods = Food.objects.filter(restoran=restaurant)
    
    return render(request, 'food_list.html', {
        'restaurant': restaurant,
        'foods': restaurant_foods,
    })

@login_required(login_url='/login/')
def add_rating(request, food_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

    food = get_object_or_404(Food, id=food_id)
    score = request.POST.get('score')

    try:
        score = int(score)
        if not (1 <= score <= 5):
            raise ValueError
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid rating score'})

    rating, created = FoodRating.objects.update_or_create(
        user=request.user,
        deskripsi_food=food,
        defaults={'score': score}
    )

    new_average = food.average_rating

    return JsonResponse({
        'status': 'success',
        'message': 'Rating added successfully',
        'food_rating': new_average,
        'is_new': created
    })

@login_required(login_url='/login/')
def edit_rating(request, rating_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

    rating = get_object_or_404(FoodRating, id=rating_id, user=request.user)
    score = request.POST.get('score')

    try:
        score = int(score)
        if not (1 <= score <= 5):
            raise ValueError
    except ValueError:
        return JsonResponse({'status': 'error', 'message': 'Invalid rating score'})

    rating.score = score
    rating.save()


    new_average = rating.deskripsi_food.average_rating

    return JsonResponse({
        'status': 'success',
        'message': 'Rating updated successfully',
        'food_rating': new_average
    })

@login_required(login_url='/login/')
def delete_rating(request, rating_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

    rating = get_object_or_404(FoodRating, id=rating_id, user=request.user)
    food = rating.deskripsi_food
    rating.delete()

    new_average = food.average_rating

    return JsonResponse({
        'status': 'success',
        'message': 'Rating deleted successfully',
        'food_rating': new_average
    })

def get_user_rating(request, food_id):
    if not request.user.is_authenticated:
        return JsonResponse({'has_rating': False})

    food = get_object_or_404(Food, id=food_id)
    rating = FoodRating.objects.filter(user=request.user, deskripsi_food=food).first()

    if rating:
        return JsonResponse({
            'has_rating': True,
            'rating_id': rating.id,
            'rating': rating.score,
            'food_rating': food.average_rating
        })
    return JsonResponse({
        'has_rating': False,
        'food_rating': food.average_rating
    })

def get_comments(request, food_id):
    food = get_object_or_404(Food, id=food_id)
    ratings = FoodRating.objects.filter(deskripsi_food=food).exclude(comment__isnull=True).exclude(comment='').order_by('-waktu_comment')
    
    comments = []
    for rating in ratings:
        comments.append({
            'username': rating.user.username,
            'comment': rating.comment,
            'formatted_time': rating.waktu_comment.strftime("%B %d, %Y %I:%M %p")
        })
    
    return JsonResponse({'comments': comments})

@login_required(login_url='/login/')
def add_comment(request, food_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
    
    try:
        data = json.loads(request.body)
        comment = data.get('comment', '').strip()
        
        if not comment:
            return JsonResponse({'status': 'error', 'message': 'Comment cannot be empty'})
        
        food = get_object_or_404(Food, id=food_id)
        
        rating, created = FoodRating.objects.get_or_create(
            user=request.user,
            deskripsi_food=food,
            defaults={'score': 3}
        )
        
        rating.comment = comment
        rating.waktu_comment = timezone.now()
        rating.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Comment added successfully'
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@require_http_methods(["POST"])
@login_required(login_url='/login/')
def toggle_wishlist(request, food_id):
    try:
        food = Food.objects.get(id=food_id)
        wishlist_item = Wishlist.objects.filter(
            user=request.user,
            item=food
        ).first()
        
        if wishlist_item:
            wishlist_item.delete()
            return JsonResponse({
                'status': 'success',
                'is_wishlisted': False,
                'message': 'Removed from wishlist'
            })
        else:
            Wishlist.objects.create(user=request.user, item=food)
            return JsonResponse({
                'status': 'success',
                'is_wishlisted': True,
                'message': 'Added to wishlist'
            })
            
    except Food.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Food not found'
        }, status=404)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required(login_url='/login/')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('item', 'item__restoran')
    
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist.html', context)

@login_required(login_url='/login/')
def get_wishlist_status(request):
    wishlisted_items = list(Wishlist.objects.filter(user=request.user).values_list('food_id', flat=True))
    return JsonResponse({'wishlisted_items': wishlisted_items})