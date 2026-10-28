from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models import User


def discover_users(
    db: Session,
    current_user: User,
    page: int = 1,
    page_size: int = 10,
) -> dict:
    # Load the current user's languages and interests.
    db.refresh(current_user)

    my_languages = {language.id: language.name for language in current_user.languages}
    my_interests = {interest.id: interest.name for interest in current_user.interests}

    # Find users in the same city, excluding the current user.
    query = (
        select(User)
        .options(
            selectinload(User.languages),
            selectinload(User.interests),
        )
        .where(
            User.id != current_user.id,
            User.current_city.is_not(None),
            User.current_city == current_user.current_city,
        )
    )

    candidates = db.scalars(query).all()

    results = []

    for candidate in candidates:
        candidate_languages = {
            language.id: language.name
            for language in candidate.languages
        }

        candidate_interests = {
            interest.id: interest.name
            for interest in candidate.interests
        }

        shared_language_ids = (
            set(my_languages) & set(candidate_languages)
        )

        shared_interest_ids = (
            set(my_interests) & set(candidate_interests)
        )

        shared_languages = sorted(
            my_languages[language_id]
            for language_id in shared_language_ids
        )

        shared_interests = sorted(
            my_interests[interest_id]
            for interest_id in shared_interest_ids
        )

        language_score = (
            40 * len(shared_language_ids) / len(my_languages)
            if my_languages
            else 0
        )

        interest_score = (
            40 * len(shared_interest_ids) / len(my_interests)
            if my_interests
            else 0
        )

        regional_score = (
            20
            if (
                current_user.home_region
                and candidate.home_region
                and current_user.home_region.casefold()
                == candidate.home_region.casefold()
            )
            else 0
        )

        match_score = round(
            language_score + interest_score + regional_score,
            2,
        )

        results.append(
            {
                "user_id": candidate.id,
                "username": candidate.username,
                "home_region": candidate.home_region,
                "current_city": candidate.current_city,
                "bio": candidate.bio,
                "shared_languages": shared_languages,
                "shared_interests": shared_interests,
                "match_score": match_score,
            }
        )

    # Sort by highest score, then username for deterministic ties.
    results.sort(
        key=lambda result: (
            -result["match_score"],
            result["username"].casefold(),
            result["user_id"],
        )
    )

    total = len(results)

    start = (page - 1) * page_size
    end = start + page_size

    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "results": results[start:end],
    }