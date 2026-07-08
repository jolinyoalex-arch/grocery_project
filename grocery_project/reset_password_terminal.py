import os
import django
import getpass

# 1. Sanifisha settings za mradi wako wa grocery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'grocery.settings')
django.setup()

# 2. Sasa ingiza get_user_model BAADA ya django kuwa tayari
from django.contrib.auth import get_user_model

def reset_admin_password():
    User = get_user_model()
    username = 'admin'
    
    user = User.objects.filter(username=username).first()
    
    if not user:
        print(f"\n❌ Error: Admin mwenye username '{username}' hajapatikana!")
        return

    print(f"\n--- 🔐 RESET PASSWORD YA '{username}' ---")
    password = getpass.getpass("Ingiza Password Mpya: ")
    confirm_password = getpass.getpass("Rudia Password Mpya: ")
    
    if password == confirm_password:
        if len(password) < 8:
            print("❌ Error: Password lazima iwe na herufi 8 au zaidi!")
            return
        user.set_password(password)
        user.save()
        print(f"\n✅ Success: Password ya admin '{username}' imebadilishwa kikamilifu!")
    else:
        print("\n❌ Error: Password hazifanani!")

if __name__ == '__main__':
    reset_admin_password()

