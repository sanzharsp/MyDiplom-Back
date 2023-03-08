from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)

import jwt
from .Manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    # Каждому пользователю нужен понятный человеку уникальный идентификатор,
    # который мы можем использовать для предоставления User в пользовательском
    # интерфейсе. Мы так же проиндексируем этот столбец в базе данных для
    # повышения скорости поиска в дальнейшем.
    username = models.CharField(db_index=True, max_length=255, verbose_name = 'Логин', unique=True)
    first_name = models.CharField(db_index=True, verbose_name='Аты', max_length=150)
    last_name = models.CharField(db_index=True, verbose_name='Тегі', max_length=150)
    surname = models.CharField(db_index=True, verbose_name='Әкесінің аты', max_length=150)
    email = models.EmailField(db_index=True, verbose_name='электрондық пошта', unique=True)
    date_create = models.DateTimeField(auto_now_add=True)
    # Когда пользователь более не желает пользоваться нашей системой, он может
    # захотеть удалить свой аккаунт. Для нас это проблема, так как собираемые
    # нами данные очень ценны, и мы не хотим их удалять :) Мы просто предложим
    # пользователям способ деактивировать учетку вместо ее полного удаления.
    # Таким образом, они не будут отображаться на сайте, но мы все еще сможем
    # далее анализировать информацию.
    is_active = models.BooleanField(default=True)

    # Этот флаг определяет, кто может войти в административную часть нашего
    # сайта. Для большинства пользователей это флаг будет ложным.
    is_staff = models.BooleanField(default=False, verbose_name='жүйеге администраторы')

    # Временная метка создания объекта.
    created_at = models.DateTimeField(auto_now_add=True)

    # Временная метка показывающая время последнего обновления объекта.
    updated_at = models.DateTimeField(auto_now=True)

    # Дополнительный поля, необходимые Django
    # при указании кастомной модели пользователя.

    # Свойство USERNAME_FIELD сообщает нам, какое поле мы будем использовать
    # для входа в систему. В данном случае мы хотим использовать почту.
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'surname']

    # Сообщает Django, что определенный выше класс UserManager
    # должен управлять объектами этого типа.
    objects = UserManager()

    class Meta:
        ordering = ['id']
        verbose_name = 'қолданушы'
        verbose_name_plural = 'Қолданушылар'

    def __str__(self):
        return "{}".format(self.username)

    @property
    def token(self):
        """
        Позволяет получить токен пользователя путем вызова Author.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """
        return self.username

    def get_short_name(self):
        """ Аналогично методу get_full_name(). """
        return self.username

    def _generate_jwt_token(self):
        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """
        dt = datetime.now() + timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%S'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token


class JK(models.Model):
    name = models.CharField(db_index=True, verbose_name='Тұрғын үй аты', max_length=255, unique=True)

    class Meta:
        ordering = ['-id']
        verbose_name='Тұрғын үй'
        verbose_name_plural='Тұрғын үй аты'
    
    def __str__(self):
        return "{}".format(self.name)


class QrCode(models.Model):
    qr = models.CharField(db_index=True, verbose_name='Qr код нәтижелері', max_length=255)
    id_in_electron = models.IntegerField(unique=True, verbose_name='id есептегіш',)

    class Meta:
        ordering = ['-id']
        verbose_name='электр есептегіш'
        verbose_name_plural='электр есептегіштер'

    def __str__(self):
        return "{}".format(self.qr)


class Profile(models.Model):
    user = models.ForeignKey(User, verbose_name='Қолднушы', on_delete=models.CASCADE)
    QrCode = models.ForeignKey(QrCode,blank = True,null = True, verbose_name='электр есептегіш', on_delete=models.CASCADE)
    JK = models.ForeignKey(JK,null = True, verbose_name='Жк', on_delete=models.CASCADE)
    room_number =  models.CharField(db_index=True, verbose_name='Пәтер нөмірі', max_length=255, unique=True)
    
    
    class Meta:
        ordering = ['-id']
        verbose_name='Қолднушы'
        verbose_name_plural='Қолднушылар'

    def __str__(self):
        return "{}".format(self.user)
    

LIKE_CHOICES = (
    ('Like', True),
    ('Unlike', False),
) 

class News(models.Model):
    name = models.CharField(verbose_name="Жаңалық аты",max_length=255)
    subNamed=models.CharField(verbose_name="Жаңалық аты",max_length=255,default="_")
    description = models.TextField(verbose_name= "жаңалық тексті")
    image = models.ImageField(verbose_name="Жаңалық фотосы")
    likes = models.ManyToManyField(User,blank=True, verbose_name='Лайктар' ,related_name='likes')
    date_create_news = models.DateTimeField(auto_now_add=True,verbose_name='Жаңалықтын құрылған күні')
    value = models.CharField(choices=LIKE_CHOICES, max_length=8,verbose_name='лайк статусы',default='Like')
    class Meta:
        ordering = ['-id']
        verbose_name='Жаңалық'
        verbose_name_plural='Жаңалықтар'

    def __str__(self):
        return "{}".format(self.name)