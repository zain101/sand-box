from oauth2client import client
import json
import os
import httplib2
from apiclient import discovery 


def get_service(request):
	BASE = os.path.dirname(os.path.abspath(__file__))
	client_secret_path = os.path.join(BASE, 'client_secret.json')

	print client_secret_path

	client_secret = None
	with open(client_secret_path) as client_secret_json:
		client_secret = json.load(client_secret_json)

	user = request.user
	token = user.user_token

	credentials = client.OAuth2Credentials(
		access_token= token.access_token,
		refresh_token=token.refresh_token,
		token_expiry=token.token_expiry,
		token_uri=client_secret['installed']['token_uri'],
		client_id= client_secret['installed']['client_id'],
		client_secret=client_secret['installed']['client_secret'],
		user_agent=None
	)

	http_auth = credentials.authorize(httplib2.Http())

	service = discovery.build('calendar', 'v3', http_auth)

	return service