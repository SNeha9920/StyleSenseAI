from rest_framework import serializers
from .models import *

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        db_table: 'tokens'
        model = Tokens
        abstract = True
        fields = '__all__'

class userLoginSerializer(serializers.ModelSerializer):
    class Meta:
        db_table: 'user_login'
        model = user_login
        abstract = True
        fields = '__all__'