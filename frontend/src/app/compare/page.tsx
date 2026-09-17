'use client';

import { useState } from 'react';
import { ArrowRight, Loader2 } from 'lucide-react';
import FileUploader from '../../components/FileUploader';
import DiffMatrix from '../../components/DiffMatrix';
import { DiffItem } from '../../lib/api';

export default function ComparePage() {
  const [fileA, setFileA] = useState<File | null>(null);
  const [fileB, setFileB] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [diffs, setDiffs] = useState<DiffItem[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleCompare = async () => {
    if (!fileA || !fileB) return;
    
    setLoading(true);
    setError(null);
    try {
      const { compareDocuments } = await import('../../lib/api');
      const result = await compareDocuments(fileA, fileB);
      setDiffs(result);
    } catch (err: any) {
      setError(err.message || 'Failed to compare documents.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col gap-8 pb-12">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold text-slate-900">Compare Contracts</h1>
        <p className="text-slate-600 max-w-2xl">
          Upload an original contract and a modified version. Our AI will analyze both documents line-by-line and generate a structured matrix of material changes, insertions, and deletions.
        </p>
      </div>

      {!diffs ? (
        <div className="flex flex-col gap-8 max-w-4xl">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-start relative">
            <div className="flex flex-col gap-3">
              <h3 className="font-semibold text-slate-800 flex items-center gap-2">
                <span className="bg-indigo-100 text-indigo-700 w-6 h-6 rounded-full flex items-center justify-center text-xs">A</span> 
                Original Contract
              </h3>
              <FileUploader 
                label="Original Version"
                onUpload={async (file) => { setFileA(file); }} 
              />
            </div>
            
            <div className="hidden md:flex absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 mt-3 text-slate-300">
               <ArrowRight className="w-8 h-8" />
            </div>

            <div className="flex flex-col gap-3">
              <h3 className="font-semibold text-slate-800 flex items-center gap-2">
                <span className="bg-amber-100 text-amber-700 w-6 h-6 rounded-full flex items-center justify-center text-xs">B</span>
                Modified Contract
              </h3>
              <FileUploader 
                label="Modified Version"
                onUpload={async (file) => { setFileB(file); }} 
              />
            </div>
          </div>
          
          {error && (
            <div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-lg text-sm">
              {error}
            </div>
          )}

          <div className="flex justify-center pt-4">
            <button
              onClick={handleCompare}
              disabled={!fileA || !fileB || loading}
              className="bg-indigo-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-indigo-500 transition-colors flex items-center gap-2 shadow-sm"
            >
              {loading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  Generating Difference Matrix...
                </>
              ) : (
                'Compare Contracts'
              )}
            </button>
          </div>
        </div>
      ) : (
        <div className="flex flex-col gap-6 animate-in fade-in slide-in-from-bottom-4 duration-500">
          <div className="flex justify-between items-center bg-white p-4 rounded-xl border shadow-sm">
            <div className="flex gap-6">
               <div className="flex flex-col">
                  <span className="text-xs text-slate-500 font-medium uppercase">Version A</span>
                  <span className="text-sm font-semibold truncate max-w-[200px]" title={fileA?.name}>{fileA?.name}</span>
               </div>
               <div className="flex flex-col">
                  <span className="text-xs text-slate-500 font-medium uppercase">Version B</span>
                  <span className="text-sm font-semibold truncate max-w-[200px]" title={fileB?.name}>{fileB?.name}</span>
               </div>
            </div>
            <button 
              onClick={() => {
                setDiffs(null);
                setFileA(null);
                setFileB(null);
              }}
              className="text-sm text-indigo-600 font-medium hover:text-indigo-800"
            >
              Start New Comparison
            </button>
          </div>
          
          <DiffMatrix diffs={diffs} />
        </div>
      )}
    </div>
  );
}
