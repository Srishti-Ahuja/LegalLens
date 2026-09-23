import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import RiskBadge from '../../../frontend/src/components/RiskBadge';
import { RiskItem } from '../../../frontend/src/lib/api';

describe('RiskBadge Component', () => {
  it('renders High risk badge correctly', () => {
    const risk: RiskItem = {
      clause: 'Unilateral Termination Clause',
      severity: 'High',
      rationale: 'Company can cancel without notice.',
    };

    render(<RiskBadge risk={risk} />);
    expect(screen.getByText('HIGH RISK')).toBeInTheDocument();
    expect(screen.getByText('Unilateral Termination Clause')).toBeInTheDocument();
    expect(screen.getByText('Company can cancel without notice.')).toBeInTheDocument();
  });

  it('renders Warning badge for Medium severity', () => {
    const risk: RiskItem = {
      clause: 'Automatic Renewal',
      severity: 'Medium',
      rationale: 'Renews annually unless opted out 60 days prior.',
    };

    render(<RiskBadge risk={risk} />);
    expect(screen.getByText('WARNING')).toBeInTheDocument();
    expect(screen.getByText('Automatic Renewal')).toBeInTheDocument();
  });

  it('renders SAFE badge for Low severity', () => {
    const risk: RiskItem = {
      clause: 'Standard Governing Law',
      severity: 'Low',
      rationale: 'Delaware state law applies.',
    };

    render(<RiskBadge risk={risk} />);
    expect(screen.getByText('SAFE')).toBeInTheDocument();
  });
});
