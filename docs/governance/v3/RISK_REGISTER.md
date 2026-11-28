# uWise v3 风险登记表

| 风险 | 严重度 | 可能性 | 证据（事实） | 缓解 | 需业主决策 |
|---|---|---|---|---|---|
| 私域内容公开暴露 | 高 | 高 | 1891 公开页均写入 `私库路径`；`sync_uwise_vault.py:117-124` 仅固定字符串脱敏；`:204-215` 写来源 | T1 门禁 + source_id 脱敏 + deny 名单 + dry-run 报告；先影子构建后生效 | 存量 1891 条是「维持公开」还是「分批下架复审」？ |
| 关系网络断裂/断链 | 中高 | 高 | 1421 条 broken_links>0，共 3715 个未解析 wikilink，`:164-180` 退化为纯文本 | T2 显式 unresolved 清单、别名表、反向链接、链接巡检；保留旧 URL | 无目标链接是补目标、标灰还是保留纯文本？ |
| 分类法混乱 | 中 | 高 | 226 未标注、22 空分类、`active`/`Active` 混用、4 组重复标题 | T3 taxonomy 单一来源 + 构建校验 + 状态映射 | 4 组重复标题的合并/并存策略？ |
| PWA 虚假能力 | 中 | 高 | `sw.js:41,74` 双 fetch 监听；缓存/注册根路径 `:5-10`、`extra.js:238`；manifest 根 scope 与图标缺失 `:5,10,11-51`（无 `docs/assets/`） | T5 单一监听、路径对齐 `/uWise/`、补图标或移除 PWA 声明；不宣称离线能力直到验证 | 保留 PWA 还是降级为普通站点？ |
| 部署无测试门禁 | 中高 | 中 | `deploy.yml:35` 非 strict、`:47` 仅 `needs: build`，不依赖 `test.yml` | T6 让 deploy 依赖 test、启用 `--strict`；同步工作流已有 strict 可复用 | 是否接受「测试失败阻断线上部署」？ |
| SEO/GEO 缺口 | 中 | 中 | 12 个页面使用绝对路径 `/uWise/...`；未发现 canonical/sitemap/结构化数据产物 | T6 生成 canonical/sitemap/robots/OG 与结构化数据，纳入链接巡检 | 是否引入站点地图与结构化数据到公开构建？ |
| 双同步工作流冲突 | 高 | 中 | `sync-uwise-vault.yml:6,54-61` 提交 main 触发 deploy；`daily-update.yml:5` 每日 cron、`:46` `git add -A`/push、`:51` `mkdocs gh-deploy --force`（业主称已 disabled） | 永久归档/删除 daily-update.yml，或统一为单一生成器 + 单一部署路径；禁止 `gh-deploy --force` 覆盖产物 | 是否正式停用 daily-update.yml 并统一同步入口？ |
| 前端 JS 在 SPA 下失效 | 中 | 高 | `mkdocs.yml:26` 启用 `navigation.instant`；`extra.js` 8 处 DOMContentLoaded、0 处 `document$.subscribe()`；`custom.css` 6 处未定义 `--uwise-radius` | T5 改造生命周期与 CSS 变量；用真实浏览器回归验证（本审计未实测） | 是否接受对交互做一次完整浏览器回归？ |

注：本表基于静态审计；Lighthouse/浏览器实测未执行，涉及行为的影响判断为推论而非测量结论。
