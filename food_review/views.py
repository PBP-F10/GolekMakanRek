from .models                            import *
from .forms                             import *
from django.shortcuts                   import render, get_object_or_404
from django.http                        import JsonResponse
from django.contrib.auth.decorators     import login_required
from main.models                        import *
from django.utils                       import timezone
from django.http                        import JsonResponse, HttpResponse
from django.contrib.auth.decorators     import login_required
from django.views.decorators.http       import require_http_methods
from django.core                        import serializers
import logging
import json
from django.views.decorators.csrf import csrf_exempt


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

@csrf_exempt
@login_required(login_url='/login/')
def add_rating(request, food_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

    try:
        food = get_object_or_404(Food, id=food_id)
        
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
        score = data.get('score')

        if not score:
            return JsonResponse({'status': 'error', 'message': 'Score is required'}, status=400)

        try:
            score = int(score)
            if not (1 <= score <= 5):
                raise ValueError
        except (ValueError, TypeError):
            return JsonResponse({'status': 'error', 'message': 'Invalid rating score'}, status=400)
        
        rating, created = FoodRating.objects.update_or_create(
            user=request.user,
            deskripsi_food=food,
            defaults={'score': score}
        )

        new_average = food.average_rating

        return JsonResponse({
            'status': 'success',
            'message': 'Rating added successfully',
            'rating_id': str(rating.id),
            'food_rating': new_average
        })

    except Exception as e:
        logger.error(f"Error in add_rating: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
@login_required(login_url='/login/')
def add_comment(request, food_id):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
    
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body.decode('utf-8'))
        else:
            data = request.POST
            
        comment = data.get('comment', '').strip()
        
        if not comment:
            return JsonResponse({'status': 'error', 'message': 'Comment cannot be empty'}, status=400)
        
        food = get_object_or_404(Food, id=food_id)
        rating, created = FoodRating.objects.get_or_create(
            user=request.user,
            deskripsi_food=food,
            defaults={'score': 0}
        )
        
        rating.comment = comment
        rating.waktu_comment = timezone.now()
        rating.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Comment added successfully',
            'comment': {
                'username': request.user.username,
                'comment': comment,
                'formatted_time': rating.waktu_comment.strftime("%B %d, %Y %I:%M %p")
            }
        })
    except Exception as e:
        logger.error(f"Error in add_comment: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@csrf_exempt
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

def serialize_data(request, model, fmt, id=None):
    if id:
        data = get_object_or_404(model, pk=id)
        data = [data]
    else:
        data = model.objects.all()
    return HttpResponse(serializers.serialize(fmt, data), content_type=f"application/{fmt}")

def foodrating_json(request):
    return serialize_data(request, FoodRating, "json")

@login_required(login_url='/login/')
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('item', 'item__restoran')
    
    context = {
        'wishlist_items': wishlist_items,
    }
    return render(request, 'wishlist.html', context)

@login_required(login_url='/login/')
def get_wishlist_status(request):
    wishlisted_items = list(Wishlist.objects.filter(user=request.user).values_list('item_id', flat=True))
    return JsonResponse({'wishlisted_items': wishlisted_items})

@login_required(login_url='/login/')
def wishlist_json(request):
    try:
        wishlist_items = Wishlist.objects.filter(user=request.user).select_related('item', 'item__restoran')

        wishlist_data = []
        for wishlist_item in wishlist_items:
            food = wishlist_item.item
            wishlist_data.append({
                'wishlist_id': str(wishlist_item.id),
                'food': {
                    'id': str(food.id),
                    'name': food.nama,
                    'category': food.kategori,
                    'description': food.deskripsi,
                    'original_price': food.harga,
                    'discount_percentage': food.diskon,
                    'discounted_price': food.harga_setelah_diskon,
                    'average_rating': food.average_rating,
                    'restaurant': {
                        'id': str(food.restoran.id),
                        'name': food.restoran.nama,
                        'category': food.restoran.kategori,
                        'description': food.restoran.deskripsi
                    }
                }
            })
        
        return JsonResponse({
            'status': 'success',
            'count': len(wishlist_data),
            'wishlist': wishlist_data
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@login_required(login_url='/login/')
def check_wishlist_items(request):
    try:
        if request.method == 'POST':
            data = json.loads(request.body)
            item_ids = data.get('item_ids', [])
        else:
            item_ids = request.GET.getlist('item_ids[]')

        if not item_ids:
            return JsonResponse({
                'status': 'error',
                'message': 'No item IDs provided'
            }, status=400)

        wishlisted_items = Wishlist.objects.filter(
            user=request.user,
            item_id__in=item_ids
        ).values_list('item_id', flat=True)

        return JsonResponse({
            'status': 'success',
            'wishlisted_items': list(str(id) for id in wishlisted_items)
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)