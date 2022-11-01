from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Refbook
from .permissions import IsOwnerOrReadOnly
from .serializers import RefbookSerializer, UserSerializer, ElementSerializer


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

        if queryset:
            serializer = self.get_serializer(queryset, many=True)
            return Response({'refbooks': serializer.data})
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True)
    def elements(self, request, pk=None):
        refbook = self.get_object()
        req_ver_name = request.query_params.get('version')

        if req_ver_name:
            try:
                target_ver = refbook.version_set.get(name=req_ver_name)
            except Exception:
                return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            curr_date = datetime.now().date()
            target_ver = refbook.version_set.filter(
                start_date__lte=curr_date
            ).latest('start_date')

        if target_ver:
            query = target_ver.element_set.all()
            serializer = ElementSerializer(query, many=True)
            return Response({'elements': serializer.data})
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
