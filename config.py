"""
Central Configuration File for Bioinformática Evaluation System
================================================================

This file contains all the contest/evaluation system variables and settings.
Update your student ID here and use this across all exercise testing.

API Documentation:
- Base URL: https://cpg3.der.usal.es/eval
- Operations: test, calificacion, ranking
- Response format: Python format (single quotes for strings in lists/dicts)
"""

# ============================================================================
# STUDENT CONFIGURATION (UPDATE THIS!)
# ============================================================================

STUDENT_ID = "Z2256773H"  # e.g., "70879303L"

# ============================================================================
# API CONFIGURATION
# ============================================================================

API_BASE_URL = "https://cpg3.der.usal.es/eval"
API_OPERATIONS = {
    'test': f"{API_BASE_URL}/test",
    'calificacion': f"{API_BASE_URL}/calificacion",
    'ranking': f"{API_BASE_URL}/ranking"
}

# ============================================================================
# EXERCISE MAPPING
# ============================================================================
# Maps folder names to session and exercise numbers
# Format: "folder_name": (session, exercise, description)

EXERCISE_MAP = {
    # TEMA 1
    "complementaria_tema1_eje1": (1, 1, "Complementaria"),
    "frecuencia_tema1_eje2": (1, 2, "Frecuencia"),
    "gccontent_tema1_eje3": (1, 3, "GC Content"),
    "skew_min_skew_tema1_eje4": (1, 4, "Skew Min Skew"),
    
    # TEMA 2
    "count_kmers_tema2_eje1": (2, 1, "Count K-mers"),
    "find_motif_tema2_eje2": (2, 2, "Find Motif"),
    "consensus_tema2_eje3": (2, 3, "Consensus"),
    "allMutations_tema2_eje4": (2, 4, "All Mutations"),
    "countKmersV2_tema2_eje5": (2, 5, "Count K-mers V2"),
    "motif_score_tema2_eje6": (2, 6, "Motif Score"),
    "profile_matrix_tema2_eje7": (2, 7, "Profile Matrix"),
    "motif_probability_tema2_eje8": (2, 8, "Motif Probability"),
    "most_probable_kmer_tema2_eje9": (2, 9, "Most Probable K-mer"),
    "greedy_motif_search_tema2_eje10": (2, 10, "Greedy Motif Search"),
    "gibbs_sampler_tema2_eje11": (2, 11, "Gibbs Sampler"),
    
    # TEMA 3
    "string_reconstruction_tema3_eje1": (3, 1, "String Reconstruction"),
    "contigs_tema3_eje2": (3, 2, "Contigs"),
    
    # TEMA 4
    "suffix_array_tema4_eje1": (4, 1, "Suffix Array"),
    "bwt_tema4_eje2": (4, 2, "Burrows-Wheeler Transform"),
    "ibwt_tema4_eje3": (4, 3, "Inverse BWT"),
    "bwmatching_tema4_eje4": (4, 4, "BW Matching"),
    "first_occurrence_tema4_eje5": (4, 5, "First Occurrence"),
    
    # TEMA 5
    "farthest_first_tema5_eje1": (5, 1, "Farthest First"),
    "mse_tema5_eje2": (5, 2, "MSE"),
    "lloyd_tema5_eje3": (5, 3, "Lloyd"),
    "hierarchical_tema5_eje4": (5, 4, "Hierarchical"),
    "annotations_tema5_eje5": (5, 5, "Annotations"),
    "functions_tema5_eje6": (5, 6, "Functions"),
    "enrichment_tema5_eje7": (5, 7, "Enrichment"),
    "enrichmentall_tema5_eje8": (5, 8, "Enrichment All"),
}

# ============================================================================
# RESPONSE FORMATTING RULES
# ============================================================================

FORMATTING_RULES = {
    'strings_in_collections': 'single_quotes',  # Use 'text' not "text"
    'decimal_places': 3,  # Round to 3 decimals
    'order_matters': False,  # Unless exercise specifies otherwise
}

# ============================================================================
# SCORING INFORMATION
# ============================================================================

SCORING_RULES = {
    'penalty_per_attempts': 3,  # -1 point every 3 attempts
    'minimum_score': 1,
    'first_solver_bonus': {
        2: 1,   # +1 bonus for 2-point exercises
        3: 2,   # +2 bonus for 3-5 point exercises
        4: 2,
        5: 2,
        6: 3,   # +3 bonus for 6+ point exercises
    }
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_exercise_info(folder_name):
    """
    Get session and exercise number from folder name.
    
    Args:
        folder_name (str): Name of the exercise folder
        
    Returns:
        tuple: (session, exercise, description) or None if not found
    """
    return EXERCISE_MAP.get(folder_name)

def format_response(response):
    """
    Format response according to API requirements.
    
    Args:
        response: Python object (str, int, float, list, dict)
        
    Returns:
        str: Properly formatted response string
    """
    if isinstance(response, str):
        return response
    elif isinstance(response, (int, float)):
        if isinstance(response, float):
            return str(round(response, FORMATTING_RULES['decimal_places']))
        return str(response)
    elif isinstance(response, list):
        # Format list with single quotes for strings
        formatted = []
        for item in response:
            if isinstance(item, str):
                formatted.append(f"'{item}'")
            else:
                formatted.append(str(item))
        return f"[{','.join(formatted)}]"
    elif isinstance(response, dict):
        # Format dict with single quotes for keys and string values
        formatted = []
        for key, value in response.items():
            key_str = f"'{key}'" if isinstance(key, str) else str(key)
            val_str = f"'{value}'" if isinstance(value, str) else str(value)
            formatted.append(f"{key_str}:{val_str}")
        return f"{{{','.join(formatted)}}}"
    else:
        return str(response)

def build_test_url(session, exercise, response, student_id=None):
    """
    Build the test URL for submitting an answer.
    
    Args:
        session (int): Session number
        exercise (int): Exercise number
        response: Your answer (will be formatted automatically)
        student_id (str): Student DNI (uses config default if not provided)
        
    Returns:
        str: Complete test URL
    """
    if student_id is None:
        student_id = STUDENT_ID
    
    formatted_response = format_response(response)
    
    return f"{API_OPERATIONS['test']}?session={session}&exercise={exercise}&response={formatted_response}&id={student_id}"

def build_calificacion_url(student_id=None):
    """
    Build the URL to check your score.
    
    Args:
        student_id (str): Student DNI (uses config default if not provided)
        
    Returns:
        str: Complete calificacion URL
    """
    if student_id is None:
        student_id = STUDENT_ID
    
    return f"{API_OPERATIONS['calificacion']}?id={student_id}"

def build_ranking_url(student_id=None):
    """
    Build the URL to check the ranking.
    
    Args:
        student_id (str): Student DNI (uses config default if not provided)
        
    Returns:
        str: Complete ranking URL
    """
    if student_id is None:
        student_id = STUDENT_ID
    
    return f"{API_OPERATIONS['ranking']}?id={student_id}"


# ============================================================================
# VALIDATION
# ============================================================================

def validate_config():
    """Check if configuration is properly set up."""
    issues = []
    
    if STUDENT_ID == "YOUR_DNI_HERE":
        issues.append("⚠️  STUDENT_ID not set! Update it in config.py")
    
    return issues

if __name__ == "__main__":
    print("Bioinformática Evaluation System - Configuration")
    print("=" * 60)
    print(f"Student ID: {STUDENT_ID}")
    print(f"API Base URL: {API_BASE_URL}")
    print(f"\nTotal exercises configured: {len(EXERCISE_MAP)}")
    
    issues = validate_config()
    if issues:
        print("\n⚠️  Configuration Issues:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✅ Configuration looks good!")
    
    print("\nExample URLs:")
    print(f"  Check score: {build_calificacion_url()}")
    print(f"  Check ranking: {build_ranking_url()}")
