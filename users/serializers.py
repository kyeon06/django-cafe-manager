import re
from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

    def validate_phone_number(self, value):
        phone_number_regex = r'^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})$'
        if not re.match(phone_number_regex, value):
            raise serializers.ValidationError("유효하지 않은 휴대폰 번호입니다. ex)010-1111-1111")
        return value
    
    def validate_password(self, value):
        password_regex = r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$'
        if not re.match(password_regex, value):
            raise serializers.ValidationError("비밀번호는 최소 8자 이상이며, 대문자, 소문자, 숫자, 특수문자를 모두 포함해야 합니다.")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(
            phone_number = validated_data['phone_number'],
            password = validated_data['password']
        )
        return user

    