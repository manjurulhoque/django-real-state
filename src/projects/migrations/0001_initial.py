# Generated by Django 5.2.3 on 2025-06-11 13:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("realtors", "0002_alter_realtor_id"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="ProjectAmenity",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "icon",
                    models.CharField(
                        blank=True, help_text="FontAwesome icon class", max_length=50
                    ),
                ),
                ("description", models.TextField(blank=True)),
            ],
            options={
                "verbose_name_plural": "Project Amenities",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                (
                    "project_type",
                    models.CharField(
                        choices=[
                            ("residential", "Residential"),
                            ("commercial", "Commercial"),
                            ("mixed_use", "Mixed Use"),
                            ("industrial", "Industrial"),
                            ("retail", "Retail"),
                            ("office", "Office"),
                            ("hospitality", "Hospitality"),
                        ],
                        default="residential",
                        max_length=50,
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("planning", "Planning"),
                            ("under_construction", "Under Construction"),
                            ("nearing_completion", "Nearing Completion"),
                            ("completed", "Completed"),
                            ("on_hold", "On Hold"),
                        ],
                        default="planning",
                        max_length=50,
                    ),
                ),
                ("address", models.CharField(max_length=200)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=100)),
                ("zipcode", models.CharField(max_length=20)),
                ("description", models.TextField()),
                (
                    "total_units",
                    models.IntegerField(
                        help_text="Total number of units/properties in project"
                    ),
                ),
                (
                    "available_units",
                    models.IntegerField(help_text="Currently available units"),
                ),
                ("price_range_min", models.IntegerField(help_text="Starting price")),
                ("price_range_max", models.IntegerField(help_text="Maximum price")),
                ("start_date", models.DateField(blank=True, null=True)),
                ("expected_completion", models.DateField(blank=True, null=True)),
                ("launch_date", models.DateField(blank=True, null=True)),
                (
                    "total_area",
                    models.DecimalField(
                        decimal_places=2,
                        help_text="Total project area in sq ft",
                        max_digits=10,
                    ),
                ),
                (
                    "floors",
                    models.IntegerField(
                        blank=True, help_text="Number of floors/levels", null=True
                    ),
                ),
                ("parking_spaces", models.IntegerField(blank=True, null=True)),
                ("green_building_certified", models.BooleanField(default=False)),
                ("main_image", models.ImageField(upload_to="projects/%Y/%m/%d/")),
                (
                    "floor_plan",
                    models.ImageField(
                        blank=True, upload_to="projects/floor_plans/%Y/%m/%d/"
                    ),
                ),
                (
                    "brochure",
                    models.FileField(
                        blank=True, upload_to="projects/brochures/%Y/%m/%d/"
                    ),
                ),
                (
                    "gallery_image_1",
                    models.ImageField(
                        blank=True, upload_to="projects/gallery/%Y/%m/%d/"
                    ),
                ),
                (
                    "gallery_image_2",
                    models.ImageField(
                        blank=True, upload_to="projects/gallery/%Y/%m/%d/"
                    ),
                ),
                (
                    "gallery_image_3",
                    models.ImageField(
                        blank=True, upload_to="projects/gallery/%Y/%m/%d/"
                    ),
                ),
                (
                    "gallery_image_4",
                    models.ImageField(
                        blank=True, upload_to="projects/gallery/%Y/%m/%d/"
                    ),
                ),
                (
                    "gallery_image_5",
                    models.ImageField(
                        blank=True, upload_to="projects/gallery/%Y/%m/%d/"
                    ),
                ),
                (
                    "gallery_image_6",
                    models.ImageField(
                        blank=True, upload_to="projects/gallery/%Y/%m/%d/"
                    ),
                ),
                ("featured", models.BooleanField(default=False)),
                ("is_published", models.BooleanField(default=True)),
                ("view_count", models.IntegerField(default=0)),
                ("virtual_tour_url", models.URLField(blank=True)),
                (
                    "website_url",
                    models.URLField(blank=True, help_text="Project official website"),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "developer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="developed_projects",
                        to="realtors.realtor",
                    ),
                ),
            ],
            options={
                "verbose_name": "Project",
                "verbose_name_plural": "Projects",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="ProjectInquiry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=254)),
                ("phone", models.CharField(max_length=20)),
                (
                    "inquiry_type",
                    models.CharField(
                        choices=[
                            ("general", "General Information"),
                            ("visit", "Schedule Visit"),
                            ("booking", "Book Unit"),
                            ("investment", "Investment Opportunity"),
                            ("brochure", "Request Brochure"),
                        ],
                        default="general",
                        max_length=50,
                    ),
                ),
                ("message", models.TextField()),
                (
                    "preferred_contact_time",
                    models.CharField(blank=True, max_length=100),
                ),
                ("budget_range", models.CharField(blank=True, max_length=100)),
                ("is_responded", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="inquiries",
                        to="projects.project",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="ProjectFeature",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("included", models.BooleanField(default=True)),
                ("additional_info", models.CharField(blank=True, max_length=200)),
                (
                    "amenity",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.projectamenity",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="projects.project",
                    ),
                ),
            ],
            options={
                "unique_together": {("project", "amenity")},
            },
        ),
    ]
