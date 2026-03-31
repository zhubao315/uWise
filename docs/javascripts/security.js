// uWise 百科 - 安全初始化脚本

(function() {
  'use strict';

  // ========== 域名验证 ==========
  const OFFICIAL_DOMAINS = [
    'zhubao315.github.io',
    'localhost'
  ];

  if (!OFFICIAL_DOMAINS.includes(window.location.hostname)) {
    console.warn('⚠️ 当前不在官方域名，请注意安全');
  }

  // ========== 防止点击劫持 ==========
  if (window.self !== window.top) {
    try {
      window.top.location = window.self.location;
    } catch (e) {
      console.warn('检测到潜在的点击劫持攻击');
    }
  }

  // ========== 内容安全策略检查 ==========
  const checkCSP = function() {
    if (!window.isSecureContext) {
      console.warn('⚠️ 当前上下文不安全，建议使用 HTTPS');
    }
  };
  checkCSP();

  // ========== 防止 XSS 注入 ==========
  const sanitizeInput = function(input) {
    const div = document.createElement('div');
    div.textContent = input;
    return div.innerHTML;
  };

  // 暴露到全局，供其他脚本使用
  window.uwiseSecurity = {
    sanitize: sanitizeInput,
    isOfficialDomain: OFFICIAL_DOMAINS.includes(window.location.hostname)
  };

  console.log('%c🔒 安全模块已加载', 'color: #10b981; font-weight: bold;');
})();
