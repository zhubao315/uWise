# 🦞 uWise 百科

> **AI驱动的领域知识百科** | 持续进化，与时俱进

[![GitHub](https://img.shields.io/badge/GitHub-zhubao315/uWise-181717?logo=github)](https://github.com/zhubao315/uWise)
[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-uWise 百科-007ACC?logo=github)](https://zhubao315.github.io/uWise/)

## 🎯 项目简介

**uWise 百科**是一个基于四大核心身份的持续进化知识体系，采用领域驱动框架（Area → Project → Task），将知识转化为实际行动。

> 成果源于**挖掘机会**，而非解决问题。——德鲁克《成果管理》(1964)

## 🌟 四大核心身份

### 🏗️ 架构师
负责设计和规划复杂系统的架构
- 人工智能专家、云计算与云原生、知识产权顾问、全栈工程师、产品经理

### 💰 投资人
善于分析市场、管理风险，实现财富增值
- 金融市场、量化投资、技术投资

### 📖 终身学习者
秉持终身学习的理念，不断追求知识提升
- 国学大师、北京文化使者、心理学专家

### 🎨 生活艺术家
从生活中发现和创造美好
- 数字人生、户外大神、健身跑者、葡萄酒大师、摄影家、游戏王者

## 🚀 技术栈

- **Wiki系统**：[MkDocs](https://www.mkdocs.org/) + [Material主题](https://squidfunk.github.io/mkdocs-material/)
- **部署平台**：[GitHub Pages](https://pages.github.com/)
- **自动更新**：GitHub Actions（每日自动抓取更新知识）
- **内容格式**：Markdown

## 📂 项目结构

```
uWise/
├── docs/                    # 文档目录
│   ├── core-identity/       # 核心身份
│   ├── specialized-domains/ # 专业领域
│   ├── cross-domains/       # 跨领域创新
│   ├── projects/            # 项目实践
│   └── incubation/          # 实践项目孵化小组
├── scripts/                 # 自动化脚本
├── mkdocs.yml              # MkDocs配置
└── .github/workflows/      # GitHub Actions
```

## 🛠️ 本地开发

### 环境准备
```bash
# 克隆项目
git clone https://github.com/zhubao315/uWise.git
cd uWise

# 安装依赖
pip install -r requirements.txt

# 启动本地服务器
mkdocs serve
```

访问 http://127.0.0.1:8000 查看本地文档。

### 构建部署
```bash
# 构建静态文件
mkdocs build

# 部署到GitHub Pages
mkdocs gh-deploy
```

## 🔄 自动更新

本项目配置了GitHub Actions，每天自动：
1. 抓取领域相关最新资讯
2. AI生成知识摘要
3. 更新文档内容
4. 部署到GitHub Pages

### 配置Secrets

在GitHub仓库Settings → Secrets中添加：
- `OPENAI_API_KEY`：OpenAI API密钥（用于AI摘要）
- `TAVILY_API_KEY`：Tavily搜索API密钥（用于资讯抓取）

## 📊 领域驱动框架

```
Area (领域) → Project (项目) → Task (任务)
```

| 身份 | Area（领域） | Project（项目） | Task（任务） |
|------|-------------|----------------|-------------|
| 架构师 | AI原生系统 | LLM应用平台 | 设计RAG架构 |
| 投资人 | 投资组合管理 | 量化策略开发 | 构建回测系统 |
| 终身学习者 | 传统文化现代化 | 国学智慧应用 | 研读《论语》 |
| 生活艺术家 | 生活品质提升 | 葡萄酒探索 | 学习品鉴技巧 |

## 📈 职业迭代路径

| 时期 | 角色 | 领域 |
|------|------|------|
| 1999-2006 | 飞机工程 | 航空电气→航材计划→计算机服务 |
| 2007-2010 | 软件交付 | MicroMuse - IBM实验室服务 |
| 2011-2015 | 运维管理 | 统一监控 - ISM中体彩 |
| 2016-2019 | 项目管理 | 数据中心 - PMO中体彩 |
| 2020-2023 | 系统架构师 | 税总党建系统架构 |
| 2024-今 | 人工智能专家 | AIGC、LLM、AI创新 |

## 🤝 参与贡献

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

- **GitHub**: [@zhubao315](https://github.com/zhubao315)
- **项目地址**: [https://github.com/zhubao315/uWise](https://github.com/zhubao315/uWise)
- **在线文档**: [https://zhubao315.github.io/uWise/](https://zhubao315.github.io/uWise/)

---

<div align="center">

**🌐 访问 uWise 百科** → [https://zhubao315.github.io/uWise/](https://zhubao315.github.io/uWise/)

*持续进化，与时俱进* 🦞

</div>
