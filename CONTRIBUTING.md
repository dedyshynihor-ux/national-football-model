# 🤝 Рекомендації для Контрибюторів

Дякуємо за інтерес до проєкту Національної Футбольної Моделі! Цей документ описує, як внести свій внесок.

## 📋 Вимоги до Внеску

### Перед початком роботи

1. **Fork репозиторій**
   ```bash
   git clone https://github.com/YOUR_USERNAME/national-football-model.git
   cd national-football-model
   ```

2. **Створіть гілку для вашої функції**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Встановіть залежності для розробки**
   ```bash
   pip install -r requirements-dev.txt
   npm install  # для frontend
   ```

## 🔧 Процес Розробки

### Кодування

- **Слідуйте стилю коду** (PEP 8 для Python, ESLint для JavaScript)
- **Пишіть тести** для кожної нової функції
- **Документуйте ваш код** з docstrings та коментарями
- **Використовуйте type hints** (Python) та TypeScript (JavaScript)

### Комітування

Використовуйте конвенцію Conventional Commits:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: нова функція
- `fix`: виправлення помилки
- `docs`: документація
- `style`: форматування коду
- `refactor`: рефакторинг коду
- `test`: додавання тестів
- `chore`: оновлення залежностей

**Приклад:**
```bash
git commit -m "feat(player-service): add player statistics endpoint"
```

### Git Workflow

1. **Синхронізуйте з upstream**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Push на вашу гілку**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Відкрийте Pull Request**
   - Заповніть шаблон PR
   - Посилайтесь на пов'язані Issues (#123)
   - Додайте опис змін
   - Додайте скріншоти (якщо UI зміни)

## ✅ Чеклист перед PR

- [ ] Код слідує styleguide проєкту
- [ ] Всі тести проходять локально
- [ ] Додано нові тести для нових функцій
- [ ] Документація оновлена
- [ ] Нема break changes (або описано у PR)
- [ ] Коміти мають чіткі повідомлення
- [ ] Нема merge conflicts

## 🧪 Тестування

### Backend (Python)
```bash
cd backend
python -m pytest tests/
python -m pytest tests/ --cov  # з覆ттям
```

### Frontend (React)
```bash
cd frontend
npm test
npm run test:coverage
```

### Лінтинг
```bash
# Python
pylint backend/src/
black backend/src/ --check

# JavaScript
npm run lint
npm run lint:fix
```

## 📖 Документування

### Python Docstrings
```python
def create_player(user_id: UUID, position: str) -> Player:
    """
    Створює новий профіль гравця.
    
    Args:
        user_id: ID користувача
        position: Позиція гравця (GK, CB, RB, LB, CM, ST)
        
    Returns:
        Player: Об'єкт створеного гравця
        
    Raises:
        UserNotFound: Якщо користувач не знайдений
        InvalidPosition: Якщо позиція невалідна
    """
    pass
```

### TypeScript JSDoc
```typescript
/**
 * Створює новий матч.
 * @param leagueId - ID ліги
 * @param homeTeamId - ID домашної команди
 * @param awayTeamId - ID гостьової команди
 * @returns Об'єкт створеного матчу
 * @throws {LeagueNotFound} Якщо ліга не знайдена
 */
function createMatch(leagueId: UUID, homeTeamId: UUID, awayTeamId: UUID): Match {
    // implementation
}
```

## 🔒 Питання Безпеки

Якщо ви знайшли вразливість безпеки:

1. **НЕ** відкривайте публічний Issue
2. Напишіть на [security@nfm.ua](mailto:security@nfm.ua)
3. Включіть детальний опис та кроки для відтворення
4. Очікуйте відповіді протягом 48 годин

## 📝 Структура Pull Request

```markdown
## Опис
[Коротко опишіть, що змінюється та чому]

## Тип змін
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Пов'язані Issues
Fixes #123
Related to #456

## Як Тестувати
1. Крок 1
2. Крок 2
3. Крок 3

## Скріншоти (якщо застосовно)
[Додайте зображення]

## Чеклист
- [ ] Мої коміти мають чіткі повідомлення
- [ ] Я додав тести для нових функцій
- [ ] Я оновив документацію
- [ ] Нема break changes
```

## 🎯 Пріоритетні Області для Контрибюцій

### High Priority
- [ ] Тести для існуючого коду
- [ ] Документація
- [ ] Виправлення критичних багів
- [ ] Безпека

### Medium Priority
- [ ] Оптимізація перформансу
- [ ] Розширення функціоналу
- [ ] Покращення UX

### Low Priority
- [ ] Косметичні зміни
- [ ] Рефакторинг

## 📚 Корисні Ресурси

- [Архітектурна Документація](docs/architecture/)
- [API Документація](docs/api/)
- [Database Schema](docs/architecture/DATABASE_SCHEMA.md)
- [Development Guide](docs/DEVELOPMENT.md)
- [Issue Templates](.github/ISSUE_TEMPLATE/)

## 🚀 Після прийняття PR

1. Ваш PR буде злит
2. Вам буде дано кредит в CONTRIBUTORS.md
3. Ви можете видалити вашу гілку
   ```bash
   git branch -d feature/your-feature-name
   ```

## ❓ Питання?

- 📧 Email: [dev@nfm.ua](mailto:dev@nfm.ua)
- 💬 Discussions: [GitHub Discussions](https://github.com/dedyshynihor-ux/national-football-model/discussions)
- 🐛 Issues: [GitHub Issues](https://github.com/dedyshynihor-ux/national-football-model/issues)

---

**Дякуємо за ваш внесок! ⚽**
