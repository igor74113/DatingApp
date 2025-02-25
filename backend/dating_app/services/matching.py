# Custom weights for different health preferences
WEIGHTS = {
    "diet": 25,  # More impact if diet aligns
    "exercise": 20,  
    "sleep": 15,  
    "goal": 40  # Lifestyle goal alignment is most important
}

def calculate_match_score(user_profile, candidate_profile):
    """
    Computes a compatibility score between two users based on health habits & preferences.
    """
    score = 0

    # ✅ Ensure user objects are correctly accessed
    user = user_profile.user
    candidate = candidate_profile.user

    # ✅ Extract user preferences
    user_age_min = user_profile.age_preference_min or 18
    user_age_max = user_profile.age_preference_max or 99
    user_gender_pref = user_profile.gender_preference or "Any"

    candidate_age = candidate_profile.age or 0
    candidate_gender = candidate_profile.gender or "Other"

    # ✅ Age preference check
    if user_age_min <= candidate_age <= user_age_max:
        score += 20  # More weight for being within the preferred age range

    # ✅ Gender preference check
    if user_gender_pref == "Any" or user_gender_pref == candidate_gender:
        score += 20

    # ✅ Health habit-based matching
    user_diet = user_profile.diet
    user_exercise = user_profile.exercise_routine
    user_sleep = user_profile.sleep_schedule
    user_goal = user_profile.lifestyle_goal

    candidate_diet = candidate_profile.diet
    candidate_exercise = candidate_profile.exercise_routine
    candidate_sleep = candidate_profile.sleep_schedule
    candidate_goal = candidate_profile.lifestyle_goal

    if user_diet and candidate_diet and user_diet == candidate_diet:
        score += 15  

    if user_exercise and candidate_exercise and user_exercise == candidate_exercise:
        score += 15  

    if user_sleep and candidate_sleep and user_sleep == candidate_sleep:
        score += 10  

    if user_goal and candidate_goal and user_goal == candidate_goal:
        score += 20  

    return min(score, 100)

def find_best_matches(user):
    from dating_app.models import Profile  # Lazy import

    # ✅ Ensure user has a profile, otherwise create one
    user_profile, created = Profile.objects.get_or_create(user=user)

    # ✅ Exclude self and filter based on age preferences
    candidates = Profile.objects.exclude(id=user_profile.id).filter(
        age__gte=user_profile.age_preference_min,
        age__lte=user_profile.age_preference_max
    )

    matches = []
    for candidate in candidates:
        if candidate and user_profile:
            match_score = calculate_match_score(user_profile, candidate)
            if match_score > 50:  # Only show relevant matches
                matches.append({'user': candidate.user, 'score': match_score})

    matches.sort(key=lambda x: x['score'], reverse=True)

    return matches
