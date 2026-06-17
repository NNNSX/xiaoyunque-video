# Xiaoyunque Video Prompting

Use production video briefs, not keyword piles. Xiaoyunque/Seedance examples benefit from concrete action, camera, timing, lighting, and audio language.

## Prompt Template

```text
视频用途：
生成模式：
画幅/时长：

核心概念：
主体与身份：
场景与时代/地点：
视觉风格：
镜头语言：
动作节拍：
光线与色彩：
音频/音乐/环境声：
字幕/文字：
参考素材角色：
必须保持：
禁止项：
验收标准：
```

Delete fields that do not apply. For English output, keep the same structure in English.

Do not include model choice, route, CLI command, cost confirmation, or API/key status in the final prompt. Store those as job metadata and CLI parameters.

## Prompt Privacy And Relevance

The final prompt sent to Xiaoyunque/Seedance is content-facing. It should describe the requested video, not the execution environment.

Keep these in `job.json`, `submit_notes.md`, `review.md`, project briefs, or the user-facing report instead of the model prompt:

- provider/tool names used only for execution, such as Xiaoyunque, Pippit, Seedance, CLI, provider, skill, API, key, token, thread id, run id, job id, route, or local command details
- testing or validation labels, such as model test, connectivity test, route verification, reference-order test, or cost experiment
- local paths, account details, internal document names, private project labels, and billing/credit notes

Use `视频用途` for the viewer/content purpose, not the operator purpose. If the run is technically a test, translate it into the video-facing form:

- Bad: `小云雀/Seedance 三参考图顺序绑定有效性测试`
- Bad: `用于验证 seedance2.0_vision 1080p 图生视频能力`
- Good: `城市战术态势三帧过渡短片`
- Good: `车辆与无人机编队公路追踪短片`
- Good: `产品广告短片`

Only mention provider/model/tool words when they must appear visibly in the generated video, such as a UI demo about that exact product.

## Field Guidance

- `视频用途`: state the content-facing use, such as storyboard keyframe animation, product ad, immersive short, one-take action, social clip, short drama, music video, or visual transition clip. Do not write operator-facing labels such as provider test, CLI test, model validation, reference-order test, or route verification.
- `生成模式`: use labels such as text-to-video, image-to-video, start/end-frame transition, one-take, multi-shot short, reference-style video, or viral-replication analysis.
- `画幅/时长`: specify `16:9`, `9:16`, `1:1`, `3:4`, or another target. If duration is unknown, describe beat density instead of inventing a duration.
- `主体与身份`: list characters/products/vehicles and their stable identity traits. For repeated characters, name them consistently.
- `镜头语言`: specify shot size, camera path, lens feel, pan/tilt/dolly/steadicam/handheld/drone, and whether cuts are allowed.
- `动作节拍`: write chronological beats. For one-take clips, emphasize continuous motion and no hard cuts.
- `音频`: mention background music, ambience, foley, dialogue, or silence only when needed.
- `字幕/文字`: put exact on-screen text in quotes. If exact text matters, keep it short and expect a review pass.

## Reference Binding

When using repeated CLI reference inputs, bind them by input order in the prompt. The first `--image` is `Image 1 / 第一张参考图`, the second is `Image 2 / 第二张参考图`, and so on. Do not rely on file names for model binding; use file names only as human-facing safeguards.

For each reference, write its ordered identity and role:

```text
参考素材角色：
Image 1 / 第一张参考图：起始帧和主体身份权威。
Image 2 / 第二张参考图：结束帧和目标构图权威。
Image 3 / 第三张参考图：风格参考，只继承光线和色彩，不继承构图。
```

The CLI argument order must match the prompt numbering:

```bash
--image image-01-start-frame.png \
--image image-02-end-frame.png \
--image image-03-style.png
```

## Good Prompt Patterns

### One-Take

```text
一镜到底，不能硬切。镜头从低角度贴地推进，跟随主体穿过场景；速度先慢后快，中间有一次平滑绕身，最后稳定停在主体正面。所有动作连续发生，光线变化自然过渡。
```

### Multi-Shot

```text
镜头1：中景建立环境和主体。
镜头2：近景展示关键动作，保持同一主体服装和脸部特征。
镜头3：广角展示动作结果，镜头运动从左向右平滑跟随。
镜头4：特写收尾，主体看向镜头，背景保持同一地点。
```

### Image-To-Video

```text
参考图是起始画面和主体身份权威。保持主体外观、服装、场景布局、色彩和画幅不变。只让镜头轻微推进，主体做一个自然的小动作，背景只有轻微环境运动。
```

### Start/End Transition

```text
Image 1 是起始帧，Image 2 是结束帧。前半段严格从 Image 1 开始，后半段自然过渡到 Image 2。过渡过程保持同一主体身份、同一空间逻辑和连续光线，不新增无关角色。
```

## Avoid List

Use narrow negatives that target likely video failures:

- no extra characters or duplicate subjects
- no sudden hard cuts unless requested
- no warped hands/faces/limbs
- no identity change between shots
- no random text, watermark, logo, UI, subtitles
- no flickering geometry or melting objects
- no camera teleportation unless requested
- no scene reset between beats

## Review Checklist

Mark each item `pass | fail | uncertain`:

- Subject identity stays consistent.
- Requested action happens in the correct order.
- Camera movement matches the brief.
- Reference roles are obeyed.
- Aspect ratio and duration are acceptable.
- No unwanted text/watermark.
- No unexpected characters/objects.
- Audio/speech/music matches or is acceptably absent.
- Motion is coherent, without severe flicker, morphing, or physics breaks.
