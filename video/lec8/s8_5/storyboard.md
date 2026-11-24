# 8.5 The surface code：对话稿 + 分镜（草稿，待确认）

- 状态：草稿，2026-11-24。`script.py` 已写好并通过 `check_script.py`（包括接话检查）；`scene.py` 还没写，没有配音，没有渲染。先确认台词和画面。
- 这一段要让观众换成的看法：**在 surface code 上，一串错误就是网格上的一条路径，check 只看得到它的两个端点。看不见的只有闭合的圈：能缩成一点的圈什么都没做，绕整个环面一圈的才是逻辑错误。所以码要变强，只要把网格做大，每个 check 始终只碰身边四个比特。**
- 内容出处：`src/content/lectures/08-stabilizer/05-the-surface-code.mdx`（Kitaev 2003；Dennis、Kitaev、Landahl、Preskill 2002；Nielsen and Chuang 没有这部分）。
- 形式：双人对话。**A** 讲解，**B** 提问。规则见 `video/STYLE_3B1B.md` 第 7、8、9 节，接话规则见根目录 `VIDEO_WORKFLOW.md`。
- 衔接：8.4 结尾 A 说"8.5 的 surface code，check 只碰平面网格上相邻的四个比特"。8.5 从"之前的码码距都只有 3"开始。
- 用词：按你的意见检查过重复词。出现多的是 checks、qubits、point、grid 这类本节的名词，没有像 exactly 那样反复出现的虚词。
- 规模：34 行，约 980 词。A 27 行约 900 词（平均每句 23.8 词）；B 7 行约 85 词，占 9%。写在脚本里的停顿合计约 23 秒。估计成片 5 分半左右，以配音为准。
- "停" 一列是句后的静默秒数，以 `script.py` 的 `PAUSE_AFTER` 为准；**加粗的是思考停顿**，期间画面不出现新信息。

## 大纲

| 场景 | 内容 | 观众带走什么 |
|---|---|---|
| I 片头 | 实验室介绍、标题卡 | |
| A 开场 | 之前的码码距都是 3；要修更多错误，check 是不是得越变越大？B 说是；A 说 surface code 的 check 永远只碰四个相邻比特 | 一个反直觉的承诺 |
| B 网格和两种 check | 比特在边上，上下、左右粘起来成环面（toric code），n = 2L²；顶点上的 X check、方格上的 Z check；共享 0 或 2 条边所以对易；硬件里每个 check 一个 ancilla、四个 CNOT；两条关系，k = 2 | 码的定义 |
| C 错误是链 | 一串 Z 错误连成路径，只有两端的顶点 check 亮；B 猜整条路都亮，被推翻；X 错误在对偶网格上一样 | syndrome = 链的端点 |
| D 圈 | 闭合的圈没有端点、不触发任何 check；围住一块的圈 = 里面方格 check 的乘积，什么都没做；绕环面的圈是逻辑算符；最短的长 L，所以码距 L，[[2L², 2, L]] | 码变强只要网格变大 |
| E 解码和平面版 | 解码器把亮点两两用最短路径配对；猜错但能缩掉就没事；绕一圈才失败，要约 L/2 个错误排成一行；最小权匹配是多项式时间；切开成平面块，一个逻辑比特，约 d² 个数据比特 | 怎么用、怎么造 |
| F 收尾 | 一句话总结；B 问测 check 的门也会错，加比特真的有用吗？指向 8.6 threshold | |

## 配色

全部沿用 `common.py` 和 8.1 到 8.4 的含义，**不新增颜色**。

| 颜色 | 只代表 |
|---|---|
| 紫（PAULI_X） / 绿（PAULI_Z） | X / Z：顶点上的 X check 画成紫色十字（四条边描紫），方格上的 Z check 画成绿色方框；Z 错误所在的边描绿，X 错误所在的边描紫 |
| 暗色（DIM）、灰（MUTED） | 网格线、比特小点 |
| 橙色（ACCENT） | 亮起的 check（syndrome 里的 1）：顶点或方格中心一个实心橙点；两个负号相消的火花 |
| 白色（INK） | 没亮的 check（空心白圈，只在需要时画出） |
| 青色（HILITE） | 当前要看的东西：围住的那块区域的浅色填充、绕环面那一圈的外发光、ancilla |

## 运镜总则

- 二维画面，镜头固定。甜甜圈用平面画法（你看过三维草稿后定的，2026-11-24）：正方形四边画成对箭头表示粘起来，旁边一个平面的甜甜圈小图标。b2 里网格的一列对应图标上"绕管子"的小圈、一行对应"绕洞"的大圈；d4 里那一行碰到右边界从左边接回来，图标上绕洞的圈亮绿；e5 里图标沿两个圈剪开，变成平面块。
- 贯穿全片的组件：**网格**（L = 6，和讲义 `ToricChains` 一样，右边、下边是虚线表示和对边粘在一起）、**比特点**（每条边中点一个灰色小点）、**错误边**（描绿或描紫的边）、**亮点**（橙色实心点）。
- B 场景的两种 check 是讲义 `ToricChecks` 的动画版；C、D 场景的三种链是讲义 `ToricChains` 图里 (a)(b)(c) 的动画版，位置相同。

## I 场景：片头

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| i1 | A | Hello everyone, and welcome back. We are QAICON Lab, … at Western University. | 和前几节相同的 logo 小动画 | 0.4 |
| i2 | B | And today, we meet the code that most quantum hardware is betting on. | 标题卡 "Quantum Computing Workshop / The surface code / Lecture 8 · Section 8.5" | 0.95 |

## A 场景：开场，check 要越变越大吗

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| a1 | A | Every code we've built so far has distance three, so each one can fix a single error and no more, and a real machine with thousands of qubits is going to need a lot more than that. | 三张小卡片 Shor [[9,1,3]]、Steane [[7,1,3]]、five-qubit [[5,1,3]] 并排，三个 "3" 依次亮青色。下面一排很多比特点，上面零星落下好几个错误方块 | 0.6 |
| a2 | A | So here is a question for you. If we want a code that can fix many errors at once, do you think its checks will have to reach across more and more qubits? | 一个 check（ancilla 点）向下连线到 4 个比特；连线数一下变成 8、再变成 16，越拉越远，最后停在一个青色 "?" 上 | **1.2** |
| a3 | B | I would think so. More errors to catch, so each check has to look at more qubits? | 画面不变 | 0.35 |
| a4 | A | Well, that's what the codes so far would suggest, since Shor's checks already touch six qubits. But the surface code can be made as strong as you like, and every one of its checks still touches just four qubits sitting next to each other. | 先闪一下 Shor 的 X₁…X₆（六连）。然后长连线全部收回，变成一个小十字：一个 check 只连着上下左右四个比特。十字复制铺开成一大片网格 | 0.95 |

## B 场景：网格和两种 check

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| b1 | A | Here's how it's laid out. Draw a square grid, put one qubit on every edge rather than on the points, and then glue the top edge to the bottom and the left edge to the right. | 6×6 网格画出来；每条边的中点长出一个灰色比特点（顶点上没有比特）。上下两条边各画一对单箭头，左右两条边各画一对双箭头（"粘起来"的标准画法）；右边和下边的线变成虚线 | 0.6 |
| b2 | A | That gluing turns the flat sheet into the surface of a doughnut, and it's why this first version is called the toric code. With L squares in each direction, you end up with two L squared qubits. | **三维**：网格离开平面，先把上下两边卷起来对齐，成一根管子；再把管子两端弯过来接上，成甜甜圈。镜头慢慢斜过来、绕半圈，网格线和比特点都贴在环面上。句尾名词 "toric code"。然后回到平面网格（四边保留成对箭头），边上标 L，下面写 n = 2L² | 0.6 |
| b3 | A | At every point where four edges meet, we put an X check on those four edges, and around every little square we put a Z check on the four edges of its border. | `ToricChecks`：一个顶点处的四条边描紫，四个比特点换成紫色 X 方块，标 A_v；一个方格的四条边描绿，四个比特点换成绿色 Z 方块，标 B_f | 0.45 |
| b4 | B | And a point and a square never clash? | 画面不变，A_v 和 B_f 各轻轻闪一下 | 0.35 |
| b5 | A | They don't, because a point and a square either share no edges at all or share two of them, and two clashes cancel, the same even overlap we needed for CSS codes in the last section. | 把那个方格挪到紧挨着顶点的位置：两者共用的两条边框青色，迸出两个橙色 "−" 相撞消失（和 8.4 同一个效果）；再挪到远处，共用 0 条。右上角一个小字 "even ✓" | 0.6 |
| b6 | A | In hardware, each check gets an ancilla of its own placed in the middle of its four qubits, and four CNOTs to its nearest neighbours are all the wiring it needs. | **线路图**：方格中心放一个青色 ancilla 点，四根短线连到四条边上的比特。旁边拉出一张小线路：四根数据线、一根辅助线、四个 CNOT、一个测量表（用 8.3 写的 `Circuit` 组件） | 0.6 |
| b7 | A | Counting is quick. Multiplying every point check together gives nothing, and so does multiplying every square check, so two of the checks aren't independent, and two L squared qubits minus two L squared minus two checks leaves two logical qubits. | 所有顶点同时亮出紫色十字，每条边被描两次，紫色叠两层后消失（每个 X 出现两次抵消）；方格同样一次。然后写出 2L² − (2L² − 2) = 2，最后写 k = 2 | 0.95 |

## C 场景：错误是链，check 只看到端点

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| c1 | A | Now let a few Z errors land on edges that join up into a path, like this chain of four, and think about which point checks will notice. | 清掉 check，回到干净的网格。`ToricChains` (a) 那条链的四条边依次描绿（Z 错误），连成一条折线 | 0.6 |
| c2 | A | Before I light anything up, take a guess. Which checks along this path do you think will fire? | 链上的五个顶点各画一个空心白圈，圈里是灰色 "?" | **1.2** |
| c3 | B | All the ones along the path, I suppose? | 画面不变 | 0.35 |
| c4 | A | Well, that seems natural, since every point on the path touches an error. But a point in the middle of the chain touches two errored edges, and two clashes cancel, so the checks that fire are just the two at its ends. | 中间三个顶点：各迸出两个橙色 "−" 相撞消失，圈变成空心白圈。两端顶点：各只迸出一个 "−"，留下来，圈变成实心橙点 | 0.6 |
| c5 | A | So the syndrome never shows you the chain, it shows you where the chain stops, and the decoder has to work backwards from those endpoints. | 链本身慢慢变淡（"看不见"），只剩两个橙点亮着；两点之间浮出三条不同的灰色虚线路径（都可能是原来那条链） | 0.6 |
| c6 | A | X errors behave the same way on the shifted grid whose points are the centres of the squares, so a chain of X errors lights up two square checks at its ends. | 网格上叠出一层虚线的"对偶网格"（点在方格中心）。一条紫色的 X 错误链横穿几条边，两端的方格中心亮橙点 | 0.95 |

## D 场景：圈

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| d1 | A | And a chain that closes up into a loop has no ends at all, so it trips no check, and that is where the danger is. | 清回 Z 错误。一条链的两端慢慢靠近，接上，变成一个闭合的绿色圈；两端原来的橙点熄灭。画面上没有任何橙点 | 0.6 |
| d2 | A | If the loop just encloses a patch of the grid, it is the product of the square checks inside it, so it did nothing to the encoded state, much like the innermost region from section eight point two. | `ToricChains` (b)：圈围住两个方格，里面浅青填充。两个方格各自的绿色 Z check 方框浮出来，相乘时共用的那条边两次抵消，剩下的外框正好是这个圈。角落小图：8.2 的三层框，最里层 "no effect" 亮一下 | 0.45 |
| d3 | B | And a loop that goes all the way around the doughnut? | 一条绿色的边从网格左边开始，沿一行一直走到右边的虚线边界，停住，青色外发光 | **1.1** |
| d4 | A | A loop around the doughnut is the dangerous one, because it can't be written as a product of checks, so it slips past every test and still changes the encoded state, which makes it a logical operator. | **三维**：画面切回 b2 的三维环面，那一行在环面上是绕甜甜圈一圈的闭合绿线，青色外发光，镜头慢慢转让人看出它真的绕了一圈；环面上所有顶点都没亮。回到平面网格，试着用方格 check 去拼这条线，拼不出来（拼一块就多出边）。标 "logical operator" | 0.6 |
| d5 | A | The shortest loop around the torus has L edges, so the distance is L, and that is the whole trick of this code: to make it stronger, you simply make the grid bigger, and the checks stay the same size. | 绕圈的那行边数一数：1 到 6，写 d = L。然后网格从 6×6 长到 10×10，绕圈那行跟着变长；一个顶点的紫色十字和一个方格的绿框在长大过程中大小不变 | 0.45 |
| d6 | B | So it really is two L squared, two, L. | 写出 [[2L², 2, L]] | 0.35 |
| d7 | A | Right. And that last L is the part I like most, because whether an error is harmless or fatal now comes down to one geometric question, whether its loop can be shrunk to a point. | 左右两幅小图：左边能缩的圈缩成一个点消失，标 harmless；右边绕一圈的线怎么缩也缩不掉，标 logical | 0.95 |

## E 场景：解码，和平面版

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| e1 | A | So how does the decoder work? It's handed a set of lit-up points, and it joins them in pairs with paths that are as short as possible, then applies errors along those paths to cancel them out. | 网格上随机几条短错误链（绿），然后错误本身隐去，只留 6 个橙点。橙点两两之间画出最短的青色路径（配对），沿路径描绿作为修正 | 0.6 |
| e2 | A | If its guess and the real error together form a loop that can be shrunk away, the encoded state comes back untouched, even if the guess took a different route. | 原来的错误链重新显示出来。有一对的修正走了不同的路，错误 + 修正拼成一个小圈，浅青填充，缩成一点消失，打 ✓ | 0.6 |
| e3 | A | It only fails when error and correction together wrap around the torus, and that takes about L over two errors lined up in a row, which gets rare fast as the grid grows. | 一行上排着 3 个错误（L = 6 的一半）；解码器把它们往"另一边"补，补完正好绕环面一圈，青色外发光，打 ✗。旁边写 ≈ L/2 | 0.6 |
| e4 | A | Pairing points with the least total length is a classical matching problem, and there are algorithms that solve it in polynomial time. | 橙点抽象成一张小图：点之间的连线标上距离，粗线是选中的配对；写 "minimum-weight matching · polynomial time" | 0.6 |
| e5 | A | And since nobody builds a doughnut-shaped chip, in practice the torus is cut open into a flat patch with two kinds of boundary, which holds one logical qubit and uses about d squared data qubits for distance d. | **三维**：三维环面沿一圈"剪开"、再沿另一圈剪开，摊平成一块方形网格（b2 的倒放）；左右两边描紫、上下两边描绿（两种边界）。写 "1 logical qubit · d² data qubits"，网格每边标 d | 0.95 |

## F 场景：收尾，指向 8.6

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| f1 | A | So the surface code turns errors into chains, sees only their ends, and fails only when a chain wraps all the way around, which you can push as far away as you like by growing the grid. | 三幅并排的小网格：一条链和两个橙点；一个能缩的圈 ✓；一条绕环面的线 ✗。第三幅的网格往外长大，那条线越拉越长 | 0.45 |
| f2 | B | But every gate that measures those checks can go wrong as well. Does adding more qubits really help? | b6 的小线路图回来，其中一个 CNOT 闪橙色 | 0.35 |
| f3 | A | Adding qubits does help, but only if the hardware is good enough to begin with, and in section eight point six we'll see where that line sits, which is called the threshold. | 标题卡 "Next: 8.6 Thresholds"，下面一条横线，线的一边写 "helps"，另一边写 "hurts" | 0.95 |

## 自查（对照 `STYLE_3B1B.md` 的清单）

| 项 | 情况 |
|---|---|
| 1 一句话看法 | 有，见文件开头 |
| 2 30 秒内的问题或被纠正的说法 | a2："check 要越来越大吗？" B 说是，a4 纠正 |
| 3 公式前先有画面 | n = 2L² 在比特点画出后写；k = 2 在"每条边被描两次抵消"之后写（b7）；d = L 在数完绕圈那行之后写（d5）；[[2L², 2, L]] 在 d6 才写 |
| 4 颜色只代表一件事 | 没有新增颜色。紫 = X、绿 = Z（check 和错误都按这个上色）；橙 = 亮起的 check |
| 5 切换还是变形 | 长连线收回成十字再铺成网格（a4）；链接成圈（d1）；甜甜圈剪开摊平（e5） |
| 6 旁白说的屏幕上都有 | 是 |
| 7 交代省略 | 见下面"讲义里有、视频里没放的" |
| 8 结尾回到开头并指向下一段 | f1 回答 a2 的问题（码靠长大变强，check 不变）；f3 指向 8.6 |
| 9 思考停顿 | 3 处：a2（1.2）、c2（1.2）、d3（1.1） |
| 10 提问者 | 7 行，占 9%。a3 猜错（check 要变大），被 a4、d5 推翻；c3 猜错（整条路都亮），被 c4 推翻；b4、d3 提问；d6 复述；f2 引出下一节 |
| 11 `check_script.py` | 全部在范围内：平均每句 23.8 词，短句 19%，承接词开头 46%，带 you 22%，带 I 或 we 22%，问句 8% |
| 12 接话接住 | a4 "Well, that's what the codes so far would suggest"（猜错，先承认合理）、b5 "They don't"（否定问题直接答）、c4 "Well, that seems natural"（猜错）、d4 "A loop around the doughnut is the dangerous one"（接她的词直接答）、d7 "Right."（她复述对了）、f3 "Adding qubits does help, but…"（接她的词直接答）。同一场景没有重复的肯定词，肯定词都单独成句 |
| 13 念出来像不像在讲 | 我念不出声音，需要你听 |

先描述后命名：toric code（b2）、logical operator（d4 句尾）、threshold（f3 句尾）。讲解者说自己的态度：d7（"the part I like most"）。

## 讲义里有、视频里没放的

- A_v、B_f 的公式只在画面上作标签出现，没有念出 ∏ 的写法。
- "给数学家看的"同调说法（码空间是环面的第一同调群）没有放进视频。
- 两个逻辑比特各自的逻辑 Z、逻辑 X 是哪两个圈：视频只演示了一个方向的绕圈，没有逐一讲两个逻辑比特。
- 平面版"两种边界"只在画面上用颜色区分，没有讲为什么剪开后只剩一个逻辑比特。
- b6 的"每个 check 一个 ancilla、四个 CNOT"讲义里这一节没有，是我加的（8.6 讲义里提到测 check 的线路），配一张线路图，和你在 8.3 想要的线路图辅助教学一致。

## 你已经定的（2026-11-24）

1. b6 的线路图：保留。
2. 甜甜圈：先做了三维，看过配音草稿后改回平面画法（正方形四边画箭头表示粘起来，旁边一个平面的甜甜圈小图标，不做三维旋转）。b2、d4、e5 三个镜头已经按平面画法重做，台词没变。
3. i2 "the code that most quantum hardware is betting on"：可以，不用改保守。

## 原来的三个问题

1. **b6 的线路图**是讲义这一节没有的，我加它是想说明"局部"在硬件上意味着什么，大约 12 秒。保留吗？
2. **甜甜圈怎么画**：我打算不做三维动画，只用"正方形四边画箭头表示粘起来"加一个平面的甜甜圈小图标（符合风格文件"二维内容镜头不动"）。如果你想要一个真的转起来的三维甜甜圈，会多花不少制作时间。用平面画法可以吗？
3. **i2 "the code that most quantum hardware is betting on"**：讲义说它是"建造大型量子计算机的头号候选"，8.6 讲义也说多数硬件路线图围绕它。这个说法可以吗，还是改得更保守一些？
