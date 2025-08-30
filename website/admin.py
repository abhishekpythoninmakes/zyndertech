from django.contrib import admin
from django.utils.html import format_html
from .models import *


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Basic Information', {
            'fields': ('site_name', 'site_logo', 'favicon', 'primary_color', 'secondary_color')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'phone_number_2', 'email', 'address')
        }),
        ('Social Media', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url')
        }),
        ('WhatsApp Business', {
            'fields': ('whatsapp_number', 'whatsapp_message')
        }),
        ('Email Settings', {
            'fields': ('smtp_host', 'smtp_port', 'smtp_username', 'smtp_password', 'smtp_use_tls')
        }),
        ('Map Location', {
            'fields': ('map_embed_code',)
        }),
    )

    def logo_preview(self, obj):
        if obj.site_logo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.site_logo.url)
        return "No logo"

    logo_preview.short_description = "Logo Preview"

    list_display = ['site_name', 'logo_preview', 'phone_number', 'email']

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()


@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle']

    def image_preview(self, obj):
        if obj.background_image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.background_image.url)
        return "No image"

    image_preview.short_description = "Background Preview"


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview', 'is_featured', 'order', 'created_at']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['name', 'short_description']
    list_editable = ['is_featured', 'order']
    ordering = ['order', 'name']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return "No image"

    image_preview.short_description = "Image Preview"

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'short_description', 'image', 'is_featured', 'order')
        }),
        ('Detailed Information', {
            'fields': ('full_description', 'features', 'specialties', 'pdf_file')
        }),
    )


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview', 'level', 'duration', 'is_featured', 'order', 'created_at']
    list_filter = ['level', 'is_featured', 'created_at']
    search_fields = ['name', 'short_description']
    list_editable = ['is_featured', 'order']
    ordering = ['order', 'name']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return "No image"

    image_preview.short_description = "Image Preview"

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'short_description', 'image', 'duration', 'level', 'is_featured', 'order')
        }),
        ('Detailed Information', {
            'fields': ('full_description', 'features', 'curriculum', 'pdf_file')
        }),
    )


@admin.register(TrustedCompany)
class TrustedCompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_preview', 'website_url', 'order', 'created_at']
    list_editable = ['order']
    search_fields = ['name']
    ordering = ['order', 'name']

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.logo.url)
        return "No logo"

    logo_preview.short_description = "Logo Preview"


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ['name', 'image_preview', 'company', 'rating', 'is_featured', 'order', 'created_at']
    list_filter = ['rating', 'is_featured', 'created_at']
    search_fields = ['name', 'company', 'review']
    list_editable = ['is_featured', 'order']
    ordering = ['order', '-created_at']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image.url)
        return "No image"

    image_preview.short_description = "Image Preview"


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone_number', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['full_name', 'email', 'phone_number']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Contact Information', {
            'fields': ('full_name', 'email', 'phone_number', 'message')
        }),
        ('Admin Section', {
            'fields': ('status', 'admin_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
