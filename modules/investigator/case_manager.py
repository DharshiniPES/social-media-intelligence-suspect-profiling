import json
import os

class CaseManager:
    @staticmethod
    def export_case(target_username, results, filename="case_report.json"):
        os.makedirs("reports", exist_ok=True)
        filepath = os.path.join("reports", filename)
        
        report = {
            "target": target_username,
            "matches": []
        }
        
        for r in results:
            report["matches"].append({
                "username": r["candidate"].username,
                "platform": r["candidate"].platform,
                "fusion_score": r["fusion_score"],
                "explanation": r["explanation"]
            })
            
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=4)
            
        return filepath