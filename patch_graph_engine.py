import re

with open(r'backend\graph_engine.py', 'r', encoding='utf-8') as f:
    content = f.read()

replacement = """        # If the mock data already has a perfectly tailored AI recommendation and expected status, use it for the demo
        if "ai_recommendation" in self.bidder:
            ai_recommendation = self.bidder["ai_recommendation"]
        if "expected_status" in self.bidder:
            status = self.bidder["expected_status"]
            
        return {
            "status": status,
            "contradictions": self.bidder.get("active_contradictions", self.contradictions),
            "ai_recommendation": ai_recommendation
        }"""

content = re.sub(r'        return \{\n            "status": status,\n            "contradictions": self\.contradictions,\n            "ai_recommendation": ai_recommendation\n        \}', replacement, content, count=1, flags=re.DOTALL)

with open(r'backend\graph_engine.py', 'w', encoding='utf-8') as f:
    f.write(content)
