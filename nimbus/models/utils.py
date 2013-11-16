from django.contrib.contenttypes import generic

from actstream.models import Action

def actstream_register_model(model):
    """
    Set up GenericRelations for a given actionable model.
    Needed because actstream's generic relationship setup
    functionality is brittle and unreliable.
    """
    for field in ('actor', 'target', 'action_object'):
        generic.GenericRelation(Action,
                                content_type_field='%s_content_type' % field,
                                object_id_field='%s_object_id' % field,
                                related_name='actions_with_%s_%s_as_%s' % (
                                    model._meta.app_label, model._meta.module_name, field),
                            ).contribute_to_class(model, '%s_actions' % field)

        setattr(Action, 'actions_with_%s_%s_as_%s' % (model._meta.app_label, model._meta.module_name, field), None)