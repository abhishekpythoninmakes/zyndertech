from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import *
from .forms import ContactForm
import json


def home(request):
    hero_section = HeroSection.objects.filter(is_active=True).first()
    services = Service.objects.filter(is_featured=True)[:6]
    trainings = Training.objects.filter(is_featured=True)[:6]
    trusted_companies = TrustedCompany.objects.all()
    testimonials = Testimonial.objects.filter(is_featured=True)[:6]

    context = {
        'hero_section': hero_section,
        'services': services,
        'trainings': trainings,
        'trusted_companies': trusted_companies,
        'testimonials': testimonials,
    }
    return render(request, 'website/index.html', context)


def services_list(request):
    services = Service.objects.all()
    paginator = Paginator(services, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'services': page_obj,
    }
    return render(request, 'website/services.html', context)


def service_detail(request, pk):
    service = get_object_or_404(Service, pk=pk)
    related_services = Service.objects.exclude(pk=pk)[:3]

    context = {
        'service': service,
        'related_services': related_services,
    }
    return render(request, 'website/service_detail.html', context)


def trainings_list(request):
    trainings = Training.objects.all()
    paginator = Paginator(trainings, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'trainings': page_obj,
    }
    return render(request, 'website/trainings.html', context)


def training_detail(request, pk):
    training = get_object_or_404(Training, pk=pk)
    whatsapp_message = f"Hi, I'm interested in {training.name} training. Please provide more details about enrollment."
    related_trainings = Training.objects.exclude(pk=pk)[:3]

    context = {
        'training': training,
        'related_trainings': related_trainings,
        "whatsapp_message": whatsapp_message,
    }
    return render(request, 'website/training_detail.html', context)


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()

            # Send email notification
            try:
                site_settings = SiteSettings.objects.first()
                if site_settings and site_settings.smtp_username:
                    send_mail(
                        subject=f'New Contact Form Submission from {contact.full_name}',
                        message=f'Name: {contact.full_name}\nEmail: {contact.email}\nPhone: {contact.phone_number}\nMessage: {contact.message}',
                        from_email=site_settings.smtp_username,
                        recipient_list=[site_settings.email or site_settings.smtp_username],
                        fail_silently=True,
                    )
            except:
                pass

            messages.success(request, 'Thank you for your message. We will get back to you soon!')
            return redirect('/')
    else:
        form = ContactForm()

    return render(request, 'website/contact.html', {'form': form})


def live_search(request):
    query = request.GET.get('q', '')
    results = []

    if query:
        # Search services
        services = Service.objects.filter(
            Q(name__icontains=query) | Q(short_description__icontains=query)
        )[:5]

        for service in services:
            results.append({
                'type': 'service',
                'id': service.id,
                'name': service.name,
                'description': service.short_description,
                'url': service.get_absolute_url(),
                'image': service.image.url if service.image else None,
            })

        # Search trainings
        trainings = Training.objects.filter(
            Q(name__icontains=query) | Q(short_description__icontains=query)
        )[:5]

        for training in trainings:
            results.append({
                'type': 'training',
                'id': training.id,
                'name': training.name,
                'description': training.short_description,
                'url': training.get_absolute_url(),
                'image': training.image.url if training.image else None,
            })

    return JsonResponse({'results': results})


def contact_view_new(request):
    """
    Renders contact form and optionally pre-fills the message from:
    /contact/?message=... or /contact/?item=Service%20Name
    """
    prefill = request.GET.get("message", "")
    item = request.GET.get("item") or request.GET.get("subject")
    if not prefill and item:
        prefill = f"I'm interested in {item}. Please share more details."

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            try:
                site_settings = SiteSettings.objects.first()
                # optional: email sending kept as in your existing codebase
                if site_settings and site_settings.smtp_username:
                    send_mail(
                        subject=f'New Contact Form Submission from {contact.full_name}',
                        message=f'Name: {contact.full_name}\nEmail: {contact.email}\nPhone: {contact.phone_number}\nMessage: {contact.message}',
                        from_email=site_settings.smtp_username,
                        recipient_list=[site_settings.email or site_settings.smtp_username],
                        fail_silently=True,
                    )
            except Exception:
                pass

            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Thank you for your message. We will get back to you soon!'
                })
            else:
                messages.success(request, "Thank you for your message. We will get back to you soon!")
                return redirect("home")
        else:
            # Handle form errors for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                }, status=400)
    else:
        form = ContactForm(initial={"message": prefill} if prefill else None)

    return render(request, "website/contact.html", {"form": form})


