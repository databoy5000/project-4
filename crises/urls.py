from django.urls import path
from .views import (
    CrisisListView,
    CrisisDetailView,
    ResourceListView,
    NGOResourceDetailView,
)

urlpatterns = [
    path('', CrisisListView.as_view()),
    path('<int:crisis_pk>/', CrisisDetailView.as_view()),
    path('resources/', ResourceListView.as_view()),
    path('NGOresources/<int:crisis_pk>/', NGOResourceDetailView.as_view()),
]