from typing import List, Optional
from ninja import NinjaAPI
from tracks.models import Track
from tracks.schema import TrackSchema, NotFoundSchema

api = NinjaAPI()

@api.get("/tracks", response=List[TrackSchema])
def tracks(request, title: Optional[str]= None):
    if title:
        return Track.objects.filter(title__icontains=title)
    return Track.objects.all()

@api.get("/tracks/{track_id}", response={200: TrackSchema, 404: NotFoundSchema}, tags=["tracks"])
def track(request, track_id: int):
    try:
        return 200, Track.objects.get(id=track_id)
    except Track.DoesNotExist:
        return 404, {"message": f"Track {track_id} not found"}

@api.post("/tracks", response={201: TrackSchema})
def create_track(request, track: TrackSchema):
    return Track.objects.create(**track.dict())

@api.put("/tracks/{track_id}", response=TrackSchema)
def update_track(request, track_id: int, track: TrackSchema):
    track = Track.objects.get(id=track_id)
    for attr, value in track.dict().items():
        setattr(track, attr, value)
    track.save()
    return track

@api.delete("/tracks/{track_id}")
def delete_track(request, track_id: int):
    track = Track.objects.get(id=track_id)
    track.delete()
    return 204

@api.exception_handler(Track.DoesNotExist)
def not_found(request, exc):
    return 404, {"message": f"Track not found"}

