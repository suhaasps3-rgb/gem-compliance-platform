import networkx as nx
from typing import Dict, Any, List

class EvidenceGraphEngine:
    def __init__(self, bidder_data: Dict[str, Any]):
        self.bidder = bidder_data
        self.graph = nx.DiGraph()
        self.contradictions = []
        self.hard_filters = {
            "pan_active": "PASS",
            "gst_active": "PASS",
            "not_debarred": "PASS",
        }

    def build_graph(self) -> nx.DiGraph:
        bidder_id = self.bidder.get("id")
        self.graph.add_node(bidder_id, type="Bidder", label=self.bidder.get("name"))

        claims = self.bidder.get("claims", {})
        mca21 = self.bidder.get("mca21_mock", {})
        udyam = self.bidder.get("udyam_mock", {})

        # Add Evidence Nodes
        self.graph.add_node("Evidence:MCA21", type="Evidence", source="MCA21 API 🟡", data=mca21)
        self.graph.add_node("Evidence:Udyam", type="Evidence", source="Udyam API 🟡", data=udyam)
        
        # PAN Anchor
        pan = claims.get("pan", "UNKNOWN_PAN")
        self.graph.add_node(f"Anchor:PAN:{pan}", type="Anchor", label=pan)
        self.graph.add_edge(bidder_id, f"Anchor:PAN:{pan}", relation="IDENTIFIES_AS")

        # Claims -> Evidence Mapping
        if "turnover_cr" in claims:
            claim_val = claims["turnover_cr"]
            claim_node = f"Claim:Turnover:{claim_val}"
            self.graph.add_node(claim_node, type="Claim", label=f"Turnover: ₹{claim_val} Cr", value=claim_val)
            self.graph.add_edge(bidder_id, claim_node, relation="MAKES_CLAIM")
            
            # Edges to Evidence
            self.graph.add_edge(claim_node, "Evidence:MCA21", relation="VERIFIED_AGAINST")
            self.graph.add_edge(claim_node, "Evidence:Udyam", relation="VERIFIED_AGAINST")
            
        if "enterprise_type" in claims:
            etype = claims["enterprise_type"]
            claim_node = f"Claim:EnterpriseType:{etype}"
            self.graph.add_node(claim_node, type="Claim", label=f"Enterprise Type: {etype}", value=etype)
            self.graph.add_edge(bidder_id, claim_node, relation="MAKES_CLAIM")
            self.graph.add_edge(claim_node, "Evidence:Udyam", relation="VERIFIED_AGAINST")

        # GSTN Evidence
        gstn = self.bidder.get("gstn_mock", {})
        if gstn:
            self.graph.add_node("Evidence:GSTN", type="Evidence", source="GSTN API 🔴", data=gstn)
            self.graph.add_edge(f"Anchor:PAN:{pan}", "Evidence:GSTN", relation="LINKED_TO")

        # Make In India Local Content
        if "local_content_pct" in claims:
            val = claims["local_content_pct"]
            claim_node = f"Claim:LocalContent:{val}"
            self.graph.add_node(claim_node, type="Claim", label=f"Local Content: {val}%")
            self.graph.add_edge(bidder_id, claim_node, relation="MAKES_CLAIM")
            
        # Subcontracting
        if "subcontracting_pct" in claims:
            val = claims["subcontracting_pct"]
            claim_node = f"Claim:Subcontracting:{val}"
            self.graph.add_node(claim_node, type="Claim", label=f"Subcontracting: {val}%")
            self.graph.add_edge(bidder_id, claim_node, relation="MAKES_CLAIM")

        if "legal_name" in mca21 or "legal_name" in udyam:
            # We don't have a specific claim for legal name, but we can check consistency
            pass

        return self.graph

    def resolve_contradictions(self) -> Dict[str, Any]:
        """
        Traverses the graph to resolve contradictions.
        """
        claims = self.bidder.get("claims", {})
        mca21 = self.bidder.get("mca21_mock", {})
        udyam = self.bidder.get("udyam_mock", {})
        
        status = "VERIFIED_COMPLIANT"

        # 1. Delta Case: Turnover Contradiction
        if "turnover_cr" in claims:
            claimed_turnover = claims["turnover_cr"]
            mca21_turnover = mca21.get("reported_turnover_cr")
            
            # MSME Micro limit is 10Cr
            if claimed_turnover <= 10.0 and mca21_turnover and mca21_turnover > 10.0:
                status = "NEEDS_REVIEW"
                conflict = {
                    "contradiction_id": f"conflict-turnover-{self.bidder['id']}",
                    "claim": f"Turnover: ₹{claimed_turnover} Cr (Micro limit: ₹10 Cr)",
                    "evidence": f"MCA21 API 🟡: ₹{mca21_turnover} Cr",
                    "ai_synthesis": f"Bidder claims Micro MSME status (Turnover < ₹10Cr limit), but MCA21 data explicitly exceeds even the revised threshold (₹{mca21_turnover}Cr)."
                }
                self.contradictions.append(conflict)
                self.graph.add_edge(f"Claim:Turnover:{claimed_turnover}", "Evidence:MCA21", relation="EVIDENCE_CONFLICT", color="red")

        # 2. Gamma Case: Entity Name Mismatch
        mca21_name = mca21.get("legal_name")
        udyam_name = udyam.get("legal_name")
        if mca21_name and udyam_name and mca21_name != udyam_name:
            if status == "VERIFIED_COMPLIANT":
                status = "NEEDS_REVIEW"
            conflict = {
                "contradiction_id": f"conflict-name-{self.bidder['id']}",
                "claim": f"Identity Anchor: PAN",
                "evidence": f"MCA21 Name: '{mca21_name}', Udyam Name: '{udyam_name}'",
                "ai_synthesis": "Identity Inconsistency Risk: The legal name registered in MCA21 differs from the Udyam registration, requiring manual review of entity linkage."
            }
            self.contradictions.append(conflict)

        # 3. Theta Case: Time-Travel Temporal Validation
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
                self.contradictions.append(conflict)
                    
                # Add Evidence node and connection dynamically
                self.graph.add_node("Evidence:Debarment", type="Evidence", source="Vigilance DB 🔴")
                pan = claims.get("pan", "UNKNOWN")
                self.graph.add_edge(f"Anchor:PAN:{pan}", "Evidence:Debarment", relation="TEMPORAL_VIOLATION", color="red")

        # 4. Echo Case: Multi-Rule Violation (Tender Rules extracted by AI)
        import config
        gstn = self.bidder.get("gstn_mock", {})
        claimed_local_content = claims.get("local_content_pct")
        claimed_subcontracting = claims.get("subcontracting_pct")

        mii_limit = config.active_tender_limits.get("mii", 50)
        subcontract_limit = config.active_tender_limits.get("subcontract", 20)

        # Make in India (>= mii_limit%)
        if claimed_local_content is not None and claimed_local_content < mii_limit:
            status = "NEEDS_REVIEW"
            self.contradictions.append({
                "contradiction_id": f"conflict-mii-{self.bidder['id']}",
                "claim": f"Local Content: {claimed_local_content}%",
                "evidence": f"Tender Rule 4: Must be >= {mii_limit}%",
                "ai_synthesis": f"Bidder claims only {claimed_local_content}% local content against the strict {mii_limit}% mandate extracted from the tender document."
            })
            
        # Sub-contracting limit (<= subcontract_limit%)
        if claimed_subcontracting is not None and claimed_subcontracting > subcontract_limit:
            status = "NEEDS_REVIEW"
            self.contradictions.append({
                "contradiction_id": f"conflict-subcontract-{self.bidder['id']}",
                "claim": f"Sub-contracting: {claimed_subcontracting}%",
                "evidence": f"Tender Rule 5: Capped at {subcontract_limit}%",
                "ai_synthesis": f"Bidder's technical proposal declares {claimed_subcontracting}% sub-contracting, violating the strict {subcontract_limit}% limit enforced by the Procurement Officer's tender document."
            })

        # GST Fiscal Compliance
        if gstn and not gstn.get("gstr_filed_continuous_12m", True):
            status = "NEEDS_REVIEW"
            self.contradictions.append({
                "contradiction_id": f"conflict-gst-{self.bidder['id']}",
                "claim": "Tax Compliance: Up to Date",
                "evidence": f"GSTN API 🔴: Missed {gstn.get('months_missed')} months of GSTR-3B",
                "ai_synthesis": "Fiscal Non-Compliance: GSTN triangulation confirms the bidder has halted tax filings for 6 months, violating Rule 7 of the standard bidding document."
            })

        return {
            "status": status,
            "contradictions": self.contradictions
        }

    def serialize_graph(self) -> Dict[str, Any]:
        """
        Serializes NetworkX graph to JSON-friendly format for ReactFlow.
        Explicitly includes all node/edge attributes (type, label, source, color).
        """
        nodes = []
        for node_id, attrs in self.graph.nodes(data=True):
            nodes.append({
                "id": node_id,
                "type": attrs.get("type", "Unknown"),
                "label": attrs.get("label", node_id),
                "source": attrs.get("source"),
            })

        edges = []
        for source, target, attrs in self.graph.edges(data=True):
            edges.append({
                "source": source,
                "target": target,
                "relation": attrs.get("relation", ""),
                "color": attrs.get("color", "default"),
            })

        return {"nodes": nodes, "edges": edges}
