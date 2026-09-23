import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import FileUploader from '../../../frontend/src/components/FileUploader';

describe('FileUploader Component', () => {
  it('renders default dropzone prompt', () => {
    render(<FileUploader onUpload={async () => {}} label="Upload Document" />);
    expect(screen.getByText(/Drag & drop or click to upload document/i)).toBeInTheDocument();
  });

  it('shows error when file exceeds 10MB limit', async () => {
    render(<FileUploader onUpload={async () => {}} />);
    
    // Create a 11MB file dummy
    const largeFile = new File([new ArrayBuffer(11 * 1024 * 1024)], 'large.pdf', { type: 'application/pdf' });
    const input = screen.getByRole('button').querySelector('input')!;
    
    fireEvent.change(input, { target: { files: [largeFile] } });

    await waitFor(() => {
      expect(screen.getByText('File exceeds 10MB limit.')).toBeInTheDocument();
    });
  });

  it('triggers onUpload callback and shows loading state', async () => {
    const mockUpload = vi.fn().mockImplementation(() => new Promise((resolve) => setTimeout(resolve, 50)));
    render(<FileUploader onUpload={mockUpload} />);

    const validFile = new File(['pdf content'], 'sample.pdf', { type: 'application/pdf' });
    const input = screen.getByRole('button').querySelector('input')!;

    fireEvent.change(input, { target: { files: [validFile] } });

    await waitFor(() => {
      expect(mockUpload).toHaveBeenCalledWith(validFile);
      expect(screen.getByText('sample.pdf')).toBeInTheDocument();
    });
  });
});
