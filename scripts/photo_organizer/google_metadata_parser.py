#!/usr/bin/env python3
"""
Google Photos Metadata Parser
Parses JSON metadata files from Google Photos Takeout
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List


class GoogleMetadataParser:
    """Parse Google Photos Takeout JSON metadata"""

    def __init__(self):
        pass

    def parse_json_metadata(self, json_path: str) -> Optional[Dict]:
        """
        Parse Google Photos JSON metadata file

        Returns dictionary with:
        - datetime: Photo taken time
        - creation_time: Upload time
        - gps: GPS coordinates (if available)
        - people: List of people in photo
        - description: Photo description
        - title: Original title
        """
        if not os.path.exists(json_path):
            return None

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            metadata = {
                'datetime': None,
                'creation_time': None,
                'gps': None,
                'people': [],
                'description': '',
                'title': '',
                'url': '',
            }

            # Extract title
            if 'title' in data:
                metadata['title'] = data['title']

            # Extract description
            if 'description' in data:
                metadata['description'] = data['description']

            # Extract photo taken time (most important!)
            if 'photoTakenTime' in data and 'timestamp' in data['photoTakenTime']:
                try:
                    timestamp = int(data['photoTakenTime']['timestamp'])
                    metadata['datetime'] = datetime.fromtimestamp(timestamp)
                except (ValueError, OSError):
                    pass

            # Fallback to creation time
            if not metadata['datetime'] and 'creationTime' in data:
                if 'timestamp' in data['creationTime']:
                    try:
                        timestamp = int(data['creationTime']['timestamp'])
                        metadata['creation_time'] = datetime.fromtimestamp(timestamp)
                        # Use as datetime if photo taken time not available
                        if not metadata['datetime']:
                            metadata['datetime'] = metadata['creation_time']
                    except (ValueError, OSError):
                        pass

            # Extract GPS data
            if 'geoData' in data:
                geo = data['geoData']
                lat = geo.get('latitude', 0.0)
                lon = geo.get('longitude', 0.0)
                # Only keep if not zero
                if lat != 0.0 or lon != 0.0:
                    metadata['gps'] = {
                        'latitude': lat,
                        'longitude': lon,
                        'altitude': geo.get('altitude', 0.0)
                    }

            # Also check geoDataExif
            if not metadata['gps'] and 'geoDataExif' in data:
                geo = data['geoDataExif']
                lat = geo.get('latitude', 0.0)
                lon = geo.get('longitude', 0.0)
                if lat != 0.0 or lon != 0.0:
                    metadata['gps'] = {
                        'latitude': lat,
                        'longitude': lon,
                        'altitude': geo.get('altitude', 0.0)
                    }

            # Extract people (privacy sensitive!)
            if 'people' in data and isinstance(data['people'], list):
                for person in data['people']:
                    if 'name' in person:
                        metadata['people'].append(person['name'])

            # Extract URL
            if 'url' in data:
                metadata['url'] = data['url']

            return metadata

        except Exception as e:
            print(f"Error parsing JSON {json_path}: {e}")
            return None

    def find_json_for_media(self, media_path: str) -> Optional[str]:
        """
        Find corresponding JSON file for a media file

        Google Photos Takeout uses pattern:
        - photo.jpg -> photo.jpg.json
        - video.mp4 -> video.mp4.json
        """
        json_path = f"{media_path}.json"
        if os.path.exists(json_path):
            return json_path

        # Some files might have different patterns
        # Try without extension first
        base = os.path.splitext(media_path)[0]
        json_path = f"{base}.json"
        if os.path.exists(json_path):
            return json_path

        return None

    def extract_datetime_from_metadata(self, media_path: str) -> Optional[datetime]:
        """
        Extract datetime from JSON metadata if available
        Returns None if no metadata found
        """
        json_path = self.find_json_for_media(media_path)
        if not json_path:
            return None

        metadata = self.parse_json_metadata(json_path)
        if metadata and metadata['datetime']:
            return metadata['datetime']

        return None


# Testing function
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        json_file = "/media/goqual/T7 Shield/takeout-extracted/BandPhoto_2014_11_05_20_06_24.jpg.json"

    parser = GoogleMetadataParser()

    if os.path.exists(json_file):
        metadata = parser.parse_json_metadata(json_file)
        if metadata:
            print("Parsed Metadata:")
            print(f"  Title: {metadata['title']}")
            print(f"  Datetime: {metadata['datetime']}")
            print(f"  GPS: {metadata['gps']}")
            print(f"  People: {metadata['people']}")
            print(f"  Description: {metadata['description']}")
    else:
        print(f"File not found: {json_file}")
