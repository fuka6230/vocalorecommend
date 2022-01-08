from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from vocalo.return_result import recommend, recom_from_artist
from django_user_agents.utils import get_user_agent
    
def tracks(request):
    return render(request, 'all_tracks.csv', {})

def artists(request):
    return render(request, 'all_artists.csv', {})

def home(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile:
        return render(request, 'home_mobile.html', {})
    else:
        return render(request, 'home.html', {})

def result(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile:
        return render(request, 'result_mobile.html', {})
    else:
        return render(request, 'result.html', {})

def form_name_view(request):
    user_agent = get_user_agent(request)
    name = request.POST.get('name', False)
    if recommend.title_to_artist(name) == 'error':
        result_name = 'まだその曲に対応していません'
        
    else:
        result_name = recommend.title_to_artist(name)
    context = {
        'result_name': result_name
        }
    if user_agent.is_mobile:
        return render(request, 'result_mobile.html', context)
    else:
        return render(request, 'result.html', context)

def form_artist_view(request):
    user_agent = get_user_agent(request)
    artist_name = request.POST['artist']
    if recom_from_artist.artist_to_artist(artist_name) == 'error':
        result_name = 'まだそのアーティストまたはボカロPに対応していません'
        
    else:
        result_name = recom_from_artist.artist_to_artist(artist_name)
    context = {
        'result_name': result_name
        }
    if user_agent.is_mobile:
        return render(request, 'result_mobile.html', context)
    else:
        return render(request, 'result.html', context)
