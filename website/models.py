from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from colorfield.fields import ColorField


class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Zynder Tech")
    site_logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    favicon = models.ImageField(upload_to='logos/', blank=True, null=True)
    primary_color = ColorField(default='#007bff')
    secondary_color = ColorField(default='#6c757d')

    # Contact Information
    phone_number = models.CharField(max_length=20, blank=True)
    phone_number_2 = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)

    # Social Media
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)

    # WhatsApp Business
    whatsapp_number = models.CharField(max_length=20, blank=True,
                                       help_text="Include country code (e.g., +917012473788)")
    whatsapp_message = models.TextField(default="Hello! I'm interested in your services.")

    # Email Settings
    smtp_host = models.CharField(max_length=100, blank=True)
    smtp_port = models.IntegerField(default=587)
    smtp_username = models.CharField(max_length=100, blank=True)
    smtp_password = models.CharField(max_length=100, blank=True)
    smtp_use_tls = models.BooleanField(default=True)

    # Map Location
    map_embed_code = models.TextField(blank=True, help_text="Google Maps embed code")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError('There can be only one SiteSettings instance')
        return super(SiteSettings, self).save(*args, **kwargs)


class HeroSection(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300)
    description = RichTextUploadingField()
    background_image = models.ImageField(upload_to='hero/', blank=True, null=True)
    cta_text = models.CharField(max_length=50, default="Get Started")
    cta_link = models.CharField(max_length=200, default="#services")
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Sections"

    def __str__(self):
        return self.title


class Service(models.Model):
    name = models.CharField(max_length=200)
    short_description = models.TextField(max_length=300)
    full_description = RichTextUploadingField()
    image = models.ImageField(upload_to='services/')
    features = RichTextUploadingField(blank=True)
    specialties = RichTextUploadingField(blank=True)
    pdf_file = models.FileField(upload_to='service_pdfs/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('service_detail', kwargs={'pk': self.pk})


class Training(models.Model):
    name = models.CharField(max_length=200)
    short_description = models.TextField(max_length=300)
    full_description = RichTextUploadingField()
    image = models.ImageField(upload_to='trainings/')
    duration = models.CharField(max_length=100, blank=True)
    level = models.CharField(max_length=50, choices=[
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], default='beginner')
    features = RichTextUploadingField(blank=True)
    curriculum = RichTextUploadingField(blank=True)
    pdf_file = models.FileField(upload_to='training_pdfs/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Training"
        verbose_name_plural = "Trainings"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('training_detail', kwargs={'pk': self.pk})


class TrustedCompany(models.Model):
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to='companies/')
    website_url = models.URLField(blank=True)
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = "Trusted Company"
        verbose_name_plural = "Trusted Companies"

    def __str__(self):
        return self.name


class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    company = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=5)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return f"{self.name} - {self.company}"


class Contact(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    admin_notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"

    def __str__(self):
        return f"{self.full_name} - {self.email}"
