from django.db import models
from django.contrib.auth.models import User

from realtors.models import Realtor


class ProjectStatus(models.TextChoices):
    PLANNING = "planning", "Planning"
    UNDER_CONSTRUCTION = "under_construction", "Under Construction"
    NEARING_COMPLETION = "nearing_completion", "Nearing Completion"
    COMPLETED = "completed", "Completed"
    ON_HOLD = "on_hold", "On Hold"


class ProjectType(models.TextChoices):
    RESIDENTIAL = "residential", "Residential"
    COMMERCIAL = "commercial", "Commercial"
    MIXED_USE = "mixed_use", "Mixed Use"
    INDUSTRIAL = "industrial", "Industrial"
    RETAIL = "retail", "Retail"
    OFFICE = "office", "Office"
    HOSPITALITY = "hospitality", "Hospitality"


class Project(models.Model):
    name = models.CharField(max_length=200)
    developer = models.ForeignKey(
        Realtor, on_delete=models.CASCADE, related_name="developed_projects"
    )
    project_type = models.CharField(
        max_length=50, choices=ProjectType.choices, default=ProjectType.RESIDENTIAL
    )
    status = models.CharField(
        max_length=50, choices=ProjectStatus.choices, default=ProjectStatus.PLANNING
    )

    # Location
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)

    # Project Details
    description = models.TextField()
    total_units = models.IntegerField(
        help_text="Total number of units/properties in project"
    )
    available_units = models.IntegerField(help_text="Currently available units")
    price_range_min = models.IntegerField(help_text="Starting price")
    price_range_max = models.IntegerField(help_text="Maximum price")

    # Timeline
    start_date = models.DateField(null=True, blank=True)
    expected_completion = models.DateField(null=True, blank=True)
    launch_date = models.DateField(null=True, blank=True)

    # Project Features
    total_area = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Total project area in sq ft"
    )
    floors = models.IntegerField(
        null=True, blank=True, help_text="Number of floors/levels"
    )
    parking_spaces = models.IntegerField(null=True, blank=True)
    green_building_certified = models.BooleanField(default=False)

    # Media
    main_image = models.ImageField(upload_to="projects/%Y/%m/%d/")
    floor_plan = models.ImageField(
        upload_to="projects/floor_plans/%Y/%m/%d/", blank=True
    )
    brochure = models.FileField(upload_to="projects/brochures/%Y/%m/%d/", blank=True)

    # Gallery images
    gallery_image_1 = models.ImageField(
        upload_to="projects/gallery/%Y/%m/%d/", blank=True
    )
    gallery_image_2 = models.ImageField(
        upload_to="projects/gallery/%Y/%m/%d/", blank=True
    )
    gallery_image_3 = models.ImageField(
        upload_to="projects/gallery/%Y/%m/%d/", blank=True
    )
    gallery_image_4 = models.ImageField(
        upload_to="projects/gallery/%Y/%m/%d/", blank=True
    )
    gallery_image_5 = models.ImageField(
        upload_to="projects/gallery/%Y/%m/%d/", blank=True
    )
    gallery_image_6 = models.ImageField(
        upload_to="projects/gallery/%Y/%m/%d/", blank=True
    )

    # SEO and Marketing
    featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    view_count = models.IntegerField(default=0)

    # Virtual tour and external links
    virtual_tour_url = models.URLField(blank=True)
    website_url = models.URLField(blank=True, help_text="Project official website")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.name

    def increment_view_count(self):
        self.view_count += 1
        self.save(update_fields=["view_count"])

    def get_completion_percentage(self):
        """Calculate project completion percentage based on status"""
        status_percentages = {
            "planning": 10,
            "under_construction": 50,
            "nearing_completion": 85,
            "completed": 100,
            "on_hold": 0,
        }
        return status_percentages.get(self.status, 0)

    def get_gallery_images(self):
        """Return list of non-empty gallery images"""
        images = []
        for i in range(1, 7):
            image = getattr(self, f"gallery_image_{i}")
            if image:
                images.append(image)
        return images

    def is_available(self):
        """Check if project has available units"""
        return self.available_units > 0

    def get_price_range_display(self):
        """Return formatted price range"""
        if self.price_range_min == self.price_range_max:
            return f"${self.price_range_min:,}"
        return f"${self.price_range_min:,} - ${self.price_range_max:,}"


class ProjectAmenity(models.Model):
    """Amenities available in the project"""

    name = models.CharField(max_length=100)
    icon = models.CharField(
        max_length=50, blank=True, help_text="FontAwesome icon class"
    )
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = "Project Amenities"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ProjectFeature(models.Model):
    """Through model for project amenities with additional details"""

    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amenity = models.ForeignKey(ProjectAmenity, on_delete=models.CASCADE)
    included = models.BooleanField(default=True)
    additional_info = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ("project", "amenity")

    def __str__(self):
        return f"{self.project.name} - {self.amenity.name}"


class ProjectInquiry(models.Model):
    """Model to handle project inquiries"""

    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="inquiries"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Contact Information
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    # Inquiry Details
    inquiry_type = models.CharField(
        max_length=50,
        choices=[
            ("general", "General Information"),
            ("visit", "Schedule Visit"),
            ("booking", "Book Unit"),
            ("investment", "Investment Opportunity"),
            ("brochure", "Request Brochure"),
        ],
        default="general",
    )

    message = models.TextField()
    preferred_contact_time = models.CharField(max_length=100, blank=True)
    budget_range = models.CharField(max_length=100, blank=True)

    # Status
    is_responded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.project.name} - {self.name} ({self.inquiry_type})"
