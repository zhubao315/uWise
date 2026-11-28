# uWise v3 统一数据模型

## 1. 条目 Schema（每条/每页一致）

| 字段 | 类型 | 规则 |
|---|---|---|
| `uid` | string | 稳定 ID：`uw-` + 规范 `source_id` 的 SHA1 前 12 位，与标题无关 |
| `title` | string | 显示标题；允许重复但需 `uid` 区分 |
| `aliases` | string[] | 别名，含中文/英文；用于 wikilink 解析与搜索 |
| `type` | enum | `concept / method / person / book / case / question / meta` |
| `domain` | string[] | 引用 taxonomy 的 domain ID，不写自由文本 |
| `identity` | string[] | 四大身份 ID（可选） |
| `project` | string[] | 项目 ID（可选） |
| `tags` | string[] | 引用 taxonomy 的 tag ID |
| `status` | enum | 统一为 `draft / reviewing / reviewed / published / archived`（原 7 种值映射） |
| `visibility` | enum | `private / internal / public` |
| `publish` | bool | 是否允许进入公开构建产物 |
| `reviewed_at` | ISO date 或 null | 人工审核日期；为空即未审核 |
| `source_id` | string | 私库相对路径 + blob SHA（不对外暴露完整私库路径） |
| `updated_at` | ISO datetime | 内容变更时间 |
| `related` | object[] | `{uid, rel}`，rel 见架构文档六类边 |

## 2. 发布状态机

```text
draft ──提交──> reviewing ──审核通过──> reviewed ──发布──> published
  ↑                │                      │                   │
  └──── 退回 ───────┘               撤回 ←──┘            归档 → archived
private / deny（覆盖态，优先级高于以上全部）：不进入公开构建
```

- 默认：新建条目 = `draft / private / publish=false`；**存量 1891 条在审核完成前维持现状**（见 Roadmap 警告）。
- `publish=true` 的必要条件：`visibility=public` 且 `reviewed_at` 非空且 `status ∈ {reviewed,published}`；生成器强制校验。
- `deny` 为显式拒绝名单（整条或敏感片段），优先级最高且不可被同步覆盖。

## 3. 稳定 ID 与 URL 规则

- `uid` 一经生成永不改变；标题、分类、状态变化均不影响 `uid`。
- URL 仍为 `/uWise/vault-encyclopedia/<slug>/`，`slug` 沿用现有算法（`:82-87`）；slug 变更必须生成 301/存根重定向。
- `source_id` 与私库路径仅留在私有元数据/报告，公开页的「来源与口径」改为脱敏后的 `source_id` 摘要，不复述完整路径（`sync_uwise_vault.py:211` 现状需改）。

## 4. 分类法单一来源

- 新增 `docs/taxonomy/domain.yml / identity.yml / tag.yml`，编译为 `docs/taxonomy.json`。
- frontmatter 只写 ID，由构建校验「未登记 ID 即报错」；空 category（22 条）与大小写混用（`active`/`Active`）在此收敛。

## 5. JSON 索引改造

现状键：`source, count, skills`。目标：

```json
{ "schema_version": "3.0", "source": "<脱敏>", "generated_at": "...",
  "count": 1891, "entries": [ { /* 第 1 节字段 */ } ],
  "edges": [ {"from":"uw-…","to":"uw-…","rel":"related"} ],
  "by_module": {}, "by_status": {} }
```

- `skills` → `entries`（读取方同步改名，保留一次性兼容别名）。
- 断链统计从 `broken_links` 整数升级为 `unresolved: [{target, line}]`，供 Explorer 与报告使用。
