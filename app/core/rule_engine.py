from app.schemas import RecommendationRequest

class RuleEngine:
    def evaluate(self, request: RecommendationRequest) -> list:
        warnings = []
        sample = request.sample_type.lower()
        res = getattr(request, 'resolution', '') or ''
        res = res.lower()
        obj = request.research_objective.lower()
        sens = getattr(request, 'sensitivity', '') or ''
        sens = sens.lower()
        domain = request.domain.lower()
        constraints = getattr(request, 'constraints', '') or ''
        constraints = constraints.lower()
        
        # Rule 1: Sample type compatibility
        if "liquid" in sample or "gas" in sample:
            warnings.append("XRD, SEM, and TEM are generally incompatible with liquid or gas samples. Consider specialized cells.")
            
        # Rule 2: Destructive vs non-destructive constraint mismatch
        if "non-destructive" in constraints and ("fib" in obj or "cross-section" in obj):
            warnings.append("Requested non-destructive testing, but objective implies destructive preparation (e.g., FIB cross-section).")
            
        # Rule 3: Resolution requirement mismatch
        if "atomic" in res and "optical" in obj:
            warnings.append("Optical microscopy cannot achieve atomic resolution.")
        if "atomic" in res and "ftir" in obj:
            warnings.append("FTIR does not provide spatial resolution at the atomic level.")
            
        # Rule 4: Domain mismatch
        if "biological" in domain and "vacuum" in constraints:
            warnings.append("Biological samples may degrade in high vacuum unless properly fixed or cryo-preserved.")
            
        # Rule 5: Instrument limitation checks
        if "organic" in sample and ("xps" in obj or "xrd" in obj):
            warnings.append("Amorphous organic materials may only yield broad halos in standard XRD, lacking distinct phase peaks.")
            
        if "metal" in sample and "crystal" not in obj and "ftir" in obj:
            warnings.append("FTIR is not typically recommended for pure metallic samples as they reflect IR radiation.")
            
        if "volatile" in sample or "wet" in sample:
            warnings.append("SEM/TEM may be problematic for wet or volatile samples due to high vacuum requirements.")
            
        if "trace" in sens or "high" in sens:
            warnings.append("Trace elemental sensitivity might require mass spectrometry (ICP-MS) beyond standard configurations.")
            
        return warnings
