import { describe, it, expect, vi, beforeEach } from 'vitest';
import { uploadDocument, chatDocument, compareDocuments } from '../../../frontend/src/lib/api';

describe('Frontend API wrapper functions', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn());
  });

  describe('uploadDocument', () => {
    it('sends POST request and returns analysis result on success', async () => {
      const mockResult = {
        document_id: 'doc-123',
        summary: 'Plain summary',
        risks: [{ clause: 'Clause 1', severity: 'High', rationale: 'Risky' }],
      };

      (fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResult,
      });

      const dummyFile = new File(['pdf content'], 'test.pdf', { type: 'application/pdf' });
      const result = await uploadDocument(dummyFile);

      expect(fetch).toHaveBeenCalledTimes(1);
      expect(result).toEqual(mockResult);
    });

    it('throws error with server message when upload fails', async () => {
      (fetch as any).mockResolvedValueOnce({
        ok: false,
        text: async () => JSON.stringify({ message: 'Only PDF files are supported.' }),
      });

      const dummyFile = new File(['text content'], 'test.txt', { type: 'text/plain' });
      await expect(uploadDocument(dummyFile)).rejects.toThrow('Only PDF files are supported.');
    });
  });

  describe('chatDocument', () => {
    it('sends POST request and returns answer text', async () => {
      (fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ answer: 'The termination clause is 30 days.' }),
      });

      const answer = await chatDocument('What is termination clause?', 'doc-123');
      expect(answer).toBe('The termination clause is 30 days.');
    });

    it('throws error when chat fails', async () => {
      (fetch as any).mockResolvedValueOnce({
        ok: false,
      });

      await expect(chatDocument('Query', 'doc-123')).rejects.toThrow('Chat failed');
    });
  });

  describe('compareDocuments', () => {
    it('sends POST request with two files and returns diff list', async () => {
      const mockDiff = [
        { topic: 'Liability', version_a: '1M', version_b: '2M', severity: 'Medium' },
      ];

      (fetch as any).mockResolvedValueOnce({
        ok: true,
        json: async () => ({ diff: mockDiff }),
      });

      const fileA = new File(['a'], 'a.pdf', { type: 'application/pdf' });
      const fileB = new File(['b'], 'b.pdf', { type: 'application/pdf' });

      const diff = await compareDocuments(fileA, fileB);
      expect(diff).toEqual(mockDiff);
    });

    it('throws error when comparison fails', async () => {
      (fetch as any).mockResolvedValueOnce({
        ok: false,
      });

      const fileA = new File(['a'], 'a.pdf', { type: 'application/pdf' });
      const fileB = new File(['b'], 'b.pdf', { type: 'application/pdf' });

      await expect(compareDocuments(fileA, fileB)).rejects.toThrow('Comparison failed');
    });
  });
});
