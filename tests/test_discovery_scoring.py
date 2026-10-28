from app.models import User, Language, Interest
from app.services.discovery import discover_users


def test_discovery_ranks_better_matches_higher(db_session):
    # Create languages
    marathi = Language(name="Marathi")
    hindi = Language(name="Hindi")
    english = Language(name="English")

    db_session.add_all([marathi, hindi, english])

    # Create interests
    cricket = Interest(name="Cricket")
    trekking = Interest(name="Trekking")
    chess = Interest(name="Chess")

    db_session.add_all([cricket, trekking, chess])
    db_session.flush()

    # Current user
    current_user = User(
        username="currentuser",
        email="currentuser@example.com",
        password_hash="test_hash",
        home_region="Maharashtra",
        current_city="Chennai",
        bio="Current user",
    )

    # Strong match: same region, two shared languages,
    # and two shared interests
    strong_match = User(
        username="strongmatch",
        email="strongmatch@example.com",
        password_hash="test_hash",
        home_region="Maharashtra",
        current_city="Chennai",
    )

    # Weak match: different region, one shared language,
    # and one shared interest
    weak_match = User(
        username="weakmatch",
        email="weakmatch@example.com",
        password_hash="test_hash",
        home_region="Gujarat",
        current_city="Chennai",
    )

    # Different city: should not appear
    other_city = User(
        username="othercity",
        email="othercity@example.com",
        password_hash="test_hash",
        home_region="Maharashtra",
        current_city="Pune",
    )

    current_user.languages = [marathi, hindi, english]
    current_user.interests = [cricket, trekking, chess]

    strong_match.languages = [marathi, hindi]
    strong_match.interests = [cricket, trekking]

    weak_match.languages = [marathi]
    weak_match.interests = [cricket]

    other_city.languages = [marathi, hindi, english]
    other_city.interests = [cricket, trekking, chess]

    db_session.add_all([
        current_user,
        strong_match,
        weak_match,
        other_city,
    ])
    db_session.flush()

    # Run the discovery algorithm
    results = discover_users(
        db=db_session,
        current_user=current_user,
        page=1,
        page_size=10,
    )

    discovered_users = results["results"]

    # Verify users from other cities are excluded
    usernames = [user["username"] for user in discovered_users]

    assert "currentuser" not in usernames
    assert "othercity" not in usernames

    # Verify both Chennai users appear
    assert "strongmatch" in usernames
    assert "weakmatch" in usernames

    # Verify stronger matches rank first
    assert usernames.index("strongmatch") < usernames.index("weakmatch")

    # Verify scores are ordered from highest to lowest
    scores = [user["match_score"] for user in discovered_users]

    assert scores == sorted(scores, reverse=True)

    # Verify shared preferences are returned
    strong_result = next(
        user for user in discovered_users
        if user["username"] == "strongmatch"
    )

    assert set(strong_result["shared_languages"]) == {
        "Marathi",
        "Hindi",
    }

    assert set(strong_result["shared_interests"]) == {
        "Cricket",
        "Trekking",
    }

    assert strong_result["match_score"] == 73.33


def test_discovery_pagination_returns_correct_page(db_session):
    language = Language(name="PaginationTestLanguage")
    interest = Interest(name="PaginationTestInterest")

    db_session.add_all([language, interest])
    db_session.flush()

    current_user = User(
        username="paginationowner",
        email="paginationowner@example.com",
        password_hash="test_hash",
        home_region="Maharashtra",
        current_city="Chennai",
    )
    current_user.languages = [language]
    current_user.interests = [interest]

    candidates = []

    for i in range(5):
        candidate = User(
            username=f"paginationuser{i}",
            email=f"paginationuser{i}@example.com",
            password_hash="test_hash",
            home_region="Maharashtra",
            current_city="Chennai",
        )
        candidate.languages = [language]
        candidate.interests = [interest]
        candidates.append(candidate)

    db_session.add_all([current_user, *candidates])
    db_session.flush()

    page_one = discover_users(
        db=db_session,
        current_user=current_user,
        page=1,
        page_size=2,
    )

    page_two = discover_users(
        db=db_session,
        current_user=current_user,
        page=2,
        page_size=2,
    )

    assert page_one["total"] == 5
    assert page_two["total"] == 5

    assert len(page_one["results"]) == 2
    assert len(page_two["results"]) == 2

    page_one_ids = {
        user["user_id"] for user in page_one["results"]
    }
    page_two_ids = {
        user["user_id"] for user in page_two["results"]
    }

    assert page_one_ids.isdisjoint(page_two_ids)


def test_discovery_returns_empty_results_when_no_candidates(db_session):
    current_user = User(
        username="aloneuser",
        email="aloneuser@example.com",
        password_hash="test_hash",
        home_region="Maharashtra",
        current_city="Chennai",
    )

    db_session.add(current_user)
    db_session.flush()

    result = discover_users(
        db=db_session,
        current_user=current_user,
        page=1,
        page_size=10,
    )

    assert result["total"] == 0
    assert result["results"] == []


def test_discovery_excludes_users_without_current_city(db_session):
    current_user = User(
        username="cityowner",
        email="cityowner@example.com",
        password_hash="test_hash",
        home_region="Maharashtra",
        current_city="Chennai",
    )

    candidate = User(
        username="nocandidatecity",
        email="nocandidatecity@example.com",
        password_hash="test_hash",
        home_region="Maharashtra",
        current_city=None,
    )

    db_session.add_all([current_user, candidate])
    db_session.flush()

    result = discover_users(
        db=db_session,
        current_user=current_user,
        page=1,
        page_size=10,
    )

    usernames = [
        user["username"] for user in result["results"]
    ]

    assert "nocandidatecity" not in usernames