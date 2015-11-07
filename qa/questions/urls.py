from django.conf.urls import url

from . import views

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

    url(r'^(?P<pk>[0-9]+)/(?P<slug>[-\w]+)$',
        views.QuestionDetailView.as_view(),
        name='details',
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
