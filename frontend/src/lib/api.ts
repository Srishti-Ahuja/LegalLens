const API_URL = process.env.NEXT_PUBLIC_API_URL || 'https://legallens-2-6sro.onrender.com/api';

export interface RiskItem {
  clause: string;
  severity: 'Low' | 'Medium' | 'High';
  rationale: string;
}

export interface AnalysisResult {
  document_id: string;
  summary: string;
  risks: RiskItem[];
}

export interface DiffItem {
  topic: string;
  version_a: string;
  version_b: string;
  severity: 'Low' | 'Medium' | 'High';
}

export const uploadDocument = async (file: File): Promise<AnalysisResult> => {
  const formData = new FormData();
  formData.append('file', file);

  console.log('[DEBUG] NEXT_PUBLIC_API_URL is:', process.env.NEXT_PUBLIC_API_URL);
  console.log('[DEBUG] Computed API_URL is:', API_URL);
  console.log('[DEBUG] Fetching from:', `${API_URL}/upload/`);

  try {
    const res = await fetch(`${API_URL}/upload/`, {
      method: 'POST',
      body: formData,
    });

    console.log('[DEBUG] Fetch response status:', res.status, res.ok);

    if (!res.ok) {
      const errText = await res.text();
      console.error('[DEBUG] Fetch error response body:', errText);
      let errMsg = 'Upload failed';
      try {
        const errJson = JSON.parse(errText);
        errMsg = errJson.message || errMsg;
      } catch (e) {}
      throw new Error(errMsg);
    }

    return await res.json();
  } catch (error) {
    console.error('[DEBUG] Fetch threw an error:', error);
    throw error;
  }
};

export const chatDocument = async (query: string, document_id: string): Promise<string> => {
  const res = await fetch(`${API_URL}/chat/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ query, document_id }),
  });

  if (!res.ok) {
    throw new Error('Chat failed');
  }

  const data = await res.json();
  return data.answer;
};

export const compareDocuments = async (fileA: File, fileB: File): Promise<DiffItem[]> => {
    const formData = new FormData();
    formData.append('file_a', fileA);
    formData.append('file_b', fileB);
  
    const res = await fetch(`${API_URL}/compare/`, {
      method: 'POST',
      body: formData,
    });
  
    if (!res.ok) {
      throw new Error('Comparison failed');
    }
  
    const data = await res.json();
    return data.diff;
  };
