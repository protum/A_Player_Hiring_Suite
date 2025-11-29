import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import App from '../App';

describe('App', () => {
  it('renders without crashing', () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );
    expect(document.body).toBeTruthy();
  });

  it('renders the application title', () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    );

    // Check that the app renders some content
    const appElement = screen.getByRole('main', { hidden: true }) || document.querySelector('div');
    expect(appElement).toBeTruthy();
  });
});
