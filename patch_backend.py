import os
import sys

ROOT = r'C:\Users\Suhaas\.gemini\antigravity\scratch\gem_compliance'

# 1. Update graph_engine.py
f = os.path.join(ROOT, 'backend', 'graph_engine.py')
with open(f, 'r', encoding='utf-8') as file:
    content = file.read()

theta_old = '''        # 3. Theta Case: Time-Travel Temporal Validation
        debarment = self.bidder.get("debarment_mock", {})
        if debarment and debarment.get("start") and debarment.get("end"):
            tender_closing_date = "2025-12-01"
            # Simple string comparison works for YYYY-MM-DD
            if debarment.get("start") <= tender_closing_date <= debarment.get("end"):
                status = "NEEDS_REVIEW"
                conflict = {
                    "contradiction_id": f"conflict-debarment-{self.bidder['id']}",
                    "claim": "Current Status: CLEAN (as of Aug 2026)",
                    "evidence": f"Debarment active from {debarment.get('start')} to {debarment.get('end')}",
                    "ai_synthesis": f"Temporal Policy Violation: While the bidder is currently not debarred, they were actively blacklisted during the Tender Closing Date ({tender_closing_date})."
                }
                self.contradictions.append(conflict)'''

theta_new = '''        # 3. Theta Case: Time-Travel Temporal Validation
        debarment = self.bidder.get("debarment_mock", {})
        tender_closing_date = "2025-12-01"
        historical = debarment.get("historical_records", [])
        for rec in historical:
            rec_start = rec.get("start_date", "")
            rec_end = rec.get("end_date", "")
            if rec_start and rec_end and rec_start <= tender_closing_date <= rec_end:
                status = "NEEDS_REVIEW"
                conflict = {
                    "contradiction_id": f"conflict-debarment-{self.bidder['id']}",
                    "claim": "Current Status: CLEAN (as of Aug 2026)",
                    "evidence": f"Debarment active from {rec_start} to {rec_end}",
                    "ai_synthesis": f"Temporal Policy Violation: While the bidder is currently not debarred, they were actively blacklisted during the Tender Closing Date ({tender_closing_date})."
                }
                self.contradictions.append(conflict)'''

if theta_old in content:
    content = content.replace(theta_old, theta_new)
else:
    print('theta_old not found')

filters_old = '''        return {
            "status": status,
            "contradictions": self.contradictions
        }'''
filters_new = '''        # Update hard filters based on actual bidder data
        vigilance = self.bidder.get("vigilance_mock", {})
        debarment_check = self.bidder.get("debarment_mock", {})
        if debarment_check.get("is_debarred_currently", False):
            self.hard_filters["not_debarred"] = "FAIL"
            status = "NEEDS_REVIEW"
        gstn_check = self.bidder.get("gstn_mock", {})
        if gstn_check and not gstn_check.get("status", "ACTIVE") == "ACTIVE":
            self.hard_filters["gst_active"] = "FAIL"

        return {
            "status": status,
            "contradictions": self.contradictions
        }'''
if filters_old in content:
    content = content.replace(filters_old, filters_new)
else:
    print('filters_old not found')

with open(f, 'w', encoding='utf-8') as file:
    file.write(content)

# 2. Update collusion_engine.py
f = os.path.join(ROOT, 'backend', 'collusion_engine.py')
with open(f, 'r', encoding='utf-8') as file:
    content = file.read()

jaccard_method = '''
    def _jaccard_similarity(self, dict_a: dict, dict_b: dict) -> float:
        keys = set(dict_a.keys()) | set(dict_b.keys())
        numeric_keys = [k for k in keys if isinstance(dict_a.get(k), (int, float)) or isinstance(dict_b.get(k), (int, float))]
        if not numeric_keys:
            return 0.0
        matches = 0
        for k in numeric_keys:
            va = dict_a.get(k)
            vb = dict_b.get(k)
            if va is not None and vb is not None:
                if abs(float(va) - float(vb)) / max(abs(float(va)), abs(float(vb)), 1) < 0.05:
                    matches += 1
        return round(matches / len(numeric_keys), 3)
'''
if '_jaccard_similarity' not in content:
    content = content.replace('    def analyze_collusion(', jaccard_method + '\n    def analyze_collusion(')

analyze_old = '''                # If any evidence found, create a lead
                if evidence:
                    lead_type_str = "_AND_".join(lead_types)
                    investigative_leads.append({
                        "lead_type": lead_type_str,
                        "bidders_involved": [bidder_a["id"], bidder_b["id"]],
                        "evidence": evidence,
                        "disclaimer": self.disclaimer
                    })'''

analyze_new = '''                # 3. Jaccard similarity on numeric claims
                claims_a = bidder_a.get("claims", {})
                claims_b = bidder_b.get("claims", {})
                jaccard = self._jaccard_similarity(claims_a, claims_b)
                if jaccard >= 0.70:
                    lead_types.append("HIGH_JACCARD_SIMILARITY")
                    evidence.append(f"Bid values suspiciously similar: Jaccard similarity score {jaccard:.0%}. Turnover, local content, and subcontracting claims are nearly identical.")

                # 4. IP/Network overlap
                ip_a = bidder_a.get("submission_metadata", {}).get("ip_address", "")
                ip_b = bidder_b.get("submission_metadata", {}).get("ip_address", "")
                if ip_a and ip_b and ip_a == ip_b:
                    lead_types.append("SHARED_IP_ADDRESS")
                    evidence.append(f"[SIMULATED DEMO DATA] Both bidders submitted from the same IP address ({ip_a}). In a real deployment, this would indicate shared network origin.")

                # If any evidence found, create a lead
                if evidence:
                    lead_type_str = "_AND_".join(lead_types)
                    investigative_leads.append({
                        "lead_type": lead_type_str,
                        "bidders_involved": [bidder_a["id"], bidder_b["id"]],
                        "bidder_names": [bidder_a.get("name", bidder_a["id"]), bidder_b.get("name", bidder_b["id"])],
                        "jaccard_score": jaccard,
                        "evidence": evidence,
                        "disclaimer": self.disclaimer
                    })'''
if 'jaccard_score' not in content:
    content = content.replace(analyze_old, analyze_new)
else:
    print('jaccard_score found in content')

extra_methods = '''    def get_metadata_clusters(self, bidders_with_pdfs: List[Dict]) -> List[Dict]:
        author_groups: Dict[str, List[str]] = {}
        for b in bidders_with_pdfs:
            meta = b.get("pdf_metadata", {})
            author = meta.get("author", "UNKNOWN")
            if author and author != "UNKNOWN":
                author_groups.setdefault(author, []).append(b["name"])
        clusters = []
        for author, names in author_groups.items():
            if len(names) >= 2:
                clusters.append({
                    "cluster_type": "SHARED_PDF_AUTHOR",
                    "author": author,
                    "bidders": names,
                    "count": len(names),
                    "risk_level": "HIGH" if len(names) >= 3 else "MEDIUM",
                    "label": "SUSPICIOUS INDICATOR - REQUIRES INVESTIGATION",
                    "note": "Same PDF author metadata may indicate shared document preparation."
                })
        return clusters

    def get_ip_clusters(self, bidders: List[Dict]) -> List[Dict]:
        ip_groups: Dict[str, List[str]] = {}
        for b in bidders:
            ip = b.get("submission_metadata", {}).get("ip_address", "")
            if ip:
                ip_groups.setdefault(ip, []).append(b.get("name", b["id"]))
        clusters = []
        for ip, names in ip_groups.items():
            if len(names) >= 2:
                subnet = ".".join(ip.split(".")[:3]) + ".x"
                clusters.append({
                    "cluster_type": "SHARED_IP_ADDRESS",
                    "ip_address": ip,
                    "subnet": subnet,
                    "bidders": names,
                    "count": len(names),
                    "risk_level": "HIGH" if len(names) >= 3 else "MEDIUM",
                    "label": "SIMULATED / DEMONSTRATION DATA",
                    "note": "IP address overlap does not prove collusion."
                })
        return clusters
'''
if 'get_ip_clusters' not in content:
    content = content + "\n" + extra_methods

with open(f, 'w', encoding='utf-8') as file:
    file.write(content)

print('Patching done.')
