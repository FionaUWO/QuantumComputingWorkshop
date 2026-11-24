# 8.4 CSS codes：对话稿 + 分镜（草稿，待确认）

- 状态：草稿，2026-11-24。`script.py` 已写好并通过 `check_script.py`（包括接话检查）；`scene.py` 还没写，没有配音，没有渲染。先确认台词和画面。
- 这一段要让观众换成的看法：**一个 CSS 码就是把两个经典码叠在同一排量子比特上，一个管比特翻转，一个管相位翻转。量子力学只多加了一个条件：两张表的每一行都要偶数次重叠（H_X H_Zᵀ = 0）。好的经典码本身不够，bit flip 码的表就过不了这一关，Hamming 码的表能过。**
- 内容出处：`src/content/lectures/08-stabilizer/04-css-codes.mdx`（Nielsen and Chuang 10.4.1、10.4.2）。
- 形式：双人对话。**A** 讲解，**B** 提问。规则见 `video/STYLE_3B1B.md` 第 7、8、9 节，接话规则见根目录 `VIDEO_WORKFLOW.md`。
- 衔接：8.3 结尾 B 注意到 Shor 和 Steane 码的 check 全是 X 或全是 Z，A 说"不是巧合，可以用两个经典码造出来"。8.4 从这里接着开始。
- 吸取 8.3 的审片意见：exactly 这类词可以用，但不要一直用同一个，换着说（just、only、precisely 或直接省掉）；CNOT 的读音表已带上（这一节其实没用到 CNOT）。
- 规模：32 行，约 950 词。A 25 行约 860 词（平均每句 24.2 词）；B 7 行约 95 词，占 10%。写在脚本里的停顿合计约 21 秒。估计成片 5 分钟左右，以配音为准。
- "停" 一列是句后的静默秒数，以 `script.py` 的 `PAUSE_AFTER` 为准；**加粗的是思考停顿**，期间画面不出现新信息。

## 大纲

| 场景 | 内容 | 观众带走什么 |
|---|---|---|
| I 片头 | 实验室介绍、标题卡 | |
| A 开场 | Steane 码的两半来自同一张 Hamming 表；"把经典表抄成 X 一份、Z 一份"这个配方总能行吗？B 说只要码好就行；A 说这只是一半 | 一个要找的"缺的那一半" |
| B 经典的表 | 每行问"这几位加起来是不是偶数"；全偶 = 通过，通过的消息构成码（kernel）；翻一位，奇数行的图案就是那一列 | parity check、kernel、syndrome 的经典来源 |
| C 两张表和一个条件 | H_X 变 X check、H_Z 变 Z check；同字母永远对易，只用管 X 对 Z；拿 bit flip 码试，XXI 和 IZZ 只重叠一位，反对易；条件 H_X H_Zᵀ = 0；k = n − rank H_X − rank H_Z | CSS 条件 |
| D 两个经典解码器 | X 错误只触发 Z check（H_Z e），Z 错误只触发 X check（H_X e′），Y 两边都亮，两个解码器各修各的 | 量子解码拆成两个经典问题 |
| E 回到 Steane | H Hᵀ = 0：任意两行重叠 2，每行和自己重叠 4；bit flip 表的乘积里有 1；"包含自己的对偶码" | 条件在 Steane 码上成立 |
| F 收尾 | 命名 CSS（Calderbank、Shor、Steane）；B 问 check 一定要横跨整个码吗，指向 8.5 surface code | |

## 配色

全部沿用 `common.py` 和 8.1 到 8.3 的含义，**不新增颜色**。

| 颜色 | 只代表 |
|---|---|
| 紫（PAULI_X） / 绿（PAULI_Z） | X / Z 方块；X 那张表 H_X 的行一律紫色，Z 那张表 H_Z 的行一律绿色 |
| 半紫半绿 | Y（和 8.3 一样） |
| 暗色（DIM） | 恒等 I；表里的 0 |
| 白色（INK） | 表里的 1；"偶数""+1"；syndrome 里的 0 |
| 橙色（ACCENT） | 负号、"奇数"、syndrome 里的 1、乘积矩阵里不为 0 的格子 |
| 青色（HILITE） | 当前要看的东西：正在讲的那一行、那一列、重叠的格子 |

经典部分（B 场景）的比特用一排小方格表示，里面写 0 或 1；被翻转的那一位上方贴一个紫色 X 方块（比特翻转就是 X），不另造颜色。

## 运镜总则

- 二维画面，镜头固定，运动都来自画面里的对象。
- 贯穿全片的组件：**表**（0/1 矩阵，1 白 0 暗，和 8.3 的 H 同一画法）、**check 串**（字母方块）、**syndrome 灯**、**重叠计数**（两行上下对齐，重叠的格子框青色，旁边写数字和"even ✓ / odd ✗"，和 8.3 b7 相同）。
- C 场景"一行 X 对一行 Z"的那张图是讲义 `CssOverlap` 的动画版：同样用 X₁X₃X₅X₇ 和 Z₂Z₃Z₆Z₇，重叠在 3 和 7。

## I 场景：片头

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| i1 | A | Hello everyone, and welcome back. We are QAICON Lab, … at Western University. | 和前几节相同的 logo 小动画 | 0.4 |
| i2 | B | And today, we build quantum codes out of classical ones. | 标题卡 "Quantum Computing Workshop / CSS codes / Lecture 8 · Section 8.4" | 0.95 |

## A 场景：开场，这个配方总能行吗

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| a1 | A | At the end of the last section we noticed that every check in Shor's code and in Steane's code is made entirely of X's or entirely of Z's, and in Steane's code both halves come from the same table of ones and zeros. | 8.3 结尾的两张小卡片 Shor、Steane 展开成 check 列表（每行全紫或全绿）。Shor 淡出，Steane 的 6 行留下；上三行（紫）和下三行（绿）各被一个括号罩住，两个括号都指向中间同一张 3×7 的表 H | 0.6 |
| a2 | A | That table is older than quantum computing by decades, since it belongs to the Hamming code, which engineers have used since the nineteen fifties to repair a single flipped bit in a message. | check 列表淡出，只留表 H 在中央。旁边出现小字 "Hamming code · 1950"；下面一排 7 个比特格，其中一位被翻转（上方贴紫色 X），再被修回 | 0.6 |
| a3 | A | So here's a tempting recipe. Take a classical code you like, write its table once with X's and once with Z's, and call the result a quantum code. Do you think that always works? | 表 H 复制成两份，左边一份的 1 变成紫色 X 方块，右边一份的 1 变成绿色 Z 方块；两份之间一个箭头指向 "quantum code"，后面一个青色 "?" | **1.2** |
| a4 | B | Hmm, the Z checks catch bit flips and the X checks catch phase flips, so as long as the code is good, right? | 绿色那份下面写 "catches bit flips"，紫色那份下面写 "catches phase flips"（她的理由） | 0.35 |
| a5 | A | Well, that's half of the answer, because a good code is certainly needed. But the half that's missing is the one genuinely quantum part of the story, so let's go and find it. | "?" 下面出现两格：第一格 "a good classical code ✓"，第二格空着、虚线框、青色 "?"。这个两格的小牌子缩到右上角，全片留着 | 0.95 |

## B 场景：一张表在经典世界里做什么

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| b1 | A | So what does a table like this actually do for a classical message? Each row picks out a few positions, and it asks whether the bits sitting in those positions add up to an even number. | 表 H 在上方，下面一排 7 位消息 0110011（一个 Hamming 码字）。第一行变青，它挑中的 4 位（4、5、6、7）在消息里也框青，这 4 位的数字飞到一边相加，得 2，写 "even"（白） | 0.6 |
| b2 | A | A message passes when every row says even, and the messages that pass are the code, which in linear algebra is called the kernel of the table, with all the arithmetic done mod two. | 第二、三行同样做一遍，都是 "even"，消息旁边出现 ✓ "passes"。几条别的码字从下面一闪而过，都打 ✓，收进一个圆角框；句尾框上写 "the code = kernel of H (mod 2)" | 0.6 |
| b3 | A | Now if one bit flips, the rows that contain it start saying odd, and the pattern of odd rows you get is the column of the table at the position that flipped. | 回到那一条消息，第 5 位上方贴紫色 X，数字 0 变 1。第一行和第三行的结果变成橙色 "odd"，第二行仍是白色 "even"；三行右边的灯读出 1 0 1，然后 H 的第 5 列（1 0 1）框青，和灯并排 | 0.45 |
| b4 | B | Oh, that's the address trick from Steane's code. | 角落淡入 8.3 的 Steane 三圆小图，比特 5 和圆 1、圆 3 亮橙 | 0.35 |
| b5 | A | Right. Now you can see where Steane's code got it from, and nothing quantum happens in this picture at all, it's an ordinary parity check, the kind of check the memory in your computer runs all day long. | 三圆小图淡出。整幅画面左上角贴一个灰色小标签 "classical"，然后整体淡出 | 0.95 |

## C 场景：两张表，和那一个条件

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| c1 | A | So now you take two tables with the same number of columns, which we'll call H X and H Z, and turn every row of the first into an X check and every row of the second into a Z check. | 左边一张表标 H_X，右边一张标 H_Z（先用两张一般的、示意的 0/1 表，n 列）。左表每一行"翻"成一行紫色 X 串，右表每一行翻成一行绿色 Z 串 | 0.6 |
| c2 | A | Two X checks always commute, and so do two Z checks, since a letter never clashes with itself, which leaves just one kind of pair to worry about, an X check against a Z check. | 两行紫色之间画一根线，标 ✓；两行绿色之间标 ✓；紫对绿的连线是青色 "?"（共几根，按两张表的行数） | 0.6 |
| c3 | A | And as we saw last time, an X and a Z clash on every qubit they share, so the pair commutes when they share an even number of qubits and anticommutes when that number is odd. | `CssOverlap` 动画：X₁X₃X₅X₇ 在上、Z₂Z₃Z₆Z₇ 在下对齐，第 3、7 列框青，迸出两个橙色 "−"，相撞消失，旁边写 "2 · even ✓" | 0.6 |
| c4 | A | Let me try the tempting recipe on the smallest table we know, the two rows of the bit flip code, written once with X and once with Z. | 清场。bit flip 码的表 110、011 出现；复制成 X 版 X X I、I X X 和 Z 版 Z Z I、I Z Z。X X I 和 I Z Z 被拉出来上下对齐，旁边一个青色 "?" | **1.2** |
| c5 | B | X X I and I Z Z only share qubit two. So they anticommute! | 第 2 列框青，重叠计数 "1" | 0.35 |
| c6 | A | That's it. Qubit two is the single clash, so a perfectly good classical code still breaks the recipe, because one row of one table overlaps one row of the other an odd number of times. | 第 2 列迸出一个橙色 "−"，没有另一个来抵消，留在原处；旁边 "1 · odd ✗"。右上角小牌子的空格轻轻闪 | 0.6 |
| c7 | A | So the missing half is this. Every row of H X has to share an even number of ones with every row of H Z, and if you collect all those overlaps into one product, the condition reads H X times H Z transpose equals zero, mod two. | 一张小格子表：竖着是 H_X 的各行，横着是 H_Z 的各行，每格填两行的重叠数 mod 2。bit flip 码那张填出来有橙色的 1。说到 "collect" 时格子表收成一个矩阵，写出 H_X H_Zᵀ = 0 (mod 2)。右上角小牌子的空格填上这条式子 | 0.6 |
| c8 | A | When that holds, the checks define a code, and the number of logical qubits is n minus the number of independent X checks minus the number of independent Z checks, the same halving count as before. | 8.1、8.3 用过的减半竖条：2ⁿ 先被 H_X 的独立行各砍一半，再被 H_Z 的独立行各砍一半，最后写出 k = n − rank H_X − rank H_Z | 0.95 |

## D 场景：两种错误，两个经典解码器

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| d1 | A | Once the checks commute, the two kinds of error stay out of each other's way. A bit flip only trips the Z checks, and the pattern it leaves is H Z times the error, so you can decode that half like an ordinary classical code. | 一排 7 个比特点。上方紫色 X 串那组 check 的灯、下方绿色 Z 串那组的灯。一个紫色 X 落到某个比特，只有绿色那组的灯亮橙；灯连到一个方框 "classical decoder for H_Z"，旁边写 H_Z e | 0.6 |
| d2 | A | A phase flip trips nothing but the X checks, leaving H X times its pattern, and that half gets a classical decoder of its own. | 绿色 Z 落到另一个比特，只有紫色那组的灯亮；连到另一个方框 "classical decoder for H_X"，写 H_X e′ | 0.45 |
| d3 | B | And a Y error, which is a bit flip and a phase flip at once? | 一个半紫半绿的 Y 方块悬在比特上方，还没落下 | **1.1** |
| d4 | A | It lights up both halves at the same time, and each decoder fixes its own part of it, one undoing the bit flip and the other the phase flip, without ever needing to talk to each other. | Y 落下，两组灯同时亮。Y 方块一分为二：紫色一半飞向 H_Z 那边的解码器，绿色一半飞向 H_X 那边（各自去找能看见它的那组 check），两个解码器各吐出一个修正，Y 消失 | 0.6 |
| d5 | A | I find that the nicest part of the construction, because all the hard work of decoding a quantum code turns into two classical problems that people already knew how to solve. | 两个解码器方框之间竖起一道淡色的墙，墙上写 "no talking needed"；两个方框各标 "classical" | 0.95 |

## E 场景：回到 Steane 码

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| e1 | A | So let's go back to Steane's code, where both tables are the same H, and the condition becomes H times its own transpose equals zero. | H（3×7）和它的转置 Hᵀ（7×3）并排，中间一个乘号，等号后面是一个 3×3 的空格子 | 0.6 |
| e2 | A | If you check, any two rows of the Hamming table share two ones, and each row shares four with itself, so every overlap is even, and the condition holds. | 3×3 格子逐格填：对角线三格先写 4 再变成 0，其余六格先写 2 再变成 0；旁边小图是 8.3 的三个圆，填哪一格，就亮哪两个圆的交集（或一个圆自己） | 0.45 |
| e3 | B | So the bit flip table failed, but the Hamming table passes. | 左边移进 bit flip 表的乘积 [[0,1],[1,0]]，两个 1 是橙色，标 ✗；右边 Steane 的全 0 矩阵标 ✓ | 0.35 |
| e4 | A | Right. Classical coding theorists have a name for a table like that, they say the code contains its dual, and it's the one extra demand that a quantum code makes on top of the classical theory. | 一个大圆角框标 "Hamming code"，里面一个小框（H 的行张成的集合），句尾小框上写 "its dual"，大框上写 "contains its dual" | 0.95 |

## F 场景：收尾，指向 8.5

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| f1 | A | So two classical codes laid over the same qubits, one for each kind of error, give you a quantum code as long as their tables overlap evenly, and codes built this way are called CSS codes, after Calderbank, Shor and Steane. | 一排量子比特点。上面浮一层紫色的表（H_X），下面一层绿色的表（H_Z），两层都对准这排比特；中间一个 "even overlaps ✓"。句尾出现名字 "CSS codes"，下面小字 "Calderbank · Shor · Steane"。右上角小牌子两格都打 ✓ | 0.45 |
| f2 | B | But these checks still reach right across the whole code. Do they have to? | Steane 的一个 check（比如 X₁X₃X₅X₇）从它的 ancilla 画出四根线，连到相隔很远的比特上 | 0.35 |
| f3 | A | They don't, and in section eight point five we'll meet the surface code, a CSS code whose checks only ever touch four neighbouring qubits on a flat grid. | 标题卡 "Next: 8.5 The surface code"，下面一小块方格网，一个 check 只连着它周围的四个比特 | 0.95 |

## 自查（对照 `STYLE_3B1B.md` 的清单）

| 项 | 情况 |
|---|---|
| 1 一句话看法 | 有，见文件开头 |
| 2 30 秒内的问题或被纠正的说法 | a3："这个配方总能行吗？" B 说只要码好就行，a5 说只对一半，c4 到 c6 用 bit flip 码推翻 |
| 3 公式前先有画面 | H_X H_Zᵀ = 0 在逐格重叠数填完之后才写出（c7）；k = n − rank − rank 在减半竖条之后（c8）；H Hᵀ = 0 先逐格算再总结（e2） |
| 4 颜色只代表一件事 | 没有新增颜色。H_X 的行一律紫、H_Z 的行一律绿；"奇数"和乘积里的 1 用橙色，和负号同属"出了冲突" |
| 5 切换还是变形 | 表的行"翻"成 check 串；重叠格子收成乘积矩阵；Y 方块一分为二 |
| 6 旁白说的屏幕上都有 | 是 |
| 7 交代省略 | 见下面"讲义里有、视频里没放的" |
| 8 结尾回到开头并指向下一段 | 右上角的两格小牌子从 a5 立起，c7 填上条件，f1 两格都打 ✓；f3 指向 8.5 |
| 9 思考停顿 | 3 处：a3（1.2）、c4（1.2）、d3（1.1） |
| 10 提问者 | 7 行，占 10%。a4 猜"码好就行"，被 c4 到 c6 推翻；c5 自己算出反对易；d3 提问；b4、e3 复述确认 |
| 11 `check_script.py` | 全部在范围内：平均每句 24.2 词，短句 20%，承接词开头 43%，带 you 23%，带 I 或 we 29%，问句 6% |
| 12 接话接住 | a5 "Well, that's half of the answer"（猜得一半对，先承认）、b5 "Right."（她认出了地址技巧）、c6 "That's it."（她算对了）、d4 "It lights up both halves"（直接答她的问题）、e4 "Right."（她复述对了）、f3 "They don't"（否定问题直接答）。同一场景没有重复的肯定词，肯定词都单独成句 |
| 13 念出来像不像在讲 | 我念不出声音，需要你听 |

先描述后命名：kernel（b2 句尾）、"contains its dual"（e4）、CSS codes（f1 句尾，前面一直只说"这种码"）。讲解者说自己的态度：d5（"I find that the nicest part"）。

## 讲义里有、视频里没放的

- 命题的证明只用画面演示（重叠数的奇偶），没有逐字念 "inner product over F₂"。
- rank 这个词没有在台词里出现，c8 说的是 "independent X checks"；画面上的式子写 rank。
- Shor 码作为 CSS 码的 H_X、H_Z 没有单独写出（8.3 已经演示过它的 X、Z check 互相对易）。
- 讲义没有 bit flip 码这个反例，是我加的（c4 到 c6、e3），用来推翻 B 的猜测。

## 需要你定的三件事

1. **c4 到 c6 的 bit flip 码反例**是讲义里没有的，我加它是为了让"好的经典码不够"有一个具体的例子，大约 30 秒。保留吗？
2. **要不要加线路图？** 8.3 你加了线路图。这一节可以在 D 场景加一张：X 型 check 和 Z 型 check 用两组分开的 ancilla 测，正好对应"两个解码器各管各的"。会再长约 20 秒。要加吗？
3. **a2 的 "since the nineteen fifties"**：Hamming 码是 1950 年发表的，这个说法没问题。画面上我打算写 "Hamming code · 1950"，可以吗？
