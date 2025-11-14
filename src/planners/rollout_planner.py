"""Regional rollout campaign planner."""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import math

from ..analyzers.regional_scorer import RegionalScorer


class RolloutPlanner:
    """Plan geographic and temporal campaign rollout strategy."""
    
    def __init__(self):
        self.scorer = RegionalScorer()
    
    def create_rollout_plan(
        self,
        regional_data: Optional[Dict[str, Dict[str, Any]]],
        release_date: str,
        budget_total: Optional[float] = None,
        campaign_weeks: Optional[int] = None,
        movie_profile: Optional[Dict[str, Any]] = None,
        precomputed_comparison: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create comprehensive regional rollout plan.
        
        Args:
            regional_data: Dict of {region_code: {metrics}}
            release_date: Movie release date (YYYY-MM-DD)
            budget_total: Total campaign budget (optional override)
            campaign_weeks: Weeks before release to start campaign (optional override)
            movie_profile: Movie metadata to customize the plan
            precomputed_comparison: Pre-scored regional comparison (optional)
        """
        regional_payload = regional_data or {}
        
        # Score and rank regions
        comparison = precomputed_comparison or self.scorer.compare_regions(regional_payload)
        ranked_regions = comparison['ranked_regions']
        
        # Parse release date
        try:
            release_dt = datetime.strptime(release_date, '%Y-%m-%d')
        except:
            release_dt = datetime.now() + timedelta(days=60)
        
        movie_signature = self._extract_movie_signature(movie_profile)
        
        planning_parameters = self._derive_campaign_parameters(
            movie_profile or {},
            comparison,
            budget_total,
            campaign_weeks,
            release_dt
        )
        
        budget_total = planning_parameters['total_budget']
        campaign_weeks = planning_parameters['campaign_weeks']
        
        campaign_start = release_dt - timedelta(weeks=campaign_weeks)
        
        # Create phased rollout
        phases = self._create_phases(
            ranked_regions,
            campaign_start,
            release_dt,
            movie_signature,
            campaign_weeks
        )
        
        # Allocate budget
        budget_allocation = self._allocate_budget(ranked_regions, budget_total)
        
        # Create timeline
        timeline = self._create_timeline(phases, campaign_start, release_dt)
        
        # Channel recommendations
        channels = self._recommend_channels(ranked_regions)
        
        return {
            'campaign_overview': {
                'release_date': release_date,
                'campaign_start': campaign_start.strftime('%Y-%m-%d'),
                'duration_weeks': campaign_weeks,
                'total_budget': budget_total,
                'target_regions': len(ranked_regions),
                'movie_positioning': {
                    'title': movie_signature['title'],
                    'primary_genre': movie_signature['primary_genre'],
                    'hook': movie_signature['hook'],
                    'lead': movie_signature['lead'],
                    'tagline': movie_signature['tagline']
                }
            },
            'phases': phases,
            'budget_allocation': budget_allocation,
            'timeline': timeline,
            'channel_strategy': channels,
            'key_milestones': self._generate_milestones(campaign_start, release_dt),
            'recommendations': comparison['recommendations'],
            'plan_logic': planning_parameters['logic'],
            'budget_duration_logic': planning_parameters['logic']
        }
    
    def _create_phases(
        self,
        ranked_regions: List[Dict[str, Any]],
        start_date: datetime,
        release_date: datetime,
        movie_signature: Dict[str, str],
        campaign_weeks: int
    ) -> List[Dict[str, Any]]:
        """Create phased rollout schedule."""
        # Group regions by tier
        tier_a = [r for r in ranked_regions if r['tier'] == 'A']
        tier_b = [r for r in ranked_regions if r['tier'] == 'B']
        tier_c = [r for r in ranked_regions if r['tier'] == 'C']
        
        if not (tier_a or tier_b or tier_c):
            return []
        
        phases = []
        total_weeks = max(1, campaign_weeks)
        
        def _offset(multiplier: float, min_week: int) -> int:
            if total_weeks <= min_week:
                return max(0, total_weeks - 1)
            tentative = int(round(total_weeks * multiplier))
            tentative = max(min_week, tentative)
            return min(total_weeks - 1, tentative)
        
        offsets = {
            'A': 0,
            'B': _offset(0.35, 1),
            'C': _offset(0.65, 2)
        }
        
        # Dynamic budget split weights
        weight_map = {}
        if tier_a:
            weight_map['A'] = 40 + min(len(tier_a) * 4, 20)
        if tier_b:
            weight_map['B'] = 30 + min(len(tier_b) * 3, 15)
        if tier_c:
            weight_map['C'] = 20 + min(len(tier_c) * 2, 10)
        
        total_weight = sum(weight_map.values()) or 1
        normalized_pct = {}
        running_total = 0
        ordered_keys = [k for k in ['A', 'B', 'C'] if k in weight_map]
        for idx, key in enumerate(ordered_keys):
            pct = round(weight_map[key] / total_weight * 100)
            if idx == len(ordered_keys) - 1:
                pct = 100 - running_total
            running_total += pct
            normalized_pct[key] = pct
        
        genre_focus = movie_signature.get('genre_focus', 'cinematic moments')
        lead_name = movie_signature.get('lead') or 'the ensemble cast'
        audience = movie_signature.get('audience_callout', 'fans')
        hook = movie_signature.get('hook') or movie_signature.get('title') or 'the film'
        title_short = movie_signature.get('title', 'the film')
        
        def _phase_duration(start: datetime) -> int:
            return max(1, math.ceil((release_date - start).days / 7))
        
        # Phase 1: Tier A (Primary markets) - Start immediately
        if tier_a:
            focus_text = (
                f"Position {title_short} as the must-see {movie_signature.get('primary_genre', '').lower()} event. "
                f"Lead with {genre_focus} and {lead_name} interviews to rally {audience} and drive premium pre-sales."
            ).strip()
            phases.append({
                'phase': len(phases) + 1,
                'name': f"{movie_signature.get('primary_genre', 'Priority')} Fan Ignition",
                'start_date': start_date.strftime('%Y-%m-%d'),
                'duration_weeks': _phase_duration(start_date),
                'regions': [r['region'] for r in tier_a],
                'intensity': 'High',
                'focus': focus_text,
                'budget_percentage': normalized_pct.get('A', 0),
                'movie_hook': hook
            })
        
        # Phase 2: Tier B expansion
        if tier_b and start_date < release_date:
            offset_weeks = offsets['B']
            phase_start = min(release_date, start_date + timedelta(weeks=offset_weeks))
            if phase_start < release_date:
                focus_text = (
                    f"Capitalize on Tier-A reactions by localizing social proof clips, critic quotes, and {hook.lower()} callouts. "
                    f"Balance paid reach with experiential moments for regional partners."
                )
                phases.append({
                    'phase': len(phases) + 1,
                    'name': "Social Proof Expansion",
                    'start_date': phase_start.strftime('%Y-%m-%d'),
                    'duration_weeks': _phase_duration(phase_start),
                    'regions': [r['region'] for r in tier_b],
                    'intensity': 'Medium',
                    'focus': focus_text,
                    'budget_percentage': normalized_pct.get('B', 0),
                    'movie_hook': f"Localized {genre_focus}"
                })
        
        # Phase 3: Long-tail + tier C
        if tier_c and start_date < release_date:
            offset_weeks = offsets['C']
            phase_start = min(release_date, start_date + timedelta(weeks=offset_weeks))
            if phase_start < release_date:
                focus_text = (
                    f"Keep {title_short} top-of-mind with cost-efficient retargeting, fan community drops, "
                    f"and partner bundles that celebrate {genre_focus}."
                )
                phases.append({
                    'phase': len(phases) + 1,
                    'name': "Long-tail Sustain & Emerging Markets",
                    'start_date': phase_start.strftime('%Y-%m-%d'),
                    'duration_weeks': _phase_duration(phase_start),
                    'regions': [r['region'] for r in tier_c],
                    'intensity': 'Low',
                    'focus': focus_text,
                    'budget_percentage': normalized_pct.get('C', 0),
                    'movie_hook': f"Community-driven {title_short}"
                })
        
        return phases
    
    def _allocate_budget(
        self,
        ranked_regions: List[Dict[str, Any]],
        total_budget: float
    ) -> List[Dict[str, Any]]:
        """Allocate budget across regions."""
        allocations = []
        
        # Use suggested percentages from scoring
        total_pct = sum(r['suggested_budget_pct'] for r in ranked_regions)
        
        for region_data in ranked_regions:
            # Normalize percentage
            pct = (region_data['suggested_budget_pct'] / total_pct * 100) if total_pct > 0 else 0
            amount = (pct / 100) * total_budget
            
            allocations.append({
                'region': region_data['region'],
                'budget_amount': round(amount, 2),
                'percentage': round(pct, 2),
                'tier': region_data['tier'],
                'justification': region_data['recommendation']
            })
        
        return sorted(allocations, key=lambda x: x['budget_amount'], reverse=True)
    
    def _create_timeline(
        self,
        phases: List[Dict[str, Any]],
        start_date: datetime,
        release_date: datetime
    ) -> List[Dict[str, Any]]:
        """Create week-by-week timeline."""
        timeline = []
        current = start_date
        week = 1
        
        while current < release_date:
            week_end = min(current + timedelta(days=7), release_date)
            
            # Determine active phase
            active_phase = None
            for phase in phases:
                phase_start = datetime.strptime(phase['start_date'], '%Y-%m-%d')
                if phase_start <= current:
                    active_phase = phase
            
            # Determine activities based on weeks to release
            weeks_to_release = (release_date - current).days // 7
            activities = self._get_weekly_activities(weeks_to_release)
            
            timeline.append({
                'week': week,
                'start_date': current.strftime('%Y-%m-%d'),
                'end_date': week_end.strftime('%Y-%m-%d'),
                'phase': active_phase['name'] if active_phase else 'Pre-campaign',
                'active_regions': active_phase['regions'] if active_phase else [],
                'key_activities': activities,
                'intensity': active_phase['intensity'] if active_phase else 'Low'
            })
            
            current = week_end
            week += 1
        
        return timeline
    
    def _get_weekly_activities(self, weeks_to_release: int) -> List[str]:
        """Get recommended activities based on weeks until release."""
        if weeks_to_release >= 6:
            return [
                "Launch teaser campaign",
                "Build social media presence",
                "Secure media partnerships"
            ]
        elif weeks_to_release >= 4:
            return [
                "Release official trailer",
                "Start paid social campaigns",
                "Begin PR tour"
            ]
        elif weeks_to_release >= 2:
            return [
                "Intensify digital ads",
                "Launch ticket pre-sales",
                "Host premiere events"
            ]
        else:
            return [
                "Final push - all channels",
                "Leverage reviews & testimonials",
                "Drive ticket sales"
            ]
    
    def _recommend_channels(
        self,
        ranked_regions: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Recommend marketing channels by region tier."""
        return {
            'tier_a_regions': {
                'regions': [r['region'] for r in ranked_regions if r['tier'] == 'A'],
                'channels': [
                    'TV spots (prime time)',
                    'YouTube pre-roll',
                    'Instagram/Facebook ads',
                    'Outdoor billboards (major cities)',
                    'Influencer partnerships',
                    'Podcast sponsorships'
                ],
                'investment_level': 'High'
            },
            'tier_b_regions': {
                'regions': [r['region'] for r in ranked_regions if r['tier'] == 'B'],
                'channels': [
                    'Digital video ads',
                    'Social media ads',
                    'Streaming platform ads',
                    'Local radio spots'
                ],
                'investment_level': 'Medium'
            },
            'tier_c_regions': {
                'regions': [r['region'] for r in ranked_regions if r['tier'] == 'C'],
                'channels': [
                    'Social media organic',
                    'Display ads',
                    'Email campaigns',
                    'Search engine marketing'
                ],
                'investment_level': 'Low-Medium'
            }
        }
    
    def _generate_milestones(
        self,
        start_date: datetime,
        release_date: datetime
    ) -> List[Dict[str, Any]]:
        """Generate key campaign milestones."""
        milestones = []
        
        # Campaign launch
        milestones.append({
            'date': start_date.strftime('%Y-%m-%d'),
            'milestone': 'Campaign Launch',
            'description': 'Teaser release, social media kickoff'
        })
        
        # Trailer release (4 weeks before)
        trailer_date = release_date - timedelta(weeks=4)
        if trailer_date > start_date:
            milestones.append({
                'date': trailer_date.strftime('%Y-%m-%d'),
                'milestone': 'Official Trailer Release',
                'description': 'Major media push, paid amplification'
            })
        
        # Ticket pre-sales (2 weeks before)
        presale_date = release_date - timedelta(weeks=2)
        if presale_date > start_date:
            milestones.append({
                'date': presale_date.strftime('%Y-%m-%d'),
                'milestone': 'Ticket Pre-Sales Open',
                'description': 'Drive early bookings, create urgency'
            })
        
        # Premiere (1 week before)
        premiere_date = release_date - timedelta(weeks=1)
        if premiere_date > start_date:
            milestones.append({
                'date': premiere_date.strftime('%Y-%m-%d'),
                'milestone': 'World Premiere',
                'description': 'Red carpet event, press coverage, reviews'
            })
        
        # Release day
        milestones.append({
            'date': release_date.strftime('%Y-%m-%d'),
            'milestone': '🎬 RELEASE DAY',
            'description': 'Full availability, maximize opening weekend'
        })
        
        return sorted(milestones, key=lambda x: x['date'])

    def _derive_campaign_parameters(
        self,
        movie_profile: Dict[str, Any],
        regional_summary: Optional[Dict[str, Any]],
        override_budget: Optional[float],
        override_duration: Optional[int],
        release_dt: datetime
    ) -> Dict[str, Any]:
        """Derive dynamic budget and campaign duration based on movie signals."""
        ranked_regions = (regional_summary or {}).get('ranked_regions', [])
        tier_a_count = len([r for r in ranked_regions if r.get('tier') == 'A'])
        tier_b_count = len([r for r in ranked_regions if r.get('tier') == 'B'])
        top_scores = [r.get('total_score', 0) for r in ranked_regions][:3]
        interest_index = (sum(top_scores) / len(top_scores) / 100) if top_scores else 0.55
        
        try:
            popularity = float(movie_profile.get('popularity', 45) or 45)
        except (TypeError, ValueError):
            popularity = 45.0
        
        try:
            production_budget = float(movie_profile.get('budget') or 0)
        except (TypeError, ValueError):
            production_budget = 0.0
        
        release_gap_days = max(0, (release_dt - datetime.now()).days)
        release_gap_weeks = math.ceil(release_gap_days / 7) if release_gap_days else 0
        
        # Duration logic
        duration_logic: List[str] = []
        if override_duration is not None:
            campaign_weeks = max(1, int(override_duration))
            duration_logic.append(f"Duration overridden upstream to {campaign_weeks} weeks.")
        else:
            if release_gap_weeks > 0:
                base_weeks = min(max(release_gap_weeks, 4), 16)
                duration_logic.append(f"{release_gap_weeks}-week runway until release -> base {base_weeks}-week plan.")
            else:
                base_weeks = 6
                duration_logic.append("Release date is in-market/unknown, applying 6-week sustain push.")
            campaign_weeks = base_weeks
            if popularity >= 70:
                campaign_weeks += 1
                duration_logic.append(f"High popularity score ({popularity:.0f}) adds +1 hype week.")
            if tier_a_count >= 3:
                campaign_weeks += 1
                duration_logic.append(f"{tier_a_count} Tier-A markets need an extra localization week.")
            if production_budget >= 150_000_000:
                campaign_weeks += 1
                duration_logic.append("Tentpole scale (> $150M production) adds +1 buffer week.")
            campaign_weeks = max(4, min(campaign_weeks, 16))
        
        # Budget logic
        budget_logic: List[str] = []
        if override_budget is not None:
            total_budget_value = int(override_budget)
            budget_logic.append(f"Budget overridden upstream at ${total_budget_value:,.0f}.")
        else:
            if production_budget > 0:
                if production_budget >= 150_000_000:
                    marketing_ratio = 0.4
                elif production_budget >= 75_000_000:
                    marketing_ratio = 0.32
                elif production_budget >= 25_000_000:
                    marketing_ratio = 0.25
                else:
                    marketing_ratio = 0.18
                base_budget = production_budget * marketing_ratio
                budget_logic.append(
                    f"Used {int(marketing_ratio * 100)}% of ${production_budget:,.0f} production budget as marketing baseline."
                )
            else:
                base_budget = 350000
                budget_logic.append("No production budget reported, starting from $350K indie baseline.")
            
            pop_score = max(0.0, min(popularity, 100.0))
            popularity_factor = 1 + (pop_score / 100) * 0.35
            base_budget *= popularity_factor
            if pop_score:
                budget_logic.append(f"Popularity score {popularity:.0f} adds {((popularity_factor - 1) * 100):.0f}% hype premium.")
            
            tier_factor = 1 + min(tier_a_count, 4) * 0.08 + min(tier_b_count, 4) * 0.03
            base_budget *= tier_factor
            budget_logic.append(f"Tier mix ({tier_a_count} Tier-A / {tier_b_count} Tier-B) drives {tier_factor:.2f}x geographic weighting.")
            
            interest_factor = 1 + max(0, interest_index - 0.55) * 0.5
            base_budget *= interest_factor
            budget_logic.append(f"Regional interest index {interest_index * 100:.0f} => {interest_factor:.2f}x demand lift.")
            
            try:
                vote_count = int(movie_profile.get('vote_count') or 0)
            except (TypeError, ValueError):
                vote_count = 0
            if vote_count:
                audience_factor = 1 + min(vote_count / 50000, 1) * 0.15
                base_budget *= audience_factor
                budget_logic.append(f"{vote_count:,} fan ratings justify {audience_factor:.2f}x proof-of-fanbase boost.")
            
            computed_budget = max(250000, min(base_budget, 20000000))
            total_budget_value = max(250000, int(round(computed_budget / 50000) * 50000))
        
        release_label = release_dt.strftime('%Y-%m-%d')
        movie_title = movie_profile.get('title', 'the film')
        logic = {
            'summary': f"Budget and timeline tuned for {movie_title} based on production scale and market demand.",
            'budget': {
                'summary': f"Allocated ${total_budget_value:,.0f} to cover {tier_a_count} Tier-A markets and momentum signals.",
                'drivers': budget_logic
            },
            'duration': {
                'summary': f"Running campaign for {campaign_weeks} weeks leading into {release_label}.",
                'drivers': duration_logic
            },
            'signals': {
                'tier_a_markets': tier_a_count,
                'tier_b_markets': tier_b_count,
                'interest_index': round(interest_index * 100, 1),
                'popularity': round(popularity, 1),
                'release_gap_weeks': release_gap_weeks
            }
        }
        
        return {
            'total_budget': total_budget_value,
            'campaign_weeks': campaign_weeks,
            'logic': logic
        }
    
    def _extract_movie_signature(
        self,
        movie_profile: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Extract positioning cues to customize rollout text."""
        if not movie_profile:
            return {
                'title': 'This film',
                'primary_genre': 'Event',
                'genre_focus': 'cinematic spectacle',
                'hook': 'Fan-favorite moments',
                'lead': 'the ensemble cast',
                'tagline': '',
                'audience_callout': 'fans',
                'supporting': []
            }
        
        title = movie_profile.get('title') or 'This film'
        
        genres = movie_profile.get('genres') or []
        if genres and isinstance(genres[0], dict):
            genres = [g.get('name') for g in genres if isinstance(g, dict) and g.get('name')]
        primary_genre = genres[0] if genres else 'Event'
        
        genre_focus_map = {
            'Action': 'high-impact action beats',
            'Adventure': 'world-building spectacle',
            'Science Fiction': 'immersive sci-fi worldbuilding',
            'Fantasy': 'mythic fantasy imagery',
            'Animation': 'signature animation style',
            'Drama': 'character-driven drama',
            'Comedy': 'sharp comedic timing',
            'Horror': 'edge-of-seat suspense',
            'Thriller': 'white-knuckle thrills',
            'Romance': 'sweeping romantic stakes',
            'Documentary': 'truth-first storytelling'
        }
        genre_focus = genre_focus_map.get(primary_genre, f"{primary_genre.lower()} energy")
        
        audience_map = {
            'Action': 'action seekers',
            'Adventure': 'genre fans',
            'Science Fiction': 'sci-fi faithful',
            'Fantasy': 'fantasy fandoms',
            'Animation': 'family audiences',
            'Drama': 'prestige audiences',
            'Comedy': 'comedy lovers',
            'Horror': 'thrill seekers',
            'Thriller': 'thriller fans',
            'Romance': 'date-night audiences',
            'Documentary': 'non-fiction fans'
        }
        audience_callout = audience_map.get(primary_genre, f"{primary_genre.lower()} fans")
        
        cast_entries = movie_profile.get('cast') or []
        cast_names: List[str] = []
        for entry in cast_entries:
            if isinstance(entry, dict):
                name = entry.get('name')
            else:
                name = str(entry) if entry else None
            if name:
                cast_names.append(name)
        
        lead = cast_names[0] if cast_names else None
        supporting = cast_names[1:3]
        directors = movie_profile.get('directors') or movie_profile.get('director')
        if isinstance(directors, dict):
            directors = [directors.get('name')]
        if isinstance(directors, str):
            directors = [directors]
        if directors and not lead:
            lead = directors[0]
        
        tagline = movie_profile.get('tagline') or ''
        if tagline:
            hook = tagline
        elif lead:
            hook = f"{lead}'s {primary_genre.lower()} turn"
        else:
            hook = f"fan-favorite {primary_genre.lower()} moments"
        
        return {
            'title': title,
            'primary_genre': primary_genre,
            'genre_focus': genre_focus,
            'hook': hook,
            'lead': lead or 'the ensemble cast',
            'tagline': tagline,
            'audience_callout': audience_callout,
            'supporting': supporting
        }


# Example usage
if __name__ == "__main__":
    planner = RolloutPlanner()
    
    regional_data = {
        'US': {'interest_score': 95, 'engagement_rate': 0.08, 'growth_rate': 0.12, 'sentiment_score': 0.85},
        'GB': {'interest_score': 87, 'engagement_rate': 0.09, 'growth_rate': 0.15, 'sentiment_score': 0.82},
        'IN': {'interest_score': 72, 'engagement_rate': 0.12, 'growth_rate': 0.35, 'sentiment_score': 0.78},
        'BR': {'interest_score': 65, 'engagement_rate': 0.07, 'growth_rate': 0.08, 'sentiment_score': 0.75},
    }
    
    plan = planner.create_rollout_plan(
        regional_data,
        release_date='2024-06-15',
        budget_total=2000000,
        campaign_weeks=6
    )
    
    print("🎬 Campaign Rollout Plan\n")
    print(f"Release: {plan['campaign_overview']['release_date']}")
    print(f"Budget: ${plan['campaign_overview']['total_budget']:,.0f}\n")
    
    print("📅 Phases:")
    for phase in plan['phases']:
        print(f"  Phase {phase['phase']}: {phase['name']}")
        print(f"  Regions: {', '.join(phase['regions'])}")
        print(f"  Budget: {phase['budget_percentage']}%\n")
