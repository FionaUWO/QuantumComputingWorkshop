# 1.2 States：对话稿 + 分镜（草稿，待确认）

- 状态：草稿，2026-11-20。还没有写 `script.py` 和 `scene.py`，没有配音，没有渲染。先确认台词。
- 这一段要让观众换成的看法：**一个量子态是一根长度为 1 的箭头。概率只记得箭头在每个方向上"有多少"，记不住它"指向哪边"；正负号就是方向。**
- 内容出处：`src/content/lectures/01-qubit/02-states.mdx`。
- 形式：双人对话。**A** 讲解，**B** 提问。规则见 `video/STYLE_3B1B.md` 第 7、8 节。
- 规模：53 句，634 词，其中 B 11 句（约 15% 的词数）。加上停顿估计 5 到 6 分钟。
- 2026-11-20 听过 A 场景后的调整：讲解者的停顿偏长，思考停顿改为 1.1 到 1.3 秒，其余停顿不超过 0.45 秒，讲解者加了四处轻微的语气词。下表"停"一列是最初的数值，实际以 `script.py` 为准。背景改为纯黑。声音：Mike 讲解，Alexandra 提问。
- 2026-11-20 第二次调整：你听完全片草稿后觉得讲解者语气怪、台词也怪。对照 3Blue1Brown 原稿后，讲解者的台词按 `STYLE_3B1B.md` 第 9 节全部重写（句子从平均 8 个词变成约 20 个词，接话时先接住提问者的话）。现在讲解者 51 句约 1000 词，提问者 11 句约 100 词，画面和句号没有变。新台词还没有配音。
- "停" 一列：`连` 表示紧接下一句；数字是句后的静默秒数；**加粗的是思考停顿**，期间画面不出现新信息。

## 配色（沿用 1.1）

| 颜色 | 只代表 |
|---|---|
| 淡紫实心 | 结果 0：横轴、|0⟩、0 的概率柱 |
| 白色空心 | 结果 1：纵轴、|1⟩、1 的概率柱 |
| 青色 | 状态箭头和当前要看的东西 |
| 橙色 | 负号和抵消 |

字幕：A 的字幕白色，B 的字幕青色。

## I 场景：片头（2026-11-20 加）

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| i1 | A | Hello everyone, and welcome back. We are QAICON Lab, the Quantum and AI for Computing, Optimization, and Networking Lab, at Western University. | 小动画（你的想法）：白色圆盘里 “AI” 两个字很小、很模糊；紫色的 Q 作为放大镜从右向左移入，罩住它；“AI” 在镜片下放大并变清晰，合成实验室的 logo。然后依次出现 "QAICON Lab"、全称、"Western University" | 0.4 |
| i2 | B | And today, we want to see what the state of a qubit actually looks like. | logo 缩到左下角；标题卡 "Quantum Computing Workshop / States / Lecture 1 · Section 1.2" | 0.9 |

## A 场景：开场，接上一节的悬念

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| a1 | A | Last time, we ended on two columns of amplitudes that differ by nothing but a minus sign in the bottom entry. | 两个列向量并排：(1/√2, 1/√2) 和 (1/√2, −1/√2)，负号是橙色 | 连 |
| a2 | A | And if you square the entries of either one, you get exactly the same thing, a half and a half, fifty-fifty. | 每个向量下面长出两根等高的概率柱，两组一模一样 | 0.5 |
| a3 | B | So if I measure them, I can't tell them apart. | 两组柱子之间出现 "=" | 连 |
| a4 | A | You can't tell them apart, at least not by measuring like this, because either way every result looks like the flip of a fair coin. | "=" 保持 | 0.4 |
| a5 | B | Then are they the same state? | "=" 变成 "?" | **1.8** |
| a6 | A | Well... no. They're not the same state, and seeing why is really the whole point of this section. | "?" 变成 "≠"，橙色负号闪一下 | 0.6 |
| a7 | A | What we need is a picture of a state where that minus sign is something you can actually see. | 柱子淡出，两个列向量留下，移到左侧 | 0.8 |

## B 场景：状态是一根箭头

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| b1 | A | Let's start by drawing two axes, a horizontal one for the outcome zero and a vertical one for the outcome one. | 画出横轴（淡紫，标 0）和纵轴（白，标 1） | 连 |
| b2 | A | A column of two amplitudes is then just a point in this plane, so we can draw an arrow from the origin out to it, like this. | 第一个列向量的两个数分别滑到两条轴上，青色箭头长出来，指向右上 45° | 0.5 |
| b3 | A | Now remember the rule from last time, that the squares of the two amplitudes have to add up to one. | 箭头在两轴上的投影各自长成一个正方形，面积相加，旁边写 "= 1" | 连 |
| b4 | B | That's Pythagoras. So the arrow has length one. | 两个正方形收回，箭头旁标 "1"，箭尖扫出一个单位圆 | 0.6 |
| b5 | A | It is Pythagoras, and it means that every state of a qubit is an arrow of length one, so as the state changes, its tip just moves around this circle. | 箭头沿圆周缓慢转到几个不同位置；右侧两根概率柱跟着联动 | 0.5 |
| b6 | A | Physicists write an arrow like this with an angle bracket around its label, and they call it a ket. | 箭头旁出现 \|ψ⟩；定义卡片 "ket = column vector" | 0.5 |
| b7 | A | The arrow lying along the zero axis is called ket zero, and the one pointing straight up the other axis is ket one. | 箭头先转到横轴，标 \|0⟩ = (1, 0)；再转到纵轴，标 \|1⟩ = (0, 1)；两根基箭头留下变暗 | 0.6 |
| b8 | A | Any other arrow you can build by taking some amount of ket zero, then some amount of ket one, and placing them tip to tail. | 青色箭头回到一般位置，被拆成沿两轴的两段，首尾相接；上方写 α\|0⟩ + β\|1⟩ | 0.5 |
| b9 | A | And when both of those amounts are non-zero, the state is called a superposition. | "superposition" 卡片出现 | 0.4 |
| b10 | B | I've heard that one. It means the qubit is zero and one at the same time, right? | 箭头旁短暂出现两个重影，一个贴横轴一个贴纵轴 | **1.5** |
| b11 | A | Well, zero and one at the same time is how it's usually put, and honestly I think that hides the picture. There is only one arrow here, and it just isn't pointing along either axis. | 重影消失，只剩一根青色箭头，闪一下 | 0.8 |

## C 场景：负号就是方向

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| c1 | A | Now let's go back to those two columns from the start, and draw the first one as an arrow, like this. | 左侧第一个列向量亮起，箭头转到右上 45° | 连 |
| c2 | A | It sits exactly halfway between the two axes, and this particular arrow comes up so often that it has its own name, ket plus. | 箭头旁标 \|+⟩ | 0.4 |
| c3 | A | The second column is the same except for that minus sign on the bottom entry, so before I draw it, where do you think it points? | 第二个列向量亮起，橙色负号闪；箭头还没画 | **1.8** |
| c4 | B | Same distance along zero, but down instead of up? | 第二根箭头长出来，指向右下 45°，纵向那一段是橙色 | 连 |
| c5 | A | Down instead of up, exactly, because the bottom entry is the one that tells you how far to go along the ket one axis. This one is called ket minus. | 标 \|−⟩ | 0.5 |
| c6 | A | Now look over at the bars for these two states, and you'll see they are exactly the same, fifty-fifty both times. | 右侧概率柱：箭头在 \|+⟩ 和 \|−⟩ 之间来回摆，柱子纹丝不动 | 连 |
| c7 | A | But the arrows themselves could hardly be more different. | 两根箭头同时显示，夹角处画出直角标记 | **1.5** |
| c8 | B | Wait, they're at a right angle. | 直角标记加亮 | 连 |
| c9 | A | Yes, they are at a right angle, and that's really the whole point. A probability can never be negative, so a random bit has nowhere to keep this difference, while a qubit keeps it in the direction of its arrow. | 左下角小图：1.1 节的概率向量只能待在第一象限的一条线段上；\|−⟩ 在线段之外 | 0.8 |

## D 场景：内积，一根箭头有多少落在另一根上

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| d1 | B | Is there a way to compute that right angle, without drawing it? | 两根箭头保持，直角标记变成 "?" | 0.5 |
| d2 | A | Definitely, there is a way to compute it, and it comes from asking how much of one arrow lies along the other, like the shadow you see here. | 一根一般箭头向 \|+⟩ 方向投下影子，影子长度随箭头转动而变 | 0.5 |
| d3 | A | When the amplitudes are real numbers, you find that by multiplying the matching entries of the two columns and adding up the results. | 两个列向量并排，对应的数用连线配对，下面写出乘积之和 | 0.4 |
| d4 | A | So try it yourself for ket plus and ket minus, before I fill in the answer. | 写出 ½·(1·1) + ½·(1·(−1))，橙色负号 | **1.5** |
| d5 | B | A half minus a half. Zero. | 两项相撞抵消，剩下 0；影子长度缩到 0 | 连 |
| d6 | A | You're right, a half minus a half, so the overlap is exactly zero, and that is what a right angle means. Two states like that are called orthogonal. | "orthogonal" 卡片；直角标记回来 | 0.6 |
| d7 | A | The way we write an overlap is with a full bracket, where the left half is called a bra and the right half is the ket you already know. | ⟨+\|−⟩ 出现，左半、右半先后高亮；写 ⟨+\|−⟩ = 0 | 0.4 |
| d8 | A | And if you take the overlap of an arrow with itself, you get its length squared, which for a state is always one. | ⟨ψ\|ψ⟩ = 1，箭头自己闪一下 | 0.8 |

## E 场景：换一组坐标轴

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| e1 | A | Now, two arrows of length one at a right angle is all that a pair of axes ever was, so nothing stops us from using these two as our axes instead. | \|+⟩ 和 \|−⟩ 两根箭头延长成一对新的坐标轴，旧坐标轴变暗但保留 | 0.5 |
| e2 | A | In other words, ket plus and ket minus are just as good a basis as ket zero and ket one, and I can turn the whole picture so that they sit level. | 整个画面旋转 45°，新轴变成水平和竖直；旧轴成为斜的暗线 | 0.6 |
| e3 | A | Notice that the arrow itself hasn't moved. Only its coordinates have changed, and each new coordinate is its overlap with one of the new axes. | 青色箭头不动；它在新轴上的两段投影被标为 ⟨+\|ψ⟩ 和 ⟨−\|ψ⟩ | 0.5 |
| e4 | A | So here's a quick check for you. In this new basis, what are the coordinates of ket zero? | 箭头转到 \|0⟩（现在是斜的），两个坐标位置是空框 | **2.0** |
| e5 | B | It sits halfway between them. One over root two, twice. | 两个空框里填入 1/√2 和 1/√2 | 连 |
| e6 | A | Halfway between them, yes, one over root two both times, and the squares still add to one, because the length of an arrow doesn't care which axes you measure it with. | 两个投影长成正方形，面积相加 "= 1"；画面转回原来的方向，正方形换成旧轴上的那一对，仍是 "= 1" | 0.8 |

## F 场景：交代省略的部分，复数

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| f1 | A | Okay, so I owe you a confession. Every arrow I've drawn so far had real numbers for its entries. | 平面缩小到左侧；右侧出现 α、β 两个符号 | 连 |
| f2 | A | In general the amplitudes can be complex numbers, and then each entry is itself a little arrow, sitting in its own disc. | α、β 各变成一个小圆盘，里面一根指针 | 0.5 |
| f3 | B | So a size, and a direction it's turned. | 一个圆盘里指针的长度和转角分别被标出 | 连 |
| f4 | A | A size and a turn, that's exactly it, and here is one example that we'll carry with us through the rest of the lecture. | 写出 \|ψ⟩ = (1/√3)\|0⟩ + ((1+i)/√3)\|1⟩ | 0.4 |
| f5 | A | Its first entry has size one over root three and isn't turned at all, while the second is longer, and turned by forty-five degrees. | 第一个圆盘：短指针指向右；第二个圆盘：较长的指针转到 45° | 0.5 |
| f6 | A | If you square just the sizes you get one third and two thirds, which add up to one, so this really is a state. | 两个圆盘下方长出 1/3 和 2/3 两根概率柱 | 0.6 |
| f7 | A | And that minus sign from before turns out to be the simplest case of all, a pointer turned exactly halfway round. | 第二个圆盘的指针转到 180°，旁边出现橙色 "−" | 0.5 |
| f8 | A | There's one last detail. With complex entries, the bra undoes each turn before multiplying, which is what keeps the overlap of an arrow with itself equal to its length squared. | ⟨ψ\| 一行里的指针相对 \|ψ⟩ 镜像翻转；乘起来都落回正实轴 | 0.8 |

## G 场景：收尾，指向 1.3

| 号 | 谁 | 台词 | 画面 | 停 |
|---|---|---|---|---|
| g1 | A | So a state carries more than a pair of probabilities. It also carries the signs and the turns of its amplitudes, which is why these two arrows are different states. | 回到 \|+⟩、\|−⟩ 两根箭头和它们相同的概率柱 | 0.5 |
| g2 | B | But measuring only showed me the bars. | 柱子加亮，箭头变暗 | **1.5** |
| g3 | A | It only showed you the bars, and that's the question we're left with. How much of the arrow does a measurement actually let us see? | 箭头上盖一个问号 | 连 |
| g4 | A | That's what we'll take up next, in section one point three. | 标题卡 "Next: 1.3 Measurement" | 1.0 |

## 自查（对照 `STYLE_3B1B.md` 的清单）

| 项 | 情况 |
|---|---|
| 一句话看法 | 有，见文件开头 |
| 30 秒内的问题 | a5 "Then are they the same state?" |
| 公式前先有画面 | 归一化（b3 正方形在 "= 1" 之前）、内积（d2 影子在 d3 算式之前）、换基（e2 旋转在 e3 坐标之前） |
| 先用后命名 | ket（b6）、superposition（b9）、orthogonal（d6）、bra（d7）都在画面出现之后 |
| 被纠正的常见说法 | b10 "同时是 0 和 1"，b11 纠正 |
| 交代省略 | f1 明说之前只画了实数 |
| 思考停顿 | 7 处：a5、b10、c3、c7、d4、e4、g2 |
| 提问者 | 11 句，只提问、猜测、复述、惊讶；b10 是猜错 |
| 结尾 | g1 回到开场的两根箭头，g3 指向 1.3 |

## 讲义里有、视频里没放的

- ⟨ψ\|φ⟩ 是 ⟨φ\|ψ⟩ 的共轭，以及"对 ket 线性、对 bra 共轭线性"。属于留给讲义的细节。
- \|±i⟩ 这一对基。f7 之后可以加一句，但会让 F 场景过长；建议留到 1.4 节 Bloch 球时再出现。
- Parseval 这个名字。e6 讲了内容，没有提名字。
