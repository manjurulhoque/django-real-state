from django.contrib import admin

from .models import Project, ProjectAmenity, ProjectFeature, ProjectInquiry


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "developer",
        "project_type",
        "status",
        "city",
        "state",
        "available_units",
        "featured",
        "is_published",
        "created_at",
    )
    list_filter = (
        "project_type",
        "status",
        "featured",
        "is_published",
        "state",
        "created_at",
    )
    search_fields = ("name", "description", "city", "state", "address")
    list_editable = ("featured", "is_published", "status")
    readonly_fields = ("view_count", "created_at", "updated_at")

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "developer", "project_type", "status", "description")},
        ),
        ("Location", {"fields": ("address", "city", "state", "zipcode")}),
        (
            "Project Details",
            {
                "fields": (
                    "total_units",
                    "available_units",
                    "price_range_min",
                    "price_range_max",
                )
            },
        ),
        ("Timeline", {"fields": ("start_date", "expected_completion", "launch_date")}),
        (
            "Features",
            {
                "fields": (
                    "total_area",
                    "floors",
                    "parking_spaces",
                    "green_building_certified",
                )
            },
        ),
        ("Media", {"fields": ("main_image", "floor_plan", "brochure")}),
        (
            "Gallery",
            {
                "fields": (
                    "gallery_image_1",
                    "gallery_image_2",
                    "gallery_image_3",
                    "gallery_image_4",
                    "gallery_image_5",
                    "gallery_image_6",
                ),
                "classes": ("collapse",),
            },
        ),
        ("SEO & Marketing", {"fields": ("featured", "is_published", "view_count")}),
        ("External Links", {"fields": ("virtual_tour_url", "website_url")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("developer")


@admin.register(ProjectAmenity)
class ProjectAmenityAdmin(admin.ModelAdmin):
    list_display = ("name", "icon")
    search_fields = ("name", "description")
    ordering = ("name",)


class ProjectFeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 1
    fields = ("amenity", "included", "additional_info")


@admin.register(ProjectInquiry)
class ProjectInquiryAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "name",
        "email",
        "inquiry_type",
        "is_responded",
        "created_at",
    )
    list_filter = ("inquiry_type", "is_responded", "created_at")
    search_fields = ("name", "email", "project__name", "message")
    list_editable = ("is_responded",)
    readonly_fields = ("created_at",)

    fieldsets = (
        (
            "Project & Contact",
            {"fields": ("project", "user", "name", "email", "phone")},
        ),
        (
            "Inquiry Details",
            {
                "fields": (
                    "inquiry_type",
                    "message",
                    "preferred_contact_time",
                    "budget_range",
                )
            },
        ),
        ("Status", {"fields": ("is_responded", "created_at")}),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("project", "user")


# Optionally add the ProjectFeature admin if you want to manage it separately
@admin.register(ProjectFeature)
class ProjectFeatureAdmin(admin.ModelAdmin):
    list_display = ("project", "amenity", "included", "additional_info")
    list_filter = ("included", "amenity")
    search_fields = ("project__name", "amenity__name")

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("project", "amenity")
