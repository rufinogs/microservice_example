from rest_framework import serializers


class CustomerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=45, required=True)
    surname = serializers.CharField(max_length=45, required=True)
    last_name = serializers.CharField(max_length=45)
    phone = serializers.CharField(max_length=45)
    email = serializers.EmailField()


class CustomerPutSerializer(serializers.Serializer):
    old_user = serializers.DictField(required=True)
    new_user = serializers.DictField(required=True)

    def validate(self, data):
        old_user = data.get("old_user")
        new_user = data.get("new_user")
        if not old_user:
            raise serializers.ValidationError("Previous user data not provided")
        if not new_user:
            raise serializers.ValidationError("New user data not provided")
        old_user_serialized = CustomerDictSerializer(data=old_user)
        new_user_serialized = CustomerDictSerializer(data=new_user)
        old_user_serialized.is_valid(raise_exception=True)
        new_user_serialized.is_valid(raise_exception=True)
        return data




class CustomerDictSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=45, required=False)
    surname = serializers.CharField(max_length=45, required=False)
    last_name = serializers.CharField(max_length=45, required=False)
    phone = serializers.CharField(max_length=45, required=False)
    email = serializers.EmailField(required=False)
