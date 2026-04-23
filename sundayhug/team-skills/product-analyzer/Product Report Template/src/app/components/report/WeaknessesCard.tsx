import { AlertCircle, HelpCircle, AlertTriangle } from 'lucide-react'

interface Weakness {
  title: string;
  description: string;
  category: 'function' | 'info' | 'concern';
  severity: 'high' | 'medium' | 'low';
}

interface WeaknessesCardProps {
  weaknesses: Weakness[];
}

const categoryIcons = {
  function: AlertCircle,
  info: HelpCircle,
  concern: AlertTriangle,
}

const categoryLabels = {
  function: '기능 한계',
  info: '정보 부족',
  concern: '우려 사항',
}

const severityStyles = {
  high: {
    border: 'border-red-200',
    bg: 'bg-red-50',
    badge: 'bg-red-600 text-white',
    badgeText: '주의',
  },
  medium: {
    border: 'border-amber-200',
    bg: 'bg-amber-50',
    badge: 'bg-amber-500 text-white',
    badgeText: '참고',
  },
  low: {
    border: 'border-gray-200',
    bg: 'bg-gray-50',
    badge: 'bg-gray-400 text-white',
    badgeText: '사소',
  },
}

export default function WeaknessesCard({ weaknesses }: WeaknessesCardProps) {
  return (
    <div className="space-y-4">
      {weaknesses.map((weakness, index) => {
        const Icon = categoryIcons[weakness.category]
        const style = severityStyles[weakness.severity]
        return (
          <div
            key={index}
            className={`p-4 rounded-lg border-2 ${style.border} ${style.bg}`}
          >
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0 w-10 h-10 bg-white rounded-lg flex items-center justify-center shadow-sm">
                <Icon className="w-5 h-5 text-amber-600" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="font-semibold text-gray-900">{weakness.title}</h4>
                  <span className="text-xs px-2 py-0.5 rounded bg-white/80 text-gray-600">
                    {categoryLabels[weakness.category]}
                  </span>
                  <span className={`text-xs px-2 py-0.5 rounded ${style.badge}`}>
                    {style.badgeText}
                  </span>
                </div>
                <p className="text-sm text-gray-700">{weakness.description}</p>
              </div>
            </div>
          </div>
        )
      })}
    </div>
  )
}
