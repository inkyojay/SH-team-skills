/* 썬데이허그 상세페이지 — 스크롤 애니메이션
   모든 .v 클래스 요소에 scroll-triggered fade-up 적용
   뷰포트 12% 진입 시 .on 클래스 추가 → rise 애니메이션 실행 */
const io=new IntersectionObserver(es=>{
  es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('on');io.unobserve(e.target);}});
},{threshold:.12,rootMargin:'0px 0px -30px 0px'});
document.querySelectorAll('.v').forEach(el=>io.observe(el));
