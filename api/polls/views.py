from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Poll
from django.http import request, JsonResponse


def polls_list(request):
    MAX_OBJECTS = 20
    polls = Poll.objects.all()[:MAX_OBJECTS]
    polls_list = list(polls.values(
        "question", "created_by__username", "pub_date"))
    data = {
        "results": polls_list
    }

    return JsonResponse(data)


def polls_detail(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    data = {
        "results": {
            "question": poll.question,
            "created_by": poll.created_by.username,
            "pub_date": poll.pub_date
        }
    }

    return JsonResponse(data)
