"""Initial API for the National Football Model MVP."""

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


class MatchStatus(str, Enum):
    scheduled = "SCHEDULED"
    live = "LIVE"
    finished = "FINISHED"
    cancelled = "CANCELLED"


class TeamCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    club: str = Field(min_length=2, max_length=255)
    age_category: Optional[str] = Field(default=None, max_length=50)


class Team(TeamCreate):
    id: UUID


class PlayerCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    date_of_birth: datetime
    nationality: Optional[str] = Field(default=None, max_length=100)
    position: str = Field(min_length=2, max_length=50)
    team_id: Optional[UUID] = None


class Player(PlayerCreate):
    id: UUID


class LeagueCreate(BaseModel):
    name: str = Field(min_length=2, max_length=255)
    season: int = Field(ge=1900, le=2200)


class League(LeagueCreate):
    id: UUID


class MatchCreate(BaseModel):
    league_id: UUID
    home_team_id: UUID
    away_team_id: UUID
    scheduled_at: datetime
    status: MatchStatus = MatchStatus.scheduled
    home_score: Optional[int] = Field(default=None, ge=0)
    away_score: Optional[int] = Field(default=None, ge=0)


class Match(MatchCreate):
    id: UUID


class Store:
    """Small in-memory store used until the persistence layer is introduced."""

    def __init__(self) -> None:
        self.teams: Dict[UUID, Team] = {}
        self.players: Dict[UUID, Player] = {}
        self.leagues: Dict[UUID, League] = {}
        self.matches: Dict[UUID, Match] = {}


def create_app(store: Optional[Store] = None) -> FastAPI:
    app = FastAPI(
        title="National Football Model API",
        version="0.1.0",
        description="MVP API for Ukrainian football entities and fixtures.",
    )
    data = store or Store()

    @app.get("/health", tags=["system"])
    def health() -> dict:
        return {"status": "ok"}

    @app.post("/api/v1/teams", response_model=Team, status_code=status.HTTP_201_CREATED)
    def create_team(payload: TeamCreate) -> Team:
        team = Team(id=uuid4(), **payload.model_dump())
        data.teams[team.id] = team
        return team

    @app.get("/api/v1/teams", response_model=List[Team])
    def list_teams() -> List[Team]:
        return list(data.teams.values())

    @app.get("/api/v1/teams/{team_id}", response_model=Team)
    def get_team(team_id: UUID) -> Team:
        return _get(data.teams, team_id, "Team")

    @app.post("/api/v1/players", response_model=Player, status_code=status.HTTP_201_CREATED)
    def create_player(payload: PlayerCreate) -> Player:
        if payload.team_id is not None and payload.team_id not in data.teams:
            raise HTTPException(status_code=404, detail="Team not found")
        player = Player(id=uuid4(), **payload.model_dump())
        data.players[player.id] = player
        return player

    @app.get("/api/v1/players", response_model=List[Player])
    def list_players() -> List[Player]:
        return list(data.players.values())

    @app.get("/api/v1/players/{player_id}", response_model=Player)
    def get_player(player_id: UUID) -> Player:
        return _get(data.players, player_id, "Player")

    @app.post("/api/v1/leagues", response_model=League, status_code=status.HTTP_201_CREATED)
    def create_league(payload: LeagueCreate) -> League:
        league = League(id=uuid4(), **payload.model_dump())
        data.leagues[league.id] = league
        return league

    @app.get("/api/v1/leagues", response_model=List[League])
    def list_leagues() -> List[League]:
        return list(data.leagues.values())

    @app.get("/api/v1/leagues/{league_id}", response_model=League)
    def get_league(league_id: UUID) -> League:
        return _get(data.leagues, league_id, "League")

    @app.post("/api/v1/matches", response_model=Match, status_code=status.HTTP_201_CREATED)
    def create_match(payload: MatchCreate) -> Match:
        if payload.home_team_id == payload.away_team_id:
            raise HTTPException(status_code=422, detail="A team cannot play itself")
        if payload.league_id not in data.leagues:
            raise HTTPException(status_code=404, detail="League not found")
        for team_id in (payload.home_team_id, payload.away_team_id):
            if team_id not in data.teams:
                raise HTTPException(status_code=404, detail="Team not found")
        match = Match(id=uuid4(), **payload.model_dump())
        data.matches[match.id] = match
        return match

    @app.get("/api/v1/matches", response_model=List[Match])
    def list_matches(league_id: Optional[UUID] = None) -> List[Match]:
        matches = data.matches.values()
        if league_id is not None:
            matches = (match for match in matches if match.league_id == league_id)
        return list(matches)

    @app.get("/api/v1/matches/{match_id}", response_model=Match)
    def get_match(match_id: UUID) -> Match:
        return _get(data.matches, match_id, "Match")

    return app


def _get(collection: Dict[UUID, BaseModel], item_id: UUID, name: str) -> BaseModel:
    item = collection.get(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail=f"{name} not found")
    return item


app = create_app()
