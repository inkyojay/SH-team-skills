import React from "react";
import { AbsoluteFill, Sequence, useVideoConfig } from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";
import { slide } from "@remotion/transitions/slide";

import { VideoClip } from "../components/VideoClip";
import { ImageSlide } from "../components/ImageSlide";
import { Caption } from "../components/Caption";
import { BrandLogo } from "../components/BrandLogo";
import { RatingBadge } from "../components/RatingBadge";
import { FeatureText } from "../components/FeatureText";
import { ColorSwatches } from "../components/ColorSwatches";
import { CtaEndCard } from "../components/CtaEndCard";
import { VIDEOS, PHOTOS } from "../media-map";

/**
 * 릴스 A - Problem-Solution형 (30초)
 *
 * 구조: 훅(공감) → 문제 → 솔루션 → 데모(3기능) → 결과 → 리뷰+컬러 → CTA
 * 톤 전환: 블루(문제) → 웜(해결)
 */

const FPS = 30;
const TRANSITION_FRAMES = 8;

// 씬 길이 (트랜지션 오버랩 보정 포함 = 총 ~30초)
const SCENE_DURATIONS = {
  hook: 3.3, // 0-3초
  problem: 3.3, // 3-6초
  solution: 4.2, // 6-10초
  demo: 6.4, // 10-16초 (3 features)
  result: 6.2, // 16-22초
  socialProof: 4.2, // 22-26초
  cta: 4.0, // 26-30초
};

export const ReelsA: React.FC = () => {
  const { fps } = useVideoConfig();
  const t = (seconds: number) => Math.round(seconds * fps);

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      <TransitionSeries>
        {/* ─── 장면 1: HOOK (0-3초) - 공감 유도 ─── */}
        <TransitionSeries.Sequence
          durationInFrames={t(SCENE_DURATIONS.hook)}
        >
          <VideoClip src={VIDEOS.iamgamza} startFrom={0}>
            {/* 어두운 블루 오버레이 (밤 느낌) */}
            <div
              style={{
                position: "absolute",
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: "rgba(0,30,60,0.3)",
              }}
            />
            <Sequence from={5} layout="none">
              <Caption
                line1="밤마다 3번씩 깨는 엄마,"
                line2="여기 모여보세요"
                emoji="🙋‍♀️"
              />
            </Sequence>
          </VideoClip>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* ─── 장면 2: PROBLEM (3-6초) - 엄마의 고충 ─── */}
        <TransitionSeries.Sequence
          durationInFrames={t(SCENE_DURATIONS.problem)}
        >
          <VideoClip src={VIDEOS.violetyoon} startFrom={5}>
            <div
              style={{
                position: "absolute",
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background: "rgba(0,20,50,0.25)",
              }}
            />
            <Sequence from={5} layout="none">
              <Caption
                line1="밤마다 이불 전쟁..."
                line2="엄마도 잠 못 자요"
                emoji="💤"
              />
            </Sequence>
          </VideoClip>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={slide({ direction: "from-right" })}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* ─── 장면 3: SOLUTION (6-10초) - 슬리핑백 착용 ─── */}
        <TransitionSeries.Sequence
          durationInFrames={t(SCENE_DURATIONS.solution)}
        >
          <VideoClip src={VIDEOS.yoohyun} startFrom={3}>
            <Sequence from={5} layout="none">
              <BrandLogo brandName="SUNDAY HUG" brandColor="#5a7d65" />
            </Sequence>
            <Sequence from={8} layout="none">
              <Caption
                line1="꿀잠 슬리핑백 하나면 끝!"
                emoji="✨"
              />
            </Sequence>
          </VideoClip>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* ─── 장면 4: DEMO (10-16초) - 3가지 기능 빠른 전환 ─── */}
        <TransitionSeries.Sequence
          durationInFrames={t(SCENE_DURATIONS.demo)}
        >
          <AbsoluteFill>
            {/* 기능 1: 양방향 지퍼 (0-2초) */}
            <Sequence from={0} durationInFrames={t(2)} premountFor={fps}>
              <VideoClip src={VIDEOS.olchaea} startFrom={5}>
                <Sequence from={3} layout="none">
                  <FeatureText icon="🔗" text="양방향 지퍼 → 초간단" />
                </Sequence>
              </VideoClip>
            </Sequence>

            {/* 기능 2: 실키 밤부 소재 (2-4초) */}
            <Sequence from={t(2)} durationInFrames={t(2)} premountFor={fps}>
              <ImageSlide src={PHOTOS.minchebaby} zoomDirection="in">
                <Sequence from={3} layout="none">
                  <FeatureText icon="🌿" text="실키 밤부 → 피부에 안심" />
                </Sequence>
              </ImageSlide>
            </Sequence>

            {/* 기능 3: 기저귀 갈기 (4-6초) */}
            <Sequence from={t(4)} durationInFrames={t(2.4)} premountFor={fps}>
              <VideoClip src={VIDEOS.mmingkkong} startFrom={10}>
                <Sequence from={3} layout="none">
                  <FeatureText icon="👶" text="입은 채로 기저귀 OK" />
                </Sequence>
              </VideoClip>
            </Sequence>
          </AbsoluteFill>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* ─── 장면 5: RESULT (16-22초) - 아기 꿀잠 ─── */}
        <TransitionSeries.Sequence
          durationInFrames={t(SCENE_DURATIONS.result)}
        >
          <VideoClip src={VIDEOS.yoohyun} startFrom={15} playbackRate={0.8}>
            <Sequence from={10} layout="none">
              <Caption
                line1="뒤척여도 절대 벗겨지지 않아요"
                line2="이제 엄마도 아기도 꿀잠"
                emoji="💤"
              />
            </Sequence>
          </VideoClip>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* ─── 장면 6: SOCIAL PROOF (22-26초) - 리뷰 + 컬러 ─── */}
        <TransitionSeries.Sequence
          durationInFrames={t(SCENE_DURATIONS.socialProof)}
        >
          <AbsoluteFill style={{ backgroundColor: "#FFF8F0" }}>
            {/* 별점 */}
            <Sequence from={5} layout="none">
              <div
                style={{
                  position: "absolute",
                  top: 250,
                  left: 60,
                  right: 120,
                  textAlign: "center",
                }}
              >
                <span style={{ fontSize: 36, color: "#FFD700" }}>
                  {"★".repeat(5)}
                </span>
                <span
                  style={{
                    fontSize: 34,
                    fontWeight: 800,
                    color: "#3E2723",
                    fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
                    marginLeft: 12,
                  }}
                >
                  4.9 | 리뷰 227개
                </span>
              </div>
            </Sequence>

            {/* 컬러 스와치 */}
            <Sequence from={15} layout="none">
              <div
                style={{
                  position: "absolute",
                  top: 400,
                  left: 0,
                  right: 0,
                  bottom: 0,
                }}
              >
                <ColorSwatches showLabels />
              </div>
            </Sequence>

            {/* 6가지 컬러 텍스트 */}
            <Sequence from={10} layout="none">
              <div
                style={{
                  position: "absolute",
                  top: 340,
                  left: 60,
                  right: 120,
                  textAlign: "center",
                }}
              >
                <span
                  style={{
                    fontSize: 40,
                    fontWeight: 800,
                    color: "#3E2723",
                    fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
                  }}
                >
                  6가지 파스텔 컬러
                </span>
              </div>
            </Sequence>
          </AbsoluteFill>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* ─── 장면 7: CTA (26-30초) ─── */}
        <TransitionSeries.Sequence
          durationInFrames={t(SCENE_DURATIONS.cta)}
        >
          <VideoClip src={VIDEOS.mmingkkong} startFrom={18}>
            <Sequence from={3} layout="none">
              <CtaEndCard
                brandName="SUNDAY HUG"
                brandColor="#5a7d65"
                line1="'이걸 왜 이제야 샀지'"
                line2="후회되실 거예요"
                price="54,900원"
              />
            </Sequence>
          </VideoClip>
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};
