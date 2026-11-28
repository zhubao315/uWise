# uWise v3 目标架构

## 1. 目标信息架构（六模块）

| 模块 | 职责 | 对应现有内容 |
|---|---|---|
| Knowledge 知识 | 1891 词条的权威正文与关系 | `docs/vault-encyclopedia/<slug>/index.md`、JSON 索引 |
| Identity 身份 | 四大核心身份的定义与视角 | `docs/core-identity/` |
| Domains 领域 | 16 个专业/3 个跨领域页，作为词条入口 | `specialized-domains/`、`cross-domains/` |
| Skills 技能 | 只做 uSkill 技能的**发现入口** | 绝对链接指向 uSkill，不迁移正文 |
| Projects 项目 | 项目实践与孵化治理 | `projects/`、`incubation/` |
| Learning 学习 | 反思、更新日志、阅读入口 | `REFLECTIONS.md`、`UPDATES.md`、uRead 链接 |

**边界（不做的事）**：不复制 uSkill 的 570 个技能正文（仅在 uWise 展示索引与链接）；不复制 uRead 的笔记与阅读器；不复制 books 站的「核心观点/金句深度解析」与主站的 `/repositories/` 列表；不引入服务端、数据库或运行时 API；不重建站点。

## 2. 渐进迁移（URL 零破坏）

- **永久链接冻结**：`docs/vault-encyclopedia/<slug>/index.md` 与 `/uWise/vault-encyclopedia/<slug>/` 保持原样；slug 算法（`sync_uwise_vault.py:82-87`）不再变更。
- **元数据就地增强**：只向现有页面 frontmatter 追加 `uid / module / visibility / publish / reviewed_at / source_id / updated_at`，不改路径、不改标题。
- **IA 放在导航与索引层**：六模块通过 `mkdocs.yml` 的 nav 分组与 JSON `module` 字段表达，必要时用 `mkdocs-redirects` 或 meta-refresh 存根页承接别名，绝不大批量改目录名。
- **外部绝对链接保持**：12 个页面中 1953 处 `/uWise/vault-encyclopedia/...` 引用继续有效；迁移后由生成器校验链接存活。
- **分阶段**：先影子生成 + dry-run 报告 → 人工抽检 → 增量切换门禁 → 全量生效。

## 3. 静态优先架构

```text
私有 vault (源) ──sync(审阅/过滤)──> docs/vault-encyclopedia/<uid>/index.md
                                  ├──> docs/uwise-encyclopedia-index.json (entries+edges)
                                  └──> docs/generated/uwise-encyclopedia.md (目录)
MkDocs build ──> 静态 site/ ──GitHub Pages──> 浏览器
Knowledge Explorer = 纯前端读取 JSON（无后端）
```

- 生成器产出两类 JSON：`uwise-encyclopedia-index.json`（条目表）与可选 `uwise-graph.json`（关系边）。
- 关系模型：`related / alias_of / part_of / contrast / derived_from / same_topic` 六类有向边，存于 JSON `related` 与 frontmatter；手写页通过 `uid` 引用词条，避免硬编码标题。
- 读路径单向：正文页是权威来源，JSON 是派生物；禁止从 JSON 反向生成正文。

## 4. 边界与协同

- uWise 输出「语义入口 + 关系」，uSkill/uRead/books/主站保留各自域名、路由和内容所有权。
- 跨站链接使用各自的绝对路径并纳入链接巡检；严禁同步他站内容到本仓库。
- 任何 AI 能力只读 `publish=published 且 reviewed_at 非空` 的语料，不写回仓库。
