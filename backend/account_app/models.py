import uuid
import pytz
from django.db import models
from django.db import connection, connections
from datetime import datetime
from django.utils import timezone

# django libraries for deleting file attachments
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

# django libraries for displaying validation error messages
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# external models
from django.contrib.auth.models import User

class Module(models.Model):
	name = models.CharField(max_length=250, unique=True)
	slug = models.SlugField(max_length=300, unique=True)
	shorthand = models.CharField(max_length=50, unique=True)
	fontawesome_icon = models.CharField(max_length=75)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(blank=True, null=True)
	created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="module_created_by", blank=True, null=True)
	updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="module_updated_by", blank=True, null=True)

	class Meta:
		db_table = 'account_app\".\"module'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return "/"

class Role(models.Model):
	name = models.CharField(max_length=250, unique=True)
	slug = models.SlugField(max_length=300, unique=True)
	shorthand = models.CharField(max_length=50, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(blank=True, null=True)
	created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="role_created_by", blank=True, null=True)
	updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="role_updated_by", blank=True, null=True)

	class Meta:
		db_table = 'account_app\".\"role'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return "/"

class Object(models.Model):
	name = models.CharField(max_length=250, unique=True)
	slug = models.SlugField(max_length=300, unique=True)
	shorthand = models.CharField(max_length=50, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(blank=True, null=True)
	created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="object_created_by", blank=True, null=True)
	updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="object_updated_by", blank=True, null=True)

	class Meta:
		db_table = 'account_app\".\"object'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return "/"

class Operation(models.Model):
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(max_length=100, unique=True)
	shorthand = models.CharField(max_length=10, unique=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(blank=True, null=True)
	created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="operation_created_by", blank=True, null=True)
	updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="operation_updated_by", blank=True, null=True)

	class Meta:
		db_table = 'account_app\".\"operation'

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return "/"

class Permission(models.Model):
	object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name="permission_object")
	operation = models.ForeignKey(Operation, on_delete=models.CASCADE, related_name="permission_operation")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(blank=True, null=True)
	created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="permission_created_by", blank=True, null=True)
	updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="permission_updated_by", blank=True, null=True)

	class Meta:
		db_table = 'account_app\".\"permission'

	def __str__(self):
		return self.object.name + " | " + self.operation.name

	def get_absolute_url(self):
		return "/"

class RoleAssignment(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="role_assignment_user")
	role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role_assignment_role")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(blank=True, null=True)
	created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="role_assignment_created_by", blank=True, null=True)
	updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="role_assignment_updated_by", blank=True, null=True)

	class Meta:
		db_table = 'account_app\".\"roleassignment'

	def __str__(self):
		return self.user.username + " | " + self.role.name

	def get_absolute_url(self):
		return "/"

class PermissionAssignment(models.Model):
	role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="permission_assignment_role")
	permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name="permission_assignment_permission")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(blank=True, null=True)
	created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="permission_assignment_created_by", blank=True, null=True)
	updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="permission_assignment_updated_by", blank=True, null=True)

	class Meta:
		db_table = 'account_app\".\"permissionassignment'

	def __str__(self):
		return self.role.name + " | " + self.permission.object.name + " | " + self.permission.operation.name

	def get_absolute_url(self):
		return "/"

class RoleModule(models.Model):
	role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role_module_role")
	module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="role_module_module")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(blank=True, null=True)
	created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="role_module_created_by", blank=True, null=True)
	updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="role_module_updated_by", blank=True, null=True)

	class Meta:
		db_table = 'account_app\".\"rolemodule'

	def __str__(self):
		return self.role.name + " | " + self.module.name

	def get_absolute_url(self):
		return "/"

class ModuleObject(models.Model):
	module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name="module_object_module")
	object = models.ForeignKey(Object, on_delete=models.CASCADE, related_name="module_object_object")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(blank=True, null=True)
	created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="module_object_created_by", blank=True, null=True)
	updated_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="module_object_updated_by", blank=True, null=True)

	class Meta:
		db_table = 'account_app\".\"moduleobject'

	def __str__(self):
		return self.module.name + " | " + self.object.name

	def get_absolute_url(self):
		return "/"


class PasswordReset(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="account_password_reset_user")
	confirmation_code = models.CharField(max_length=16)
	confirmed = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		db_table = 'account_app\".\"passwordreset'

	def __str__(self):
		return self.user.username + " | " + self.confirmation_code

	def get_absolute_url(self):
		return "/"

	@classmethod
	def create(cls, user, confirmation_code):
		try:
			pr = cls(user=user, confirmation_code=confirmation_code)
			pr.save()
			return pr
		except Exception as e:
			print(e)
			return e