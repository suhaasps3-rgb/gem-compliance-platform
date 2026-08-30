import hashlib
import json
from datetime import datetime
import copy

class AuditEngine:
    def __init__(self):
        self._ledger = []
        # Genesis block
        self._ledger.append({
            "event_type": "GENESIS",
            "payload": {},
            "timestamp": datetime.utcnow().isoformat(),
            "previous_hash": "0" * 64,
            "current_hash": "0" * 64
        })

    def _recursive_mask(self, data):
        import re
        aadhaar_pattern = re.compile(r'\b\d{4}\s?\d{4}\s?\d{4}\b|\b\d{12}\b')
        if isinstance(data, dict):
            for k, v in data.items():
                data[k] = self._recursive_mask(v)
        elif isinstance(data, list):
            data = [self._recursive_mask(item) for item in data]
        elif isinstance(data, str):
            return aadhaar_pattern.sub("[Aadhaar Redacted]", data)
        return data

    def _mask_pii(self, payload: dict) -> dict:
        """
        Aggressively masks sensitive identifiers (e.g. 12-digit Aadhaar) before hashing.
        Ensures DPDP Act compliance.
        """
        masked = copy.deepcopy(payload)
        return self._recursive_mask(masked)

    def commit_audit_event(self, event_type: str, payload: dict) -> str:
        previous_hash = self._ledger[-1]["current_hash"]
        timestamp = datetime.utcnow().isoformat()
        
        masked_payload = self._mask_pii(payload)
        payload_str = json.dumps(masked_payload, sort_keys=True)
        
        # SHA-256 Hash Chain computation
        raw_string = f"{previous_hash}{timestamp}{payload_str}"
        current_hash = hashlib.sha256(raw_string.encode('utf-8')).hexdigest()
        
        self._ledger.append({
            "event_type": event_type,
            "payload": masked_payload,
            "timestamp": timestamp,
            "previous_hash": previous_hash,
            "current_hash": current_hash
        })
        
        return current_hash
