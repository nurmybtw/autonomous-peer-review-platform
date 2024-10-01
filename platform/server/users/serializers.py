from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Publication

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'password', 'username', 'first_name', 'last_name', 'email', 'is_reviewer']
        extra_kwargs = {'password': {'write_only': True}} 
    
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

class PublicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publication
        fields = ['title', 'abstract', 'publication_date', 'categories']