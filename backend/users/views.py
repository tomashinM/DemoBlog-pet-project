from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from users.models import User
from users.serializers import (
    LoginSerializer,
    ProfileSerializer,
    UserSerializer,
)
from utils.parsers import get_custom_parser
from utils.wrappers import wrap_response, wrap_schema


class UserViewSet(mixins.CreateModelMixin, GenericViewSet):
    """
    API endpoints for new users
    """

    object_name = "user"
    serializer_class = UserSerializer
    parser_classes = [get_custom_parser(object_name)]

    @wrap_response(object_name)
    @wrap_schema(object_name)(serializer_class, serializer_class, 201, [400])
    def create(self, request, *args, **kwargs):
        """
        Registration endpoint
        """
        return super().create(request, *args, **kwargs)

    @wrap_response(object_name)
    @wrap_schema(object_name)(LoginSerializer, serializer_class)
    @action(detail=False, methods=["post"])
    def login(self, request):
        """
        Login endpoint
        """
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.context["user"]

        return Response(UserSerializer(user).data)

    @action(detail=False, methods=["get"], url_path="verify/(?P<token>[^/.]+)")
    def verify(self, request, token=None):
        """
        Verification endpoint
        """
        try:
            user = User.objects.get(verification_token=token, is_active=False)
        except User.DoesNotExist:
            raise PermissionDenied()
        user.is_active = True
        user.verification_token = None
        user.save()
        return Response()


class UserView(APIView):
    """
    API endpoints for authenticated users
    """

    object_name = "user"
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    parser_classes = [get_custom_parser(object_name)]

    @wrap_response(object_name)
    @wrap_schema(object_name)(response_serializer=serializer_class)
    def get(self, request, *args, **kwargs):
        """
        Access to current user info
        """
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)

    @wrap_response(object_name)
    @wrap_schema(object_name, partial=True)(serializer_class, serializer_class)
    def put(self, request, *args, **kwargs):
        """
        Update current user info
        """
        serializer = UserSerializer(
            self.request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ProfileViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    """
    API endpoints for users profiles
    """

    object_name = "profile"
    lookup_url_kwarg = "username"
    lookup_field = "username"
    serializer_class = ProfileSerializer

    @wrap_response(object_name)
    @wrap_schema(object_name)(response_serializer=serializer_class)
    def retrieve(self, request, *args, **kwargs):
        """
        Get profile of a user
        """
        return super().retrieve(request, *args, **kwargs)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return User.objects.none()
        queryset = User.objects.all()
        if self.action == "follow":
            return queryset.exclude(pk=self.request.user.pk)
        return queryset

    @wrap_response(object_name)
    @wrap_schema(object_name)(response_serializer=serializer_class)
    @action(detail=True, methods=["POST", "DELETE"])
    def follow(self, request, username=None):
        """
        Follow/Unfollow a user
        """
        if request.user.is_anonymous:
            raise PermissionDenied()
        user = self.get_object()
        if request.method == "DELETE":
            request.user.following.remove(user)
        else:
            request.user.following.add(user)
        return Response(self.get_serializer(user).data)
