from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, TemplateView
from .models import University, College
from collages.models import *
import logging
from django.db.models import Q
logger = logging.getLogger(__name__)

class HomeView(ListView):
    template_name = 'index.html'
    context_object_name = 'data'

    def get_queryset(self):
        try:
            universities = list(University.objects.only("id", "name", "location"))
            colleges = list(College.objects.only("id", "name", "location"))
            blog  = list(Blog.objects.only("id", "title", "image", "slug"))
            return {"universities": universities, "colleges": colleges, "blogs": blog}
        except University.DoesNotExist:
            logger.error("University data not found.")
            return {"universities": [], "colleges": []}
        except College.DoesNotExist:
            logger.error("College data not found.")
            return {"universities": [], "colleges": []}
        except Blog.DoesNotExist:
            logger.error("Blog data not found.")
            return {"universities": [], "colleges": []}
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            return {"universities": [], "colleges": []}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_queryset())
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


class CollegeDetailsView(TemplateView):
    template_name = 'collage-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        college = get_object_or_404(College, slug=slug)
        course =  Courses.objects.filter(college=college)
        for c in course:
            print(f" Course Name: {c.name}, Image : {c.image} ")

        if not course.exists():
            logger.warning(f"No courses found for college: {college.name}")
        else:
            logger.info(f"Courses found for college: {college.name}")
        context['courses'] = course
        context['page_title'] = "College Details"
        context['college'] = college
        return context
    

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
    



    