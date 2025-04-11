from django.urls import path
from .views import *

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('colleges/', CollageListView.as_view(), name='colleges'),
    path('contact/', ContactView.as_view(), name='contact'),

    path('blog/', BlogListView.as_view(), name='blog'),
    path('blog/<slug:slug>/', BlogDetailsView.as_view(), name='blog_detail'),

    path('college/<str:slug>/details/', CollegeDetailsView.as_view(), name='college_details'),
    path('college/<int:id>/apply/', CourseDetailsView.as_view(), name='college_apply'),

    path('about/', AboutView.as_view(), name='about'),

]