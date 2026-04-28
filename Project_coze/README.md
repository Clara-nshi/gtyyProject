# 多平台AI内容生成工作台 - 项目文档

## 一、项目概述

基于 Coze 智能体 + FastAPI + 精美前端，实现抖音、微信公众号、小红书、CSDN 四大平台的一键AI内容生成。

### 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 智能体平台 | Coze（扣子） | 托管4个工作流的智能体 |
| 后端 | FastAPI + cozepy | Python异步Web框架 + Coze官方SDK |
| 前端 | HTML + Tailwind CSS + marked.js + GSAP | 单文件SPA，CDN引入，无需构建 |
| 动画 | GSAP 3.12.5 + ScrollTrigger | 高性能前端动画库 |
| 通信 | SSE (Server-Sent Events) | 流式响应，实时展示生成进度 |

### 项目结构

```
整合/
├── main.py                  # FastAPI 后端服务
├── index.html               # 前端页面（单文件）
├── lovely.py                # 彩蛋脚本（本地 tkinter 版）
├── 工作流输入输出汇总.md      # 工作流参数文档
├── 项目文档.md               # 本文件
├── music/                   # 背景音乐文件夹
│   ├── 1.mp3
│   └── 2.mp3
├── 抖音/workflow/            # 抖音工作流 YAML
├── 微信公众号/workflow/       # 微信公众号工作流 YAML
├── 小红书/workflow/           # 小红书工作流 YAML
└── csdn/workflow/            # CSDN工作流 YAML
```

### 启动方式

```bash
cd c:\Users\24905\Desktop\项目\coze实战项目\整合
python main.py
# 浏览器打开 http://localhost:8000
```

---

## 二、Coze 智能体配置

| 配置项 | 值 |
|--------|-----|
| API Key | `pat_ML6c35gSfrMlgozQAiAjrUzE4zMi4AdF1LBwa8dyAOc8SYT3tah6i0TU4VNI0g5R` |
| Bot ID | `7633418462655709219` |
| API 基地址 | `https://api.coze.cn` |
| 调用方式 | `coze.chat.stream()` 流式对话 |

### 智能体内包含的4个工作流

| 平台 | 工作流名称 | 工作流ID | 描述 |
|------|-----------|----------|------|
| 抖音 | B_1111111_2 | 7633033660450537491 | 视频流生成 |
| 微信公众号 | T1_wx | 7632339044687003648 | 公众号自动发文基础版改写 |
| 小红书 | xhs_text_generate | 7632308035550003209 | 红薯文本生成 |
| CSDN | szai5_xm01_1 | 7632291301712756763 | 制作带图像的文本 |

### 工作流输入输出详情

#### 1. 抖音 - B_1111111_2（视频流生成）

**开始节点输入：**

| 参数名 | 类型 | 是否必填 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| title | string | ✅ 必填 | - | 标题，例如：羊群效应 |
| vo_type | string | ✅ 必填 | 渊博小叔 | 音色（渊博小叔/邻家女孩/湾湾小何/爽快思思/魅力女友/解说小明/温暖阿虎/少年梓辛） |
| style | string | ✅ 必填 | 黑白 | 颜色风格（彩色/黑白） |
| is_show_img_keywords | boolean | ✅ 必填 | true | 是否展示图片顶部字幕 |
| left_top | string | ❌ 可选 | "" | 左上角注解，如：平台账号昵称 |
| right_top | string | ❌ 可选 | - | 右上角注解，如：个人观点·仅供参考 |
| logo | image | ❌ 可选 | - | Logo图片 |
| text | string | ❌ 可选 | - | 自定义字幕文案 |
| type | string | ❌ 可选 | - | 类型 |

**结束节点输出：**

| 参数名 | 类型 | 来源节点 | 来源路径 | 说明 |
|--------|------|----------|----------|------|
| draft_url | - | 1246796 | Group1 | 草稿URL |
| title | string | 100001(开始节点) | title | 标题（透传输入） |

#### 2. 微信公众号 - T1_wx（公众号自动发文基础版改写）

**开始节点输入：**

| 参数名 | 类型 | 是否必填 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| url | string | ✅ 必填 | - | 文章URL地址 |
| appid | string | ❌ 可选 | - | 微信公众号AppID |
| appsecret | string | ❌ 可选 | - | 微信公众号AppSecret |

**结束节点输出：**

| 参数名 | 类型 | 来源节点 | 来源路径 | 说明 |
|--------|------|----------|----------|------|
| output | string | 136997 | output | 最终输出内容 |

#### 3. 小红书 - xhs_text_generate（红薯文本生成）

**开始节点输入：**

| 参数名 | 类型 | 是否必填 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| topic | string | ❌ 可选 | - | 主题 |
| requirement | string | ❌ 可选 | - | 需求/要求 |

**结束节点输出：**

| 参数名 | 类型 | 来源节点 | 来源路径 | 说明 |
|--------|------|----------|----------|------|
| content | string | 组合输出 | - | 最终内容（文本+图片拼接） |
| ↳ output | string | 1260285 | output | 文本内容部分 |
| ↳ pic | list\<image\> | 168922 | output | 图片列表部分 |

> 输出格式：`{{output}}\n{{pic}}`

#### 4. CSDN - szai5_xm01_1（制作带图像的文本）

**开始节点输入：**

| 参数名 | 类型 | 是否必填 | 默认值 | 说明 |
|--------|------|----------|--------|------|
| topic | string | ❌ 可选 | - | 主题 |

**结束节点输出：**

| 参数名 | 类型 | 来源节点 | 来源路径 | 说明 |
|--------|------|----------|----------|------|
| output | string | 1210335 | output | 最终输出内容 |

---

## 三、后端架构（main.py）

### API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/` | 返回前端页面 index.html |
| POST | `/api/chat` | SSE 流式对话接口 |
| GET | `/music/{file}` | 静态音乐文件路由 |

### 音乐文件服务

```python
from fastapi.staticfiles import StaticFiles

music_dir = Path(__file__).parent / 'music'
if music_dir.exists():
    app.mount('/music', StaticFiles(directory=str(music_dir)), name='music')
```

访问地址：`http://localhost:8000/music/1.mp3`

### 请求参数（POST /api/chat）

```json
{
    "message": "请使用抖音视频流生成工作流，羊群效应",
    "user_id": "web_user",
    "conversation_id": "xxx"  // 可选，多轮对话时传入
}
```

### SSE 响应事件

| type | 说明 | 数据字段 |
|------|------|----------|
| `conversation` | 对话创建，返回会话ID | `conversation_id` |
| `delta` | 增量文本内容 | `content` |
| `done` | 对话完成 | `conversation_id` |
| `error` | 错误信息 | `message` |

### 关键实现细节

1. **多轮对话**：通过 `conversation_id` 实现上下文连续，从 `CONVERSATION_CHAT_CREATED` 事件中尽早获取
2. **流式输出**：使用 `coze.chat.stream()` + `StreamingResponse` 实时推送
3. **会话管理**：`conversation_id` 由后端从 `chunk.chat.conversation_id` 提取，前端保存后下次请求传入

### cozepy ChatEvent 结构

| chunk 属性 | 类型 | 何时有值 | 说明 |
|-----------|------|---------|------|
| `chunk.event` | ChatEventType | 始终 | 事件类型 |
| `chunk.chat` | Chat | 对话类事件 | 包含 conversation_id, status, last_error |
| `chunk.message` | Message | 消息类事件 | 包含 content, role, type |

> ⚠️ ChatEvent 没有 `data` 属性！获取 conversation_id 应使用 `chunk.chat.conversation_id`

---

## 四、前端架构（index.html）

### 页面布局

```
┌────┬─────────────────────────────────────────┐
│    │  Header: Logo + 标题 + 状态灯 + 新对话   │
│ 侧 │─────────────────────────────────────────│
│ 边 │  平台选择: [抖音] [公众号] [小红书] [CSDN] │
│ 栏 │─────────────────────────────────────────│
│    │  统计数字区 (点击开始创作后滚动动画)      │
│ 🎵 │─────────────────────────────────────────│
│ 🌙 │           聊天消息区域                    │
│    │   欢迎页 / 多轮对话消息列表               │
│    │─────────────────────────────────────────│
│    │  输入框 + 发送按钮                        │
└────┴─────────────────────────────────────────┘
```

> 侧边栏包含：Logo、4个平台快捷入口、音乐控制、彩蛋按钮

### 核心功能

| 功能 | 说明 |
|------|------|
| 平台切换 | 4个平台卡片，选中后自动在消息前拼接工作流前缀 |
| 流式对话 | SSE 实时接收，打字机效果 + Markdown 渲染 |
| 多轮对话 | 自动保存 conversation_id，支持上下文连续 |
| 复制按钮 | AI回复悬浮显示，点击复制内容 |
| 新建对话 | 清空消息列表和 conversation_id |
| 背景音乐 | 多首音乐循环播放，控制按钮位于侧边栏 |
| 统计数字 | 点击"开始创作"后触发的数字滚动动画 |
| 彩蛋特效 | 网页版爱心绽放 + 满屏暴击动画 |
| 侧边导航 | 左侧玻璃态导航栏，快捷切换平台 |
| Toast通知 | 右上角通知提示（音乐开关、彩蛋启动等） |

### 平台消息前缀映射

| 平台 | 前缀 |
|------|------|
| 抖音 | `请使用抖音视频流生成工作流，` |
| 微信公众号 | `请使用微信公众号自动发文工作流，` |
| 小红书 | `请使用小红书图文生成工作流，` |
| CSDN | `请使用CSDN技术博文生成工作流，` |

### UI 设计体系

| 设计元素 | 实现 |
|----------|------|
| 字体 | Space Grotesk（UI）+ JetBrains Mono（代码） |
| 配色 | CSS变量系统：6级surface + 3级border + 4色accent |
| 玻璃态 | 3级 glass 效果（blur 24/32/40px） |
| 标题 | 四色渐变流动动画 + Glitch故障闪烁 |
| 气泡 | AI左上尖角 + 用户右上尖角 |
| 输入框 | focus时渐变描边动画 |
| 滚动条 | 紫蓝渐变超细滚动条 |
| 平台卡片 | 3D倾斜 + 光泽反射 + 渐变边框 |
| 发送按钮 | 磁性吸引 + 表面光泽 |

### 背景音乐功能

| 组件 | 说明 |
|------|------|
| 播放列表 | `playlist` 数组定义音乐路径 |
| 控制按钮 | 位于侧边栏，带音乐跳动动画 |
| 状态显示 | 播放时音乐条跳动 + Toast 通知 |
| 自动切换 | 当前曲目播放完毕后自动播放下一首 |
| 循环播放 | 播完最后一首后从头开始循环 |
| 侧边栏同步 | Header按钮和侧边栏音乐图标同步状态 |

**前端实现：**
```javascript
const playlist = ['./music/1.mp3', './music/2.mp3'];
let currentTrack = 0;

function playTrack(index) {
    currentTrack = index % playlist.length;
    bgMusic.src = playlist[currentTrack];
    bgMusic.play();
}

bgMusic.addEventListener('ended', () => playTrack(currentTrack + 1));
```

**添加更多音乐：**
1. 将音乐文件放入 `music/` 目录
2. 在 `playlist` 数组中添加路径

---

## 五、视觉特效

> ⚡ 所有动画已升级为 GSAP 实现，性能更优，动画更流畅

### 1. 粒子背景动画（Canvas）

| 配置项 | 值 | 说明 |
|--------|-----|------|
| PARTICLE_COUNT | 500 | 粒子数量 |
| CONNECTION_DIST | 150 | 连线最大距离 |
| MOUSE_ATTRACT | 80 | 鼠标吸引范围 |
| PARTICLE_COLOR | [139, 92, 246] | 紫色RGB |
| SPEED | 1 | 移动速度 |

**优化点：**
- 距离平方判断（避免不必要的开根号）
- 鼠标交互（粒子跟随鼠标吸引）
- 窗口缩放防抖（100ms）
- 自然边界重置（出界从对侧出现）

### 2. 鼠标特效

| 特效 | 实现 |
|------|------|
| 光标光晕 | 300px紫蓝径向渐变跟随，移出窗口自动隐藏 |
| 彩虹彗星尾迹 | 每25ms生成彩色拖尾粒子，HSL色相随时间0-360°循环变化，带光晕核心和径向渐变外层 |
| 点击涟漪 | GSAP 动画：3层扩散光环 + 中心光爆 + 8颗火花向四周迸射 |

**彩虹彗星尾迹实现细节：**
- `trailHue` 全局变量递增实现彩虹过渡
- 多层 DOM 结构：`.trail-dot` 容器 > `.trail-core` 明亮核心 + `.trail-glow` 径向渐变光晕
- 动画：GSAP 控制 opacity、scale、y 属性，0.8s ease-out

### 3. 环境光效（GSAP）

3个浮动光球（ambient-orb），120px模糊，GSAP 缓动漂浮动画，不同延迟错开。

| 光球 | 动画周期 | 偏移 |
|------|---------|------|
| #1 | 5s | scale: 1→1.05, x: 30, y: -20 |
| #2 | 6s | scale: 0.95, x: -20, y: 30 |
| #3 | 7s | scale: 1.02, x: 20, y: 20 |

### 4. 极光效果（Aurora）

页面顶部3层极光光带，紫/蓝/青三色，使用 `mix-blend-mode: screen` 与背景叠加融合。

| 属性 | 值 |
|------|-----|
| 位置 | 固定定位，top: -50%，覆盖页面上半部分 |
| 模糊 | 60px blur |
| 透明度 | 0.4 |
| 混合模式 | screen |

3层极光分别使用 GSAP 实现漂移 + 旋转 + 缩放动画，错开节奏避免同步。

### 5. 噪点纹理（Noise Grain）

Canvas 实时生成随机噪点，叠加在页面最上层，模拟电影胶片质感。

| 属性 | 值 |
|------|-----|
| 画布尺寸 | 256×256（自动拉伸全屏） |
| 刷新频率 | 100ms |
| 透明度 | 0.025 |
| 混合模式 | overlay |
| z-index | 2（在粒子之上，内容之下） |

实现方式：每100ms重新生成 `ImageData`，填充随机灰度值，`putImageData` 渲染到 Canvas。

### 6. 故障文字（Glitch Text）

标题 "AI Content Studio" 使用 Glitch 故障风格闪烁效果，GSAP Timeline 控制。

- 双层伪元素 `::before` / `::after`，通过 `attr(data-text)` 复制文字
- 每4秒触发一次故障：使用 `clip-path: inset()` 随机切割文字片段 + `translate` 位移抖动
- GSAP Timeline 实现精确的时间控制
- 两层伪元素错开1帧，产生红蓝错位效果

### 7. 3D倾斜卡片（3D Tilt Card）

平台选择卡片跟随鼠标实时3D旋转 + 光泽反射。

| 属性 | 值 |
|------|-----|
| 最大旋转角度 | ±12° |
| 透视距离 | 600px |
| 缩放 | hover时 scale3d(1.03) |
| 过渡 | 0.15s ease-out |

实现逻辑：
1. `mousemove` 计算鼠标相对卡片中心的偏移
2. 将偏移映射为 `rotateX` / `rotateY` 角度
3. 卡片内 `.card-glare` 层显示径向渐变高光，位置跟随鼠标
4. `mouseleave` 时重置变换

### 8. 磁性发送按钮（Magnetic Button）

发送按钮在鼠标靠近60px范围内被磁吸偏移。

| 属性 | 值 |
|------|-----|
| 吸引范围 | 60px |
| 最大偏移 | 8px |
| 缩放 | 吸引时 scale(1.08) |

实现逻辑：
1. 计算鼠标与按钮中心的距离
2. 距离 < 60px 时，按 `(1 - dist/60) * 8` 计算偏移量
3. 按钮向鼠标方向偏移，距离越近吸力越强
4. 同时通过 CSS 变量 `--glare-x` / `--glare-y` 控制按钮表面光泽位置
5. `mouseleave` 时重置

### 9. 统计数字滚动动画

点击"开始创作"按钮后，统计数字从 0 滚动到目标值。

| 配置 | 说明 |
|------|------|
| 触发时机 | 欢迎弹窗关闭时 |
| 缓动函数 | easeOutExpo |
| 动画时长 | 1800ms |
| 小数支持 | data-decimal 属性控制 |

**实现代码：**
```javascript
function animateCounter(el) {
    const target = parseFloat(el.dataset.target);
    const decimal = parseInt(el.dataset.decimal) || 0;
    const duration = 1800;
    // requestAnimationFrame + easeOutExpo 缓动
}
```

### 10. 滚动触发动画（Scroll Reveal）

使用 IntersectionObserver 实现的元素淡入上浮效果。

| 类名 | 效果 |
|------|------|
| `.reveal` | opacity 0→1, y: 30→0 |
| `.reveal-delay-1` | 延迟 100ms |
| `.reveal-delay-2` | 延迟 200ms |
| `.reveal-delay-3` | 延迟 300ms |

### 11. 彩蛋特效（网页版）

纯网页实现的爱心绽放 + 满屏暴击动画，局域网用户都能看到。

**阶段一：爱心绽放**
- 100个彩色方块组成心形曲线
- GSAP 动画：从屏幕中心向外扩散形成心形
- 最后一个方块显示"选我们"

**阶段二：满屏暴击**
- 随机位置弹出彩色提示卡片
- 50%概率显示"为我们投票"
- 5秒后自动关闭或点击/按空格退出

### 12. 背景网格

64px 紫色细线网格背景，增加科技感。

```css
background-image:
    linear-gradient(rgba(139,92,246,0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(139,92,246,0.03) 1px, transparent 1px);
background-size: 64px 64px;
```

### 13. Toast 通知系统

右上角通知提示，3秒后自动消失。

| 样式 | 说明 |
|------|------|
| 背景 | glass 态（blur 16px） |
| 动画 | opacity 0→1, y: -10→0 |
| 时长 | 显示 2.7s，动画 0.3s |

### 14. GSAP 动画库集成

| CDN | 地址 |
|-----|------|
| GSAP Core | `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js` |
| ScrollTrigger | `https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js` |

**已转换的 CSS 动画（全部移除 @keyframes）：**

| 动画名 | 元素 | GSAP 实现 |
|--------|------|-----------|
| orbFloat | 环境光球 | gsap.to() 浮动+缩放 |
| gradientShift | 渐变文字 | gsap.to() 背景位置 |
| auroraDrift | 极光效果 | gsap.to() 移动+旋转 |
| glitch1/glitch2 | 故障文字 | GSAP Timeline |
| msgSlide | 消息滑入 | gsap.fromTo() |
| typingPulse | 打字动画 | gsap.to() 缩放 |
| statusPulse | 状态呼吸 | gsap.to() 透明度 |
| musicPulse | 音乐脉冲 | gsap.to() 缩放 |
| cursorBlink | 光标闪烁 | gsap.to() 步进 |
| welcomeFade | 欢迎弹窗 | gsap.fromTo() |
| iconFloat | 欢迎图标 | gsap.to() 浮动 |
| dotPulse | 分割线点 | gsap.to() 缩放 |
| waveBar | 声波动画 | gsap.to() 逐条 |
| rippleExpand | 点击涟漪 | gsap.fromTo() |
| aiPulse | AI组件脉冲 | gsap.to() 缩放 |
| scanFlicker | 扫描线 | gsap.to() 闪烁 |

### 15. 11层视觉特效总览

页面同时运行11层视觉特效，从底到顶：

| 层级 | 特效 | 技术 |
|------|------|------|
| ① | 粒子网络背景 | Canvas 2D |
| ② | 背景网格 | CSS background |
| ③ | 极光光带 | CSS animation + GSAP |
| ④ | 环境光球 | CSS blur + GSAP |
| ⑤ | 噪点纹理 | Canvas 2D + overlay |
| ⑥ | 光标光晕 | CSS radial-gradient |
| ⑦ | 彩虹彗星尾迹 + 点击涟漪 | DOM + GSAP |
| ⑧ | 3D倾斜卡片光泽 | JS mousemove + CSS |
| ⑨ | 磁性按钮 | JS mousemove + CSS |
| ⑩ | 彩蛋特效层 | DOM + GSAP |
| ⑪ | 背景音乐播放器 | HTML5 Audio |

---

## 六、彩蛋功能（lovely.py）

### 本地 tkinter 版本

`lovely.py` 是本地运行的 tkinter 弹窗彩蛋：

| 特性 | 说明 |
|------|------|
| 爱心绽放 | 100个弹出窗口组成心形曲线 |
| 满屏暴击 | 随机弹出投票提示 |
| 快捷键 | 按空格键立即退出 |

**启动方式：**
```bash
python lovely.py
```

> ⚠️ tkinter 版本只能在运行脚本的本地电脑上显示弹窗，无法在局域网其他电脑上显示

### 网页版彩蛋（index.html 内置）

纯 JavaScript + GSAP 实现的网页版彩蛋，局域网所有用户都能看到。

| 特性 | 说明 |
|------|------|
| 爱心绽放 | 100个 DOM 元素组成心形，GSAP 动画 |
| 满屏暴击 | 随机位置显示彩色卡片 |
| 退出方式 | 点击任意卡片 / 按空格键 / 5秒后自动关闭 |
| Toast 提示 | 启动时显示通知 |

---

## 七、Bug 修复记录

### Bug 1：第二轮对话时第一轮AI回答消失

- **原因**：每条AI回复的内容区域都使用固定的 `id="botMsgContent"`，`getElementById` 找到的是第一轮的元素，内容被覆盖
- **修复**：引入 `msgCounter` 计数器，每条消息分配唯一ID `botMsg_1`、`botMsg_2`...，用 `currentBotMsgId` 变量追踪当前消息

### Bug 2：多轮对话时AI不记得上下文

- **原因**：后端代码使用 `chunk.data.conversation_id`，但 `ChatEvent` 对象没有 `data` 属性，`conversation_id` 从未被正确提取，每次都是新会话
- **修复**：改用 `chunk.chat.conversation_id`，并在 `CONVERSATION_CHAT_CREATED` 事件中尽早获取推送给前端

---

## 七、依赖清单

| 包 | 版本 | 用途 |
|----|------|------|
| fastapi | 0.136.1 | Web框架 |
| uvicorn | 0.46.0 | ASGI服务器 |
| cozepy | 0.20.0 | Coze官方Python SDK |
| pydantic | 2.10.3 | 数据模型验证 |

安装命令：`python -m pip install fastapi uvicorn cozepy`
