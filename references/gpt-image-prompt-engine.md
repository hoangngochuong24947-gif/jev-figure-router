# GPT-Image 工业级提示词引擎与模板参考 (gpt-image-prompt-engine)

> **源头背书**：基于 `freestylefly/awesome-gpt-image-2`（530+ 案例逆向工程，20+ 套工业级模板）与 Prompt-as-Code 范式提炼。
> **定位**：`figure-router` 分支四（生成式视觉）与 `document-router`（文档配图）的底层提示词生成规范。

---

## 一、 核心架构：Prompt as Code 原子 Schema

为了保证出图的稳定、可复用与可控性，禁止使用散文式堆砌。所有提示词组装遵循 7 段原子结构：

```text
1. [Subject & Task] 核心主体与任务目标（明确单一主体与核心事件）
2. [Composition & View] 构图与机位（居中/等轴测/中画幅微距/留白空间）
3. [Visual Style & Medium] 艺术媒介与风格（3D Octane渲染/瑞士平面矢量/胶片摄影）
4. [Color Palette & Lighting] 配色系统与光影（低饱和商务色/丁达尔光线/柔和环境光遮蔽）
5. [Materials & Texture] 表面材质与物理纹理（磨砂玻璃/拉丝金属/哑光粘土/细腻颗粒）
6. [Text & Typography Rules] 文字与排版约束（精准声明画面中需渲染的具体汉字/英文与字体版式；或明确声明纯净无文字）
7. [Negative & Collage Guard] 防拼贴与画幅负向硬约束（见第二节）
```

---

## 二、 数量控制与防四宫格硬约束 (Anti-Collage Invariant)

### 1. 痛点根因
ChatGPT / DALL-E 在处理包含“多张图/多个概念”的单次请求时，默认会把画面分割为 **2x2 四宫格、横排拼贴或连环画分屏**，严重破坏画质与可用性。

### 2. 硬性执行规范
1. **单提示词单画幅**：绝对不在单个提示词内提及“多张”或“系列”。必须拆解为独立的候选提示词块（方案 1、方案 2、方案 3）。
2. **强制注入 Anti-Collage 负向锁**：
   ```text
   [Composition Guard]: Single continuous full-bleed scene, single unified camera perspective, strictly no split screen, no collage, no 2x2 grid, no multi-panel, no picture-in-picture, no border frames, no inset thumbnails.
   ```
3. **交互话术提示**：告知用户向 ChatGPT 每次只发送一个提示词块，生成完毕满意后再发送下一个。

---

## 三、 现代生图认知纠偏与红线准则 (Modern Grounding & Anti-Preach Invariants)

### 1. 常见旧认知 vs 现代生图实现冲突核对表 (Legacy Myths vs Modern Reality)

| 维度 | ❌ 淘汰的旧认知 (Legacy Myths) | ✅ 现代实现与标准规范 (Modern Standard) |
| :--- | :--- | :--- |
| **中文字符渲染** | 以为模型无法处理中文、汉字必然乱码严重，强行劝退用户或私自篡改为英文。 | **现代模型全面支持高精度汉字渲染**。海报标题、UI 标签、标牌文字用双引号明确字样（如 `"智算中心"`），明确指定现代黑体/书法楷体等，坚决按需输出。 |
| **提示词语言** | 盲目迷信“提示词必须全翻成英文生图效果才好”。 | **语义与文化对齐优先**。新中式水墨、本土商业/政企、特定文化语境直接输出纯正专业中文 Prompt，避免机翻失真；西式科技/通用国际化场景使用英文装配。 |
| **画幅比例控制** | 盲目输出 Midjourney 专属指令（如 `--ar 16:9`、`--v 6.0`），导致模型误将指令文字画到图上。 | **标准像素与自然语言控制**。在提示词元数据或向 ChatGPT 对话时直接声明尺寸需求（如 16:9 宽屏 `1792x1024`、1:1 正方形 `1024x1024`、9:16 竖屏 `1024x1792`）。严禁输出 `--ar` 语法。 |
| **文字密度与体量** | 走向两个极端：要么无脑全加 `no text`，要么把几百字长篇正文全塞给生图模型。 | **主次分明、字量克制**。生图模型最擅长核心大标题（2~8字）、简短副标、印章和核心 UI 标签；密集说明文字应留白交由排版软件或占位符处理。 |
| **修饰词与负向词** | 疯狂堆砌陈旧垃圾词（`8k, masterpiece, photorealistic, trending on artstation`）或几十行长篇负向词。 | **物理光学参数 + 精准防拼贴锁**。改用真实镜头焦段（`85mm f/1.4`）、真实材质（`subsurface scattering`）、真实光影（`chiaroscuro side rim light`）；负向词仅保留防拼贴锁，严禁长篇无意义堆砌。 |
| **修改与微调逻辑** | 以为模型没有上下文记忆，每次微调必须推倒所有提示词重新盲抽。 | **善用会话上下文与局部重绘 (Inpainting)**。ChatGPT Image 支持在对话中直接指出“保持主体不变，把标题文字改为‘...’”，或点击选区进行局部微调。 |

### 2. 中文字符渲染核心铁律
- **技术事实**：现代生图模型（如 ChatGPT 4o Image / 升级版 DALL-E 3 / Flux 等）早已攻克中文字形渲染，具备出色的汉字排版与笔画渲染能力。无论是常见汉字、专业术语、海报大标题、门头印章还是 UI 中文标签，均能端正准确渲染，**完全不存在“中文必定乱码/严重幻觉/无法出中文字”的技术限制**。
- **严禁自以为是与傲慢说教**：AI 严禁沉溺于 2022~2023 年陈旧的技术偏见中自作多情。**严禁**向用户输出诸如“AI 无法生成中文”、“中文会有严重乱码和幻觉”、“建议改成英文以保证效果”等劝退与爹味说教。
- **严禁擅自篡改用户需求**：当用户明确要求中文海报、中文 UI 标签、中文招牌或指定具体中文字符时，坚决按照用户要求生成包含精准中文文字要求的提示词，**绝对禁止擅自翻译成英文或抹除中文字符**。

### 3. 中文文字与排版提示词装配范式

#### ① 用户要求中文提示词（直接输出纯正地道的全中文 Prompt）
当用户习惯中文交互或明确要求中文提示词时，直接输出高质量全中文 Prompt，将汉字排版要求作为独立字段清晰表达：
```text
【主体与任务】现代企业数字化智能调度中心全景，中央悬浮半透明全息数据大屏。
【构图机位】中心对称构图，宽幅微仰视角，预留顶部呼吸空间。
【艺术风格】高质感 3D 科技拟真渲染，磨砂亚克力与深空深色调。
【光影配色】低饱和极客蓝（#0F172A）底色，主视觉搭配青蓝与琥珀金能量流光。
【文字与排版】中央全息屏正中醒目清晰渲染中文标题：“智能算力调度中心”，字体为现代无衬线粗黑体，笔画规整严谨、字形清晰锐利、无错别字。
【防拼贴约束】单幅全画幅构图，单一机位视角，严禁分屏，严禁四宫格拼图，严禁多面板拼贴，无多余装饰边框。
```

#### ② 英文装配 Prompt 中嵌入中文文字需求（精准双引号界定）
当在英文装配中渲染中文字符时，必须用双引号显式界定具体中文字样，并附带清晰的字体排版修饰词：
```text
[Typography Rules]: Prominently render the exact Chinese characters "智算未来" on the central frosted glass plaque, elegant modern Chinese sans-serif typography, razor-sharp stroke clarity, perfectly legible, bold weight, pristine letterforms.
```

#### ③ “无文字”声明的严格边界（严禁扩大化）
- **仅在以下场景声明无文字**：用户明确表示“纯视觉背景”、“只要干净素材”、“预留后期人工贴字”时，才在负向约束中加入 `no text, no letters, no characters, clean blank surface`。
- **红线**：严禁把“防乱码”偷换为“禁止出中文”；只要画面语义上有文字诉求（如书名、看板、UI、招牌、品牌名），必须按需求实打实输出中文。

---

## 四、 三轴正交风格发散矩阵 (Multi-Style Diversity)

当用户未指定明确风格，或需要为同一文档主题进行多段尝试时，**默认必须提供 2~3 套截然不同的正交视觉风格**：

- **风格 A【工业极简与现代矢量】**：`minimalist clean vector art, flat design with subtle depth, isometric perspective, elegant corporate slate and navy palette, crisp lines, negative space, no clutter`
- **风格 B【高质感 3D 拟真材质】**：`high-end 3D claymation and frosted glass rendering, Cinema 4D Octane style, tactile matte textures, soft diffused volumetric studio lighting, playful yet premium, vibrant accent highlights`
- **风格 C【电影级微距写实摄影】**：`cinematic editorial photography, Hasselblad 85mm f/1.4 lens, dramatic chiaroscuro natural side lighting, realistic physical materials, subtle film grain, emotional atmosphere`
- **风格 D【极客学术蓝图与拓扑】**：`technical blueprint schematic, dark blueprint grid background, glowing cyan and amber data nodes, intricate line-art topology, engineering precision, HUD technical overlays`

---

## 五、 20+ 工业级模板索引速查 (Template Index)

### 1. 界面、信息图与图表类 (UI & Infographics)
- **`ui-screenshot-system` (UI 截图系统)**：
  - *适用*：App 界面、SaaS 仪表盘、移动端功能特写、网页交互。
  - *要点*：锁定平台外壳（iOS/Web）、状态栏、卡片层级与单一高亮按钮；**支持精准中文导航栏与数据标签（如“概览”、“节点集群”、“吞吐率”）**；防泛化白板。
- **`infographic-engine` (信息图引擎)**：
  - *适用*：技术流程图解、时间线、概念知识卡片、模块关系图。
  - *要点*：定义 3-5 个明确模块，用色块与连线体现信息流，精准标注各环节中英文核心概念，严格控制全图文字密度。
- **`scientific-scale-diagram` (科学尺度缩放图)**：
  - *适用*：宏观到微观渐进展示、系统分层切面、技术深度穿透。
  - *要点*：左大右小或层级递进，统一背景色调，防比例失调。
- **`tech-blueprint-schematic` (工业蓝图与网络拓扑)**：
  - *适用*：系统架构、数据流拓扑、硬件原理图、专利示意。
  - *要点*：深蓝或深灰网格底，高精度单像素线稿，发光连接点，专业工程标签。

### 2. 3D、材质与实体拟真类 (3D & Materials)
- **`claymation-3d-scene` (3D 粘土与微缩模型)**：
  - *适用*：产品功能拆解、轻松活泼的概念配图、团队协同卡片。
  - *要点*：哑光粗糙粘土表面，微缩景深，柔和顶部漫射光。
- **`frosted-glass-acrylic` (磨砂亚克力与半透明玻璃)**：
  - *适用*：高端前沿科技、AI 算法黑盒概念、数字资产、企业成果展台。
  - *要点*：次表面散射（SSS）、边缘折射光、悬浮层次感，支持雕刻级中文品牌名/标题。
- **`papercraft-origami-diorama` (多层纸雕立体景深)**：
  - *适用*：生态系统、智慧城市、多层堆栈技术架构。
  - *要点*：明确前中后 4-5 层纸张阴影，哑光水彩纸纹理。
- **`macro-circuit-board` (微距元器件与光路)**：
  - *适用*：算力基础设施、芯片、边缘计算硬件、深科技封面。
  - *要点*：金手指走线、硅晶圆反光、微距浅景深。

### 3. 商业产品与实体摄影类 (Photography & Product)
- **`product-photography` (商业静物产品摄影)**：
  - *适用*：智能硬件实物、工业设备、包装设计、高管汇报。
  - *要点*：单一纯色或水磨石台面，专业影棚柔光箱，85mm 无畸变视角。
- **`editorial-fashion-portrait` (现代专业人物特写)**：
  - *适用*：人物访谈、创始人寄语、用户画像 (Persona)。
  - *要点*：自然眼神光，电影感肤色质感，低对比环境光。

### 4. 艺术概念与风格化表现类 (Artistic & Conceptual)
- **`chinese-watercolor` (新中式水墨意境)**：
  - *适用*：文化科技融合、宏观愿景、留白意境。
  - *要点*：宣纸纹理、浓淡墨晕染、大面积留白，支持印章朱文与书法题跋汉字。
- **`cyberpunk-diorama` (赛博朋克微缩都市)**：
  - *适用*：未来城市、数字孪生、万物互联。
  - *要点*：雨夜地面倒影、蓝紫霓虹对比、微缩模型景深、中英文霓虹招牌。
- **`vintage-botanical-lithograph` (古典生物版画)**：
  - *适用*：生物医药、农业科技、生态保护。
  - *要点*：铜版画排线、泛黄古籍纸张底色、工笔手绘细节。
- **`chalkboard-lecture-diagram` (黑板粉笔手绘板书)**：
  - *适用*：底层算法推导、第一性原理教学、数学机理。
  - *要点*：墨绿黑板质感、粉笔手绘连线与公式、局部擦除痕迹。
- **`retro-pixel-art-screen` (复古 16-bit 像素界面)**：
  - *适用*：开发者工具、游戏化产品、开源社区运营。
  - *要点*：等比例像素网格、有限色彩调色板、CRT 微扫描线。
- **`organic-molecular-crystal` (晶体与微观晶格艺术)**：
  - *适用*：材料科学、化学合成、固态电池、新材料 TOC。
  - *要点*：原子多面体网络、晶面解理反光、无杂乱背景。

---

## 六、 提示词工程六大防坑铁律 (Six Engineering Invariants)

1. **文字排版实事求是（严禁中文乱码偏见）**：现代生图模型完全支持中英文精准文字渲染。关键在于控制文字在画面的体量（以核心标题、关键短语、清晰标签为主），用双引号明确字样；不要因噎废食拒出文字，更**严禁擅自退回全英文或以“中文必然幻觉乱码”为由拒绝用户需求**。
2. **画幅控制严禁 Midjourney 指令**：严禁向 ChatGPT / DALL-E 输出 `--ar 16:9`、`--v 6.0` 等 Midjourney 专属指令。采用自然语言与标准像素声明尺寸需求（横屏 `1792x1024`、竖屏 `1024x1792`、方屏 `1024x1024`）。
3. **剔除无用修饰词与陈旧咒语**：禁止堆砌空泛的垃圾修饰词（如 `hyperrealistic, 8k, photorealistic, masterpiece, ultra HD, trending on artstation` 等），改用明确的物理光学属性（如 `Hasselblad 85mm f/1.4`, `subsurface scattering`, `volumetric softbox studio lighting`, `Cinema 4D Octane render`）。
4. **负向词保持克制，严禁长篇堆砌**：不要从旧 SD 复制几十行无意义负向词。ChatGPT 对负向词具备直接语义解析，过度堆砌会导致反向触发。除防拼贴锁（`strictly no split screen, no collage`）与纯背景无字声明外，不写废话。
5. **主体聚焦，防止多概念过载**：一个画面只聚焦 1 个核心主体（或 1 个高内聚的组件复合体）。超过 5 个散乱无序元素会导致模型语义混淆。
6. **善用会话上下文与局部重绘 (Inpainting)**：在多轮对话中修改细节时，指导用户利用 ChatGPT 的原图局部重绘或针对性上下文反馈（“保持主体不变，把标题文字改为‘...’”），避免每次推倒从零重新抽卡。
