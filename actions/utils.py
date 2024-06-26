from .models import Action
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType

def create_action(user, verb, target=None):
    
    # Check for any similar action made in the last minute
    # to avoid duplicate actions
    now = timezone.now()
    last_minute = now - timezone.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id,
                                            verb=verb,
                                            created__gte=last_minute)
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,
                                                target_id=target.id)
    
    if not similar_actions:
        # no existing actions found
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True
    return False