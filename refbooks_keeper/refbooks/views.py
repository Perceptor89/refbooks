from datetime import datetime
from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Refbook
from .permissions import IsOwnerOrReadOnly
from .serializers import RefbookSerializer, UserSerializer, ElementSerializer


class RefbookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Refbook.objects.all()
    serializer_class = RefbookSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly
    ]

    def get_version(self, request):
        refbook = self.get_object()
        req_ver_name = request.query_params.get('version')

        if req_ver_name:
            query = refbook.version_set.filter(name=req_ver_name)
        else:
            curr_date = datetime.now().date()
            query = refbook.version_set.filter(start_date__lte=curr_date)
        return query.latest('start_date') if query.exists() else None

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        ver_starts = request.query_params.get('date')
        if ver_starts:
            queryset = queryset.filter(version__start_date__lte=ver_starts)

        # page = self.paginate_queryset(queryset)
        # if page is not None:
        #     serializer = self.get_serializer(page, many=True)
        #     return self.get_paginated_response(serializer.data)

        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response({'refbooks': serializer.data})
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True)
    def elements(self, request, pk=None):
        target_ver = self.get_version(request)

        if target_ver:
            query = target_ver.element_set.all()
            serializer = ElementSerializer(query, many=True)
            return Response({'elements': serializer.data})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True)
    def check_element(self, request, pk=None):
        target_ver = self.get_version(request)
        code = request.query_params.get('code')
        value = request.query_params.get('value')

        if target_ver:
            query = target_ver.element_set.all()
            query = query.filter(code=code) if code is not None else query
            query = query.filter(value=value) if value is not None else query
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

        if query.exists():
            serializer = ElementSerializer(query, many=True)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
