/* ============================================================
   SundayHug Blog — Navigation & Interactions
   ============================================================ */

(function () {
  'use strict';

  // ─── Sticky Nav Scroll Effect ───
  const nav = document.getElementById('blogNav');
  if (nav) {
    let lastScroll = 0;
    window.addEventListener('scroll', function () {
      const currentScroll = window.pageYOffset;
      if (currentScroll > 20) {
        nav.classList.add('scrolled');
      } else {
        nav.classList.remove('scrolled');
      }
      lastScroll = currentScroll;
    }, { passive: true });
  }

  // ─── Mobile Menu Toggle ───
  const menuToggle = document.getElementById('menuToggle');
  const mobileDrawer = document.getElementById('mobileDrawer');

  if (menuToggle && mobileDrawer) {
    menuToggle.addEventListener('click', function () {
      const isOpen = mobileDrawer.classList.contains('open');
      if (isOpen) {
        mobileDrawer.classList.remove('open');
        menuToggle.classList.remove('open');
        menuToggle.setAttribute('aria-label', '메뉴 열기');
        document.body.style.overflow = '';
      } else {
        mobileDrawer.classList.add('open');
        menuToggle.classList.add('open');
        menuToggle.setAttribute('aria-label', '메뉴 닫기');
        document.body.style.overflow = 'hidden';
      }
    });

    // Close drawer when a link is clicked
    mobileDrawer.querySelectorAll('.blog-nav-link').forEach(function (link) {
      link.addEventListener('click', function () {
        mobileDrawer.classList.remove('open');
        menuToggle.classList.remove('open');
        document.body.style.overflow = '';
      });
    });
  }

  // ─── Category Filter (Main Page Only) ───
  const filterBar = document.getElementById('filterBar');
  const blogGrid = document.getElementById('blogGrid');

  if (filterBar && blogGrid) {
    const chips = filterBar.querySelectorAll('.blog-filter-chip');
    const cards = blogGrid.querySelectorAll('.blog-card');

    chips.forEach(function (chip) {
      chip.addEventListener('click', function () {
        // Update active chip
        chips.forEach(function (c) { c.classList.remove('active'); });
        chip.classList.add('active');

        var filter = chip.getAttribute('data-filter');

        // Filter cards
        cards.forEach(function (card) {
          var category = card.getAttribute('data-category');
          if (filter === 'all' || category === filter) {
            card.style.display = '';
            // Re-trigger animation
            card.classList.remove('on');
            requestAnimationFrame(function () {
              requestAnimationFrame(function () {
                card.classList.add('on');
              });
            });
          } else {
            card.style.display = 'none';
          }
        });
      });
    });
  }

  // ─── Scroll Reveal Animation ───
  var reveals = document.querySelectorAll('.v');

  if (reveals.length > 0) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('on');
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -40px 0px'
    });

    reveals.forEach(function (el) {
      observer.observe(el);
    });
  }

})();
