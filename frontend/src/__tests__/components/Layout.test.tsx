import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import Layout from '../../components/Layout';

describe('Layout Component', () => {
  it('renders children correctly', () => {
    render(
      <BrowserRouter>
        <Layout>
          <div>Test Content</div>
        </Layout>
      </BrowserRouter>
    );

    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('renders navigation elements', () => {
    render(
      <BrowserRouter>
        <Layout>
          <div>Content</div>
        </Layout>
      </BrowserRouter>
    );

    // Check for navigation or header elements
    // Adjust based on actual Layout implementation
    const layoutElement = document.querySelector('nav') || document.querySelector('header');
    expect(layoutElement).toBeTruthy();
  });
});
