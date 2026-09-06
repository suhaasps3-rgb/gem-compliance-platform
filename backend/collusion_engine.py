from typing import List, Dict, Any

class CollusionEngine:
    def __init__(self, bidders: List[Dict[str, Any]]):
        self.bidders = bidders
        self.disclaimer = "This is a heuristic signal of potential cartelization requiring Officer investigation, not a deterministic finding of collusion."


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

    def analyze_collusion(self, tender_id: str) -> Dict[str, Any]:
        investigative_leads = []
        num_bidders = len(self.bidders)

        for i in range(num_bidders):
            for j in range(i + 1, num_bidders):
                bidder_a = self.bidders[i]
                bidder_b = self.bidders[j]

                evidence = []
                lead_types = []

                # 1. Check Shared Directors (MCA21)
                directors_a = set(bidder_a.get("mca21_mock", {}).get("active_directors", []))
                directors_b = set(bidder_b.get("mca21_mock", {}).get("active_directors", []))
                shared_directors = directors_a.intersection(directors_b)
                
                if shared_directors:
                    lead_types.append("SHARED_DIRECTOR")
                    for d in shared_directors:
                        evidence.append(f"Director {d} appears in MCA21 records for both entities.")

                # 2. Check Identical PDF Metadata
                meta_a = bidder_a.get("pdf_metadata", {})
                meta_b = bidder_b.get("pdf_metadata", {})
                
                if meta_a and meta_b:
                    author_a = meta_a.get("author")
                    author_b = meta_b.get("author")
                    date_a = meta_a.get("creation_date")
                    date_b = meta_b.get("creation_date")
                    
                    if author_a and author_a == author_b and date_a and date_a == date_b:
                        lead_types.append("SHARED_METADATA")
                        evidence.append(f"Technical Bid PDFs share identical author metadata ({author_a}) and creation timestamp ({date_a}).")

                # 3. Jaccard similarity on numeric claims
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
                    })

        return {
            "status": "ANALYSIS_COMPLETE",
            "investigative_leads": investigative_leads
        }

    def get_metadata_clusters(self, bidders_with_pdfs: List[Dict]) -> List[Dict]:
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
