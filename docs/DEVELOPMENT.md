# 🚀 Гайд Розробника (Development Guide)

## Локальне Налаштування

### Вимоги
- Git
- Docker & Docker Compose
- Python 3.9+
- Node.js 18+
- PostgreSQL 13+ (або Docker)
- Redis (або Docker)

### Встановлення

```bash
# 1. Клонування репозиторію
git clone https://github.com/dedyshynihor-ux/national-football-model.git
cd national-football-model

# 2. Копіювання .env файлу
cp .env.example .env

# 3. Запуск Docker контейнерів
docker-compose up -d

# 4. Запуск міграцій
cd backend
python manage.py migrate

# 5. Створення суперюзера
python manage.py createsuperuser

# 6. Запуск backend сервера
python manage.py runserver

# 7. Встановлення frontend залежностей
cd ../frontend
npm install

# 8. Запуск frontend сервера
npm start
```

### Перевірка

- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/api/docs
- Admins: http://localhost:8000/admin

## Структура Проєкту

```
project/
├── backend/
│   ├── src/
│   │   ├── users/
│   │   ├── organizations/
│   │   ├── teams/
│   │   ├── players/
│   │   ├── matches/
│   │   └── analytics/
│   ├── tests/
│   ├── migrations/
│   ├── manage.py
│   ├── requirements.txt
│   └── docker-compose.yml
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/
│   │   ├── styles/
│   │   └── App.tsx
│   ├── public/
│   ├── tests/
│   └── package.json
├── mobile/
├── docs/
└── README.md
```

## Workflow

### Розробка функції

1. **Створіть гілку**
   ```bash
   git checkout -b feature/feature-name
   ```

2. **Розробіть функцію**
   ```bash
   # Пишіть код, тести, документацію
   ```

3. **Запустіть тести**
   ```bash
   # Backend
   python -m pytest tests/
   
   # Frontend
   npm test
   ```

4. **Перевіримо лінтинг**
   ```bash
   # Backend
   pylint src/
   black src/
   
   # Frontend
   npm run lint
   ```

5. **Закомітьте зміни**
   ```bash
   git add .
   git commit -m "feat(service): add new feature"
   git push origin feature/feature-name
   ```

6. **Відкрийте PR**
   - Заповніть шаблон
   - Посилайтесь на issues
   - Запросіть review

## Тестування

### Unit Tests

```python
# tests/test_users.py
import pytest
from users.service import UserService

@pytest.fixture
def user_service():
    return UserService()

def test_create_user(user_service):
    user = user_service.create_user(
        email="test@example.com",
        password="password123",
        first_name="John",
        last_name="Doe"
    )
    assert user.email == "test@example.com"
    assert user.first_name == "John"
```

### Integration Tests

```python
# tests/test_user_api.py
from django.test import TestCase
from rest_framework.test import APIClient

class UserAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    def test_register_user(self):
        response = self.client.post('/api/v1/auth/register', {
            'email': 'test@example.com',
            'password': 'password123',
            'first_name': 'John',
            'last_name': 'Doe'
        })
        self.assertEqual(response.status_code, 201)
```

### E2E Tests

```typescript
// tests/e2e/user.spec.ts
import { test, expect } from '@playwright/test';

test('User registration flow', async ({ page }) => {
    await page.goto('http://localhost:3000/register');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="password"]', 'password123');
    await page.click('button[type="submit"]');
    await expect(page).toHaveURL('/login');
});
```

## Debugging

### Backend

```python
# Використовуйте pdb
import pdb; pdb.set_trace()

# Або ipdb
import ipdb; ipdb.set_trace()

# Або VS Code debugger
# .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/backend/manage.py",
            "args": ["runserver"],
            "django": true
        }
    ]
}
```

### Frontend

```typescript
// Використовуйте console
console.log('Debug:', variable);
console.table(data);

// Або React DevTools
// https://react-devtools-tutorial.vercel.app/

// Або VS Code debugger
// .vscode/launch.json
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "chrome",
            "request": "launch",
            "name": "Launch Chrome",
            "url": "http://localhost:3000",
            "webRoot": "${workspaceFolder}/frontend/src"
        }
    ]
}
```

## Environment Variables

```bash
# .env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/nfm

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600

# AWS S3
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
AWS_STORAGE_BUCKET_NAME=nfm-bucket
AWS_S3_REGION_NAME=eu-central-1

# Email
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password

# Frontend
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_WS_URL=ws://localhost:8000/ws
```

## Database Migrations

```bash
# Створення міграції
python manage.py makemigrations

# Перегляд SQL
python manage.py sqlmigrate app migration_name

# Застосування міграцій
python manage.py migrate

# Скасування останньої міграції
python manage.py migrate app 0001

# Перегляд статусу
python manage.py showmigrations
```

## API Documentation

### OpenAPI/Swagger

```bash
# Доступно на http://localhost:8000/api/docs

# Або генеруйте YAML
python manage.py spectacular --file schema.yml
```

### API Endpoints

```
POST   /api/v1/auth/register
POST   /api/v1/auth/login
GET    /api/v1/users/{id}
PUT    /api/v1/users/{id}
GET    /api/v1/organizations
POST   /api/v1/organizations
GET    /api/v1/teams/{id}
GET    /api/v1/players/{id}
GET    /api/v1/matches/{id}
POST   /api/v1/matches/{id}/events
```

## Performance Optimization

### Database

```python
# Використовуйте select_related для ForeignKey
User.objects.select_related('organization')

# Використовуйте prefetch_related для ManyToMany
Team.objects.prefetch_related('players')

# Додавайте indexes на часто запитувані поля
class Player(models.Model):
    position = models.CharField(max_length=50, db_index=True)
```

### Caching

```python
from django.core.cache import cache

# Кешування результату
result = cache.get('player_stats_123')
if result is None:
    result = expensive_calculation()
    cache.set('player_stats_123', result, 3600)  # 1 час
```

### Frontend

```typescript
// Lazy loading
const PlayerList = React.lazy(() => import('./PlayerList'));

// Code splitting
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

// Memoization
const Player = React.memo(({ player }) => (
    <div>{player.name}</div>
));
```

## Deployment

### Docker

```bash
# Збирання образу
docker build -t nfm:latest .

# Запуск контейнера
docker run -p 8000:8000 nfm:latest

# Docker Compose
docker-compose up -d
docker-compose logs -f
docker-compose down
```

### Kubernetes

```bash
# Застосування конфігурації
kubectl apply -f k8s/

# Перевірка стану
kubectl get pods
kubectl describe pod pod-name

# Логи
kubectl logs pod-name

# Масштабування
kubectl scale deployment/nfm --replicas=3
```

## Корисні Команди

```bash
# Git
git log --oneline
git diff
git stash
git cherry-pick

# Docker
docker ps
docker exec -it container_name bash
docker logs container_name

# Database
psql -U user -d database -h localhost
\dt              # List tables
\d table_name    # Describe table

# Python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Node
npm install
npm start
npm run build
npm run test
```

## Troubleshooting

### Problem: Database connection error
```bash
# Solution:
psql -U postgres -h localhost -c "CREATE DATABASE nfm;"
```

### Problem: Port already in use
```bash
# Solution:
lsof -i :8000
kill -9 PID
```

### Problem: Module not found
```bash
# Solution:
pip install -r requirements.txt
npm install
```

## Resources

- [Django Docs](https://docs.djangoproject.com/)
- [React Docs](https://react.dev/)
- [PostgreSQL Docs](https://www.postgresql.org/docs/)
- [Redis Docs](https://redis.io/docs/)
- [Docker Docs](https://docs.docker.com/)

---

**Щасливої розробки! 🚀**
