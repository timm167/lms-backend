from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed

class DebugTokenAuthentication(TokenAuthentication):

    def authenticate(self, request):
        print("DebugTokenAuthentication: authenticate called")
        print("DebugTokenAuthentication: request:", request)
        print("DebugTokenAuthentication: request.headers:", request.headers)
        token = request.headers.get('Authorization')
        print("DebugTokenAuthentication: token:", token)
        auth = super().authenticate(request)

        if auth is None:
            print("DebugTokenAuthentication: No authentication credentials provided")
        else:
            print("DebugTokenAuthentication: User authenticated")
        return auth

    def authenticate_credentials(self, key):
        print("DebugTokenAuthentication: authenticate_credentials called with key:", key)
        try:
            return super().authenticate_credentials(key)
        except AuthenticationFailed as e:
            print("DebugTokenAuthentication: Authentication failed:", str(e))
            raise