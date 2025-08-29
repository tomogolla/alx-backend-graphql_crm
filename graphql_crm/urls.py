from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from .schema import schema  
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the GraphQL CRM API")


urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),  # Trailing slash is required
]

