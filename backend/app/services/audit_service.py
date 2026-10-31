"""
CLAIMSIGHT AI - Audit Logging Service
Provides tamper-evident compliance audit trailing for SIU operations.
"""

import datetime
from app.core.database import get_database

class AuditService:
    @staticmethod
    def log(claim_id: str, user_id: str, action: str, details: str):
        db = get_database()
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        log_entry = {
            "log_id": f"AUD-{int(datetime.datetime.now().timestamp() * 1000)}",
            "claim_id": claim_id,
            "user_id": user_id,
            "action": action,
            "details": details,
            "timestamp": now
        }
        db.audit_logs.insert_one(log_entry)
        return log_entry

