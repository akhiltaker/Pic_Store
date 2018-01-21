from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404
from .models import Album,Picture
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import AlbumForm, PictureForm, UserForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
# Create your views here.
def index(request):
    if not request.user.is_authenticated():
        return render(request, 'photo/index.html')
    else:
        albums = Album.objects.filter(user=request.user).order_by('-pk')
        picture_results = Picture.objects.all()
        query = request.GET.get("q")
        if query:
            albums = albums.filter(
                Q(album_title__icontains=query)
            ).distinct()
            picture_results = picture_results.filter(
                Q(pic_title__icontains=query)
            ).distinct()
            return render(request, 'photo/index.html', {
                'albums': albums,
                'songs': picture_results,
            })
        else:
            return render(request, 'photo/index.html', {'albums': albums})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return redirect('/')
            else:
                return render(request, 'photo/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'photo/login.html', {'error_message': 'Invalid login'})
    return render(request, 'photo/login.html')

def register(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                albums = Album.objects.filter(user=request.user)
                return redirect('photo:index')
    context = {
        "form": form,
    }
    return render(request, 'photo/register.html', context)

def logout_user(request):
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return redirect('photo:login_user')

def create_album(request):
    if not request.user.is_authenticated():
        return redirect('photo:login_user')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.user = request.user
            album.album_logo = request.FILES['album_logo']
            album.save()
            return redirect('photo:detail', album_id=album.id)
        context = {
            "form": form,
        }
        return render(request, 'photo/create_album.html', context)

def detail(request, album_id):
    if not request.user.is_authenticated():
        return redirect('photo:login_user')
    else:
        user = request.user
        album = get_object_or_404(Album, pk=album_id)
        return render(request, 'photo/detail.html', {'album': album, 'user': user})

def create_picture(request, album_id):
    form = PictureForm(request.POST or None, request.FILES or None)
    album = get_object_or_404(Album, pk=album_id)
    if form.is_valid():
        albums_pictures = album.picture_set.all()
        for s in albums_pictures:
            if s.pic_title == form.cleaned_data.get("pic_title"):
                context = {
                    'album': album,
                    'form': form,
                    'error_message': 'You already added that picture',
                }
                return render(request, 'photo/create_picture.html', context)
        song = form.save(commit=False)
        song.album = album
        song.save()
        return redirect('photo:detail', album_id=album.id)
    context = {
        'album': album,
        'form': form,
    }
    return render(request, 'photo/create_picture.html', context)

def delete_album(request, album_id):
    album = Album.objects.get(pk=album_id)
    album.delete()
    albums = Album.objects.filter(user=request.user)
    return redirect('/')

def favorite(request, song_id):
    pic = get_object_or_404(Picture, pk=song_id)
    try:
        if pic.is_favorite:
            pic.is_favorite = False
        else:
            pic.is_favorite = True
        pic.save()
    except (KeyError, Picture.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

def favorite_album(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        if album.is_favorite:
            album.is_favorite = False
        else:
            album.is_favorite = True
        album.save()
    except (KeyError, Album.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})

def delete_pic(request, album_id, song_id):
    album = get_object_or_404(Album, pk=album_id)
    song = Picture.objects.get(pk=song_id)
    song.delete()
    return redirect('photo:detail',album_id)
