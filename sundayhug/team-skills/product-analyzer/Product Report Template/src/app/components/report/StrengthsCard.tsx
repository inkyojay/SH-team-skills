import { Zap, Palette, DollarSign, Star, ChevronRight } from 'lucide-react'

interface Strength {
  title: string;
  description: string;
  category: 'function' | 'design' | 'price' | 'unique';
  importance: 'high' | 'medium' | 'low';
}

interface StrengthsCardProps {
  strengths: Strength[];
}

const categoryIcons = {
  function: Zap,
  design: Palette,
  price: DollarSign,
  unique: Star,
}

const categoryLabels = {
  function: '기능',
  design: '디자인',
  price: '가격',
  unique: '차별화',
}

const importanceColors = {
  high: 'bg-emerald-100 text-emerald-700 border-emerald-200',
  medium: 'bg-blue-100 text-blue-700 border-blue-200',
  low: 'bg-gray-100 text-gray-600 border-gray-200',
}

export default function StrengthsCard({ strengths }: StrengthsCardProps) {
  return (
    <div className="space-y-4">
      {strengths.map((strength, index) => {
        const Icon = categoryIcons[strength.category]
        return (
          <div
            key={index}
            className={`p-4 rounded-lg border-2 ${importanceColors[strength.importance]} transition-all hover:shadow-md`}
          >
            <div className="flex items-start gap-4">
              <div className="flex-shrink-0 w-10 h-10 bg-white rounded-lg flex items-center justify-center shadow-sm">
                <Icon className="w-5 h-5" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <h4 className="font-semibold text-gray-900">{strength.title}</h4>
                  <span className="text-xs px-2 py-0.5 rounded bg-white/50">
                    {categoryLabels[strength.category]}
                  </span>
                  {strength.importance === 'high' && (
                    <span className="text-xs px-2 py-0.5 rounded bg-emerald-600 text-white">
                      핵심
                    </span>
                  )}
                </div>
                <p className="text-sm text-gray-700">{strength.description}</p>
              </div>
              <ChevronRight className="w-5 h-5 text-gray-400 flex-shrink-0" />
            </div>
          </div>
        )
      })}
    </div>
  )
}
