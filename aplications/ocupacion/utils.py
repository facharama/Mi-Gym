# aplications/ocupacion/utils.py
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from .models import ActiveSession

def get_current_occupancy():
    return ActiveSession.objects.filter(status="ACTIVE").count()

#def publish_occupancy_update():
#   channel_layer = get_channel_layer()
#   payload = {
#       "type": "occupancy.message",
#       "count": get_current_occupancy(),
#       "ts": None
#   }
#   async_to_sync(channel_layer.group_send)("occupancy", {"type":"occupancy.message", "payload":payload})


def publish_occupancy_update():
    # Placeholder sin channels
    print(f"[DEBUG] Ocupación actual: {get_current_occupancy()} socios")
