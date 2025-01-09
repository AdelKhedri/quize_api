from rest_framework import serializers
from django.contrib.auth.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        exclude = ['is_staff', 'is_superuser', 'is_active', 'password', 'groups', 'user_permissions']
        read_only_fields = ['date_joined', 'last_login']


    def create(self, validated_data):
        password = validated_data.pop('password1', None)
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user

    def validate(self, attrs):
        password1 = attrs.get('password1', None)
        password2 = attrs.pop('password2', None)
        if not password2 or not password1:
            raise serializers.ValidationError('password is required')
        if attrs['password1'] != password2:
            raise serializers.ValidationError('passwords not match.')
        return attrs


class UserUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=False, write_only=True)
    password1 = serializers.CharField(required=False, write_only=True)
    password2 = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        exclude = ['is_staff', 'is_superuser', 'is_active', 'password', 'groups', 'user_permissions']
        read_only_fields = ['date_joined', 'last_login']


    def update(self, instance, validated_data):
        password1 = validated_data.get('password1', None)
        for name, attr in validated_data.items():
            if name == 'password1':
                instance.set_password(password1)
            elif hasattr(instance, name):
                setattr(instance, name, attr)
        instance.save()
        return instance

    def validate(self, attrs):
        old_password = attrs.get('old_password', None)
        password1 = attrs.get('password1', None)
        password2 = attrs.get('password2', None)
        user = self.context['request'].user

        if password1 or password2 or old_password:
            passwords = ['password1', 'password2', 'old_password']
            for field_name in passwords:
                if not attrs.get(field_name):
                    raise serializers.ValidationError({field_name: 'required'})

            if password1 != password2:
                raise serializers.ValidationError('passwords not match.')
            elif password1 == old_password:
                raise serializers.ValidationError('you not change password.')
            if not user.check_password(old_password):
                raise serializers.ValidationError({'old_password': 'old password is warring.'})
        return attrs
