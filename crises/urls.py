from django.urls import path
from .views import (
    CrisisListView,
    CrisisDetailView,
    ResourceListView,
    NGOResourceListView,
    NGOResourceDetailView,
)

urlpatterns = [
    path('', CrisisListView.as_view()),
    path('<int:crisis_pk>/', CrisisDetailView.as_view()),
    path('resources/', ResourceListView.as_view()),
    path('ngoresources/', NGOResourceListView.as_view()),
    path('ngo_resources/<int:resource_pk>/', NGOResourceDetailView.as_view()),
]