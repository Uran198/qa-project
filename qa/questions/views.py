# from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView, DetailView, DeleteView
from django.views.generic import ListView
from django.core.urlresolvers import reverse_lazy

from .models import Question, Answer
from .forms import AnswerForm


class QuestionListView(ListView):
    model = Question


class QuestionCreateView(CreateView):
    model = Question
    fields = ("title", "details")


class QuestionUpdateView(UpdateView):
    model = Question
    template_name_suffix = '_update_form'
    fields = ("title", "details")


class QuestionDeleteView(DeleteView):
    model = Question
    success_url = reverse_lazy('questions:list')


class QuestionDetailView(DetailView):
    model = Question

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        context['answers'] = self.object.answer_set.all()
        context['answer_form'] = AnswerForm()
        return context

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


# Create your views here.
