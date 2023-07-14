from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Advertisement

token = 'cba6d56ea6e198070426c99ec0036c3bb806ec2f'


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at',)

    def create(self, validated_data):
        """Метод для создания"""
        validated_data["creator"] = self.context["request"].user
        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""
        num_adv = Advertisement.objects.filter(status='OPEN', creator=self.context["request"].user).count()  # noqa
        if self.initial_data.get('status') in ('OPEN', None) and num_adv > 9:
            raise ValidationError(
                f'Исчерпан лимит открытых объявлений: 10{self.initial_data.get("status")}')  # noqa
        return data
