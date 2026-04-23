import { exampleData, ProductReportData } from './data/productData'
import ProductOverview from './components/report/ProductOverview'
import StrengthsCard from './components/report/StrengthsCard'
import WeaknessesCard from './components/report/WeaknessesCard'
import FeatureAnalysis from './components/report/FeatureAnalysis'
import CompetitorComparison from './components/report/CompetitorComparison'
import PurchaseRecommendation from './components/report/PurchaseRecommendation'

function App() {
  const data: ProductReportData = exampleData

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-10">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-xl font-bold text-gray-900">제품 분석 리포트</h1>
              <p className="text-sm text-gray-500">{data.meta.date} | {data.meta.storeName}</p>
            </div>
            <div className="text-right">
              <span className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-100 text-blue-800">
                추천 점수: {data.recommendation.score}/10
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-8 max-w-5xl">
        {/* Product Title */}
        <div className="mb-8 text-center">
          <h2 className="text-3xl font-bold text-gray-900 mb-2">{data.meta.productName}</h2>
          <p className="text-xl text-blue-600 font-semibold">{data.meta.price}</p>
          <a
            href={data.meta.productUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-gray-500 hover:text-blue-600 mt-2 inline-block"
          >
            스마트스토어에서 보기 &rarr;
          </a>
        </div>

        {/* Sections */}
        <div className="space-y-8">
          {/* Section 01: Overview */}
          <section id="overview" className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="bg-gray-900 text-white px-6 py-3 flex items-center gap-3">
              <span className="text-sm font-mono opacity-60">01</span>
              <h3 className="font-semibold">제품 개요</h3>
            </div>
            <div className="p-6">
              <ProductOverview data={data.overview} />
            </div>
          </section>

          {/* Section 02: Strengths */}
          <section id="strengths" className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="bg-emerald-600 text-white px-6 py-3 flex items-center gap-3">
              <span className="text-sm font-mono opacity-60">02</span>
              <h3 className="font-semibold">강점 분석</h3>
            </div>
            <div className="p-6">
              <StrengthsCard strengths={data.strengths} />
            </div>
          </section>

          {/* Section 03: Weaknesses */}
          <section id="weaknesses" className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="bg-amber-500 text-white px-6 py-3 flex items-center gap-3">
              <span className="text-sm font-mono opacity-60">03</span>
              <h3 className="font-semibold">단점 / 개선점</h3>
            </div>
            <div className="p-6">
              <WeaknessesCard weaknesses={data.weaknesses} />
            </div>
          </section>

          {/* Section 04: Feature Analysis */}
          <section id="features" className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="bg-blue-600 text-white px-6 py-3 flex items-center gap-3">
              <span className="text-sm font-mono opacity-60">04</span>
              <h3 className="font-semibold">기능별 상세 분석</h3>
            </div>
            <div className="p-6">
              <FeatureAnalysis features={data.featureAnalysis} />
            </div>
          </section>

          {/* Section 05: Competitor Comparison */}
          <section id="comparison" className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="bg-purple-600 text-white px-6 py-3 flex items-center gap-3">
              <span className="text-sm font-mono opacity-60">05</span>
              <h3 className="font-semibold">경쟁 제품 비교</h3>
            </div>
            <div className="p-6">
              <CompetitorComparison comparisons={data.competitorComparison} />
            </div>
          </section>

          {/* Section 06: Recommendation */}
          <section id="recommendation" className="bg-white rounded-xl shadow-sm border border-gray-200 overflow-hidden">
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 flex items-center gap-3">
              <span className="text-sm font-mono opacity-60">06</span>
              <h3 className="font-semibold">구매 추천</h3>
            </div>
            <div className="p-6">
              <PurchaseRecommendation recommendation={data.recommendation} />
            </div>
          </section>
        </div>

        {/* Footer */}
        <footer className="mt-12 text-center text-sm text-gray-500 pb-8">
          <p>이 리포트는 AI 분석을 기반으로 생성되었습니다.</p>
          <p className="mt-1">실제 구매 전 상세페이지와 리뷰를 추가로 확인하세요.</p>
        </footer>
      </main>
    </div>
  )
}

export default App
