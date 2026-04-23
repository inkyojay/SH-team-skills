import { TrendingUp, Minus, TrendingDown } from 'lucide-react'

interface Comparison {
  aspect: string;
  thisProduct: string;
  competitors: string;
  verdict: 'advantage' | 'similar' | 'disadvantage';
}

interface CompetitorComparisonProps {
  comparisons: Comparison[];
}

const verdictConfig = {
  advantage: {
    icon: TrendingUp,
    label: '우위',
    color: 'text-emerald-600',
    bg: 'bg-emerald-50',
    border: 'border-emerald-200',
  },
  similar: {
    icon: Minus,
    label: '유사',
    color: 'text-blue-600',
    bg: 'bg-blue-50',
    border: 'border-blue-200',
  },
  disadvantage: {
    icon: TrendingDown,
    label: '열위',
    color: 'text-red-500',
    bg: 'bg-red-50',
    border: 'border-red-200',
  },
}

export default function CompetitorComparison({ comparisons }: CompetitorComparisonProps) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead>
          <tr className="border-b-2 border-gray-200">
            <th className="text-left py-3 px-4 font-semibold text-gray-700 w-1/6">비교 항목</th>
            <th className="text-left py-3 px-4 font-semibold text-blue-600 w-1/3">이 제품</th>
            <th className="text-left py-3 px-4 font-semibold text-gray-500 w-1/3">경쟁 제품</th>
            <th className="text-center py-3 px-4 font-semibold text-gray-700 w-1/6">평가</th>
          </tr>
        </thead>
        <tbody>
          {comparisons.map((comparison, index) => {
            const verdict = verdictConfig[comparison.verdict]
            const Icon = verdict.icon
            return (
              <tr key={index} className="border-b border-gray-100 hover:bg-gray-50">
                <td className="py-4 px-4">
                  <span className="font-medium text-gray-900">{comparison.aspect}</span>
                </td>
                <td className="py-4 px-4">
                  <span className="text-sm text-gray-700">{comparison.thisProduct}</span>
                </td>
                <td className="py-4 px-4">
                  <span className="text-sm text-gray-500">{comparison.competitors}</span>
                </td>
                <td className="py-4 px-4">
                  <div className="flex justify-center">
                    <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium ${verdict.bg} ${verdict.color} border ${verdict.border}`}>
                      <Icon className="w-4 h-4" />
                      {verdict.label}
                    </span>
                  </div>
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>

      {/* Summary */}
      <div className="mt-4 p-4 bg-gray-50 rounded-lg">
        <div className="flex items-center gap-6 justify-center">
          {Object.entries(verdictConfig).map(([key, config]) => {
            const count = comparisons.filter(c => c.verdict === key).length
            const Icon = config.icon
            return (
              <div key={key} className="flex items-center gap-2">
                <Icon className={`w-4 h-4 ${config.color}`} />
                <span className="text-sm text-gray-600">{config.label}:</span>
                <span className={`font-bold ${config.color}`}>{count}</span>
              </div>
            )
          })}
        </div>
      </div>
    </div>
  )
}
