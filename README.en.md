# Painless Learning Web · painless-learning

[中文](README.md) | **English**

An AI agent skill that turns lecture slides, textbooks, lecture transcripts and sample exams, or even just "I want to learn X", into an interactive learning website, **one site per course**.

This repository contains three skill packages. They follow the same rules; each is adapted to its agent's environment:

| Package | For | How the site is delivered |
|---|---|---|
| `claude/painless-learning-web/` | Claude (claude.ai web / desktop) | Published as an artifact, a hosted page with a link. Screenshots of the cited slide pages are uploaded with it |
| `codex/painless-learning-web/` | OpenAI Codex | Written to `_学习网页/index.html` in your course folder and opened directly in a browser. Includes `agents/openai.yaml` for the Codex UI |
| `workbuddy/painless-learning-web/` | Tencent WorkBuddy | Same as the Codex package, without `agents/openai.yaml` |

Other tools that support the [Agent Skills standard](https://agentskills.io/specification), such as Claude Code, Gemini CLI and GitHub Copilot, can use the Codex or WorkBuddy package.

> **Language note**: the skill instructions are written in Chinese. By default the generated sites explain things in Chinese and keep the original English terms, because the skill was built for students taking English-taught courses. To get English output, just tell the agent "write the site in English".

## What it does

- **Fine-grained concepts and a prerequisite graph.** Each concept covers one idea. The graph is built backwards from exam questions or your learning goal: each concept's prerequisites, then theirs, with links across modules. Concepts are numbered so that each prerequisite comes just before it is first needed. The graph is clickable: select a concept to highlight everything before and after it, or switch to "view by exam question" to see everything a question needs.
- **Every step follows one fixed layout:** why now → intuition → definition or formula → plain-language explanation → worked example → common pitfalls → self-check → exam references. Formulas use real LaTeX, and derivations are aligned with a short reason on every line.
- **A storyline for every lesson.** The last step of each lesson is a cause-and-effect chain (problem → idea → method → result → new problem) that ties the details together. Every step also shows where it sits on that chain.
- **Checks that you have really learned it.** Every concept has a testable mastery criterion. Questions come in four levels: recall, explain, apply, transfer. Each comes with a library of common wrong answers that trigger targeted feedback, plus two levels of hints. One question card is used across the whole site. You tick "mastered" yourself, and the "not mastered" filter is your mistake book.
- **Easy to pick up, and everything can be undone.** Each section opens with a one-line how-to. Ticking, answering, resetting, removing and importing can all be undone. A one-click full reset backs up your progress first.
- **Weekly updates.** Concepts have stable IDs, so your progress survives updates. Fixed rules handle prerequisites that are taught later, corrections from the lecturer, conflicts between old and new material, and dependency cycles.
- **Exam mode.** Works backwards from sample exams to the concepts you need, and sets how deep each concept must go from the way questions are asked. The thorough version drills you on look-alike practice questions first and keeps the real past papers locked until the end. If notes are allowed in the exam, a cheat-sheet inbox collects material that becomes your note sheet.
- **Plan from scratch / quick intro.** With no materials, the agent first researches authoritative courses and plans a route, then builds the site. If you only want to understand one concept (under 3 hours), it builds a compact site straight away without asking questions.
- **Self-improvement.** When you ask for changes, the agent fixes the site first. Then it decides whether the problem belongs only to this course, to a whole subject area, or to every subject. In the last two cases it proposes a new rule, and writes it into the skill only after you confirm. Each change is recorded in the skill's rule changelog.

### Six modes

| Mode | When to use |
|---|---|
| Quick intro | You just want to understand one concept; under 3 hours in total |
| Self-study | You have a textbook or course transcripts, no exam; you want to understand it correctly |
| Self-study · plan from scratch | You know what area you want to learn but have no materials |
| Course study | During semester, adding new slides every week or two |
| Exam · sprint | The exam is close and time is short |
| Exam · thorough | You are aiming for a high score: look-alike questions first, real papers last |

You don't have to pick a mode. Describe your situation and goal, and the agent decides; if it can't tell, it asks.

## Repository layout

```
painless-learning/
├── README.md                            ← Chinese
├── README.en.md                         ← English
├── LICENSE
├── claude/painless-learning-web/
│   ├── SKILL.md
│   └── scripts/validate_course.py
├── codex/painless-learning-web/
│   ├── SKILL.md
│   ├── agents/openai.yaml
│   └── scripts/validate_course.py
├── workbuddy/painless-learning-web/
│   ├── SKILL.md
│   └── scripts/validate_course.py
└── dist/                                ← ready-made zips for uploading in an app
    ├── painless-learning-web-claude.zip
    ├── painless-learning-web-codex.zip
    └── painless-learning-web-workbuddy.zip
```

The SKILL.md in the Codex and WorkBuddy packages starts with an extra section, "零、环境约定" (Environment conventions). It covers the differences from the Claude version:

- The site is written as local files.
- Slides are linked by relative path to a specific PDF page.
- The page cannot call an AI, so cheat-sheet entries are tidied up by copying them to the agent.
- Self-improvement edits the skill file directly.

## Installation

```bash
git clone https://github.com/leonaluo88/painless-learning.git
cd painless-learning
```

**Claude (claude.ai / desktop):** upload `dist/painless-learning-web-claude.zip` on the Skills page in Claude's settings.

**OpenAI Codex**
```bash
mkdir -p ~/.agents/skills
cp -r codex/painless-learning-web ~/.agents/skills/
# or for one project only: <project root>/.agents/skills/
```
Older versions of Codex read `~/.codex/skills/` instead. Restart Codex after installing. Then describe your task, or call the skill explicitly with `$painless-learning-web`.

**Tencent WorkBuddy**, either:
- Upload it in the app: Skills → Add skill → Upload skill, then choose `dist/painless-learning-web-workbuddy.zip`.
- Or copy it in by hand, then restart WorkBuddy:
  ```bash
  mkdir -p ~/.workbuddy/skills
  cp -r workbuddy/painless-learning-web ~/.workbuddy/skills/
  ```

**Claude Code / other tools:** copy `codex/painless-learning-web` into that tool's skills folder, for example `~/.claude/skills/` or `~/.gemini/skills/`.

## Example prompts

```
Here are the Week 3 slides and lecture transcript for MAST90138, in ~/Courses/MAST90138/Week3. Turn them into a learning site.
The Week 4 materials for MAST90138 are in. Update the site.
The final is on 10 November; the sample and past papers are in exam/. I want the thorough version and a high score.
I want to teach myself Bayesian statistics well enough to read papers. I don't have a textbook.
What is KL divergence? Make me a quick intro.
```

## Validation script

```bash
python3 codex/painless-learning-web/scripts/validate_course.py path/to/data/course.json --order
```
The script reports these as errors and exits with code 1:
- missing prerequisites
- dependency cycles
- references to concepts that don't exist

These only produce warnings and don't change the exit code:
- missing mastery criteria
- concepts with no questions
- lessons without a storyline
- a suspicious teaching order

`--order` prints one valid learning order.

## License

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/): you may use, share and adapt it with attribution, but not for commercial purposes. See [LICENSE](LICENSE).
