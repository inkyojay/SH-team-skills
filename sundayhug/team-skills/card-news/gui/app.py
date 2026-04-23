"""
Card News Creator - Streamlit GUI

실행 방법:
    streamlit run app.py

내부 공유 방법:
    streamlit run app.py --server.address 0.0.0.0
    → 같은 네트워크에서 http://YOUR_IP:8501 로 접속
"""

import streamlit as st
import sys
import json
import tempfile
import zipfile
import io
from pathlib import Path

# 스크립트 경로 추가
SCRIPT_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from fetch_content import fetch_content
from gemini_image_api import generate_image, load_api_key, save_api_key

# 페이지 설정
st.set_page_config(
    page_title="Card News Creator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 스타일
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .card-preview {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 10px;
        margin: 10px 0;
    }
    .stButton > button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


def init_session_state():
    """세션 상태 초기화"""
    if 'cards' not in st.session_state:
        st.session_state.cards = []
    if 'generated_images' not in st.session_state:
        st.session_state.generated_images = {}
    if 'content' not in st.session_state:
        st.session_state.content = None
    if 'api_key_set' not in st.session_state:
        st.session_state.api_key_set = bool(load_api_key())


def sidebar_settings():
    """사이드바 설정"""
    with st.sidebar:
        st.markdown("## ⚙️ 설정")

        # API 키 설정
        st.markdown("### 🔑 Gemini API 키")
        api_key = load_api_key()

        if api_key:
            st.success("API 키 설정됨 ✓")
            if st.button("API 키 변경"):
                st.session_state.show_api_input = True
        else:
            st.warning("API 키를 설정하세요")
            st.session_state.show_api_input = True

        if st.session_state.get('show_api_input', not api_key):
            new_key = st.text_input("API 키 입력", type="password")
            if st.button("저장"):
                if new_key:
                    save_api_key(new_key)
                    st.session_state.api_key_set = True
                    st.session_state.show_api_input = False
                    st.rerun()

        st.markdown("---")

        # 브랜드 설정
        st.markdown("### 🏷️ 브랜드 설정")
        brand_name = st.text_input("브랜드명", value="BRAND NAME")

        # 색상 테마
        color_theme = st.selectbox(
            "색상 테마",
            ["warm", "cool", "dark", "minimal", "vibrant"],
            index=0
        )

        # 카드 설정
        st.markdown("### 📝 카드 설정")
        card_count = st.slider("카드 수", 5, 12, 8)
        text_length = st.selectbox(
            "텍스트 분량",
            ["short (1-2문장)", "medium (3-4문장)", "long (5+문장)"],
            index=1
        )

        # 이미지 스타일
        st.markdown("### 🎨 이미지 스타일")
        style_prefix = st.text_area(
            "스타일 프롬프트",
            value="soft watercolor illustration style, warm pastel colors, Korean aesthetic, minimal background",
            height=100
        )

        return {
            'brand_name': brand_name,
            'color_theme': color_theme,
            'card_count': card_count,
            'text_length': text_length.split()[0],
            'style_prefix': style_prefix
        }


def extract_content_tab():
    """콘텐츠 추출 탭"""
    st.markdown("### 1️⃣ 콘텐츠 소스 입력")

    source_type = st.radio(
        "소스 유형",
        ["YouTube URL", "웹페이지 URL", "직접 입력"],
        horizontal=True
    )

    if source_type == "YouTube URL":
        url = st.text_input("YouTube URL", placeholder="https://youtube.com/watch?v=...")
        if st.button("콘텐츠 추출", type="primary"):
            if url:
                with st.spinner("콘텐츠 추출 중..."):
                    result = fetch_content(url)
                    if result.get('success'):
                        st.session_state.content = result
                        st.success(f"추출 완료! 제목: {result.get('title', 'N/A')}")
                    else:
                        st.error(f"추출 실패: {result.get('error', '알 수 없는 오류')}")
            else:
                st.warning("URL을 입력하세요")

    elif source_type == "웹페이지 URL":
        url = st.text_input("웹페이지 URL", placeholder="https://example.com/article")
        if st.button("콘텐츠 추출", type="primary"):
            if url:
                with st.spinner("콘텐츠 추출 중..."):
                    result = fetch_content(url)
                    if result.get('success'):
                        st.session_state.content = result
                        st.success(f"추출 완료!")
                    else:
                        st.error(f"추출 실패: {result.get('error', '알 수 없는 오류')}")

    else:
        title = st.text_input("제목")
        content = st.text_area("내용", height=300, placeholder="카드뉴스로 만들 내용을 입력하세요...")
        if st.button("저장", type="primary"):
            if content:
                st.session_state.content = {
                    'success': True,
                    'source_type': 'text',
                    'title': title,
                    'content': content
                }
                st.success("저장 완료!")

    # 추출된 콘텐츠 표시
    if st.session_state.content:
        with st.expander("📄 추출된 콘텐츠 보기", expanded=False):
            st.markdown(f"**제목:** {st.session_state.content.get('title', 'N/A')}")
            st.markdown(f"**소스 유형:** {st.session_state.content.get('source_type', 'N/A')}")
            content_text = st.session_state.content.get('content', '')
            st.text_area("내용", value=content_text[:3000] + "..." if len(content_text) > 3000 else content_text, height=200, disabled=True)


def edit_cards_tab(settings):
    """카드 편집 탭"""
    st.markdown("### 2️⃣ 카드 구조 편집")

    if not st.session_state.content:
        st.info("먼저 '콘텐츠 추출' 탭에서 소스를 입력하세요.")
        return

    # 자동 생성 버튼
    if st.button("🪄 카드 구조 자동 생성", type="primary"):
        st.info("Claude Code에서 이 기능을 사용하세요. 콘텐츠를 분석하여 카드 구조를 생성해드립니다.")
        # 기본 템플릿 제공
        st.session_state.cards = generate_default_cards(st.session_state.content, settings)
        st.rerun()

    st.markdown("---")

    # 카드 편집 UI
    if st.session_state.cards:
        for i, card in enumerate(st.session_state.cards):
            with st.expander(f"카드 {i+1}: {card.get('type', 'content')} - {card.get('content', {}).get('heading', card.get('content', {}).get('title', ''))[:30]}", expanded=i==0):
                col1, col2 = st.columns([1, 1])

                with col1:
                    card_type = st.selectbox(
                        "카드 유형",
                        ["cover", "content", "info", "summary"],
                        index=["cover", "content", "info", "summary"].index(card.get('type', 'content')),
                        key=f"type_{i}"
                    )
                    st.session_state.cards[i]['type'] = card_type

                    if card_type == "cover":
                        episode = st.text_input("에피소드", value=card.get('content', {}).get('episode', ''), key=f"episode_{i}")
                        title = st.text_area("타이틀", value=card.get('content', {}).get('title', ''), key=f"title_{i}", height=100)
                        subtitle = st.text_input("부제목", value=card.get('content', {}).get('subtitle', ''), key=f"subtitle_{i}")
                        st.session_state.cards[i]['content'] = {'episode': episode, 'title': title, 'subtitle': subtitle}

                    elif card_type == "content":
                        heading = st.text_input("소제목", value=card.get('content', {}).get('heading', ''), key=f"heading_{i}")
                        body = st.text_area("본문", value=card.get('content', {}).get('body', ''), key=f"body_{i}", height=150)
                        st.session_state.cards[i]['content'] = {'heading': heading, 'body': body}

                    elif card_type == "info":
                        title = st.text_input("제목", value=card.get('content', {}).get('title', ''), key=f"info_title_{i}")
                        items = card.get('content', {}).get('items', [{'icon': '💡', 'text': ''}, {'icon': '📌', 'text': ''}, {'icon': '✨', 'text': ''}])
                        new_items = []
                        for j, item in enumerate(items[:3]):
                            col_icon, col_text = st.columns([1, 4])
                            with col_icon:
                                icon = st.text_input(f"아이콘", value=item.get('icon', '💡'), key=f"icon_{i}_{j}")
                            with col_text:
                                text = st.text_input(f"내용", value=item.get('text', ''), key=f"item_text_{i}_{j}")
                            new_items.append({'icon': icon, 'text': text})
                        st.session_state.cards[i]['content'] = {'title': title, 'items': new_items}

                    elif card_type == "summary":
                        title = st.text_input("제목", value=card.get('content', {}).get('title', '오늘의 핵심 정리'), key=f"sum_title_{i}")
                        points = card.get('content', {}).get('points', ['', '', '', ''])
                        new_points = []
                        for j, point in enumerate(points[:4]):
                            p = st.text_input(f"포인트 {j+1}", value=point, key=f"point_{i}_{j}")
                            if p:
                                new_points.append(p)
                        st.session_state.cards[i]['content'] = {'title': title, 'points': new_points}

                with col2:
                    st.markdown("**이미지 프롬프트**")
                    prompt = st.text_area(
                        "프롬프트",
                        value=card.get('image_prompt', ''),
                        key=f"prompt_{i}",
                        height=100,
                        label_visibility="collapsed"
                    )
                    st.session_state.cards[i]['image_prompt'] = prompt

                    # 이미지 미리보기
                    if i in st.session_state.generated_images:
                        st.image(st.session_state.generated_images[i], caption="생성된 이미지")

                    if st.button("🖼️ 이미지 생성", key=f"gen_img_{i}"):
                        if prompt and st.session_state.api_key_set:
                            with st.spinner("이미지 생성 중..."):
                                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                                    result = generate_image(
                                        prompt=prompt,
                                        output_path=f.name,
                                        style_prefix=settings['style_prefix']
                                    )
                                    if result.get('success'):
                                        st.session_state.generated_images[i] = f.name
                                        st.rerun()
                                    else:
                                        st.error(f"생성 실패: {result.get('error')}")
                        else:
                            st.warning("API 키를 설정하고 프롬프트를 입력하세요")

        # 카드 추가/삭제
        col1, col2 = st.columns(2)
        with col1:
            if st.button("➕ 카드 추가"):
                st.session_state.cards.append({
                    'type': 'content',
                    'content': {'heading': '', 'body': ''},
                    'image_prompt': ''
                })
                st.rerun()
        with col2:
            if len(st.session_state.cards) > 1:
                if st.button("➖ 마지막 카드 삭제"):
                    st.session_state.cards.pop()
                    st.rerun()


def generate_default_cards(content, settings):
    """기본 카드 구조 생성"""
    title = content.get('title', '제목 없음')
    card_count = settings['card_count']

    cards = [
        {
            'type': 'cover',
            'content': {
                'episode': '',
                'title': title[:50] if len(title) > 50 else title,
                'subtitle': '핵심 내용을 알려드립니다'
            },
            'image_prompt': 'friendly illustration related to the topic, soft watercolor style'
        }
    ]

    # 중간 콘텐츠 카드들 생성
    content_count = card_count - 3  # cover, info, summary 제외
    for i in range(content_count):
        if i == content_count // 2:  # 중간에 info 카드 삽입
            cards.append({
                'type': 'info',
                'content': {
                    'title': '알아두면 좋은 포인트',
                    'items': [
                        {'icon': '💡', 'text': '첫 번째 포인트'},
                        {'icon': '📌', 'text': '두 번째 포인트'},
                        {'icon': '✨', 'text': '세 번째 포인트'}
                    ]
                },
                'image_prompt': ''
            })
        else:
            cards.append({
                'type': 'content',
                'content': {
                    'heading': f'핵심 개념 {i + 1}',
                    'body': f'여기에 {i + 1}번째 핵심 내용을 입력하세요.'
                },
                'image_prompt': 'concept illustration, soft watercolor style'
            })

    # 마지막 summary 카드
    cards.append({
        'type': 'summary',
        'content': {
            'title': '오늘의 핵심 정리',
            'points': [
                '핵심 포인트 1',
                '핵심 포인트 2',
                '핵심 포인트 3',
                '핵심 포인트 4'
            ]
        },
        'image_prompt': 'soft gradient warm colors, abstract peaceful background'
    })

    return cards[:card_count]


def preview_tab(settings):
    """미리보기 탭"""
    st.markdown("### 3️⃣ 미리보기 및 내보내기")

    if not st.session_state.cards:
        st.info("먼저 '카드 편집' 탭에서 카드를 생성하세요.")
        return

    # 미리보기
    cols = st.columns(3)
    for i, card in enumerate(st.session_state.cards):
        with cols[i % 3]:
            st.markdown(f"**카드 {i+1}: {card.get('type')}**")

            # 카드 내용 미리보기
            content = card.get('content', {})
            if card['type'] == 'cover':
                st.markdown(f"_{content.get('episode', '')}_")
                st.markdown(f"**{content.get('title', '')}**")
                st.markdown(content.get('subtitle', ''))
            elif card['type'] == 'content':
                st.markdown(f"**{content.get('heading', '')}**")
                st.markdown(content.get('body', ''))
            elif card['type'] == 'info':
                st.markdown(f"**{content.get('title', '')}**")
                for item in content.get('items', []):
                    st.markdown(f"{item.get('icon', '')} {item.get('text', '')}")
            elif card['type'] == 'summary':
                st.markdown(f"**{content.get('title', '')}**")
                for point in content.get('points', []):
                    st.markdown(f"✓ {point}")

            # 이미지 미리보기
            if i in st.session_state.generated_images:
                st.image(st.session_state.generated_images[i], use_container_width=True)

            st.markdown("---")

    # 내보내기
    st.markdown("### 📥 내보내기")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("🖼️ 모든 이미지 생성", type="primary"):
            if not st.session_state.api_key_set:
                st.error("API 키를 먼저 설정하세요")
                return

            progress = st.progress(0)
            for i, card in enumerate(st.session_state.cards):
                if card.get('image_prompt') and i not in st.session_state.generated_images:
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
                        result = generate_image(
                            prompt=card['image_prompt'],
                            output_path=f.name,
                            style_prefix=settings['style_prefix']
                        )
                        if result.get('success'):
                            st.session_state.generated_images[i] = f.name
                progress.progress((i + 1) / len(st.session_state.cards))
            st.success("모든 이미지 생성 완료!")
            st.rerun()

    with col2:
        if st.button("📦 JSON으로 내보내기"):
            export_data = {
                'brand': {'name': settings['brand_name'], 'theme': settings['color_theme']},
                'cards': st.session_state.cards,
                'settings': settings
            }
            json_str = json.dumps(export_data, ensure_ascii=False, indent=2)
            st.download_button(
                label="💾 JSON 다운로드",
                data=json_str,
                file_name="card_news_structure.json",
                mime="application/json"
            )

    # 생성된 이미지 다운로드
    if st.session_state.generated_images:
        st.markdown("### 🖼️ 생성된 이미지")

        # ZIP으로 묶어서 다운로드
        if st.button("📦 모든 이미지 ZIP 다운로드"):
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:
                for i, img_path in st.session_state.generated_images.items():
                    card_type = st.session_state.cards[i].get('type', 'card')
                    zf.write(img_path, f"{i+1:02d}_{card_type}.png")

            st.download_button(
                label="💾 ZIP 다운로드",
                data=zip_buffer.getvalue(),
                file_name="card_news_images.zip",
                mime="application/zip"
            )


def main():
    """메인 함수"""
    init_session_state()

    # 헤더
    st.markdown('<p class="main-header">🎨 Card News Creator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">URL 입력 → AI 이미지 생성 → 카드뉴스 완성</p>', unsafe_allow_html=True)

    # 사이드바 설정
    settings = sidebar_settings()

    # 탭
    tab1, tab2, tab3 = st.tabs(["📥 콘텐츠 추출", "✏️ 카드 편집", "👁️ 미리보기"])

    with tab1:
        extract_content_tab()

    with tab2:
        edit_cards_tab(settings)

    with tab3:
        preview_tab(settings)


if __name__ == "__main__":
    main()
