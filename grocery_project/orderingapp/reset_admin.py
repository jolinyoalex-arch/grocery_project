def reset():
    User = get_user_model()
    username = 'john'
    password = 'jolinyo001' # Hii ndio itakuwa password yako mpya
    email = 'john@gmail.com'

    user = User.objects.filter(username=username).first()
    if user:
        user.set_password(password)
        user.save()
        print(f"✅ SUCCESS: Password ya admin '{username}' imebadilishwa kikamilifu kule Render!")
    else:
        User.objects.create_superuser(username=username, email=email, password=password)
        print(f"✅ SUCCESS: Admin mpya '{username}' ametengenezwa kikamilifu kule Render!")