from django.urls import path
from .views import *


urlpatterns = [
    path('', AdminDashboard.as_view(), name='dashboard'),
    path('add/university/', AdminAddUniversityView.as_view(), name='university'),
    path('universitys/', AdminAllUniversityViews.as_view(), name='universitys'),
    path('university/update/<str:slug>/', UniversityUpdateView, name='university_update'),
    path('university/delete/<str:slug>/', UniversityDeleteView, name='university_delete'),

    path('add/blog/', BlogCreateView.as_view(), name='blog_create'),
    path('blogs/', BlogListView.as_view(), name='blog_list'),

]