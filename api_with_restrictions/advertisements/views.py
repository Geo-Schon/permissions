from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import SearchFilter, OrderingFilter
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .filters import AdvertisementFilter
from .models import Advertisement
from .serializers import AdvertisementSerializer

from .permissions import IsOwnerOrReadOnly


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsOwnerOrReadOnly]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['creator', 'status']

    # search_fields = ['status', 'title']
    # ordering_fields = ['id', 'username', 'creator', 'status', 'created_at']

    # TODO: настройте ViewSet, укажите атрибуты для кверисета,
    #   сериализаторов и фильтров

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsOwnerOrReadOnly()]
        return []

    def list(self, request):
        queryset = Advertisement.objects.all()
        queryset = AdvertisementFilter(data=request.GET, queryset=queryset, request=request).qs  # noqa
        serializer = AdvertisementSerializer(queryset, many=True)
        return Response(serializer.data)
