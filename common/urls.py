from django.urls import path
from common import views

app_name = 'common'
urlpatterns = [
    path('file/protected/', views.ProtectedFileView.as_view(), name='protected_file'),
]
