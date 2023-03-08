from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ObjectDoesNotExist




class RegistrationSerializer(serializers.ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """

    # Убедитесь, что пароль содержит не менее 8 символов, не более 128,
    # и так же что он не может быть прочитан клиентской стороной


    password = serializers.CharField(
        max_length=128,
        min_length=4,
        write_only=True,
        label="Пароль"

    )
    nameResidentialComplex = serializers.CharField(
        max_length=128,
        min_length=0,
        write_only=True,
        label="Жк аты"

    )



    roomNumber = serializers.IntegerField(
        write_only=True,
        label="Квартира номері"

    )



    # Клиентская сторона не должна иметь возможность отправлять токен вместе с
    # запросом на регистрацию. Сделаем его доступным только на чтение.


    class Meta:
        model = User
        # Перечислить все поля, которые могут быть включеWны в запрос
        # или ответ, включая поля, явно указанные выше.
        fields = [
        'username',
        'first_name',
        'last_name',
        'surname',
        'email', 
        'password',
        'nameResidentialComplex',
        'roomNumber',
        ]

        


class LogoutSerilizers(serializers.Serializer):
    refresh_token = serializers.CharField(
        write_only=True,
        label="Refresh токен"

    )

class JKSerilizer(serializers.ModelSerializer):
        
    class Meta:
        model = JK
        fields = '__all__'


class UserSerilizer(serializers.ModelSerializer):
    date_create = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model = User
        fields = 'first_name', 'last_name','surname', 'username', 'email', 'date_create'

class AuthorizateSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        refresh = self.get_token(user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['user'] =UserSerilizer(User.objects.get(username=user)).data
        return data


class QrCodeSerilizer(serializers.ModelSerializer):
    class Meta:
        model = QrCode
        fields = ('qr','id_in_electron',)

class ProfileSerilizer(serializers.ModelSerializer):
    QrCode = QrCodeSerilizer()
    JK = JKSerilizer()
    class Meta:
        model = Profile
        fields = ('user','QrCode','room_number','JK')



class ProfileQrCodeSerilizerAddUser(serializers.ModelSerializer):
    user =UserSerilizer()
    QrCode = QrCodeSerilizer()
    JK = JKSerilizer()
    class Meta:
        model = Profile
        fields = '__all__'


class QrCodeSerilizerAdd(serializers.Serializer):
    username = serializers.CharField(
        write_only=True,
        label="username"

    )

    id_in_electron = serializers.IntegerField(

        write_only=True,
        label="ID счетчика"

    )
    class Meta:
        fields = ('user_id','id_in_electron',)



class LikeSerilizer(serializers.ModelSerializer):
    post = serializers.IntegerField(
        label=("Id поста"),
        write_only=True)
    class Meta:
        model = News
        fields = ( 'post',)



class NewsSerilizer(serializers.ModelSerializer):
    
    
    class Meta:
        model = News
        fields = '__all__'