# 8.2 Stabilizer codes：对话稿 + 分镜（草稿，待确认）

- 状态：草稿，2026-11-23。`script.py` 已写好并通过 `check_script.py`（包括新的接话检查）；`scene.py` 还没写，没有配音，没有渲染。先确认台词和画面。
- 这一段要让观众换成的看法：**check 从来看不到错误本身，只看到它和哪些 check 反对易。所以错误分三类：什么都没做的、被抓到的、和所有 check 都对易却改了编码态的。一个码有多强，就看最轻的那种"看不见的错误"有多重。**
- 内容出处：`src/content/lectures/08-stabilizer/02-stabilizer-codes.mdx`（Nielsen and Chuang 10.5.1、10.5.5）。
- 形式：双人对话。**A** 讲解，**B** 提问。规则见 `video/STYLE_3B1B.md` 第 7、8、9 节，接话规则见根目录 `VIDEO_WORKFLOW.md`。
- 衔接：8.1 结尾停在"三个被调暗的格子是单比特翻转把码送去的地方"。8.2 从那个 2×2 格子直接开始。
- 规模：39 行，约 1060 词。A 31 行约 970 词（41 句，平均每句 23.7 词）；B 8 行约 95 词，占 9%。写在脚本里的停顿合计约 26 秒。估计成片 5 分半到 6 分钟。
- "停" 一列是句后的静默秒数，以 `script.py` 的 `PAUSE_AFTER` 为准；**加粗的是思考停顿**，期间画面不出现新信息。

## 大纲

| 场景 | 内容 | 观众带走什么 |
|---|---|---|
| I 片头 | 实验室介绍、标题卡 | |
| A 开场 | X₁ 被抓到；Z₁ 两个 check 都说 +1，可编码态的符号变了 | check 安静不等于没事 |
| B syndrome | 错误和 check 对易：答案不变；反对易：甩出一个负号，答案变 −1。答案和编码态无关 | syndrome 的定义 |
| C syndrome 会相加 | X₁X₂ 的 syndrome 和 X₃ 一样，解码器补错位置，结果变成 XXX | 两个错误可能被当成另一个 |
| D 三个区域 | S 里（无事）、被检测到、中间区域（逻辑错误） | 逻辑错误、逻辑算符 |
| E 权重和码距 | weight；distance；B 猜 3，实际是 1；乘积规则和可纠正的个数 | [[n, k, d]] 的 d 是什么 |
| F 收尾 | 一句话总结，指向 8.3 | |

## 配色

全部沿用 `common.py` 和 8.1 草稿里的含义，**不新增颜色**。

| 颜色 | 只代表 |
|---|---|
| 橙色（ACCENT） | 负号、回答 −1、syndrome 里的 1 |
| 白色（INK） | 回答 +1、syndrome 里的 0 |
| 青色（HILITE） | 当前要看的东西：码空间、正在讲的那个区域的边框 |
| 暗色（DIM） | 恒等 I 的空格；被调暗的格子 |
| 紫 / 绿 | X / Z 方块（沿用 8.1，还等你确认） |

syndrome 画成一排小灯，每个 check 一盏：亮橙色是 1，白色空心是 0。三个区域只用细线框，讲到哪一个，哪一个的边框变青色。

## 运镜总则

- 二维画面，镜头固定，运动都来自画面里的对象。
- 贯穿全片的组件：8.1 的 2×2 格子（左上是码空间）和它的列表 Z Z I、I Z Z；**错误串**（一行字母方块，从左边飞进来）；**syndrome 灯**（列表每一行右边一盏灯）。
- D 场景的三层嵌套框是讲义里 `ErrorClasses` 那张图的动画版，形状和文字相同。

## I 场景：片头

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| i1 | A | Hello everyone, and welcome back. We are QAICON Lab, … at Western University. | 和 1.2、8.1 相同的 logo 小动画 | 0.4 |
| i2 | B | And today, we find out what a code can actually see when something goes wrong. | 标题卡 "Quantum Computing Workshop / Stabilizer codes / Lecture 8 · Section 8.2" | 0.95 |

## A 场景：开场，一个被抓到的错误和一个没被抓到的

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| a1 | A | At the end of the last section we flipped the first qubit of the bit flip code, and the state moved out to a box where the first check answers minus one, so we knew straight away that something had happened. | 8.1 结尾的 2×2 格子，左上青色；列表 Z Z I、I Z Z 在左边，每行右边一盏灯。错误串 X I I 飞进来，箭头从左上指到右上格；第一盏灯亮橙色 | 0.6 |
| a2 | A | Now let's hit the same qubit with a different error, a Z instead of an X, and ask both checks again. | 箭头和橙灯退回；错误串换成 Z I I | 0.6 |
| a3 | A | This time both checks answer plus one, exactly as if nothing had happened at all. | 两盏灯都是白色；状态留在左上格不动 | 0.45 |
| a4 | B | Hmm, so a Z on one qubit just doesn't bother this code? | 画面不变，左上格轻轻闪一下 | **1.1** |
| a5 | A | Well... it does bother it, quite a lot. If you look at the encoded state, zero zero zero plus one one one has turned into zero zero zero minus one one one, which is a different state, and not one of the checks noticed. | 左上格放大，里面写出 \|000⟩ + \|111⟩；Z₁ 碰到 \|111⟩ 那一项，吐出一个橙色 "−"，"+" 变成 "−"。两盏灯始终白色 | 0.6 |
| a6 | A | So the checks never look at the error itself, they only learn something about it, and the question for us is what exactly they learn, and what can slip past them unseen. | 错误串和两盏灯之间画一道半透明的墙：灯只能看到墙上的影子。整个画面缩到左上角当小窗 | 0.95 |

## B 场景：syndrome

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| b1 | A | Let's start with a state in the code and a single check, which the state answers with plus one, so applying the check just gives the state back. | 中央一根青色箭头代表码里的态；一个 check 方块串 g 作用上去，箭头不变，旁边写 +1（白） | 0.6 |
| b2 | A | Now suppose an error E hits first. If E commutes with the check, you can slide the check straight past it, and the damaged state still answers plus one. | 错误串 E 先作用，箭头转到别处（仍是青色）。g 从 E 的左边滑到右边，滑过时没有火花；回答仍是 +1 | 0.6 |
| b3 | A | But if E anticommutes with the check, sliding past it throws off a minus sign, like the ones we counted last time, and now the damaged state answers minus one. | 换一个 E。g 滑过时迸出一个橙色 "−"（和 8.1 c 场景相同的效果），"−" 贴到箭头上；回答变成 −1（橙） | 0.45 |
| b4 | B | Every time? It isn't random? | 画面不变 | 0.35 |
| b5 | A | Not random at all, no. The answer depends only on the error and the check, and not on which encoded state you started from, which is why we can measure the checks without learning, or disturbing, the information we've stored. | 码空间里换三根不同的箭头，各自被同一个 E 打到；三次都是 −1。最后箭头本身被一层青色的罩子盖住，灯照不进去 | 0.6 |
| b6 | A | So if you write a one for every check that answers minus one, and a zero for every check that answers plus one, you get a short string of bits, which is called the syndrome. | 回到 bit flip 码的列表和两盏灯。橙灯下面写 1，白灯下面写 0；两个数字连成一个小串，句尾出现名词 "syndrome" | 0.6 |
| b7 | A | For the bit flip code, the three single flips give three different syndromes, one zero, one one, and zero one, and that's exactly why the three dimmed boxes could tell them apart. | 小窗里的 2×2 格子放大回来。X₁、X₂、X₃ 依次飞进来，各自的灯是 10、11、01，对应的格子各亮一下，格子上贴上它的 syndrome | 0.95 |

## C 场景：syndrome 会相加

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| c1 | A | Now, here is one for you to try. If qubits one and two both flip at once, what does each check say? | 错误串 X X I 飞进来，停在列表前面；两盏灯变成问号 | **1.2** |
| c2 | B | The first check sees two flips, so they cancel. And the second sees one, so zero one? | 画面不变 | 0.35 |
| c3 | A | Spot on. Each check just counts the minus signs it gets from both errors together, so syndromes add up, with two ones making a zero, the way a parity does. | 第一行 check 碰到两个 X，迸出两个橙色 "−"，相撞消失，灯白；第二行只迸出一个，灯橙。下方竖式：10 + 11 = 01（X₁ 和 X₂ 的 syndrome 相加） | 0.6 |
| c4 | A | But zero one is also the syndrome of a single flip on qubit three, so a decoder that trusts it will flip qubit three, and now all three qubits have been flipped. | 01 指向左下格（X₃ 的格子），一个标 "decoder" 的小手把 X₃ 补上去；错误串变成 X X X | **1.1** |
| c5 | B | Wait, so it lands on one one one? That's the other code word. | 箭头回到左上格。格子里的态写成 α\|000⟩ + β\|111⟩，两根振幅柱一高一低；补完之后两根柱子对调（α、β 不同才看得出变化，所以这里不用等高的柱子） | 0.35 |
| c6 | A | Right. X on all three qubits turns zero zero zero into one one one and back again, it passes both checks, and it isn't a check itself, so the code has quietly been turned into a different encoded state. | 两盏灯都白；X X X 串旁边一个 ✓（过了两个 check）和一个 ✗（不在列表里） | 0.95 |

## D 场景：三个区域

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| d1 | A | So every Pauli error you could name lands in one of three regions, depending on what the checks say about it, and the innermost region is the easiest. | 三层嵌套的圆角框由外向内画出（讲义 `ErrorClasses` 的形状），先不写字 | 0.6 |
| d2 | A | If the error is one of the checks, or a product of them, like Z Z on the first two qubits, then it fixes every state in the code, so it did nothing at all and there's nothing to repair. | 最里层边框变青。Z Z I 落进去，标签 "no effect"、"in S" 在句尾出现 | 0.6 |
| d3 | A | If the error anticommutes with at least one check, the syndrome isn't all zeros, and we say the error is detected, which covers every single flip in the bit flip code. | 最外层边框变青。X I I、I X I、I I X 落进去，各自带着它的橙灯；标签 "detected" | 0.6 |
| d4 | A | And then there is this region in between, the errors that commute with every check without being checks themselves, like the Z on qubit one, or the X on all three. | 中间层边框变青。Z I I 和 X X X 落进去，各带两盏白灯 | 0.45 |
| d5 | B | So those are the ones that change the state and nobody notices. | 中间层轻轻闪一下 | 0.35 |
| d6 | A | Exactly. An error in there passes every test and still changes the encoded state, so it's called a logical error, and the strings that live there are called the logical operators. | 标签 "logical error" 在句中出现，"logical operators" 在句尾出现 | 0.6 |
| d7 | A | I like that the same strings play both parts, because a logical operator applied by accident is a failure, while the same operator applied on purpose is a gate on the encoded qubit. | X X X 一分为二：左边一份贴 "error"，右边一份放进一个小电路里当门，标 X_L | 0.95 |

## E 场景：权重和码距

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| e1 | A | So how strong a code is comes down to how short its shortest logical error is, and we measure a string by counting the letters in it that aren't the identity, which is called its weight. | 中间层里的串排成一列。每个串旁边数出非 I 的方块个数：Z I I → 1，X X X → 3；名词 "weight" 在句尾出现 | 0.6 |
| e2 | A | The smallest weight of any logical error is the distance of the code, and an error lighter than that can never be a logical error, so it is either caught by the checks or does nothing at all. | 一根刻度尺从 0 往上，中间层里最轻的那个串的位置标 d；比 d 轻的那一段整体标 "caught, or harmless" | 0.6 |
| e3 | A | So for the bit flip code, what do you think the distance is? | 刻度尺上的 d 变成 "?"，Z I I 暂时调暗（不让答案先出现） | **1.2** |
| e4 | B | X X X is the logical error, so three? | X X X 移到刻度 3 的位置 | 0.35 |
| e5 | A | Well, that's the natural guess, because it's the logical error we just met. But remember the Z on qubit one from the start, which sits in the same region with a weight of only one, so the distance of this code is one. | Z I I 重新亮起，滑到刻度 1 的位置，"?" 变成 d = 1 | 0.6 |
| e6 | A | And that matches what you saw in lecture seven, where this code could fix any one bit flip but not a general error on a single qubit. | 角落出现一行小字 "[[3, 1, 1]]"，下面两行：bit flip ✓，any single-qubit error ✗ | 0.6 |
| e7 | A | In general, a set of errors can all be corrected as long as no two of them multiply to a logical error, and that is just what went wrong before, since X one X two times X three is X on all three. | 两个错误串 X X I 和 I I X 并排，相乘合成 X X X，落进中间层（青色边框闪） | 0.6 |
| e8 | A | So with distance d, any two errors of weight at most d minus one over two, rounded down, multiply to something lighter than d, and a code of distance d corrects every one of them. | 刻度尺上画两段，各长 ⌊(d−1)/2⌋，首尾相接后仍短于 d。两段都完成后才写出 t = ⌊(d−1)/2⌋ | 0.95 |

## F 场景：收尾，指向 8.3

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| f1 | A | So the checks never see an error itself, only the pattern of which checks it anticommutes with, and a code is only as strong as the lightest error that none of them can see. | 回到 A 场景结尾的墙和影子；中间层的框缩成一个小图标放在旁边 | 0.45 |
| f2 | B | Then can we build a code where every single-qubit error gets caught? | 画面不变 | 0.35 |
| f3 | A | We can, and in section eight point three we'll meet three of them, each with distance three, so any error on a single qubit is not only caught but corrected. | 标题卡 "Next: 8.3 Three codes" | 0.95 |

## 自查（对照 `STYLE_3B1B.md` 的清单）

| 项 | 情况 |
|---|---|
| 1 一句话看法 | 有，见文件开头 |
| 2 30 秒内的问题或被纠正的说法 | a3 到 a5：两个 check 都说 +1，B 以为 Z₁ 没事，a5 纠正 |
| 3 公式前先有画面 | t = ⌊(d−1)/2⌋ 在两段刻度拼完之后才写出（e8）；10 + 11 = 01 在负号相消之后（c3） |
| 4 颜色只代表一件事 | 没有新增颜色。syndrome 的 1 用橙色，和"回答 −1"是同一件事 |
| 5 切换还是变形 | A 结尾缩成小窗，B 结尾放大回来；D 的三个区域由外向内逐层画出 |
| 6 旁白说的屏幕上都有 | 是 |
| 7 交代省略 | 见下面"讲义里有、视频里没放的" |
| 8 结尾回到开头并指向下一段 | f1 回到 A 场景的"墙和影子"，f3 指向 8.3 |
| 9 思考停顿 | 4 处：a4（1.1）、c1（1.2）、c4（1.1）、e3（1.2） |
| 10 提问者 | 8 行，占 9%。a4 和 e4 是猜错，都被画面推翻；c2 猜对 |
| 11 `check_script.py` | 全部在范围内：平均每句 23.7 词，短句 22%，承接词开头 49%，带 you 20%，带 I 或 we 32%，问句 5% |
| 12 接话接住 | 按新规则写的：a5 "Well..."（纠正误解）、b5 "Not random at all, no."（否定句用 no 同意）、c3 "Spot on."（猜对）、c6 "Right."（她的发现）、d6 "Exactly."（她总结对了）、e5 "Well, that's the natural guess"（猜错，先承认合理）、f3 "We can"（直接回答问题）。同一场景没有重复的肯定词，肯定词都单独成句 |
| 13 念出来像不像在讲 | 我念不出声音，需要你听 |

先描述后命名：syndrome（b6 句尾）、detected（d3）、logical error / logical operators（d6）、weight（e1 句尾）、distance（e2）。讲解者说自己的态度：d7。

## 讲义里有、视频里没放的

- 定义里的 [[n, k]] 写法和 "−I ∉ S" 的条件。8.1 已经讲过维数公式；e6 只顺带出现 [[3, 1, 1]] 这个写法，没有逐项解释。
- N(S) 这个记号（normalizer）。视频只说"和所有 check 都对易"，不出现 N(S)。
- 可纠正条件 E_j†E_k ∉ N(S)∖S 的正式写法。e7 用"乘积不是逻辑错误"说了同一件事。
- Z₁ 作为逻辑 Z、XXX 作为逻辑 X 的命名。d7 只给 XXX 标了 X_L。
- 检测能力"权重小于 d 都能发现"在 e2 说了，没有单独演示。

## 需要你定的三件事

1. **c4 到 c6 的"解码器补错"这一段**讲义里没有，是我加的，用来让 e7 的乘积规则有一个具体的例子。它让片子长了约 40 秒。保留，还是删掉、让 e7 直接讲？
2. **e8 的可纠正个数**我只用刻度尺演示了"两个轻错误乘起来仍比 d 轻"，没有讲为什么这就够了（要用到 e7 的乘积规则）。这样够吗，还是 e8 整句删掉，只留到 distance 为止？
3. **a6 的"墙和影子"比喻**会在 f1 再用一次。你觉得这个比喻合适吗？不合适的话，可以只用 syndrome 灯，不画墙。
