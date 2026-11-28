# uWise v3 路线图（7 条轨道）

> **P0 前置警告（事实+判断）**：现有 1891 条全部公开，其中仅 8 条 `published`、172 条 `draft`、226 条 `未标注`。若立即按 `publish/reviewed_at` 门禁构建，**绝大多数条目会一次性下架**。因此必须先 dry-run、影子构建与抽检，**禁止一次性下架**。

| # | 阶段/轨道 | 具体交付 | 验收标准 | 依赖 |
|---|---|---|---|---|
| T1 | **P0 发布治理** | 条目 Schema 落地；`visibility/publish/reviewed_at/deny`；生成器门禁；dry-run/报告/回滚；脱敏 `source_id` | dry-run 报告列出将受影响条目；存量不被自动移除；公开页不再出现完整私库路径；`publish=true` 必满足审核条件 | 无（先做） |
| T2 | **P1 链接治理** | 未解析 wikilink 升级为显式 `unresolved` 清单；别名表与 4 组重复标题处置；反向链接；链接巡检脚本 | 3715 断链 100% 可列举与定位；重复标题有唯一 uid；12 个页面的绝对链接零 404 | T1 |
| T3 | **P1 元数据治理** | 226 未标注、22 空分类、状态归一化；taxonomy 单一来源与编译校验 | 状态取值只含 5 种；空 category=0；未登记 ID 构建失败 | T1 |
| T4 | **P1 Knowledge Explorer + 首页** | 前端读取 `entries/edges` 的筛选、搜索、关系视图；首页六模块入口 | URL 零变更；断网/无 JS 时目录页仍可用；不新增后端 | T1、T3 |
| T5 | **P2 视觉/PWA/JS 生命周期** | 定义或替换 `--uwise-radius`（6 处）；`document$.subscribe()` 替代 8 处 DOMContentLoaded；SW 单一 fetch 监听；注册路径与 scope 对齐 `/uWise/`；补齐或移除图标/截图声明 | 无重复 respondWith；SPA 切换后交互仍生效；PWA 声明与真实资源一致 | T4 |
| T6 | **P2 CI/SEO/GEO** | `deploy.yml` 依赖测试并启用 `--strict`；canonical/sitemap/robots/OG/结构化数据；统一分析 SPA 事件 | 测试失败阻断部署；断链/损坏引用导致构建失败；结构化数据校验通过 | T1、T2 |
| T7 | **P3 AI 能力** | 仅基于 `published+reviewed` 语料的检索/问答/摘要；人工确认后写入；禁自动发布 | 零自动写回仓库；可溯源到 uid；拒绝私库/未审内容 | T1、T3、T6 |

**顺序**：T1（含 dry-run）→ T2/T3 并行 → T4 → T5/T6 并行 → T7。双同步工作流的取舍（daily-update.yml 归档或对齐）需在 T6 前由业主决策。
