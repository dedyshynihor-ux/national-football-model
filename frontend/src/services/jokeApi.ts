export interface Joke {
  id: string;
  text: string;
  type: string;
  category: string;
  reaction?: 'like' | 'dislike';
}

interface JokeResponse {
  id?: string | number;
  joke?: string;
  text?: string;
  content?: string;
  setup?: string;
  punchline?: string;
  delivery?: string;
  type?: string;
  category?: string;
}

const API_ROOT = '/api/v1/jokes';

function normalizeJoke(data: JokeResponse, fallbackCategory?: string): Joke {
  const text =
    data.joke ??
    data.text ??
    data.content ??
    [data.setup, data.punchline ?? data.delivery].filter(Boolean).join('\n');

  if (!text) {
    throw new Error('Сервер повернув жарт у невідомому форматі.');
  }

  return {
    id: String(data.id ?? `${Date.now()}-${Math.random()}`),
    text,
    type: data.type ?? 'single',
    category: data.category ?? fallbackCategory ?? 'Загальна',
  };
}

async function requestJoke(endpoint: string, fallbackCategory?: string): Promise<Joke> {
  const response = await fetch(endpoint, {
    headers: { Accept: 'application/json' },
  });

  if (!response.ok) {
    throw new Error(`Не вдалося завантажити жарт (${response.status}).`);
  }

  return normalizeJoke((await response.json()) as JokeResponse, fallbackCategory);
}

export function getRandomJoke(category?: string): Promise<Joke> {
  if (category) {
    return requestJoke(
      `${API_ROOT}/category/${encodeURIComponent(category)}`,
      category,
    );
  }

  return requestJoke(`${API_ROOT}/random`);
}
