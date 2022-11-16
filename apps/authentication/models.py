from email.policy import default
from pyexpat import model
from sqlite3 import Timestamp
from statistics import mode
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from apps.authentication.managers import UserManager
from django.db import models
from django.core.mail import send_mail
from django.utils import timezone
import sys
from django.core.files.storage import default_storage
from django.db.models.signals import post_delete
from django.dispatch import receiver
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
import os


STATUS_POST =  (
    ('Enable','Enable'),
    ('Disable','Disable')
    )

class User(AbstractBaseUser, PermissionsMixin):
    """ 
        User
    """

    role              = models.CharField(max_length=10,     default='USER')
    username          = models.CharField(max_length=50,     unique=True)
    email             = models.EmailField(unique=True)
    status            = models.CharField(max_length=15,     choices=STATUS_POST, default='Enable')

    is_active         = models.BooleanField(default=True)
    is_staff          = models.BooleanField(default=False)
    is_superuser      = models.BooleanField(default=False)

    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)


    objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        
    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

    
    def __str__(self):
        return f"Username : {self.username} Email : {self.email} Role : {self.role}"

        

class Profile(models.Model):
    user              = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name        = models.CharField(max_length=50)
    last_name         = models.CharField(max_length=50,    null=True, blank=True)
    phone             = models.CharField(max_length=20)
    image             = models.ImageField(upload_to='profile/', default="", blank=True)
    bio               = models.TextField(null=True ,  blank=True)
    
    address           = models.TextField(null=True ,  blank=True)
    latitude          = models.FloatField(blank=True, null=True)
    longitude         = models.FloatField(blank=True, null=True)

    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Username : {self.user.username} Full Name : {self.first_name} Last Name : {self.last_name}"


    @receiver(post_delete, sender=image)
    def delete_associated_files(sender, instance, **kwargs):
        """Remove all files of an image after deletion."""
        path = instance.image
        if path:
            default_storage.delete(path)

     # resize image before saving
    # def save(self):
    # 	#Opening the uploaded image
    #     im = Image.open(self.image)
    #     output = BytesIO()
    #     #Resize/modify the image
    #     im = im.resize( (44,44) )
    #     #after modifications, save it to the output
    #     img_format = os.path.splitext(self.image.name)[1][1:].upper()
    #     img_format = 'JPEG' if img_format == 'JPG' else img_format
    #     im.save(output, format=f'{img_format}', quality=75)
    #     output.seek(0)
    #     #change the imagefield value to be the newley modifed image value
    #     self.image = InMemoryUploadedFile(output,'ImageField', "%s.jpg" %self.image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)

    #     super(Profile,self).save()

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 44 or img.width > 44:
            output_size = (44,44)
            img.thumbnail(output_size)
            img.save(self.image.path)


class PasswordResetToken(models.Model):

    user       = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now = True)
    token      = models.CharField(max_length=100)

    def __str__(self):
        return "Password reset token for user {user}".format(user=self.user)


class Posts(models.Model):
    
    """ 
        Posts
    """
    STATUS = (
    ('Public','Public'),
    ('Friends','Friends'),
    ('Only me','Only me'))

    user            =   models.ForeignKey(User,              on_delete=models.CASCADE)
    views           =   models.IntegerField(default=0,       blank=True)
    share           =   models.IntegerField(default=0,       blank=True)
    tags            =   models.CharField(max_length=100,     blank=True)
    caption         =   models.TextField(blank=True,         null=True)
    upload_img_file =   models.FileField(upload_to='posts/', blank=True, null=True)
    upload_file     =   models.FileField(upload_to='posts/', blank=True, null=True)

    post_status     =   models.CharField(max_length=20,      choices=STATUS, default='Public')
    status          =   models.CharField(max_length=15,      choices=STATUS_POST, default='Enable')
   
    location        =   models.CharField(max_length=200, blank=True, null=True)
    latitude        =   models.FloatField(blank=True,         null=True)
    longitude       =   models.FloatField(blank=True,         null=True)

    created_at      =   models.DateTimeField(auto_now_add=True)
    updated_at      =   models.DateTimeField(auto_now=True)



    def __str__(self):
        return f"User : {self.user.username}  Uploaded File : {self.upload_file} Status Post : {self.post_status}"



class Comments(models.Model):
    post            = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment         = models.TextField(blank=False,    null=False)

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)


class Like(models.Model):
    post            =  models.ForeignKey(Posts, related_name='post', on_delete=models.CASCADE)
    sender          =  models.ForeignKey(User, related_name='user_sender', on_delete=models.CASCADE)
    likes           =  models.IntegerField(default=1, blank=False,    null=False)
   
    created_at      =  models.DateTimeField(auto_now_add=True)
    updated_at      =  models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Posts : {self.post} likes : {self.likes}"


# class SharePost(models.Model):
#     post            = models.ForeignKey(Posts, related_name='posts', on_delete=models.CASCADE)
#     share           = models.IntegerField(default=0, blank=False,    null=False)

#     def __str__(self):
#         return self.share



class Friends(models.Model):
    STATUS = (
    ('Block','Block'),
    ('Unblock','Unblock'),
    ('Mute','Mute'))

    user         = models.ForeignKey(User, on_delete=models.CASCADE)
    sender       = models.ForeignKey(User, related_name='sender', on_delete=models.CASCADE)

    follower     = models.IntegerField(default=0, blank=False,    null=False)
    status       = models.CharField(max_length=15   ,     choices=STATUS, default='Unblock')

    def __str__(self):
        return f"User : {self.user.username} Followers : {self.follower}"


class TotalPost(models.Model):
    user            = models.ForeignKey(User,  on_delete=models.CASCADE)
    total_views     = models.IntegerField(default=0,      blank=True)
    comments        = models.IntegerField(default=0,      blank=True)
    reaction        = models.IntegerField(default=0,      blank=True)

    created_at      =  models.DateTimeField(auto_now_add=True)
    updated_at      =  models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"User : {self.user.username} Total Views : {self.total_views} Comments : {self.comments} Reactions : {self.reaction}"


class PageContent(models.Model):
    STATUS = (
    ('Active','Active'),
    ('Deactive','Deactive'),
    ('Suspend','Suspend'))

    user            = models.ForeignKey(User, on_delete=models.CASCADE)
    title           = models.CharField(max_length=200)
    description     = models.TextField(blank=True,     null=True)
    content         = models.TextField(blank=True,     null=True)
    status          = models.CharField(max_length=15,  choices=STATUS, default='Active')


    created_at      =  models.DateTimeField(auto_now_add=True)
    updated_at      =  models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"User : {self.user.username} Title : {self.title}"




class FriendList(models.Model):
    user     = models.OneToOneField(User, related_name='user_friend', on_delete=models.CASCADE)
    friends  = models.ManyToManyField(User, related_name='friends_list', blank=True)

    def __str__(self):
        return self.user.username

    
    def accept(self, account):
        """
        add friend in friendlist
        """
        if not account in self.friends.all():
            self.friends.add(account)

    
    def remove_friend(self,account):
        if account in self.friends.all():
            self.friends.remove(account)

    
    def unfriend(self,removee):
        """
            Initiate the action of unfriending someone
        """
        remover_friends_list = self

        # remove friends from remover friends list 
        remover_friends_list.remove_friend(removee)

        # remove friends from removee friends list
        friends_list = FriendList.objects.get(user=removee)
        friends_list.remove_friend(self.user)


    def is_mutual(self,friend):
        """
            is this a friend?
        """

        if friend in self.friends.all():
            return True
        return False


class FriendRequest(models.Model):
    """
        1. SENDER - Person sending or Initiating friend request
        2. RECIEVER - Person receiving the friend request
    """

    sender      =   models.ForeignKey(User, related_name='user_friend_list', on_delete=models.CASCADE)
    reciever    =   models.ForeignKey(User, related_name='user_reciever', on_delete=models.CASCADE)

    is_active   =   models.BooleanField(default=False)

    timestamp   =   models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.sender.username

    
    def accept(self):
        """
            Accept the friend request
            update both sender and receiver friend list
        """

        receiver_friend_list = FriendList.objects.get(user = self.reciever)
        if receiver_friend_list:
            receiver_friend_list.add_friend(self.sender)
            sender_friend_list = FriendList.objects.get(user = self.sender)
            if sender_friend_list:
                sender_friend_list.add_friend(self.reciever)
                self.as_active = False
                self.save()


    def decline(self):
        """
            Decline a friend request 
            It is Declined by setting the 'is_active' field to False
        """
        self.is_active = False
        self.save()

    
    def cancel(self):
        """
            cancel a friend request
        """
        self.is_active = False
        self.save()



