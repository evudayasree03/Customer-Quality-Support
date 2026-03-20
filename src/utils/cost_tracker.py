"""
SamiX Financial Intelligence & Cost Tracking

This module manages the economic layer of the platform. It calculates 
real-time API consumption costs and projected subscription margins.

Pricing is based on:
- Groq: Token-based LLM throughput.
- Deepgram: Per-minute audio transcription (Pre-recorded).
- Twilio: Per-minute live media stream ingestion.
"""
from __future__ import annotations

from dataclasses import dataclass, field


# Pricing Configuration 
# Constants representing current USD market rates for core infrastructure.

# Price per 1,000 tokens (USD)
_GROQ_INPUT_PER_1K  = 0.00027
_GROQ_OUTPUT_PER_1K = 0.00027

# Deepgram pricing: $0.0043 per minute of processed audio.
_DG_PER_MINUTE = 0.0043

# Twilio Media Streams: $0.004 per minute of active connection.
_TWILIO_PER_MINUTE = 0.004

# Monthly subscription tiers for customer billing.
_PLAN_PRICES: dict[str, float] = {
    "Basic":      99.0,
    "Pro":        299.0,
    "Enterprise": 999.0,
}


@dataclass
class SessionCost:
    """
    Detailed financial breakdown for a single audit execution.
    Tracks exact micro-spend across all integrated providers.
    """
    token_count:         int   = 0
    groq_cost_usd:       float = 0.0
    deepgram_cost_usd:   float = 0.0
    twilio_cost_usd:     float = 0.0
    total_cost_usd:      float = 0.0

    def to_dict(self) -> dict:
        """ Returns a human-friendly dictionary with formatted currency strings. """
        return {
            "tokens":      self.token_count,
            "groq":        f"${self.groq_cost_usd:.4f}",
            "deepgram":    f"${self.deepgram_cost_usd:.4f}",
            "twilio":      f"${self.twilio_cost_usd:.4f}",
            "total":       f"${self.total_cost_usd:.4f}",
        }


@dataclass
class MonthlySummary:
    """
    Executive-level aggregation of platform expenditure and revenue.
    Used to calculate Gross Margin and project ROI.
    """
    total_audits:         int   = 0
    total_tokens:         int   = 0
    groq_total_usd:       float = 0.0
    deepgram_total_usd:   float = 0.0
    twilio_total_usd:     float = 0.0
    total_api_cost_usd:   float = 0.0
    subscription_revenue: float = 0.0
    gross_margin_pct:     float = 0.0


class CostTracker:
    """
    The central accounting engine for SamiX.
    
    Translates raw infrastructure usage (tokens, seconds) into 
    business-level metrics (costs, margins, profit).
    """

    def calculate_session_cost(
        self,
        token_count: int,
        audio_duration_sec: int = 0,
        is_live_call: bool = False,
    ) -> SessionCost:
        """
        Calculates the infrastructure cost for a single session.
        
        Args:
            token_count: Total tokens consumed by LLM calls.
            audio_duration_sec: Length of the call/recording.
            is_live_call: Whether Twilio or Deepgram pricing applies.
        """
        # Assume 2 LLM calls per session (summary + scoring).
        groq_cost = (token_count / 1000) * _GROQ_INPUT_PER_1K * 2  
        
        # Calculate transcription/ingestion costs based on mode.
        dg_cost   = (audio_duration_sec / 60) * _DG_PER_MINUTE if not is_live_call and audio_duration_sec > 0 else 0.0
        tw_cost   = (audio_duration_sec / 60) * _TWILIO_PER_MINUTE if is_live_call and audio_duration_sec > 0 else 0.0
        total     = groq_cost + dg_cost + tw_cost

        return SessionCost(
            token_count=token_count,
            groq_cost_usd=round(groq_cost, 5),
            deepgram_cost_usd=round(dg_cost, 5),
            twilio_cost_usd=round(tw_cost, 5),
            total_cost_usd=round(total, 5),
        )

    def build_monthly_summary(
        self,
        sessions: list[dict],
        customer_plans: list[str],
    ) -> MonthlySummary:
        """
        Aggregates session data to provide a holistic view of billing.
        Computes total platform revenue vs. API expenditure.
        """
        total_tokens  = sum(s.get("token_count", 0)  for s in sessions)
        total_groq    = sum(s.get("groq_cost", 0.0)  for s in sessions)
        total_dg      = sum(s.get("deepgram_cost", 0.0) for s in sessions)
        total_tw      = sum(s.get("twilio_cost", 0.0)   for s in sessions)
        total_api     = total_groq + total_dg + total_tw
        
        # Sum revenue based on active customer subscription tiers.
        revenue       = sum(_PLAN_PRICES.get(p, 0) for p in customer_plans)
        margin        = ((revenue - total_api) / revenue * 100) if revenue > 0 else 0.0

        return MonthlySummary(
            total_audits=len(sessions),
            total_tokens=total_tokens,
            groq_total_usd=round(total_groq, 2),
            deepgram_total_usd=round(total_dg, 2),
            twilio_total_usd=round(total_tw, 2),
            total_api_cost_usd=round(total_api, 2),
            subscription_revenue=round(revenue, 2),
            gross_margin_pct=round(margin, 1),
        )

    @staticmethod
    def metric_card_data(cost: SessionCost, revenue_per_audit: float = 5.0) -> dict:
        """
        Prepares a formatted data payload for the UI cost evaluation card.
        Allocates a nominal share of subscription revenue to each audit ($5.00).
        """
        profit = revenue_per_audit - cost.total_cost_usd
        return {
            "tokens":           cost.token_count,
            "api_cost":         f"${cost.total_cost_usd:.5f}",
            "revenue_per_call": f"${revenue_per_audit:.2f}",
            "profit_per_call":  f"${profit:.4f}",
            "margin_pct":       f"{(profit / revenue_per_audit * 100):.1f}%" if revenue_per_audit else "N/A",
        }
