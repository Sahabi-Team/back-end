from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Comment

from .utils import PersianSwearWordRemover

@receiver(pre_save, sender=Comment)
def auto_check_comment(sender, instance, **kwargs):
    if instance.comment:
        remover = PersianSwearWordRemover()
        flagged, _ = remover.contains_swear_word(instance.comment)
        instance.approved = not flagged