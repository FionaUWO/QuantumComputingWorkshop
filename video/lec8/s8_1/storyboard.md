# 8.1 The Pauli group and stabilizers：对话稿 + 分镜（草稿，待确认）

- 状态：草稿，2026-11-23。台词已按你的要求压到约 6 分钟；`script.py` 通过 `check_script.py`；`scene.py` 已写好，低清无声版已渲染（`out/lec8/s8_1/media/videos/scene/480p15/low.mp4`）。还没有配音。
- 这一段要让观众换成的看法：**描述一个量子码，不必列出它的振幅，只要列出它对哪些问题回答"是"。每多一个问题，剩下的空间就砍掉一半。**
- 内容出处：`src/content/lectures/08-stabilizer/01-the-pauli-group-and-stabilizers.mdx`（Nielsen and Chuang 10.5.1）。
- 形式：双人对话。**A** 讲解，**B** 提问。规则见 `video/STYLE_3B1B.md` 第 7、8、9 节。
- 规模：47 行，约 1172 词。A 38 行约 1067 词（48 句，平均每句 22 词）；B 9 行约 105 词，占 9%。脚本里的停顿合计约 31 秒。1.2 节 1139 词成片 5.8 分钟，按同样语速这一节约 6.0 分钟，实际以配音为准。无声版按每分钟 150 词估计每句时长，所以长 8.4 分钟，配音后会缩短。
- "停" 一列：数字是句后的静默秒数，以 `script.py` 的 `PAUSE_AFTER` 为准；**加粗的是思考停顿**，期间画面不出现新信息。
- 前提：观众读过第 7 讲的讲义（bit-flip 码、Z₁Z₂ 和 Z₂Z₃ 两个 check）。第 7 讲目前没有视频，所以 A 场景会把这两样东西重新摆出来，不依赖上一期的画面。

## 大纲

| 场景 | 内容 | 观众带走什么 |
|---|---|---|
| I 片头 | 实验室介绍、标题卡 | |
| A 开场 | 同一个码的两种写法；比特数增加时，一种爆炸，一种只多几行 | 为什么要换一种写法 |
| B 字母表 | I、X、Y、Z 排成一串；一串字母是一个只有 ±1 两种回答的问题 | Pauli 串、Pauli 群 |
| C 两个问题 | 逐格比较，数"冲突"的格数；偶数对易，奇数反对易 | 什么样的问题可以同时问 |
| D 被固定的空间 | 两个串 XX、ZZ 钉住一个 Bell 态 | stabilizer、生成元 |
| E 每问砍一半 | bit-flip 码的两个 check 把 8 维切成 2 维；一般情形 2ⁿ → 2ᵏ；不独立的 check 什么都切不掉 | 维数公式和"独立"这个条件 |
| F 算账 | 50 个比特：约五千比特对 2⁵⁰ 个复数；并非所有态都能这样写 | 这套写法的代价和适用范围 |
| G 收尾 | 被调暗的三格是单比特翻转把码送去的地方 | 引出 8.2 的 syndrome |

## 压到 6 分钟时拿掉的内容（2026-11-23）

- C 场景的三组快速演示，以及"反对易的两个串没有共同的 +1 态"的箭头推导。现在只在 c7 用一句话和一行小字交代结论。
- E 场景的天平（解释为什么每次正好一半）。
- "−I 不能出现在列表里"。
- D 场景里 XX·ZZ = −YY "白送"的那一行。
- F 场景原来分两句的算账并成了一句。

## 配色

沿用 `common.py` 的含义，新增两种用于字母方块。**这两种新用法已经用在草稿里，但还没有写进 `common.py`，等你确认。**

| 颜色 | 只代表 |
|---|---|
| 橙色（ACCENT） | 负号、回答 −1、两个负号相消。和前几节"橙色是负号和抵消"一致 |
| 白色（INK） | 回答 +1、没有出错的东西 |
| 青色（HILITE） | 当前要看的东西：扫描框、切开空间的线、被保留下来的那部分空间、码空间 |
| 暗色（DIM） | 恒等 I 的空格；被切掉的那部分空间（调暗，不删除） |
| 紫色（PURPLE）**新用法** | 字母 X 的方块，以及 X 引起的箭头 |
| 绿色（GOOD）**新用法** | 字母 Z 的方块 |

Y 的方块画成紫绿各半，对应 Y 是 X 和 Z 合在一起。字幕：A 白色，B 青色，和 1.2 相同。

## 运镜总则

- 全片是二维画面，**镜头固定不动**，运动都来自画面里的对象。
- 场景之间是淡出再淡入。草稿里原本设想的"全景缩成角落小窗、之后再放大回来"没有做：F 场景和 G 场景各自重新摆出需要的画面。这样每个场景可以单独渲染和修改。如果你想要小窗的效果，可以再加。
- 场景内部尽量变形而不切换：串变成另一个串、数字变成另一个数字、圈框从一行移到另一行。被排除的东西调暗保留。
- 贯穿全片的组件有两个：**字母方块串**（一行 n 个方块，每格一个字母）和**切线**（一条青色的线划过空间，把回答 −1 的那一半调暗）。

## I 场景：片头

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| i1 | A | Hello everyone, and welcome back. We are QAICON Lab, the Quantum and AI for Computing, Optimization, and Networking Lab, at Western University. | 和 1.2 相同的 logo 小动画，依次出现 "QAICON Lab"、全称、"Western University" | 0.4 |
| i2 | B | And today, we want a much shorter way to write down a quantum code. | logo 缩到左下角；标题卡 "Quantum Computing Workshop / The Pauli group and stabilizers / Lecture 8 · Section 8.1" | 0.95 |

## A 场景：开场，同一个码的两种写法

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| a1 | A | In lecture seven we described the bit flip code in two quite different ways, without making any fuss about it. | 画面中央出现 "bit flip code"，随后缩小上移到顶部；左右各出现一个小标题 "its states" 和 "its questions" | 0.6 |
| a2 | A | The first way was to write out its states, so here are all eight basis states of three qubits, and you can see that the code only ever uses these two. | 左边自上而下列出 \|000⟩ 到 \|111⟩ 八行，每行一根横条；\|000⟩ 和 \|111⟩ 两行亮成青色，其余六行是暗的 | 0.6 |
| a3 | A | The second way was a pair of questions, do the first two bits agree, and do the last two agree, which we wrote as Z Z on one pair and Z Z on the other. | 右边先后出现两行方块：Z Z I 和 I Z Z（Z 绿色，I 是暗色空格），然后两行各闪一下 | 0.6 |
| a4 | A | Now watch what happens to each of these descriptions as I keep adding qubits. | 中间计数 n = 3 → 4 → … → 8，每 0.55 秒跳一格。左边每跳一次行数翻倍，到 n = 5 已冲出画面底部；右边每次只多一行、每行多一格 | 0.45 |
| a5 | B | The left one explodes. But couldn't you just store the amplitudes that aren't zero? | 左边除首尾两行外，其余行淡到几乎看不见 | **1.1** |
| a6 | A | Storing only the ones that aren't zero is a good instinct, but for the codes at the end of this lecture, even those keep doubling as the code grows, while the list on the right just gets a few lines longer. | 左边标题换成 "not zero: 2"，数字依次跳到 4、8、16、32、64，亮着的行随之成倍增加；最后右边的列表被青色框圈住 | 0.6 |
| a7 | A | So in this section, I want to show you how a short list of questions like this one can pin down a quantum state. | 左边振幅柱变暗，右边问题列表闪一下；画面保持到这句说完，下一场景开始时才淡出 | 0.95 |

## B 场景：字母表，一串字母是一个问题

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| b1 | A | Let's start with the alphabet these questions are written in, which has only four letters, the identity and the three Pauli matrices X, Y and Z. | 四个方块依次落下排成一行：I（暗色空格）、X（紫）、Y（紫绿各半）、Z（绿） | 0.6 |
| b2 | A | To act on several qubits you just line the letters up, one for each qubit, so this string means X on the first qubit, nothing on the second, and Z on the third. | 字母表缩小上移。画出三条水平的比特线，编号 1、2、3；X、I、Z 三个方块分别从字母表飞到三条线上；随后比特线淡出，三块并成一行 "X I Z"，旁边写 X₁Z₃ | 0.6 |
| b3 | A | We also allow a sign out in front, and all the strings you can make this way are together called the Pauli group. | 串的最前面多出一个小格，依次翻出 +1、−1、+i、−i、+1（带负号的是橙色）；名词卡 "Pauli group" 在句尾出现 | 0.4 |
| b4 | B | You called them questions, though. How is a string of matrices a question? | 串的上方出现一个青色的 "?" | 0.45 |
| b5 | A | It's a question because each string we'll use has only two possible answers, plus one and minus one. | 名词卡、符号格、字母表和 "?" 淡出；串变形成 Z Z I；右边先后出现两个出口 "answer +1"（白）和 "answer −1"（橙） | 0.6 |
| b6 | A | Take Z Z on the first two qubits, and feed it this state, where the first two bits agree. Each Z turns a one into a minus sign, the two signs cancel, and the answer is plus one. | 串的上方出现 \|1 1 0⟩，每个数字对着一个方块。前两个 1 各自一闪，方块下方各掉出一个橙色 "−"；两个 "−" 靠拢、相撞消失；"+1" 出口闪一下 | 0.6 |
| b7 | A | But here the first two bits disagree, so only one minus sign appears, nothing cancels it, and the answer is minus one. | 数字换成 \|1 0 0⟩：只有第一格掉出一个橙色 "−"，它留在那里；"−1" 出口闪一下 | 0.95 |

## C 场景：两个问题能不能同时问

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| c1 | A | Now, once you have two questions, you need to know whether one state can answer plus one to both, and that comes down to whether the two strings commute. | 清场。画面上只有两个单格方块，上下叠放：X 在上，Z 在下 | 0.6 |
| c2 | A | For a single qubit you already know how this goes, because X followed by Z is minus Z followed by X, and that's what we mean when we say the two anticommute. | 两个方块沿弧线交换上下位置，交换完左边迸出一个橙色 "−"；它落进下方写出的 XZ = −ZX；句尾出现名词卡 "anticommute" | 0.6 |
| c3 | A | For longer strings you compare them slot by slot, and every slot where the two hold different letters, with neither of them the identity, contributes one of these minus signs. | 换成两行五格的串：X Z Z X I 和 I X Z Z X。一个青色竖框从左到右逐格扫过：第 2 格（Z 对 X）和第 4 格（X 对 Z）闪橙色，并各在下方掉出一个 "−"；其余三格不亮 | 0.6 |
| c4 | A | So here's one for you to try. This is X X on two qubits, and this is Z Z on the same two. Do they commute? | 两行换成 X X 和 Z Z，扫描框停在最左边还没开始扫 | **1.3** |
| c5 | B | X and Z don't commute, so I'd say no. | 画面不变，扫描框轻轻闪一下 | 0.35 |
| c6 | A | You're right that X and Z don't commute, but notice that there are two slots here, and each of them gives a minus sign. Those two minus signs cancel, so these strings commute after all. | 扫描框扫过两格，掉出两个橙色 "−"；两个 "−" 相撞消失，原地出现白色的 "commute" | 0.6 |
| c7 | A | And that's the whole rule. An even number of clashing slots means the two strings commute, while an odd number means they anticommute, and then no state at all can answer plus one to both. | 下方依次出现两行规则："even number of clashes → commute"，"odd number of clashes → anticommute"（anticommute 是橙色），最后在第二行右边补上小字 "no state answers +1 to both" | 0.95 |

## D 场景：被一张列表固定的空间

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| d1 | A | So let's take a list of strings that do commute, and collect every state that answers plus one to all of them. | 清场。左侧出现一个列表框，标题 "list"，里面两行：X X 和 Z Z | 0.6 |
| d2 | A | With two qubits there are four basis states, and the question Z Z keeps the two where the bits agree, zero zero and one one. | 右侧排出四格 \|00⟩、\|01⟩、\|10⟩、\|11⟩，每格上方一根振幅柱（高低不同）。列表里的 Z Z 被圈住，一条青色竖线从左扫到右，\|01⟩ 和 \|10⟩ 的柱子降到零、标签调暗 | 0.6 |
| d3 | A | The question X X swaps those two with each other, so answering plus one to it means carrying the same amplitude on both. | 圈住的框移到 X X。\|00⟩ 和 \|11⟩ 上方架起一根紫色双向弧箭头；两根柱子一高一低，对调两次，然后稳定在同样的高度 | 0.45 |
| d4 | B | So that leaves one state. Isn't that the Bell state? | 弧箭头和圈框淡出，只剩两根等高的柱子 | 0.35 |
| d5 | A | Yes, it leaves exactly one state, the Bell state from lecture two, and look at what it took to pin it down, two short strings instead of four amplitudes. | 柱子下方写出 (\|00⟩ + \|11⟩)/√2；随后左边的列表框被青色框圈住 | 0.6 |
| d6 | A | The set of states that a list fixes like this is called the space stabilized by the list, and the list itself, together with all the products of its strings, is called the stabilizer. | 四格上方出现 V_S；稍后圈框淡出，列表的标题从 "list" 变成 "stabilizer S" | 0.6 |
| d7 | A | The strings you actually write down are its generators, and those are the only ones you ever need to check. | 列表下方出现小字 "generators"，两行方块一起闪一下 | 0.95 |

## E 场景：每个 check 把空间砍一半

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| e1 | A | Now we can go back to the bit flip code, and watch its two checks do their work on all eight dimensions of three qubits. | 清场。左边列表框（标题 "checks"）里是 Z Z I 和 I Z Z。中间是 2×2 的格子，每格两个态：左上 \|000⟩ \|111⟩，右上 \|100⟩ \|011⟩，左下 \|001⟩ \|110⟩，右下 \|010⟩ \|101⟩。右边 "dimension" 下面一个大数字 8 | 0.6 |
| e2 | A | The first check, Z Z on qubits one and two, answers plus one on exactly half of them, so it keeps this half, and we can dim the rest. | 列表里 Z Z I 被圈住；一条青色竖线沿格子中线划下；两列上方出现 +1（白）和 −1（橙）；右边一列调暗，数字 8 变成 4 | 0.6 |
| e3 | A | The second check asks about qubits two and three, and it cuts across the first one, so again only half of what's left survives. | 圈框移到 I Z Z；一条青色横线沿格子中线划过；两行左侧出现 +1 和 −1；左下格调暗。数字先不变 | 0.6 |
| e4 | A | So with three qubits and two checks, how many dimensions do you think are left? | 数字 4 变成青色的 "?"，左上格的边框闪一下 | **1.2** |
| e5 | B | Eight, then four, then two. That's one qubit. | 数字依次闪过 8、4、2，停在 2 | 0.35 |
| e6 | A | Yes, two dimensions, which is one qubit's worth of room, and those two are exactly zero zero zero and one one one, the code space we started with. | 左上格亮起青色的底和边框；数字变成 2 = 2¹；格内出现小字 "code space" | 0.6 |
| e7 | A | And the same thing happens for any number of qubits. You start with two to the n dimensions, every new check halves that, and after n minus k checks you're left with two to the k, which is room for k qubits. | 格子下方出现一根长条，右端标 2ⁿ。长条的左半、左四分之一……依次亮起，各自右端标 2ⁿ⁻¹、2ⁿ⁻²、⋯、2ᵏ。全部亮完之后才在右边写出 dim V_S = 2ᵏ | 0.4 |
| e8 | B | Any check at all? What if I add Z on one and Z on three? | 长条和公式淡出。列表下面多出半透明的第三行 Z I Z，列表框随之变高 | 0.45 |
| e9 | A | Good, Z on one and three is a nice one to try, because it's just the product of the two checks we already have, so this cut removes nothing. | 列表里前两行各飞出一份，叠到第三行上，第三行变实。右上格和左下格被橙色框圈了一下（Z₁Z₃ 回答 −1 的正是这两个已经暗掉的格子），框消失，数字 2 闪一下 | 0.6 |
| e10 | A | That's why the count only works for independent checks, where none of them is a product of the others. | 一条橙色横线划掉 Z I Z 这一行；句尾出现名词卡 "independent" | 0.95 |

## F 场景：算账，以及没讲的部分

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| f1 | A | So for fifty qubits, the list is at most fifty strings of fifty letters, which is about five thousand bits, while the amplitudes come to two to the fifty complex numbers, around a million billion. | 清场。顶部 n = 50。右边先出现一块 10×10 的小方块阵（代表 50 行 50 个字母），下面 "≈ 5 000 bits"；左边再长出一根向下冲出画面的长条 "the amplitudes"，中间写 2⁵⁰ ≈ 10¹⁵ | 0.45 |
| f2 | B | So can every state be written as a list like this? | 两者之间的下方出现青色的 "?" | 0.45 |
| f3 | A | No, not every state, and I should be honest about that. Only very special states can be written as a list like this, but they happen to include every code we'll meet in the rest of the lecture. | 清场。画一个大圆角框，左上角标 "all states"；里面亮起一个青色小椭圆，标 "stabilizer states"；椭圆里依次出现四个名字：bit flip、Shor、Steane、surface | 0.95 |

## G 场景：收尾，指向 8.2

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| g1 | A | So a code doesn't have to be handed to you as a table of amplitudes. You can hand over a short list of questions instead. | 清场。回到 E 场景结束时的样子：列表 Z Z I、I Z Z 和 2×2 的格子，左上格亮，其余三格暗 | 0.45 |
| g2 | B | And the three boxes we dimmed, are those just thrown away? | 三个暗格的边框依次闪一下 | **1.1** |
| g3 | A | They're not thrown away at all, and I think that's the best part. Those three boxes are where a single bit flip sends the code, and which box you land in tells you which qubit was flipped. | 三根紫色弧箭头依次从左上格出发：X₁ 从上方绕到右上格，X₂ 穿过格子正中的交点到右下格，X₃ 从左侧绕到左下格。每到一格，那一格恢复亮度，并在格内写出它的两个回答（右上 −1 +1，右下 −1 −1，左下 +1 −1，−1 为橙色） | 0.6 |
| g4 | A | That's what we'll take up next, in section eight point two, where the answers that come back minus one turn into the syndrome. | 格子里所有橙色的 −1 一起闪；然后全部淡出，标题卡 "Next / 8.2 Stabilizer codes" | 0.95 |

## 自查（对照 `STYLE_3B1B.md` 的清单）

| 项 | 情况 |
|---|---|
| 1 一句话看法 | 有，见文件开头 |
| 2 30 秒内的问题或被纠正的说法 | a4 到 a6：两种写法随比特数增长的对比；B 在 a5 提出"只存非零振幅"，a6 纠正 |
| 3 公式前先有画面 | XZ = −ZX 在方块交换迸出负号之后（c2）；dim V_S = 2ᵏ 在长条逐次减半之后（e7） |
| 4 颜色只代表一件事 | 橙色仍然只是负号和 −1；X、Z 方块的紫和绿是新用法，待你确认 |
| 5 切换还是变形 | 场景之间是淡出淡入；场景内部是变形 |
| 6 旁白说的屏幕上都有 | 是 |
| 7 交代省略 | f3 明说不是所有态都能这样写 |
| 8 结尾回到开头并指向下一段 | g1 回到"两种写法"，g4 指向 8.2 |
| 9 思考停顿 | 4 处：a5（1.1）、c4（1.3）、e4（1.2）、g2（1.1）。清单要求四到六处 |
| 10 提问者 | 9 行，占 9%。只提问、猜测、复述；a5 和 c5 是猜错，都被画面推翻 |
| 11 `check_script.py` | 全部在范围内：平均每句 22.2 词，短句 8%，承接词开头 42%，带 you 31%，带 I 或 we 38%，问句 4% |
| 12 接话接住 | 检查工具没有报出未接住的地方 |
| 13 念出来像不像在讲 | 我念不出声音，需要你听 |

先用后命名：Pauli group（b3 句尾）、anticommute（c2 句尾）、stabilizer（d6）、generators（d7）、independent（e10）都在画面演过之后才出现。

压缩后少了一项：原稿 e7 里讲解者说自己的理解过程（"我当初也纳闷为什么正好一半"）随天平一起拿掉了。风格文件要求全片至少一处，现在只剩 g3 的 "I think that's the best part" 和 f3 的 "I should be honest about that" 两处表态。

## 讲义里有、视频里没放的

- **weight**（一个串里非恒等字母的个数）。8.1 讲义里定义了，但要到 8.2 讲码距时才用到，建议放到 8.2 的视频。
- "每个元素平方为 ±I，厄米的那些本征值是 ±1"。视频里只说"我们要用的串只有 ±1 两种回答"。
- Pauli 群有 4ⁿ⁺¹ 个元素这个数字。
- 2n(n − k) 这个一般公式。f1 只给了 n = 50 时的数量级。
- 为什么每个 check 正好留下一半（迹为零）、为什么 −I 不能在列表里、为什么反对易的两个串没有共同的 +1 态。这三条都因为压缩时长拿掉了，讲义里有。

## 需要你定的两件事

1. X 用紫色、Z 用绿色的方块，可以吗？这会成为第 8 讲之后所有视频的固定配色。
2. a6 说"讲到后面的码，非零振幅的个数也会随码的大小不断翻倍"。这对 toric code 是对的，但 8.1 的讲义没有这句话。保留，还是换一个更保守的说法？
