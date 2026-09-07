import { useState } from 'react';
import { useJokes } from '../hooks/useJokes';

const CATEGORIES = [
  { value: '', label: 'Будь-яка категорія' },
  { value: 'general', label: 'Загальні' },
  { value: 'programming', label: 'Програмування' },
  { value: 'knock-knock', label: 'Стук-стук' },
];

function fallbackCopy(text: string): boolean {
  const textarea = document.createElement('textarea');
  textarea.value = text;
  textarea.style.position = 'fixed';
  textarea.style.opacity = '0';
  document.body.appendChild(textarea);
  textarea.select();
  const copied = document.execCommand?.('copy') ?? false;
  textarea.remove();
  return copied;
}

export default function JokeGenerator() {
  const {
    currentJoke,
    history,
    isLoading,
    error,
    generateJoke,
    reactToJoke,
  } = useJokes();
  const [category, setCategory] = useState('');
  const [shareStatus, setShareStatus] = useState('');

  const shareJoke = async () => {
    if (!currentJoke) return;

    setShareStatus('');
    try {
      if (navigator.share) {
        await navigator.share({
          title: 'Смішний жарт',
          text: currentJoke.text,
        });
        setShareStatus('Жарт поширено!');
        return;
      }

      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(currentJoke.text);
      } else if (!fallbackCopy(currentJoke.text)) {
        throw new Error('Copy is unavailable');
      }
      setShareStatus('Жарт скопійовано!');
    } catch (shareError) {
      if (shareError instanceof DOMException && shareError.name === 'AbortError') {
        return;
      }
      setShareStatus('Не вдалося поширити жарт.');
    }
  };

  return (
    <section className="generator" aria-labelledby="page-title">
      <header className="hero">
        <span className="eyebrow">Щоденна порція гумору</span>
        <h1 id="page-title">Генератор жартів</h1>
        <p>Обери тему або довірся випадку — гарний настрій збережемо локально.</p>
      </header>

      <div className="controls">
        <label htmlFor="category">Категорія</label>
        <select
          id="category"
          value={category}
          onChange={(event) => setCategory(event.target.value)}
          disabled={isLoading}
        >
          {CATEGORIES.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </select>
        <button
          className="generate-button"
          type="button"
          onClick={() => void generateJoke(category || undefined)}
          disabled={isLoading}
        >
          {isLoading ? 'Шукаємо жарт…' : 'Згенерувати жарт'}
        </button>
      </div>

      {error && (
        <p className="notice error" role="alert">
          {error}
        </p>
      )}

      <article className={`joke-card ${isLoading ? 'loading' : ''}`} aria-live="polite">
        {isLoading && !currentJoke ? (
          <div className="skeleton" aria-label="Завантаження жарту">
            <span />
            <span />
            <span />
          </div>
        ) : currentJoke ? (
          <>
            <div className="badges">
              <span>{currentJoke.category}</span>
              <span>{currentJoke.type}</span>
            </div>
            <p className="joke-text">{currentJoke.text}</p>
            <div className="actions">
              <button
                type="button"
                className={currentJoke.reaction === 'like' ? 'selected' : ''}
                aria-pressed={currentJoke.reaction === 'like'}
                onClick={() => reactToJoke('like')}
              >
                👍 Подобається
              </button>
              <button
                type="button"
                className={currentJoke.reaction === 'dislike' ? 'selected' : ''}
                aria-pressed={currentJoke.reaction === 'dislike'}
                onClick={() => reactToJoke('dislike')}
              >
                👎 Не моє
              </button>
              <button type="button" onClick={() => void shareJoke()}>
                ↗ Поділитися
              </button>
            </div>
            {shareStatus && (
              <p className="share-status" role="status">
                {shareStatus}
              </p>
            )}
          </>
        ) : (
          <div className="empty-state">
            <span aria-hidden="true">🎭</span>
            <p>Натисни кнопку — і тут з’явиться жарт.</p>
          </div>
        )}
      </article>

      <aside className="history" aria-labelledby="history-title">
        <div className="section-heading">
          <h2 id="history-title">Останні жарти</h2>
          <span>{history.length}/5</span>
        </div>
        {history.length ? (
          <ol>
            {history.map((joke) => (
              <li key={joke.id}>
                <p>{joke.text}</p>
                <div>
                  <span>{joke.category}</span>
                  {joke.reaction && (
                    <span aria-label={joke.reaction === 'like' ? 'Сподобалось' : 'Не сподобалось'}>
                      {joke.reaction === 'like' ? '👍' : '👎'}
                    </span>
                  )}
                </div>
              </li>
            ))}
          </ol>
        ) : (
          <p className="muted">Історія з’явиться після першого жарту.</p>
        )}
      </aside>
    </section>
  );
}
