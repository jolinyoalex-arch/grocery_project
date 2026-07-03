#!/bin/bash
# Quick Setup Script for Email Verification Testing

echo "🚀 Setting up Email Verification..."
echo ""

# Navigate to project
cd /home/john/Desktop/grocery_project/grocery_project || exit

# Check if migrations are applied
echo "✅ Running migrations..."
python manage.py migrate --noinput

# Create superuser if doesn't exist
echo ""
echo "📝 Creating superuser (optional)..."
echo "   You can skip this if you already have a superuser"
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print("Creating superuser...")
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("✅ Superuser created!")
    print("   Username: admin")
    print("   Email: admin@example.com")
    print("   Password: admin")
else:
    print("✅ Superuser already exists")
END

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Start the development server:"
echo "   python manage.py runserver"
echo ""
echo "2. Go to http://localhost:8000/register/"
echo ""
echo "3. Fill in the registration form"
echo ""
echo "4. Check your TERMINAL for the verification code"
echo "   (It will print there, not in the browser)"
echo ""
echo "5. Enter the code on the verification page"
echo ""
echo "6. You'll be logged in!"
echo ""
echo "💡 For real emails with Gmail:"
echo "   1. Update EMAIL_HOST_USER and EMAIL_HOST_PASSWORD in .env"
echo "   2. See EMAIL_VERIFICATION_SETUP.md for instructions"
echo ""
echo "Admin panel: http://localhost:8000/admin/"
echo "Use credentials: admin / admin"
