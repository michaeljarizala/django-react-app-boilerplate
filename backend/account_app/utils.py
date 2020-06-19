from django.conf import settings
from datetime import date, datetime
from django.utils import timezone
from django.contrib.auth.models import User

class EmailOrUsernameModelBackend(object):
	def authenticate(self, username=None, password=None):
		if '@' in username:
			kwargs = {'email': username}
		else:
			kwargs = {'username': username}

		try:
			user = User.objects.get(**kwargs)
			if user.check_password(password):
				return user
		except User.DoesNotExist:
			return None

	def get_user(self, user_id):
		try:
			return User.objects.get(pk=user_id)
		except User.DoesNotExist:
			return None
			
class DateTimeHandling():
	def get_datetime_diff__tz_aware(time, current_time):
		try:
			now = timezone.make_aware(current_time, timezone.get_default_timezone())
			timediff = now - time
			return timediff
		except Exception as e:
			print(e)
			return e