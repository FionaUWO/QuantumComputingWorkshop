# 8.3 Three codes：对话稿 + 分镜（草稿，待确认）

- 状态：草稿，2026-11-24。`script.py` 已写好并通过 `check_script.py`（包括接话检查）；`scene.py` 还没写，没有配音，没有渲染。先确认台词和画面。
- 2026-11-24 第二版：按你的要求加了四张线路图（b4、b5、c8、d2），每张都配一句新台词，讲"这个 check 在线路里怎么测"。
- 这一段要让观众换成的看法：**一个能修好任意单比特错误的码，就是让每一种"一个比特出错"的情形都留下不同 syndrome 的码。所以要数的是 syndrome 够不够分：Steane 码里 syndrome 直接就是出错比特的二进制地址；把情形和 syndrome 一数，五个比特刚好够，少一个都不行。**
- 内容出处：`src/content/lectures/08-stabilizer/03-three-codes.mdx`（Nielsen and Chuang 10.5.6；计数界 10.3.4）。
- 形式：双人对话。**A** 讲解，**B** 提问。规则见 `video/STYLE_3B1B.md` 第 7、8、9 节，接话规则见根目录 `VIDEO_WORKFLOW.md`。
- 衔接：8.2 结尾 B 问"能不能做一个每个单比特错误都被抓到的码"，A 说 8.3 有三个，码距都是 3。8.3 从这个回答接着开始。
- 规模：43 行，约 1110 词。A 34 行约 1000 词（平均每句 25.2 词）；B 9 行约 105 词，占 10%。写在脚本里的停顿合计约 27 秒。估计成片 5 分半到 6 分钟，以配音为准。
- "停" 一列是句后的静默秒数，以 `script.py` 的 `PAUSE_AFTER` 为准；**加粗的是思考停顿**，期间画面不出现新信息。

## 大纲

| 场景 | 内容 | 观众带走什么 |
|---|---|---|
| I 片头 | 实验室介绍、标题卡 | |
| A 开场 | Shor 码用 9 个比特；先猜最少要几个，B 猜 9，A 说更少，留到最后 | 一个贯穿全片的问题 |
| B Shor 码 | 8 个 check：6 个块内 Z 对、2 个跨块 X 六连；**线路图：Z 型 check 和 X 型 check 各怎么测**；重叠 0 或 2，对易；9 − 8 → 1 个逻辑比特；逻辑 X 全是 Z | Shor 码的 stabilizer 写法；check 是用辅助比特测的 |
| C Steane 码 | 1 到 7 的二进制当列；三个圆；6 个 check；X₅ 的 syndrome 是 101 = 5；**线路图：X₅ 只传到两根辅助线** | syndrome 就是地址 |
| D 五比特码 | 循环移位的 XZZXI；**线路图：混合 check 也一样测**；数情形和 syndrome：3n + 1 ≤ 2ⁿ⁻¹，n = 5 刚好相等；回答开头的问题；坦白"退化码"这一点 | 为什么最少是 5 |
| E 收尾 | 一句话总结；B 注意到 Shor、Steane 的 check 全是 X 或全是 Z，指向 8.4 | |

## 配色

全部沿用 `common.py` 和 8.1、8.2 草稿里的含义，**不新增颜色**。

| 颜色 | 只代表 |
|---|---|
| 紫（PAULI_X） / 绿（PAULI_Z） | X / Z 方块（沿用 8.1、8.2） |
| 暗色（DIM） | 恒等 I 的空格；被调暗的东西 |
| 橙色（ACCENT） | 回答 −1、syndrome 里的 1、块内的负号 |
| 白色（INK） | 回答 +1、syndrome 里的 0 |
| 青色（HILITE） | 当前要看的东西：正在讲的那个块、那个圆、那个比特 |

syndrome 仍画成一排小灯（8.2 的组件），亮橙色是 1，白色空心是 0。Steane 的三个圆平时是 MUTED 细线，讲到哪个，哪个变青。

## 运镜总则

- 二维画面，镜头固定，运动都来自画面里的对象。
- 贯穿全片的组件：**比特排**（一排编号圆点，Shor 9 个分三块，Steane 7 个，五比特码 5 个）、**check 列表**（字母方块串，和 8.1、8.2 一样）、**syndrome 灯**、右上角一个小**计分牌**"fewest qubits = ?"，开头立起，D 场景结尾填上 5。
- 三个码依次出场时，前一个码缩成左下角的小卡片（"Shor [[9,1,3]]"、"Steane [[7,1,3]]"），不删除，E 场景三张卡片并排。
- C 场景的三个圆是讲义里 `SteaneVenn` 那张图的动画版，比特编号位置相同。

## 线路图的画法（四张共用）

- 和第 7 讲讲义的 `BitFlipCircuit` 同一种画法：数据线在上，辅助线在下、起点标 \|0⟩，右端是测量表。线和 CNOT 用白色（INK），H 是白框方块。
- 只有真的是 X 门、Z 门的方块才上色：受控 X 是紫色方块，受控 Z 是绿色方块，和 check 列表里的字母同色。所以线路图里的门一格一格对得上那一行字母。
- 错误用一个橙色小脉冲表示，沿 CNOT 的竖线传到辅助线；测量表读出 1 时亮橙，读出 0 时白，和 syndrome 灯同一套颜色。
- 每张线路图都从 check 列表里的那一行"拉出来"（变形），讲完缩回去或淡出，不是硬切。
- 线路图只出现在这四句，其余时间画面上没有线路。

## I 场景：片头

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| i1 | A | Hello everyone, and welcome back. We are QAICON Lab, … at Western University. | 和 8.1、8.2 相同的 logo 小动画 | 0.4 |
| i2 | B | And today, we meet three codes that can fix any error on a single qubit. | 标题卡 "Quantum Computing Workshop / Three codes / Lecture 8 · Section 8.3" | 0.95 |

## A 场景：开场，最少要几个比特

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| a1 | A | Last time we ended on a question, whether a code can catch every possible error on a single qubit, and the answer is yes, as long as the lightest error that slips past all of its checks has a weight of at least three. | 8.2 的刻度尺从左边滑进来，d 的位置标在 3；比 3 轻的那段写 "caught, or harmless"（和 8.2 e2 同一个画面） | 0.6 |
| a2 | A | Peter Shor found the first code like that in 1995, and it spends nine physical qubits to protect a single qubit of information, which does feel like rather a lot. | 刻度尺退到一边。中央一排 9 个比特圆点，上面一个小圆点代表 1 个逻辑比特，九条细线把它连到下面 9 个点 | 0.6 |
| a3 | A | So here's something for you to guess before we start. What do you think is the fewest qubits that could possibly do the job? | 右上角出现计分牌 "fewest qubits = ?"，"?" 是青色 | **1.2** |
| a4 | B | Hmm, there are three kinds of error, and the bit flip code needed three qubits for just one kind, so nine? | 9 个点分成三组，每组 3 个；三组上方各写一个字母 X、Y、Z 的小标（她的算法：3 × 3） | 0.35 |
| a5 | A | Well, that's a very natural way to count, and it's the way Shor's code is put together. But the true answer is smaller than nine, and by the end you'll be able to see why, just by counting something else. | "3 × 3" 的小标留着；计分牌上的 "?" 下面出现一个灰色小字 "< 9"，"?" 本身不变 | 0.95 |

## B 场景：Shor 码写成 check 列表

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| b1 | A | Let's write Shor's code the way we learned to in the last two sections, as a list of checks, which for nine qubits sitting in three blocks of three comes to eight strings. | 9 个点排成三块（块之间留空）。下方列表一行一行出现，共 8 行，每行 9 个字母方块；先不上色，全是灰色空格 | 0.6 |
| b2 | A | The first six are Z pairs inside each block, just like the checks of the bit flip code, so each block on its own can catch a bit flip on any of its three qubits. | 前 6 行填上绿色 Z 方块：Z₁Z₂、Z₂Z₃、Z₄Z₅、Z₅Z₆、Z₇Z₈、Z₈Z₉。每填一对，上面对应的块轻轻变青 | 0.6 |
| b3 | A | The last two put an X on six qubits at a time, and they compare the signs of two neighbouring blocks, which is how a phase flip anywhere inside a block gets noticed. | 后 2 行填上紫色 X：X₁…X₆、X₄…X₉，上方两个括号各罩住两块。一个 Z₂ 错误落到第一块，第 7 行的灯亮橙色 | 0.6 |
| b4 | A | If you're wondering how a check like that actually gets measured, here is the circuit for the first one, where an extra ancilla qubit starts in zero and two CNOTs copy the parity of qubits one and two onto it, just as in lecture seven. | **线路图 1**（Z 型 check）。列表第 1 行（Z₁Z₂）向右下拉出一张小线路：上面三根数据线（比特 1、2、3），下面一根辅助线标 \|0⟩。说到 "two CNOTs" 时两个 CNOT 依次画出（控制点在比特 1、2，目标 ⊕ 在辅助线，白色），然后测量表。先放一个 X₁ 进去：一个橙色小脉冲从比特 1 沿 CNOT 竖线下到辅助线，测量表读出 1（橙）；再换 X₁X₂：两个脉冲先后到达，相消，读出 0（白）。和第 7 讲 `BitFlipCircuit` 同一种画法 | 0.6 |
| b5 | A | An X check is read the other way round, with a Hadamard on the ancilla before and after, and in between the ancilla controls an X on each of its six qubits, so the ancilla reads one only when that check answers minus one. | **线路图 2**（X 型 check）。线路图 1 缩到左边，右边画第 7 行（X₁…X₆）的线路：六根数据线，辅助线上先一个 H 方块，然后六个受控门，控制点在辅助线上，目标是六个紫色 X 方块在数据线上，再一个 H，再测量表。b3 里的那个 Z₂ 错误这时出现在比特 2 的线上，辅助线读出 1（橙），和列表第 7 行那盏亮橙的灯连一根细线 | 0.45 |
| b6 | B | But the X checks and the Z checks overlap. Do they still commute? | 两张线路图淡出，回到 check 列表。第 1 行（Z₁Z₂）和第 7 行（X₁…X₆）轻轻闪一下 | 0.35 |
| b7 | A | They do. Every Z pair sits either completely inside an X check or completely outside it, so the two share either two qubits or none, and an even number of clashes means they commute. | 第 1 行和第 7 行上下对齐，重叠的两格框出来写 "2"；再拿第 5 行（Z₇Z₈）和第 7 行比，重叠格数 "0"。两个数旁边都写 "even ✓"（8.1 c 场景的数冲突动画） | 0.6 |
| b8 | A | And with nine qubits and eight independent checks, each one cutting the space in half, we're left with two dimensions, which is one logical qubit. | 左边一根竖条标 2⁹，8 个 check 依次各砍一半（8.1 e 场景的组件），最后剩 2，标 "1 logical qubit"。列表缩成左下角小卡片 "Shor [[9,1,3]]" | 0.6 |
| b9 | A | Now here is something I found strange the first time I saw it, which is that the operator acting as a logical X on this code is made entirely of Z letters. | 中央一个 9 格串，全是绿色 Z，旁边写 "= X_L ?" | 0.45 |
| b10 | B | Wait, so Z on all nine qubits flips the logical bit? | 画面不变，"?" 轻轻闪 | **1.1** |
| b11 | A | Yes. Z on the three qubits of a block turns the plus inside that block into a minus, and logical zero and logical one differ by just those three signs, so Z on all nine swaps them, while X on all nine ends up playing the logical Z. | 上方写出 \|0_L⟩ = (\|000⟩ + \|111⟩)⊗3、\|1_L⟩ = (\|000⟩ − \|111⟩)⊗3。Z Z Z 作用在每一块，三个 "+" 依次变成橙色 "−"，\|0_L⟩ 变成 \|1_L⟩；"?" 去掉。句尾在旁边补一个 9 格紫色 X 串，标 Z_L | 0.95 |

## C 场景：Steane 码，syndrome 就是地址

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| c1 | A | Andrew Steane found a code that does the same job with seven qubits, and it comes from a classical idea, which is to write the numbers one to seven in binary as the columns of a table. | 一排数字 1 到 7；每个数字往下展开成一列 3 位二进制，拼成 3 × 7 的表 H。1 是白色，0 是暗色 | 0.6 |
| c2 | A | Each row of this table picks out four of the qubits, so if you draw each row as a circle around its four, you get three overlapping circles with one qubit in every region. | 第一行的四个 1（列 4、5、6、7）变青，那四个比特点被拉到一起，画出圆 1；第二、三行同样，得到 `SteaneVenn` 的三个圆，七个区域各一个比特，7 在正中 | 0.6 |
| c3 | A | Every circle carries two checks, X on its four qubits and Z on the same four, so that's six checks on seven qubits, which once again leaves one logical qubit. | 每个圆旁边贴两张小卡：紫色 X X X X、绿色 Z Z Z Z。右边列出六行 check（讲义里的表）。下面 "7 − 6 = 1" | 0.6 |
| c4 | A | And any two circles share two qubits, while a circle's own X and Z checks share all four, so every overlap is even and all six checks commute. | 圆 1 和圆 2 的交集（比特 6、7）变青，写 "2"；再换圆 1 和圆 3（5、7），"2"；最后圆 1 自身的 X 和 Z，"4"。三个数都标 "even ✓" | 0.6 |
| c5 | A | So now suppose an X error hits qubit five. Before I light anything up, which circles do you think are going to notice it? | 一个紫色 X 落到比特 5 上；三个圆旁边各一盏灯，都是问号 | **1.2** |
| c6 | B | Five sits inside circles one and three, but it's outside circle two. | 画面不变 | 0.35 |
| c7 | A | Exactly. So the three Z checks answer one, zero, one, and if you read that as a number in binary, it comes out as five. | 圆 1、圆 3 的边框变橙，灯亮橙；圆 2 灯白。三盏灯下面写 1 0 1，再变形成 "= 5"，箭头指回比特 5 | 0.6 |
| c8 | A | You can watch the same thing happen in the circuit, where each circle gets its own ancilla, and the X on qubit five only reaches the two ancillas that have a CNOT coming from qubit five. | **线路图 3**（Steane 的三个 Z 型 check）。三个圆缩到左边，右边画 7 根数据线、3 根辅助线（每根辅助线旁边一个小圆圈图标，和左边的圆对应）。12 个 CNOT 按圆分三组，一组一组画出，每组画的时候左边那个圆变青。比特 5 线上的紫色 X 发出橙色脉冲，只沿着它的两根 CNOT 竖线下到辅助线 1 和 3；三个测量表读出 1 0 1，和左边三盏灯对上 | 0.45 |
| c9 | B | Oh, so the syndrome is just the address of the qubit? | 表 H 回到画面上方，第 5 列（1 0 1）亮起，和三盏灯并排 | 0.35 |
| c10 | A | That's it. Each qubit's column in the table is its own number written in binary, so whichever qubit is hit, the syndrome spells out where, and a Z error does the same thing through the X checks. | X 错误快速换到比特 3、6、7，灯分别读出 011、110、111，每次都指回那个比特。最后一个绿色 Z 落到比特 5，这次是 X 那一组的灯读出 101。整幅图缩成小卡片 "Steane [[7,1,3]]"，放到 Shor 卡片旁边 | 0.95 |

## D 场景：五比特码，以及为什么最少是 5

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| d1 | A | The smallest code of all uses five qubits, and its four checks are really one string, X Z Z X I, shifted one place along each time. | 一个 5 格串 X Z Z X I（紫绿绿紫暗）。它向右滑一格、末尾的字母绕回最前面，得到下一行；共四行 | 0.6 |
| d2 | A | Even a mixed check like this one can be measured the same way, with the ancilla sitting between two Hadamards and controlling an X on the first and fourth qubits and a Z on the second and third. | **线路图 4**（混合 check）。第一行 X Z Z X I 拉出线路：5 根数据线、1 根辅助线。辅助线上 H，然后四个受控门，控制点在辅助线上，比特 1、4 上是紫色 X 方块，比特 2、3 上是绿色 Z 方块，比特 5 没有门；再 H、测量表。门的颜色和上面那串字母一格一格对齐，一眼看出线路就是把这串字母竖着画 | 0.6 |
| d3 | A | And now we can finally answer the question from the start, where the trick is just to count the different cases that a syndrome has to tell apart. | 列表缩成第三张小卡片 "five-qubit [[5,1,3]]"。右上角的计分牌 "fewest qubits = ?" 移到画面中央偏上 | 0.6 |
| d4 | A | On n qubits, each qubit can suffer an X, a Y or a Z, which makes three n single-qubit errors, and then there is one more case where nothing went wrong at all. | 左边一列小方块：每个比特三块（X 紫、Y、Z 绿），最上面多一块白色 "no error"。数字 "3n + 1" 在句尾出现（Y 方块的颜色见下面要你定的第 2 条） | 0.6 |
| d5 | A | With one logical qubit you have n minus one checks, and they give two to the n minus one different syndromes, so if every case needs a syndrome of its own, three n plus one can be at most two to the n minus one. | 右边一列空格子，每格是一个 syndrome（一排小灯）；格子数 "2ⁿ⁻¹" 在句中出现。左边的方块一块一块飞进右边的格子，一格一块。最后才写出 3n + 1 ≤ 2ⁿ⁻¹ | 0.45 |
| d6 | B | So let me try. Three qubits gives ten cases, but only four syndromes. | n = 3：10 块飞向 4 格，4 块进去，6 块留在外面，调暗 | 0.35 |
| d7 | A | Right. Four qubits gives thirteen cases and still only eight syndromes, and five gives sixteen cases and exactly sixteen syndromes, so five is the first size that fits, with not a single syndrome left over. | n = 4：13 块、8 格，留 5 块在外面。n = 5：16 块、16 格，全部进去，没有空格。计分牌的 "?" 变成 "5" | **1.1** |
| d8 | B | So my nine was almost twice what we need. | a4 的 "3 × 3 = 9" 小标飞回来，放在 "5" 旁边 | 0.35 |
| d9 | A | It was, but it was a very reasonable nine, since Shor's code was the first one anyone found. And I should be honest that this count assumes every error needs its own syndrome, which Shor's code doesn't bother with, because a Z on qubit one and a Z on qubit two look identical to its checks. | Shor 小卡片放大回来。Z₁ 和 Z₂ 各自落下，第 7 行的灯都是亮橙、第 8 行都是白：两组灯一模一样 | 0.6 |
| d10 | A | That turns out to be harmless, since the two of them multiply to one of the checks, and fixing the wrong one does nothing at all. A different argument shows that even codes like that can't get below five qubits. | Z₁ 和 Z₂ 相乘合成 Z₁Z₂，滑进列表第 1 行，和它重合（8.2 里"什么都没做"的最里层）。Shor 卡片缩回去；计分牌 "5" 旁边加一个小字 "for any code" | 0.95 |

## E 场景：收尾，指向 8.4

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| e1 | A | So a code that fixes any single-qubit error needs a different syndrome for every way one qubit can go wrong, and five qubits turn out to be just enough room for that. | 三张小卡片并排在中央：Shor 9、Steane 7、five-qubit 5；五比特那张下面是 d7 里刚好填满的 16 格 | 0.45 |
| e2 | B | Shor's and Steane's checks were all X's or all Z's, though. Is that a coincidence? | Shor 和 Steane 卡片的 check 列表展开：每一行要么全紫，要么全绿；五比特码的行是紫绿混着的 | 0.35 |
| e3 | A | Not a coincidence at all. In section eight point four we'll see how codes like those two can be built from a pair of classical codes, one for each kind of error. | 标题卡 "Next: 8.4 CSS codes" | 0.95 |

## 自查（对照 `STYLE_3B1B.md` 的清单）

| 项 | 情况 |
|---|---|
| 1 一句话看法 | 有，见文件开头 |
| 2 30 秒内的问题或被纠正的说法 | a3："最少要几个比特？" B 猜 9，a5 说更少 |
| 3 公式前先有画面 | 3n + 1 ≤ 2ⁿ⁻¹ 在方块飞进格子之后才写出（d4）；"7 − 6 = 1" 在六张 check 卡片贴好之后（c3）；\|0_L⟩、\|1_L⟩ 的符号变化先演再说（b9） |
| 4 颜色只代表一件事 | 没有新增颜色。块内的负号用橙色，和"回答 −1"同属"负号" |
| 5 切换还是变形 | 每个码讲完缩成小卡片，D、E 场景再放大或并排；Steane 的圆由表 H 的行变形而来 |
| 6 旁白说的屏幕上都有 | 是 |
| 7 交代省略 | d9、d10 当场坦白"计数假设每个错误要自己的 syndrome"；其余见下面"讲义里有、视频里没放的" |
| 8 结尾回到开头并指向下一段 | 计分牌从 a3 立起，d7 填上 5，d8 回收 B 的猜测；e3 指向 8.4 |
| 9 思考停顿 | 4 处：a3（1.2）、b10（1.1）、c5（1.2）、d7（1.1） |
| 10 提问者 | 9 行，占 10%。a4 猜错（9），在 d7、d8 被推翻；c6 猜对；b10、c9 是意外；d6 是她自己动手算 |
| 11 `check_script.py` | 全部在范围内：平均每句 25.2 词，短句 16%，承接词开头 36%，带 you 20%，带 I 或 we 25%，问句 7% |
| 12 接话接住 | a5 "Well, that's a very natural way to count"（猜错，先承认合理）、b7 "They do."（直接答问题）、b11 "Yes."（直接答她的问题）、c7 "Exactly."（猜对）、c10 "That's it."（她总结对了）、d7 "Right."（她算对了）、d9 "It was, but…"（接她的话）、e3 "Not a coincidence at all."（直接答）。同一场景没有重复的肯定词，肯定词都单独成句 |
| 13 念出来像不像在讲 | 我念不出声音，需要你听 |

先描述后命名：这一节没有新名词，用的都是 8.1、8.2 里的（check、syndrome、logical X / Z、weight）。讲解者说自己的态度：b9（"I found strange"）、d9（"I should be honest"）。

## 讲义里有、视频里没放的

- [[n, k, d]] 的写法只出现在小卡片上，不再解释（8.2 讲过 d）。
- Shor 码的 \|0_L⟩、\|1_L⟩ 在讲义里是第 7 讲的内容，这里在 b9 直接写出，没有重新推导。
- Steane 码的 X⊗7、Z⊗7 逻辑算符没讲。
- Y 错误的 syndrome（两组灯同时亮）没有演示；c10 只说了 X 和 Z。
- 五比特码的 check 互相对易、逻辑算符 X⊗5、Z⊗5 都没讲。
- 计数界对退化码也成立的那个"不同的论证"（量子 Singleton 界，n − k ≥ 2(d − 1)）只在 d9 提了一句，讲义里没有。

## 需要你定的三件事

1. **d10 的 "A different argument shows that even codes like that can't get below five qubits."** 讲义只说"5 是最小的"，没给退化码的论证。这句话是对的（量子 Singleton 界），但讲义里没有出处。保留这句，还是删掉、只说"这个计数假设了每个错误要有自己的 syndrome"？
2. **Y 方块的颜色。** d4 要画 X、Y、Z 三种错误方块，配色表里只有 X 紫、Z 绿。我打算让 Y 是一半紫一半绿（Y 就是 X 和 Z 一起），不新增颜色。可以吗？
3. **开头的人名和年份**（a2 "Peter Shor … in 1995"，c1 "Andrew Steane"）讲义里没有，是我加的，事实没问题。要不要保留？
4. **线路图要不要再多一张？** 现在四张都是"怎么测一个 check"。还可以加一张 Shor 码的编码线路（先用 CNOT 做相位翻转码、再在每块里做比特翻转码，正好对应 a4 B 说的 3 × 3）。讲义第 8 讲没有这张图，会让片子再长约 25 秒。要加吗？
