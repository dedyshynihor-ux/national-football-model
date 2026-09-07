# 📊 Схема Бази Даних (Database Schema)

## Огляд

База даних розділена на логічні модулі, кожний з яких обслуговує специфічну область функціональності.

## 1. Модуль Користувачів (Users Module)

### users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    phone VARCHAR(20),
    avatar_url TEXT,
    bio TEXT,
    role VARCHAR(50) NOT NULL, -- ADMIN, FEDERATION, LEAGUE, CLUB, COACH, PLAYER, SCOUT, MEDIA, FAN
    status VARCHAR(50) DEFAULT 'active', -- active, inactive, suspended, deleted
    organization_id UUID REFERENCES organizations(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    email_verified BOOLEAN DEFAULT false,
    email_verified_at TIMESTAMP,
    INDEX idx_email,
    INDEX idx_organization_id,
    INDEX idx_role
);

CREATE TABLE user_roles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) NOT NULL,
    organization_id UUID REFERENCES organizations(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, role, organization_id),
    INDEX idx_user_id
);

CREATE TABLE user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    theme VARCHAR(50), -- light, dark
    language VARCHAR(10), -- uk, en
    notifications_enabled BOOLEAN DEFAULT true,
    email_notifications BOOLEAN DEFAULT true,
    push_notifications BOOLEAN DEFAULT true,
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 2. Модуль Організацій (Organizations Module)

### organizations
```sql
CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    type VARCHAR(50) NOT NULL, -- FEDERATION, LEAGUE, CLUB, ACADEMY, MEDIA
    country VARCHAR(100),
    city VARCHAR(100),
    region VARCHAR(100),
    address TEXT,
    description TEXT,
    logo_url TEXT,
    banner_url TEXT,
    website URL,
    email VARCHAR(255),
    phone VARCHAR(20),
    established_year INTEGER,
    parent_organization_id UUID REFERENCES organizations(id),
    metadata JSONB DEFAULT '{}',
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_type,
    INDEX idx_parent_id,
    INDEX idx_country_city
);

CREATE TABLE organization_members (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    position VARCHAR(100),
    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'active',
    UNIQUE(organization_id, user_id),
    INDEX idx_organization_id,
    INDEX idx_user_id
);
```

## 3. Модуль Команд (Teams Module)

### teams
```sql
CREATE TABLE teams (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    club_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    age_category VARCHAR(50), -- U-6, U-8, ..., U-21, PRO
    season INTEGER,
    coach_id UUID REFERENCES users(id),
    assistant_coach_id UUID REFERENCES users(id),
    manager_id UUID REFERENCES users(id),
    founded_year INTEGER,
    logo_url TEXT,
    status VARCHAR(50) DEFAULT 'active',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_club_id,
    INDEX idx_season,
    INDEX idx_age_category
);

CREATE TABLE team_squad (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    player_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    squad_number INTEGER,
    position VARCHAR(50), -- GK, CB, RB, LB, RWB, LWB, CM, CDM, CAM, RM, LM, ST, CF, RW, LW
    joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    departure_date TIMESTAMP,
    captain BOOLEAN DEFAULT false,
    vice_captain BOOLEAN DEFAULT false,
    status VARCHAR(50) DEFAULT 'active',
    UNIQUE(team_id, player_id, season),
    INDEX idx_team_id,
    INDEX idx_player_id
);
```

## 4. Модуль Гравців (Players Module)

### players
```sql
CREATE TABLE players (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    nationality VARCHAR(100),
    height_cm INTEGER,
    weight_kg INTEGER,
    preferred_foot VARCHAR(10), -- LEFT, RIGHT, BOTH
    position VARCHAR(50) NOT NULL,
    registration_number VARCHAR(100) UNIQUE,
    passport_number VARCHAR(100),
    current_team_id UUID REFERENCES teams(id),
    contract_start DATE,
    contract_end DATE,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id,
    INDEX idx_nationality,
    INDEX idx_position,
    INDEX idx_date_of_birth
);

CREATE TABLE player_statistics (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_id UUID NOT NULL REFERENCES players(id) ON DELETE CASCADE,
    season INTEGER NOT NULL,
    league_id UUID REFERENCES organizations(id),
    matches_played INTEGER DEFAULT 0,
    goals INTEGER DEFAULT 0,
    assists INTEGER DEFAULT 0,
    yellow_cards INTEGER DEFAULT 0,
    red_cards INTEGER DEFAULT 0,
    minutes_played INTEGER DEFAULT 0,
    pass_accuracy DECIMAL(5,2),
    dribbles INTEGER DEFAULT 0,
    tackles INTEGER DEFAULT 0,
    interceptions INTEGER DEFAULT 0,
    statistics JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(player_id, season, league_id),
    INDEX idx_player_id,
    INDEX idx_season
);
```

## 5. Модуль Матчів (Matches Module)

### fixtures
```sql
CREATE TABLE fixtures (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    league_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    season INTEGER NOT NULL,
    round INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(league_id, season, round),
    INDEX idx_league_id
);

CREATE TABLE matches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    fixture_id UUID NOT NULL REFERENCES fixtures(id) ON DELETE CASCADE,
    league_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    home_team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    away_team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    scheduled_at TIMESTAMP NOT NULL,
    started_at TIMESTAMP,
    finished_at TIMESTAMP,
    venue_id UUID REFERENCES venues(id),
    home_score INTEGER,
    away_score INTEGER,
    status VARCHAR(50) NOT NULL, -- SCHEDULED, LIVE, FINISHED, CANCELLED, POSTPONED
    referee_id UUID REFERENCES users(id),
    fourth_official_id UUID REFERENCES users(id),
    weather JSONB,
    attendance INTEGER,
    statistics JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_fixture_id,
    INDEX idx_league_id,
    INDEX idx_home_team_id,
    INDEX idx_away_team_id,
    INDEX idx_scheduled_at
);

CREATE TABLE match_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    match_id UUID NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
    minute INTEGER NOT NULL,
    second INTEGER,
    event_type VARCHAR(50) NOT NULL, -- GOAL, ASSIST, YELLOW_CARD, RED_CARD, SUBSTITUTION, OWN_GOAL, PENALTY
    player_id UUID REFERENCES users(id),
    team_id UUID REFERENCES teams(id),
    details JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_match_id,
    INDEX idx_player_id
);
```

## 6. Модуль Ліг (Leagues Module)

### leagues
```sql
CREATE TABLE leagues (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    federation_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    level INTEGER, -- 1 = Highest, 2, 3, etc
    season INTEGER NOT NULL,
    format VARCHAR(50), -- ROUND_ROBIN, KNOCKOUT, GROUP_STAGE
    teams_count INTEGER,
    matches_per_week INTEGER,
    start_date DATE,
    end_date DATE,
    status VARCHAR(50) DEFAULT 'planning', -- PLANNING, ACTIVE, FINISHED
    rules JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(federation_id, level, season),
    INDEX idx_federation_id,
    INDEX idx_season
);

CREATE TABLE league_tables (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    league_id UUID NOT NULL REFERENCES leagues(id) ON DELETE CASCADE,
    team_id UUID NOT NULL REFERENCES teams(id) ON DELETE CASCADE,
    position INTEGER,
    matches_played INTEGER DEFAULT 0,
    wins INTEGER DEFAULT 0,
    draws INTEGER DEFAULT 0,
    losses INTEGER DEFAULT 0,
    goals_for INTEGER DEFAULT 0,
    goals_against INTEGER DEFAULT 0,
    goal_difference INTEGER DEFAULT 0,
    points INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(league_id, team_id),
    INDEX idx_league_id,
    INDEX idx_team_id
);
```

## 7. Модуль Stadiums/Venues

### venues
```sql
CREATE TABLE venues (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    capacity INTEGER,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    address TEXT,
    phone VARCHAR(20),
    surface VARCHAR(50), -- GRASS, ARTIFICIAL_GRASS, HYBRID
    lighting BOOLEAN DEFAULT false,
    owner_id UUID REFERENCES organizations(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_city,
    INDEX idx_owner_id
);
```

## 8. Модуль Медіа (Media Module)

### media
```sql
CREATE TABLE media (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    organization_id UUID REFERENCES organizations(id),
    match_id UUID REFERENCES matches(id),
    player_id UUID REFERENCES players(id),
    type VARCHAR(50) NOT NULL, -- IMAGE, VIDEO, DOCUMENT
    title VARCHAR(255),
    description TEXT,
    file_url TEXT NOT NULL,
    thumbnail_url TEXT,
    file_size BIGINT,
    mime_type VARCHAR(100),
    duration INTEGER, -- для відео
    tags JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}',
    visibility VARCHAR(50) DEFAULT 'public', -- PUBLIC, PRIVATE, RESTRICTED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id,
    INDEX idx_match_id,
    INDEX idx_player_id
);
```

## 9. Індекси та Оптимізація

```sql
-- Найчастіші запити
CREATE INDEX idx_matches_scheduled ON matches(league_id, scheduled_at) WHERE status != 'CANCELLED';
CREATE INDEX idx_player_stats ON player_statistics(player_id, season);
CREATE INDEX idx_league_standings ON league_tables(league_id, position);
CREATE INDEX idx_team_squad_active ON team_squad(team_id) WHERE status = 'active';
```

## 10. Партиціонування для Великих Таблиць

```sql
-- Партиціювати по сезону для matches
CREATE TABLE matches_2024 PARTITION OF matches FOR VALUES IN (2024);
CREATE TABLE matches_2025 PARTITION OF matches FOR VALUES IN (2025);
```

## 11. Для посилення безпеки

```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Для аудиту
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(255),
    operation VARCHAR(10), -- INSERT, UPDATE, DELETE
    record_id UUID,
    user_id UUID REFERENCES users(id),
    changes JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_table_name,
    INDEX idx_user_id,
    INDEX idx_created_at
);
```

Оця схема забезпечує:
- ✅ Нормалізацію даних
- ✅ Цілісність даних
- ✅ Гнучкість для майбутніх розширень
- ✅ Оптимальну продуктивність
- ✅ Безпеку та аудит
