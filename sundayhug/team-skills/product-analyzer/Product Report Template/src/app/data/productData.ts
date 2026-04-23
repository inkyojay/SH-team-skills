export interface ProductReportData {
  meta: {
    date: string;
    productName: string;
    storeName: string;
    productUrl: string;
    price: string;
  };
  overview: {
    category: string;
    targetAudience: string;
    coreFeatures: string[];
    summary: string;
  };
  strengths: {
    title: string;
    description: string;
    category: 'function' | 'design' | 'price' | 'unique';
    importance: 'high' | 'medium' | 'low';
  }[];
  weaknesses: {
    title: string;
    description: string;
    category: 'function' | 'info' | 'concern';
    severity: 'high' | 'medium' | 'low';
  }[];
  featureAnalysis: {
    feature: string;
    score: number;
    evidence: string;
    pros: string[];
    cons: string[];
  }[];
  competitorComparison: {
    aspect: string;
    thisProduct: string;
    competitors: string;
    verdict: 'advantage' | 'similar' | 'disadvantage';
  }[];
  recommendation: {
    score: number;
    summary: string;
    bestFor: string[];
    notFor: string[];
  };
  images: {
    thumbnail: string;
    detailImages: string[];
  };
}

export const exampleData: ProductReportData = {
  "meta": {
    "date": "2026-01-14",
    "productName": "리안 벨라 유모차",
    "storeName": "리안베이비",
    "productUrl": "https://ryanbaby.co.kr/product/리안-벨라-기내반입-휴대용-유모차/5129/",
    "price": "498,000원"
  },
  "overview": {
    "category": "유아용품 > 유모차 > 휴대용/절충형 유모차",
    "targetAudience": "여행을 자주 다니는 가족, 도심에서 대중교통을 이용하는 부모, 세컨드 유모차를 찾는 가정",
    "coreFeatures": [
      "기내반입 가능 (컴팩트 폴딩)",
      "어깨끈 휴대 가능",
      "5점식 안전벨트",
      "다양한 컬러 옵션",
      "방풍커버/스낵트레이 사은품"
    ],
    "summary": "도심과 여행에 최적화된 프리미엄 휴대용 유모차. 세련된 디자인과 실용적인 폴딩 기능이 돋보이는 제품"
  },
  "strengths": [
    {
      "title": "뛰어난 휴대성",
      "description": "접었을 때 어깨끈으로 메고 다닐 수 있어 계단이나 에스컬레이터 이용 시 매우 편리합니다. 기내반입 가능한 컴팩트한 사이즈로 여행 시 필수품입니다.",
      "category": "function",
      "importance": "high"
    },
    {
      "title": "세련된 디자인",
      "description": "베이지, 로즈핑크, 카키, 그린 등 다양한 트렌디 컬러를 제공합니다. 알루미늄 프레임과 가죽 손잡이로 프리미엄 감성을 살렸습니다.",
      "category": "design",
      "importance": "high"
    },
    {
      "title": "넉넉한 좌석 공간",
      "description": "휴대용 유모차임에도 아이가 편안하게 앉을 수 있는 충분한 좌석 공간을 제공합니다. 등받이 각도 조절도 가능해 보입니다.",
      "category": "function",
      "importance": "medium"
    },
    {
      "title": "실용적인 사은품 구성",
      "description": "방풍커버와 스낵트레이가 기본 사은품으로 제공되어 별도 구매 비용을 절약할 수 있습니다.",
      "category": "price",
      "importance": "medium"
    },
    {
      "title": "안전한 5점식 벨트",
      "description": "어깨, 허리, 가랑이를 감싸는 5점식 안전벨트로 아이의 안전을 확보합니다. 벨트 조절도 간편해 보입니다.",
      "category": "function",
      "importance": "high"
    },
    {
      "title": "도심형 휠 설계",
      "description": "4륜 구동 방식으로 도심 보도블럭이나 매장 내에서도 부드러운 주행이 가능합니다.",
      "category": "function",
      "importance": "medium"
    }
  ],
  "weaknesses": [
    {
      "title": "정확한 무게 정보 미표기",
      "description": "상세페이지에서 유모차의 정확한 무게가 확인되지 않습니다. 휴대용 유모차에서 무게는 중요한 구매 결정 요소입니다.",
      "category": "info",
      "severity": "high"
    },
    {
      "title": "접힌 사이즈 미표기",
      "description": "기내반입 가능하다고 하지만 접었을 때의 정확한 사이즈(가로x세로x높이)가 명시되어 있지 않습니다.",
      "category": "info",
      "severity": "high"
    },
    {
      "title": "프리미엄 가격대",
      "description": "498,000원은 휴대용 유모차 중에서 상위 가격대입니다. 동급 기능의 경쟁 제품 대비 가격 경쟁력 검토가 필요합니다.",
      "category": "concern",
      "severity": "medium"
    },
    {
      "title": "하부 수납 공간 제한",
      "description": "이미지상 하부 수납바구니가 있지만 크기가 제한적으로 보입니다. 외출 시 짐이 많은 경우 수납 공간이 부족할 수 있습니다.",
      "category": "function",
      "severity": "low"
    },
    {
      "title": "신생아 사용 가능 여부 불명확",
      "description": "몇 개월부터 사용 가능한지, 신생아용 인서트가 별도로 필요한지에 대한 정보가 부족합니다.",
      "category": "info",
      "severity": "medium"
    }
  ],
  "featureAnalysis": [
    {
      "feature": "휴대성",
      "score": 5,
      "evidence": "어깨끈으로 메고 다닐 수 있는 폴딩 구조, 기내반입 가능 사이즈",
      "pros": [
        "원터치 폴딩 추정",
        "어깨끈 휴대 가능",
        "기내반입 가능"
      ],
      "cons": [
        "정확한 무게 미공개"
      ]
    },
    {
      "feature": "디자인",
      "score": 5,
      "evidence": "알루미늄 프레임, 가죽 손잡이, 다양한 트렌디 컬러",
      "pros": [
        "프리미엄 소재 사용",
        "컬러 옵션 다양",
        "모던한 실루엣"
      ],
      "cons": []
    },
    {
      "feature": "안전성",
      "score": 4,
      "evidence": "5점식 안전벨트, 안정적인 4륜 구조",
      "pros": [
        "5점식 벨트",
        "안정적인 프레임"
      ],
      "cons": [
        "안전 인증 정보 미확인"
      ]
    },
    {
      "feature": "편의성",
      "score": 4,
      "evidence": "사은품 방풍커버/스낵트레이, 등받이 조절",
      "pros": [
        "실용적 사은품",
        "등받이 각도 조절"
      ],
      "cons": [
        "수납 공간 제한적"
      ]
    },
    {
      "feature": "가성비",
      "score": 3,
      "evidence": "498,000원 가격대, 사은품 포함",
      "pros": [
        "사은품 구성 우수"
      ],
      "cons": [
        "프리미엄 가격대",
        "경쟁사 대비 가격 비교 필요"
      ]
    }
  ],
  "competitorComparison": [
    {
      "aspect": "휴대성",
      "thisProduct": "어깨끈 휴대 가능, 기내반입 사이즈",
      "competitors": "요요/버기: 유사 수준, 지비: 조금 더 컴팩트",
      "verdict": "similar"
    },
    {
      "aspect": "디자인",
      "thisProduct": "알루미늄 프레임, 가죽 손잡이, 다양한 컬러",
      "competitors": "해외 브랜드: 심플한 디자인, 국내 브랜드: 유사 수준",
      "verdict": "advantage"
    },
    {
      "aspect": "가격",
      "thisProduct": "498,000원 (사은품 포함)",
      "competitors": "버기비+: 60만원대, 요요2: 70만원대, 중저가: 20-30만원대",
      "verdict": "similar"
    },
    {
      "aspect": "브랜드 인지도",
      "thisProduct": "리안베이비 - 국내 유모차 전문 브랜드",
      "competitors": "베이비젠, 지비 등 글로벌 브랜드",
      "verdict": "disadvantage"
    }
  ],
  "recommendation": {
    "score": 7,
    "summary": "세련된 디자인과 뛰어난 휴대성을 갖춘 프리미엄 휴대용 유모차입니다. 여행이나 도심 외출이 잦은 가정에 적합하며, 사은품 구성도 실용적입니다. 다만 정확한 스펙 정보가 부족하여 구매 전 문의가 필요합니다.",
    "bestFor": [
      "해외여행/국내여행을 자주 다니는 가족",
      "대중교통 이용이 많은 도심 거주자",
      "세컨드 유모차를 찾는 가정",
      "디자인을 중시하는 부모"
    ],
    "notFor": [
      "신생아부터 사용하려는 가정 (사용 가능 월령 확인 필요)",
      "가성비를 최우선으로 생각하는 분",
      "수납 공간이 많이 필요한 분",
      "정확한 스펙 정보 없이는 구매 결정이 어려운 분"
    ]
  },
  "images": {
    "thumbnail": "https://ryanbaby.co.kr/web/product/big/202601/2c14407289ba79a7f8ca15c796dbf2ac.jpg",
    "detailImages": [
      "https://ryanbaby.co.kr/web/product/extra/small/202601/06646592b8301c910db5f6a326cd7e15.jpg",
      "https://ryanbaby.co.kr/web/product/extra/small/202601/ba3fd8f330d5ea68b5ab01533b4b5af4.jpg",
      "https://ryanbaby.co.kr/web/product/extra/small/202601/3e18db35a0a9e9f02cd82d4decce1349.jpg",
      "https://ryanbaby.co.kr/web/product/extra/small/202601/e138c8f77004b2fe7f020d27597823aa.jpg"
    ]
  }
};
