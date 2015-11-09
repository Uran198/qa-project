from django.http.response import HttpResponseForbidden


def owner_required(dispatch):
    def decorated(self, request, *args, **kwargs):
        owner = self.model.objects.get(pk=kwargs['pk']).owner
        if request.user != owner:
            return HttpResponseForbidden()
        return dispatch(self, request, *args, **kwargs)
    return decorated
