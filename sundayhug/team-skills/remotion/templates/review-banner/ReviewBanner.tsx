import React from "react";
import { AbsoluteFill, Sequence, useVideoConfig } from "remotion";

import type { ReviewBannerConfig } from "./types";
import { BabyPhoto } from "./components/BabyPhoto";
import { ReviewCard } from "./components/ReviewCard";
import { ProductBanner } from "./components/ProductBanner";

/**
 * 리뷰 배너형 광고 - 메인 컴포넌트
 *
 * 정적 컴포지트 레이아웃으로 리뷰 카드 + 제품 배너를 조합합니다.
 * 씬 전환 없이 각 요소가 순차적으로 등장하는 짧은 피드 광고입니다.
 *
 * 등장 순서:
 * 1. 배경 이미지/비디오 (페이드인)
 * 2. 리뷰 카드 (스케일인)
 * 3. 제품 배너 (슬라이드업)
 *
 * @example
 * ```tsx
 * <Composition
 *   id="ReviewBannerAd"
 *   component={ReviewBanner}
 *   durationInFrames={30 * 6}
 *   fps={30}
 *   width={1080}
 *   height={1920}
 *   defaultProps={{ config: myBannerConfig }}
 * />
 * ```
 */
export const ReviewBanner: React.FC<{ config: ReviewBannerConfig }> = ({
  config,
}) => {
  const { fps } = useVideoConfig();

  const durationSeconds = config.durationSeconds ?? 6;
  const durationInFrames = Math.round(durationSeconds * fps);
  const reviewDelay = config.reviewDelay ?? 15;
  const bannerDelay = config.bannerDelay ?? 30;

  return (
    <AbsoluteFill style={{ backgroundColor: "#000" }}>
      {/* ─── 배경 이미지/비디오 ─── */}
      <BabyPhoto
        src={config.backgroundSrc}
        isVideo={config.isBackgroundVideo}
        videoStartFrom={config.backgroundStartFrom}
        durationInFrames={durationInFrames}
      />

      {/* ─── 리뷰 카드 ─── */}
      <Sequence from={reviewDelay} layout="none">
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            paddingBottom: 200,
          }}
        >
          <ReviewCard
            rating={config.review.rating}
            reviewText={config.review.reviewText}
            reviewerName={config.review.reviewerName}
          />
        </div>
      </Sequence>

      {/* ─── 제품 배너 ─── */}
      <Sequence from={bannerDelay} layout="none">
        <div
          style={{
            position: "absolute",
            bottom: 120,
            left: 0,
            right: 0,
          }}
        >
          <ProductBanner
            imageSrc={config.product.imageSrc}
            productName={config.product.productName}
            priceText={config.product.priceText}
            ctaText={config.product.ctaText}
            brandColor={config.brand.color}
          />
        </div>
      </Sequence>
    </AbsoluteFill>
  );
};
