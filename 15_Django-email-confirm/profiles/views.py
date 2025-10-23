from django.core.serializers.json import DjangoJSONEncoder
from django.shortcuts import render, redirect,get_object_or_404, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import ProfileForm
from datetime import datetime, time, date
from users.models import *
from collections import defaultdict
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django import template
from django.db.models import F, Count
from django.db.models.functions import TruncDay
import json
from django.db.models import Q
from django.urls import reverse
from django.http import HttpResponseForbidden

# views.py

register = template.Library()

@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)
@login_required
def profile_settings(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None

    cities = City.objects.all()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            print("Form saved successfully")  # Add debug print
            if user_profile.is_complete():
                print("User profile is complete")  # Add debug print
                return redirect('/profiles/')
        else:
            print("Form errors:", form.errors)  # Add debug print
            print("Form data:", request.POST)  # Add debug print
            print("Files:", request.FILES)  # Add debug print
    else:
        form = ProfileForm(instance=user_profile)

    if user_profile and not user_profile.is_complete():
        return render(request, 'profiles/settings.html', {'form': form, 'cities': cities, 'gender_choices': UserProfile.GENDER_CHOICES})
    else:
        return redirect('/profiles/profile/')


@login_required
def profile(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect('/profiles/settings/')

    posts = Img.objects.filter(user=user_profile).order_by('-added_date')
    albums = Album.objects.filter(userId=user_profile).order_by('-createDT')
    if user_profile.is_complete():
        return render(request, 'profiles/profile.html', {'profile': user_profile,'posts':posts,'albums':albums})
    else:
        return redirect('/profiles/settings/')

@login_required
def profileHomePage(request):
    user = request.user
    current_time = datetime.now()
    
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    people_you_might_know = UserProfile.objects.exclude(user=user)
    user_stories = Story.objects.filter(userprofile__user=user, expiration_time__gt=current_time)
    
    other_users = UserProfile.objects.exclude(user=user)

    grouped_stories = defaultdict(list)
    for other_user in other_users:
        stories = Story.objects.filter(userprofile=other_user, expiration_time__gt=current_time)
        grouped_stories[other_user].extend(stories)
    
    posts = Img.objects.all().order_by('-added_date')
    imgHP = Img.objects.all().order_by('-price')[:3]
    has_bought_dict = {}

    for post in posts:
        has_bought_dict[post.imageid] = OrderDetails.objects.filter(ImageId=post, userId=user_profile).exists()
    
    
    return render(request, "profiles/index.html", {'profile': user_profile, 'peoples': people_you_might_know, 'user_stories': user_stories, 'grouped_stories': grouped_stories.values(),'posts':posts,'has_bought': has_bought_dict,'img_hp':imgHP})

def profile_view(request, username):
    user_profile = UserProfile.objects.get(user__username=username)
    posts = Img.objects.filter(user=user_profile).order_by('-added_date')
    albums = Album.objects.filter(userId=user_profile).order_by('-createDT')
    
    # Count the number of following and followers
    following_count = Follow.objects.filter(followerId=request.user.id).count() if request.user.is_authenticated else 0
    followers_count = Follow.objects.filter(userId=user_profile).count()
    
    # Check if the logged-in user is following the displayed profile
    is_following = False
    if request.user.is_authenticated:
        try:
            follow_instance = Follow.objects.get(userId=user_profile, followerId=request.user.id)
            is_following = True
        except Follow.DoesNotExist:
            is_following = False
    
    return render(request, 'profiles/profile2.html', {'user_profile': user_profile, 'posts': posts, 'albums': albums, 'is_following': is_following, 'following_count': following_count, 'followers_count': followers_count})


def createStory(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    
    photo = request.FILES.get("fup")
    caption = request.POST.get("caption")

    expiration_time = datetime.now() + timedelta(hours=24)

    print("Expiration Time:", expiration_time)

    upSt = Story(
        userprofile=user_profile,
        photo=photo,
        caption=caption,
        expiration_time=expiration_time
    )
    upSt.save()

    print("Story saved successfully:", upSt)

    return redirect('/profiles/')

def search_user(request):
    searched_user_profile = None
    search_username = request.GET.get('search_username', '')  # Get the username from the query parameters

    if search_username:
        try:
            searched_user = CustomUser.objects.get(username=search_username)
            searched_user_profile = UserProfile.objects.get(user=searched_user)
        except CustomUser.DoesNotExist:
            pass
        except UserProfile.DoesNotExist:
            pass
    return redirect('/profiles/')

def createPost(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    
    photo = request.FILES.get("")
    caption = request.POST.get("caption")

    upSt = Img(
        userprofile=user_profile,
        photo=photo,
        caption=caption,
    )
    upSt.save()

    print("Story saved successfully:", upSt)

    return redirect('/profiles/')

def loadImgForm(request):
   return render(request,"profiles/image_form.html",{"Category": Category.objects.all(), "SubCategory": Subcategory.objects.all()})

def UpdImage(request):
    user=request.user
    user_profile = UserProfile.objects.get(user=user)

    if "btnImgSell" in request.POST:
        p = Img()
        p.user=user_profile
        p.title = request.POST.get("txtTitle1")
        p.categoryid = Category.objects.filter(categoryid=request.POST.get("CateOp")).first()
        p.subcategoryid = Subcategory.objects.filter(subcategoryid=request.POST.get("SubCateOp")).first()
        p.url = request.FILES.get("fupImage1")
        p.description = request.POST.get("txtDescription1")
        p.price = request.POST.get("txtPrice1")
        p.discount = request.POST.get("txtDisc1")
    
        p.save()
        return redirect('/profiles/')
    return render(request, "profiles/image_form.html", {"Category": Category.objects.all(), "SubCategory": Subcategory.objects.all()})

    
def addToWishlist(request, imageid):
    user_profile = request.user.userprofile
    post_id = get_object_or_404(Img, pk=imageid)
    if Wishlist.objects.filter(userId=user_profile, ImageId=post_id).exists():
        pass
    else:
         wishlist_item = Wishlist(userId=user_profile, ImageId=post_id)
         wishlist_item.save()

    return redirect('/profiles/wishlist/')

def addToCart(request, imageid):
    user_profile = request.user.userprofile
    post_id = get_object_or_404(Img, pk=imageid)
    if Cart.objects.filter(userId=user_profile, ImageId=post_id).exists():
        pass
    else:
         cart_item = Cart(userId=user_profile, ImageId=post_id)
         cart_item.save()

    return redirect('/profiles/cart/')

def wishlist(request):
    user_profile = request.user.userprofile
    wishlist_list = Wishlist.objects.filter(userId=user_profile)
    return render(request,"profiles/wishlist.html",{'wishlist':wishlist_list})

def cart(request):
    user_profile = request.user.userprofile
    cart_list = Cart.objects.filter(userId=user_profile)
    return render(request,"profiles/cart.html",{'carts':cart_list})

    
def removeWishlist(request, imageid):
    w = Wishlist.objects.filter(wishlistId=imageid)
    w.delete()
    user_profile = request.user.userprofile
    wishlist_list = Wishlist.objects.filter(userId=user_profile)
    return render(request,"profiles/wishlist.html",{'wishlist':wishlist_list})

def removeCart(request, imageid):
    w = Cart.objects.filter(cartId=imageid)
    w.delete()
    return redirect("/profiles/cart/")
    
    
def shop(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None
    return render(request,"profiles/shop.html",{'images':Img.objects.all(),'profile':user_profile})

def loadExplore(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = None
    posts = Img.objects.all()
    return render(request,"profiles/explore.html",{'profile': user_profile,'posts':posts}) 

def imageInfo(request, imageid):
    image = get_object_or_404(Img, imageid=imageid)
    comments = comment.objects.filter(imageid=imageid)

    Img.objects.filter(imageid=imageid).update(total_views=F('total_views') + 1)

    user_profile = request.user.userprofile
    has_bought = OrderDetails.objects.filter(ImageId=image, userId=user_profile).exists()

    likes = Like.objects.filter(imageid=image)

    my_likes = Like.objects.filter(userid=user_profile, imageid=image)
    total_sales = OrderDetails.objects.filter(ImageId=image).count()
    context = {
        'image': image,
        'likes': likes,
        'hasLike': my_likes.exists(),  # Check if the current user has liked the image
        'comms': comments,
        'has_bought': has_bought,
        'total_views': image.total_views,
        'total_sales': total_sales if total_sales else 0,# Include total views
    }

    return render(request, 'profiles/imageinfo.html', context)

def insertLike(request):
    userInfo = request.user.userprofile
    pid = request.GET.get("pid")
    imgs = Img.objects.filter(imageid=pid).first()

    likeadd = Like(userid=userInfo, imageid=imgs)
    likeadd.save()

    return redirect('image_info', imageid=pid)

def deleteLike(request):
    userInfo = request.user.userprofile
    pid = request.GET.get("pid")
    imgs = Img.objects.filter(imageid=pid).first()
    
    likedel = Like.objects.filter(userid=userInfo, imageid=imgs).first()
    likedel.delete()

    return redirect('image_info', imageid=pid)

def addCommnet(request):
    userInfo = request.user.userprofile
    
    pid=request.GET.get("pid")

    c=comment(userid=userInfo,
              imageid=Img.objects.filter(imageid=pid).first(),
              comment=request.POST.get("txtComment")
              )
    c.save()
    return redirect('image_info', imageid=pid)

def loadCheckout(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    cart_det = Cart.objects.filter(userId=user_profile)
    total_price = cart_det.aggregate(total=Sum('ImageId__price'))['total'] or 0
    
    return render(request,"profiles/checkout.html",{'user_profiles':user_profile,'carts':cart_det,'total_price': total_price})

def razorpaycheck(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    cart = Cart.objects.filter(userId=user_profile)
    total_price = 0
    for item in cart:
        total_price = total_price + item.ImageId.price
    print(total_price)
    return JsonResponse({
        'total_price':total_price,
    })
    
@csrf_exempt
def place_order(request):
    if request.method == "POST":
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            contact = request.POST.get('contact')
            image_ids = request.POST.getlist('image_ids[]')  # Retrieve the list of image IDs from the AJAX request
            
            total_amount = 0
            for image_id in image_ids:
                image_instance = Img.objects.get(pk=image_id)
                total_amount += image_instance.price
            
            payment_successful = True
            
            if payment_successful:
                order_date = datetime.now()  # Get the current date and time
                order = Order.objects.create(orderDT=order_date, userId=request.user.userprofile, status='Pending')
                
                for image_id in image_ids:
                    image_instance = Img.objects.get(pk=image_id)
                    order_details = OrderDetails.objects.create(ImageId=image_instance, userId=request.user.userprofile, orderId=order)
                    order_details.save()  # Save the OrderDetails instance
                    print("OrderDetails created for image_id:", image_id)
                
                # Clear the user's cart
                cart_items = Cart.objects.filter(userId=request.user.userprofile)
                cart_items.delete()
                
                return JsonResponse({'message': 'Order placed successfully'})
            else:
                return JsonResponse({'error': 'Payment failed'}, status=400)
                
        except Exception as e:
            error_message = str(e)
            return JsonResponse({'error': error_message}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
def myBuy(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    ord_det = OrderDetails.objects.filter(userId=user_profile)
    print(ord_det)
    return render(request,"profiles/mybuy.html",{'orders':ord_det})

def myLike(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    likes = Like.objects.filter(userid=user_profile)
    return render(request,"profiles/mylike.html",{'likes':likes})

def my_sales(request):
    user = request.user
    try:
        user_profile2 = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile2 = None
        
    user_profile = request.user.userprofile
    
    sold_items = OrderDetails.objects.filter(ImageId__user=user_profile)
    
    total_income_dict = sold_items.aggregate(total_income=Sum('ImageId__price'))
    total_income = total_income_dict['total_income'] if total_income_dict is not None else 0

    today = datetime.now().date()
    start_of_day = datetime.combine(today, time.min)
    end_of_day = datetime.combine(today, time.max)
    total_today_income_dict = sold_items.filter(orderId__orderDT__range=(start_of_day, end_of_day)).aggregate(total_today_income=Sum('ImageId__price'))
    total_today_income = total_today_income_dict.get('total_today_income', 0)

    current_month = today.month
    current_year = today.year
    start_of_month = datetime(current_year, current_month, 1)
    end_of_month = datetime(current_year, current_month, date.today().day, 23, 59, 59)
    total_monthly_income_dict = sold_items.filter(orderId__orderDT__range=(start_of_month, end_of_month)).aggregate(total_monthly_income=Sum('ImageId__price'))
    total_monthly_income = total_monthly_income_dict.get('total_monthly_income', 0)
    
    total_views = Img.objects.filter(user=user_profile).aggregate(total_views=Sum('total_views'))['total_views']

    total_likes = Like.objects.filter(imageid__user=user_profile).count()

    total_comments = comment.objects.filter(imageid__user=user_profile).count()

    day_wise_sales = sold_items.annotate(date=TruncDay('orderId__orderDT')).values('date').annotate(total_sales=Sum('ImageId__price')).order_by('date')
    
    image_sales_data = Img.objects.filter(user=user_profile).annotate(total_sales=Sum('orderdetails__ImageId__price')).values('title', 'total_sales')
    image_sales = [{'title': item['title'], 'total_sales': float(item['total_sales']) if item['total_sales'] is not None else 0} for item in image_sales_data]

    total_interaction = total_views + total_likes + total_comments
    
    unique_buyers = sold_items.values('orderId__userId__user__username').annotate(total_earnings=Sum('ImageId__price'))

    data = [[str(buyer['orderId__userId__user__username']), float(buyer['total_earnings'])] for buyer in unique_buyers]

    unique_buyers_json = json.dumps(data, cls=DjangoJSONEncoder)

    per_image_unique_buyers = []
    for item in image_sales_data:
        image_unique_buyers = sold_items.filter(ImageId__title=item['title']).values('orderId__userId').annotate(total_earnings=Sum('ImageId__price'))
        data_per_image_buyers = [[str(buyer['orderId__userId']), float(buyer['total_earnings'])] for buyer in image_unique_buyers]
        per_image_unique_buyers.append({'title': item['title'], 'data': data_per_image_buyers})
    per_image_unique_buyers_json = json.dumps(per_image_unique_buyers, cls=DjangoJSONEncoder)
    
    print("Per image unique buyers data:", per_image_unique_buyers_json)

    
    context = {
        'sold_items': sold_items,
        'total_income': total_income,
        'total_today_income': total_today_income,
        'total_monthly_income': total_monthly_income,
        'total_views': total_views,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'day_wise_sales': day_wise_sales,
        'items': json.dumps(image_sales),
        'total_interaction': total_interaction,
        'unique_buyers': unique_buyers_json,
        'per_image_unique_buyers': per_image_unique_buyers_json,
        'profile':user_profile2,
    }

    return render(request, "profiles/mysales.html", context)

def analytics(request, image_id):
    image = get_object_or_404(Img, pk=image_id)

    # Retrieve analytics data for the image
    total_downloads = image.total_download
    total_revenue = OrderDetails.objects.filter(ImageId=image).count() * image.price  # Assuming each purchase counts as revenue
    total_purchases = OrderDetails.objects.filter(ImageId=image).count()
    total_likes = Like.objects.filter(imageid=image).count()
    total_comments = comment.objects.filter(imageid=image).count()

    context = {
        'image': image,
        'total_downloads': total_downloads,
        'total_revenue': total_revenue,
        'total_purchases': total_purchases,
        'total_likes': total_likes,
        'total_comments': total_comments,
    }

    return render(request, 'profiles/analytics.html', context)

def download_image(request, image_id):
    image = get_object_or_404(Img, imageid=image_id)

    image.total_download += 1
    image.save()

    file_path = image.url.path
    with open(file_path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename={image.title}.png'
    return response

def search_images(request):
    categories = Category.objects.all()
    category_name = request.GET.get('category', '')
    
    if category_name=="":
        images = Img.objects.all()
    else:
        images = Img.objects.filter(categoryid__categoryname=category_name)
        
    if "btnsea" in request.POST:
        category_name_post = request.POST.get('category')
        seatitle = request.POST.get("search")
        if seatitle:
            images = images.filter(Q(title__icontains=seatitle) | Q(user__user__username__icontains=seatitle))
        
        price_level = request.POST.get('price', '')

        if category_name_post:
            images = images.filter(categoryid__categoryname=category_name_post)
            
        if price_level == "cheap":
            images = images.filter(price__lte=100)
        elif price_level == "moderate":
            images = images.filter(price__range=[100, 500])
        elif price_level == "expensive":
            images = images.filter(price__gte=501)

    return render(request, 'profiles/search_results.html', {'images': images,"categories":categories})

def createAlubms(request):
    user = request.user.userprofile  # Assuming UserProfile is linked with User model
    if request.method == 'POST':
        title = request.POST.get('Title')
        images_to_add = request.POST.getlist('images')  # Assuming checkboxes with 'images' name in HTML

        album = Album.objects.create(Title=title, userId=user, createDT=datetime.now())
        for image_id in images_to_add:
            image = Img.objects.filter(user=user).get(pk=image_id)
            image.album = album 
            image.save()

        return redirect('/profiles/albums/')  # Redirect to album detail page

    images = Img.objects.filter(user=user)  # Get all images, adjust this as per your requirement
    return render(request, 'profiles/createAlbum.html', {'images': images})

@login_required
def all_albums(request):
    user = request.user.userprofile
    albums = Album.objects.filter(userId=user)
    return render(request, 'profiles/all_albums.html', {'albums': albums})

def album_detail(request, album_id):
    album = get_object_or_404(Album, pk=album_id, userId=request.user.userprofile)
    images = Img.objects.filter(album=album)
    return render(request, 'profiles/album_detail.html', {'album': album, 'images': images})

def displayAuction(request):
    auctions = Auction.objects.all()
    return render(request, 'profiles/auctions.html', {'auctions': auctions})

def create_auction(request):
    user_images = Img.objects.filter(user=request.user.userprofile)
    
    if request.method == 'POST':
        image_id = request.POST['image_id']
        auction_amount = request.POST['auction_amount']
        description = request.POST['description']
        
        image = Img.objects.get(pk=image_id)
        
        auction_end_date = timezone.now() + timedelta(days=3)  # Adjust end date as needed
        
        auction = Auction(
            ImageId=image,
            AuctionAmount=auction_amount,
            Description=description,
            AuctionEndDate=auction_end_date
        )
        auction.save()
        return redirect('/profiles/auction/')  # Redirect to the auction list page or any other page
    
    return render(request, 'profiles/createAuction.html', {'user_images': user_images})

def auction_details(request):
    auction_id = request.GET.get('auction_id')
    auction = get_object_or_404(Auction, pk=auction_id)
    
    if request.method == 'POST':
        bid_amount = request.POST.get('bid_amount')
        user = request.user.userprofile
        action = request.POST.get('action')
        
        highest_bid = Bid.objects.filter(imageid=auction.ImageId).order_by('-amount').first()
        bid_history = Bid.objects.filter(imageid=auction.ImageId).order_by('-bid_time')
        existing_bid = Bid.objects.filter(imageid=auction.ImageId, userid=user).first()
        
        if action == 'submit':
            if existing_bid:
                return render(request, 'profiles/auction_details.html', {
                    'auction': auction,
                    'highest_bid': highest_bid,
                    'bid_history': bid_history,
                    'error_message': "You have already placed a bid on this auction.",
                })
            
            bid = Bid(
                userid=user,
                imageid=auction.ImageId,
                amount=bid_amount
            )
            bid.save()
            
            # Update the highest bid amount for the auction
            auction.highest_bid_amount = bid_amount
            auction.save()
            
            return redirect('/profiles/detauction?auction_id=' + auction_id)
        
        elif action == 'update':
            if not existing_bid:
                return render(request, 'profiles/auction_details.html', {
                    'auction': auction,
                    'highest_bid': highest_bid,
                    'bid_history': bid_history,
                    'error_message': "You haven't placed a bid yet.",
                })
            
            existing_bid.amount = bid_amount
            existing_bid.save()
            
            # Update the highest bid amount for the auction
            auction.highest_bid_amount = bid_amount
            auction.save()
            
            return redirect('/profiles/detauction?auction_id=' + auction_id)
        
        elif action == 'end':
            auction.status = 'ENDED'
            if highest_bid:
                auction.winner = highest_bid.userid
            else:
                auction.winner = None
            
            # Update the highest bid amount for the auction
            if highest_bid:
                auction.highest_bid_amount = highest_bid.amount
            auction.save()
            
            return redirect('/profiles/detauction?auction_id=' + auction_id)
    
    else:
        highest_bid = Bid.objects.filter(imageid=auction.ImageId).order_by('-amount').first()
        bid_history = Bid.objects.filter(imageid=auction.ImageId).order_by('-bid_time')
        existing_bid = Bid.objects.filter(imageid=auction.ImageId, userid=request.user.userprofile).exists()
        
        return render(request, 'profiles/auction_details.html', {
            'auction': auction,
            'highest_bid': highest_bid,
            'bid_history': bid_history,
            'existing_bid': existing_bid
        })


def create_auction_page(request, image_id):
    image = Img.objects.get(pk=image_id)
    
    if request.method == 'POST':
        auction_amount = request.POST['auction_amount']
        description = request.POST['description']
        
        
        auction_end_date = timezone.now() + timedelta(days=3)  # Adjust end date as needed
        
        auction = Auction(
            ImageId=image,
            AuctionAmount=auction_amount,
            Description=description,
            AuctionEndDate=auction_end_date
        )
        auction.save()
        return redirect('/profiles/auction/')  # Redirect to the auction list page or any other page
    
    return render(request, 'profiles/createAuction2.html', {'user_images': image})

@login_required
def follow_toggle(request):
    if 'u_id' in request.GET:
        username = request.GET['u_id']
        user_profile = UserProfile.objects.get(user__username=username)
        follower_id = request.user.id  # Get the ID of the logged-in user
        try:
            follow_instance = Follow.objects.get(userId=user_profile, followerId=follower_id)
            # If already following, unfollow
            follow_instance.delete()
        except Follow.DoesNotExist:
            # If not following, follow
            Follow.objects.create(userId=user_profile, followerId=follower_id)
        return redirect('profile', username=user_profile.user.username)
    else:
        # Handle the case where 'u_id' parameter is missing in the request
        return redirect('/profiles/')  # Or any other appropriate redirect


@csrf_exempt
def update_auction_status(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        auction_id = data.get('auction_id')
        payment_id = data.get('payment_id')

        # Retrieve the auction object
        try:
            auction = Auction.objects.get(pk=auction_id)
        except Auction.DoesNotExist:
            return JsonResponse({'error': 'Auction not found'}, status=404)

        # Perform any necessary validation
        
        # Create AuctionPayment object
        auction_payment = AuctionPayment.objects.create(
            auction=auction,
            user=request.user.userprofile,
            amount=auction.highest_bid_amount,
            razorpay_payment_id=payment_id,
        )
        
        auction.payment_status = 'paid'
        # Update the auction status if needed
        auction.save()
        
        PastOwner.objects.create(
            image=auction.ImageId,  # Access the ImageId attribute of the Auction model
            auction=auction,
            past_owner=auction.ImageId.user,
            transfer_date=datetime.now(),
            amount=auction.highest_bid_amount,
        )
        
        img = Img.objects.get(pk=auction.ImageId.pk)  
        print(img)  # Retrieve the Img object
        img.user = request.user.userprofile
        img.save()
        
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@login_required
def process_payment(request):
    if request.method == 'POST':
        auction_id = request.POST.get('auction_id')
        auction = Auction.objects.get(pk=auction_id)
        # Perform any necessary validation
        
        if auction.ImageId.user != request.user.userprofile:
            return HttpResponseForbidden("You are not authorized to perform this action.")
        
        # Process the payment and create an AuctionPayment object
        amount = auction.AuctionAmount  # You may adjust this based on your application logic
        razorpay_payment_id = request.POST.get('razorpay_payment_id')
        auction_payment = AuctionPayment.objects.create(
            auction=auction,
            user=request.user.userprofile,
            amount=amount,
            razorpay_payment_id=razorpay_payment_id
        )
        
        # Update the auction status or perform any other necessary actions
        auction.save()
        
        return redirect('auction_details', auction_id=auction_id)
    return HttpResponse('<h1>ERROR</h1>')