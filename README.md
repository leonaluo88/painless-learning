# 无痛学习网页 · painless-learning

**中文** | [English](README.en.md)

一个 AI Agent Skill：把课件、教材、lecture 转写稿、样卷，甚至只是“我想学 X”，做成**一门课一个**的交互式学习网页。

这个仓库包含三个 skill 包，内容相同，只是按各 agent 的环境做了适配：

| 包 | 用于 | 网页交付方式 |
|---|---|---|
| `claude/painless-learning-web/` | Claude（claude.ai 网页版 / 桌面端） | 发布为 artifact（带链接的托管网页），课件页截图随网页上传 |
| `codex/painless-learning-web/` | OpenAI Codex | 能用 Sites 插件时发布为托管网页，之后一直在同一个 site 上更新；否则写到课程文件夹的 `_学习网页/index.html`。附 `agents/openai.yaml` 界面信息 |
| `workbuddy/painless-learning-web/` | 腾讯 WorkBuddy | 写到课程文件夹的 `_学习网页/index.html`，浏览器直接打开 |

Claude Code、Gemini CLI、GitHub Copilot 等其他支持 [Agent Skills 标准](https://agentskills.io/specification)的工具，可以用 Codex 包或 WorkBuddy 包。

## 它能做什么

- **细粒度知识点 + 前置依赖拓扑**：每个知识点只讲一件事。拓扑图从考题或学习目标出发，往回找前置、前置的前置，跨模块连线；知识点编号按“即时前置”顺序排。图可以点击，点一个知识点会亮出它的全部前置和后续；“按考题看”会亮出做某道题需要的全部知识点。
- **一步讲解的固定写法**：每一步都按 为什么现在学 → 直觉 → 定义或公式 → 人话 → 例题 → 常见卡点 → 自测 → 考题出处 的顺序写。公式用真正的 LaTeX，推导链对齐，并写出每一步的依据。
- **逻辑主线**：每课最后用一条因果链（问题 → 思路 → 做法 → 结果 → 新问题）把细节串起来；每一步都标出它在主线上的位置。
- **验证真的掌握了**：每个知识点都有可以检验的掌握标准；题目按 认得 / 会解释 / 会用 / 能迁移 四级出题；配错误答案库和两级提示。全站只有一种题卡，“已掌握”只由你自己勾，“未掌握”筛选就是错题本。
- **上手成本低，操作都能撤销**：每个板块有一行使用说明；勾选、作答、清零、移除、导入都能撤销；可以一键重置，重置前会自动备份。
- **每周增量更新**：知识点用稳定 ID，更新后进度不会丢。后补前置、老师更正、新旧材料矛盾、循环依赖都有固定的处理规则。
- **备考模式**：从样卷反推需要的知识点，按题目的问法定每个知识点学到多深。扎实版先刷仿真题，真题封存到最后再做。考试允许带笔记时，有 Cheat Sheet 暂存功能，可以据此生成笔记纸。
- **从零规划 / 轻量入门**：没有材料时，先调研权威课程，规划路线再做网页；只想弄懂一个概念（少于 3 小时）时，不提问，直接生成精简网页。
- **自我改进**：你提出修改意见后，AI 先改网页，再判断这个问题是只属于这门课、属于某一类学科，还是所有学科都有。后两种情况会提出规则修改建议，你确认后写进 skill，并记在文末的“规则迭代记录”里。

### 六种规格

| 规格 | 什么时候用 |
|---|---|
| 轻量入门 | 只想快速弄懂一个概念，总时长少于 3 小时 |
| 自学理解 | 有教材或网课转写稿，不为考试，只想理解、学对 |
| 自学·从零规划 | 只知道想学哪一块，没有材料 |
| 课程学习 | 学期中每周或每两周加入新课件 |
| 备考·冲刺 | 离考试近、时间少 |
| 备考·扎实 | 要冲高分，先刷仿真题再做真题 |

不用自己选规格：描述你的情况和目标，AI 会判断，判断不了时会问你。

## 仓库结构

```
painless-learning/
├── README.md                            ← 中文说明
├── README.en.md                         ← English
├── LICENSE
├── claude/painless-learning-web/
│   ├── SKILL.md
│   └── scripts/validate_course.py
├── codex/painless-learning-web/
│   ├── SKILL.md                         ← 精简核心：必须做到的事 + 流程
│   ├── references/                      ← 各环节细则，做到哪步读哪个
│   ├── agents/openai.yaml
│   └── scripts/validate_course.py
├── workbuddy/painless-learning-web/
│   ├── SKILL.md
│   └── scripts/validate_course.py
└── dist/                                ← 打包好的 zip，用于界面上传
    ├── painless-learning-web-claude.zip
    ├── painless-learning-web-codex.zip
    └── painless-learning-web-workbuddy.zip
```

WorkBuddy 包的 SKILL.md 开头多了一节“零、环境约定”。它说明了和 Claude 版的区别：网页写成本地文件；课件用相对路径链接到 PDF 的某一页；网页里不能调用 AI，Cheat Sheet 的整理改成“复制给 AI”；自我改进时直接修改 skill 文件。

Codex 包拆成了“精简 SKILL.md + references/”：SKILL.md 只写必须做到的事（学习目的只听用户说、知识点级拓扑图、确认稿最低要求和样例、怎么提问、网页交付），细则按环节放在 `references/` 里。这样做是因为单个长文件在 Codex 里容易被略读，出现过只给模块级直线路线、不提问的情况。

## 安装

```bash
git clone https://github.com/leonaluo88/painless-learning.git
cd painless-learning
```

**Claude（claude.ai / 桌面端）**：在 Claude 设置的 Skills 页面上传 `dist/painless-learning-web-claude.zip`。

**OpenAI Codex**
```bash
mkdir -p ~/.agents/skills
cp -r codex/painless-learning-web ~/.agents/skills/
# 或者只放进某个项目：<项目根目录>/.agents/skills/
```
较早版本的 Codex 读取 `~/.codex/skills/`。装好后重启 Codex；可以直接描述任务，也可以用 `$painless-learning-web` 调用。

建议再做两件事：
- **让 Codex 弹出选项对话框提问**：Codex 的提问工具 `request_user_input` 默认只在 Plan 模式下可用。在 `~/.codex/config.toml` 里加上下面几行，普通模式下也能用（没打开时，skill 会在回复里列出编号选项，然后停下来等你回答）：
  ```toml
  suppress_unstable_features_warning = true

  [features]
  default_mode_request_user_input = true
  ```
- **用 Sites 托管网页**：在 Codex 里装好 Sites 插件后，skill 会先把拓扑图确认稿发布成一个网页，之后补课堂、补题库、每周更新都在同一个 site 上改。新建的 site 默认只有你自己能看，分享前检查分享范围。

**腾讯 WorkBuddy**：有两种方式。
- 在界面上传：技能 → 添加技能 → 上传技能，选择 `dist/painless-learning-web-workbuddy.zip`。
- 手动放入：
  ```bash
  mkdir -p ~/.workbuddy/skills
  cp -r workbuddy/painless-learning-web ~/.workbuddy/skills/
  ```
  放好后重启 WorkBuddy。

**Claude Code / 其他工具**：把 `codex/painless-learning-web` 复制到该工具的 skills 目录，例如 `~/.claude/skills/`、`~/.gemini/skills/`。

## 使用示例

```
这是 MAST90138 第 3 周的课件和 lecture 转写，在 ~/Courses/MAST90138/Week3。做成学习网页。
MAST90138 第 4 周的材料来了，更新一下网页。
11 月 10 日期末，样卷和往年卷在 exam/ 里。我要扎实版，冲高分。
我想自学贝叶斯统计，能看懂相关论文就行，手上没有教材。
什么是 KL 散度？给我做个轻量入门。
```

## 校验脚本

```bash
python3 codex/painless-learning-web/scripts/validate_course.py path/to/data/course.json --order
```
脚本检查缺失的前置、循环依赖、引用了不存在的知识点；有错误时返回码为 1。没有掌握标准、没有题目、没有逻辑主线、顺序可疑这几类只给提醒，不影响返回码。加 `--order` 会输出一个合法的学习顺序。

## 许可证

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)：可以自由使用、转发和修改，但需要署名，并且不能用于商业用途。详见 [LICENSE](LICENSE)。
