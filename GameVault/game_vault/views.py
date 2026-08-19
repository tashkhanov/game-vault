from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q


def main_page(request):
    last_games = Game.objects.all().order_by('-created_at')
    genres = Genre.objects.all()
    last_news = News.objects.all().order_by('-created_at')
    query = request.GET.get('q', '')

    if query:
        last_games = last_games.filter(Q(title__icontains=query) | Q(short_description__icontains=query))
        last_news = last_news.filter(Q(title__icontains=query) |
                                     Q(short_content__icontains=query) |
                                     Q(content__icontains=query))

    context = {
        'title': 'GameVault',
        'last_games': last_games,
        'genres': genres,
        'last_news': last_news,
        'query': query
    }
    return render(request, 'game_vault/index.html', context)


def games_page(request):
    games = Game.objects.all()
    genres = Genre.objects.all()
    last_games = Game.objects.all().order_by('-created_at')
    query = request.GET.get('q', '')

    if query:
        games = games.filter(Q(title__icontains=query) | Q(short_description__icontains=query))

    context = {
        'title': 'GameVault - игры',
        'games': games,
        'last_games': last_games,
        'genres': genres,
        'query': query
    }
    return render(request, 'game_vault/games.html', context)


def game_by_genre(request, pk):
    games = Game.objects.filter(genre=pk).order_by('-created_at')
    genre = Genre.objects.get(pk=pk)
    genres = Genre.objects.all().exclude(pk=genre.pk)
    last_games = Game.objects.all().order_by('-created_at')
    context = {
        'genre_name': genre.name,
        'title': f'GameVault - {genre.name}',
        'games': games,
        'genres': genres,
        'last_games': last_games
    }

    return render(request, 'game_vault/games.html', context)


def news_page(request):
    news = News.objects.all()
    last_news = News.objects.all().order_by('-created_at')
    query = request.GET.get('q', '')

    if query:
        news = news.filter(Q(title__icontains=query) | Q(short_content__icontains=query))

    context = {
        'title': 'GameVault - новости',
        'last_news': last_news,
        'news': news,
        'query': query
    }
    return render(request, 'game_vault/news.html', context)


def mods_page(request):
    mods = Mod.objects.all()
    query = request.GET.get('q', '')

    if query:
        mods = mods.filter(
            Q(game__title__icontains=query) | Q(title__icontains=query) | Q(description__icontains=query))

    context = {
        'mods': mods,
        'query': query,
        'title': f'GameVault - моды',
    }
    return render(request, 'game_vault/mods.html', context)


def game_detail(request, pk):
    game = Game.objects.get(pk=pk)
    system = SystemRequirements.objects.get(game=game)
    same_games = Game.objects.filter(genre__in=game.genre.all()).distinct().exclude(pk=game.pk)
    news = News.objects.all().order_by('-created_at')
    images = game.images.all()
    comments = Comment.objects.filter(game=game)

    context = {
        'game': game,
        'system': system,
        'title': f'GameVault - {game.title}',
        'same_games': same_games,
        'news': news,
        'images': images,
        'comments': comments
    }
    return render(request, 'game_vault/full-info-game.html', context)


def new_detail(request, pk):
    new = News.objects.get(pk=pk)
    last_games = Game.objects.all().order_by('-created_at')
    last_news = News.objects.all().order_by('-created_at').exclude(pk=new.pk)
    comments = Comment.objects.filter(news=new)

    context = {
        'new': new,
        'title': f'GameVault - {new.title}',
        'last_games': last_games,
        'last_news': last_news,
        'comments': comments
    }
    return render(request, 'game_vault/full-info-new.html', context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')

    last_games = Game.objects.all().order_by('-created_at')
    genres = Genre.objects.all()
    last_news = News.objects.all().order_by('-created_at')

    return render(request, 'game_vault/index.html', {
        'last_games': last_games,
        'genres': genres,
        'last_news': last_news,
    })


def logout_view(request):
    logout(request)
    return redirect('main')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('main')

    if request.method == 'POST':
        username = request.POST.get('username')
        p1 = request.POST.get('password')
        p2 = request.POST.get('confirm_password')

        if p1 != p2:
            messages.error(request, 'Пароли не совпадают.')
            return redirect('main')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Такой логин уже существует.')
            return redirect('main')

        user = User.objects.create_user(
            username=username,
            password=p1,
            email=request.POST.get('email'),
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name')
        )

        profile = Profile.objects.create(user=user)
        avatar = request.FILES.get('avatar')
        if avatar:
            profile.avatar = avatar
            profile.save()

        login(request, user)
        return redirect('main')

    return render(request, 'game_vault/index.html')


def add_comment(request, target_type, target_id):
    if request.method == 'POST' and request.user.is_authenticated:
        content = request.POST.get('content', '').strip()
        if not content:
            return redirect(request.META.get('HTTP_REFERER', '/'))

        if target_type == 'game':
            game = get_object_or_404(Game, pk=target_id)
            Comment.objects.create(user=request.user, game=game, content=content)
            return redirect('game', pk=game.pk)

        elif target_type == 'news':
            news = get_object_or_404(News, pk=target_id)
            Comment.objects.create(user=request.user, news=news, content=content)
            return redirect('new', pk=news.pk)

    return redirect('/')


def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
    if request.method == 'POST':
        new_text = request.POST.get('content', '').strip()
        if new_text:
            comment.content = new_text
            comment.save()

    if comment.game:
        return redirect('game', pk=comment.game.pk)
    elif comment.news:
        return redirect('new', pk=comment.news.pk)
    return redirect('/')


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
    if comment.game:
        redirect_pk = comment.game.pk
        redirect_to = 'game'
    elif comment.news:
        redirect_pk = comment.news.pk
        redirect_to = 'new'
    else:
        return redirect('/')

    comment.delete()
    return redirect(redirect_to, pk=redirect_pk)
