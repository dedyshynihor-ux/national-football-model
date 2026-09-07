# 🔧 Мікросервісна Архітектура

## Огляд

Кожний мікросервіс є незалежним модулем, який:
- Розпочинає власний процес
- Має свою базу даних
- Спілкується через API/Message Queue
- Масштабується незалежно
- Розгортається незалежно

## 1. User Service

### Відповідальність
- Управління користувачами
- Автентифікація та авторизація
- Профілі та параметри

### API Endpoints
```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
POST   /api/v1/auth/logout
POST   /api/v1/auth/refresh-token
GET    /api/v1/users/{id}
PUT    /api/v1/users/{id}
DELETE /api/v1/users/{id}
GET    /api/v1/users/{id}/roles
POST   /api/v1/users/{id}/roles
```

### Events
- `UserRegistered`
- `UserLoggedIn`
- `UserProfileUpdated`
- `UserDeleted`

### Tech Stack
- Runtime: Node.js
- Framework: Express.js
- DB: PostgreSQL
- Cache: Redis
- Auth: JWT + OAuth 2.0

---

## 2. Organization Service

### Відповідальність
- Управління организаціями (федерації, ліги, клуби, академії)
- Управління членами організації
- Структура та ієрархія

### API Endpoints
```
POST   /api/v1/organizations
GET    /api/v1/organizations/{id}
PUT    /api/v1/organizations/{id}
DELETE /api/v1/organizations/{id}
GET    /api/v1/organizations/{id}/members
POST   /api/v1/organizations/{id}/members
DELETE /api/v1/organizations/{id}/members/{memberId}
```

### Events
- `OrganizationCreated`
- `OrganizationUpdated`
- `MemberJoined`
- `MemberLeft`

### Tech Stack
- Runtime: Python
- Framework: FastAPI
- DB: PostgreSQL
- Message Queue: RabbitMQ

---

## 3. Team Service

### Відповідальність
- Управління командами
- Склад команди (squad)
- Інформація про тренерів та менеджерів

### API Endpoints
```
POST   /api/v1/teams
GET    /api/v1/teams/{id}
PUT    /api/v1/teams/{id}
GET    /api/v1/teams/{id}/squad
POST   /api/v1/teams/{id}/squad
DELETE /api/v1/teams/{id}/squad/{playerId}
GET    /api/v1/clubs/{clubId}/teams
```

### Events
- `TeamCreated`
- `SquadUpdated`
- `PlayerAdded`
- `PlayerRemoved`

### Tech Stack
- Runtime: Python
- Framework: FastAPI
- DB: PostgreSQL
- Cache: Redis

---

## 4. Player Service

### Відповідальність
- Управління гравцями
- Профілі гравців
- Статистика гравців
- Історія переходів

### API Endpoints
```
POST   /api/v1/players
GET    /api/v1/players/{id}
PUT    /api/v1/players/{id}
DELETE /api/v1/players/{id}
GET    /api/v1/players/{id}/statistics
GET    /api/v1/players/{id}/history
GET    /api/v1/players?nationality=UA&position=ST
```

### Events
- `PlayerCreated`
- `PlayerProfileUpdated`
- `PlayerTransferred`
- `PlayerStatisticsUpdated`

### Tech Stack
- Runtime: Node.js
- Framework: Express.js
- DB: PostgreSQL
- Search: Elasticsearch

---

## 5. Match Service

### Відповідальність
- Управління матчами
- Розписи матчів
- Результати матчів
- Live scoring

### API Endpoints
```
POST   /api/v1/matches
GET    /api/v1/matches/{id}
PUT    /api/v1/matches/{id}
GET    /api/v1/matches?league={id}&season={year}
POST   /api/v1/matches/{id}/events
GET    /api/v1/fixtures/{id}
```

### WebSocket Events (Real-time)
```
ws://api.nfm.ua/ws/matches/{matchId}
- match:started
- match:goal
- match:substitution
- match:finished
- match:updated
```

### Events
- `MatchScheduled`
- `MatchStarted`
- `GoalScored`
- `CardIssued`
- `MatchFinished`

### Tech Stack
- Runtime: Node.js
- Framework: Express.js + Socket.io
- DB: PostgreSQL
- Cache: Redis
- Message Queue: RabbitMQ

---

## 6. League Service

### Відповідальність
- Управління лігами
- Таблиці та рейтинги
- Правила та регламенти
- Сезони

### API Endpoints
```
POST   /api/v1/leagues
GET    /api/v1/leagues/{id}
PUT    /api/v1/leagues/{id}
GET    /api/v1/leagues/{id}/table
GET    /api/v1/leagues/{id}/standings
GET    /api/v1/leagues/{id}/matches
```

### Events
- `LeagueCreated`
- `SeasonStarted`
- `TableUpdated`
- `SeasonFinished`

### Tech Stack
- Runtime: Python
- Framework: FastAPI
- DB: PostgreSQL
- Cache: Redis

---

## 7. Analytics Service

### Відповідальність
- Обчислення статистики
- Аналітика матчів
- Рейтинги гравців
- Звіти та аналізи

### API Endpoints
```
GET    /api/v1/analytics/player/{id}
GET    /api/v1/analytics/team/{id}
GET    /api/v1/analytics/league/{id}
GET    /api/v1/analytics/match/{id}
POST   /api/v1/analytics/reports
GET    /api/v1/analytics/trends
```

### Events (Consumer)
- Слухає: `PlayerStatisticsUpdated`
- Слухає: `MatchFinished`
- Публікує: `AnalyticsUpdated`

### Tech Stack
- Runtime: Python
- Framework: Django
- DB: PostgreSQL + MongoDB (для аналітики)
- Analytics: Apache Spark

---

## 8. Notification Service

### Відповідальність
- Відправлення сповіщень
- Email, SMS, Push
- Управління підписками

### API Endpoints
```
POST   /api/v1/notifications/send
GET    /api/v1/notifications/user/{id}
PUT    /api/v1/notifications/{id}/read
PUT    /api/v1/users/{id}/preferences
```

### Events (Consumer)
- Слухає: Усі події в системі
- Публікує: `NotificationSent`

### Tech Stack
- Runtime: Node.js
- Framework: Express.js
- Message Queue: Bull (Redis-based)
- Providers: SendGrid, Twilio, Firebase

---

## 9. Media Service

### Відповідальність
- Управління медіа-контентом
- Завантаження файлів
- Обробка зображень/видео
- CDN інтеграція

### API Endpoints
```
POST   /api/v1/media/upload
GET    /api/v1/media/{id}
DELETE /api/v1/media/{id}
PUT    /api/v1/media/{id}
GET    /api/v1/media?type=video&match={id}
```

### Events
- `MediaUploaded`
- `MediaProcessed`
- `MediaDeleted`

### Tech Stack
- Runtime: Go
- Framework: Echo
- Storage: AWS S3 / Google Cloud Storage
- Processing: FFmpeg
- CDN: CloudFlare / AWS CloudFront

---

## 10. AI/ML Service

### Відповідальність
- Machine Learning моделі
- Предиктивна аналітика
- Рекомендацій система
- Скаутинг асистент

### API Endpoints
```
POST   /api/v1/ai/predict/match
GET    /api/v1/ai/recommendations/player
GET    /api/v1/ai/scouting/analysis
POST   /api/v1/ai/models/train
```

### Tech Stack
- Runtime: Python
- ML Framework: TensorFlow / PyTorch
- Server: FastAPI
- Deployment: Docker + K8s

---

## Комунікація між Сервісами

### Синхронна комунікація (REST/gRPC)
```
Client → API Gateway → User Service → (REST) → Organization Service
```

### Асинхронна комунікація (Message Queue)
```
Match Service → RabbitMQ → {
    Analytics Service (слухає MatchFinished),
    Notification Service (слухає MatchFinished),
    League Service (слухає MatchFinished)
}
```

### Circuit Breaker Pattern
```
При помилці сервісу:
1. CLOSED → запити проходять
2. OPEN → запити не проходять (fail fast)
3. HALF_OPEN → спроба відновлення
4. CLOSED → сервіс відновлений
```

## Обробка помилок

### Error Codes
```
400: Bad Request
401: Unauthorized
403: Forbidden
404: Not Found
409: Conflict (duplicate)
429: Too Many Requests (Rate Limited)
500: Internal Server Error
503: Service Unavailable
```

### Retry Strategy
- Exponential Backoff
- Jitter для уникнення thundering herd
- Max retries: 3
- Initial delay: 100ms

## Моніторинг

### Метрики для кожного сервісу
- Request count
- Error rate
- Response time
- Database query time
- Message queue size

### Health Checks
```
GET /health
GET /health/ready (Kubernetes readiness)
GET /health/live  (Kubernetes liveness)
```

Кожний сервіс має:
- Свій GitHub репозиторій
- Свій Docker образ
- Свій Kubernetes Deployment
- Свої тести
- Свою документацію
