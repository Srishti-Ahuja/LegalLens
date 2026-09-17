'use client';

import { useState } from 'react';
import FileUploader from '../components/FileUploader';
import RiskBadge from '../components/RiskBadge';
import ChatInterface from '../components/ChatInterface';
import { AnalysisResult } from '../lib/api';

export default function Home() {
  const [analysis, setAnalysis] = useState<AnalysisResult | null>(null);
  const [activeTab, setActiveTab] = useState<'summary' | 'risks'>('summary');

  return (
    <div className="flex flex-col gap-6 h-[calc(100vh-8rem)]">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold text-slate-900">Document Analysis</h1>
        <p className="text-slate-600">Upload a legal contract to instantly extract key terms, identify risks, and ask questions.</p>
      </div>

      <div className="w-full max-w-3xl">
        <FileUploader 
          onUpload={async (file) => {
            const { uploadDocument } = await import('../lib/api');
            const result = await uploadDocument(file);
            setAnalysis(result);
          }} 
        />
      </div>

      {analysis && (
        <div className="flex-1 flex flex-col md:flex-row gap-6 min-h-0 pb-4">
          {/* Left Panel: Tabs for Summary and Risks */}
          <div className="w-full md:w-3/5 flex flex-col bg-white border rounded-xl shadow-sm overflow-hidden min-h-[400px]">
            <div className="flex border-b border-slate-200">
              <button
                className={`flex-1 py-3 px-4 text-sm font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-indigo-500 transition-colors ${
                  activeTab === 'summary' 
                    ? 'border-b-2 border-indigo-600 text-indigo-600 bg-indigo-50/50' 
                    : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
                }`}
                onClick={() => setActiveTab('summary')}
              >
                Plain English Summary
              </button>
              <button
                className={`flex-1 py-3 px-4 text-sm font-medium focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-inset focus-visible:ring-indigo-500 transition-colors ${
                  activeTab === 'risks' 
                    ? 'border-b-2 border-indigo-600 text-indigo-600 bg-indigo-50/50' 
                    : 'text-slate-500 hover:text-slate-700 hover:bg-slate-50'
                }`}
                onClick={() => setActiveTab('risks')}
              >
                Risk Matrix ({analysis.risks.length})
              </button>
            </div>
            
            <div className="flex-1 overflow-y-auto p-6">
              {activeTab === 'summary' ? (
                <div className="prose prose-slate prose-sm max-w-none">
                  {/* Gemini's summary is returned as plain text/markdown. Using simple formatting here. */}
                  {analysis.summary.split('\n').map((line, i) => (
                    <p key={i} className="mb-2">{line.replace(/\*\*/g, '')}</p> 
                  ))}
                </div>
              ) : (
                <div className="flex flex-col gap-1">
                  {analysis.risks.length === 0 ? (
                    <p className="text-sm text-slate-500 italic text-center py-8">No significant risks identified.</p>
                  ) : (
                    analysis.risks.map((risk, idx) => (
                      <RiskBadge key={idx} risk={risk} />
                    ))
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Right Panel: Chat Interface */}
          <div className="w-full md:w-2/5 min-h-[400px]">
            <ChatInterface documentId={analysis.document_id} />
          </div>
        </div>
      )}
    </div>
  );
}
