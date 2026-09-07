import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import JokeGenerator from './JokeGenerator';

describe('JokeGenerator', () => {
  beforeEach(() => {
    localStorage.clear();
    vi.restoreAllMocks();
  });

  it('loads a random joke and stores a reaction in history', async () => {
    vi.spyOn(globalThis, 'fetch').mockResolvedValue(
      new Response(
        JSON.stringify({
          id: 7,
          setup: 'Тестовий жарт',
          punchline: 'Тестова відповідь',
          type: 'general',
          category: 'general',
        }),
        { status: 200 },
      ),
    );
    const user = userEvent.setup();
    render(<JokeGenerator />);

    await user.click(screen.getByRole('button', { name: 'Згенерувати жарт' }));

    expect(
      await screen.findAllByText(/Тестовий жарт\s+Тестова відповідь/),
    ).toHaveLength(2);
    expect(fetch).toHaveBeenCalledWith('/api/v1/jokes/random', {
      headers: { Accept: 'application/json' },
    });

    await user.click(screen.getByRole('button', { name: '👍 Подобається' }));
    expect(screen.getByRole('button', { name: '👍 Подобається' })).toHaveAttribute(
      'aria-pressed',
      'true',
    );
    await waitFor(() =>
      expect(localStorage.getItem('joke-generator-history-v1')).toContain('"reaction":"like"'),
    );
  });

  it('uses the category endpoint and falls back to the cached joke on error', async () => {
    localStorage.setItem(
      'joke-generator-history-v1',
      JSON.stringify([
        {
          id: 'cached',
          text: 'Жарт без інтернету',
          type: 'single',
          category: 'general',
        },
      ]),
    );
    vi.spyOn(globalThis, 'fetch').mockRejectedValue(new Error('Мережа недоступна.'));
    const user = userEvent.setup();
    render(<JokeGenerator />);

    await user.selectOptions(screen.getByLabelText('Категорія'), 'programming');
    await user.click(screen.getByRole('button', { name: 'Згенерувати жарт' }));

    expect(fetch).toHaveBeenCalledWith('/api/v1/jokes/category/programming', {
      headers: { Accept: 'application/json' },
    });
    expect(await screen.findByRole('alert')).toHaveTextContent(
      'Показуємо останній збережений жарт',
    );
    expect(screen.getAllByText('Жарт без інтернету')).toHaveLength(2);
  });

  it('copies the joke when Web Share is unavailable', async () => {
    const writeText = vi.fn().mockResolvedValue(undefined);
    const user = userEvent.setup();
    Object.defineProperty(navigator, 'share', {
      configurable: true,
      value: undefined,
    });
    Object.defineProperty(navigator, 'clipboard', {
      configurable: true,
      value: { writeText },
    });
    localStorage.setItem(
      'joke-generator-history-v1',
      JSON.stringify([
        {
          id: 'share',
          text: 'Поділись мною',
          type: 'single',
          category: 'general',
        },
      ]),
    );
    render(<JokeGenerator />);

    await user.click(screen.getByRole('button', { name: '↗ Поділитися' }));

    expect(writeText).toHaveBeenCalledWith('Поділись мною');
    expect(await screen.findByRole('status')).toHaveTextContent('Жарт скопійовано!');
  });
});
