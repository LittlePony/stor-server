from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import DriveSerializer, PartitionSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Drive, StorError
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST


class DriveViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        drives = Drive.get_all()
        serializer = DriveSerializer(drives, many=True)
        return Response(serializer.data)

    @action(methods=['post'], detail=True)
    def unmount(self, request, pk=None):
        try:
            drive = Drive.umount(pk)
            serializer = PartitionSerializer(drive)
            return Response(serializer.data)
        except StorError as exc:
            return Response({'detail': str(exc)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=True)
    def mount(self, request, pk=None):
        try:
            mountpoint = request.data['mountpoint']
            drive = Drive.mount(pk, mountpoint)
            serializer = PartitionSerializer(drive)
            return Response(serializer.data)
        except KeyError:
            return Response({'detail': 'Wrong request'}, status=HTTP_400_BAD_REQUEST)
        except StorError as exc:
            return Response({'detail': str(exc)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=True)
    def format(self, request, pk=None):
        Drive.format(pk)
        return Response({'detail': 'ok'})
