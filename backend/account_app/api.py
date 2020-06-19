import traceback
from django.conf import settings
from datetime import date, datetime, timedelta
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.models import Permission, Group
from django.contrib.auth.signals import user_logged_in, user_logged_out
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.serializers import DateTimeField
from knox.models import AuthToken
from knox.auth import TokenAuthentication
from knox.settings import knox_settings

# Tokenization libraries for user account activation link
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

# Hashed string generator
from django.utils.http import base36_to_int, int_to_base36

from .serializers import (
	UserSerializer,
	RegisterSerializer,
	LoginSerializer,
	PermissionSerializer,
	UserRoleSerializer,
	ActivationSerializer,
	ActivationResendSerializer
)
from account_app.models import (
	Module,
	Role,
	Object,
	Operation,
	RoleAssignment,
	PermissionAssignment,
	RoleModule,
	ModuleObject,
	PasswordReset
)
from .connections import EmailConnection
from .utils import DateTimeHandling


"""
TOKEN GENERATOR CLASS
"""
class TokenGenerator(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		return (
			six.text_type(user.pk) + six.text_type(timestamp) +
			six.text_type(user.is_active)
		)
account_activation_token = TokenGenerator()

"""
CONFIRMATION CODE GENERATOR CLASS
"""
class ConfirmationCodeGenerator(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		return (six.text_type(user.pk) + six.text_type(timestamp))
account_confirmation_code = ConfirmationCodeGenerator()
# Method for activating user account
# using the account activation token sent to user's email
def activate(request, uidb64, token):
	try:
		uid = force_text(urlsafe_base64_decode(uidb64))
		user = User.objects.get(pk=uid)
	except(TypeError, ValueError, OverflowError, User.DoesNotExist):
		user = None
	if user:
		if not user.is_active:
			if account_activation_token.check_token(user, token):
				user.is_active = True
				user.save()
				return Response({
					"success": True,
					"message": "Your account has been successfully activated. You may now login using your registered credentials."
				}, status=status.HTTP_200_OK)
			else:
				return Response({
					"success": False,
					"message": "There was a problem activating your account. It's either the activation link has expired or is invalid.",
					"user": {
						"email": user.email,
						"can_reactivate": True
					}
				}, status=status.HTTP_400_BAD_REQUEST)
		else:
			return Response({
				"success": False,
				"message": "Oops! You are already an active user. You may disregard this link from now on."
			}, status=status.HTTP_400_BAD_REQUEST)
	else:
		return Response({
			"success": False,
			"message": "Uh-oh! Your account could not be found."
		}, status=status.HTTP_400_BAD_REQUEST)


"""
EMAIL TRANSACTION
-this class is used for sending email to specified recipient
"""
class EmailTransaction():
	def send(subject, message, sender, recipient, connection, content_type):
		email = EmailMessage(subject, message, sender, to=[recipient], connection=connection)
		email.content_subtype = content_type
		email.send()


"""
REGISTRATION API
"""
class RegisterAPI(generics.GenericAPIView):
	serializer_class = RegisterSerializer
	permission_classes = ()
	authentication_classes = ()

	def post(self, request, *args, **kwargs):
		userInactivelyExists = User.objects.filter(
			Q(email=request.data.get('email'),
			is_active=False)
			|
			Q(email=request.data.get('email'),
			username=request.data.get('username'),
			is_active=False)
		)
		if userInactivelyExists:
			return Response({
				"success": False,
				"for_activation": True,
				"message": "It seems that a JobNet account with this email address is already registered by someone, and the account is just awaiting activation. If you own this account, click on the link below to resend an activation link to your email."
			}, status=status.HTTP_400_BAD_REQUEST)
		elif User.objects.filter(email=request.data.get('email')).exists():
			return Response({
				"success": False,
				"message": "An account with this email address already exists."
			}, status=status.HTTP_400_BAD_REQUEST)
		elif User.objects.filter(username=request.data.get('username')).exists():
			return Response({
				"success": False,
				"message": "An account with this username address already exists."
			}, status=status.HTTP_400_BAD_REQUEST)
		else:
			user = User.objects.none()
			try:
				user = User.objects._create_user(
					request.data.get('username'),
					request.data.get('email'),
					request.data.get('password'),
				)
				user.is_active = False
				user.save()
			except Exception as e:
				return Response({
					"success": False,
					"message": "Internal System Error: " + str(e)
				}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
			if user:
				if not user.is_active:
					try:
						EmailTransaction.send(
							subject='Provincial Government of Agusan del Norte | JobNet System account activation.',
							message=render_to_string('jobnet_app/misc/account_activation_email.html', {
							  'user': user,
							  'domain': request.get_host,
							  'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
							  'token':account_activation_token.make_token(user),
							}, request=request),
							sender=settings.GENERIC_EMAIL_HOST_USER_MISD,
							recipient=request.data.get('email'),
							connection=EmailConnection.connection(
								host=settings.GENERIC_EMAIL_HOST_MISD,
								port=settings.GENERIC_EMAIL_PORT_MISD,
								username=settings.GENERIC_EMAIL_HOST_USER_MISD,
								password=settings.GENERIC_EMAIL_HOST_PASSWORD_MISD
							),
							content_type='html'
						)
						return Response({
							"success": True,
							"message": "Yeeey, great! Your JobNet account is partially registered. To complete the registration and be able to login to your account, kindly check the email we sent you for account activation."
						}, status=status.HTTP_201_CREATED)
					except Exception as e:
						user.delete()
						return Response({
							"success": False,
							"message":"Internal System Error: " + str(e)
						}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
				else:
					return Response({
						"success": False,
						"message": "Oops! You are already an active user. You may login"
					}, status=status.HTTP_204_NO_CONTENT)

		return Response({
			"status":False,
			"message": "Unknown error has been encountered."
		}, status=status.HTTP_400_BAD_REQUEST)


"""
ACTIVATION LINK RESEND API
"""
class ActivationResendAPI(generics.GenericAPIView):
	serializer_class = ActivationResendSerializer
	permission_classes = ()
	authentication_classes = ()

	def post(self, request, *args, **kwargs):
		user = User.objects.get(
			email=request.data.get('email'),
			is_active=False
		)
		if user:
			try:
				EmailTransaction.send(
					'Provincial Government of Agusan del Norte | JobNet System account activation.',
					render_to_string('jobnet_app/misc/account_activation_resend_email.html', {
					  'user': user,
					  'domain': request.get_host,
					  'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
					  'token':account_activation_token.make_token(user),
					}, request=request),
					sender=settings.GENERIC_EMAIL_HOST_USER_MISD,
					recipient=request.data.get('email'),
					connection=EmailConnection.connection(
						host=settings.GENERIC_EMAIL_HOST_MISD,
						port=settings.GENERIC_EMAIL_PORT_MISD,
						username=settings.GENERIC_EMAIL_HOST_USER_MISD,
						password=settings.GENERIC_EMAIL_HOST_PASSWORD_MISD
					),
					content_type='html'
				)
				return Response({
					"success": True,
					"message": "Awesome! You are one step closer to enjoying the JobNet system. Kindly check the activation link that we have re-sent to your email and read on the instructions for activating your JobNet account."
				}, status=status.HTTP_200_OK)
			except Exception as e:
				return Response({
					"success": False,
					"message": "Internal System Error: " + str(e)
				}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
		else:
			return Response({
				"success": False,
				"message": "Sorry. An account with the given credentials could not be found."
			}, status=status.HTTP_400_BAD_REQUEST)


"""
ACCOUNT ACTIVATION API
"""
class ActivatationAPI(generics.GenericAPIView):
	serializer_class = ActivationSerializer
	permission_classes = ()
	authentication_classes = ()

	def get(self, request, uidb64, token):
		return activate(request, uidb64, token)


"""
PASSWORD RESET API
"""
class PasswordResetAPI(generics.GenericAPIView):
	serializer_class = ActivationResendSerializer
	permission_classes = ()
	authentication_classes = ()
	# Set the confirmation code expiration to 3 minutes.
	confirmation_code_expiration = timedelta(minutes=3)

	# Clear password resets that have not been confirmed...
	# ...by the user. Ideally, perform this when user...
	# ...attempts to confirm a code. More importantly...
	# ...confirm this when code confirmation passes or fails.
	def clean_unconfirmed_password_reset(self, user):
		try:
			#pr = PasswordReset.objects.filter(user__username=user, confirmed=False)
			pr = PasswordReset.objects.filter( Q(user__username=user, confirmed=False) | Q(user__email=user, confirmed=False))
			if pr:
				for x in pr:
					x.delete()
		except Exception as e:
			traceback.print_exc()
			return Response({
				"success": False,
				"message": "Internal System Error: " + str(e)	
			}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	# Handles logging of each password reset attempt...
	# ...by the user, capturing the confirmation code...
	# ...and sending the code to user's email. This process...
	# ...is necessary for the ff. reasons:
	# 1.) Confirm user's action and its identity to...
	# ...make sure that it is a valid action from the real user.
	# 2.) Log each attempt with the confirmation code so...
	# ...we can enforce expiration to the attempt later on...
	# ...This is great to force the user to confirm...
	# ...the attempt right away and avoid having the...
	# ...password reset option be abused by hackers...
	# ...and the user itself.
	def post(self, request, *args, **kwargs):
		# Identify the user by its email or username.
		# Only get the user if it has an active account.
		try:
			user = User.objects.get(
				Q(email=request.data.get('account'), is_active=True)|
				Q(username=request.data.get('account'), is_active=True)
			)
		except Exception  as e:
			user = User.objects.none()
			print(e)


		if user: # Check if user exists
			if user.is_active: # Check if user is active
				# Begin the process of sending email confirmation...
				# ...and logging attempts.
				try:
					# Generate the confirmation code in URL-safe base64.
					# The code is a combination of the ff:
					# 1.) int-parsed timestamp of the datetime when the action was taken
					# 2.) int-parsed microsecond of the datetime when the action was taken
					# 3.) User's unique ID
					# 4.) timestamp of the datetime when the action was taken, parsed into base36
					confirmation_code_encoded = urlsafe_base64_encode(force_bytes(int(datetime.now().timestamp()) + int(datetime.now().microsecond) + user.pk + base36_to_int(int_to_base36(int(datetime.now().timestamp()))))).decode()

					# Log the attempt together with user info...
					# ...and the confirmation code.
					pr = PasswordReset.create(
						user=user,
						confirmation_code=confirmation_code_encoded,
					)

					# Email the confirmation code to user's registered email address...
					# ...using the MISD email setting. MISD's smtp setting will be...
					# ...used for sending email for notifications regarding account.
					EmailTransaction.send(
						subject=settings.GENERIC_EMAIL_SUBJECT_PREFIX_MISD + ' | JobNet System account password reset.',
						message=render_to_string('jobnet_app/misc/account_password_reset_email.html', {
						  'user': user,
						  'confirmation_code': confirmation_code_encoded
						}, request=request),
						sender=settings.GENERIC_EMAIL_HOST_USER_MISD,
						recipient=user.email,
						connection=EmailConnection.connection(
							host=settings.GENERIC_EMAIL_HOST_MISD,
							port=settings.GENERIC_EMAIL_PORT_MISD,
							username=settings.GENERIC_EMAIL_HOST_USER_MISD,
							password=settings.GENERIC_EMAIL_HOST_PASSWORD_MISD
						),
						content_type='html'
					)
					return Response({
						"success": True,
						"message": "Great! To continue, kindly check the confirmation code we sent to your JobNet-registered email address."
					}, status=status.HTTP_200_OK)
				except Exception as e:
					pr.delete()
					traceback.print_exc()
					return Response({
						"success": False,
						"message": "Internal System Error: " + str(e)
					}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
			else: # Inactive users cannot change their passwords.
				return Response({
					"success": False,
					"message": "Uh-oh! Your JobNet account has not been activated yet. Please activate your account first then you can proceed to resetting your password. Click on the link below to resend an account activation link to your registered email address."
				}, status=status.HTTP_400_BAD_REQUEST)
		else: # Error handler for unknown users.
			return Response({
				"success": False,
				"message": "Sorry. We could not find your account."
			}, status=status.HTTP_400_BAD_REQUEST)

	# Handles the verification of confirmation code.
	# The confirmation code is set to expire in 3 minutes.
	# The system must clean all unconfirmed attempts...
	# ...that have already expired.
	def patch(self, request, *args, **kwargs):
		# Beging verification of confirmation code.
		try:
			# Retrieve the attempt log based on user, confirmation code...
			# ...and unconfirmed attempt.
			pr = PasswordReset.objects.filter( Q(user__username=request.data.get('account'), confirmation_code=request.data.get('code')) | Q(user__email=request.data.get('account'), confirmation_code=request.data.get('code'))).first()

			# Verify if a log has been retrieved
			if pr:
				# Define the elapsed time since the action was taken...
				# ...against the time when the code was attempted to confirm.
				# This variable is vital on the verification of expired attempts.
				elapsed_time_since_pr_attempt = DateTimeHandling.get_datetime_diff__tz_aware(pr.created_at, datetime.now())
				
				# Verify that the attempt being confirmed...
				# ...has not expired yet by comparing...
				# ...the elapsed time against the expiration time...
				# ...that has been set above.
				if self.confirmation_code_expiration >= elapsed_time_since_pr_attempt:
					if not pr.confirmed:
						# Confirm the attempt
						pr.confirmed=True
						pr.save()

						#clean any expired, unconfirmed attemts.
						self.clean_unconfirmed_password_reset(user=request.data.get('account'))
						return Response({
							"success": True,
							"message": "Request for password reset has been confirmed. You may now set a new password for your JobNet account."
						}, status=status.HTTP_200_OK)
					else: # Execute when confirmation code is already confirmed.
						# We still want to clean the attempt logs...
						# ...for any expired, unconfirmed attempts.
						self.clean_unconfirmed_password_reset(user=request.data.get('account'))
						return Response({
							"success": False,
							"message": "The confirmation code you entered is either incorrect or no longer valid. Please check the code and try again, or generate a new one."
						}, status=status.HTTP_400_BAD_REQUEST)
				else: # Prohibit expired, unconfirmed attempts
					# We still want to clean the attempt logs...
					# ...for any expired, unconfirmed attempts.
					self.clean_unconfirmed_password_reset(user=request.data.get('account'))
					return Response({
						"success": False,
						"message": "The confirmation code you entered has already expired. You may resend a new confirmation code."
					}, status=status.HTTP_400_BAD_REQUEST)
			else: # Execute when the attempt is not found or the confirmation code is invalid.
				return Response({
					"success": False,
					"message": "The confirmation code you entered is either incorrect or no longer valid. Please check the code and try again, or refresh the page to restart the process."
				}, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			traceback.print_exc()
			return Response({
				"success": False,
				"message": "Internal System Error: " + str(e)
			},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

	# Handles the actual modification of user password.
	def put(self, request, *args, **kwargs):
		try:
			user = User.objects.get(
				Q(email=request.data.get('account'))
				|
				Q(username=request.data.get('account'))
				)
			if user:
				if user.is_active:
					user.set_password(request.data.get('password'))
					user.save()
					return Response({
						"success": True,
						"message": "Password reset has been successful."
					}, status=status.HTTP_200_OK)
				else:
					return Response({
						"success": False,
						"message": "Uh-oh! Your JobNet account has not been activated yet. Please activate your account first then you can proceed to resetting your password. Click on the link below to resend an account activation link to your registered email address." + str(e)
					},status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response({
					"success": False,
					"message": "Sorry. We could not find your account."
				}, status=status.HTTP_400_BAD_REQUEST)
		except Exception as e:
			traceback.print_exc()
			return Response({
				"success": False,
				"message": "Internal System Error: " + str(e)
			},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
LOGIN API
"""
class LoginAPI(generics.GenericAPIView):
	serializer_class = LoginSerializer
	authentication_classes = api_settings.DEFAULT_AUTHENTICATION_CLASSES
	permission_classes = ()

	def get_context(self):
		return {'request': self.request, 'format': self.format_kwarg, 'view': self}

	def get_token_ttl(self):
		return knox_settings.TOKEN_TTL

	def get_token_limit_per_user(self):
		return knox_settings.TOKEN_LIMIT_PER_USER

	def get_user_serializer_class(self):
		return knox_settings.USER_SERIALIZER

	def get_expiry_datetime_format(self):
		return knox_settings.EXPIRY_DATETIME_FORMAT

	def format_expiry_datetime(self, expiry):
		datetime_format = self.get_expiry_datetime_format()
		return DateTimeField(format=datetime_format).to_representation(expiry)

	def get_post_response_data(self, request, token, instance):
		UserSerializer = self.get_user_serializer_class()

		data = {
	      'expiry': self.format_expiry_datetime(instance.expiry),
	      'token': token,
    	}
		if UserSerializer is not None:
		  data["user"] = UserSerializer(
		  	user,
		  	context=self.get_context()
		  ).data
		return data

	def post(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data

		token = None
		current_token = None
		roles = RoleAssignment.objects.none()
		role_modules = RoleModule.objects.none()
		module_objects = ModuleObject.objects.none()
		user_modules = Module.objects.none()
		objects = Object.objects.none()
		permissions = PermissionAssignment.objects.none()
		response_status = status.HTTP_400_BAD_REQUEST

		now = timezone.now()
		token_limit_per_user = self.get_token_limit_per_user()
		if token_limit_per_user is not None:
			token = user.auth_token_set.filter(expiry__gt=now)
			if token.count() >= token_limit_per_user:
				return Response(
		  {"error": "Maximum amount of tokens allowed per user exceeded."},
		  status=status.HTTP_403_FORBIDDEN
		)
		current_token = user.auth_token_set.filter(created__date=now, expiry__gt=now)

		if user: 
			if user.is_active:
				token_ttl = self.get_token_ttl()
				if user.is_staff and request.data['app'] == 'employee':
					instance, token = AuthToken.objects.create(user, token_ttl)
					user_logged_in.send(sender=user.__class__, request=request, user=user)
					roles = RoleAssignment.objects.filter(user=user).values('role__id', 'role__name')
					for role in roles:
						# get user's modules based on roles
						role_modules |= RoleModule.objects.filter(role=role['role__id']).values(
							'role__id',
							'module__id',
							'module__name',
							'module__slug',
							'module__fontawesome_icon'
						).order_by('module__name')
						# get user's permissions based on roles
						permissions |= PermissionAssignment.objects.filter(role=role['role__id']).values(
							'permission__object__id',
							'permission__object__name',
							'permission__object__slug',
							'permission__operation__id',
							'permission__operation__name'
						)
					for role_module in role_modules:
						module_objects |= ModuleObject.objects.filter(module=role_module['module__id']).values(
							'module__id',
							'module__name',
							'object__id',
							'object__name',
							'object__slug'
						)

						# get current user's objects...
						# ...based on his roles and permissions
						user_objects_temp = []
						for perm in permissions:
							[
								user_objects_temp.append(
									{
										'module':obj['module__id'],
										'id':obj['object__id'],
										'name':obj['object__name'],
										'slug':obj['object__slug']
									}
								)
								for obj in module_objects if obj['object__id'] == perm['permission__object__id']
							]
						# this code block aims to filter user_objects...
						# ... so that duplicates are handled properly
						# originally, user_objects are repeated (n) times...
						# ... depending on the permission linked to that object...
						# ... in conjuction to the user's role
						seen = set()
						user_objects = []
						for yy in user_objects_temp:
							t=tuple(yy.items())
							if t not in seen:
								seen.add(t)
								user_objects.append(yy)

					# format modules to include respective objects and permissions
					# this logic is primarily designed so that sidebar links can be...
					# ...generated seamlessly thru frontend 
					formatted_modules = [
						{
							"id": x['module__id'],
							"name": x['module__name'],
							"slug": x['module__slug'],
							"icon": x['module__fontawesome_icon'],
							"objects": [
								{
									"id": y['id'],
									"name": y['name'],
									"slug": y['slug'],
									"operations": [z['permission__operation__name']
										for z in permissions if z['permission__object__id']==y['id']
									]
								}
								for y in user_objects if x['module__id']==y['module']
							]
						}
						for x in role_modules
					]

					response_status = status.HTTP_200_OK
					data = {
						"user": UserSerializer(user, context=self.get_serializer_context()).data,
						"token": token,
						"authenticated": True,
						"staff": True,
						"roles": roles,
						"modules": formatted_modules,
						"expiry": self.format_expiry_datetime(instance.expiry),
					}
				elif not user.is_staff and request.data['app'] == 'jobnet':
					instance, token = AuthToken.objects.create(user, token_ttl)
					user_logged_in.send(sender=user.__class__, request=request, user=user)
					response_status = status.HTTP_200_OK
					data = {
						"user": UserSerializer(user, context=self.get_serializer_context()).data,
						"token": token,
						"authenticated": True,
						"staff": False,
						"roles": [],
						"modules": [],
						"expiry": self.format_expiry_datetime(instance.expiry),
					}
				else:
					data = {
						"errors": [
							"Your user account could not be authenticated for this portal."
						]
					}
			else:
				response_status = status.HTTP_403_FORBIDDEN
				data = {
					"errors": [
						"Cannot log you in. Your account seems to have been deactivated."
					]
				}
		else:
			response_status = status.HTTP_404_FORBIDDEN
			data = {
				"errors": [
					"User could not be found."
				]
			}

		return Response(data, response_status)


"""
LOGOUT API
"""
class LogoutAPI(generics.GenericAPIView):
	authentication_classes = (TokenAuthentication,)
	permission_classes = (permissions.IsAuthenticated,)

	def post(self, request, *args, **kwargs):
		request._auth.delete()
		user_logged_out.send(sender=request.user.__class__,
							 request=request, user=request.user)
		return Response(
			{
				"detail": "You have been logged out successfully!",
				"authenticated": False
			},
			status=status.HTTP_200_OK
		)


"""
USER ROLE API
"""
class UserRoleAPI(generics.ListCreateAPIView):
	queryset = Group.objects.all()
	serializer_class = UserRoleSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (DjangoModelPermissions,)

	def get_queryset(self):
		user_roles = Group.objects.filter(user=self.request.user)
		return user_roles


"""
PERMISSION API
"""
class PermissionAPI(generics.ListCreateAPIView):
	queryset = Permission.objects.all()
	serializer_class = PermissionSerializer
	authentication_classes = (TokenAuthentication,)
	permission_classes = (DjangoModelPermissions,)

	def get_queryset(self):
		permissions = Permission.objects.filter(group__user=self.request.user)
		return permissions