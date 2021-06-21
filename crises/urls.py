from django.urls import path
from .views import (
    CrisisListView,
    CrisisDetailView,
    DisasterTypesListView,
    ResourceListView,
    NGOResourceListView,
    NGOResourceDetailView,
    UserCrisisListView,
    RequestDetailView,
)

urlpatterns = [
    path('', CrisisListView.as_view()),
    path('types/', DisasterTypesListView.as_view()),
    path('<int:user_pk>/', UserCrisisListView.as_view()),
    path('crisis/<int:crisis_pk>/', CrisisDetailView.as_view()),
    path('resources/', ResourceListView.as_view()),
    path('ngo_resources/<int:resource_pk>/', NGOResourceDetailView.as_view()),
    path('ngo_resources/', NGOResourceListView.as_view()),
    path('request/<int:crisis_request_pk>/', RequestDetailView.as_view()),
]