"""Users amanagement serializer module
"""
from rest_framework import serializers
from organisation.models import Organisation


class OrgListSerializer(serializers.ModelSerializer):
    """
    Organisation serializer
    """

    class Meta:
        model = Organisation
        fields = ['orgId', 'name', 'description']


class CreateSerializer(serializers.ModelSerializer):
    """
    create serializer
    """

    class Meta:
        model = Organisation
        fields = ['orgId', 'name', 'description']
        read_only_fields = ['orgId']

    def create(self, validated_data):
        """perform create
        """

        name = validated_data['name']
        description = validated_data['description']
       
        org = Organisation.objects.create(
            name=name,
            description=description,
        )

        return org


class AddUserSerializer(serializers.Serializer):
    """
    serializer
    """

    userId = serializers.CharField(max_length=300)

    def validate_userId(self, value):
        """
        Validate credentials
        """

        if not value:
            raise serializers.ValidationError('Must include "userId"')
        
        return value