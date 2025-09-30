from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from django.db import transaction
from aplications.socios.models import Socio
from .models import AccessEvent, ActiveSession

# simple header token for device authentication
DEVICE_TOKENS = {"kiosk-1":"secret-token-123"}  # en prod: DB + rotate

def authenticate_device(request):
    token = request.headers.get("X-Device-Token")
    return token in DEVICE_TOKENS.values()

class CheckInOutAPIView(APIView):
    permission_classes = [permissions.AllowAny]  # device uses token header

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """
        body: { "member_code": "SOC123", "type":"IN"|"OUT", "source":"RFID", "raw_uid":"04A1B2C3", "device_id":"kiosk-1" }
        """
        if not authenticate_device(request):
            return Response({"detail":"invalid device token"}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        member_code = data.get("member_code")
        try:
            socio = Socio.objects.get(code=member_code)
        except Socio.DoesNotExist:
            return Response({"detail":"member not found"}, status=status.HTTP_404_NOT_FOUND)

        atype = data.get("type")
        source = data.get("source")
        device_id = data.get("device_id")
        raw_uid = data.get("raw_uid")

        # register event
        AccessEvent.objects.create(member=socio, type=atype, source=source, device_id=device_id, raw_uid=raw_uid)

        # business rules:
        now = timezone.now()
        if atype == "IN":
            session, created = ActiveSession.objects.get_or_create(member=socio, defaults={"check_in_at": now})
            if not created and session.status == "ACTIVE":
                # duplicate IN -> ignore or log
                return Response({"status":"already_active"}, status=status.HTTP_200_OK)
            session.status = "ACTIVE"
            session.check_in_at = now
            session.check_out_at = None
            session.save()
        else:  # OUT
            try:
                session = ActiveSession.objects.get(member=socio, status="ACTIVE")
                session.check_out_at = now
                session.status = "CLOSED"
                session.save()
            except ActiveSession.DoesNotExist:
                # orphan OUT -> ignore or log
                return Response({"status":"no_active_session"}, status=status.HTTP_200_OK)

        # publish occupancy update (see function abajo)
        #publish_occupancy_update()

        return Response({"status":"ok"}, status=status.HTTP_200_OK)
