import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { UploadCloud, File, X, AlertCircle, Loader2 } from 'lucide-react';

interface FileUploaderProps {
  onUpload: (file: File) => Promise<void>;
  label?: string;
}

export default function FileUploader({ onUpload, label = "Upload Document" }: FileUploaderProps) {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setError(null);
    if (acceptedFiles.length === 0) return;
    
    const selectedFile = acceptedFiles[0];
    if (selectedFile.size > 10 * 1024 * 1024) {
      setError("File exceeds 10MB limit.");
      return;
    }
    
    setFile(selectedFile);
    setLoading(true);
    try {
      await onUpload(selectedFile);
    } catch (err: any) {
      setError(err.message || "Failed to upload document.");
      setFile(null);
    } finally {
      setLoading(false);
    }
  }, [onUpload]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'application/pdf': ['.pdf'] },
    maxFiles: 1,
    disabled: loading
  });

  return (
    <div className="w-full">
      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 text-red-700 rounded-md flex items-center gap-2" role="alert" aria-live="polite">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span className="text-sm font-medium">{error}</span>
        </div>
      )}
      
      {!file ? (
        <div
          {...getRootProps()}
          role="button"
          tabIndex={0}
          className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:outline-none
            ${isDragActive ? 'border-indigo-500 bg-indigo-50' : 'border-slate-300 hover:border-slate-400 bg-white'}`}
        >
          <input {...getInputProps()} />
          <UploadCloud className="mx-auto h-12 w-12 text-slate-400 mb-4" aria-hidden="true" />
          <p className="text-sm font-medium text-slate-900 mb-1">
            {isDragActive ? "Drop the PDF here" : `Drag & drop or click to ${label.toLowerCase()}`}
          </p>
          <p className="text-xs text-slate-500">PDF files only, up to 10MB</p>
        </div>
      ) : (
        <div className="border rounded-xl p-4 bg-white flex items-center justify-between shadow-sm">
          <div className="flex items-center gap-3 overflow-hidden">
            <div className="p-2 bg-indigo-50 text-indigo-600 rounded-lg shrink-0">
              <File className="w-6 h-6" />
            </div>
            <div className="truncate">
              <p className="text-sm font-semibold text-slate-900 truncate">{file.name}</p>
              <p className="text-xs text-slate-500">{(file.size / 1024 / 1024).toFixed(2)} MB</p>
            </div>
          </div>
          <div className="ml-4 shrink-0">
            {loading ? (
              <div className="flex items-center gap-2 text-sm text-indigo-600 font-medium">
                <Loader2 className="w-5 h-5 animate-spin" />
                <span aria-live="polite">Analyzing...</span>
              </div>
            ) : (
              <button 
                onClick={() => setFile(null)}
                className="p-1 text-slate-400 hover:text-slate-600 focus-visible:ring-2 focus-visible:ring-indigo-500 rounded"
                aria-label="Remove file"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
