import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import Navbar from '../../../frontend/src/components/Navbar';

describe('Navbar Component', () => {
  it('renders Legal Lens brand title and link', () => {
    render(<Navbar />);
    const brandLink = screen.getByRole('link', { name: /Legal Lens/i });
    expect(brandLink).toBeInTheDocument();
    expect(brandLink).toHaveAttribute('href', '/');
  });
});
