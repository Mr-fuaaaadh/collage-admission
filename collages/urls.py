from django.urls import path
from .views import *

urlpatterns = [
    path('colleges/', CollegeListView.as_view(), name='college_list'),
    path('colleges/add/', CollegeCreateView.as_view(), name='college_add'),
    path('colleges/<int:pk>/edit/', CollegeUpdateView.as_view(), name='college_edit'),
    path('colleges/<int:pk>/delete/', CollegeDeleteView, name='college_delete'),
    path('colleges/<int:pk>/', CollegeDetailView.as_view(), name='college_detail'),


    path('collage/<int:pk>/courses/', CourseListView.as_view(), name='course_list'),
    path('collage/<int:pk>/course/delete/', CourseDeleteView, name='course_delete'),
    path('collage/<int:pk>/course/edit/', CourseUpdateView, name='course_update'),

    path('collage/admission/enquiry/', AllAdmissionEnquiryView.as_view(), name='admission_enquiry'),
    path('admission/enquiry/mark/viewed/<int:pk>/', AdmissionEnquiryDetailView.as_view(), name='admission_enquiry_mark_viewed'),
    path('admission/enquiry/<int:pk>/mark/viewed/', MarkAsViewedView.as_view(), name='admission_enquiry_mark_viewed_column'),
]