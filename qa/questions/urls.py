from django.conf.urls import url

from . import views
from . import models

urlpatterns = [
    url(r'^create/$',
        views.QuestionCreateView.as_view(),
        name='create',
        ),

    url(r'^$',
        views.QuestionListView.as_view(),
        name='list',
        ),

    url(r'^(?P<pk>[0-9]+)/update/$',
        views.QuestionUpdateView.as_view(),
        name='update',
        ),

    url(r'^(?P<pk>[0-9]+)/delete/$',
        views.QuestionDeleteView.as_view(),
        name='delete',
        ),

    url(r'^(?P<pk>[0-9]+)/(?P<slug>[-\w]*)/$',
        views.QuestionDetailView.as_view(),
        name='details',
        ),

    url(r'^comments/(?P<parent_pk>[0-9]+)/create/$',
        views.CommentCreateView.as_view(parent_model=models.Question),
        name='add_question_comment'
        ),

    url(r'^comments/answers/(?P<parent_pk>[0-9]+)/create/$',
        views.CommentCreateView.as_view(parent_model=models.Answer),
        name='add_answer_comment'
        ),

    url(r'^comments/delete/(?P<pk>[0-9]+)/$',
        views.CommentDeleteView.as_view(),
        name='delete_comment'
        ),

    url(r'^comments/update/(?P<pk>[0-9]+)/$',
        views.CommentUpdateView.as_view(),
        name='update_comment'
        ),

    url(r'^api/$',
        views.QuestionListCreateAPIView.as_view(),
        name='api'
        ),

    url(r'^api/(?P<pk>[0-9]+)$',
        views.QuestionRetrieveUpdateDestroyAPIView.as_view(),
        name='api'
        ),
]
