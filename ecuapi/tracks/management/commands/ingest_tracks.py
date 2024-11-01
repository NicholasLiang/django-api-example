from datetime import datetime
import json
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils import timezone

from tracks.models import Track

class Command(BaseCommand):
    help = "Ingest tracks from a JSON file"

    def handle(self, *args, **kwargs):
        #set the path to the datafile
        datafile = settings.BASE_DIR / "data" / "tracks.json"
        assert datafile.exists(), f"File not found: {datafile}"

        #open the datafile
        with open(datafile, "r") as file:
            data = json.load(file)

        # create tz-aware datetime object from the JSON string
        DATE_FMT = "%Y-%m-%d %H:%M:%S"
        for track in data:
            track["last_play"] = timezone.make_aware(
                datetime.strptime(track["last_play"], DATE_FMT)
            )

            # convert list of dictionaries to list of Track instances
            tracks = [Track(**track) for track in data]

            # bulk create the Track instances
            Track.objects.bulk_create(tracks)
