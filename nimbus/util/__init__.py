from actstream import action

def generate_action(actor, verb, action_object=None, target=None):
    action.send(actor, verb=verb, action_object=action_object, target=target)