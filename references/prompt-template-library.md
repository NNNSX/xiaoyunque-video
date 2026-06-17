# Prompt Template Library

Use this file to choose one prompt family before drafting non-trivial Xiaoyunque/Seedance prompts. Adapt examples; do not paste long third-party prompt collections verbatim.

## Source Inspiration

- `YouMind-OpenLab/awesome-seedance-2-prompts` is a public collection of Seedance 2.0 prompt examples. Use it as inspiration for prompt structure, categories, and specificity.
- Its README describes Seedance 2.0 as supporting text, image, video, and audio inputs, 4-15 second generation, up to 1080p, and automatic voice/music generation. Treat these as collection notes, not a guaranteed Xiaoyunque account/API contract.
- When browsing the repository for a task, open only the relevant category or example. Record the adapted prompt pattern in project notes when it works.

## Template Families

### cinematic-one-take

Use for continuous camera movement, no hard cuts, parkour, travel-through-space, product reveal, or "一镜到底".

Key fields:
- continuous camera path
- subject path and speed changes
- spatial landmarks
- lighting transition
- no hard cuts
- audio continuity

Skeleton:

```text
一镜到底连续镜头。镜头从 <起点/景别> 开始，沿 <路径> 跟随 <主体>，经过 <空间节点1>、<空间节点2>，最后停在 <终点画面>。动作节奏为 <慢/快/停顿/爆发>，光线从 <A> 平滑过渡到 <B>。全程无硬切、无场景重置、无主体身份变化。音频为 <环境声/音乐/无声>。
```

### multi-shot-story

Use for short drama, narrative ads, multi-beat action, or cases where cuts are allowed.

Key fields:
- numbered shots
- identity continuity across shots
- shot size and camera motion per shot
- transition type
- emotional or story arc

Skeleton:

```text
生成一个多镜头短片。
镜头1：<建立场景和主体>。
镜头2：<关键动作近景>。
镜头3：<结果或冲突升级>。
镜头4：<收尾特写/产品/情绪落点>。
所有镜头保持同一 <主体/服装/产品/场景逻辑>，转场自然，不新增无关角色。
```

### image-to-video-subtle

Use when an input image is already accepted and only needs motion.

Key fields:
- input image is identity/layout authority
- allowed motion is narrow
- preserve background and composition
- forbid redraw drift

Skeleton:

```text
参考图是起始画面和主体身份权威。保持主体外观、服装、场景布局、构图、色彩和画幅不变。只添加 <轻微镜头推进/风吹/眨眼/设备灯光变化/环境运动>。不要重设计场景，不要新增主体，不要改变镜头角度。
```

### start-end-transition

Use when the user supplies first and last frames or wants controlled transformation.

Key fields:
- Image 1 start authority
- Image 2 end authority
- transition path
- fixed identity and spatial logic

Skeleton:

```text
Image 1 是起始帧，Image 2 是结束帧。视频从 Image 1 的画面严格开始，用 <运动/变形/镜头路径> 自然过渡到 Image 2。保持同一主体身份、空间方向、光线逻辑和画幅，不新增无关元素，不突然切换场景。
```

### product-ad

Use for commercial clips, pack shots, cosmetics, food, apparel, devices, and social ads.

Key fields:
- product identity and materials
- macro/hero shot sequence
- background and lighting
- brand text policy
- final pack shot

Skeleton:

```text
高质感产品广告短片。主体产品为 <产品>，材质特征 <玻璃/金属/织物/液体> 必须清晰。镜头从 <微距细节> 开始，经过 <使用场景/材质动态/环境互动>，最后落到 <产品英雄镜头>。光线 <棚拍/自然/霓虹>，背景 <简洁/场景化>。不生成随机文字或错误 logo。
```

### audio-aware-scene

Use when music, ambience, foley, or dialogue is part of the result.

Key fields:
- audio layers
- sync points
- silence/beat changes
- speech/subtitle exactness caveat

Skeleton:

```text
音频是叙事的一部分：背景为 <音乐类型>，环境声为 <环境>，关键动作 <动作> 需要同步 <音效/节拍>。在 <时间/动作节点> 音乐增强或短暂停顿。除非明确要求，不生成字幕和屏幕文字。
```

## Selection Rules

- Pick one primary family. Combining too many families often causes motion drift.
- Adapt templates into content-facing prompts only. Keep provider names, CLI/tool names, route tests, local paths, API/key terms, job ids, and cost notes out of prompt text unless those words must be visible in the video.
- For accepted images, prefer `image-to-video-subtle` over broad cinematic rewriting.
- For exact start/end control, use `start-end-transition` and keep reference count low.
- For multi-reference prompts, bind references by CLI input order: first `--image` is `Image 1`, second `--image` is `Image 2`, etc. Use the same numbering in the prompt template; do not depend on file names as model-visible bindings.
- For high-cost runs, create a job package first and require explicit confirmation before provider submission.
