from rest_framework import viewsets
from apps.products.serializers.profiles import ProductProfileCreateSerializer
from apps.products.models import ProductProfile

class ProductProfileViewSet(viewsets.ModelViewSet):
    queryset = ProductProfile.objects.filter()
    lookup_field = "id"

    serializer_action_classes = {
        'create': ProductProfileCreateSerializer,
    }

    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class