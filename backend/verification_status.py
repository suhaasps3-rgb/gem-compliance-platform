"""Shared result vocabulary. A check that could not be run must never read as a pass."""

VERIFIED = "VERIFIED"            # checked against evidence and passed
FAILED = "FAILED"                # checked against evidence and did not pass
UNVERIFIED = "UNVERIFIED"        # could not be checked (no data, no source, parser found nothing)
NOT_APPLICABLE = "NOT_APPLICABLE"  # the tender does not require this check

ALL_STATUSES = (VERIFIED, FAILED, UNVERIFIED, NOT_APPLICABLE)
