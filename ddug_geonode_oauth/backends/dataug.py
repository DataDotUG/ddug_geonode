"""
Github OAuth2 backend, docs at:
    http://psa.matiasaguirre.net/docs/backends/github.html
"""
from requests import HTTPError

from social.exceptions import AuthFailed
from social.backends.oauth import BaseOAuth2


class DataugOAuth2(BaseOAuth2):
    """Github OAuth authentication backend"""
    name = 'dataug'
    AUTHORIZATION_URL = 'http://localhost:5000/oauth2/authorize'
    ACCESS_TOKEN_URL = 'http://localhost:5000/oauth2/access_token'
    ACCESS_TOKEN_METHOD = 'POST'
    SCOPE_SEPARATOR = ','
    DEFAULT_SCOPE = [
        'http://localhost:5000/oauth2/identity',
    ]
    EXTRA_DATA = [
        ('id', 'id'),
        ('expires', 'expires')
    ]

    def get_user_details(self, response):
        """Return user details from Github account"""
        fullname, first_name, last_name = self.get_user_names(
            response.get('name')
        )
        return {'username': response.get('login'),
                'email': response.get('email') or '',
                'fullname': fullname,
                'first_name': first_name,
                'last_name': last_name}

    def user_data(self, access_token, *args, **kwargs):
        """Loads user data from service"""
        data = self._user_data(access_token)
        if not data.get('email'):
            try:
                email = self._user_data(access_token, '/emails')[0]
            except (HTTPError, IndexError, ValueError, TypeError):
                email = ''

            if isinstance(email, dict):
                email = email.get('email', '')
            data['email'] = email
        return data

    def _user_data(self, access_token, path=None):
        #url = 'https://api.github.com/user{0}'.format(path or '')
	url = 'http://localhost:5000/oauth2/identity'
        return self.get_json(url, params={'access_token': access_token})

