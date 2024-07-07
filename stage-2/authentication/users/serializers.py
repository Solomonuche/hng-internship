"""Users amanagement serializer module
"""
from rest_framework import serializers
from users.models import User
from organisation.models import Organisation
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    """
    Register serializer
    """

    class Meta:
        model = User
        fields = ['firstName', 'lastName', 'email',
                  'password', 'phone']

    def validate_email(self, email):
        """
        Ensure email is unique
        """

        if User.objects.filter(email=email).exists():
            return serializers.ValidationError('email must be unique')
        return email


    def create(self, validated_data):
        """perform create
        """

        firstName = validated_data['firstName']
        lastName = validated_data['lastName']
        email = validated_data['email']
        password = validated_data['password']
        phone = validated_data['phone']

        user = User.objects.create(
            firstName=firstName,
            lastName=lastName,
            email=email,
            phone=phone
        )

        user.set_password(validated_data['password'])
        user.save()
        user_org = Organisation.objects.create(name=f"{firstName}'s Organisation")
        user_org.users.add(user)
        return user


class LoginSerializer(serializers.Serializer):
    """
    Login serializer
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        Validate user credentials
        """
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)
            if not user:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Must include "email" and "password"')
        data['user'] = user
        return data