from app.schemas import RecommendationRequest

class ConfidenceCalculator:
    def calculate(self, retrieved_chunks: list, warnings: list, request: RecommendationRequest) -> tuple:
        base_confidence = 0.8
        explanation = "High confidence based on standard parameters."
        
        # Safely handle None inputs
        retrieved_chunks = retrieved_chunks or []
        warnings = warnings or []
        
        if not retrieved_chunks:
            return 0.1, "No context retrieved. Very low confidence."
            
        # Deduct for large average distances safely checking keys
        valid_distances = [c.get('distance', 1.0) for c in retrieved_chunks if isinstance(c, dict)]
        if valid_distances:
            avg_distance = sum(valid_distances) / len(valid_distances)
            if avg_distance > 1.5:
                base_confidence -= 0.15
                explanation = "Reduced confidence due to low similarity in retrieved context."
            elif avg_distance > 1.0:
                base_confidence -= 0.05
                
        # Deduct if few chunks
        if len(retrieved_chunks) < 2:
            base_confidence -= 0.1
            explanation = "Reduced confidence due to limited supporting chunks."
            
        # Deduct based on deterministic warnings
        if warnings:
            penalty = len(warnings) * 0.15
            base_confidence -= penalty
            explanation = f"Reduced confidence due to {len(warnings)} rule violations."
        
        # Deduct based on input completeness
        if not request.sensitivity or not request.resolution:
            base_confidence -= 0.05
            if "Reduced" not in explanation:
                explanation = "Confidence slightly lowered due to missing optional constraints."
                
        # Bound confidence strictly between 0.0 and 1.0
        final_score = max(0.0, min(1.0, base_confidence))
        
        if final_score >= 0.8:
            explanation = "Strong match with high confidence based on retrieved literature."
            
        return round(float(final_score), 2), str(explanation)
