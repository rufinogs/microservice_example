from django.db import IntegrityError
from rest_framework import status as status_codes
from .models import User
from .serializers import CustomerSerializer, CustomerPutSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
import json


class CustomerViewSet(ListCreateAPIView, DestroyAPIView, UpdateAPIView):
    model = User
    queryset = User.objects.all()
    serializer_class = CustomerSerializer
    serializer_put_class = CustomerPutSerializer
    http_method_names = ['get', 'post', 'delete', 'patch']

    # Overwrite the get method to set to my personal choose
    def get(self, request, *args, **kwargs):
        inner_id = kwargs.get("id")
        try:
            if inner_id:
                response, status = list(User.objects.filter(id=inner_id).values()), status_codes.HTTP_200_OK
            else:
                response, status = list(User.objects.all().values()), status_codes.HTTP_200_OK
        except Exception as e:
            response, status = {"detail": "Unknown error"}, status_codes.HTTP_500_INTERNAL_SERVER_ERROR

        return Response(data=response, status=status)

    def post(self, request, *args, **kwargs):
        payload = request.data
        serialized_data = self.serializer_class(data=payload)
        try:
            serialized_data.is_valid(raise_exception=True)
            data = serialized_data.validated_data
            # I use the validated data like kwargs to create the instance
            instance = User.objects.create(**data)
            instance.save()
            response, status = "OK.User created", status_codes.HTTP_201_CREATED
        except ValidationError:
            errors = serialized_data.errors
            response, status = {"detail": errors}, status_codes.HTTP_400_BAD_REQUEST
        except IntegrityError as e:
            response, status = {"detail": "Unknown error"}, status_codes.HTTP_500_BAD_REQUEST

        return Response(data=response, status=status)

    def delete(self, request, *args, **kwargs):
        customer_id = kwargs.get("id")
        if not customer_id:
            response = {"detail": "id for user not provided"}
            return Response(data=response, status=status_codes.HTTP_404_NOT_FOUND)

        try:
            instance = User.objects.get(id=customer_id)
            instance.delete()
            response, status = "OK.User deleted", status_codes.HTTP_200_OK
        except IntegrityError:
            response, status = {"detail": "User doesn't exist"}, 404
        except Exception as e:
            response, status = {"detail": "Unknown error"}, 500

        return Response(data=response, status=200)

    def patch(self, request, *args, **kwargs):
        payload = request.data
        # old_user = payload.get("old_user")
        # new_user = payload.get("new_user")
        # old_user_serialized = self.serializer_put_class(data=old_user)
        # new_user_serialized = self.serializer_put_class(data=new_user)
        try:
            # serialized_data = old_user_serialized
            # serialized_data.is_valid(raise_exception=True)
            # serialized_data = new_user_serialized
            # serialized_data.is_valid(raise_exception=True)
            serialized_data = self.serializer_put_class(data=payload)
            serialized_data.is_valid(raise_exception=True)
            instance = User.objects.filter(**serialized_data.validated_data["old_user"])
            # instance = User.objects.filter(**old_user_serialized.validated_data)

            if len(instance) == 0:
                return Response(data={"detail": "User not found"}, status=status_codes.HTTP_404_NOT_FOUND)
            if len(instance) > 1:
                return Response(data={"detail": "Multiple users. Unique user doesn't exist"},
                                status=status_codes.HTTP_404_NOT_FOUND)
            # instance.update(**new_user_serialized.validated_data)
            instance.update(**serialized_data.validated_data["new_user"])
            response, status = f"User updated with\r\n{json.dumps(serialized_data.validated_data['new_user'])}", status_codes.HTTP_200_OK
        except ValidationError:
            errors = serialized_data.errors
            response, status = {"detail": errors}, status_codes.HTTP_400_BAD_REQUEST
        except IntegrityError:
            response, status = {"detail": "User doesn't exist"}, 404
        except Exception:
            response, status = {"detail": "Unknown error"}, status_codes.HTTP_500_BAD_REQUEST

        return Response(data=response, status=status)
