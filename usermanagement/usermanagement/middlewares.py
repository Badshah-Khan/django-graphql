from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_authentication = JWTAuthentication()

    def __call__(self, request):
        # Authenticate the user using JWT
        try:
            user = self.jwt_authentication.authenticate(request)
            if user:
                request.user = user
                request.is_auth = True
            else:
                request.is_auth = False
        except InvalidToken:
            pass  # Handle invalid token error as needed

        # Call the next middleware in the stack
        return self.get_response(request)
