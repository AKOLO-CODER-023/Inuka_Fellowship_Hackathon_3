"""
backend/alerts.py

Sends alerts when the decision engine flags something urgent.

HONEST SCOPE:
The hackathon brief asks for "automated alerting (e.g. PagerDuty/Slack
integrations)". We don't have real PagerDuty/Slack credentials to wire
up, so this module:

  1. ALWAYS writes a structured, level-appropriate log line -- this part
     is fully real and works right now, with no configuration needed.
  2. OPTIONALLY posts to a Slack Incoming Webhook if the SLACK_WEBHOOK_URL
     environment variable is set. If it's not set, this is a safe no-op --
     it does not pretend to have sent anything it didn't.

This means the demo can show: "here is the alert firing in the logs the
moment risk_level goes CRITICAL -- and if we point SLACK_WEBHOOK_URL at
our team's Slack, the exact same call also posts there, live."
"""

import logging
import os
from typing import Optional

import requests

logger = logging.getLogger("inuka-alerts")

SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

_ALERT_RISK_LEVELS = {"CRITICAL", "HIGH"}


def alert_on_decision(decision: dict) -> Optional[dict]:
    """
    Inspect a decision from the decision engine and fire an alert if its
    risk level warrants one. Safe to call on every decision -- it's a
    no-op for SAFE/WARNING risk levels.

    Returns a small dict describing what happened, for logging/testing:
        {"fired": bool, "channel": "log" | "log+slack" | None, "reason": str | None}
    """
    risk_level = decision.get("risk_level")

    if risk_level not in _ALERT_RISK_LEVELS:
        return {"fired": False, "channel": None, "reason": None}

    message = (
        f"[{risk_level}] {decision.get('depot')} / {decision.get('product')} -- "
        f"{decision.get('days_of_cover')} days of cover, "
        f"recommended action: {decision.get('recommended_action')} "
        f"({decision.get('recommended_volume_m3')} m3, priority={decision.get('priority')})"
    )

    if risk_level == "CRITICAL":
        logger.critical(message)
    else:
        logger.warning(message)

    channel = "log"
    if SLACK_WEBHOOK_URL:
        try:
            requests.post(SLACK_WEBHOOK_URL, json={"text": message}, timeout=3)
            channel = "log+slack"
        except requests.RequestException:
            logger.exception("Slack alert failed to send; alert was still logged above.")

    return {"fired": True, "channel": channel, "reason": message}
