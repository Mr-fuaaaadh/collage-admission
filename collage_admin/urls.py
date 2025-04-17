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
    path('blog/update/<str:slug>/', BlogUpdateView.as_view(), name='blog_update'),
    path('blog/delete/<str:slug>/', BlogDeleteView.as_view(), name='blog_delete'),



    path('add/review/', ReviewCreateView.as_view(), name='review_create'),
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('review/update/<int:pk>/', ReviewUpdateView.as_view(), name='review_update'),
    path('review/delete/<int:pk>/', ReviewDeleteView.as_view(), name='review_delete'),

]