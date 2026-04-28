"""31 섹션 카탈로그.

각 섹션 HTML 헤더 코멘트(SECTION/ORDER/REQUIRED/BACKGROUND/PURPOSE/DATA REQUIRED)
를 자동 파싱해서 SectionMeta 객체로 만든다.

수동 큐레이션 영역:
  - SECTION_DEFAULTS: 브랜드 표준 default 슬롯 값 (trust_1_main 등)
  - PREMIUM_PRESET:   프리미엄 라이브 기본 13개 섹션 추천 조합
  - PALETTE_LIST:     12개 캠페인 팔레트
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


# 템플릿 위치
TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
SECTIONS_DIR = TEMPLATES_DIR / "sections"


# ── 12 팔레트 (스마트스토어와 동일) ──────────────────────────────────────────
PALETTE_LIST = [
    "warm-spring", "cool-summer", "cozy-autumn", "gentle-winter",
    "rose-dawn", "fresh-garden", "moonlit-calm", "blush-touch",
    "slate-mood", "golden-hour", "coral-sunset", "midnight-luxe",
]

# 시즌 키워드 → 팔레트 자동 매핑 (인터뷰 폴백)
MONTH_TO_PALETTE = {
    1: "gentle-winter", 2: "gentle-winter", 3: "warm-spring",
    4: "warm-spring", 5: "warm-spring", 6: "fresh-garden",
    7: "cool-summer", 8: "cool-summer", 9: "cozy-autumn",
    10: "cozy-autumn", 11: "coral-sunset", 12: "midnight-luxe",
}


# ── 프리미엄 프리셋 (기본 추천 13개) ────────────────────────────────────────
PREMIUM_PRESET = [
    "01-live-hero",
    "02-trust-bar",
    "03-schedule",
    "04-countdown",
    "05-live-benefits",
    "06-coupon",
    "10-mid-cta",
    "11-host-recommendation",
    "12-quick-showcase",
    "13-lifestyle",
    "15-review",
    "19-faq",
    "25-final-cta",
    "27-footer",
]


# ── 브랜드 표준 default 슬롯 값 ───────────────────────────────────────────────
# 사용자가 인터뷰에서 안 채운 슬롯 중 거의 항상 같은 값을 갖는 것들.
SECTION_DEFAULTS: dict[str, dict] = {
    "02-trust-bar": {
        "trust_1_main": "오늘 발송",
        "trust_1_sub": "평일 14시 이전",
        "trust_2_main": "100일 환불",
        "trust_2_sub": "조건 없이",
        "trust_3_main": "무료 배송",
        "trust_3_sub": "5만원 이상",
    },
    "20-shipping": {
        "ship_title_1": "배송",
        "ship_desc_1": "평일 14시 이전 주문 시 당일 발송",
        "ship_title_2": "교환",
        "ship_desc_2": "수령 후 7일 이내",
        "ship_title_3": "환불",
        "ship_desc_3": "수령 후 100일 이내, 조건 없이",
        "ship_title_4": "고객센터",
        "ship_desc_4": "카카오톡 @sundayhug",
    },
    "21-guarantee": {
        "guarantee_1_title": "100일 환불 보장",
        "guarantee_1_desc": "사용 후에도 마음에 들지 않으면 조건 없이 환불",
        "guarantee_2_title": "유해물질 ZERO",
        "guarantee_2_desc": "OEKO-TEX 인증 원단만 사용",
    },
    "27-footer": {
        "channel_name": "Sunday Hug",
        "channel_url": "https://sundayhug.kr",
    },
}


# ── 섹션 메타데이터 ───────────────────────────────────────────────────────────
@dataclass
class SectionMeta:
    """단일 섹션의 메타데이터."""
    id: str                                 # "01-live-hero"
    order: int                              # 1
    name: str                               # "Live Hero (라이브 히어로)"
    required: bool                          # ✅ 필수 / 🔶 선택
    background: str = ""                    # "palette gradient" / "white"
    purpose: str = ""
    slot_vars: list[str] = field(default_factory=list)        # ["host_image", "live_title_html", ...]
    array_slots: list[str] = field(default_factory=list)      # ["live_benefits", "faqs", ...]
    conditional_slots: list[str] = field(default_factory=list)  # ["featured", "warm", "rev"]

    @property
    def template_path(self) -> Path:
        return SECTIONS_DIR / f"{self.id}.html"

    @property
    def has_array_slot(self) -> bool:
        return bool(self.array_slots)


# ── 헤더 코멘트 파서 ──────────────────────────────────────────────────────────
_HEADER_RE = re.compile(r"<!--=+\n(.*?)\n=+-->", re.DOTALL)
_FIELD_RE = re.compile(r"^\s*([A-Z][A-Z ]+):\s*(.+?)\s*$")
_VAR_RE = re.compile(r"\{\{([^}#/?]+?)\}\}")           # plain {{var}}
_ARRAY_RE = re.compile(r"\{\{#([a-zA-Z_][a-zA-Z0-9_]*)\}\}")   # {{#array}}
_COND_RE = re.compile(r"\{\{\?([a-zA-Z_][a-zA-Z0-9_]*)\}\}")    # {{?cond}}


def _parse_section(path: Path) -> SectionMeta:
    """섹션 HTML에서 메타데이터 + 슬롯 추출."""
    text = path.read_text(encoding="utf-8")
    sec_id = path.stem  # "01-live-hero"

    # 헤더 필드 파싱
    header_match = _HEADER_RE.search(text)
    fields: dict[str, str] = {}
    if header_match:
        for line in header_match.group(1).splitlines():
            m = _FIELD_RE.match(line)
            if m:
                fields[m.group(1).strip()] = m.group(2).strip()

    name = fields.get("SECTION", sec_id)
    order_str = fields.get("ORDER", sec_id.split("-")[0])
    try:
        order = int(order_str)
    except ValueError:
        order = 99
    required = "필수" in fields.get("REQUIRED", "") or "✅" in fields.get("REQUIRED", "")
    background = fields.get("BACKGROUND", "")
    purpose = fields.get("PURPOSE", "")

    # 슬롯 추출 (헤더 제외 본문에서)
    body = text[header_match.end():] if header_match else text
    plain_vars = sorted(set(v.strip() for v in _VAR_RE.findall(body)
                            if v.strip() and v.strip() != "."))
    array_slots = sorted(set(_ARRAY_RE.findall(body)))
    conditional_slots = sorted(set(_COND_RE.findall(body)))

    # 배열 안의 변수는 plain_vars에 같이 들어옴 (chevron이 컨텍스트 자동 처리)
    return SectionMeta(
        id=sec_id,
        order=order,
        name=name,
        required=required,
        background=background,
        purpose=purpose,
        slot_vars=plain_vars,
        array_slots=array_slots,
        conditional_slots=conditional_slots,
    )


# ── 카탈로그 빌더 ─────────────────────────────────────────────────────────────
def load_catalog() -> dict[str, SectionMeta]:
    """모든 31 섹션을 파싱해서 {id: SectionMeta} 반환."""
    if not SECTIONS_DIR.exists():
        raise FileNotFoundError(f"sections folder missing: {SECTIONS_DIR}")
    catalog: dict[str, SectionMeta] = {}
    for path in sorted(SECTIONS_DIR.glob("*.html")):
        meta = _parse_section(path)
        catalog[meta.id] = meta
    return catalog


def get_preset(name: str = "premium") -> list[str]:
    """프리셋 이름으로 추천 섹션 ID 리스트 반환."""
    presets = {"premium": PREMIUM_PRESET}
    if name not in presets:
        raise ValueError(f"Unknown preset '{name}'. Valid: {list(presets)}")
    return list(presets[name])


def get_defaults(section_id: str) -> dict:
    """섹션 ID의 브랜드 표준 default 슬롯 dict 반환 (없으면 빈 dict)."""
    return dict(SECTION_DEFAULTS.get(section_id, {}))


# ── CLI: 카탈로그 요약 ──────────────────────────────────────────────────────
if __name__ == "__main__":
    catalog = load_catalog()
    print(f"Total sections: {len(catalog)}")
    print(f"Required (필수): {sum(1 for s in catalog.values() if s.required)}")
    print(f"Premium preset: {len(PREMIUM_PRESET)} sections\n")

    for sec_id, meta in catalog.items():
        flag = "✅" if meta.required else "🔶"
        in_preset = "★" if sec_id in PREMIUM_PRESET else " "
        slots_summary = f"{len(meta.slot_vars)} vars"
        if meta.array_slots:
            slots_summary += f" + {len(meta.array_slots)} arrays"
        if meta.conditional_slots:
            slots_summary += f" + {len(meta.conditional_slots)} cond"
        print(f"  {in_preset} {flag} {sec_id:<32} {meta.name:<35} {slots_summary}")
