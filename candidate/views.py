from candidate.models import Candidate
from rest_framework.response import Response
from candidate.serializers import CandidateSerializer
from rest_framework import viewsets
from rest_framework import status
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank


class CandidateViewSet(viewsets.ModelViewSet):

    """
    ViewSet for managing candidates, supporting search, create, update, and delete operations.
    """

    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    http_method_names = ["get", "post", "put", "delete"]

    @staticmethod
    def _get_name_combinations(search_keywords):
        """
        Generate all possible name combinations (including partial matches) from the search keywords.
        """
        combinations = []
        combinations.append(" ".join(search_keywords))
        if len(search_keywords) > 1:
            for i in range(len(search_keywords)):
                partial_name = " ".join(search_keywords[:i] + search_keywords[i + 1 :])
                combinations.append(partial_name)
        return combinations

    def list(self, request):
        """
        Override the default 'list' method to support search functionality with relevance ranking.
        """
        search_query = request.query_params.get("search", None)
        if search_query:
            result = Candidate.objects.annotate(
                rank=SearchRank("vector_column", SearchQuery(search_query))
            ).values_list("name", flat=True)
            return Response({"result": result}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Please provide a search name."},
            status=status.HTTP_400_BAD_REQUEST,
        )
