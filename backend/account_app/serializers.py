from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission, ContentType
from django.contrib.auth import authenticate

# User Serializer
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'id',
			'username',
			'email',
		)

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = (
			'id',
			'username',
			'email',
			'password',
		)
		extra_kwargs = {
			'password': {'write_only': True}
		}

# Activation Serializer
class ActivationSerializer(serializers.Serializer):
	username = serializers.CharField()
	email = serializers.CharField()

class ActivationResendSerializer(serializers.Serializer):
	email = serializers.CharField()

# Login Serializer
class LoginSerializer(serializers.Serializer):
	username = serializers.CharField()
	password = serializers.CharField()

	def validate(self, data):
		user = authenticate(**data)
		if user and user.is_active:
			return user
		raise serializers.ValidationError("Incorrect credentials...")

# Content Type Serializer
class ContentTypeSerializer(serializers.ModelSerializer):
	class Meta:
		model = ContentType
		fields = (
			'app_label',
			'model',
		)

# User Role Serializer
class UserRoleSerializer(serializers.ModelSerializer):
	class Meta:
		model = Group
		fields = (
			'name',
		)

# Permission Serializer thru User Group/Role
class PermissionSerializer(serializers.ModelSerializer):
	content_type = ContentTypeSerializer(read_only=True)
	class Meta:
		model = Permission
		fields = (
			'name',
			'codename',
			'content_type',
		)