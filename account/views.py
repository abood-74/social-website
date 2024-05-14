from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.password_validation import validate_password
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import LimitOffsetPagination
#local imports
from .models import CustomUser, Contact
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer, EditUserSerializer, AuthSerializer, UserFollowSerializer,UserDashboardSerializer, ActionSerializer
from .services import create_jwt_token_for_google_authnticated_user
from actions.utils import create_action
from actions.models import Action
from .tasks import send_congratulatory_email


class RegisterView(APIView):
        
        def post(self, request):
            serializer = RegisterSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                create_action(user, 'has created an account')
                send_congratulatory_email.delay(UserSerializer(user).data)
                return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
            
            
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status= status.HTTP_200_OK)
            return Response({'message': 'Invalid credentials'}, status= status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        


    


class PasswordChangeView(APIView): 
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if request.user.is_authenticated:
            
            try:
                validate_password(request.data['password'])
                request.user.set_password(request.data['password'])
                request.user.save()
                return Response({'message': 'Password changed successfully'}, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({'message': e.messages}, status=status.HTTP_400_BAD_REQUEST)
            
        

class UserEditView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'username':request.user.username, 'email': request.user.email, 'first_name': request.user.first_name})
    
    
    def put(self, request):
        serializer = UserSerializer(instance=request.user,data=request.data)
        if serializer.is_valid():     
            serializer.save()
            return Response({'message': 'User updated successfully'}, status=status.HTTP_201_CREATED) 
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        serializer = EditUserSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully'}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    
    def get(self, request):
        qs = CustomUser.objects.all()
        paginator = self.pagination_class()
        users = paginator.paginate_queryset(qs, request)
        return Response(UserSerializer(users, many=True).data, status=status.HTTP_200_OK) 

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            id = request.user.id
            user = CustomUser.objects.get(id=id)
            return Response(UserDashboardSerializer(user).data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, id):
        try:
            user = CustomUser.objects.get(id=id)
            user.delete()
            return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        
class UserFollowView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = UserFollowSerializer(data=request.data)
        if serializer.is_valid():
            try:
                id = serializer.validated_data['id']
                action = serializer.validated_data['action']
                user = CustomUser.objects.get(id=id)
                if action == 'follow':
                    Contact.objects.get_or_create(user_from=request.user, user_to=user)
                    create_action(request.user, 'is following', user)
                else:
                    Contact.objects.filter(user_from=request.user, user_to=user).delete()
                return Response({'message': 'Action successful'}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   
class DashBoardView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination
    
    def get(self, request):
        actions = Action.objects.exclude(user=request.user)
        following_ids = request.user.following.values_list('id', flat=True)
        
        if following_ids:
            actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile')\
                                        .prefetch_related('target')
        paginator = self.pagination_class()
        paginated_actions = paginator.paginate_queryset(actions, request)
        return Response(ActionSerializer(paginated_actions, many=True).data, status=status.HTTP_200_OK)
        
        

class GoogleLoginView(APIView):
    
    def get(self, request, *args, **kwargs):
        
        Auth_data = AuthSerializer(data=request.GET)
        Auth_data.is_valid(raise_exception=True)
        
        validated_data = Auth_data.validated_data
        
        refresh, access_token = create_jwt_token_for_google_authnticated_user(validated_data)
        
        return Response({'refresh': str(refresh), 'access': str(access_token)}, status=status.HTTP_200_OK)
            
        
