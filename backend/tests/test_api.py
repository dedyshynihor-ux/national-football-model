from datetime import datetime, timezone

from fastapi.testclient import TestClient

from src.main import Store, create_app


def client() -> TestClient:
    return TestClient(create_app(Store()))


def test_health() -> None:
    response = client().get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_entities_and_match() -> None:
    api = client()
    home = api.post("/api/v1/teams", json={"name": "Dynamo U19", "club": "Dynamo Kyiv"}).json()
    away = api.post("/api/v1/teams", json={"name": "Rukh U19", "club": "Rukh Lviv"}).json()
    league = api.post("/api/v1/leagues", json={"name": "U19 Championship", "season": 2026}).json()

    response = api.post(
        "/api/v1/matches",
        json={
            "league_id": league["id"],
            "home_team_id": home["id"],
            "away_team_id": away["id"],
            "scheduled_at": datetime(2026, 9, 20, 15, tzinfo=timezone.utc).isoformat(),
        },
    )

    assert response.status_code == 201
    assert response.json()["status"] == "SCHEDULED"


def test_match_requires_existing_teams_and_league() -> None:
    response = client().post(
        "/api/v1/matches",
        json={
            "league_id": "00000000-0000-0000-0000-000000000001",
            "home_team_id": "00000000-0000-0000-0000-000000000002",
            "away_team_id": "00000000-0000-0000-0000-000000000003",
            "scheduled_at": "2026-09-20T15:00:00Z",
        },
    )
    assert response.status_code == 404


def test_league_standings_use_finished_matches() -> None:
    api = client()
    home = api.post("/api/v1/teams", json={"name": "Dynamo", "club": "Dynamo Kyiv"}).json()
    away = api.post("/api/v1/teams", json={"name": "Rukh", "club": "Rukh Lviv"}).json()
    league = api.post("/api/v1/leagues", json={"name": "Premier League", "season": 2026}).json()
    api.post(
        "/api/v1/matches",
        json={
            "league_id": league["id"],
            "home_team_id": home["id"],
            "away_team_id": away["id"],
            "scheduled_at": "2026-09-20T15:00:00Z",
            "status": "FINISHED",
            "home_score": 2,
            "away_score": 1,
        },
    )

    response = api.get(f"/api/v1/leagues/{league['id']}/standings")

    assert response.status_code == 200
    assert response.json()[0]["team_name"] == "Dynamo"
    assert response.json()[0]["points"] == 3
    assert response.json()[1]["goal_difference"] == -1
