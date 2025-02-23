def calculate_match_score(user_profile, candidate_profile):
    """
    Computes a compatibility score between two users based on their profiles.
    """
    score = 0

    # ✅ Ensure we use User objects correctly
    user = user_profile.user
    candidate = candidate_profile.user

    user_gender_pref = user_profile.gender_preference or "Any"
    user_age_min = user_profile.age_preference_min or 18
    user_age_max = user_profile.age_preference_max or 99
    user_interests = set(user_profile.interests.split(',')) if user_profile.interests else set()
    user_health_goals = user_profile.health_goals or ""

    candidate_gender = candidate_profile.gender or "Other"
    candidate_age = candidate_profile.age or 0
    candidate_interests = set(candidate_profile.interests.split(',')) if candidate_profile.interests else set()
    candidate_health_goals = candidate_profile.health_goals or ""

    # ✅ Gender preference check
    if user_gender_pref == "Any" or user_gender_pref == candidate_gender:
        score += 10

    # ✅ Age preference check
    if user_age_min <= candidate_age <= user_age_max:
        score += 10

    # ✅ Common interests boost
    common_interests = user_interests & candidate_interests
    score += len(common_interests) * 10

    # ✅ Health goals match boost
    if user_health_goals == candidate_health_goals:
        score += 20

    return min(score, 100)  # ✅ Ensure score does not exceed 100

def find_best_matches(user):
    from dating_app.models import Profile  # ✅ Lazy import to avoid circular dependencies

    """
    Returns a list of best-matching candidates for the given user.
    """
    try:
        user_profile = Profile.objects.get(user=user)  # ✅ Retrieve the user’s profile
    except Profile.DoesNotExist:
        return []  # Return empty list if no profile exists

    # ✅ Fix: Exclude the user's **User instance**, not the Profile instance
    candidates = Profile.objects.exclude(user=user)

    matches = []
    for candidate_profile in candidates:
        match_score = calculate_match_score(user_profile, candidate_profile)
        if match_score > 50:
            matches.append({'user': candidate_profile.user, 'score': match_score})  # ✅ Return User instance

    matches.sort(key=lambda x: x['score'], reverse=True)  # ✅ Sort from highest to lowest score
    return matches
