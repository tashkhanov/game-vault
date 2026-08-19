from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

user = get_user_model()


class Genre(models.Model):
    name = models.CharField('Название', max_length=50)
    photo = models.ImageField('Фото', upload_to='genre_images/', blank=True, null=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def get_absolute_url(self):
        return reverse('genre', kwargs={'pk': self.pk})

    def __str__(self):
        return self.name


class Game(models.Model):
    title = models.CharField('Название', max_length=200)
    short_description = models.CharField('Короткое описание', max_length=350, blank=True, null=True)
    description = models.TextField('Описание', blank=True)
    released = models.CharField(max_length=30, verbose_name='Дата выхода', null=True, blank=True)
    developer = models.CharField('Разработчик', max_length=100, blank=True, null=True)
    publisher = models.CharField(max_length=100, verbose_name='Издатель', null=True, blank=True)
    platform = models.CharField('Платформа', max_length=30, null=True, blank=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр', null=True, blank=True)
    trailer = models.TextField('HTML-код трейлера', blank=True, null=True)
    image = models.ImageField('Фото', upload_to='games_images/', blank=True, null=True)

    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('game', kwargs={'pk': self.pk})

    def get_genres_names(self):
        return ', '.join(genre.name for genre in self.genre.all())

    class Meta:
        verbose_name = 'Игра'
        verbose_name_plural = 'Игры'


class SystemRequirements(models.Model):
    game = models.OneToOneField(Game, on_delete=models.CASCADE, verbose_name='Игра')
    op_system = models.CharField('Операционная система', max_length=150)
    processor = models.CharField('Процессор', max_length=150)
    op_memory = models.CharField('Оперативая память (ОЗУ)', max_length=150)
    video_card = models.CharField('Видеокарта', max_length=150)
    hard_memory = models.CharField('Память на диске', max_length=150)

    def __str__(self):
        return f'Систменые требования игры {self.game.title}'

    class Meta:
        verbose_name = 'Системные требования'
        verbose_name_plural = 'Системные требования'


class GameImage(models.Model):
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='images', verbose_name='Игра')
    image = models.ImageField('Доп. изображение', upload_to='games_images/extra/')

    class Meta:
        verbose_name = 'Изображение игры'
        verbose_name_plural = 'Изображения игр'

    def __str__(self):
        return f'Изображение {self.game.title}'


class Mod(models.Model):
    game = models.ForeignKey(Game, verbose_name='Игра', on_delete=models.CASCADE, related_name='mods')
    title = models.CharField('Название мода', max_length=200)
    description = models.TextField('Описание', blank=True)
    file = models.FileField('Файл мода', upload_to='mods/', blank=False, null=False)
    created_at = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Мод'
        verbose_name_plural = 'Моды'

    def __str__(self):
        return f'{self.title} для {self.game.title}'


class News(models.Model):
    title = models.CharField('Заголовок', max_length=300)
    short_content = models.CharField('Короткое содержание', max_length=300, blank=True, null=True)
    content = models.TextField('Содержание')
    banner = models.ImageField('Баннер', upload_to='news_banners/', blank=True, null=True)
    author = models.ForeignKey(user, verbose_name='Автор', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField('Дата публикации', auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('new', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    news = models.ForeignKey(News, verbose_name='Новость', on_delete=models.CASCADE, null=True, blank=True)
    game = models.ForeignKey(Game, verbose_name='Игра', on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.user.username}: {self.content[:30]}'


