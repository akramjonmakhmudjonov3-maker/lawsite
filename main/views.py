import stripe 
from django.views.decorators.csrf import csrf_exempt
from .models import Payment
from django.conf import settings
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.shortcuts import render
from .models import ContactMessage
from django.contrib.auth.models import User
from reportlab.pdfgen import canvas
from django.http import HttpResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    event = None

    try:
            event = stripe.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
    )
    except Exception:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
    
    email = session['customer_email']['email']
    amount = session['amount_total'] / 100

    Payment.objects.create(
        email=email,
        amoount=amount,
        plan="Consultation"
        
    )
    return HttpResponse(status=200)

def create_checkout(request, price):
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=request.GET.get("email"),
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': ' Consultation',
                },
                'unit_amount': int(price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://lawsite.onrender.com/success/',
        cancel_url='https://lawsite.onrender.com/cancel/',
    )
    return redirect(session.url)

def success(request):
    return render(request, 'main/success.html')

def cancel(request):
    return render(request, 'main/cancel.html')

def home(request):
    return render(request, 'main/index.html')



def pdf_view(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, "Invoice")
    p.drawString(100, 730, "Client Test")
    p.drawString(100, 710, "Amount: $1000")
    
    
    p.save()

    return response

if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="pasprague623@gmail.com",
        password="adminpassword"

    )

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        subject = request.POST.get("subject") or "New Contact Form"
        email = request.POST.get("email")
        message = request.POST.get("message")
        
        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        full_message = f"From: {name}\nEmail: {email}\nMessage: {message}"
        
        send_mail(
                  subject,
                  full_message,
                  email,
                  ['pasprague623@gmail.com'],
        )
        send_mail(
            "We received your message",
            "Thank you for contacting us. We will get back to you shortlt",
            'pasprague623@gmail.com',
            [email],
        )
        
        return render(request, "main/index.html", {"success_message": "Your message has been sent successfully!"})
    return render(request, "main/index.html")