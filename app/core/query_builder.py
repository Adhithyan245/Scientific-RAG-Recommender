from app.schemas import RecommendationRequest

class QueryBuilder:
    def build_query(self, request: RecommendationRequest) -> str:
        parts = [
            f"Research Objective: {request.research_objective}",
            f"Sample Type: {request.sample_type}",
            f"Domain: {request.domain}"
        ]
        if request.sensitivity:
            parts.append(f"Sensitivity Requirement: {request.sensitivity}")
        if request.resolution:
            parts.append(f"Resolution Requirement: {request.resolution}")
        if request.constraints:
            parts.append(f"Constraints: {request.constraints}")
            
        return "\n".join(parts)
