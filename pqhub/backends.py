from django.contrib.auth.backends import ModelBackend
from tutdb.models import User

class CustomUserModelBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        # Try to find a user matching the email (instead of email)
        users = User.objects.filter(email=email)

        if not users.exists():
            print("User does not exist")
            return None
        
        user = users.first()
        
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
