/**
 * Mosaic AI — Core Client-side Interactions & Motion System
 * Spec: .webby/DESIGN-SPEC-mosaic.md & .webby/NGUYEN-LIEU-AP-DUNG.md
 * Tuân thủ 14 thẻ nguyên liệu, vanilla JS, không framework nặng, hỗ trợ prefers-reduced-motion.
 */

(function () {
  'use strict';

  // --------------------------------------------------------------------------
  // 1. THEME SWITCH & PERSISTENCE (component|tactile-bicolor-toggle-switch)
  // --------------------------------------------------------------------------
  const THEME_KEY = 'mosaic-theme';

  function isReducedMotion() {
    return window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  }

  function getStoredTheme() {
    try {
      return localStorage.getItem(THEME_KEY);
    } catch (e) {
      return null;
    }
  }

  function getSystemTheme() {
    return window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }

  function applyTheme(theme) {
    const root = document.documentElement;
    root.setAttribute('data-bs-theme', theme);
    try {
      localStorage.setItem(THEME_KEY, theme);
    } catch (e) {
      // Ignore storage errors in restricted contexts
    }

    // Sync all toggle switch UI elements on the page
    document.querySelectorAll('.mz-theme-toggle').forEach(function (btn) {
      btn.setAttribute('data-theme', theme);
      btn.setAttribute('aria-checked', theme === 'dark' ? 'true' : 'false');
      btn.setAttribute('title', theme === 'dark' ? 'Chuyển sang chế độ sáng' : 'Chuyển sang chế độ tối');
    });

    // Dispatch custom event for widgets/charts
    window.dispatchEvent(new CustomEvent('mosaic-theme-change', { detail: { theme: theme } }));
  }

  function toggleTheme() {
    const current = document.documentElement.getAttribute('data-bs-theme') || 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    applyTheme(next);
  }

  window.MosaicTheme = {
    get: function () {
      return document.documentElement.getAttribute('data-bs-theme') || 'light';
    },
    set: applyTheme,
    toggle: toggleTheme,
  };

  // --------------------------------------------------------------------------
  // 2. SHARED LAYOUT TAB INDICATOR (component|shared-layout-tab-indicator)
  // --------------------------------------------------------------------------
  function initTabIndicators() {
    const tabLists = document.querySelectorAll('.mz-tab-list, [data-mz-tabs]');
    tabLists.forEach(function (list) {
      let indicator = list.querySelector('.mz-tab-indicator');
      if (!indicator) {
        indicator = document.createElement('div');
        indicator.className = 'mz-tab-indicator';
        list.appendChild(indicator);
      }

      function updateIndicator(targetTab) {
        if (!targetTab) return;
        const listRect = list.getBoundingClientRect();
        const tabRect = targetTab.getBoundingClientRect();
        const left = tabRect.left - listRect.left + list.scrollLeft;
        const width = tabRect.width;

        indicator.style.transform = `translateX(${left}px)`;
        indicator.style.width = `${width}px`;
      }

      const activeTab = list.querySelector('.mz-tab-item.active') || list.querySelector('.mz-tab-item');
      if (activeTab) {
        activeTab.classList.add('active');
        updateIndicator(activeTab);
      }

      list.addEventListener('click', function (e) {
        const tab = e.target.closest('.mz-tab-item');
        if (!tab || !list.contains(tab)) return;

        list.querySelectorAll('.mz-tab-item').forEach(function (t) {
          t.classList.remove('active');
        });
        tab.classList.add('active');
        updateIndicator(tab);
      });

      // Recalculate on window resize
      window.addEventListener('resize', function () {
        const currentActive = list.querySelector('.mz-tab-item.active');
        if (currentActive) updateIndicator(currentActive);
      });
    });
  }

  // --------------------------------------------------------------------------
  // 3. CUBIC DRAWER SLIDE TRANSITION (motion|cubic-drawer-slide-transition)
  // --------------------------------------------------------------------------
  function initDrawer() {
    const toggleBtns = document.querySelectorAll('[data-mz-toggle="sidebar"], [data-mz-toggle="drawer"]');
    let backdrop = document.querySelector('.mz-drawer-backdrop');

    if (!backdrop) {
      backdrop = document.createElement('div');
      backdrop.className = 'mz-drawer-backdrop';
      document.body.appendChild(backdrop);
    }

    let lastFocusedElement = null;

    function openSidebar() {
      const sidebar = document.querySelector('.mz-sidebar');
      if (!sidebar) return;
      lastFocusedElement = document.activeElement;
      sidebar.classList.add('show');
      backdrop.classList.add('show');
      document.body.style.overflow = 'hidden';
      const firstLink = sidebar.querySelector('a, button');
      if (firstLink) firstLink.focus();
    }

    function closeSidebar() {
      const sidebar = document.querySelector('.mz-sidebar');
      if (!sidebar) return;
      sidebar.classList.remove('show');
      backdrop.classList.remove('show');
      document.body.style.overflow = '';
      if (lastFocusedElement) {
        lastFocusedElement.focus();
        lastFocusedElement = null;
      }
    }

    toggleBtns.forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        const sidebar = document.querySelector('.mz-sidebar');
        if (sidebar && sidebar.classList.contains('show')) {
          closeSidebar();
        } else {
          openSidebar();
        }
      });
    });

    backdrop.addEventListener('click', closeSidebar);

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') {
        const sidebar = document.querySelector('.mz-sidebar');
        if (sidebar && sidebar.classList.contains('show')) {
          closeSidebar();
        }
      }
    });

    // Close on mobile navigation item click
    document.querySelectorAll('.mz-sidebar .mz-nav-item').forEach(function (item) {
      item.addEventListener('click', function () {
        if (window.innerWidth < 768) {
          closeSidebar();
        }
      });
    });
  }

  // --------------------------------------------------------------------------
  // 4. WAAPI PROGRAMMATIC REVEAL (motion|waapi-programmatic-reveal-hook)
  // --------------------------------------------------------------------------
  function revealElement(element, options) {
    if (!element) return;
    options = options || {};
    const duration = options.duration || 240;
    const delay = options.delay || 0;

    if (isReducedMotion() || typeof element.animate !== 'function') {
      element.style.opacity = '1';
      element.style.transform = 'none';
      return;
    }

    element.animate(
      [
        { opacity: 0, transform: 'translateY(8px)' },
        { opacity: 1, transform: 'translateY(0)' },
      ],
      {
        duration: duration,
        delay: delay,
        easing: 'cubic-bezier(0.16, 1, 0.3, 1)',
        fill: 'forwards',
      }
    );
  }

  window.MosaicReveal = revealElement;

  function initReveals() {
    const revealTargets = document.querySelectorAll('[data-mz-reveal]');
    revealTargets.forEach(function (el, idx) {
      const delay = Math.min(idx * 35, 140);
      revealElement(el, { delay: delay });
    });
  }

  // --------------------------------------------------------------------------
  // 5. SCORE BLOCK M1-M5 ANIMATION
  // --------------------------------------------------------------------------
  function initScoreBars() {
    const bars = document.querySelectorAll('.mz-model-bar-fill[data-score]');
    bars.forEach(function (bar, idx) {
      const targetScore = parseFloat(bar.getAttribute('data-score')) || 0;
      const targetWidth = Math.min(Math.max(targetScore, 0), 100) + '%';

      if (isReducedMotion()) {
        bar.style.width = targetWidth;
      } else {
        setTimeout(function () {
          bar.style.width = targetWidth;
        }, idx * 35);
      }
    });
  }

  // --------------------------------------------------------------------------
  // 6. CONFIRM MODAL REJECT REASON VALIDATION (Quyết định nghiệp vụ bắt buộc)
  // --------------------------------------------------------------------------
  function initRejectModalValidation() {
    const reasonTextareas = document.querySelectorAll('textarea[name="reason"][data-mz-reject-reason]');
    reasonTextareas.forEach(function (textarea) {
      const form = textarea.closest('form');
      if (!form) return;
      const submitBtn = form.querySelector('[type="submit"]');
      const errorMsg = form.querySelector('.mz-form-error');

      function validate() {
        const val = textarea.value.trim();
        const isValid = val.length >= 5;
        if (submitBtn) {
          submitBtn.disabled = !isValid;
        }
        if (errorMsg) {
          if (val.length > 0 && !isValid) {
            errorMsg.style.display = 'block';
            errorMsg.textContent = 'Lý do từ chối phải có tối thiểu 5 ký tự.';
          } else {
            errorMsg.style.display = 'none';
          }
        }
      }

      textarea.addEventListener('input', validate);
      validate(); // Initial state check
    });
  }

  // --------------------------------------------------------------------------
  // 7. TOAST AUTO-DISMISS
  // --------------------------------------------------------------------------
  function initToasts() {
    const toasts = document.querySelectorAll('.mz-toast');
    toasts.forEach(function (toast) {
      const dismissBtn = toast.querySelector('[data-mz-dismiss="toast"]');
      function close() {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-8px)';
        toast.style.transition = 'opacity 160ms var(--ease-standard), transform 160ms var(--ease-standard)';
        setTimeout(function () {
          if (toast.parentNode) toast.parentNode.removeChild(toast);
        }, 160);
      }

      if (dismissBtn) {
        dismissBtn.addEventListener('click', close);
      }

      // Auto dismiss after 4.5 seconds
      setTimeout(close, 4500);
    });
  }

  // --------------------------------------------------------------------------
  // 8. INITIALIZATION ON DOM READY
  // --------------------------------------------------------------------------
  document.addEventListener('DOMContentLoaded', function () {
    // Theme toggle button click listeners
    document.querySelectorAll('.mz-theme-toggle').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        toggleTheme();
      });
    });

    // Listen to system theme changes if not overridden
    if (window.matchMedia) {
      window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', function (e) {
        if (!getStoredTheme()) {
          applyTheme(e.matches ? 'dark' : 'light');
        }
      });
    }

    initDrawer();
    initTabIndicators();
    initReveals();
    initScoreBars();
    initRejectModalValidation();
    initToasts();
  });
})();
