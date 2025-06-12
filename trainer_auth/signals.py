from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Comment
from .utils import remover 

@receiver(pre_save, sender=Comment)
def auto_check_comment(sender, instance, **kwargs):
    if instance.comment:
        # print("dbg:>>> ",remover.contains_swear_word(instance.comment))
        if remover.contains_swear_word(instance.comment):
            instance.approved = False
        else:
            instance.approved = True