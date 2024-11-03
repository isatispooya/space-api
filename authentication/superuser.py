from django.contrib.auth import get_user_model

def create_superuser_if_not_exists(username, email, password, birth_date):
    User = get_user_model()
    
    # Check if the user already exists
    if User.objects.filter(username=username).exists():
        print('User already exists.')
        return

    # Validate birth_date input
    if not birth_date:
        print('Birth date cannot be empty.')
        return

    # Create the superuser
    user = User(username=username, email=email, birth_date=birth_date)
    user.set_password(password)
    user.is_superuser = True  # Set superuser flag
    user.is_staff = True  # Set staff flag
    user.save()
    print('-'*20)
    print(user)
    print('-'*20)
    print('Superuser created successfully.')

