"""Utilities to assemble a ready-to-share campaign export pack."""

from __future__ import annotations

import csv
import io
import json
import re
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union


class ExportPackBuilder:
    """Create a zipped asset bundle for a generated campaign."""
    
    def __init__(self, campaign: Dict[str, Any]):
        self.campaign = campaign or {}
        self.movie = self.campaign.get('movie_data', {})
        self.rollout = self.campaign.get('rollout_plan', {})
    
    def build(
        self,
        output_path: Union[str, Path]
    ) -> str:
        """
        Build the export pack zip on disk.
        
        Returns path to the zip file.
        """
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            self._write_contents(archive)
        
        return str(output_path)
    
    def build_bytes(self) -> bytes:
        """Build the export pack and return the bytes."""
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as archive:
            self._write_contents(archive)
        buffer.seek(0)
        return buffer.read()
    
    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _write_contents(self, archive: zipfile.ZipFile) -> None:
        archive.writestr('ad_copy_ab.csv', self._ad_copy_csv())
        archive.writestr('social_posts.csv', self._social_posts_csv())
        archive.writestr('email_campaign.md', self._email_markdown())
        archive.writestr('storyboard.json', self._storyboard_json())
        archive.writestr('thumbnail_brief.md', self._thumbnail_brief_markdown())
        archive.writestr('rollout_plan.csv', self._rollout_csv())
        archive.writestr('citations.json', self._citations_json())
        archive.writestr('metadata.json', json.dumps(self._metadata(), indent=2))
    
    def _ad_copy_csv(self) -> str:
        """Return CSV content for A/B ad copy variants."""
        output = io.StringIO()
        fieldnames = ['label', 'variant', 'length', 'platform', 'text']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        ad_copy = self.campaign.get('ad_copy', {})
        base_variants = ad_copy.get('variants', [])
        ai_variants = ad_copy.get('ai_enhanced_variants', [])
        combined = list(base_variants) + list(ai_variants)
        
        labels = ['A', 'B']
        written = 0
        for label, variant in zip(labels, combined[:2]):
            writer.writerow({
                'label': label,
                'variant': variant.get('variant', ''),
                'length': variant.get('length', ''),
                'platform': variant.get('platform', ''),
                'text': variant.get('text', '').replace('\n', ' ')
            })
            written += 1
        
        # Fallback placeholders if less than 2 variants exist
        while written < 2:
            writer.writerow({
                'label': labels[written],
                'variant': 'N/A',
                'length': 'N/A',
                'platform': '',
                'text': 'No variant generated'
            })
            written += 1
        
        return output.getvalue()
    
    def _social_posts_csv(self) -> str:
        """Return CSV of social platform posts."""
        output = io.StringIO()
        fieldnames = ['platform', 'text', 'optimal_time', 'post_type', 'image_suggestion']
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        social_posts = self.campaign.get('social_posts', {})
        for platform, payload in social_posts.items():
            if platform == 'generated_at':
                continue
            writer.writerow({
                'platform': payload.get('platform', platform),
                'text': payload.get('text', '').replace('\n', ' ').strip(),
                'optimal_time': payload.get('optimal_time', ''),
                'post_type': payload.get('post_type', ''),
                'image_suggestion': payload.get('image_suggestion', '')
            })
        
        return output.getvalue()
    
    def _email_markdown(self) -> str:
        """Generate a simple email asset."""
        title = self.movie.get('title', 'This Film')
        tagline = self.movie.get('tagline') or ''
        release_date = self.movie.get('release_date') or 'TBD'
        overview = (self.movie.get('overview') or '').strip()
        cast = ', '.join(self.movie.get('cast', [])[:3])
        
        cta = self._cta_for_release(release_date)
        subject_a = f"{title}: {tagline}" if tagline else f"{title} arrives {release_date}"
        subject_b = f"{title} — {cta}"
        
        highlights = []
        if tagline:
            highlights.append(tagline)
        if cast:
            highlights.append(f"Starring {cast}")
        genres = self.movie.get('genres')
        if genres:
            if isinstance(genres[0], dict):
                genre_name = genres[0].get('name')
            else:
                genre_name = genres[0]
            if genre_name:
                highlights.append(f"Genre fans: {genre_name}")
        
        body_intro = overview or f"{title} is gearing up for release on {release_date}."
        
        lines = [
            f"# Email Campaign: {title}",
            "",
            f"**Subject Line A:** {subject_a}",
            f"**Subject Line B:** {subject_b}",
            "",
            f"**Preview Text:** {title} lands {release_date}. {cta}.",
            "",
            "Hi {{FirstName}},",
            "",
            body_intro,
            "",
            "Key highlights:",
        ]
        
        if highlights:
            for highlight in highlights:
                lines.append(f"- {highlight}")
        else:
            lines.append("- Exclusive first look at the film.")
        
        lines.extend([
            "",
            f"Ready to secure your seats? {cta}.",
            "",
            "Best,",
            "The Campaign Team"
        ])
        
        return "\n".join(lines)
    
    def _storyboard_json(self) -> str:
        """Generate storyboard frames derived from rollout phases."""
        title = self.movie.get('title', 'This Film')
        frames = []
        
        phases = self.rollout.get('phases', [])
        if not phases:
            phases = [{
                'name': 'Teaser Drop',
                'focus': 'Intro hero moments & release date reveal',
                'regions': self.campaign.get('regional_analysis', {}).get('target_regions', [])
            }]
        
        for idx, phase in enumerate(phases[:4], start=1):
            frames.append({
                'frame': idx,
                'title': phase.get('name', f'Phase {idx}'),
                'visual_direction': self._visual_direction(idx),
                'copy': phase.get('focus', '') or f"Highlight why {title} is a must-see.",
                'cta': 'Get tickets' if idx >= 2 else 'Watch the trailer',
                'start_date': phase.get('start_date'),
                'regions': phase.get('regions', []),
                'intensity': phase.get('intensity', '')
            })
        
        payload = {
            'title': title,
            'release_date': self.movie.get('release_date'),
            'frames': frames
        }
        return json.dumps(payload, indent=2)
    
    def _thumbnail_brief_markdown(self) -> str:
        """Return markdown instructions for thumbnail creation."""
        title = self.movie.get('title', 'This Film')
        primary_genre = self._primary_genre()
        tagline = self.movie.get('tagline') or ''
        cast = ', '.join(self.movie.get('cast', [])[:2])
        
        lines = [
            f"# Thumbnail Brief — {title}",
            "",
            f"**Tone/Genre:** {primary_genre}",
            f"**Tagline/Hook:** {tagline or 'Use bold text to tease the conflict or stakes.'}",
            "",
            "## Visual Directions",
            "- High contrast still of the lead with cinematic lighting",
            "- Layer subtle grain or texture for a premium feel",
            "- Include release date badge in a corner",
            "",
            "## Text Overlay Options",
            f"- \"{title}\" large with secondary line \"{self._cta_for_release(self.movie.get('release_date') or '')}\"",
            "- Use angle brackets or slashes to hint at motion/action",
            "",
            "## Talent / Elements",
            f"- Priority cast: {cast or 'Use key art silhouettes if cast unavailable.'}",
            "- Background motif inspired by primary location or genre iconography",
            "",
            "## Color Palette",
            "- Accent: Electric violet or fiery orange for CTA badge",
            "- Base: Deep navy/charcoal to keep text legible",
        ]
        return "\n".join(lines)
    
    def _rollout_csv(self) -> str:
        """Convert rollout timeline to CSV."""
        output = io.StringIO()
        fieldnames = [
            'week', 'start_date', 'end_date', 'phase',
            'intensity', 'regions', 'activities'
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        timeline = self.rollout.get('timeline', [])
        for entry in timeline:
            regions = entry.get('active_regions') or []
            activities = entry.get('key_activities') or []
            writer.writerow({
                'week': entry.get('week'),
                'start_date': entry.get('start_date'),
                'end_date': entry.get('end_date'),
                'phase': entry.get('phase'),
                'intensity': entry.get('intensity'),
                'regions': ', '.join(regions),
                'activities': ' | '.join(activities)
            })
        
        return output.getvalue()
    
    def _citations_json(self) -> str:
        """Return citations JSON extracted from the ad copy source tracker."""
        ad_copy = self.campaign.get('ad_copy', {})
        details = ad_copy.get('source_details') or {}
        
        if isinstance(details, str):
            try:
                parsed = json.loads(details)
            except json.JSONDecodeError:
                parsed = {'raw': details}
        elif isinstance(details, dict):
            parsed = details
        else:
            parsed = {}
        
        parsed['citation_strings'] = ad_copy.get('sources', [])
        return json.dumps(parsed, indent=2)
    
    def _metadata(self) -> Dict[str, Any]:
        """High-level metadata for the bundle."""
        title = self.movie.get('title', 'campaign')
        safe_title = re.sub(r'[^A-Za-z0-9\\-_ ]+', '', title).strip()
        generated_at = self.campaign.get('generated_at') or datetime.now().isoformat()
        
        return {
            'title': safe_title or 'campaign',
            'generated_at': generated_at,
            'assets': [
                'ad_copy_ab.csv',
                'social_posts.csv',
                'email_campaign.md',
                'storyboard.json',
                'thumbnail_brief.md',
                'rollout_plan.csv',
                'citations.json'
            ]
        }
    
    def _primary_genre(self) -> str:
        genres = self.movie.get('genres') or []
        if not genres:
            return 'Event'
        first = genres[0]
        if isinstance(first, dict):
            return first.get('name', 'Event')
        return first
    
    def _visual_direction(self, idx: int) -> str:
        palette = [
            "High-energy montage of hero shots",
            "Character close-up with moody lighting",
            "World-building wide shot with typography overlay",
            "Fan/community oriented collage"
        ]
        return palette[(idx - 1) % len(palette)]
    
    def _cta_for_release(self, release_date: str) -> str:
        """Choose CTA language based on release window."""
        if not release_date:
            return "Learn more"
        try:
            release = datetime.strptime(release_date, '%Y-%m-%d')
            now = datetime.now()
            if release <= now:
                return "Watch now"
            elif (release - now).days <= 21:
                return "Get tickets"
            else:
                return f"Coming {release.strftime('%b %d')}"
        except Exception:
            return "Get tickets"
