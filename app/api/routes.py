from fastapi import APIRouter
from app.schemas import RecommendationRequest, RecommendationResponse
from app.core.query_builder import QueryBuilder
from app.core.retriever import Retriever
from app.core.rule_engine import RuleEngine
from app.core.reasoner import Reasoner
from app.core.confidence import ConfidenceCalculator
from app.core.response_formatter import ResponseFormatter

router = APIRouter()

retriever = Retriever()
reasoner = Reasoner()
query_builder = QueryBuilder()
rule_engine = RuleEngine()
confidence_calc = ConfidenceCalculator()
formatter = ResponseFormatter()

@router.post("/recommend", response_model=RecommendationResponse)
def recommend_instrument(request: RecommendationRequest):
    try:
        semantic_query = query_builder.build_query(request)
        retrieved = Retriever().retrieve(semantic_query, top_k=3)
        warnings = rule_engine.evaluate(request)
        
        if retrieved:
            context_text = "\n\n".join([f"({c.get('instrument', 'Unknown')}) {c.get('chunk', '')}" for c in retrieved])
        else:
            context_text = "No literature found."
            
        reasoner_output = reasoner.generate_reasoning(semantic_query, context_text)
        confidence, explanation = confidence_calc.calculate(retrieved, warnings, request)
        
        result = formatter.format(
            reasoner_output=reasoner_output,
            confidence=confidence,
            explanation=explanation,
            warnings=warnings,
            retrieved=retrieved,
            debug=request.debug
        )
        return result
        
    except Exception as e:
        print(f"API Error POST /recommend: {e}")
        # Defensive fallback response guaranteeing schema compliance regardless of internal crash severity
        return {
            "recommendations": [{
                "instrument": "System Error",
                "reasoning": "A runtime error occurred processing your request. Please try modifying constraints.",
                "alternatives": [],
                "limitations": "API inference failed.",
                "score": 0.0
            }],
            "confidence": 0.0,
            "confidence_explanation": f"API explicitly failed with an internal exception.",
            "warnings": ["CRITICAL: Internal Server Error returned safe payload schema."],
            "debug_info": {"error": str(e)} if request.debug else None
        }

@router.get("/health")
def health_check():
    return {"status": "healthy"}
