#!/usr/bin/env python3
"""
Google Photos Organizer - Google Takeout Processor
Organizes photos/videos from Google Photos Takeout using Denote naming convention
This is a universal tool for all Google Photos Takeout users
"""

import os
import sys
import json
import shutil
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from collections import defaultdict
import argparse

# Import our modules
from denote_namer import DenoteNamer
from duplicate_checker import DuplicateChecker
from google_metadata_parser import GoogleMetadataParser


class GooglePhotosOrganizer:
    """Main organizer for processing Google Photos Takeout"""

    def __init__(self, source_dir: str, target_dir: str, dry_run: bool = False):
        """
        Initialize the organizer

        Args:
            source_dir: Google Takeout extracted directory or ZIP file
            target_dir: Target directory for organized files
            dry_run: If True, don't actually move files
        """
        self.source_dir = Path(source_dir)
        self.target_dir = Path(target_dir)
        self.dry_run = dry_run

        # Initialize modules
        self.namer = DenoteNamer()
        self.duplicate_checker = DuplicateChecker(
            cache_file=str(self.target_dir / "logs" / "duplicate_cache.json")
        )
        self.metadata_parser = GoogleMetadataParser()

        # Setup logging
        self.setup_logging()

        # Statistics
        self.stats = {
            'total_files': 0,
            'processed': 0,
            'duplicates': 0,
            'errors': 0,
            'json_parsed': 0,
            'json_missing': 0,
            'by_type': defaultdict(int),
            'by_year': defaultdict(int),
            'by_source': defaultdict(int),
            'size_saved': 0,
            'gps_found': 0,
            'people_found': 0
        }

    def setup_logging(self):
        """Setup logging configuration"""
        log_dir = self.target_dir / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)

        log_file = log_dir / f"google_organize_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )

        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Starting Google Photos organization from {self.source_dir} to {self.target_dir}")

    def find_takeout_root(self) -> Optional[Path]:
        """
        Find the Takeout/Google 포토 or google-photos directory

        Google Takeout structure:
        - Takeout/Google 포토/Photos from YYYY/
        - Takeout/google-photos/photos-YYYY/ (renamed)
        """
        # Check renamed folder first
        if (self.source_dir / "google-photos").exists():
            return self.source_dir / "google-photos"

        if (self.source_dir / "Takeout" / "google-photos").exists():
            return self.source_dir / "Takeout" / "google-photos"

        # Check original Korean folder name
        if (self.source_dir / "Google 포토").exists():
            return self.source_dir / "Google 포토"

        if (self.source_dir / "Takeout" / "Google 포토").exists():
            return self.source_dir / "Takeout" / "Google 포토"

        return None

    def get_media_files(self) -> List[Path]:
        """
        Get all media files from Google Takeout
        Filters by size (>100KB) to exclude thumbnails
        """
        media_extensions = {
            # Photos
            '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.heic', '.heif',
            # Videos
            '.mp4', '.mov', '.avi', '.mkv', '.wmv', '.m4v', '.3gp', '.webm',
        }

        media_files = []
        min_size = 100 * 1024  # 100KB minimum

        takeout_root = self.find_takeout_root()
        if not takeout_root:
            self.logger.error(f"Could not find Google Photos Takeout directory in {self.source_dir}")
            return []

        self.logger.info(f"Found Google Photos Takeout at: {takeout_root}")

        # Search for media files
        for file_path in takeout_root.rglob('*'):
            if file_path.is_file():
                # Skip JSON metadata files
                if file_path.suffix.lower() == '.json':
                    continue

                # Check extension
                if file_path.suffix.lower() in media_extensions:
                    # Check size
                    if file_path.stat().st_size >= min_size:
                        media_files.append(file_path)

        self.logger.info(f"Found {len(media_files)} media files (>100KB)")
        return media_files

    def extract_metadata(self, file_path: Path) -> Dict:
        """
        Extract metadata from file using Google Photos JSON first,
        then fallback to EXIF and filename parsing
        """
        metadata = {
            'datetime': None,
            'gps': None,
            'people': [],
            'description': '',
            'original_name': file_path.name,
            'source_folder': file_path.parent.name
        }

        # Try Google Photos JSON metadata first
        json_path = self.metadata_parser.find_json_for_media(str(file_path))
        if json_path:
            google_meta = self.metadata_parser.parse_json_metadata(json_path)
            if google_meta:
                self.stats['json_parsed'] += 1
                metadata.update(google_meta)

                if google_meta.get('gps'):
                    self.stats['gps_found'] += 1
                if google_meta.get('people'):
                    self.stats['people_found'] += 1

                self.logger.debug(f"Parsed JSON metadata for {file_path.name}")
            else:
                self.stats['json_missing'] += 1
        else:
            self.stats['json_missing'] += 1

        # Fallback to filename parsing if no datetime from JSON
        if not metadata['datetime']:
            metadata['datetime'] = self.namer.extract_datetime(str(file_path))

        return metadata

    def determine_target_path(self, source_file: Path, metadata: Dict) -> Path:
        """
        Determine target path based on file type and metadata
        """
        # Generate Denote filename
        denote_name = self.namer.generate_denote_name(str(source_file))

        # Determine category folder
        ext = source_file.suffix.lower()
        folder_name = source_file.parent.name.lower()

        # Main category
        if ext in self.namer.video_extensions:
            category = 'videos'
        elif 'screenshot' in folder_name:
            category = 'screenshots'
        elif 'document' in folder_name or '서류' in folder_name:
            category = 'documents'
        else:
            category = 'photos'

        # Year subfolder
        dt = metadata.get('datetime')
        if dt:
            year = str(dt.year)
        else:
            # Fallback to source folder name (Photos from YYYY)
            if 'Photos from' in metadata['source_folder']:
                try:
                    year = metadata['source_folder'].split('from ')[-1].strip()
                except:
                    year = str(datetime.now().year)
            else:
                year = str(datetime.now().year)

        # Construct target path
        target_path = self.target_dir / category / year / denote_name

        return target_path

    def process_file(self, source_file: Path) -> bool:
        """
        Process a single file
        Returns True if successful, False otherwise
        """
        try:
            # Extract metadata
            metadata = self.extract_metadata(source_file)

            # Determine target path
            target_path = self.determine_target_path(source_file, metadata)

            # Check for duplicates
            if target_path.parent.exists():
                duplicate = self.duplicate_checker.check_duplicate(
                    str(source_file),
                    str(target_path.parent)
                )

                if duplicate:
                    self.logger.info(f"Duplicate found: {source_file.name} -> {duplicate}")
                    self.stats['duplicates'] += 1
                    self.stats['size_saved'] += source_file.stat().st_size
                    return True  # Consider it successful, just skip

            # Create target directory
            if not self.dry_run:
                target_path.parent.mkdir(parents=True, exist_ok=True)

                # Copy file
                shutil.copy2(source_file, target_path)
                self.logger.info(f"Copied: {source_file.name} -> {target_path}")
            else:
                self.logger.info(f"[DRY RUN] Would copy: {source_file.name} -> {target_path}")

            # Update statistics
            self.stats['processed'] += 1

            # Update by type
            if target_path.suffix.lower() in self.namer.video_extensions:
                self.stats['by_type']['videos'] += 1
            else:
                self.stats['by_type']['photos'] += 1

            # Update by year
            year = target_path.parent.name
            self.stats['by_year'][year] += 1

            # Update by source folder
            source_folder = source_file.parent.name
            self.stats['by_source'][source_folder] += 1

            return True

        except Exception as e:
            self.logger.error(f"Error processing {source_file}: {e}")
            self.stats['errors'] += 1
            return False

    def process_all(self, limit: int = None):
        """
        Process all media files

        Args:
            limit: Process only this many files (for testing)
        """
        # Get all media files
        media_files = self.get_media_files()

        if limit:
            media_files = media_files[:limit]
            self.logger.info(f"Processing limited to {limit} files")

        self.stats['total_files'] = len(media_files)

        # Process each file
        for i, media_file in enumerate(media_files, 1):
            self.logger.info(f"Processing {i}/{len(media_files)}: {media_file.name}")
            self.process_file(media_file)

            # Progress report every 100 files
            if i % 100 == 0:
                self.print_progress()

        # Final report
        self.print_final_report()

        # Save duplicate cache
        self.duplicate_checker.save_cache()

    def print_progress(self):
        """Print progress report"""
        total = self.stats['total_files']
        processed = self.stats['processed']
        duplicates = self.stats['duplicates']
        errors = self.stats['errors']

        percent = (processed + duplicates + errors) / total * 100 if total > 0 else 0

        self.logger.info(f"""
        Progress: {percent:.1f}%
        Processed: {processed}/{total}
        Duplicates: {duplicates}
        JSON Parsed: {self.stats['json_parsed']}
        Errors: {errors}
        """)

    def print_final_report(self):
        """Print final report"""
        report = f"""
        ========================================
        GOOGLE PHOTOS TAKEOUT - FINAL REPORT
        ========================================
        Total Files: {self.stats['total_files']}
        Successfully Processed: {self.stats['processed']}
        Duplicates Skipped: {self.stats['duplicates']}
        Errors: {self.stats['errors']}

        Metadata:
        - JSON Parsed: {self.stats['json_parsed']}
        - JSON Missing: {self.stats['json_missing']}
        - GPS Found: {self.stats['gps_found']}
        - People Found: {self.stats['people_found']}

        By Type:
        - Photos: {self.stats['by_type']['photos']}
        - Videos: {self.stats['by_type']['videos']}

        By Year:
        """

        for year in sorted(self.stats['by_year'].keys()):
            report += f"\n        - {year}: {self.stats['by_year'][year]}"

        report += f"\n\n        By Source Folder (Top 20):"
        sorted_sources = sorted(self.stats['by_source'].items(), key=lambda x: x[1], reverse=True)
        for folder, count in sorted_sources[:20]:
            report += f"\n        - {folder}: {count}"

        # Calculate space saved
        size_saved = self.stats['size_saved']
        size_saved_mb = size_saved / (1024 * 1024)
        report += f"\n\n        Space Saved (duplicates): {size_saved_mb:.2f} MB"

        report += "\n        ========================================"

        self.logger.info(report)

        # Save report to file
        report_file = self.target_dir / "logs" / f"google_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)


def main():
    parser = argparse.ArgumentParser(
        description='Organize photos/videos from Google Photos Takeout'
    )
    parser.add_argument('source', help='Google Takeout extracted directory or Takeout root')
    parser.add_argument('target', help='Target directory for organized files')
    parser.add_argument('--dry-run', action='store_true', help='Run without actually moving files')
    parser.add_argument('--limit', type=int, help='Limit number of files to process (for testing)')

    args = parser.parse_args()

    # Initialize organizer
    organizer = GooglePhotosOrganizer(args.source, args.target, args.dry_run)

    # Process files
    organizer.process_all(limit=args.limit)


if __name__ == "__main__":
    main()
