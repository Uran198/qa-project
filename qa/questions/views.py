# from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Question, Answer
from .forms import AnswerForm
from .serializers import QuestionSerializer


class QuestionListView(ListView):
    model = Question


class QuestionCreateView(CreateView):
    model = Question
    fields = ("title", "details")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(QuestionCreateView, self).dispatch(*args, **kwargs)


class QuestionUpdateView(UpdateView):
    model = Question
    template_name_suffix = '_update_form'
    fields = ("title", "details")

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(QuestionUpdateView, self).dispatch(*args, **kwargs)


class QuestionDeleteView(DeleteView):
    model = Question
    success_url = reverse_lazy('questions:list')

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(QuestionDeleteView, self).dispatch(*args, **kwargs)


class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['answers'] = self.object.answer_set.all()
        context['answer_form'] = AnswerForm()
        return context

    @method_decorator(login_required)
    def post(self, request, pk, **kwargs):
        form = AnswerForm(request.POST)
        self.object = self.get_object()
        if form.is_valid():
            answer = Answer(text=form.cleaned_data['text'])
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


class QuestionRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
