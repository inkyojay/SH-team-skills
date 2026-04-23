import { Package, Users, Sparkles } from 'lucide-react'

interface ProductOverviewProps {
  data: {
    category: string;
    targetAudience: string;
    coreFeatures: string[];
    summary: string;
  };
}

export default function ProductOverview({ data }: ProductOverviewProps) {
  return (
    <div className="space-y-6">
      {/* Summary */}
      <div className="bg-blue-50 rounded-lg p-4 border-l-4 border-blue-500">
        <p className="text-gray-800 font-medium">{data.summary}</p>
      </div>

      {/* Grid */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Category */}
        <div className="flex gap-4">
          <div className="flex-shrink-0 w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
            <Package className="w-5 h-5 text-gray-600" />
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-500 mb-1">카테고리</h4>
            <p className="text-gray-900">{data.category}</p>
          </div>
        </div>

        {/* Target Audience */}
        <div className="flex gap-4">
          <div className="flex-shrink-0 w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
            <Users className="w-5 h-5 text-gray-600" />
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-500 mb-1">타겟 고객</h4>
            <p className="text-gray-900">{data.targetAudience}</p>
          </div>
        </div>
      </div>

      {/* Core Features */}
      <div>
        <div className="flex items-center gap-2 mb-3">
          <Sparkles className="w-5 h-5 text-blue-600" />
          <h4 className="font-semibold text-gray-900">핵심 기능</h4>
        </div>
        <div className="flex flex-wrap gap-2">
          {data.coreFeatures.map((feature, index) => (
            <span
              key={index}
              className="inline-flex items-center px-3 py-1.5 rounded-full text-sm bg-gray-100 text-gray-800"
            >
              {feature}
            </span>
          ))}
        </div>
      </div>
    </div>
  )
}
