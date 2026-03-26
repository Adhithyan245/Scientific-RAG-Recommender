import json
from typing import List, Dict, Any, Optional
from app.schemas import RecommendationResponse, RecommendationItem

class ResponseFormatter:
    def format(self, reasoner_output: dict, confidence: float, explanation: str, warnings: list, retrieved: list, debug: bool = False) -> dict:
        alts = ["XRD", "SEM", "FTIR", "TEM"]
        
        # Safely extract dict values handling potential None values
        reasoner_output = reasoner_output or {}
        top_inst = reasoner_output.get("instrument") or "Unknown"
        reasoning = reasoner_output.get("reasoning") or "Based on retrieval."
        limitations = reasoner_output.get("limitations") or "See warnings for constraints."
        
        # Determine actual alternatives safely
        if top_inst in alts:
            alts.remove(top_inst)
            
        inst_scores = {}
        retrieved = retrieved or []
        for c in retrieved:
            # Safely handle missing c dict fields
            inst = c.get('instrument', 'Unknown')
            dist = c.get('distance', 1.0)
            score = max(0.0, 1.0 - (dist / 2.0))
            if inst not in inst_scores:
                inst_scores[inst] = score
            else:
                inst_scores[inst] = max(inst_scores[inst], score)
                
        if top_inst not in inst_scores and top_inst != "Unknown":
            inst_scores[top_inst] = 0.9
            
        for a in alts:
            if a not in inst_scores:
                inst_scores[a] = 0.5
                
        warnings = warnings or []
        for w in warnings:
            if not isinstance(w, str): continue
            w_lower = w.lower()
            if "xrd" in w_lower and "XRD" in inst_scores: inst_scores["XRD"] *= 0.8
            if "sem" in w_lower and "SEM" in inst_scores: inst_scores["SEM"] *= 0.8
            if "ftir" in w_lower and "FTIR" in inst_scores: inst_scores["FTIR"] *= 0.8
            if "tem" in w_lower and "TEM" in inst_scores: inst_scores["TEM"] *= 0.8
            
        sorted_insts = sorted(inst_scores.items(), key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for i, (inst, score) in enumerate(sorted_insts[:3]):
            if i == 0:
                item = RecommendationItem(
                    instrument=str(inst) if top_inst == "Unknown" else str(top_inst),
                    reasoning=str(reasoning),
                    alternatives=[str(x[0]) for x in sorted_insts[1:3]],
                    limitations=str(limitations),
                    score=round(float(max(0.1, score)), 2)
                )
            else:
                item = RecommendationItem(
                    instrument=str(inst),
                    reasoning=f"Alternative option based on partial match. Score: {round(float(score), 2)}",
                    alternatives=[],
                    limitations="May not fully meet all constraints. Please check warnings.",
                    score=round(float(max(0.1, score)), 2)
                )
            recommendations.append(item)
            
        if not recommendations:
             recommendations.append(RecommendationItem(
                instrument=str(top_inst),
                reasoning=str(reasoning),
                alternatives=[],
                limitations=str(limitations),
                score=round(float(confidence), 2)
            ))
            
        response_dict = {
            "recommendations": [r.model_dump() for r in recommendations],
            "confidence": round(float(confidence), 2),
            "confidence_explanation": str(explanation or ""),
            "warnings": [str(w) for w in warnings],
            "debug_info": None
        }
        
        if debug:
            response_dict["debug_info"] = {
                "retrieved_chunks": retrieved,
                "scores": inst_scores
            }
            
        return response_dict
