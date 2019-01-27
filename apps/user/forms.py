"""Account management forms"""
import django.contrib.auth.forms as auth_forms


class Login(auth_forms.AuthenticationForm):
    error_messages = {
        'invalid_login': (
            'Please enter a correct email and password.'
        ),
        'inactive': 'This account is inactive.'
    }
