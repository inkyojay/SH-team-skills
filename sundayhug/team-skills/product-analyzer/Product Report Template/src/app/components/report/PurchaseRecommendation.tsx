import { CheckCircle, XCircle } from 'lucide-react'

interface Recommendation {
  score: number;
  summary: string;
  bestFor: string[];
  notFor: string[];
}

interface PurchaseRecommendationProps {
  recommendation: Recommendation;
}

function ScoreCircle({ score }: { score: number }) {
  const getScoreColor = (score: number) => {
    if (score >= 8) return 'from-emerald-500 to-emerald-600'
    if (score >= 6) return 'from-blue-500 to-blue-600'
    if (score >= 4) return 'from-amber-500 to-amber-600'
    return 'from-red-500 to-red-600'
  }

  const getScoreLabel = (score: number) => {
    if (score >= 8) return '강력 추천'
    if (score >= 6) return '추천'
    if (score >= 4) return '보통'
    return '비추천'
  }

  return (
    <div className={`w-32 h-32 rounded-full bg-gradient-to-br ${getScoreColor(score)} flex flex-col items-center justify-center text-white shadow-lg`}>
      <span className="text-4xl font-bold">{score}</span>
      <span className="text-sm opacity-90">/10</span>
      <span className="text-xs mt-1 opacity-80">{getScoreLabel(score)}</span>
    </div>
  )
}

export default function PurchaseRecommendation({ recommendation }: PurchaseRecommendationProps) {
  return (
    <div className="space-y-6">
      {/* Score and Summary */}
      <div className="flex flex-col md:flex-row items-center gap-6">
        <ScoreCircle score={recommendation.score} />
        <div className="flex-1 text-center md:text-left">
          <h4 className="text-lg font-semibold text-gray-900 mb-2">종합 평가</h4>
          <p className="text-gray-700 leading-relaxed">{recommendation.summary}</p>
        </div>
      </div>

      {/* Best For / Not For */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Best For */}
        <div className="bg-emerald-50 rounded-lg p-4 border border-emerald-200">
          <div className="flex items-center gap-2 mb-3">
            <CheckCircle className="w-5 h-5 text-emerald-600" />
            <h5 className="font-semibold text-emerald-800">이런 분께 추천</h5>
          </div>
          <ul className="space-y-2">
            {recommendation.bestFor.map((item, index) => (
              <li key={index} className="flex items-start gap-2 text-sm text-emerald-700">
                <span className="text-emerald-500 mt-0.5">+</span>
                {item}
              </li>
            ))}
          </ul>
        </div>

        {/* Not For */}
        <div className="bg-red-50 rounded-lg p-4 border border-red-200">
          <div className="flex items-center gap-2 mb-3">
            <XCircle className="w-5 h-5 text-red-500" />
            <h5 className="font-semibold text-red-800">이런 분께 비추천</h5>
          </div>
          <ul className="space-y-2">
            {recommendation.notFor.map((item, index) => (
              <li key={index} className="flex items-start gap-2 text-sm text-red-700">
                <span className="text-red-500 mt-0.5">-</span>
                {item}
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}
