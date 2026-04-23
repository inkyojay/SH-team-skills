import React from "react";
import { Composition } from "remotion";

import { ProblemSolutionSample } from "./samples/ProblemSolutionSample";
import { EmotionalSample } from "./samples/EmotionalSample";
import { SocialProofSample } from "./samples/SocialProofSample";
import { BeforeAfterSample } from "./samples/BeforeAfterSample";
import { LifestyleRoutineSample } from "./samples/LifestyleRoutineSample";

/**
 * 소구점별 Remotion 영상 템플릿 프리뷰
 *
 * 각 템플릿을 Reels(9:16), Feed Square(1:1), Feed Vertical(4:5) 3개 포맷으로 등록합니다.
 * 실제 비디오/이미지 없이 플레이스홀더로 모션과 레이아웃을 확인할 수 있습니다.
 *
 * 실행: cd _preview && npm install && npm start
 */

const FORMATS = [
  { suffix: "Reels", width: 1080, height: 1920, label: "9:16" },
  { suffix: "Square", width: 1080, height: 1080, label: "1:1" },
  { suffix: "Vertical", width: 1080, height: 1350, label: "4:5" },
] as const;

const TEMPLATES = [
  { id: "01-ProblemSolution", component: ProblemSolutionSample, durationSec: 16, label: "01 문제-해결" },
  { id: "02-Emotional", component: EmotionalSample, durationSec: 22, label: "02 감성" },
  { id: "04-SocialProof", component: SocialProofSample, durationSec: 18, label: "04 사회적 증거" },
  { id: "07-BeforeAfter", component: BeforeAfterSample, durationSec: 13, label: "07 비포/애프터" },
  { id: "12-LifestyleRoutine", component: LifestyleRoutineSample, durationSec: 24, label: "12 라이프스타일" },
] as const;

const FPS = 30;

export const RemotionRoot: React.FC = () => {
  return (
    <>
      {TEMPLATES.map((template) =>
        FORMATS.map((format) => (
          <Composition
            key={`${template.id}-${format.suffix}`}
            id={`${template.id}-${format.suffix}`}
            // @ts-expect-error - readonly component type
            component={template.component}
            durationInFrames={FPS * template.durationSec}
            fps={FPS}
            width={format.width}
            height={format.height}
          />
        )),
      )}
    </>
  );
};
