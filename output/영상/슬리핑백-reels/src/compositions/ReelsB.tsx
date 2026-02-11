import React from "react";
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";

import { VideoClip } from "../components/VideoClip";
import { ImageSlide } from "../components/ImageSlide";
import { Caption } from "../components/Caption";
import { ReviewCard } from "../components/ReviewCard";
import { ColorSwatches } from "../components/ColorSwatches";
import { CtaEndCard } from "../components/CtaEndCard";
import { VIDEOS, PHOTOS } from "../media-map";

/**
 * 릴스 B - UGC 리뷰 컴필레이션형 (25초)
 *
 * 구조: 숫자 임팩트 → UGC 1 → UGC 2 → UGC 3 → UGC 4+5(빠른컷) → 컬러 쇼케이스 → CTA
 * 페이스: 빠름 (비트 편집), 각 클립마다 리뷰 카드 오버레이
 */

const FPS = 30;
const TRANSITION_FRAMES = 6; // 빠른 트랜지션

export const ReelsB: React.FC = () => {
  const { fps } = useVideoConfig();
  const t = (seconds: number) => Math.round(seconds * fps);

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <TransitionSeries>
        {/* ─── 장면 1: HOOK (0-3초) - 227 숫자 임팩트 ─── */}
        <TransitionSeries.Sequence durationInFrames={t(3.2)}>
          <AbsoluteFill>
            {/* 배경: 사진 콜라주 블러 */}
            <ImageSlide src={PHOTOS.jieunwoo} zoomDirection="out">
              <div
                style={{
                  position: "absolute",
                  top: 0,
                  left: 0,
                  right: 0,
                  bottom: 0,
                  backdropFilter: "blur(12px)",
                  background: "rgba(0,0,0,0.4)",
                }}
              />
            </ImageSlide>

            {/* 카운트업 숫자 */}
            <Sequence from={3} layout="none">
              <CountUpHook fps={fps} />
            </Sequence>
          </AbsoluteFill>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* ─── 장면 2: UGC 1 - @im_yoohyun (3-7초) ─── */}
        <TransitionSeries.Sequence durationInFrames={t(4.2)}>
          <VideoClip src={VIDEOS.yoohyun} startFrom={2}>
            <Sequence from={8} layout="none">
              <ReviewCard
                text="첫째 때 써보고 둘째도 재구매했어요"
                direction="left"
              />
            </Sequence>
          </VideoClip>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={slide({ direction: "from-right" })}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* ─── 장면 3: UGC 2 - @mming_kkong__ (7-11초) ─── */}
        <TransitionSeries.Sequence durationInFrames={t(4.2)}>
          <VideoClip src={VIDEOS.mmingkkong} startFrom={5}>
            <Sequence from={8} layout="none">
              <ReviewCard
                text="밤새 안 깨고 7시간 꿀잠 잤어요!"
                direction="right"
              />
            </Sequence>
          </VideoClip>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={slide({ direction: "from-left" })}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* ─── 장면 4: UGC 3 - @ol_chaea (11-15초) ─── */}
        <TransitionSeries.Sequence durationInFrames={t(4.2)}>
          <VideoClip src={VIDEOS.olchaea} startFrom={8}>
            <Sequence from={8} layout="none">
              <ReviewCard
                text="실키 밤부 촉감이 진짜 장난 아니에요"
                direction="center"
              />
            </Sequence>
          </VideoClip>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* ─── 장면 5: UGC 4+5 빠른 컷 (15-19초) ─── */}
        <TransitionSeries.Sequence durationInFrames={t(4.2)}>
          <AbsoluteFill>
            {/* 클립 4: @_iamgamza (2초) */}
            <Sequence from={0} durationInFrames={t(2)} premountFor={fps}>
              <VideoClip src={VIDEOS.iamgamza} startFrom={20}>
                <Sequence from={3} layout="none">
                  <Caption line1='★★★★★ "이불 전쟁 끝!"' size="medium" />
                </Sequence>
              </VideoClip>
            </Sequence>

            {/* 클립 5: @violet_yoon (2초) */}
            <Sequence from={t(2)} durationInFrames={t(2.2)} premountFor={fps}>
              <VideoClip src={VIDEOS.violetyoon} startFrom={15}>
                <Sequence from={3} layout="none">
                  <Caption line1='★★★★★ "사계절 내내 써요"' size="medium" />
                </Sequence>
              </VideoClip>
            </Sequence>
          </AbsoluteFill>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* ─── 장면 6: 컬러 쇼케이스 (19-22초) ─── */}
        <TransitionSeries.Sequence durationInFrames={t(3)}>
          <AbsoluteFill style={{ backgroundColor: "#FFF8F0" }}>
            <ColorSwatches highlightIndex={5} showLabels />
            <Sequence from={5} layout="none">
              <div
                style={{
                  position: "absolute",
                  bottom: 400,
                  left: 60,
                  right: 120,
                  textAlign: "center",
                }}
              >
                <p
                  style={{
                    fontSize: 40,
                    fontWeight: 800,
                    color: "#3E2723",
                    fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
                    margin: 0,
                  }}
                >
                  블룸 라벤더
                </p>
                <p
                  style={{
                    fontSize: 34,
                    fontWeight: 600,
                    color: "#B39DDB",
                    fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
                    margin: "4px 0 0",
                  }}
                >
                  나만 알고 싶었는데 인기 폭발 💜
                </p>
              </div>
            </Sequence>
          </AbsoluteFill>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* ─── 장면 7: CTA (22-25초) ─── */}
        <TransitionSeries.Sequence durationInFrames={t(3.2)}>
          <ImageSlide src={PHOTOS.mmingkkongPhoto} zoomDirection="in">
            <Sequence from={3} layout="none">
              <CtaEndCard
                brandName="SUNDAY HUG"
                brandColor="#5a7d65"
                line1="'이걸 왜 이제야 샀지'"
                line2="후회되실 거예요 👆"
              />
            </Sequence>
          </ImageSlide>
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};

/**
 * 숫자 카운트업 훅 컴포넌트 (0 → 227)
 */
const CountUpHook: React.FC<{ fps: number }> = ({ fps }) => {
  const frame = useCurrentFrame();

  // 1.5초(45프레임)에 걸쳐 0→227
  const countDuration = Math.round(1.5 * fps);
  const count = Math.min(
    227,
    Math.round((frame / countDuration) * 227),
  );

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 60,
        right: 120,
        bottom: 0,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <span
        style={{
          fontSize: 120,
          fontWeight: 900,
          color: "#fff",
          fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
          textShadow: "0 4px 20px rgba(0,0,0,0.8)",
        }}
      >
        {count}
      </span>
      <span
        style={{
          fontSize: 44,
          fontWeight: 700,
          color: "#fff",
          fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
          textShadow: "0 2px 12px rgba(0,0,0,0.7)",
          marginTop: 8,
        }}
      >
        명의 엄마가
      </span>
      <span
        style={{
          fontSize: 48,
          fontWeight: 800,
          color: "#FFD700",
          fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
          textShadow: "0 2px 12px rgba(0,0,0,0.7)",
          marginTop: 4,
        }}
      >
        별점 4.9를 준 슬리핑백 ⭐
      </span>
    </div>
  );
};

