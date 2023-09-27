from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name',
                  'restaurants', 'created_at', 'updated_at')
        read_only_fields = ('restaurants', 'created_at', 'updated_at')

    def validate(self, attrs):
        username = attrs.get('username', None)
        password = attrs.get('password', None)

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError("User with this username already exists!")
        if not password or (len(password) < 5):
            raise serializers.ValidationError("Password not provided or its lenght lower than 5!")

        return super().validate(attrs)

    def create(self, validated_data):
        username = validated_data.get('username', None)
        password = validated_data.get('password', None)

        first_name = validated_data.get('first_name', '')
        last_name = validated_data.get('last_name', '')

        user = User.objects.create_user(username, password, first_name=first_name, last_name=last_name)

        return user
