# uWise 深度审计报告（v3 前置）

## 1. 范围与方法

- 对象：`zhubao315/uWise` 工作副本 `/tmp/opencode/uwise-fix`（只读），源私库导出 `/tmp/opencode/uwise-vault`。
- 方法：纯静态审计——读取 Markdown/YAML/JS/CSS/Python、git 状态、对 JSON 与目录做精确计数；引用均给出 `文件:行号` 或精确计数。
- **未做**：Lighthouse、真实浏览器运行、线上抓包、性能/可访问性实测、任何文件修改或远端操作。以下「事实」可复核，「判断」为架构推论。

## 2. 总体成熟度：约 5.8/10（加权）

| 维度 | 分 | 权重 | 依据 |
|---|---|---|---|
| 内容资产与规模 | 8.5 | 0.15 | 1891 词条、1891 发布页 |
| 信息架构与导航 | 6.5 | 0.10 | mkdocs.yml:95-137 结构清晰但扁平 |
| 发布治理与隐私 | 2.5 | 0.15 | 全量发布、无审核门禁（P0） |
| 链接/元数据质量 | 3.5 | 0.10 | 3715 断链、226 未标注、22 空分类 |
| 前端/PWA/可访问性 | 3.0 | 0.10 | 双 fetch 监听、根路径注册、undefined CSS 变量 |
| CI/CD 与交付 | 5.0 | 0.10 | deploy 非 strict 且不依赖 test |
| 工程规范与测试 | 8.5 | 0.20 | black/flake8/mypy/pytest 全绿 |
| 生态协同与边界 | 6.0 | 0.10 | 与 uSkill/uRead 互通但边界未文档化 |
| **加权合计** | **5.75 ≈ 5.8** | 1.00 | — |

## 3. 证据表（事实）

| 项 | 证据 |
|---|---|
| 词条规模 | JSON `count=1891`，键 `source,count,skills`；发布页 `docs/vault-encyclopedia/*/index.md` 共 1891 |
| 断链 | 1421 条 `broken_links>0`，合计 3715 个未解析 wikilink |
| 元数据 | `未标注`226、`draft`172、`published`8、`active`2、`Active`1、`成熟`1、`已确立`1481；空 category 22 |
| 重复标题 | 4 组：痛楚与磨难解耦 / 键盘政治 / 火鸡问题 / 苦难不是意义的障碍，而是意义的来源 |
| 跨域引用 | 12 个非词条文件含绝对链接（11 个手写页 + 生成目录）；`specialized-domains/` 下 56 处 `/uWise/vault-encyclopedia/` |
| 同步脚本 | 手写 frontmatter 解析 `sync_uwise_vault.py:90-114`；固定字符串脱敏 `:117-124`；未解析链接退化为纯文本 `:164-180`；全量 `rmtree` 重建 `:182`；公开页写入来源/私库路径 `:204-215`；JSON `skills` `:231-243`；无 dry-run/增量/回滚 |
| 工作流 | `sync-uwise-vault.yml:6` 每周一 03:47 UTC；`:46` 用 `mkdocs build --strict`；`:54-61` 仅提交目标目录；`VAULT_SYNC_PAT` 见 `:26,:40,:50`；`daily-update.yml:5` 每日 cron（业主确认已 disabled_manually） |
| 部署门禁 | `deploy.yml:35` `mkdocs build`（无 --strict），`:47` 仅 `needs: build`，不依赖 `test.yml:30-40` |
| 前端 | `sw.js:41` 与 `:74` 两个 `fetch` 监听均 `respondWith`；缓存路径 `/` `:5-10`；注册 `/sw.js` `extra.js:238`；manifest `start_url/scope=/` `:5,:10`，图标 `:11-51` 但 `docs/assets/` 不存在；`custom.css` 6 处未定义 `--uwise-radius`（`:106,128,161,228,247,377`）；`extra.js` 8 处 `DOMContentLoaded`、0 处 `document$.subscribe`，与 `mkdocs.yml:26` 的 `navigation.instant` 冲突；`security.js:25-31` 仅检查 `isSecureContext`，无真实 CSP |
| 分析 | `overrides/main.html:6-13` 注入站点配置；`zhubao-analytics.js` 为共享 SDK（公开写令牌，不在本文复述） |

## 4. 优势（事实 + 判断）

- **事实**：slug 由规范名 + SHA1 派生（`sync_uwise_vault.py:82-87`），URL 稳定；脚本声明不编造内容、不执行私库脚本（`:11`）；Python 四检全绿（10 passed）。
- **判断**：内容体量与确定性生成是 v3 的最大资产；每周同步已具备 strict 校验和条件提交，是治理改造的良好底座。

## 5. 优先问题清单

1. **P0（事实）**：全量发布且无 visibility/publish/reviewed_at 门禁，私库路径写入 1891 个公开页；**（判断）**最高隐私与合规风险。
2. **P1（事实）**：3715 未解析 wikilink 退化为纯文本，关系网络断裂；4 组重复标题削弱引用唯一性。
3. **P1（事实）**：226 未标注、22 空分类、状态值混杂（含 `Active`/`active` 大小写）；无单一分类法来源。
4. **P1（判断）**：JSON 字段 `skills` 误导（实为通用词条），阻碍统一数据模型。
5. **P2（事实）**：PWA 声明与实际资源/作用域不匹配，SPA 下 JS 生命周期失效。
6. **P2（事实/判断）**：部署不经测试门禁且非 strict，SEO/GEO 结构化缺失，双同步工作流存在覆盖风险。
