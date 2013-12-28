from actstream import action

def generate_action(actor, verb, action_object=None, target=None, *args, **kwargs):
    action.send(actor, verb=verb, action_object=action_object, target=target, *args, **kwargs)