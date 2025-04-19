from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, UpdateView, DetailView
from django.views import View
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.db.models import Q
from django.contrib import messages
from admission_app.models import College
from.models import Courses, Admission
from django.core.exceptions import ValidationError
from admission_app.forms import AdmissionApplicationForm
from admission_app.models import University
from django.http import JsonResponse
from .forms import CourseForm, CollageForm
import logging
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Configure logging
logger = logging.getLogger(__name__)

# Utility function for displaying messages
def display_message(request, msg, msg_type="info"):
    messages.add_message(request, getattr(messages, msg_type.upper()), msg)

# Base College View (for common functionality)
@method_decorator(login_required(login_url='admin-login'), name='dispatch')
class BaseCollegeView(View):
    model = College
    template_name = ''
    success_url = reverse_lazy('college_list')

    def get_object(self, pk):
        try:
            return get_object_or_404(self.model, pk=pk)
        except ValidationError:
            display_message(self.request, "Invalid College ID", "warning")
            return None

# College List View
@method_decorator(login_required(login_url='admin-login'), name='dispatch')
class CollegeListView(BaseCollegeView):
    template_name = 'admin/college_list.html'

    def get(self, request):
        colleges = self.model.objects.all()

        context = {'colleges': colleges}
        return render(request, self.template_name, context)

# College Create View
@method_decorator(login_required(login_url='admin-login'), name='dispatch')
class CollegeCreateView(BaseCollegeView):
    template_name = 'admin/college_form.html'
    success_url = 'college_add'  # You can override this as needed

    def get(self, request):
        universities = University.objects.all()
        if not universities.exists():
            messages.warning(request, "No universities available. Please add a university first.")
            return redirect(self.success_url)

        form = CollageForm()
        context = {
            'form': form,
            'universities': universities,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = CollageForm(request.POST, request.FILES)

        # Debug uploaded files (optional)
        print("FILES:", request.FILES)

        if form.is_valid():
            try:
                form.save()
                messages.success(request, "College added successfully!")
                return redirect(self.success_url)
            except Exception as e:
                messages.error(request, f"Error saving college: {str(e)}")
                return redirect(self.success_url)
        else:
            errors = form.errors.as_text()
            messages.error(request, f"Form is invalid:\n{errors}")
            universities = University.objects.all()
            context = {
                'form': form,
                'universities': universities,
            }
            return render(request, self.template_name, context)


@method_decorator(login_required(login_url='admin-login'), name='dispatch')
class CollegeUpdateView(BaseCollegeView):
    template_name = 'admin/college_form.html'

    def get(self, request, pk):
        college = self.get_object(pk)
        if not college:
            display_message(request, "College not found.", "warning")
            return redirect(self.success_url)

        universities = University.objects.all()
        if not universities.exists():
            display_message(request, "No universities available. Please add a university first.", "warning")
            return redirect(self.success_url)

        form = CollageForm(instance=college)
        return render(request, self.template_name, {
            'college': college,
            'universities': universities,
            'form': form,
        })

    def post(self, request, pk):
        college = self.get_object(pk)
        if not college:
            display_message(request, "College not found.", "warning")
            return redirect(self.success_url)

        form = CollageForm(request.POST, request.FILES, instance=college)
        print("FILES:", request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "College updated successfully!")
            return redirect(self.success_url)
        else:
            universities = University.objects.all()
            display_message(request, f"Please correct the errors in the form.", "{form.error}")
            messages.error(request, mark_safe(form.errors.as_ul()))
            return render(request, self.template_name, {
                'college': college,
                'universities': universities,
                'form': form,
            })

# College Detail View
@method_decorator(login_required(login_url='admin-login'), name='dispatch')
class CollegeDetailView(BaseCollegeView):
    template_name = 'admin/college_detail.html'

    def get(self, request, pk):
        college = self.get_object(pk)
        if college is None:
            return redirect(self.success_url)
        context = {'college': college}
        return render(request, self.template_name, context)

# College Delete View
@method_decorator(login_required(login_url='admin-login'), name='dispatch')
def CollegeDeleteView(request, pk,):
    college = get_object_or_404(College, pk=pk)
    try:
        college.delete()
        display_message(request, "College deleted successfully!", "success")
    except Exception as e:
        display_message(request, f"Error deleting college: {str(e)}", "error")
    return redirect('college_list')







# Note : The above code is a using collage based coureses model and its views.
# The code has been modified to include the necessary imports and utility functions.
# The views are structured to handle the creation, updating, listing, and deletion of college courses.
# The code also includes error handling and user feedback through messages.


@method_decorator(login_required(login_url='admin-login'), name='dispatch')
class CourseListView(View):
    template_name = 'admin/course_list.html'

    def get(self, request, pk=None):
        """Handles GET request to retrieve all or filtered courses."""
        try:
            if pk:
                courses = Courses.objects.filter(college__pk=pk).select_related('college')
            else:
                courses = Courses.objects.select_related('college').all()

            return render(request, self.template_name, {'courses': courses,'form': CourseForm()})
        except Exception as e:
            messages.error(request, f"Error fetching courses: {str(e)}")
            return render(request, self.template_name, {'courses': [], 'form': CourseForm()})

    def post(self, request, pk=None):
        """Handles POST request to create a new course."""
        try:
            form = CourseForm(request.POST)
            print(f"form data is  {form.data}")
            if form.is_valid():
                form.save()
                print("Course added successfully!")
                messages.success(request, "Course added successfully.")
                return redirect('course_list', pk=pk)  # Redirect to the same page

            messages.error(request, "Invalid data. Please correct the errors below.")
            return self.get(request, pk)  # Reload page with errors

        except Exception as e:
            messages.error(request, f"Error adding course: {str(e)}")
            return self.get(request, pk)


@method_decorator(login_required(login_url='admin-login'), name='dispatch')
def CourseDeleteView(request, pk):
    try:
        course = get_object_or_404(Courses, pk=pk)
        collage_id = course.college.pk 
        course.delete()
        messages.success(request, "Course deleted successfully.")
    except Exception as e:
        messages.error(request, f"Error deleting course: {str(e)}")
    return redirect('course_list', pk=collage_id)

@method_decorator(login_required(login_url='admin-login'), name='dispatch')
def CourseUpdateView(request, pk):
    course = get_object_or_404(Courses, pk=pk)

    if request.method == 'POST':
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, "Course updated successfully.")
            return redirect(reverse('course_list', kwargs={'pk': course.college.pk}))
        else:
            messages.error(request, "Invalid data. Please correct the errors below.")
    else:
        form = CourseForm(instance=course)

    return render(request, 'admin/course_edit.html', {
        'form': form,
        'course': course
    })


def display_message(request, message, level="info"):
    levels = {
        "debug": messages.DEBUG,
        "info": messages.INFO,
        "success": messages.SUCCESS,
        "warning": messages.WARNING,
        "error": messages.ERROR,
    }
    messages.add_message(request, levels.get(level, messages.INFO), message)



class PageTitleMixin:
    """Mixin to inject a page title into the context."""
    page_title: str = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = self.page_title
        return context

@method_decorator(login_required(login_url='admin-login'), name='dispatch')
class AllAdmissionEnquiryView(PageTitleMixin, ListView):
    """
    View to list all admission enquiries.
    Displays 10 enquiries per page.
    """
    model = Admission
    template_name = 'admin/admission_enquiry.html'
    context_object_name = 'enquiries'
    paginate_by = 10
    page_title = "Admission Enquiries"

    def get_queryset(self):
        return Admission.objects.order_by('-created_at')

@method_decorator(login_required(login_url='admin-login'), name='dispatch')
class AdmissionEnquiryDetailView(PageTitleMixin, DetailView):
    """
    View to display the detail of a single admission enquiry.
    """
    model = Admission
    template_name = 'admin/admission_enquiry_detail.html'
    context_object_name = 'enquiry'
    page_title = "Admission Enquiry Detail"

@method_decorator(login_required(login_url='admin-login'), name='dispatch')
class MarkAsViewedView(View):
    """
    View to update the is_viewed field of an enquiry.
    Triggered by a POST request from the detail page.
    """
    def get(self, request, pk):
        enquiry = get_object_or_404(Admission, pk=pk)
        if not enquiry.is_viewed:
            enquiry.is_viewed = True
            enquiry.save()
        return redirect('admission_enquiry_mark_viewed', pk=pk)
    
