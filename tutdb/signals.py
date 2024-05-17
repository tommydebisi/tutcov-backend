from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserResponse

@receiver(post_save, sender=UserResponse)
def check_selected_choice(sender, instance, created, **kwargs):
    if created:
        selected_choice = instance.selected_choice
        if selected_choice == instance.question.answer:
            instance.is_correct = True
        else:
            instance.is_correct = False
        instance.save()
