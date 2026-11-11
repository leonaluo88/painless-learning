# 课程数据文件 course.json

## 二、课程数据文件

每门课维护一个 `course.json`，网页由它生成。更新时改这个文件，再重新生成网页。

保存在两个地方，保证下次对话能接着做：
1. 网页文件夹里的 `data/course.json`
2. 用户的课程文件夹 `_学习网页/course.json`（能写入时）

更新前先读这个文件。两处都找不到时，从已发布的网页里还原，并告诉用户。

```json
{
  "course": {"code":"…", "name":"…", "profile":"self|self-plan|course|exam-sprint|exam-deep",
             "exam": {"date":"…", "format":"…", "answer_lang":"en|zh", "allowed":"…"}},
  "sources": [{"id":"W03L1", "file":"…", "url":"…", "type":"lecture|transcript|textbook|tutorial|lab|assignment|sample_exam|past_exam|exam_info|web", "week":3, "added":"…"}],
  "modules": [{"id":"M-sql-basic", "name":"…", "order":5}],
  "points": [{
    "id":"sql-left-join",        // 稳定 ID，生成后永不修改
    "no":57,                      // 显示编号，每次生成时重新排
    "title":"一句话内容",
    "module":"M-sql-basic",
    "week":5,
    "tier":3,                     // 3 核心 / 2 重要 / 1 次要 / 0 不考（自学类可以不分级）
    "depth":"apply",              // recall 认得 / explain 会解释 / apply 会用 / transfer 能迁移
    "pre":[{"id":"sql-inner-join","kind":"hard"}, {"id":"null","kind":"soft","why":"IS NULL"}],
    "src":[{"source":"W05L1","page":24}, {"source":"W05L1-transcript","time":"32:10"}],
    "exam_refs":["样卷2 Q2A"],
    "mastery":"做对什么题算掌握（一句话，必须能用题检验）",
    "status":"active|merged|deprecated",
    "changed":"日期：改了什么",
    "note":"不考 / 补充 / 老师说过…"
  }],
  "storyline": [{"from":"M-tree", "to":"M-rf", "why":"一句话：前一个模块留下了什么问题，后一个模块怎么接上"}],
  "lessons": [{"id":"L-w05", "track":"learn|review", "title":"…", "points":[…], "steps":[…],
               "storyline":[{"role":"问题|思路|做法|结果|新问题", "text":"一两句", "formula":"可选，写最简形式", "steps":[3,4]}]}],
  "questions": [ … 见第八节 … ],
  "changelog": [{"date":"…", "summary":"…", "added":[…], "changed":[…], "conflicts":[…]}],
  "course_notes": [{"date":"…", "note":"只适用于这门课的偏好或修正（例如记号、某个模块要讲更深），以后更新这门课时一律遵守"}]
}
```

规则：
- **ID 稳定**：进度、勾选、错题都按 ID 存，所以更新后用户的进度不会丢。
- 不删知识点。不再需要的标 `deprecated`；合并的标 `merged`，并指向新 ID。
- `pre` 只写直接前置。`hard` 表示必须先学；`soft` 表示只用到其中一个概念，并写明是哪个。
