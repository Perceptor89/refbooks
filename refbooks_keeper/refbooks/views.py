from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Refbook
from .permissions import IsOwnerOrReadOnly
from .serializers import RefbookSerializer, UserSerializer


class RefbookViewSet(viewsets.ModelViewSet):
    queryset = Refbook.objects.all()
    serializer_class = RefbookSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        ver_starts = request.query_params.get('date')
        if ver_starts:
            queryset = queryset.filter(version__start_date__lte=ver_starts)

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response({'refbooks': serializer.data})


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
