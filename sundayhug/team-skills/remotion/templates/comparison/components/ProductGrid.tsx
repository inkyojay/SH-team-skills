import React from "react";
import {
  AbsoluteFill,
  Img,
  useCurrentFrame,
  useVideoConfig,
  spring,
  interpolate,
  staticFile,
} from "remotion";

import type { ProductItem } from "../types";

/**
 * 제품 비교 그리드 컴포넌트
 *
 * 2~4개 제품을 그리드로 배치하여 비교합니다.
 * 추천 제품은 브랜드 컬러 보더로 하이라이트됩니다.
 */
export const ProductGrid: React.FC<{
  products: ProductItem[];
  questionText?: string;
  brandColor?: string;
  children?: React.ReactNode;
}> = ({ products, questionText, brandColor = "#4A90D9", children }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const titleProgress = spring({
    frame,
    fps,
    config: { damping: 12, stiffness: 150 },
  });

  const cols = products.length <= 2 ? 2 : 2;
  const rows = Math.ceil(products.length / cols);

  return (
    <AbsoluteFill style={{ backgroundColor: "#111" }}>
      {/* 상단 질문 텍스트 */}
      {questionText && (
        <div
          style={{
            position: "absolute",
            top: 120,
            left: 0,
            right: 0,
            display: "flex",
            justifyContent: "center",
            opacity: interpolate(titleProgress, [0, 1], [0, 1]),
            transform: `translateY(${interpolate(titleProgress, [0, 1], [20, 0])}px)`,
          }}
        >
          <p
            style={{
              fontSize: 52,
              fontWeight: 900,
              color: "#fff",
              fontFamily: "Pretendard, system-ui, -apple-system, sans-serif",
              textAlign: "center",
              margin: 0,
              textShadow: "0 2px 8px rgba(0,0,0,0.5)",
            }}
          >
            {questionText}
          </p>
        </div>
      )}

      {/* 제품 그리드 */}
      <div
        style={{
          position: "absolute",
          top: questionText ? 260 : 200,
          left: 40,
          right: 40,
          bottom: 400,
          display: "grid",
          gridTemplateColumns: `repeat(${cols}, 1fr)`,
          gridTemplateRows: `repeat(${rows}, 1fr)`,
          gap: 20,
        }}
      >
        {products.map((product, i) => {
          const itemProgress = spring({
            frame: frame - i * 5,
            fps,
            config: { damping: 12, stiffness: 150 },
          });

          return (
            <div
              key={i}
              style={{
                background: "rgba(255,255,255,0.08)",
                borderRadius: 24,
                padding: 20,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
                gap: 12,
                border: product.isRecommended
                  ? `4px solid ${brandColor}`
                  : "2px solid rgba(255,255,255,0.15)",
                opacity: interpolate(itemProgress, [0, 1], [0, 1]),
                transform: `scale(${interpolate(itemProgress, [0, 1], [0.8, 1])})`,
              }}
            >
              <Img
                src={staticFile(product.imageSrc)}
                style={{
                  width: "80%",
                  height: "60%",
                  objectFit: "contain",
                  borderRadius: 12,
                }}
              />
              <p
                style={{
                  fontSize: 28,
                  fontWeight: 700,
                  color: product.isRecommended ? brandColor : "#fff",
                  fontFamily:
                    "Pretendard, system-ui, -apple-system, sans-serif",
                  textAlign: "center",
                  margin: 0,
                }}
              >
                {product.name}
              </p>
              {product.description && (
                <p
                  style={{
                    fontSize: 22,
                    fontWeight: 400,
                    color: "rgba(255,255,255,0.7)",
                    fontFamily:
                      "Pretendard, system-ui, -apple-system, sans-serif",
                    textAlign: "center",
                    margin: 0,
                  }}
                >
                  {product.description}
                </p>
              )}
              {product.isRecommended && (
                <div
                  style={{
                    background: brandColor,
                    borderRadius: 20,
                    padding: "6px 16px",
                  }}
                >
                  <span
                    style={{
                      fontSize: 20,
                      fontWeight: 700,
                      color: "#fff",
                      fontFamily:
                        "Pretendard, system-ui, -apple-system, sans-serif",
                    }}
                  >
                    추천
                  </span>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {children}
    </AbsoluteFill>
  );
};
