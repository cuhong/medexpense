from django.urls import path
from expense import views_company as views

app_name = 'company'
urlpatterns = [
    path('', views.UserIndexView.as_view(), name='index'),
    path('claim/create/', views.ClaimCreateView.as_view(), name='claim_create'),
    path('claim/<uuid:claim_id>/', views.ClaimDetailView.as_view(), name='claim_detail')
]
