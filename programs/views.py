from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response

from programs.models import Program
from programs.serializers import ProgramSerializer
from .permissions import IsConsumerOrReadOnly


class ProgramViewSet(ModelViewSet):
    queryset = Program.objects.order_by('-created_at')
    serializer_class = ProgramSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly, IsConsumerOrReadOnly]
    permission_classes = [AllowAny,]  # AllowAny

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=('POST', 'DELETE'))
    def subscribe(self, request, *args, **kwargs):
        program = self.get_object()

        if request.method == 'POST':
            program.subscriber.add(request.user)
        elif request.method == 'DELETE':
            program.subscriber.remove(request.user)

        return Response(self.serializer_class(program).data)
