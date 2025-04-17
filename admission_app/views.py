from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView
from .models import University, College
from  collage_admin.models import Review
from .forms import AdmissionApplicationForm
from collages.models import *
from django.http import Http404

import logging
from django.views import View
from django.db.models import Q
logger = logging.getLogger(__name__)

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Default empty lists
        context['universities'] = []
        context['colleges'] = []
        context['blogs'] = []
        context['reviews'] = []

        # Fetch data with error handling and logging
        try:
            context['universities'] = University.objects.all().only("id", "name", "location")
        except Exception as e:
            logger.error(f"Error fetching universities: {e}")

        try:
            context['colleges'] = College.objects.all().only("id", "name", "location")
        except Exception as e:
            logger.error(f"Error fetching colleges: {e}")

        try:
            context['blogs'] = Blog.objects.all().only("id", "title", "image", "slug")
        except Exception as e:
            logger.error(f"Error fetching blogs: {e}")

        try:
            context['reviews'] = Review.objects.all().only("id", "author", "image", "rating", "comment", "created_at", "updated_at")
        except Exception as e:
            logger.error(f"Error fetching reviews: {e}")

        return context
    

class CollageListView(ListView):
    template_name = 'collages.html'
    context_object_name = 'collages'
    model = College
    paginate_by = 20
    ordering = 'name'

    def get_queryset(self):
        queryset = College.objects.order_by(self.ordering).only("id", "name", "location")
        query = self.request.GET.get('q', '')

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(location__icontains=query)
            )

        if not queryset.exists():
            logger.warning("No colleges found matching query.")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_count'] = self.get_queryset().count()
        context['page_title'] = "College List"
        context['query'] = self.request.GET.get('q', '')  # Keep the query value in template
        return context

    
class ContactView(TemplateView):
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Contact Us"
        return context


class CollegeDetailsView(View):
    template_name = 'collage-details.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = AdmissionApplicationForm()
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print("Form submission received.")
        form = AdmissionApplicationForm(request.POST, request.FILES)
        context = self.get_context_data()

        if form.is_valid():
            form.save()
            logger.info(f"Application submitted: {form.cleaned_data}")
            context['success'] = "Application submitted successfully."
            context['form'] = AdmissionApplicationForm()
            print("Form submission successful.")
        else:
            logger.warning("Form submission failed due to validation errors.")
            logger.warning(f"Form errors: {form.errors}")
            context['error'] = "There were errors in your form. Please correct them and try again."
            context['form'] = form
            print("Form submission failed.")

        return render(request, self.template_name, context)


    def get_context_data(self):
        slug = self.kwargs.get('slug')

        if not slug:
            logger.error("College slug not provided in URL.")
            raise Http404("College slug not provided.")

        college = get_object_or_404(College, slug=slug)
        courses = Courses.objects.filter(college=college)
        colleges = College.objects.all()

        if not courses.exists():
            logger.warning(f"No courses found for college: {college.name}")
        else:
            logger.info(f"Courses found for college: {college.name}")

        return {
            'college': college,
            'courses': courses,
            'colleges': colleges,
            'page_title': "College Details",
        }
    

class CourseDetailsView(TemplateView):
    template_name = 'course-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('id')
        course = get_object_or_404(Courses, pk=id)
        context['page_title'] = "Course Details"
        context['course'] = course
        return context
    



class BlogListView(ListView):
    model = Blog
    template_name = 'blog.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Blogs"
        
        return context
    

class BlogDetailsView(TemplateView):
    template_name = 'blog-details.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get the blog by slug
        slug = self.kwargs.get("slug")
        blog = get_object_or_404(Blog, slug=slug)

        # Pass the specific blog and all blogs (if needed for sidebar/recent posts)
        context[self.context_object_name] = blog
        context['blogs'] = Blog.objects.all()  # Get all blogs for sidebar or related posts
        context['page_title'] = "Blog Details"

        return context


class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogs = Blog.objects.all()
        context['blogs'] = blogs
        context['page_title'] = "About Us"
        return context
    

