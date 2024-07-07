from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework.response import Response
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from organisation.models import Organisation


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.
class RegisterView(APIView):
    """
    class view for user registartion
    """

    def post(self, request):
        """
        Handle post endpoint
        """

        data = {
            'firstName': request.data.get('firstName'),
            'lastName': request.data.get('lastName'),
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'phone': request.data.get('phone'),
        }

        serializer = RegisterSerializer(data=data)
        
        if serializer.is_valid():
            user = serializer.save()
            token = get_tokens_for_user(user)
            payload = {
                "status": "success",
                "message": "Registration successful",
                "data": {
                "accessToken": token['access'],
                "user": {
                    "userId": user.userId,
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "phone": user.phone,
                    }
                }
            }
            return Response(payload, status=status.HTTP_201_CREATED)
        if serializer.errors:
            error = []
            for key, value in serializer.errors.items():
                error.append({'field': key, 'message': value[0]})
            return Response({"errors": error}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response(
            {
                "status": "Bad request",
                "message": "Registration unsuccessful",
                "statusCode": 400
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        

class LoginView(APIView):
    """
    Jwt login view
    """

    def post(self, request):
        """
        Login 
        """

        serializer = LoginSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = get_tokens_for_user(user)
            payload = {
                "status": "success",
                "message": "Login successful",
                "data": {
                "accessToken": token['access'],
                "user": {
                    "userId": user.userId,
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "phone": user.phone,
                    }
                }
            }
            return Response(payload, status=status.HTTP_200_OK)
        
        if serializer.errors:
            for key, value in serializer.errors.items():
                if value[0] == 'Invalid credentials':
                    return Response(
                        {
                            "status": "Bad request",
                            "message": "Authentication failed",
                            "statusCode": 401
                        },
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            errors = [{'field': key, 'message': value[0]} for key, value in serializer.errors.items()]
            return Response({"errors": errors}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

