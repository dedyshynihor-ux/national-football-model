import { useCallback, useEffect, useState } from 'react';
import { getRandomJoke, type Joke } from '../services/jokeApi';

const STORAGE_KEY = 'joke-generator-history-v1';
const HISTORY_LIMIT = 5;

function readHistory(): Joke[] {
  try {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (!saved) return [];

    const parsed: unknown = JSON.parse(saved);
    return Array.isArray(parsed) ? (parsed as Joke[]).slice(0, HISTORY_LIMIT) : [];
  } catch {
    return [];
  }
}

export function useJokes() {
  const [history, setHistory] = useState<Joke[]>(readHistory);
  const [currentJoke, setCurrentJoke] = useState<Joke | null>(
    () => readHistory()[0] ?? null,
  );
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
    } catch {
      // The app remains usable when storage is unavailable or full.
    }
  }, [history]);

  const generateJoke = useCallback(
    async (category?: string) => {
      setIsLoading(true);
      setError(null);

      try {
        const joke = await getRandomJoke(category);
        setCurrentJoke(joke);
        setHistory((previous) => [
          joke,
          ...previous.filter((item) => item.id !== joke.id),
        ].slice(0, HISTORY_LIMIT));
      } catch (requestError) {
        const message =
          requestError instanceof Error
            ? requestError.message
            : 'Не вдалося завантажити жарт.';
        setError(
          currentJoke
            ? `${message} Показуємо останній збережений жарт.`
            : message,
        );
      } finally {
        setIsLoading(false);
      }
    },
    [currentJoke],
  );

  const reactToJoke = useCallback((reaction: 'like' | 'dislike') => {
    setCurrentJoke((current) => {
      if (!current) return current;
      const updated = {
        ...current,
        reaction: current.reaction === reaction ? undefined : reaction,
      };
      setHistory((previous) =>
        previous.map((item) => (item.id === updated.id ? updated : item)),
      );
      return updated;
    });
  }, []);

  return {
    currentJoke,
    history,
    isLoading,
    error,
    generateJoke,
    reactToJoke,
  };
}
