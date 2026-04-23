/* 사용자 전용 JS를 정의합니다. */


/* 세트 제품 슬라이드 */

// 즉시 실행 함수로 감싸서 독립적인 스코프 생성
(function() {
    // 안전한 DOM 로드 방식 (jQuery와 충돌 방지)
    function whenDocumentReady(fn) {
        if (document.readyState !== 'loading') {
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    }
    
    whenDocumentReady(function() {
        // 모든 코드를 로컬 변수로 격리
        // 필요한 요소 선택
        const sliderContainer = document.querySelector('.sunday-slider-container');
        const slides = document.querySelectorAll('.sunday-slide');
        const prevBtn = document.querySelector('.sunday-prev-btn');
        const nextBtn = document.querySelector('.sunday-next-btn');
        const dotsContainer = document.querySelector('.sunday-dots');
        const setContents = document.querySelectorAll('.sunday-set-content');
        
        // 애니메이션 프레임 ID 관리
        let animationFrameId = null;
        
        // 변수 초기화
        let currentIndex = 0;
        const totalSlides = slides.length;
        let slideWidth = slides[0].clientWidth;
        let touchStartX = 0;
        let touchMoveX = 0;
        let isDragging = false;
        let startPos = 0;
        let currentTranslate = 0;
        
        // 도트 생성
        for (let i = 0; i < totalSlides; i++) {
            const dot = document.createElement('div');
            dot.classList.add('sunday-dot');
            if (i === 0) dot.classList.add('active');
            dot.addEventListener('click', function() {
                goToSlide(i);
            });
            dotsContainer.appendChild(dot);
        }
        
        // 도트 선택
        const dots = document.querySelectorAll('.sunday-dot');
        
        // 윈도우 리사이즈 이벤트 처리
        window.addEventListener('resize', function() {
            // 디바운스 처리
            clearTimeout(window.resizeTimeout);
            window.resizeTimeout = setTimeout(function() {
                slideWidth = slides[0].clientWidth;
                goToSlide(currentIndex, false); // 애니메이션 없이 즉시 이동
            }, 200);
        });
        
        // 이전 슬라이드로 이동
        prevBtn.addEventListener('click', function() {
            if (currentIndex > 0) {
                goToSlide(currentIndex - 1);
            } else {
                goToSlide(totalSlides - 1); // 마지막 슬라이드로 이동
            }
        });
        
        // 다음 슬라이드로 이동
        nextBtn.addEventListener('click', function() {
            if (currentIndex < totalSlides - 1) {
                goToSlide(currentIndex + 1);
            } else {
                goToSlide(0); // 첫 번째 슬라이드로 이동
            }
        });
        
        // 터치 및 마우스 이벤트 처리 (모바일 스와이프 향상)
        function setupTouchEvents() {
            // 터치 이벤트
            sliderContainer.addEventListener('touchstart', touchStart, { passive: true });
            sliderContainer.addEventListener('touchmove', touchMove, { passive: true });
            sliderContainer.addEventListener('touchend', touchEnd);
            
            // 마우스 이벤트 (데스크톱)
            sliderContainer.addEventListener('mousedown', touchStart);
            sliderContainer.addEventListener('mousemove', touchMove);
            sliderContainer.addEventListener('mouseup', touchEnd);
            sliderContainer.addEventListener('mouseleave', touchEnd);
            
            // 컨텍스트 메뉴 방지
            sliderContainer.addEventListener('contextmenu', function(e) {
                e.preventDefault();
                e.stopPropagation();
                return false;
            });
        }
        
        function getPositionX(event) {
            return event.type.includes('mouse') ? event.pageX : event.touches[0].clientX;
        }
        
        function touchStart(event) {
            startPos = getPositionX(event);
            isDragging = true;
            
            // 진행 중인 애니메이션 취소
            if (animationFrameId) {
                cancelAnimationFrame(animationFrameId);
            }
            
            // 현재 translateX 값 저장
            const transformMatrix = window.getComputedStyle(sliderContainer).getPropertyValue('transform');
            if (transformMatrix !== 'none') {
                const matrix = transformMatrix.match(/^matrix\((.+)\)$/);
                if (matrix) {
                    const matrixValues = matrix[1].split(', ');
                    currentTranslate = parseFloat(matrixValues[4]);
                }
            } else {
                currentTranslate = 0;
            }
        }
        
        function touchMove(event) {
            if (isDragging) {
                const currentPosition = getPositionX(event);
                const diff = currentPosition - startPos;
                
                // requestAnimationFrame으로 부드러운 움직임 구현
                animationFrameId = requestAnimationFrame(function() {
                    sliderContainer.style.transform = `translateX(${currentTranslate + diff}px)`;
                });
                
                // 현재 움직인 위치 저장 (touchEnd에서 사용)
                touchMoveX = currentPosition;
            }
        }
        
        function touchEnd() {
            isDragging = false;
            
            if (animationFrameId) {
                cancelAnimationFrame(animationFrameId);
            }
            
            const movedBy = touchMoveX - startPos;
            
            // 임계값 (슬라이드 너비의 20%)
            const threshold = slideWidth * 0.2;
            
            if (movedBy < -threshold) {
                // 왼쪽으로 스와이프 - 다음 슬라이드
                if (currentIndex < totalSlides - 1) {
                    goToSlide(currentIndex + 1);
                } else {
                    goToSlide(0); // 첫 슬라이드로 순환
                }
            } else if (movedBy > threshold) {
                // 오른쪽으로 스와이프 - 이전 슬라이드
                if (currentIndex > 0) {
                    goToSlide(currentIndex - 1);
                } else {
                    goToSlide(totalSlides - 1); // 마지막 슬라이드로 순환
                }
            } else {
                // 임계값 이하로 움직였으면 현재 슬라이드로 복귀
                goToSlide(currentIndex);
            }
            
            // 변수 초기화
            touchStartX = 0;
            touchMoveX = 0;
        }
        
        // 특정 슬라이드로 이동
        function goToSlide(index, animate = true) {
            currentIndex = index;
            
            if (animate) {
                sliderContainer.style.transition = 'transform 0.5s ease';
            } else {
                sliderContainer.style.transition = 'none';
            }
            
            sliderContainer.style.transform = `translateX(-${slideWidth * currentIndex}px)`;
            
            // 트랜지션 후 복원
            if (!animate) {
                setTimeout(() => {
                    sliderContainer.style.transition = 'transform 0.5s ease';
                }, 50);
            }
            
            updateDots();
            updateSetContent();
        }
        
        // 도트 업데이트
        function updateDots() {
            dots.forEach((dot, index) => {
                if (index === currentIndex) {
                    dot.classList.add('active');
                } else {
                    dot.classList.remove('active');
                }
            });
        }
        
        // 세트 내용 업데이트
        function updateSetContent() {
            const activeSlide = slides[currentIndex];
            const setId = activeSlide.getAttribute('data-set');
            
            setContents.forEach(content => {
                content.classList.remove('active');
            });
            
            const targetContent = document.getElementById('sunday-set-' + setId);
            if (targetContent) {
                targetContent.classList.add('active');
            }
            
            // 디버깅 (필요 시 주석 처리)
            console.log('현재 슬라이드:', currentIndex, '세트 ID:', setId);
        }
        
        // 슬라이더 초기화
        function initSlider() {
            setupTouchEvents();
            updateSetContent();
            
            // 모바일 뷰포트 메타 태그 확인
            let viewportMeta = document.querySelector('meta[name="viewport"]');
            if (!viewportMeta) {
                viewportMeta = document.createElement('meta');
                viewportMeta.name = 'viewport';
                document.getElementsByTagName('head')[0].appendChild(viewportMeta);
            }
            viewportMeta.content = 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no';
        }
        
        // 초기화 호출
        initSlider();
    });
})(); 




/* 버튼형 제품 슬라이드 */


// 컬러 버튼 기능
$(document).ready(function() {
    $('#c_btnbox1 > li').click(function() {
        var indexNo = $(this).index();
        $(this).addClass("on").siblings().removeClass("on");
        $('#c_bgbox1 > li').eq(indexNo).addClass("on").siblings().removeClass("on");
    });
});

// 몰 스와이퍼 초기화
$(document).ready(function() {
    $('[id^=\'mall_swiper_slide\']').each(function(index) {
        index = index + 1;
        var slidePage = '#mall_swiper_slide' + index + ' .swiper-pagination';
        var slideScr = '#mall_swiper_slide' + index + ' .swiper-scrollbar';
        var mallSlide = new Swiper(this, {
            slidesPerView: 1.19,
            slidesPerGroup: 1,
            spaceBetween: '3%',
            centeredSlides: true,
            observer: true,
            observeParents: true,
            //loop: true,
            pagination: true,
            pagination: {
                el: slidePage,
                clickable: true,
            },
            scrollbar: {
                el: slideScr,
                hide: true,
            },
        });
    });
});


/* 원단 탭 기능 */

document.addEventListener('DOMContentLoaded', function() {
    // 원단 탭 기능 구현
    const tabButtons = document.querySelectorAll('.sh_fabric-tab-btn');
    const fabricItems = document.querySelectorAll('.sh_fabric-content-item');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', function() {
            const fabricType = this.getAttribute('data-fabric');
            
            // 모든 탭 버튼에서 active 클래스 제거
            tabButtons.forEach(btn => btn.classList.remove('active'));
            
            // 현재 클릭된 버튼에 active 클래스 추가
            this.classList.add('active');
            
            // 모든 컨텐츠 아이템에서 active 클래스 제거
            fabricItems.forEach(item => item.classList.remove('active'));
            
            // 선택된 패브릭 아이템에 active 클래스 추가
            document.getElementById(fabricType).classList.add('active');
        });
    });
});


  /**
 * 선물세트 페이지 자바스크립트
 * FAQ 토글 기능과 탭 전환 기능을 포함합니다.
 */

// DOM이 완전히 로드된 후 스크립트 실행
document.addEventListener('DOMContentLoaded', function() {
    // FAQ 토글 기능
    initFaqToggle();
    
    // 탭 전환 기능
    initTabSwitching();
});

/**
 * FAQ 아코디언 토글 기능 초기화
 */
function initFaqToggle() {
    // 모든 FAQ 질문 요소 선택
    const faqQuestions = document.querySelectorAll('.faq-question');
    
    // 초기 상태에서는 모든 답변 숨기기
    document.querySelectorAll('.faq-answer').forEach(answer => {
        answer.style.display = 'none';
    });
    
    // 각 질문에 클릭 이벤트 리스너 추가
    faqQuestions.forEach(question => {
        question.addEventListener('click', () => {
            // 현재 답변 요소 가져오기
            const answer = question.nextElementSibling;
            // 현재 열림/닫힘 상태 확인
            const isOpen = answer.style.display === 'block';
            
            // 상태에 따라 토글
            answer.style.display = isOpen ? 'none' : 'block';
            // + / - 아이콘 변경
            question.querySelector('span').textContent = isOpen ? '+' : '-';
        });
    });
}

/**
 * 선물세트 탭 전환 기능 초기화
 */
function initTabSwitching() {
    // 모든 탭 요소 선택
    const tabs = document.querySelectorAll('.gift-tab');
    
    // 각 탭에 클릭 이벤트 리스너 추가
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // 현재 활성화된 탭 찾기
            const activeTab = document.querySelector('.gift-tab.active');
            
            // 이미 활성화된 탭이면 아무것도 하지 않음
            if (tab === activeTab) return;
            
            // 현재 활성화된 탭에서 active 클래스 제거
            activeTab.classList.remove('active');
            
            // 클릭한 탭에 active 클래스 추가
            tab.classList.add('active');
            
            // 여기에 탭 내용 전환 로직 추가
            switchTabContent(tab.textContent);
        });
    });
}

/**
 * 선택한 탭에 따라 콘텐츠를 전환하는 함수
 * @param {string} tabName - 선택한 탭의 이름
 */
function switchTabContent(tabName) {
    // 이 함수는 실제 구현 시 각 탭에 맞는 콘텐츠를 표시하도록 확장
    console.log(`${tabName} 탭으로 전환됩니다.`);
    
    // 예: 탭에 따라 다른 선물세트 상품을 표시하는 로직
    // 여기서는 간단한 예시만 제공
    
    // 1. 모든 상품 섹션 숨기기
    // document.querySelectorAll('.gift-section').forEach(section => {
    //     section.style.display = 'none';
    // });
    
    // 2. 선택된 탭에 해당하는 섹션만 표시
    // const selectedSection = document.querySelector(`.gift-section[data-tab="${tabName}"]`);
    // if (selectedSection) {
    //     selectedSection.style.display = 'block';
    // }
    
    // 실제 구현 시에는 서버에서 데이터를 가져오거나 
    // 미리 로드된 데이터를 필터링하여 표시하는 로직이 필요합니다.
}



/* 썬데이허그 스와들 슬라이더 */
(function() {
    // DOM 로드 후 초기화
    function initWhenReady(fn) {
      if (document.readyState !== 'loading') {
        fn();
      } else {
        document.addEventListener('DOMContentLoaded', fn);
      }
    }
    
    initWhenReady(function() {
      // 필요한 요소 선택
      const sliderContainer = document.querySelector('.sunday-slider-container');
      // 정확히 .sunday-slide 클래스를 가진 요소만 선택
      const slides = document.querySelectorAll('.sunday-slide');
      const prevBtn = document.querySelector('.sunday-prev-btn');
      const nextBtn = document.querySelector('.sunday-next-btn');
      const dotsContainer = document.querySelector('.sunday-dots');
      const setContents = document.querySelectorAll('.sunday-set-content');
      
      // 도트 컨테이너 내용 초기화 (기존 도트가 있을 경우 제거)
      dotsContainer.innerHTML = '';
      
      // 변수 초기화
      let currentIndex = 0;
      // 슬라이드 개수 로그 확인
      const totalSlides = slides.length;
      console.log('슬라이드 총 개수:', totalSlides);
      
      let slideWidth = slides[0].clientWidth;
      let touchStartX = 0;
      let touchEndX = 0;
      let isDragging = false;
      
      // 도트 생성 - 정확히 슬라이드 개수만큼만 생성
      for (let i = 0; i < totalSlides; i++) {
        const dot = document.createElement('div');
        dot.classList.add('sunday-dot');
        if (i === 0) dot.classList.add('active');
        dot.addEventListener('click', function() {
          goToSlide(i);
        });
        dotsContainer.appendChild(dot);
      }
      
      // 도트 선택
      const dots = document.querySelectorAll('.sunday-dot');
      console.log('생성된 도트 개수:', dots.length);
      
      // 윈도우 리사이즈 이벤트
      window.addEventListener('resize', function() {
        clearTimeout(window.resizedFinished);
        window.resizedFinished = setTimeout(function() {
          slideWidth = slides[0].clientWidth;
          goToSlide(currentIndex, false);
        }, 250);
      });
      
      // 이전 슬라이드
      prevBtn.addEventListener('click', function() {
        if (currentIndex > 0) {
          goToSlide(currentIndex - 1);
        } else {
          goToSlide(totalSlides - 1); // 마지막 슬라이드로
        }
      });
      
      // 다음 슬라이드
      nextBtn.addEventListener('click', function() {
        if (currentIndex < totalSlides - 1) {
          goToSlide(currentIndex + 1);
        } else {
          goToSlide(0); // 첫 슬라이드로
        }
      });
      
      // 터치 이벤트
      function setupTouchEvents() {
        sliderContainer.addEventListener('touchstart', touchStart, { passive: true });
        sliderContainer.addEventListener('touchmove', touchMove, { passive: true });
        sliderContainer.addEventListener('touchend', touchEnd);
        
        // 마우스 이벤트 (데스크톱)
        sliderContainer.addEventListener('mousedown', touchStart);
        sliderContainer.addEventListener('mousemove', touchMove);
        sliderContainer.addEventListener('mouseup', touchEnd);
        sliderContainer.addEventListener('mouseleave', touchEnd);
      }
      
      function touchStart(e) {
        touchStartX = e.type.includes('mouse') ? e.pageX : e.touches[0].clientX;
        isDragging = true;
        sliderContainer.style.transition = 'none';
      }
      
      function touchMove(e) {
        if (!isDragging) return;
        
        const currentPosition = e.type.includes('mouse') ? e.pageX : e.touches[0].clientX;
        const diff = currentPosition - touchStartX;
        
        // 현재 위치에서 드래그 거리만큼 이동
        sliderContainer.style.transform = `translateX(${-currentIndex * slideWidth + diff}px)`;
        
        touchEndX = currentPosition;
      }
      
      function touchEnd() {
        isDragging = false;
        sliderContainer.style.transition = 'transform 0.5s ease';
        
        if (touchStartX === 0 || touchEndX === 0) return;
        
        const diff = touchEndX - touchStartX;
        
        // 스와이프 방향 결정 (슬라이드 너비의 20% 이상 이동)
        if (diff < -slideWidth * 0.2) {
          // 왼쪽으로 스와이프 - 다음 슬라이드
          if (currentIndex < totalSlides - 1) {
            goToSlide(currentIndex + 1);
          } else {
            goToSlide(0);
          }
        } else if (diff > slideWidth * 0.2) {
          // 오른쪽으로 스와이프 - 이전 슬라이드
          if (currentIndex > 0) {
            goToSlide(currentIndex - 1);
          } else {
            goToSlide(totalSlides - 1);
          }
        } else {
          // 충분히 스와이프하지 않았으면 현재 슬라이드로 복귀
          goToSlide(currentIndex);
        }
        
        // 변수 초기화
        touchStartX = 0;
        touchEndX = 0;
      }
      
      // 특정 슬라이드로 이동
      function goToSlide(index, animate = true) {
        currentIndex = index;
        
        if (animate) {
          sliderContainer.style.transition = 'transform 0.5s ease';
        } else {
          sliderContainer.style.transition = 'none';
        }
        
        sliderContainer.style.transform = `translateX(-${slideWidth * currentIndex}px)`;
        
        // 트랜지션 복원
        if (!animate) {
          setTimeout(() => {
            sliderContainer.style.transition = 'transform 0.5s ease';
          }, 50);
        }
        
        updateDots();
        updateContent();
      }
      
      // 도트 업데이트
      function updateDots() {
        dots.forEach((dot, index) => {
          if (index === currentIndex) {
            dot.classList.add('active');
          } else {
            dot.classList.remove('active');
          }
        });
      }
      
      // 상세 컨텐츠 업데이트
      function updateContent() {
        const activeSlide = slides[currentIndex];
        const setId = activeSlide.getAttribute('data-set');
        
        setContents.forEach(content => {
          content.classList.remove('active');
        });
        
        const targetContent = document.getElementById('sunday-set-' + setId);
        if (targetContent) {
          targetContent.classList.add('active');
        }
      }
      
      // 자동 슬라이드 (선택사항)
      let autoSlideInterval;
      
      function startAutoSlide() {
        autoSlideInterval = setInterval(() => {
          if (currentIndex < totalSlides - 1) {
            goToSlide(currentIndex + 1);
          } else {
            goToSlide(0);
          }
        }, 5000); // 5초마다 슬라이드
      }
      
      function stopAutoSlide() {
        clearInterval(autoSlideInterval);
      }
      
      // 마우스 올리면 자동 슬라이드 정지
      const slider = document.querySelector('.sunday-simple-slider');
      if (slider) {
        slider.addEventListener('mouseenter', stopAutoSlide);
        slider.addEventListener('mouseleave', startAutoSlide);
      }
      
      // 초기화
      function init() {
        setupTouchEvents();
        startAutoSlide();
      }
      
      init();
    });
  })();


(function() {
  document.addEventListener('DOMContentLoaded', function() {
    // ==========================
    // 1. 소재 탭 전환
    // ==========================
    document.querySelectorAll('.sh_fabric-tab-btn').forEach(tab => {
      tab.addEventListener('click', function() {
        document.querySelectorAll('.sh_fabric-tab-btn').forEach(btn => btn.classList.remove('active'));
        document.querySelectorAll('.sh_fabric-content-item').forEach(item => item.classList.remove('active'));
        this.classList.add('active');
        document.getElementById(this.getAttribute('data-fabric')).classList.add('active');

        // 탭 클릭 시 옵션 텍스트 갱신
        updateOptionText();
      });
    });

    // ==========================
    // 2. 색상 버튼 전환
    // ==========================
    document.querySelectorAll('.sh_fabric-content-item').forEach(fabricItem => {
      const btns = fabricItem.querySelectorAll('.c_btnbox li');
      const imgs = fabricItem.querySelectorAll('.c_bgbox .color_bg');
      btns.forEach((btn, idx) => {
        btn.addEventListener('click', function() {
          btns.forEach(b => b.classList.remove('active'));
          this.classList.add('active');
          imgs.forEach(img => img.classList.remove('on'));
          if (imgs[idx]) imgs[idx].classList.add('on');

          // 색상 선택 시 옵션 텍스트 갱신
          updateOptionText();
        });
      });
    });

    // ==========================
    // 3. 선택 옵션 텍스트 표시
    // ==========================
    let optionDisplay = document.createElement('div');
    optionDisplay.className = 'selected-option';
    const titleEl = document.querySelector('.detail_section .title.txtcenter');
    if (titleEl) titleEl.after(optionDisplay);

    function updateOptionText() {
      const fabric = document.querySelector('.sh_fabric-tab-btn.active')?.innerText || '';
      const color = document.querySelector('.sh_fabric-content-item.active .c_btnbox li.active')?.getAttribute('data-color') || '';
      optionDisplay.textContent = (fabric && color) ? `${fabric} - ${color}` : '';
    }

    // ==========================
    // 4. 초기 세팅
    // ==========================
    // 기본 활성 색상(li.active)이 없는 경우 → 첫 번째를 자동 선택
    document.querySelectorAll('.sh_fabric-content-item').forEach(fabricItem => {
      const btns = fabricItem.querySelectorAll('.c_btnbox li');
      const imgs = fabricItem.querySelectorAll('.c_bgbox .color_bg');
      if (btns.length > 0 && !fabricItem.querySelector('.c_btnbox li.active')) {
        btns[0].classList.add('active');
        if (imgs[0]) imgs[0].classList.add('on');
      }
    });

    // 초기 표시 (첫 번째 기본값)
    updateOptionText();
  });
})();




