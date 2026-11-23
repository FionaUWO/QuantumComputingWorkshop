# 教学视频：流程和方法

这是总览。逐条的风格规则、数字和来由在 `video/STYLE_3B1B.md`；有冲突时以那份为准，改规则也改那份，再回来更新这里的摘要。

## 形式

- 3Blue1Brown 风格，一男一女对话。A 讲解（Brian，男），B 提问（Alexandra，女）。声音 id 和参数在 `video/pipeline/voice.json` 的 `dialogue`。
- 旁白英文；给你的说明、画面描述、分镜用中文。
- 画面 Manim CE（venv `C:/Users/Yanwe/venvs/manim-video`），配音 ElevenLabs text-to-dialogue（`eleven_v4`，每个场景一次请求），`build.py` 负责切句、字幕、合成。
- 纯黑背景，右上角实验室水印，片头 `logo_reveal()`。字幕是可关的独立轨道（`.vtt`），不烧进画面。
- 配色只在 `video/pipeline/common.py` 里定，一种颜色在整个系列只代表一件事。

## 文件放哪

```
video/
├─ STYLE_3B1B.md          风格规则和开工前自查清单
├─ pipeline/              共享：build.py、common.py、voice.json、check_script.py
├─ lec<N>/s<N>_<M>/       每节一个文件夹：storyboard.md、script.py、scene.py
└─ out/lec<N>/s<N>_<M>/   生成的文件（不进 git）
```

## 一节视频的顺序

1. 读这一节的讲义 `src/content/lectures/…`，再看做完的例子 `video/lec1/s1_2/`。
2. 写 `storyboard.md`：第一行是这一节要让观众换成的那个看法；之后每行一句台词，写说话人、台词、画面、句后停顿。每个场景先写成一段连贯的口语，再按画面变化切行。
3. **停下来给你看台词。** 台词定了才配音、渲染。
4. 写 `script.py`、`scene.py`，跑 `check_script.py`，改掉它标出的问题；先静音低画质渲染一个场景给你看。
5. **先配一个场景给你听**，你满意了再配其余的。配音花额度，每次要你同意。
6. 全片渲染，再出 HD，复制到 `public/assets/video/`，用 `Video.astro` 嵌入。你说可以才 commit、push。

审片用 `build.py <节号> review`（精修工具），你把它生成的笔记贴回来。

命令（在 `video/` 下）：

```
C:/Users/Yanwe/venvs/manim-video/Scripts/python.exe pipeline/build.py <节号> <步骤>
C:/Users/Yanwe/venvs/manim-video/Scripts/python.exe pipeline/check_script.py <节号> [--scene 字母]
```

## 台词的要点（详见 STYLE_3B1B.md 第 9 节）

- 讲解者句子要长、像说话：平均每句 14 到 30 词，常用 you / I / we 和 So、But、Now 这类承接词开头。不念要点。
- 不预告路线，不做 recap。片尾一句话指向下一节。
- 停顿：场景之间 0.5 到 1 秒；同一人两句之间约 0.6 秒；换人约 0.35 秒；思考停顿 1.1 到 1.3 秒。不用 break 标签。

### 讲解者怎么接她的话（2026-11-23）

原则不变：先明确接住，再往下讲，不能各说各的。但机械地"肯定词 + 整句复述"听起来像念标准答案，所以：

1. **按她这句的类型接：**

   | 她说的是 | 他怎么接 |
   |---|---|
   | 一个猜测 | Exactly. / Spot on. 然后说对在哪 |
   | 一个发现、意外 | Right? / Isn't that strange? 跟她一起意外 |
   | 一个问题 | 直接答：There is, and… / Good question. 不用 Definitely 去答"有没有" |
   | 常见误解 | Well… 先承认它为什么合理，再纠正 |
   | 否定句（"I can't…"） | 用 No 来同意：Not like this, no. |

2. **复述最多一个关键词，而且要往前推。** 她已经说出的数字或结论不再重说一遍。
3. **肯定词单独成句**，写 "Exactly." 再另起一句，不写 "Exactly, …, because …"。这样它有自己的语调。
4. **同一个场景里不重复同一个肯定词**：Right / Exactly / Spot on / That's it / Good / Not quite 轮换。
5. **语气词放在真会犹豫的地方**：纠正之前（Well…）、坦白之前（Okay, so…）。回答简单核对题时不放。提问者偶尔也可以有一个（Hmm, so…）。

`check_script.py` 会标出：没有接住她的话、第一句复述了她一半以上的话、肯定词后面跟逗号、同一场景肯定词重复。它只会数数，读起来自不自然还要你听。

## 每次都要你点头的事

安装和下载、把台词发给配音服务（花额度）、git commit 和 push。语气、发音、节奏由你判断，我听不到声音。
