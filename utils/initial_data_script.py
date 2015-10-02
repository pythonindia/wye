from django.contrib.auth.models import User
u = User(username='user1',
         email='user1@user1.com')
u.set_password('user1')
u.is_staff = True
u.is_superuser = True
u.is_active = True
u.save()
