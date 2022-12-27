from django.urls import path
from . import views

app_name = 'arquivos'

urlpatterns = [
    path('', views.home, name='home'),
    path('files', views.files, name='files'),
    path('search/', views.search, name='search'),
    path('media-images/', views.images, name='images'),
    path('media-documents/', views.documents, name='documents'),
    path('media-videos/', views.videos, name='videos'),
    path('categorys/<str:categoria>', views.categorys, name='categorys'),
    path('detail/<int:id>', views.detail, name='detail')
]