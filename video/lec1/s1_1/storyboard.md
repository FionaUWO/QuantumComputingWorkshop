# 1.1 From bits to amplitudes：旁白 + 运镜分镜稿（草稿）

- 状态：草稿。2026-11-19 按 `video/STYLE_3B1B.md` 全片改过一遍（配色、先例子后规则、先演后写、屏幕上少放整句），并用新配法全片重新配了音。旁白、语气、停顿都以 `script.py` 为准，改的时候改脚本。
- 规模：64 句，949 词，480p 草稿 6 分 36 秒。
- 内容出处：`src/content/lectures/01-qubit/01-from-bits-to-amplitudes.mdx`（Nielsen & Chuang 1.2 节）。
- 旁白是英文（和网站一致），画面与运镜说明用中文。

## 全片固定元素

| 位置 | 内容 |
|---|---|
| 左上角 | 小字 "1.1 From bits to amplitudes" |
| 右上角 | "谜题徽章"：一个小图标 `H H → ?`。D 场景结束时旁边出现 "coin ✗"，E 场景结束时出现 "amplitudes ✓"，F 场景变成 "→ 1.6" |
| 下方三分之一 | 定义卡片（Probability vector、Stochastic matrix、Amplitude）。卡片在旁白说出名词时才出现 |
| 最底部一条 | 字幕，动画内容不进入这一条 |

配色沿用网站，一种颜色只代表一件事（定义在 `pipeline/common.py`）：

| 颜色 | 只代表 |
|---|---|
| 深紫 `#24123f` | 背景 |
| 淡紫 `#b9a3dc`（实心） | 结果 0，和网站模拟器里的圆点一致。不再用作强调色 |
| 白色空心 | 结果 1 |
| 青色 `#7fd4e6` | 强调：当前要看的东西、新名词、边框、Bloch 球上的状态箭头 |
| 橙色 `#f28c28` | 负号和"抵消"，只在 E 场景出现 |
| 绿色 | 自测题的正确答案、徽章上的对勾 |

## 配音：现在的做法（2026-11-19 起）

- **按段生成**：`script.py` 的 `GROUPS` 把相邻几句编成一段，一段发一次请求，读完再按时间戳切回各句。段内句间的停顿是配音自己读出来的，表里"句后停"一列写"连读"。需要刻意长停顿的句子放在段尾。
- **统一语气**：全片用 `voice.json` 里同一组设置，下面表里的四档"语气"目前不发给配音，只作为试听时的对照说明。
- **语速**：服务自带语速 1.1，后期再加速到原来的总语速。
- **合成时**每句对齐响度，首尾淡入淡出。
- 命令：`python pipeline/build.py 1.1 tts --grouped`。

## 配音：最初的设计（逐句生成，已停用）

三件事一起起作用，都写在脚本里，逐句可改。

| 手段 | 做法 | 在表里的位置 |
|---|---|---|
| 写法口语化 | 用缩写（can't、let's、here's）、对观众说话（"Let's suppose one does"）、短问句、转折词（Now、But look closely）。配音模型是照着句子的写法读的，书面句子读出来就是念稿 | "旁白"列 |
| 句内停顿 | 在句子里写 `‖0.5` 表示这里换气停 0.5 秒。字幕里不显示。全片 31 处，共约 12 秒 | "旁白"列里的 `‖` |
| 句后停顿 | 每句读完后的静音。默认 0.35 秒，场景结尾 1 秒，关键句更长（d8 之后 1.6 秒），自测题之后留 5 秒给观众作答。这部分是合成时加的静音，不花配音额度，也不受加速影响 | "句后停"列 |
| 语气 | 每句四种读法之一：**平稳**、**中性**、**轻快**、**强调**，对应配音服务的两个参数（越"强调"越有起伏）。后面的说明写重音落在哪个词、是什么情绪，供你听的时候对照 | "语气"列 |

情绪走向：A 场景从闲聊开始，到 a6 真正发问；B、C 耐心、轻松；D 认真起来，d8 是全片最重的一句；E 先松一口气，再一步步推到 e13 的"抵消"；之后平稳收尾。

两点要先说明：

- **句内停顿要先试一句**。它靠配音服务的停顿标记实现，我没有在这条流程里用过，需要先拿一句（建议 a5）试听确认有效。如果无效，退路是把那一句拆成两句，用句后停顿代替。
- **读得像不像人，只能你来听**。我听不到声音。流程里可以对任意一句出几种读法让你挑。

运镜用语：**全景** = 画面完整可见；**推近** = 镜头放大到某一部分；**拉远** = 回到全景；**平移** = 镜头横移到相邻内容；**定格** = 画面不动只等旁白读完。

---

## A. 谜题（a1–a7，约 40 秒）

画面分左右两半：左边一枚硬币，右边一个 Bloch 球。每边下方各有一排 100 个小圆点（5 行 × 20 列）。

| 编号 | 旁白（`‖` = 句内停顿，秒） | 语气 | 句后停 | 画面 | 运镜与动画 |
|---|---|---|---|---|---|
| a1 | Flip a fair coin. `‖0.4` You get a random bit. | **平稳**。像在跟人聊天，不要像念稿 | 连读 | 左半：硬币，下方 100 个空点。右半暗着 | 硬币翻转落下。只有第一个点亮起：一次抛掷对应一个点 |
| a2 | Flip it again. `‖0.3` Still random. `‖0.3` Flip it a hundred times, and it never gets easier to predict. | **中性**。Still random 带一点无奈；重音在 never | 0.7 秒 | 同上 | 再抛一次，第二个点亮起；说到"a hundred times"时硬币连翻，整排 100 个点才填满，约一半紫一半白，下方出现计数 |
| a3 | Now, a qubit behaves differently. | **轻快**。Now 之后微顿；differently 上扬，带点卖关子 | 连读 | 0⟩ | 平移到右半，左半变暗但保留在画面边缘 |
| a4 | There is a gate called H. Apply it once, and measuring the qubit is a fair coin flip. | **中性**。H 读清楚；fair coin flip 平着读 | 连读 | 箭头沿弧线从北极摆到赤道上的 \ | +⟩，留下虚线轨迹；下方 100 个点填成一半一半 |
| a5 | Apply it a second time, and `‖0.5` the outcome is certain again. | **强调**。停顿之后带惊讶；重音在 certain | 1 秒 | 第二个 H 方框接在后面 | 箭头沿同一条弧摆回北极；100 个点清空后重新填，这次全是紫色。最后一个点落下时点阵整体轻闪一次 |
| a6 | So where did the randomness go? `‖0.8` That's the question this lecture answers. | **强调**。真的在好奇地发问；第二句放松下来 | 1.2 秒 | 左右两半同时可见，中间一个大问号 | 拉远到全景。左边杂色点阵和右边全紫点阵并排，问号淡入 |
| a7 | In this first section, we show that ordinary probability can't do it. Then we see what quantum theory changes. | **平稳**。交代路线，语速略快 | 1 秒 | 问号缩小飞到右上角，变成谜题徽章 `H H → ?` | 两个半边淡出，只留左上角标题和右上角徽章，画面清场 |

## B. 随机比特（b1–b7，约 35 秒）

| 编号 | 旁白（`‖` = 句内停顿，秒） | 语气 | 句后停 | 画面 | 运镜与动画 |
|---|---|---|---|---|---|
| b1 | Let's start with a bit we're unsure about. | **平稳**。放慢，重新起头，语气亲切 | 连读 | 画面中央一个方框，里面是 "?" | 全景。方框淡入，"?" 在 0 和 1 之间闪动两次 |
| b2 | We describe it with two numbers: the probability that it is zero, `‖0.3` and the probability that it is one. | **中性** | 连读 | 方框下方长出两根柱子，标 0 和 1，高度 p₀、p₁ | 两根柱子依次升起，柱顶各出现 p₀、p₁ |
| b3 | Stack them in a column. `‖0.3` This is a probability vector. | **中性**。probability vector 是新名词，放慢读 | 0.6 秒 | 列向量 (p₀, p₁) | 两根柱子上的 p₀、p₁ 飞到右侧叠成一列，括号合上。下方出现卡片 **Probability vector** |
| b4 | Both numbers are at least zero, and they add up to one. | **中性** | 连读 | 向量旁写 p₀, p₁ ≥ 0 和 p₀ + p₁ = 1 | 两个条件逐条写出，写第二条时两根柱子叠成一根满格的柱子再分开 |
| b5 | For example, a bit that is zero seven times in ten is the vector zero point seven, zero point three. | **轻快**。举例，轻快一点 | 0.35 秒 | 柱子变成 0.7 和 0.3，向量变成 (0.7, 0.3) | 推近到向量。数字从 p₀、p₁ 变成 0.7、0.3，柱子同步变高变矮 |
| b6 | Two vectors are special. E zero means certainly zero. `‖0.3` E one means certainly one. | **中性**。两个 certainly 都重读 | 连读 | 同一组柱子和同一个列向量，变成 e₀ = (1, 0)，再变成 e₁ = (0, 1)；说明文字 "certainly 0"（淡紫）/ "certainly 1"（白） | 不清场。b5 的柱子和向量直接变形：先全在 0，再全在 1，左侧的 p = 同步变成 e₀ =、e₁ = |
| b7 | Every probability vector is a mixture of these two. A fair coin is half of each. | **中性** | 1 秒 | 同一组柱子变成两根等高，向量变成 (½, ½)，左侧 ½ e₀ + ½ e₁ = | 继续变形，不切换画面 |

## C. 操作：矩阵按列读（c1–c11，约 60 秒）

| 编号 | 旁白（`‖` = 句内停顿，秒） | 语气 | 句后停 | 画面 | 运镜与动画 |
|---|---|---|---|---|---|
| c1 | Now let's do something to the bit. Take the NOT gate: `‖0.3` it turns zero into one, and one into zero. | **轻快**。新话题起头；NOT 读清楚 | 0.35 秒 | 画面中央一组柱子 0.7 / 0.3，上方标签 NOT | 先看操作做了什么：两根柱子的高度互换成 0.3 / 0.7。此时还没有矩阵 |
| c2 | To write down what an operation does, we use a matrix. `‖0.4` And here's the trick: read it one column at a time. | **轻快**。像在分享一个小窍门；one column at a time 一词一顿 | 连读 | 柱子缩到左侧保留；中央出现空的 2×2 矩阵 | 矩阵画出后，一条高亮竖带从第一列扫到第二列 |
| c3 | The first column says what happens to a bit that is certainly zero. `‖0.4` The second column, to a bit that is certainly one. | **中性**。前后两句对称 | 0.35 秒 | 第一列上方标 "input: certainly 0"，第二列上方标 "input: certainly 1"；左侧标 "output 0" / "output 1" | 读到哪一列，哪一列高亮，标签随之出现 |
| c4 | For NOT, zero certainly becomes one, so the first column is zero, one. | **中性**。承接上一句，不用重新起头 | 连读 | 矩阵上方标 NOT。旁边小图：0 → 1 | 推近到第一列。箭头 0 → 1 画出，第一列填入 0、1 |
| c5 | One certainly becomes zero, so the second column is one, zero. | **中性** | 0.35 秒 | 小图：1 → 0 | 平移到第二列。箭头 1 → 0 画出，第二列填入 1、0。拉远，NOT 矩阵完整显示后缩到左上方存放 |
| c6 | Now a noisy channel. It flips the bit with a small probability, epsilon. | **轻快**。新例子起头；epsilon 读清楚 | 连读 | 新的空矩阵，标 N_ε。下方一排 12 个结果 0 的圆点 | 圆点出现后，其中一个翻成结果 1 的白圈并闪一下 |
| c7 | A zero stays zero with probability one minus epsilon, `‖0.3` and becomes one with probability epsilon. That is the first column. | **中性**。放慢；one minus epsilon 和 epsilon 对比着读 | 连读 | 分叉图：0 → 0 标 1−ε，0 → 1 标 ε | 推近到第一列。两条分叉依次画出，标签飞入第一列的上下两格 |
| c8 | The second column works the same way. | **平稳**。快速带过，轻松 | 0.35 秒 | 分叉图：1 → 0 标 ε，1 → 1 标 1−ε | 平移到第二列，快速填完 |
| c9 | Each column is itself a probability vector. Matrices like this are called stochastic matrices. | **中性**。stochastic matrices 是新名词，放慢读 | 0.7 秒 | NOT 和 N_ε 并排，每一列外面套一个圆角框 | 拉远。四个列框依次闪一下，各自旁边出现"和为 1"的小勾。下方出现卡片 **Stochastic matrix** |
| c10 | One more example. Throw the bit away, and just flip a fair coin. Both columns are one half, one half. | **轻快**。just flip a fair coin 带一点玩笑感 | 连读 | 第三个矩阵 F。右侧一个写着 0 的方框，随后换成一枚硬币 | 方框向下掉出画面（比特被扔掉），硬币出现并翻转，然后 F 的两列同时填入 |
| c11 | Apply it twice, and nothing changes. `‖0.3` A fair coin, flipped again, is still a fair coin. | **平稳**。still a fair coin 收得平，略带笑意 | 1 秒 | 柱状图 (0.7, 0.3) → F → (0.5, 0.5) → F → (0.5, 0.5) | 平移跟随柱状图从左到右穿过两个 F 方框。第一次柱子被拉平，第二次不变，柱子轻轻一颤后保持原样 |

## D. 为什么硬币做不到（d1–d8，约 50 秒）

本场景是全片的论证核心，画面是一棵从左到右的分支树。

| 编号 | 旁白（`‖` = 句内停顿，秒） | 语气 | 句后停 | 画面 | 运镜与动画 |
|---|---|---|---|---|---|
| d1 | Now for the key question. `‖0.4` Could some stochastic matrix behave like H? | **强调**。认真起来；Could 起调高 | 0.9 秒 | 右上角徽章闪一次；画面中央只有符号 M ≟ H | 不放整句英文，问题由旁白说 |
| d2 | Let's suppose one does. A matrix M turns a certain zero into a fair coin. | **中性**。Let's suppose one does 像在和观众一起试 | 连读 | 树的根："certainly 0"。经过一个 M 方框，分成两支，各标 ½，到达 "0" 和 "1" | 全景。根节点出现，两条分支同时长出 |
| d3 | Apply M a second time. The bit is now zero half the time, and one half the time. | **中性** | 连读 | 两个中间节点后面各接一个 M 方框 | 两个中间节点依次高亮，各显示 "½ of the time" |
| d4 | M acts on each case separately. | **平稳**。放慢，each case separately 读清楚 | 0.6 秒 | 上下两支之间出现一条细分隔线 | 上半支和下半支分别套上淡色底，表示分开处理 |
| d5 | Follow the first case. The bit is zero, and M makes it a fair coin again. `‖0.3` So one quarter of the time, we end at one. | **中性**。重音在 one quarter | 连读 | 上半支：0 再分成两支，各 ½。到达 "1" 的那条路径标 ½ × ½ = ¼ | 推近到上半支。路径"0 → 0 → 1"逐段点亮，终点出现一个实心方块，标 ¼ |
| d6 | Now the second case. And here's the point. `‖0.4` Whatever M does here, it can only add probability. It can never take that quarter away. | **强调**。here's the point 压低放慢；重音在 only add 和 never | 0.8 秒 | 下半支：M 之后是一团灰云，标 "unknown, but ≥ 0" | 平移到下半支。灰云在 0 和任意正值之间来回变形，但从不低于零线 |
| d7 | So outcome one keeps a probability of at least one quarter. | **中性**。重音在 at least | 0.35 秒 | 右侧一根柱子 "probability of 1"，底部是那块 ¼，上面可叠灰云 | 拉远。¼ 方块落入柱底并锁住，灰云只能叠在上面。柱子旁标 "≥ ¼" |
| d8 | Certainty doesn't come back. `‖0.6` Probabilities add. `‖0.5` They never cancel. | **强调**。三个短句一句比一句沉；全片最重的一句 | 1.6 秒 | 整棵树变暗，中央一行字 | 定格。字幕式大字 "Probabilities add. They never cancel." 右上角徽章旁出现 "coin ✗" |

## E. 两处改动（e1–e13，约 85 秒）

顺序是先例子后规则：先看到一个硬币不可能有的向量，再给它起名、再说规则。"平方得概率"用面积演出来，不写公式。

| 编号 | 旁白（`‖` = 句内停顿，秒） | 语气 | 句后停 | 画面 | 运镜与动画 |
|---|---|---|---|---|---|
| e1 | So what does quantum theory do differently? `‖0.5` Surprisingly little. It keeps the same picture: a column of two numbers, acted on by matrices. | **轻快**。换一口气；Surprisingly little 带一点意外 | 0.35 秒 | 左边一个矩阵，右边一个列向量，都是空位 | 旁白一开口轮廓就在屏幕上；说到"same picture"时整体闪一次 |
| e2 | Start with the fair coin: `‖0.3` one half, one half. | **平稳**。平稳，回到熟悉的东西 | 连读 | 左栏：(½, ½)，标 "a fair coin" | 骨架里的空列向量直接变形成硬币的向量，矩阵淡出 |
| e3 | Now here's a qubit. One over root two, `‖0.4` minus one over root two. | **轻快**。重音在 minus，前面微顿；带一点卖关子 | 0.8 秒 | 右栏：(1/√2, −1/√2)，标 "a qubit"，负号橙色 | 先出现上面的数，停一下，再出现带负号的数；负号放大闪一次 |
| e4 | A minus sign. `‖0.4` No probability vector looks like that. That's the first change: the entries may be negative. They're called amplitudes. | **中性**。A minus sign 放慢；amplitudes 是新名词，放慢读 | 连读 | 右栏标题从 "a qubit" 变成青色的 "amplitudes" | 先让硬币的向量闪一下（那边没有负号），旁白说到名字时标题才变形 |
| e4b | They can even be complex, `‖0.3` but real numbers are all we need for now. | **平稳**。顺带一提，轻轻带过 | 0.6 秒 | 下方卡片 **Amplitude** | 卡片升起。这句交代省略：复数先不管 |
| e5 | So what keeps these numbers in check? `‖0.3` Square each one. You get one half, and one half, `‖0.3` and together they make one. | **中性**。问句真的在问；Square each one 干脆；重音在最后的 one | 连读 | 右栏向量下方：每个数长出一个正方形，边长是这个数的大小，面积 ½。结果 0 的是淡紫实心，结果 1 的是白色空心 | 两个数依次落成正方形（负号在这一步消失）。两块面积再变形成两条横板，正好拼满一个单位正方形，旁边出现 "= 1" |
| e6 | That's the second change: the squares must total one, not the numbers themselves. | **中性**。重音在 squares | 0.6 秒 | 同上 | 拼好的单位正方形和 "= 1" 一起闪一次 |
| e7 | Drop the minus sign, and you get another qubit: one over root two, one over root two. Its squares total one as well. | **平稳**。快速带过，轻松 | 0.35 秒 | 中栏：(1/√2, 1/√2)，标 "amplitudes" | 右栏向量复制一份滑到中栏，负号消失。它的两个数同样落成正方形、拼成单位正方形 |
| e8 | One more rule connects amplitudes to what we see. The square of each amplitude is the probability of that outcome. | **中性** | 连读 | 一条规则 "probability of an outcome = square of its amplitude"。中栏、右栏下方是柱状图 | 规则出现后，两栏的面积板各自变形成 0 和 1 两根柱子。面积就是概率，中间没有切换 |
| e9 | So both of these qubits give zero and one half the time each. Measured, each looks exactly like a fair coin. | **中性**。重音在 exactly | 连读 | 三栏下方的柱状图一模一样：都是 ½、½ | 硬币的柱状图淡入，一条水平虚线穿过三组柱顶 |
| e10 | That is what one H produces: a fair coin, as far as a measurement can tell. | **平稳**。as far as a measurement can tell 压低 | 0.35 秒 | 中栏上方出现标签 "what one H gives" | 标签淡入，右上角徽章闪一次，中栏向量闪一次 |
| e11 | But look closely. `‖0.4` The two vectors are different. They differ by a sign. | **强调**。But look closely 压低，像提醒人注意；重音在 different 和 sign | 0.7 秒 | 中栏和右栏下面那个数各套一个框：正的青色，负的橙色 | 两个框同时画出 |
| e12 | A measurement can't see that sign. `‖0.4` A second H can. `‖0.4` It sends the first vector back to certainly zero, and the other to certainly one. | **轻快**。A second H can 短而有力 | 0.35 秒 | 规则换成 "a measurement cannot tell them apart"。之后两栏标题变成 "after a second H"，向量变成 (1, 0) 和 (0, 1) | 先换规则文字并停住；再依次让两个向量变形，柱状图同步变成"全在 0"和"全在 1" |
| e13 | And it works because amplitudes can cancel: `‖0.4` a negative number against a positive one. | **强调**。重音在 cancel；像揭开谜底 | 1.4 秒 | 左侧：+½ 和 −½ 两个小块，负的橙色 | 两个小块相向移动，相撞后消失，留下 0。右上角徽章下的 "coin ✗" 变成 "amplitudes ✓" |

说明：e13 只演示"一正一负相消"这件事本身，不展开两次 H 的完整计算，那是 1.6 节的内容。

## F. 两个世界对照，接下来讲什么（f1–f5，约 30 秒）

| 编号 | 旁白（`‖` = 句内停顿，秒） | 语气 | 句后停 | 画面 | 运镜与动画 |
|---|---|---|---|---|---|
| f1 | Here are the two worlds, side by side. | **平稳**。平稳 | 连读 | 一张两列的表，表头 "Random bit" / "Qubit"，三行空着 | 清场后全景。表格框线画出 |
| f2 | A random bit: two probabilities, changed by stochastic matrices, read by looking. | **中性**。三段并列，节奏均匀 | 连读 | 左列三行依次填入 | 逐行填入，每行填完左侧行名亮一下（State / Operations / Reading it out） |
| f3 | A qubit: two amplitudes, changed by unitary matrices, read by measuring. | **中性**。和 f2 同样的节奏，便于对照 | 0.35 秒 | 右列三行依次填入 | 同上，右列。"unitary" 一词用斜体，表示是新名词 |
| f4 | The next sections take these one at a time: states, measurement, a picture of a qubit, and gates, `‖0.3` which is where unitary matrices get explained. | **中性** | 连读 | 表格缩到上方。下方一条横向路线，五个站点：1.2 States、1.3 Measurement、1.4 The Bloch sphere、1.5 Gates、1.6 Interference | 平移向下。前四个站点随旁白逐个亮起 |
| f5 | Then, in section one point six, we come back to the two H gates, `‖0.3` and watch the cancellation happen. | **轻快**。预告，带期待感 | 1.2 秒 | 第五个站点 1.6 亮起，上方出现谜题徽章 | 推近到 1.6 站点。右上角的徽章飞到站点上方，变成 "→ 1.6" |

## R. 回顾（r0–r3，约 25 秒）

| 编号 | 旁白（`‖` = 句内停顿，秒） | 语气 | 句后停 | 画面 | 运镜与动画 |
|---|---|---|---|---|---|
| r0 | Let's recap. | **平稳**。平稳 | 连读 | 标题 "Recap" | 清场，全景 |
| r1 | One. `‖0.4` A random bit is a probability vector. Operations are stochastic matrices, read column by column. | **中性** | 连读 | 第 1 条要点，配一个小的 (p₀, p₁) 图标 | 要点从左滑入 |
| r2 | Two. `‖0.4` Probabilities only add. So no coin can turn randomness back into certainty. | **中性**。重音在 only add | 连读 | 第 2 条要点，配 ¼ 方块图标 | 同上 |
| r3 | Three. `‖0.4` A qubit holds amplitudes. They can be negative, and their squares total one. | **中性**。重音在 negative | 1 秒 | 第 3 条要点，配橙色负号图标 | 同上 |

## Q. 自测（q0–q3a，约 50 秒）

每题的节奏：问题出现 → 5 秒倒计时条 → 答案以绿色出现。

| 编号 | 旁白（`‖` = 句内停顿，秒） | 语气 | 句后停 | 画面 | 运镜与动画 |
|---|---|---|---|---|---|
| q0 | Three quick questions. Try each one yourself, before the answer appears. | **轻快**。邀请的语气 | 0.35 秒 | 标题 "Check yourself" | 清场，全景 |
| q1 | Question one. Is zero point seven, zero point five a probability vector? | **中性**。疑问上扬 | 5 秒 | 向量 (0.7, 0.5) 和问题文字 | 问题淡入，倒计时条开始缩短 |
| q1a | No. `‖0.4` The entries add up to one point two, not one. | **平稳**。No 干脆 | 0.35 秒 | 0.7 + 0.5 = 1.2 ≠ 1 | 答案绿色淡入，1.2 上画一个小叉 |
| q2 | Question two. What is the second column of the NOT matrix, and why? | **中性**。疑问上扬 | 5 秒 | NOT 矩阵，第二列用问号盖住 | 同上 |
| q2a | One, zero. `‖0.3` An input of one certainly becomes zero. | **平稳**。平稳 | 0.35 秒 | 问号揭开，露出 (1, 0)，旁边 1 → 0 | 第二列高亮 |
| q3 | Question three. Is one half, one half a valid pair of amplitudes? | **中性**。疑问上扬 | 5 秒 | 向量 (½, ½) 和问题文字 | 同上 |
| q3a | No. `‖0.4` The squares add up to one half. One over root two, twice, is the valid pair. | **平稳**。No 干脆 | 1 秒 | ¼ + ¼ = ½ ≠ 1；下方 (1/√2, 1/√2) 打勾 | 答案绿色淡入 |

## Z. 片尾（z1，约 5 秒）

| 编号 | 旁白（`‖` = 句内停顿，秒） | 语气 | 句后停 | 画面 | 运镜与动画 |
|---|---|---|---|---|---|
| z1 | Next up, section one point two: states. | **轻快**。收尾，轻快 | 1 秒 | "Next: 1.2 States" | 淡入，停留，淡出 |

---

## 待你确认的点

1. **读音**：`qubit` 已指定读成 "cubit"，`NOT gate` 读成 "not gate"。`epsilon`、`stochastic`、`unitary` 是否读得对，只能配音后由你听。
2. **A 场景的 100 个点**：和网站模拟器的动画保持一致，这样看过视频再去点按钮是同一个画面。
3. **D 场景的"灰云"**：用来表示"不知道是多少，但不会是负的"。如果觉得抽象，可以换成一个带问号的柱子。
4. **橙色只留给负号和抵消**：全片其他地方不用橙色，让它在 E 场景出现时有分量。
5. **时长**：约 6 分 45 秒，其中停顿约 1 分钟。如果想压到 5 分钟以内，最容易删的是 c6–c8（噪声信道）和 Q 场景的第 2 题。
