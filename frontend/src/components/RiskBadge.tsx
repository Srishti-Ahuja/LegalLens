import { AlertTriangle, CheckCircle, Info } from 'lucide-react';
import { RiskItem } from '../lib/api';

export default function RiskBadge({ risk }: { risk: RiskItem }) {
  const getStyle = () => {
    switch (risk.severity) {
      case 'High':
        return {
          bg: 'bg-red-50',
          border: 'border-red-200',
          text: 'text-red-700',
          icon: <AlertTriangle className="w-5 h-5 text-red-600" aria-hidden="true" />,
          label: 'HIGH RISK'
        };
      case 'Medium':
        return {
          bg: 'bg-amber-50',
          border: 'border-amber-200',
          text: 'text-amber-700',
          icon: <Info className="w-5 h-5 text-amber-600" aria-hidden="true" />,
          label: 'WARNING'
        };
      case 'Low':
      default:
        return {
          bg: 'bg-emerald-50',
          border: 'border-emerald-200',
          text: 'text-emerald-700',
          icon: <CheckCircle className="w-5 h-5 text-emerald-600" aria-hidden="true" />,
          label: 'SAFE'
        };
    }
  };

  const style = getStyle();

  return (
    <div className={`p-4 rounded-lg border ${style.bg} ${style.border} mb-4 shadow-sm`}>
      <div className="flex items-start gap-3">
        <div className="flex-shrink-0 mt-0.5">{style.icon}</div>
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <span className={`text-xs font-bold px-2 py-0.5 rounded uppercase tracking-wide ${style.text} bg-white border ${style.border}`}>
              {style.label}
            </span>
          </div>
          <h4 className="text-sm font-semibold text-slate-900 mb-1">{risk.clause}</h4>
          <p className="text-sm text-slate-700">{risk.rationale}</p>
        </div>
      </div>
    </div>
  );
}
