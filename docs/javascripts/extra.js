// uWise 百科 - JavaScript 交互增强

(function() {
  'use strict';

  // ========== 页面加载进度条 ==========
  document.addEventListener('DOMContentLoaded', function() {
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    document.body.prepend(progressBar);

    let width = 0;
    const interval = setInterval(() => {
      width += Math.random() * 30;
      if (width >= 90) clearInterval(interval);
      progressBar.style.width = width + '%';
    }, 200);

    window.addEventListener('load', () => {
      progressBar.style.width = '100%';
      setTimeout(() => {
        progressBar.style.opacity = '0';
        setTimeout(() => progressBar.remove(), 300);
      }, 500);
    });
  });

  // ========== 图片懒加载 ==========
  document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img[data-src]');

    if ('IntersectionObserver' in window) {
      const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            img.classList.add('loaded');
            observer.unobserve(img);
          }
        });
      }, {
        rootMargin: '50px 0px',
        threshold: 0.01
      });

      images.forEach(img => imageObserver.observe(img));
    } else {
      // 降级处理
      images.forEach(img => {
        img.src = img.dataset.src;
        img.classList.add('loaded');
      });
    }
  });

  // ========== Toast 通知系统 ==========
  window.showToast = function(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = 'toast toast-' + type;
    toast.textContent = message;
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'polite');

    // 不同类型的样式
    const typeColors = {
      info: 'var(--uwise-primary)',
      success: '#10b981',
      warning: '#f59e0b',
      error: '#ef4444'
    };
    toast.style.background = typeColors[type] || typeColors.info;

    document.body.appendChild(toast);

    setTimeout(() => {
      toast.style.animation = 'slideIn 0.3s ease reverse';
      setTimeout(() => toast.remove(), 300);
    }, duration);
  };

  // ========== 返回顶部增强 ==========
  document.addEventListener('DOMContentLoaded', function() {
    const backToTop = document.querySelector('.md-top');
    if (backToTop) {
      backToTop.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
          top: 0,
          behavior: 'smooth'
        });
      });
    }
  });

  // ========== 搜索防抖 ==========
  function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
      const later = () => {
        clearTimeout(timeout);
        func(...args);
      };
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
    };
  }

  // ========== 搜索增强 ==========
  document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.md-search__input');
    if (searchInput) {
      const debouncedSearch = debounce(function(e) {
        // 搜索逻辑可以在这里扩展
        console.log('搜索:', e.target.value);
      }, 300);

      searchInput.addEventListener('input', debouncedSearch);
    }
  });

  // ========== 复制按钮增强 ==========
  document.addEventListener('DOMContentLoaded', function() {
    const copyButtons = document.querySelectorAll('.md-clipboard');
    copyButtons.forEach(btn => {
      btn.addEventListener('click', function() {
        window.showToast('已复制到剪贴板', 'success', 2000);
      });
    });
  });

  // ========== 代码块行号点击 ==========
  document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.linenos').forEach(lineno => {
      lineno.addEventListener('click', function(e) {
        if (e.target.classList.contains('linenos')) {
          const line = window.getSelection().toString();
          if (line) {
            navigator.clipboard.writeText(line);
            window.showToast('已复制行内容', 'success', 2000);
          }
        }
      });
    });
  });

  // ========== 平滑滚动到锚点 ==========
  document.addEventListener('click', function(e) {
    if (e.target.closest('a[href^="#"]')) {
      const link = e.target.closest('a[href^="#"]');
      const targetId = link.getAttribute('href');

      if (targetId && targetId !== '#') {
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
          e.preventDefault();
          const headerOffset = 64;
          const elementPosition = targetElement.getBoundingClientRect().top;
          const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

          window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
          });
        }
      }
    }
  });

  // ========== 外部链接新标签页打开 ==========
  document.addEventListener('DOMContentLoaded', function() {
    const links = document.querySelectorAll('a[href^="http"]');
    links.forEach(link => {
      const href = link.getAttribute('href');
      if (href && !href.includes(window.location.hostname)) {
        link.setAttribute('target', '_blank');
        link.setAttribute('rel', 'noopener noreferrer');
        if (!link.querySelector('[aria-label]')) {
          const icon = document.createElement('span');
          icon.innerHTML = '&nbsp;↗';
          icon.setAttribute('aria-label', '在新标签页打开');
          link.appendChild(icon);
        }
      }
    });
  });

  // ========== 键盘快捷键 ==========
  document.addEventListener('keydown', function(e) {
    // Alt + S: 聚焦搜索框
    if (e.altKey && e.key === 's') {
      e.preventDefault();
      const searchInput = document.querySelector('.md-search__input');
      if (searchInput) {
        searchInput.focus();
      }
    }

    // Alt + T: 返回顶部
    if (e.altKey && e.key === 't') {
      e.preventDefault();
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  });

  // ========== 阅读进度指示器 ==========
  document.addEventListener('DOMContentLoaded', function() {
    window.addEventListener('scroll', debounce(function() {
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      const scrollHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = (scrollTop / scrollHeight) * 100;

      // 可以在这里添加阅读进度指示器逻辑
    }, 100));
  });

  // ========== 性能监控 ==========
  if ('performance' in window) {
    window.addEventListener('load', function() {
      setTimeout(() => {
        const perfData = performance.getEntriesByType('navigation')[0];
        if (perfData) {
          console.log('页面加载时间:', {
            DNS查询: perfData.domainLookupEnd - perfData.domainLookupStart,
            TCP连接: perfData.connectEnd - perfData.connectStart,
            请求响应: perfData.responseEnd - perfData.requestStart,
            DOM解析: perfData.domContentLoadedEventEnd - perfData.domContentLoadedEventStart,
            完全加载: perfData.loadEventEnd - perfData.loadEventStart
          });
        }
      }, 0);
    });
  }

  // ========== Service Worker 注册 (PWA支持) ==========
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js').then(registration => {
        console.log('Service Worker 注册成功:', registration.scope);
      }).catch(error => {
        console.log('Service Worker 注册失败:', error);
      });
    });
  }

  // ========== 离线提示 ==========
  window.addEventListener('offline', function() {
    window.showToast('您已离线，部分功能可能不可用', 'warning', 5000);
  });

  window.addEventListener('online', function() {
    window.showToast('网络已恢复', 'success', 2000);
  });

  console.log('%c🦞 uWise 百科', 'font-size: 24px; font-weight: bold; color: #6366f1;');
  console.log('%c交互增强已加载', 'color: #818cf8;');
})();
