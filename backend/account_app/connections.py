from django.core.mail import get_connection

class EmailConnection():
	# Gmail connection
	def connection(host, port, username, password):
		try:
			connection = get_connection(
				host=host,
				port=port,
				username=username,
				password=password,
				use_tls=True
			)
			return connection
		except Exception as e:
			print(e)