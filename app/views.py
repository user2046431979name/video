from django.shortcuts import render

from .models import *

from django.views.generic.edit import CreateView

from django.urls import reverse_lazy

from django.contrib.auth.forms import UserCreationForm

from django.core.paginator import *

from django.conf import settings

from django.contrib.auth import get_user_model


# Create your views here.

def index(request):
    is_admin = False
    if request.user.is_authenticated:
        try:
            Admin.objects.get(selectedUser=request.user)
            is_admin = True
        except:
            pass


    if request.method == 'POST':
        user = request.user

        team_id = request.POST.get('teamObject')
        teamObject = Team.objects.get(id=team_id)
        try:
            like_object = Like.objects.get(author=user, teamObject=teamObject)
            like_object.delete()

        except Like.DoesNotExist:
             Like.objects.create(author=user, teamObject=teamObject)




    team = Team.objects.annotate(like_count=Count('like')).order_by('-like_count')[:4]


    contex = {
        'team':team,
        'is_admin': is_admin,

    }
    return render(request,'index.html',contex)


def series(request,id):
    if request.method == 'POST':
        text = request.POST.get('text')
        teamobject = Team.objects.get(id = id)
        Comments.objects.create(text = text,teamobject = teamobject,author = request.user)

    num_vid = Videos.objects.filter(teamobject__id = id)

    team = Team.objects.get(id = id)
    comments = Comments.objects.filter(teamobject = team)[::-1]
    num_comm = len(comments)
    contex = {
        'info':num_vid,
        'team':team,
        'comments':comments,
        'num_comm':num_comm,
    }

    return render(request,'series.html',contex)

def detailVideo(request, id):
    video = Videos.objects.filter(teamobject__id=id)
    paginator = Paginator(video, 1)

    page_number = request.GET.get('page', 1)

    try:
        page_number = int(page_number)
    except (TypeError, ValueError):
        page_number = 1

    try:
        rows = paginator.page(page_number)
    except (PageNotAnInteger, EmptyPage):
        rows = paginator.page(1)

    team = Team.objects.get(id=id)
    team.counter += 1
    team.save()

    next_page = rows.next_page_number() if rows.has_next() else 1
    previous_page = rows.previous_page_number() if rows.has_previous() else 1

    context = {
        'rows': rows,
        'team': team,
        'nextP': next_page,
        'previosP': previous_page,
    }
    return render(request, 'detail_video.html', context)
class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def allVideos(request):
   
    if request.method == 'POST':
        user = request.user

        team_id = request.POST.get('teamObject')
        teamObject = Team.objects.get(id=team_id)
        try:
            like_object = Like.objects.get(author=user, teamObject=teamObject)
            like_object.delete()

        except Like.DoesNotExist:
            Like.objects.create(author=user, teamObject=teamObject)
    query = request.GET.get('query')
    popul = request.GET.get('popularity')
    like = request.GET.get('like_filter')
 
    team = Team.objects.all()
    if popul:
        team = Team.objects.order_by('-counter')[:5]
 

    if query:
        team = Team.objects.filter(title__icontains=query)

    
    if like:
        team = Team.objects.annotate(like_count=Count('like')).order_by('-like_count')
        
    
   
    paginator = Paginator(team,6)
    page_number = 1
    if request.GET.get('page'):
        page_number = int(request.GET.get('page'))

    contex = {
        'team':paginator.page(page_number),
        'pages':paginator.page_range,
    }
    return render(request,'all_videos.html',contex)

def about(request):
    return render(request,'about.html')



def contact(request):
    if request.method == "POST":
        fullname = request.POST.get('fullname')
        number = request.POST.get('number')
        text = request.POST.get('text')
        email = request.POST.get('email')
        Reviews.objects.create(fullname=fullname,number=number,email=email,text=text,user=request.user)
    return render(request,'contact.html')