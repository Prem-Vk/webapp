from candidate.models import Candidate
from rest_framework.response import Response
from candidate.serializers import CandidateSerialiazer, CandidateSearchSerializer
from rest_framework.decorators import api_view
from django.db.models import Q, Count
from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action


class CandidateViewSet(viewsets.ViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']

    def create(self, request):
        serializer = CandidateSerialiazer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            candidate = Candidate.objects.get(pk=pk)
        except Candidate.DoesNotExist:
            return Response({'detail': 'Candidate Does not exists!!'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CandidateSerialiazer(candidate, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            candidate = Candidate.objects.get(pk=pk)
        except Candidate.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        candidate.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def search(self, request):
        name = request.query_params.get('name', None)
        search_keywords = name.split()

        filters = Q()
        for word in search_keywords:
            filters |= Q(name__icontains=word)

        candidates = Candidate.objects.filter(filters)

        candidates = candidates.annotate(
            name_match_count = Count(
                'id',
                filter=Q(name__icontaines=search_keywords[0])
            )
        ).order_by('-name_match_count')

        serializer = CandidateSearchSerializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
