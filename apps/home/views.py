from re import U
from django import template
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.dispatch import receiver
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
from django.conf import settings
from apps import COMMON
# from apps.accounts.views import profile
from apps.authentication.models import FriendList,Comments, Like, Profile, User, Posts ,FriendRequest
import json
from django.db.models import Max
from django.core.files.storage import FileSystemStorage

from apps.helpers import check_extention, get_current_location
import datetime
 

FILE_EXTENTION =  {'.jpg', '.jpeg', '.png'}


# @login_required(login_url="/login/")
def index(request):
    print("start")
    sign = 0
    all_posts = Posts.objects.filter(status="Enable").order_by("-id")
    data_list = []
    for ps in all_posts:
        data = {}
        data['likes_count'] = Like.objects.filter(post__id=ps.id, likes__gte=1).count()
        current_user_like = Like.objects.filter(post__id=ps.id, post__user__id=ps.user.id, sender_id=request.user.id).first()
        if current_user_like:
            data['current_user_react'] = current_user_like.likes
        else:
            data['current_user_react'] = 0
        data['id']          = ps.id
        data['user_id']     = ps.user.id
        data['views']     = ps.views
        comments = Comments.objects.filter(post_id = ps.id)
        if comments.exists():
             all_comments= Comments.objects.filter(post_id = ps.id)
             data['comments'] = []
             for com in all_comments:
                temp = {}
                temp['id'] = com.id
                temp['comment'] = com.comment
                user = User.objects.get(id = com.user_id)
                temp['user_name'] = user.username
                temp['post_id'] = com.post_id
                # temp['created_at'] = com.created_at
                # temp['updated_at'] = com.updated_at
                data['comments'].append(temp)
        else:
            data['comments'] = 0

        data['user_image'] = ps.user.profile.image.name
        data['username']    = ps.user.username
        data['post_status'] = ps.post_status
        data['caption']     = ps.caption
        data['location']    = ps.location
        if ps.upload_file:
            data['upload_file']  = ps.upload_file.name
            data['img_vid'] = 'vid'
        if ps.upload_img_file:
            data['upload_img_file'] = ps.upload_img_file.name
            data['img_vid'] = 'img'
        data['lat']         = ps.latitude
        data['long']        = ps.longitude
        # data['created_at']  = ps.created_at
        data_list.append(data)
    context = {'all_posts' : data_list,'request_user' : request, 'sign': sign}
    # context = {'request' : request}
    return render(request,"home/index.html", context)

# @login_required
# (login_url="/login/")
def userprofile(request, id):
    sign = 0
    # exists()
    all_posts = Posts.objects.filter(status="Enable", user_id = id).order_by("-id")
    data_list = []
    for ps in all_posts:
        data = {}
        data['likes_count'] = Like.objects.filter(post__id=ps.id, likes__gte=1).count()
        current_user_like = Like.objects.filter(post__id=ps.id, post__user__id=ps.user.id, sender_id=request.user.id).first()
        if current_user_like:
            data['current_user_react'] = current_user_like.likes
        else:
            data['current_user_react'] = 0
        data['id']          = ps.id
        data['user_id']     = ps.user.id
        data['views']     = ps.views
        comments = Comments.objects.filter(post_id = ps.id)
        if comments.exists():
             all_comments= Comments.objects.filter(post_id = ps.id)
             data['comments'] = []
             for com in all_comments:
                temp = {}
                temp['id'] = com.id
                temp['comment'] = com.comment
                user = User.objects.get(id = com.user_id)
                temp['user_name'] = user.username
                temp['post_id'] = com.post_id
                # temp['created_at'] = com.created_at
                # temp['updated_at'] = com.updated_at
                data['comments'].append(temp)
        else:
            data['comments'] = 0
        data['user_image'] = ps.user.profile.image.name
        data['username']    = ps.user.username
        data['post_status'] = ps.post_status
        data['caption']     = ps.caption
        data['location']    = ps.location
        if ps.upload_file:
            data['upload_file']  = ps.upload_file.name
            data['img_vid'] = 'vid'
        if ps.upload_img_file:
            data['upload_img_file'] = ps.upload_img_file.name
            data['img_vid'] = 'img'
        data['lat']         = ps.latitude
        data['long']        = ps.longitude
        # data['created_at']  = ps.created_at
        data_list.append(data)
    # current_user = request.user
    context = {'all_posts' : data_list, 'request_user' : request, 'sign': sign}
    # context = {'request' : request}
    return render(request,"home/userprofile.html", context)
 
# @login_required(login_url="/login/")
# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:

#         load_template = request.path.split('/')[-1]

#         if load_template == 'admin':
#             return HttpResponseRedirect(reverse('admin:index'))

#         segment, active_menu = get_segment(request)

#         context['segment'] = segment
#         context['active_menu'] = active_menu

#         html_template = loader.get_template('home/' + load_template)
#         return HttpResponse(html_template.render(context, request))

#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template('home/page-404.html')
#         return HttpResponse(html_template.render(context, request))

#     except:
#         html_template = loader.get_template('home/page-500.html')
#         return HttpResponse(html_template.render(context, request))

# Helper - Extract current page name from request


def get_segment(request):

    try:

        segment = request.path.split('/')[-1]
        active_menu = None

        if segment == '' or segment == 'index.html':
            segment = 'index'
            active_menu = 'dashboard'

        if segment.startswith('dashboards-'):
            active_menu = 'dashboard'

        if segment.startswith('account-') or segment.startswith('users-') or segment.startswith('profile-') or segment.startswith('projects-'):
            active_menu = 'pages'

        if segment.startswith('notifications') or segment.startswith('sweet-alerts') or segment.startswith('charts.html') or segment.startswith('widgets') or segment.startswith('pricing'):
            active_menu = 'pages'

        return segment, active_menu

    except:
        return 'index', 'dashboard'

def profileView(request):
    print(2222)
    user_all_posts =  Posts.objects.filter(user__id=request.user.id, status="Enable").order_by("-id")
    data_list = []
    for ps in user_all_posts:
        data = {}
        data['likes_count'] = Like.objects.filter(post__id=ps.id, likes__gte=1).count()
        current_user_like = Like.objects.filter(post__id=ps.id, post__user__id=ps.user.id, sender_id=request.user.id).first()
        if current_user_like:
            data['current_user_react'] = current_user_like.likes
        else:
            data['current_user_react'] = 0
        data['id']          = ps.id
        data['user_id']     = ps.user.id
        data['username']    = ps.user.username
        data['post_status'] = ps.post_status
        data['caption']     = ps.caption
        data['location']    = ps.location
        if ps.upload_file:
            data['upload_file']  = ps.upload_file
        if ps.upload_img_file:
            data['upload_img_file'] = ps.upload_img_file
        data['lat']         = ps.latitude
        data['long']        = ps.longitude
        data['created_at']  = ps.created_at
        data_list.append(data)
    context = {'user_all_posts' : data_list}
    return render(request,"home/profile.html", context)


def editprofileView(request, id):
    
    if request.method == "POST":
        image = request.FILES.get('image')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        bio = request.POST.get('bio')
        postsnum =  Profile.objects.filter(user_id =id).count()
        if postsnum == 0:
            obj = Profile()
        else:
            obj = Profile.objects.get(user_id=id)
        
        if image is not None:
            # delete old if exists
            import os
            if os.path.exists(os.path.join(settings.MEDIA_ROOT,str(obj.image))):
                os.remove(os.path.join(settings.MEDIA_ROOT,str(obj.image)))
            # using now() to get current time
            current_time = datetime.datetime.now()
            image.name = str(id)+"_"+str(current_time)+"_"+image.name
            obj.image = image
        obj.first_name = first_name
        obj.last_name = last_name
        obj.phone = phone
        obj.address = address
        obj.bio = bio
        obj.user_id = id
        obj.save()

        return redirect('userprofile')

    if request.method == "GET":
        postsnum =  Profile.objects.filter(user_id =id).count()
        if postsnum == 0:
            profile= Profile()
        else:
            profile = Profile.objects.get(user_id=id)
        # profile = Profile.objects.all()
        context = {'profile':profile}
        return render(request, "home/edit-profile.html", context)



def addpost(request):
    sign = 0
   
    if request.method == "POST":
        data        = request.POST
        lat         = data.get('lat')
        lng         = data.get('lng')
        caption     = data.get('caption')
        upload_file = request.FILES.get('img-vid')
       
        if lat and lng is None:
            return HttpResponse("Please turn on you location.")
        try:
            # for get current location and address 
            address, lat, lng = get_current_location(lat,lng)
            # save data
            obj = Posts()
            current_time = datetime.datetime.now()
            if check_extention(upload_file) in FILE_EXTENTION:
                upload_file.name = str(request.user.id)+"_"+str(current_time)+"_"+upload_file.name
                obj.upload_img_file = upload_file
                
            else:
                upload_file.name = str(request.user.id)+"_"+str(current_time)+"_"+upload_file.name
                obj.upload_file = upload_file
          
            obj.user        = request.user
            obj.caption     = caption
            obj.latitude    = lat
            obj.longitude   = lng
            obj.location    = address
        
            obj.save()
            sign = 0
            return render(request, "home/index.html", {'sign': sign})
            # return redirect('home')
        except Exception as e:
            return HttpResponse("Invalid location api key.")
    
    else:
        sign = 3
        return render(request, "home/index.html", {'sign': sign})



def userViewProfileView(request, id):
    
    if request.method == "GET":
        try:
            user  = User.objects.get(id=id)
            friend_rqst =  FriendRequest.objects.filter(sender_id=request.user.id).first()
        except User.DoesNotExist:
            return HttpResponse(" Sorry that User doesn't exist.")

        if user:
            
            posts = Posts.objects.filter(user__id=id, status="Enable")

            # defining state of template variables
            is_self = True
            userr = request.user

            if userr.is_authenticated and userr!=user:
                is_self = False
            elif not userr.is_authenticated:
                is_self = False
            # if check friend request
            rqst_status = True
            if friend_rqst:
                rqst_status = friend_rqst.is_active

            context = {
                'user':user, "posts": posts,"is_self":is_self,
                "rqst_status" : rqst_status
                }

            return render(request, "home/user-view-profile.html", context)





def addLikeByUser(request):
    if request.is_ajax():
        id      = int(request.POST.get('id'))
        post_id = int(request.POST.get('post_id'))
        ps      = Posts.objects.filter(user__id=id, id=post_id).first()
        user    = User.objects.get(id=id)
        like    = Like()
        like.sender =  request.user
        like.post   =  ps

        likes_count = Like.objects.filter(post__id=post_id).aggregate(Max('likes'))
        like_obj    = Like.objects.filter(post__id=post_id, post__user__id=user.id, sender_id=request.user.id).first()

        if like_obj:
            if  like_obj.likes == 0:
                like_obj.likes = 1
            else:
                like_obj.likes = 0
            like_obj.save()
        else:
            if likes_count['likes__max'] is None:
                count = 0
            else:
                count = 1
                
            like.likes = count

            like.save()

        results = {}
        results["status"]  = True
        results["message"] =  "Successs"
        data = json.dumps(results)
        # return redirect('/')
    else:
        data = 'No record found!'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

# chat
@login_required(login_url="/login/")
def message_chat(request):
    # all_posts = Posts.objects.filter(status="Enable").order_by("-id")
    # context = {'all_posts' : all_posts}
    return render(request,"home/chat.html")




def profileView(request):
    user_all_posts =  Posts.objects.filter(user__id=request.user.id, status="Enable").order_by("-id")
    data_list = []
    for ps in user_all_posts:
        data = {}
        data['likes_count'] = Like.objects.filter(post__id=ps.id, likes__gte=1).count()
        data['id']          = ps.id
        data['user_id']     = ps.user.id
        data['username']    = ps.user.username
        data['post_status'] = ps.post_status
        data['caption']     = ps.caption
        data['location']    = ps.location
        if ps.upload_file:
            data['upload_file']  = ps.upload_file
        if ps.upload_img_file:
            data['upload_img_file'] = ps.upload_img_file
        data['lat']         = ps.latitude
        data['long']        = ps.longitude
        data['created_at']  = ps.created_at
        data_list.append(data)
    context = {'user_all_posts' : data_list}
    return render(request,"home/profile.html", context)



@login_required
def send_friend_request(request):
    if request.is_ajax():
        data = json.load(request)
        if data['status'] == "add_request":
            from_user = request.user
            to_user = User.objects.get(id=data['id'])
            friend_request, created = FriendRequest.objects.get_or_create(sender=from_user, reciever=to_user)
            if created:
                return JsonResponse({"status":True,"message" :"Request sent successfully."})

        else:
            try:
                FriendRequest.objects.get(sender_id=request.user.id).delete()
            except Exception as e:
                return JsonResponse({"status":False,"message" :str(e)})

            return JsonResponse({"status":True,"message" :"Request cancelled."})



@login_required
def accept_friend_request(request):
    try:
        friend_request = FriendRequest.objects.get(sender_id=10)
        # try:
        #     friend_list = FriendList.objects.filter(user=request.user).first()
        # except FriendList.DoesNotExist:
        #     return JsonResponse({"status":False,"message" :"Record deos not exists."})
        # friend_list = FriendList.objects.filter(user=request.user).first()

        friend_list_obj =  FriendList.objects.create(user = request.user)
        friend_list_obj.friends.add(friend_request.sender_id)
        friend_request.delete()
        return redirect('profile')

    except FriendRequest.DoesNotExist:
        return JsonResponse({"status":False,"message" :"Record deos not exists."})
   

# for cancel the request
@login_required
def decline_friend_request(request, id):
    frequest = FriendRequest.objects.filter(sender=request.user,receiver=request.user.id).first()
    frequest.delete()
    return redirect('profile')

# ajax
# view increase
def view_increase(request):
    if request.method == "POST" and request.is_ajax():
        pid = request.POST.get('pid')
        pviewnum = request.POST.get('viewnum')
        print(pid, pviewnum)
        post = Posts.objects.get(id = pid)
        post.views = pviewnum
        post.save()
        msg = True
        return JsonResponse({"msg": msg}, status=200)

# comment save
def comment_save(request):
    if request.method == "POST" and request.is_ajax():
        pid = request.POST.get('pid')
        comment = request.POST.get('comment')
        user_id = request.POST.get('user_id')
        print(pid, comment, user_id)
        com = Comments()
        com.post_id = pid
        com.comment = comment
        com.user_id = user_id
        com.save()
        msg = True
        return JsonResponse({"msg": msg}, status=200)
 

