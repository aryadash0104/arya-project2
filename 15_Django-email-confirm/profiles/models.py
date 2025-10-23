from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField('users.CustomUser', on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profile_photos', blank=True)
    # cover_photo = models.ImageField(upload_to='cover_photos', blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    contact_number = models.CharField(max_length=20)
    bio = models.TextField(blank=True)
    STATUS_CHOICES = (
        (0, 'Blocked'),
        (1, 'Active'),
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=1)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    def __str__(self):
        return self.user.username

    def is_complete(self):
        # Check if all required fields are filled
        return all([self.profile_photo, self.city, self.contact_number, self.bio, self.gender])
    
class Story(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='stories')
    caption = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_time = models.DateTimeField()

    def save(self, *args, **kwargs):
        # Set expiration time to current time + 24 hours
        self.expiration_time = timezone.now() + timezone.timedelta(hours=24)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expiration_time

    def delete_expired_stories(cls):
        expired_stories = cls.objects.filter(expiration_time__lte=timezone.now())
        expired_stories.delete()

    def __str__(self):
        return f"Story {self.pk} by {self.userprofile.user.username}"
    
class Category(models.Model):
    categoryid=models.AutoField(primary_key=True)
    categoryname=models.TextField(max_length=20)

    def __str__(self):
        return self.categoryname
    
class Subcategory(models.Model):
    subcategoryid = models.AutoField(primary_key=True)
    subcategoryname = models.CharField(max_length=50)
    categoryid = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.subcategoryname
    
class Album(models.Model):
    AlbumId=models.AutoField(primary_key=True)
    Title=models.CharField(max_length=50)
    userId=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    createDT=models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return str(self.AlbumId)+"-"+self.Title

class Img(models.Model):
    imageid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, default="--Not Defined--")
    url = models.ImageField(upload_to='images')
    is_approved = models.BooleanField(default=False)
    status = models.IntegerField(default=0)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    categoryid = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    subcategoryid = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    total_download = models.IntegerField(default=0)
    total_views = models.IntegerField(default=0)
    discount = models.IntegerField(default=0)
    added_date = models.DateTimeField(default=datetime.now)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return f"{self.title}/{self.imageid}/{self.user.user.username}" 
    
class Wishlist(models.Model):
    wishlistId=models.AutoField(primary_key=True)
    userId=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ImageId=models.ForeignKey(Img, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.wishlistId)+"-"+self.userId.user.username

class Cart(models.Model):
    cartId=models.AutoField(primary_key=True)
    userId=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    ImageId=models.ForeignKey(Img, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.cartId)+"-"+self.userId.user.username
    
class Follow(models.Model):
    followId=models.AutoField(primary_key=True)
    userId=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    followerId=models.IntegerField()
    
    def __str__(self):
        return str(self.followId)
class Order(models.Model):
    orderId=models.AutoField(primary_key=True)
    orderDT=models.DateTimeField(default=datetime.now)
    userId=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    status=models.CharField(max_length=50)

    def __str__(self):
        return str(self.orderId)
    
class OrderDetails(models.Model):
    OrderDetailsId=models.AutoField(primary_key=True)
    ImageId=models.ForeignKey(Img, on_delete=models.CASCADE)
    userId=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    orderId = models.ForeignKey(Order, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.OrderDetailsId)
    
class Payment(models.Model):
    paymentId=models.AutoField(primary_key=True)
    userId=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    PaymentDT=models.DateTimeField(default=datetime.now)
    PaymentAmount=models.IntegerField()
    status=models.CharField(max_length=50)
    
    def __str__(self):
        return str(self.paymentId)
class Auction(models.Model):
    ACTIVE = 'Active'
    ENDED = 'Ended'

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (ENDED, 'Ended'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('pending', 'Pending'),
    ]
    auctionId=models.AutoField(primary_key=True)
    ImageId=models.ForeignKey(Img, on_delete=models.CASCADE)
    createdDT=models.DateTimeField(default=datetime.now)
    AuctionAmount=models.IntegerField()
    Description=models.TextField() 
    AuctionStartDate = models.DateField(auto_now_add=True)
    AuctionEndDate = models.DateField(default=datetime.now() + timedelta(days=3))
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=ACTIVE)
    winner = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    highest_bid_amount = models.IntegerField(null=True, blank=True)
    def __str__(self):
        return str(self.auctionId)
'''
class Post(models.Model):
    postid=models.AutoField(primary_key=True)
    Title=models.CharField(max_length=50)
    url=models.ImageField()
    description=models.TextField(max_length=100)
    categoryId=models.ForeignKey(Category, on_delete=models.CASCADE)
    SubcategoryId=models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    price=models.IntegerField(default=0)
    discount=models.IntegerField(default=0)
'''


class Like(models.Model):
    likeid=models.AutoField(primary_key=True)
    userid=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    imageid=models.ForeignKey(Img,on_delete=models.CASCADE)

    def __str__(self):
        return f'Profile for {self.userid.user.username}'

class comment(models.Model):
    commentid=models.AutoField(primary_key=True)
    userid=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    imageid=models.ForeignKey(Img,on_delete=models.CASCADE)
    comment=models.TextField(max_length=100)
    date_time=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment 

class Bid(models.Model):
    bidid=models.AutoField(primary_key=True)
    userid = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    imageid = models.ForeignKey(Img, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return f"Bid by {self.userid.user.username} on {self.imageid.title} for {self.amount}"
    
class AuctionPayment(models.Model):
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    razorpay_payment_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Auction Payment - {self.id}"
    
class PastOwner(models.Model):
    image = models.ForeignKey('Img', on_delete=models.CASCADE)
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE)
    past_owner = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='past_owner')
    amount = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    transfer_date = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return f"Image: {self.image.title}, Auction: {self.auction.pk}, Past Owner: {self.past_owner.user.username}, Transfer Date: {self.transfer_date}"