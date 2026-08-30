from typing import List, Dict, Any

class CollusionEngine:
    def __init__(self, bidders: List[Dict[str, Any]]):
        self.bidders = bidders
        self.disclaimer = "This is a heuristic signal of potential cartelization requiring Officer investigation, not a deterministic finding of collusion."

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

                # If any evidence found, create a lead
                if evidence:
                    lead_type_str = "_AND_".join(lead_types)
                    investigative_leads.append({
                        "lead_type": lead_type_str,
                        "bidders_involved": [bidder_a["id"], bidder_b["id"]],
                        "evidence": evidence,
                        "disclaimer": self.disclaimer
                    })

        return {
            "status": "ANALYSIS_COMPLETE",
            "investigative_leads": investigative_leads
        }
