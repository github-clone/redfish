# cookbook/ingredients/schema.py
import graphene
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from graphql_relay.node.node import from_global_id

from .models import Note
from django.contrib.auth.models import User


# Graphene will automatically map the Category model's fields onto the CategoryNode.
# This is configured in the CategoryNode's Meta class (as you can see below)
class NoteNode(DjangoObjectType):
    class Meta:
        model = Note
        filter_fields = ['title', 'content', 'color', 'pinned']
        interfaces = (relay.Node, )

    @classmethod
    def get_node(cls, info, id):
        # get object by provided id
        try:
            note = cls._meta.model.objects.get(id=id)
        except cls._meta.model.DoesNotExist:
            return None
        # check the ownership
        if info.context.user == note.owner:
            return note
        # different owner. Not allowed
        return None

class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ['username']
        exclude_fields = ('password', 'is_superuser', 'is_staff',)
        interfaces = (relay.Node, )


class Query(object):
    note = relay.Node.Field(NoteNode)
    all_notes = DjangoFilterConnectionField(NoteNode)
    profile = DjangoFilterConnectionField(UserNode)

    def resolve_all_notes(self, info, **kwargs):
        # context will reference to the Django request
        if not info.context.user.is_authenticated:
            return Note.objects.none()
        else:
            return Note.objects.filter(owner=info.context.user)

    def resolve_profile(self, info):
        if info.context.user.is_authenticated:
            return User.objects.filter(username=info.context.user)


class AddNote(relay.ClientIDMutation):

    class Input:
        title = graphene.String(required=False)
        content = graphene.String(required=False)

    new_note = graphene.Field(NoteNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        if not info.context.user.is_authenticated:
            return None
        note = Note.objects.create(owner=info.context.user, **input)
        return AddNote(new_note=note)

class DeleteNotes(relay.ClientIDMutation):
    class Input:
        ids = graphene.List(graphene.ID, required=True)

    deleted_notes = graphene.List(NoteNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, **input):
        local_ids = [from_global_id(i)[1] for i in input['ids']]
        try:
            notes = Note.objects.filter(id__in=local_ids, owner=info.context.user)
        except Note.DoesNotExist:
            return None
        snapshot = list(notes)
        notes.delete()
        return DeleteNotes(snapshot)


class Mutation(ObjectType):
    add_note = AddNote.Field()
    delete_notes = DeleteNotes.Field()
