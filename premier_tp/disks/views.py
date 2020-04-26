from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from .models import artist,album,track
from .forms import search_form

# Create your views here.

def home(request):

    albums = album.objects.all()
    return render(request,'disks/home.html',{'derniers_albums' : albums})


def lire(request,id):
    albums = get_object_or_404(album, id=id)
    Liste_album = track.objects.filter(album_id = id)
    return render(request, 'disks/Lire_album.html', {'Liste_album': Liste_album,'the_album' : albums})


def search(request):
    form = search_form(request.POST or None)

    if form.is_valid():
        # Ici nous pouvons traiter les données du formulaire
        search= form.cleaned_data['search']
        search_albums = album.objects.filter(Title__contains=search)
    # Quoiqu'il arrive, on affiche la page du formulaire.
    return render(request, 'disks/home.html', {'derniers_albums': search_albums})