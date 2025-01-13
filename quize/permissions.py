from rest_framework.permissions import BasePermission
from django.utils import timezone


class IsCreator(BasePermission):
    """
    ## Access to creator to edit
      only the creator of the **Model Name** can edit it
    """

    message = "only the creator of the question can edit it"
    def has_object_permission(self, request, view, obj):
        self.message = f"only the creator of the {obj.__class__.__name__} can edit it"
        return request.user == obj.creator


class IsParticipant(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            if obj.quiz.end_at > timezone.now():
                self.message = 'quiz not ended.'
                return False
            return True
        else:
            return False
