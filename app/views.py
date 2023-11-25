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




    team = Team.objects.all().order_by('-counter')[:4]


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
    comments = Comments.objects.filter(teamobject = team)
    contex = {
        'info':num_vid,
        'team':team,
        'comments':comments,
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
    team = Team.objects.all()
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

    paginator = Paginator(team,3)
    page_number = 1

    if request.GET.get('page'):
        page_number = int(request.GET.get('page'))

    if query:
        team = Team.objects.filter(title__icontains=query)
        contex={'team':team}
        return render(request, 'all_videos.html', contex)
    contex = {
        'team':paginator.page(page_number),
        'pages':paginator.page_range,
    }
    return render(request,'all_videos.html',contex)

def about(request):
    return render(request,'about.html')
