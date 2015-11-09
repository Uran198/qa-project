# from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.views.generic import ListView
# from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError

from .models import Question, Answer, Comment
from .forms import AnswerForm
from .serializers import QuestionSerializer
from .decorators import owner_required


class QuestionListView(ListView):
    model = Question


class QuestionCreateView(CreateView):
    model = Question
    fields = ("title", "details")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(QuestionCreateView, self).form_valid(form)

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(QuestionCreateView, self).dispatch(*args, **kwargs)


class QuestionUpdateView(UpdateView):
    model = Question
    template_name_suffix = '_update_form'
    fields = ("title", "details")

    @method_decorator(login_required)
    @owner_required
    def dispatch(self, *args, **kwargs):
        return super(QuestionUpdateView, self).dispatch(*args, **kwargs)


class QuestionDeleteView(DeleteView):
    model = Question
    success_url = reverse_lazy('questions:list')

    @method_decorator(login_required)
    @owner_required
    def dispatch(self, *args, **kwargs):
        return super(QuestionDeleteView, self).dispatch(*args, **kwargs)


class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        # for better performance need equivalent of select_relative
        # for answer comments
        context['answers'] = self.object.answer_set.all()
        context['comments'] = self.object.comments.all()
        context['answer_form'] = AnswerForm()
        return context

    @method_decorator(login_required)
    def post(self, request, pk, **kwargs):
        form = AnswerForm(request.POST)
        self.object = self.get_object()
        if form.is_valid():
            answer = Answer(text=form.cleaned_data['text'])
            answer.owner = request.user
            answer.question = self.object
            answer.save()
            return redirect(answer.question)
        context = self.get_context_data()
        context['answer_form'] = form
        return self.render_to_response(context)


class QuestionListCreateAPIView(ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class QuestionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_update(self, serializer):
        instance = serializer.instance
        if instance.owner != self.request.user:
            raise ValidationError("You can update only your own questions")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise ValidationError("You can destroy only your own questions")
        return super(QuestionRetrieveUpdateDestroyAPIView,
                     self).perform_destroy(instance)


class CommentCreateView(CreateView):
    model = Comment
    fields = ('text',)
    http_method_names = [u'post']
    parent_model = None

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class(request.POST)
        parent_pk = kwargs['parent_pk']
        parent_instance = self.parent_model.objects.get(pk=parent_pk)
        if not parent_instance:
            raise ValidationError("Parent is invalid")
        if form.is_valid():
            form.instance.content_object = parent_instance
            form.instance.owner = request.user
            form.save()
        referer = request.META.get('HTTP_REFERER')
        if referer:
            return redirect(referer)
        return redirect(parent_instance)


class CommentUpdateView(UpdateView):
    model = Comment
    fields = ('text',)
    http_method_names = [u'post']

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()

    @method_decorator(login_required)
    @owner_required
    def dispatch(self, *args, **kwargs):
        return super(CommentUpdateView, self).dispatch(*args, **kwargs)


class CommentDeleteView(DeleteView):
    model = Comment
    http_method_names = [u'post']

    def get_success_url(self):
        return self.object.content_object.get_absolute_url()

    @method_decorator(login_required)
    @owner_required
    def dispatch(self, *args, **kwargs):
        return super(CommentDeleteView, self).dispatch(*args, **kwargs)
