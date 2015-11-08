from django.http.response import HttpResponseForbidden

from .models import Question


def owner_required(dispatch):
    def decorated(request, *args, **kwargs):
        owner = Question.objects.get(pk=kwargs['pk']).owner
        if request.user != owner:
            return HttpResponseForbidden()
        return dispatch(request, *args, **kwargs)
    return decorated
