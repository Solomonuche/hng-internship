from django.urls import path
from .views import UserDetailView, OrgsListCreateView, OrgsDetailAddView

urlpatterns = [
    path('users/<userId>/', UserDetailView.as_view(), name='user'),
    path('organisations/', OrgsListCreateView.as_view(), name='user-orgs'),
    path('organisations/<orgId>/', OrgsDetailAddView.as_view(), name='org-detail'),
]