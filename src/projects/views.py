from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Project, ProjectInquiry, ProjectAmenity
from listings.choices import state_choices


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/projects.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        return Project.objects.filter(is_published=True).order_by('-featured', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_projects'] = Project.objects.filter(
            is_published=True, featured=True
        ).order_by('-created_at')[:3]
        context['state_choices'] = state_choices
        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'
    context_object_name = 'project'
    pk_url_kwarg = 'project_id'
    
    def get_object(self):
        project = get_object_or_404(Project, id=self.kwargs['project_id'], is_published=True)
        # Increment view count
        project.increment_view_count()
        return project
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        project = self.get_object()
        
        # Get related projects (same city/state)
        context['related_projects'] = Project.objects.filter(
            is_published=True,
            city=project.city,
            state=project.state
        ).exclude(id=project.id)[:3]
        
        # Get project amenities
        context['project_amenities'] = project.projectfeature_set.filter(included=True)
        
        return context


def search_projects(request):
    """Search projects based on various criteria"""
    queryset = Project.objects.filter(is_published=True)
    
    # Search parameters
    query = request.GET.get('query', '')
    project_type = request.GET.get('project_type', '')
    status = request.GET.get('status', '')
    city = request.GET.get('city', '')
    state = request.GET.get('state', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    
    # Apply filters
    if query:
        queryset = queryset.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(address__icontains=query)
        )
    
    if project_type:
        queryset = queryset.filter(project_type=project_type)
    
    if status:
        queryset = queryset.filter(status=status)
    
    if city:
        queryset = queryset.filter(city__iexact=city)
    
    if state:
        queryset = queryset.filter(state__iexact=state)
    
    if min_price:
        try:
            queryset = queryset.filter(price_range_min__gte=int(min_price.replace(',', '')))
        except ValueError:
            pass
    
    if max_price:
        try:
            queryset = queryset.filter(price_range_max__lte=int(max_price.replace(',', '')))
        except ValueError:
            pass
    
    # Pagination
    paginator = Paginator(queryset.order_by('-featured', '-created_at'), 12)
    page_number = request.GET.get('page')
    projects = paginator.get_page(page_number)
    
    context = {
        'projects': projects,
        'state_choices': state_choices,
        'project_types': Project._meta.get_field('project_type').choices,
        'project_statuses': Project._meta.get_field('status').choices,
        'values': request.GET,
        'search_performed': bool(request.GET),
    }
    
    return render(request, 'projects/search.html', context)


def project_inquiry(request, project_id):
    """Handle project inquiry form submission"""
    project = get_object_or_404(Project, id=project_id, is_published=True)
    
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        inquiry_type = request.POST.get('inquiry_type', 'general')
        message = request.POST.get('message', '').strip()
        preferred_contact_time = request.POST.get('preferred_contact_time', '').strip()
        budget_range = request.POST.get('budget_range', '').strip()
        
        # Basic validation
        if not all([name, email, message]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('projects:project_detail', project_id=project.id)
        
        # Create inquiry
        try:
            inquiry = ProjectInquiry.objects.create(
                project=project,
                user=request.user if request.user.is_authenticated else None,
                name=name,
                email=email,
                phone=phone,
                inquiry_type=inquiry_type,
                message=message,
                preferred_contact_time=preferred_contact_time,
                budget_range=budget_range,
            )
            
            messages.success(
                request, 
                f'Thank you for your interest in {project.name}! '
                'Our team will contact you within 24 hours.'
            )
            
        except Exception as e:
            messages.error(request, 'There was an error submitting your inquiry. Please try again.')
        
        return redirect('projects:project_detail', project_id=project.id)
    
    # GET request - redirect to project detail
    return redirect('projects:project_detail', project_id=project.id)


@login_required
def my_project_inquiries(request):
    """Display user's project inquiries"""
    inquiries = ProjectInquiry.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(inquiries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'inquiries': page_obj,
    }
    
    return render(request, 'projects/my_inquiries.html', context) 