from rest_framework.permissions import BasePermission


class IsCreator(BasePermission):
    '''
    ## Access to creator to edit
      only the creator of the **Model Name** can edit it
    '''
    message = 'only the creator of the question can edit it'

    def has_object_permission(self, request, view, obj):
        self.message = f'only the creator of the {obj.__class__.__name__} can edit it'
        return request.user == obj.creator