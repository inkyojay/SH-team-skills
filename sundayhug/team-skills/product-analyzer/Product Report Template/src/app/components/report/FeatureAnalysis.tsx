import { ThumbsUp, ThumbsDown } from 'lucide-react'

interface Feature {
  feature: string;
  score: number;
  evidence: string;
  pros: string[];
  cons: string[];
}

interface FeatureAnalysisProps {
  features: Feature[];
}

function ScoreBar({ score }: { score: number }) {
  const percentage = (score / 5) * 100
  const colors = {
    1: 'bg-red-500',
    2: 'bg-orange-500',
    3: 'bg-yellow-500',
    4: 'bg-blue-500',
    5: 'bg-emerald-500',
  }
  const color = colors[score as keyof typeof colors] || 'bg-gray-400'

  return (
    <div className="flex items-center gap-3">
      <div className="flex-1 h-2 bg-gray-200 rounded-full overflow-hidden">
        <div
          className={`h-full ${color} transition-all duration-500`}
          style={{ width: `${percentage}%` }}
        />
      </div>
      <span className="text-lg font-bold text-gray-900 w-8 text-right">{score}</span>
      <span className="text-sm text-gray-500">/5</span>
    </div>
  )
}

export default function FeatureAnalysis({ features }: FeatureAnalysisProps) {
  return (
    <div className="space-y-6">
      {features.map((feature, index) => (
        <div key={index} className="border border-gray-200 rounded-lg overflow-hidden">
          {/* Header */}
          <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
            <div className="flex items-center justify-between">
              <h4 className="font-semibold text-gray-900">{feature.feature}</h4>
              <ScoreBar score={feature.score} />
            </div>
          </div>

          {/* Content */}
          <div className="p-4 space-y-4">
            {/* Evidence */}
            <p className="text-sm text-gray-600 bg-blue-50 px-3 py-2 rounded">
              {feature.evidence}
            </p>

            {/* Pros & Cons */}
            <div className="grid md:grid-cols-2 gap-4">
              {/* Pros */}
              {feature.pros.length > 0 && (
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <ThumbsUp className="w-4 h-4 text-emerald-600" />
                    <span className="text-sm font-medium text-emerald-600">장점</span>
                  </div>
                  <ul className="space-y-1">
                    {feature.pros.map((pro, i) => (
                      <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                        <span className="text-emerald-500 mt-1">+</span>
                        {pro}
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* Cons */}
              {feature.cons.length > 0 && (
                <div>
                  <div className="flex items-center gap-2 mb-2">
                    <ThumbsDown className="w-4 h-4 text-red-500" />
                    <span className="text-sm font-medium text-red-500">단점</span>
                  </div>
                  <ul className="space-y-1">
                    {feature.cons.map((con, i) => (
                      <li key={i} className="text-sm text-gray-700 flex items-start gap-2">
                        <span className="text-red-500 mt-1">-</span>
                        {con}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
