from django.http import JsonResponse, request
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from rest_framework import serializers, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Choice, Poll
from .serializers import ChoiceSerializer, PollSerializer


# example of getting the data in json representation using pure Django
# use the following url to test it: pure-django/polls/
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


# example of working with data using APIView from django rest framework
# use the following url to test it: apiview/polls/
class PollList(APIView):
    """
    Example using APIView class
    returns polls or add a new one
    """

    def get(self, request):
        polls = Poll.objects.all()[:20]
        data = PollSerializer(polls, many=True).data
        return Response(data)

    def post(self, request):
        # breakpoint()
        serializer = PollSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PollDetail(APIView):
    """
    Example using APIView class
    returns a specific poll by id
    """

    def get(self, request, pk):
        poll = get_object_or_404(Poll, pk=pk)
        data = PollSerializer(poll).data
        return Response(data)


# Using of generic views of Django Rest Framework
class PollListGeneric(generics.ListCreateAPIView):
    """
    Example using generic view ListCreateAPIView class
    """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class PollDetailGeneric(generics.RetrieveDestroyAPIView):
    """
    Example using generic view RetrieveDestroyAPIView class
    """
    queryset = Poll.objects.all()
    serializer_class = PollSerializer


class ChoiceListGeneric(generics.ListCreateAPIView):
    """
    returns all available choices
    """
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


class ChoiceListByPollGeneric(generics.ListAPIView):
    """
    returns all available choices by poll id.
    """
    serializer_class = ChoiceSerializer
    lookup_url_kwarg = "poll_id"

    def get_queryset(self):
        """
        parses and get form the url the poll id
        filters the queryset by poll id
        """
        poll_id = self.kwargs.get(self.lookup_url_kwarg)
        queryset = Choice.objects.filter(poll=poll_id)
        return queryset


class CreateVoteGeneric(generics.CreateAPIView):
    serializer_class = ChoiceSerializer
