import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import DiffMatrix from '../../../frontend/src/components/DiffMatrix';
import { DiffItem } from '../../../frontend/src/lib/api';

describe('DiffMatrix Component', () => {
  it('renders diff rows with topics and versions', () => {
    const diffs: DiffItem[] = [
      {
        topic: 'Notice Period',
        version_a: '30 days written notice',
        version_b: '60 days written notice',
        severity: 'Medium',
      },
    ];

    render(<DiffMatrix diffs={diffs} />);
    expect(screen.getByText('Notice Period')).toBeInTheDocument();
    expect(screen.getByText('30 days written notice')).toBeInTheDocument();
    expect(screen.getByText('60 days written notice')).toBeInTheDocument();
  });

  it('renders empty message when diff list is empty', () => {
    render(<DiffMatrix diffs={[]} />);
    expect(screen.getByText(/No substantial differences found between these contracts/i)).toBeInTheDocument();
  });
});
