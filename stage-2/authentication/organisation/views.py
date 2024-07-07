from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import User
from rest_framework.permissions import IsAuthenticated
from organisation.models import Organisation
from .serializers import CreateSerializer, OrgListSerializer, AddUserSerializer

# Create your views here.
class UserDetailView(APIView):
    """
    Return user's data or user record in the organisation ther belong
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, userId):
        """
        retrieve user details
        """

        try:
            # Check if the requested userId is the same as the authenticated user's ID
            if request.user.userId == userId:
                user = User.objects.get(userId=userId)
            else:
                # Query the organisation for the user
                user = None
                organisations = Organisation.objects.filter(users=request.user)
                for org in organisations:
                    user = org.users.filter(userId=userId).first()
                    if user:
                        break
            
            if not user:
                return Response(
                    {
                        "status": "error",
                        "message": "User not found or not in the same organization",
                        "statusCode": 404
                    },
                    status=status.HTTP_404_NOT_FOUND
                )

            payload = {
                "status": "success",
                "message": "User details",
                "data": {
                    "userId": user.userId,
                    "firstName": user.firstName,
                    "lastName": user.lastName,
                    "email": user.email,
                    "phone": user.phone,
                }
            }
            return Response(payload, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(
                    {
                        "status": "error",
                        "message": "User not found or not in the same organization",
                        "statusCode": 404
                    },
                    status=status.HTTP_404_NOT_FOUND
                )


class OrgsListCreateView(APIView):
    """
    List and create organisation for a logged in user
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        list user organisation
        """

        orgs = Organisation.objects.filter(users=request.user)

        serializer = OrgListSerializer(orgs, many=True)
        payload = {
                "status": "success",
                "message": "User organisation",
                "data": {
                    "organisations": serializer.data
                }
            }
        return Response(payload, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handle post endpoint
        """

        data = {
            'name': request.data.get('name'),
            'description': request.data.get('description'),
            }

        serializer = CreateSerializer(data=data)
        
        if serializer.is_valid():
            user = serializer.save()
            payload = {
                "status": "success",
                "message": "Organisation created successfully",
                "data": serializer.data
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


class OrgsDetailAddView(APIView):
    """
    List single organisation for a logged in user
    Add a user to a specified organisation
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, orgId):
        """
        list a single organisation
        """

        try:
            org = Organisation.objects.get(orgId=orgId)
        except Organisation.DoesNotExist:
            return Response(
                {"status": "error", "message": "Organisation not found"}, 
                status=status.HTTP_404_NOT_FOUND
                )

        serializer = OrgListSerializer(org)
        payload = {
                "status": "success",
                "message": "Organisation",
                "data": serializer.data
            }
        return Response(payload, status=status.HTTP_200_OK)

    def post(self, request, orgId):
        """
        add user
        """
        data = {'userId': request.data.get('userId')}
        serializer = AddUserSerializer(data=data)
        if serializer.is_valid():
            userId = serializer.validated_data['userId']
            
            try:
                user = User.objects.get(pk=userId)
            except User.DoesNotExist:
                return Response(
                    {"status": "error", "message": "User not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                    )
            
            try:
                org = Organisation.objects.get(orgId=orgId)
            except Organisation.DoesNotExist:
                return Response(
                    {"status": "error", "message": "Organisation not found"}, 
                    status=status.HTTP_404_NOT_FOUND
                    )
            
            org.users.add(user)
            
            payload = {
                "status": "success",
                "message": "User added to organisation successfully",
            }
            return Response(payload, status=status.HTTP_200_OK)
        
        return Response(
            {"status": "error", "errors": serializer.errors}, 
            status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
