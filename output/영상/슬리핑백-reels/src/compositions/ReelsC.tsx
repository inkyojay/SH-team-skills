import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
} from "remotion";
import { TransitionSeries, linearTiming } from "@remotion/transitions";
import { fade } from "@remotion/transitions/fade";

import { VideoClip } from "../components/VideoClip";
import { ImageSlide } from "../components/ImageSlide";
import { ColorSwatches } from "../components/ColorSwatches";
import { VIDEOS, PHOTOS } from "../media-map";

/**
 * 릴스 C - 소재감 감성형 ASMR (20초)
 *
 * 구조: 원단 클로즈업(훅) → 밤부 리빌 → 3혜택 → 감성 수면 → CTA+컬러
 * 페이스: 느림, 감각적, 최소 텍스트
 * 트랜지션: 느린 fade (12프레임)
 */

const FPS = 30;
const TRANSITION_FRAMES = 12; // 느린 트랜지션

export const ReelsC: React.FC = () => {
  const { fps } = useVideoConfig();
  const t = (seconds: number) => Math.round(seconds * fps);

  return (
    <AbsoluteFill style={{ backgroundColor: "#1a1a1a" }}>
      <TransitionSeries>
        {/* ─── 장면 1: HOOK (0-3초) - 촉감 티저 ─── */}
        <TransitionSeries.Sequence durationInFrames={t(3.4)}>
          <VideoClip src={VIDEOS.mmingkkong} startFrom={0} playbackRate={0.7}>
            {/* 웜톤 오버레이 */}
            <div
              style={{
                position: "absolute",
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background:
                  "linear-gradient(180deg, rgba(40,30,20,0.2) 0%, rgba(40,30,20,0.1) 50%, rgba(40,30,20,0.5) 100%)",
              }}
            />
            <Sequence from={8} layout="none">
              <TypewriterCaption text="새벽 3시, 습관처럼 눈이 떠졌는데..." />
            </Sequence>
          </VideoClip>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* ─── 장면 2: REVEAL (3-7초) - "사실은 대나무" ─── */}
        <TransitionSeries.Sequence durationInFrames={t(4.4)}>
          <ImageSlide
            src={PHOTOS.minchebaby}
            zoomDirection="out"
            zoomRange={[1.15, 1.0]}
            backgroundColor="#FFF8F0"
          >
            <Sequence from={10} layout="none">
              <div
                style={{
                  position: "absolute",
                  top: 0,
                  left: 60,
                  right: 120,
                  bottom: 340,
                  display: "flex",
                  justifyContent: "center",
                  alignItems: "center",
                }}
              >
                <BambooRevealCard />
              </div>
            </Sequence>
          </ImageSlide>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* ─── 장면 3: 3가지 혜택 (7-11초) ─── */}
        <TransitionSeries.Sequence durationInFrames={t(4.4)}>
          <AbsoluteFill>
            {/* 서브 씬 3-1: 통기성 */}
            <Sequence from={0} durationInFrames={t(1.4)} premountFor={fps}>
              <ImageSlide src={PHOTOS.myluv} zoomDirection="in">
                <Sequence from={3} layout="none">
                  <GlowText text="통기성 면의 3배" />
                </Sequence>
              </ImageSlide>
            </Sequence>

            {/* 서브 씬 3-2: 항균 */}
            <Sequence from={t(1.4)} durationInFrames={t(1.4)} premountFor={fps}>
              <ImageSlide src={PHOTOS.honeys} zoomDirection="in">
                <Sequence from={3} layout="none">
                  <GlowText text="천연 항균" />
                </Sequence>
              </ImageSlide>
            </Sequence>

            {/* 서브 씬 3-3: 온도 조절 */}
            <Sequence from={t(2.8)} durationInFrames={t(1.6)} premountFor={fps}>
              <VideoClip src={VIDEOS.olchaea} startFrom={12} playbackRate={0.8}>
                <Sequence from={3} layout="none">
                  <GlowText text="사계절 온도 조절" />
                </Sequence>
              </VideoClip>
            </Sequence>
          </AbsoluteFill>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* ─── 장면 4: 감성 수면 (11-16초) ─── */}
        <TransitionSeries.Sequence durationInFrames={t(5.4)}>
          <VideoClip src={VIDEOS.yoohyun} startFrom={18} playbackRate={0.7}>
            {/* 따뜻한 비네트 */}
            <div
              style={{
                position: "absolute",
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                background:
                  "radial-gradient(ellipse at center, rgba(0,0,0,0) 50%, rgba(30,15,0,0.4) 100%)",
              }}
            />
            <Sequence from={15} layout="none">
              <SoftCaption
                line1="예민한 우리 아기도"
                line2="이 안에서는 꿀잠 🌙"
              />
            </Sequence>
          </VideoClip>
        </TransitionSeries.Sequence>

        <TransitionSeries.Transition
          presentation={fade()}
          timing={linearTiming({ durationInFrames: TRANSITION_FRAMES })}
        />

        {/* ─── 장면 5: CTA + 컬러 FOMO (16-20초) ─── */}
        <TransitionSeries.Sequence durationInFrames={t(4.0)}>
          <AbsoluteFill style={{ backgroundColor: "#FFF8F0" }}>
            {/* 컬러 스와치 (블룸 라벤더 강조) */}
            <Sequence from={0} layout="none">
              <div
                style={{
                  position: "absolute",
                  top: 200,
                  left: 0,
                  right: 0,
                  height: 600,
                }}
              >
                <ColorSwatches highlightIndex={5} showLabels />
              </div>
            </Sequence>

            {/* FOMO 카피 */}
            <Sequence from={15} layout="none">
              <div
                style={{
                  position: "absolute",
                  bottom: 500,
                  left: 60,
                  right: 120,
                  textAlign: "center",
                }}
              >
                <p
                  style={{
                    fontSize: 42,
                    fontWeight: 800,
                    color: "#B39DDB",
                    fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
                    margin: 0,
                  }}
                >
                  블룸 라벤더
                </p>
                <p
                  style={{
                    fontSize: 36,
                    fontWeight: 600,
                    color: "#3E2723",
                    fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
                    margin: "4px 0 0",
                  }}
                >
                  나만 알고 싶었는데 인기 폭발 💜
                </p>
              </div>
            </Sequence>

            {/* CTA */}
            <Sequence from={25} layout="none">
              <div
                style={{
                  position: "absolute",
                  bottom: 370,
                  left: 60,
                  right: 120,
                  textAlign: "center",
                }}
              >
                <span
                  style={{
                    fontSize: 30,
                    fontWeight: 500,
                    color: "#5D4037",
                    fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
                  }}
                >
                  프로필 링크에서 만나보세요
                </span>
              </div>
            </Sequence>

            {/* 브랜드 로고 */}
            <div
              style={{
                position: "absolute",
                bottom: 340,
                left: 60,
                right: 120,
                textAlign: "center",
              }}
            >
              <span
                style={{
                  fontSize: 22,
                  fontWeight: 700,
                  color: "#5a7d65",
                  fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
                  letterSpacing: 3,
                }}
              >
                SUNDAY HUG
              </span>
            </div>
          </AbsoluteFill>
        </TransitionSeries.Sequence>
      </TransitionSeries>
    </AbsoluteFill>
  );
};

// ─── 릴스 C 전용 서브 컴포넌트 ───

/** 타이프라이터 자막 (글자 한 자씩 등장) */
const TypewriterCaption: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const charsToShow = Math.min(
    text.length,
    Math.floor(frame / (fps * 0.06)), // 0.06초마다 한 글자
  );

  return (
    <div
      style={{
        position: "absolute",
        bottom: 400,
        left: 60,
        right: 120,
        textAlign: "center",
      }}
    >
      <span
        style={{
          fontSize: 42,
          fontWeight: 300, // Light (우아한 느낌)
          color: "rgba(255,255,255,0.9)",
          fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
          textShadow: "0 2px 12px rgba(0,0,0,0.8)",
          letterSpacing: 1,
        }}
      >
        {text.slice(0, charsToShow)}
        <span style={{ opacity: frame % 15 < 8 ? 1 : 0 }}>|</span>
      </span>
    </div>
  );
};

/** 밤부 리빌 카드 */
const BambooRevealCard: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const pop = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 150 },
  });

  return (
    <div
      style={{
        background: "rgba(255,255,255,0.85)",
        borderRadius: 24,
        padding: "32px 48px",
        backdropFilter: "blur(8px)",
        boxShadow: "0 8px 32px rgba(0,0,0,0.1)",
        transform: `scale(${interpolate(pop, [0, 1], [0.8, 1])})`,
        opacity: interpolate(pop, [0, 1], [0, 1]),
        textAlign: "center",
      }}
    >
      <p
        style={{
          fontSize: 48,
          fontWeight: 600,
          color: "#5D4037",
          fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
          margin: 0,
        }}
      >
        사실은 대나무예요 🎋
      </p>
    </div>
  );
};

/** 글로우 텍스트 (기능 키워드) */
const GlowText: React.FC<{ text: string }> = ({ text }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fadeIn = spring({
    frame,
    fps,
    config: { damping: 15, stiffness: 200 },
  });

  return (
    <div
      style={{
        position: "absolute",
        top: 0,
        left: 60,
        right: 120,
        bottom: 340,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        opacity: interpolate(fadeIn, [0, 1], [0, 1]),
      }}
    >
      <span
        style={{
          fontSize: 56,
          fontWeight: 800,
          color: "#fff",
          fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
          textShadow:
            "0 0 40px rgba(255,255,255,0.5), 0 4px 16px rgba(0,0,0,0.7)",
          letterSpacing: 2,
        }}
      >
        {text}
      </span>
    </div>
  );
};

/** 부드러운 자막 (감성 씬용) */
const SoftCaption: React.FC<{ line1: string; line2: string }> = ({
  line1,
  line2,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const fadeIn = interpolate(frame, [0, fps * 1], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <div
      style={{
        position: "absolute",
        top: 250,
        left: 60,
        right: 120,
        textAlign: "center",
        opacity: fadeIn,
      }}
    >
      <p
        style={{
          fontSize: 42,
          fontWeight: 400,
          color: "#FFF5E6",
          fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
          textShadow: "0 2px 16px rgba(0,0,0,0.7)",
          lineHeight: 1.5,
          margin: 0,
        }}
      >
        {line1}
      </p>
      <p
        style={{
          fontSize: 42,
          fontWeight: 400,
          color: "#FFF5E6",
          fontFamily: "Pretendard, 'Noto Sans KR', system-ui, sans-serif",
          textShadow: "0 2px 16px rgba(0,0,0,0.7)",
          lineHeight: 1.5,
          margin: "4px 0 0",
        }}
      >
        {line2}
      </p>
    </div>
  );
};
