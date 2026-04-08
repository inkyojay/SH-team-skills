/* SundayHug Pages — Shared Navigation JS */
(function() {
  'use strict';

  /* ─── Menu Toggle ─── */
  const toggle = document.querySelector('.menu-toggle');
  const nav = document.querySelector('.nav');
  const overlay = document.querySelector('.overlay');

  if (toggle && nav && overlay) {
    toggle.addEventListener('click', function() {
      nav.classList.toggle('open');
      overlay.classList.toggle('active');
    });

    overlay.addEventListener('click', function() {
      nav.classList.remove('open');
      overlay.classList.remove('active');
    });
  }

  /* ─── Active Link ─── */
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.nav a').forEach(function(link) {
    const href = link.getAttribute('href');
    if (href && href === currentPage) {
      link.classList.add('active');
    }
  });

  /* ─── Scroll Animations ─── */
  const observer = new IntersectionObserver(function(entries) {
    entries.forEach(function(entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('on');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  document.querySelectorAll('.v').forEach(function(el) {
    observer.observe(el);
  });
})();
