# Mathmaking algorithm based on preferences 
def calculate_match_score(user, candidate):
    """
    Computes a compatibility score between two users.
    """
    score = 0
    if user.gender_preference == candidate.gender:
        score += 10
    if user.age_preference_min <= candidate.age <= user.age_preference_max:
        score += 10
    if user.interests and candidate.interests:
        common_interests = set(user.interests.split(',')) & set(candidate.interests.split(','))
        score += len(common_interests) * 10
    if user.health_goals == candidate.health_goals:
        score += 20
    return min(score, 100)

def find_best_matches(user):
    from dating_app.models import UserProfile  # Lazy import
    """
    Returns a list of best-matching candidates for the given user.
    """
    candidates = UserProfile.objects.exclude(id=user.id)
    matches = []
    for candidate in candidates:
        match_score = calculate_match_score(user, candidate)
        if match_score > 50:
            matches.append({'user': candidate, 'score': match_score})
    matches.sort(key=lambda x: x['score'], reverse=True)
    return matches