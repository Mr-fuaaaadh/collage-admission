from django.shortcuts import render,redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.cache import cache
from django.core.exceptions import ValidationError
from .models import *
from admission_app.models import *
from .forms import ReviewForm , BlogForm
from collages.models import Blog
from django.views.generic.edit import UpdateView , DeleteView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views import View
from django.views.decorators.http import require_http_methods
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class AdminLoginView(View):
    template_name = 'admin/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        print(f"username :  {username}, password   : {password}")

        if not username or not password:
            messages.error(request, 'Username and password are required.')
            return render(request, self.template_name)

        try:
            user = authenticate(request, username=username, password=password)

            if not user :
                messages.error(request, 'Invalid credentials or access denied.')
                return render(request, self.template_name)

            login(request, user)
            return redirect('dashboard')

        except Exception as e:
            logger.exception("Login error")
            messages.error(request, 'An unexpected error occurred. Please try again later.')
            return render(request, self.template_name)



@method_decorator(login_required(login_url='admin-login'), name='dispatch')  # Apply to dispatch method
class AdminDashboard(TemplateView):
    template_name = 'admin/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_data'] = 'Some data to show in the template'
        return context
    
class AdminLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "You have been logged out.")
        return redirect('admin-login')

    
@method_decorator(login_required(login_url='admin-login'), name='dispatch')   
class AdminAddUniversityView(TemplateView ):
    template_name = 'admin/add-university.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def post(self, request, *args, **kwargs):
        try:
            name = request.POST.get('name')
            location = request.POST.get('location')
            rank = request.POST.get('rank')
            description = request.POST.get('description')
            image = request.FILES.get('image')

            # Input validation
            if not name or not location or not rank or not description or not image:
                messages.error(request, "All fields are required.")
                return self.render_to_response(self.get_context_data())

            # Generate slug
            slug = slugify(name)

            # Check if a university with the same slug already exists
            if University.objects.filter(slug=slug).exists():
                messages.error(request, "A university with this name already exists.")
                return self.render_to_response(self.get_context_data())

            # Create and save the university object
            data = University(
                name=name,
                location=location,
                rank=rank,
                description=description,
                image=image,
                slug=slug
            )
            data.save()
            messages.success(request, 'University added successfully!')
            return redirect('university')

        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            return self.render_to_response(self.get_context_data())
        


@method_decorator(login_required(login_url='admin-login'), name='dispatch')   
class AdminAllUniversityViews( TemplateView):
    template_name = 'admin/university_list.html'

    def get(self, request, *args, **kwargs):
        try:
            # Check cache
            universities = cache.get('university_list')
            if not universities:
                universities = University.objects.only('name', 'rank').order_by('-rank')
                cache.set('university_list', universities, 600)

            # Pagination
            paginator = Paginator(universities, 10)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {'universities': page_obj}
            return self.render_to_response(context)
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            return self.render_to_response({'universities': []})
    


@method_decorator(login_required(login_url='admin-login'), name='dispatch')   
def UniversityDeleteView(request, slug):
    try:
        university = get_object_or_404(University, slug=slug)
        university.delete()
        messages.success(request, "University deleted successfully!")
        return redirect("universitys")  # Make sure this is the correct URL name
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return redirect("universitys")



@method_decorator(login_required(login_url='admin-login'), name='dispatch')      
def UniversityUpdateView(request, slug):
    try:
        university = get_object_or_404(University, slug=slug)

        if request.method == 'POST':
            # Get data from the POST request
            university.name = request.POST.get('name')
            university.location = request.POST.get('location')
            university.rank = request.POST.get('rank')
            university.description = request.POST.get('description')

            # Handle file upload if an image is provided
            if 'image' in request.FILES:
                university.image = request.FILES['image']

            # Save the updated university object
            university.save()
            messages.success(request, "University updated successfully!")
            return redirect("universitys")

        # Render the update page with the current data
        return render(request, "admin/university_update.html", {"university": university})

    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")
        return redirect("universitys")
    


@method_decorator(login_required(login_url='admin-login'), name='dispatch')   
class BlogCreateView(SuccessMessageMixin, CreateView):
    model = Blog
    form_class = BlogForm
    template_name = 'admin/blog-create.html'
    success_url = reverse_lazy('blog_create') 
    success_message = "Blog post '%(title)s' was created successfully."

    def form_invalid(self, form):
        messages.error(self.request, "There was an error creating the blog post. Please check the form for errors.")
        print(form.errors)  # Log the form errors for debugging
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Create Blog"
        return context

@method_decorator(login_required(login_url='admin-login'), name='dispatch')   
class BlogListView(ListView):
    model = Blog
    template_name = 'admin/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 10  # Number of blogs per page

    def get_queryset(self):
        return Blog.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Blog List"
        return context


@method_decorator(login_required(login_url='admin-login'), name='dispatch')   
class BlogUpdateView(SuccessMessageMixin, UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = 'admin/blog_update.html'
    success_url = reverse_lazy('blog_list')
    success_message = "Blog post '%(title)s' was updated successfully."

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            print(f"Blog post '{form.instance.title}' updated by user.")
            return response
        except Exception as e:
            print(f"Error while updating blog: {e}")
            form.add_error(None, "An unexpected error occurred.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit Blog: {self.object.title}"
        return context


@method_decorator(login_required(login_url='admin-login'), name='dispatch')   
class BlogDeleteView(View):
    def get(self, request, slug):
        try:
            blog = get_object_or_404(Blog, slug=slug)
            blog.delete()
            messages.success(request, "Blog post deleted successfully!")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
        return redirect("blog_list")

    def post(self, request, slug):
        return self.get(request, slug)  # Use the same logic for both GET and POST



@method_decorator(login_required(login_url='admin-login'), name='dispatch')   
class ReviewCreateView(SuccessMessageMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'admin/review_create.html'
    success_url = reverse_lazy('review_create')
    success_message = "Review by '%(author)s' was created successfully."

    def form_invalid(self, form):
        # Provide clear user feedback and log errors for debugging
        messages.error(self.request, "There was an error creating the review. Please correct the form below.")
        print("Form errors:", form.errors.as_json())  # Better visibility for debugging
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Create Review"
        return context
    


@method_decorator(login_required(login_url='admin-login'), name='dispatch')   
class ReviewListView(ListView):
    model = Review
    template_name = 'admin/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 25 

    def get_queryset(self):
        return Review.objects.all().order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Review List"
        return context



@method_decorator(login_required(login_url='admin-login'), name='dispatch')   
class ReviewUpdateView(SuccessMessageMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'admin/review_create.html' 
    success_url = reverse_lazy('review_list')
    success_message = "Review by '%(author)s' was updated successfully."

    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            print(f"Review updated by {form.instance.author}.")
            return response
        except Exception as e:
            print(f"Error while updating review: {e}")
            form.add_error(None, "An unexpected error occurred.")
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = f"Edit Review by: {self.object.author}"
        return context


@method_decorator(login_required(login_url='admin-login'), name='dispatch')   
class ReviewDeleteView(View):
    def get(self, request, pk):
        try:
            blog = get_object_or_404(Review, pk=pk)
            blog.delete()
            messages.success(request, "Blog post deleted successfully!")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
        return redirect("review_list")

    def post(self, request, pk):
        return self.get(request, pk)  # Use the same logic for both GET and POST

