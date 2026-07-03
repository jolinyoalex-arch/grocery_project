from decimal import Decimal

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Order, OrderItem, Product, User, VerificationCode


def _get_cart(request):
    return request.session.get('cart', {})


def _save_cart(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def home_view(request):
    products = Product.objects.all().select_related('vendor', 'category')
    return render(request, 'home.html', {'products': products})


def compare_prices_view(request):
    products = Product.objects.all().select_related('vendor', 'category').order_by('price')
    return render(request, 'compare_prices.html', {'products': products})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Welcome back!')
            return redirect('home')
        messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        if not username or not email or not password1 or not password2:
            messages.error(request, 'Please fill in all fields.')
        elif password1 != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            # Create user with inactive status (until email is verified)
            user = User.objects.create_user(username=username, email=email, password=password1, is_active=True)
            
            # Generate and save verification code
            verification_code = VerificationCode.create_code_for_user(user)
            
            # Send verification email
            try:
                subject = 'Email Verification Code'
                message = f'''
Hello {username},

Thank you for registering with us!

Your email verification code is:

    {verification_code.code}

This code will expire in 10 minutes.

If you did not create this account, please ignore this email.

Best regards,
Grocery Store Team
                '''
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, f'Verification code sent to {email}. Please check your inbox.')
                # Store user id in session for verification
                request.session['pending_verification_user_id'] = user.id
                return redirect('verify_email')
            except Exception as e:
                user.delete()  # Delete the user if email fails
                messages.error(request, f'Failed to send verification email. Please try again. Error: {str(e)}')

    return render(request, 'register.html')


def verify_email_view(request):
    """Verify user email with verification code"""
    user_id = request.session.get('pending_verification_user_id')
    
    if not user_id:
        messages.error(request, 'No pending verification found. Please register first.')
        return redirect('register')
    
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        messages.error(request, 'User not found.')
        return redirect('register')
    
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        
        try:
            verification_code = VerificationCode.objects.get(user=user)
            
            if not verification_code.is_valid():
                messages.error(request, 'Verification code has expired. Please register again.')
                user.delete()
                del request.session['pending_verification_user_id']
                return redirect('register')
            
            if verification_code.code != code:
                messages.error(request, 'Invalid verification code.')
                return render(request, 'verify_email.html', {'email': user.email})
            
            # Mark email as verified
            user.is_email_verified = True
            user.save()
            verification_code.is_used = True
            verification_code.save()
            
            # Clear session and log in user
            del request.session['pending_verification_user_id']
            login(request, user)
            messages.success(request, 'Email verified successfully! Welcome to Grocery Store!')
            return redirect('home')
            
        except VerificationCode.DoesNotExist:
            messages.error(request, 'Verification code not found.')
            return redirect('register')
    
    return render(request, 'verify_email.html', {'email': user.email})


def resend_verification_code_view(request):
    """Resend verification code to user email"""
    user_id = request.session.get('pending_verification_user_id')
    
    if not user_id:
        messages.error(request, 'No pending verification found.')
        return redirect('register')
    
    try:
        user = User.objects.get(id=user_id)
        
        # Create new verification code
        verification_code = VerificationCode.create_code_for_user(user)
        
        # Send email
        subject = 'Email Verification Code (Resent)'
        message = f'''
Hello {user.username},

Your new email verification code is:

    {verification_code.code}

This code will expire in 10 minutes.

Best regards,
Grocery Store Team
        '''
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        messages.success(request, f'New verification code sent to {user.email}.')
        return redirect('verify_email')
        
    except Exception as e:
        messages.error(request, f'Failed to resend code. Please try again. Error: {str(e)}')
        return redirect('verify_email')


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def add_to_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    cart[str(product.id)] = cart.get(str(product.id), 0) + 1
    _save_cart(request, cart)
    messages.success(request, f'{product.name} added to cart.')
    return redirect('home')


@login_required
def cart_view(request):
    cart = _get_cart(request)
    product_ids = [int(product_id) for product_id in cart.keys()]
    products = Product.objects.filter(id__in=product_ids).select_related('vendor', 'category')
    items = []
    total = Decimal('0.00')

    for product in products:
        quantity = cart.get(str(product.id), 0)
        if quantity:
            line_total = Decimal(str(product.price)) * quantity
            total += line_total
            items.append({'product': product, 'quantity': quantity, 'line_total': line_total})

    return render(request, 'cart.html', {'items': items, 'total': total})


@login_required
def update_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    quantity = int(request.POST.get('quantity', 1) or 1)

    if quantity <= 0:
        cart.pop(str(product.id), None)
    else:
        cart[str(product.id)] = quantity

    _save_cart(request, cart)
    messages.success(request, f'{product.name} updated in cart.')
    return redirect('cart')


@login_required
def remove_from_cart_view(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = _get_cart(request)
    cart.pop(str(product.id), None)
    _save_cart(request, cart)
    messages.success(request, f'{product.name} removed from cart.')
    return redirect('cart')


@login_required
def checkout_view(request):
    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address', '').strip() or 'Address not provided'
        cart = _get_cart(request)
        if not cart:
            messages.error(request, 'Your cart is empty.')
            return redirect('cart')

        order = Order.objects.create(customer=request.user, delivery_address=delivery_address, total_price=Decimal('0.00'))
        total = Decimal('0.00')

        for product_id, quantity in cart.items():
            product = get_object_or_404(Product, id=product_id)
            line_total = Decimal(str(product.price)) * int(quantity)
            total += line_total
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_purchase=product.price,
            )

        order.total_price = total
        order.save(update_fields=['total_price'])
        request.session['cart'] = {}
        request.session.modified = True
        messages.success(request, 'Order placed successfully.')
        return redirect('orders')

    return render(request, 'checkout.html')


@login_required
def orders_view(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})