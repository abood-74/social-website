
import requests
from django.conf import settings                        
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'


def get_google_access_token(code):
    """
    Get the access token from Google API
    """
    
    data = {
        'code': code,
        'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
        'redirect_uri': settings.GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    
    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)
    
    if not response.ok:
        raise ValidationError('Could not get access token from Google.')
    
    access_token = response.json()['access_token']
    return access_token

def get_google_user_info(access_token):
    """
    Get the user info from Google API
    """
    
    params = {
        'access_token': access_token
    }
    
    # used params instead of data because it is a GET request
    response = requests.get(GOOGLE_USER_INFO_URL, params=params)
    
    if not response.ok:
        raise ValidationError('Could not get user info from Google.')
    
    return response.json()


def create_jwt_token_for_google_authnticated_user(validated_data):
    """
    Create a JWT token for the user who authenticated with Google
    """
    #used get insted of bracket notation because it will raise an error if the key is not found
    code = validated_data.get('code')
    error = validated_data.get('error')
    
    if error or not code:
        raise ValidationError('Google authentication failed.')
    
    access_token = get_google_access_token(code)
    user_info = get_google_user_info(access_token)
    
    email = user_info.get('email')
    first_name = user_info.get('given_name')
    
    user = CustomUser.objects.get_or_create(email=email, username=email)[0]
    refresh = RefreshToken.for_user(user)
    
    return refresh, refresh.access_token
    
    

    
    
    
    
    
    
    
    