import { DiffItem } from '../lib/api';
import { AlertTriangle, Info, CheckCircle } from 'lucide-react';

export default function DiffMatrix({ diffs }: { diffs: DiffItem[] }) {
  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'High': return <AlertTriangle className="w-5 h-5 text-red-600" aria-label="High severity" />;
      case 'Medium': return <Info className="w-5 h-5 text-amber-600" aria-label="Medium severity" />;
      case 'Low':
      default: return <CheckCircle className="w-5 h-5 text-emerald-600" aria-label="Low severity" />;
    }
  };

  return (
    <div className="overflow-x-auto rounded-xl border border-slate-200 bg-white shadow-sm">
      <table className="min-w-full divide-y divide-slate-200">
        <thead className="bg-slate-50">
          <tr>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider w-1/5">
              Topic / Issue
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider w-1/12">
              Impact
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider w-[35%]">
              Original Contract (Version A)
            </th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-slate-500 uppercase tracking-wider w-[35%]">
              Modified Contract (Version B)
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-slate-200">
          {diffs.map((diff, idx) => (
            <tr key={idx} className="hover:bg-slate-50 transition-colors">
              <td className="px-6 py-4 text-sm font-semibold text-slate-900 align-top">
                {diff.topic}
              </td>
              <td className="px-6 py-4 text-sm text-slate-500 align-top whitespace-nowrap">
                <div className="flex items-center gap-1.5" title={diff.severity}>
                   {getSeverityIcon(diff.severity)}
                   <span className="sr-only">{diff.severity} Severity</span>
                </div>
              </td>
              <td className="px-6 py-4 text-sm text-slate-700 align-top whitespace-pre-wrap bg-red-50/30">
                {diff.version_a || <span className="text-slate-400 italic">Not present in Original</span>}
              </td>
              <td className="px-6 py-4 text-sm text-slate-700 align-top whitespace-pre-wrap bg-emerald-50/30">
                {diff.version_b || <span className="text-slate-400 italic">Removed in Modified version</span>}
              </td>
            </tr>
          ))}
          {diffs.length === 0 && (
             <tr>
                <td colSpan={4} className="px-6 py-12 text-center text-sm text-slate-500">
                   No substantial differences found between these contracts.
                </td>
             </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}
