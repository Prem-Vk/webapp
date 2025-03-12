from candidate.models import Candidate
from rest_framework.response import Response
from candidate.serializers import CandidateSerialiazer
from rest_framework import viewsets
from rest_framework import status
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


class CandidateViewSet(viewsets.ModelViewSet):
    #  We are using model view set for create, update and delete functions.
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerialiazer
    http_method_names = ['get', 'post', 'put', 'delete']

    #  Modifed list method to show relevance response based on search name.
    def list(self, request):
        search_by = request.query_params.get('search', None)
        if search_by:
            search_keywords = search_by.split()
            combinations = []
            combinations.append(' '.join(search_keywords))
            if len(search_by) > 1:
                for i in range(len(search_keywords)):
                    partial_name = ' '.join(search_keywords[:i] + search_keywords[i+1:])
                    combinations.append(partial_name)

            #  We are using postgres full text search here for getting search reponse in relevance:
            #  Ref:- https://pganalyze.com/blog/full-text-search-django-postgres
            results = Candidate.objects.none()
            for combo in combinations:
                search_query = SearchQuery(combo)
                search_vector = SearchVector('name')
                partial_results = Candidate.objects.annotate(
                    rank=SearchRank(search_vector, search_query)
                ).filter(rank__gt=0).order_by('-rank').values_list('name', flat=True)
                results |= partial_results
            return Response({'result':results}, status=status.HTTP_200_OK)
        return Response({'error': 'Please provide a search name.'}, status=status.HTTP_400_BAD_REQUEST)
