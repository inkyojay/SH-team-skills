/**
 * 미디어 파일 매핑
 *
 * 소스: /Users/inkyo/Downloads/슬리핑백/
 * Remotion에서는 public/media/ 심링크를 통해 접근
 * setup.sh 실행 필요
 */

// ─── 영상 소스 (720x1280, 9:16) ───
export const VIDEOS = {
  /** @iamgamza - 55.9초, 720x1280, 11.8MB */
  iamgamza: "media/_iamgamza_1760199121_3741142369095042387_52885396971.mp4",
  /** @im_yoohyun - 25.7초, 720x1280, 3.3MB */
  yoohyun: "media/im_yoohyun_1760530509_3743911904265065272_66310175573.mp4",
  /** @mming_kkong__ - 28.3초, 720x1280, 3.8MB */
  mmingkkong: "media/mming_kkong__1760531956_3743934751872058491_3587164260.mp4",
  /** @ol_chaea - 22.3초, 720x1280, 3.2MB */
  olchaea: "media/ol_chaea_1760483522_3743528985323292336_69193025607.mp4",
  /** @our.kongtteok - 44.8초, 360x640, 1.7MB (저해상도) */
  kongtteok: "media/our.kongtteok_1760102100_3740327831483385662_64649054412.mp4",
  /** @violet_yoon - 49.4초, 720x1280, 8.3MB */
  violetyoon: "media/violet_yoon_1762774259_3762745258447966364_1401592524.mp4",
} as const;

// ─── 사진 소스 (인플루언서별 대표 1장) ───
export const PHOTOS = {
  /** @__minchebaby - 제품 착용샷 */
  minchebaby: "media/__minchebaby_1760266569_3741709635683298010_70841086281.jpg",
  /** @ddidong2_m21 - 실사용 */
  ddidong: "media/ddidong2_m21_1760173473_3740928689001534611_44615471898.jpg",
  /** @hi_seowo_o - 아기 사진 */
  seowoo: "media/hi_seowo_o_1758420925_3726227258068877754_65366928480.jpg",
  /** @im_yoohyun - 제품 사진 */
  yoohyunPhoto: "media/im_yoohyun_1759984598_3739344290842913782_66310175573.jpg",
  /** @ji_eunwoooo - 제이드 그린 착용 */
  jieunwoo: "media/ji_eunwoooo_1758544683_3727265411953226230_56729168769.jpg",
  /** @mming_kkong__ - 착용샷 */
  mmingkkongPhoto: "media/mming_kkong__1760015410_3739602762645870166_3587164260.jpg",
  /** @mongdol.zip - 블룸 라벤더 */
  mongdol: "media/mongdol.zip_1762759114_3762618618493516369_69437222169.jpg",
  /** @myluv_jua - 베이비 핑크 */
  myluv: "media/myluv_jua_1758595506_3727691748417412141_68917446288.jpg",
  /** @ol_chaea - 오트 베이지 */
  olchaeaPhoto: "media/ol_chaea_1759919392_3738797308504064982_69193025607.jpg",
  /** @ss__honeys__ss - 화이트 크림 */
  honeys: "media/ss__honeys__ss_1758256537_3724848265812841821_51850137427.jpg",
  /** @ddyo0ong */
  ddyoong: "media/ddyo0ong_1758590065_3727646106764593091_65733054277.jpg",
} as const;
