import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import ChatInterface from '../../../frontend/src/components/ChatInterface';
import * as api from '../../../frontend/src/lib/api';

vi.mock('../../../frontend/src/lib/api', () => ({
  chatDocument: vi.fn(),
}));

describe('ChatInterface Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders initial assistant greeting', () => {
    render(<ChatInterface documentId="doc-123" />);
    expect(screen.getByText(/Hello! I have analyzed this document/i)).toBeInTheDocument();
  });

  it('handles submitting user question and displays answer', async () => {
    (api.chatDocument as any).mockResolvedValueOnce('The agreement term is 12 months.');

    render(<ChatInterface documentId="doc-123" />);

    const input = screen.getByPlaceholderText('Ask a question...');
    const submitBtn = screen.getByRole('button', { name: /Send message/i });

    fireEvent.change(input, { target: { value: 'What is the agreement term?' } });
    fireEvent.click(submitBtn);

    expect(screen.getByText('What is the agreement term?')).toBeInTheDocument();

    await waitFor(() => {
      expect(api.chatDocument).toHaveBeenCalledWith('What is the agreement term?', 'doc-123');
      expect(screen.getByText('The agreement term is 12 months.')).toBeInTheDocument();
    });
  });

  it('displays error message when chat API fails', async () => {
    (api.chatDocument as any).mockRejectedValueOnce(new Error('Network error'));

    render(<ChatInterface documentId="doc-123" />);

    const input = screen.getByPlaceholderText('Ask a question...');
    const submitBtn = screen.getByRole('button', { name: /Send message/i });

    fireEvent.change(input, { target: { value: 'Faulty query' } });
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(screen.getByText(/Sorry, I encountered an error while answering your question/i)).toBeInTheDocument();
    });
  });
});
