from .views import ChoiceListByPollGeneric, ChoiceListGeneric, CreateVoteGeneric, PollDetail, PollDetailGeneric, PollList, PollListGeneric, polls_detail, polls_list
from django.urls import include, path

urlpatterns = [
    path("pure-django/polls/", polls_list, name="pure-django_polls_list"),
    path("pure-django/polls/<int:pk>/", polls_detail,
         name="pure-django_polls_detail"),
    path("apiview/polls/", PollList.as_view(), name="apiview_polls_list"),
    path("apiview/polls/<int:pk>/", PollDetail.as_view(),
         name="apiview_polls_detail"),
    path("genericviews/polls/", PollListGeneric.as_view(),
         name="genericviews_polls_list"),
    path("genericviews/polls/<int:pk>/", PollDetailGeneric.as_view(),
         name="genericviews_polls_detail"),
    path("genericviews/choices/", ChoiceListGeneric.as_view(),
         name="genericviews_choices_list"),
    path("genericviews/choices/<int:poll_id>", ChoiceListByPollGeneric.as_view(),
         name="genericviews_choices_list_by_poll"),
    path("genericviews/vote/", CreateVoteGeneric.as_view(),
         name="genericviews_vote"),
]
