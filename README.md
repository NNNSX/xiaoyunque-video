# Xiaoyunque Video Skill

这是一个 Codex skill，用于通过官方小云雀 / Pippit CLI 调用 Seedance 视频生成模型，准备可复现的视频任务包，并自动查询、下载异步结果。

默认路线是官方 CLI，不使用未验证的私有 API。真实视频生成通常会消耗额度，提交前必须确认模型、时长、比例、参考素材和费用风险。

## 能力范围

- 文生视频：`pippit-tool-cli generate-video`
- 图像、视频、音频参考：重复传入 `--image`、`--video`、`--audio`
- 异步查询与下载：`pippit-tool-cli query-result`
- 任务包创建、环境诊断、项目视频记忆：`scripts/xiaoyunque_video_job.py`
- Seedance 提示词模板与参考绑定规则：`references/prompting.md`、`references/prompt-template-library.md`

## 快速开始

安装官方 CLI：

```bash
npx @pippit-dev/cli@latest install
```

真实生成默认使用绝对路径，不依赖 `PATH`：

```bash
$HOME/.npm-global/bin/pippit-tool-cli
```

设置 key 时只在本地终端声明环境变量：

```bash
export XYQ_ACCESS_KEY="..."
```

如果已经进入 Codex 会话后才设置 key，当前 Codex 进程通常看不到新环境变量。首次正式使用时建议：

1. 在 Codex 中输入 `/quit` 退出。
2. 回到同一个终端执行 `export XYQ_ACCESS_KEY="..."`。
3. 从这个终端重新进入或恢复 Codex 会话。
4. 运行诊断确认 key 可见。

诊断不会打印 key 值：

```bash
python3 skills/xiaoyunque-video/scripts/xiaoyunque_video_job.py doctor
```

`XIAOYUNQUE_API_KEY` 只作为旧本地配置兼容 fallback；正式使用优先设置 `XYQ_ACCESS_KEY`。

## 模型与参数速查

以当前 CLI 帮助和已整理资料为准，详细规则见 `references/usage.md`。

| 用途 | 推荐值 |
| --- | --- |
| 普通默认 / 成本速度平衡 | `seedance2.0_fast_direct`、`720p`、`5s` |
| 质量优先 | `seedance2.0_direct`，必要时再试账号支持的 VIP 模型 |
| 1080p | 仅推荐 `seedance2.0_vision`，并先确认账号支持 |
| 横版分镜 / 电影感预览 | `16:9` |
| 竖屏社媒 | `9:16` |
| 产品细节 / 人物半身 | `3:4` 或 `4:3` |

已知 CLI 模型 ID：

- 普通用户：`seedance2.0_direct`、`seedance2.0_fast_direct`
- VIP 用户：`seedance2.0_direct`、`seedance2.0_fast_direct`、`seedance2.0_vision`、`seedance2.0_fast_vision`

当前 CLI 帮助列出的画幅包括 `9:16`、`16:9`、`3:4`、`4:3`；分辨率包括 `720p`、`1080p`。公开示例中出现的 `1:1` 需按当前账号和 CLI 版本实测确认。

## 最小工作流

1. 创建或读取项目视频记忆：

```bash
python3 skills/xiaoyunque-video/scripts/xiaoyunque_video_job.py brief \
  --path VIDEO_PROJECT_BRIEF.md
```

2. 按提示词规则写 `prompt.md`。非简单任务先看：

- `references/prompting.md`
- `references/prompt-template-library.md`
- `references/usage.md`

3. 创建任务包：

```bash
python3 skills/xiaoyunque-video/scripts/xiaoyunque_video_job.py create \
  --name demo-video-v01 \
  --prompt-file prompt.md \
  --out-dir outputs/xiaoyunque-video \
  --model seedance2.0_fast_direct \
  --mode text-to-video \
  --aspect-ratio 16:9 \
  --resolution 720p \
  --duration 5s \
  --require-key \
  --cost-confirmation not-confirmed
```

4. 用户确认真实付费生成后，用官方 CLI 提交并记录 `thread_id`、`run_id`：

```bash
$HOME/.npm-global/bin/pippit-tool-cli generate-video \
  --prompt "<final prompt>" \
  --duration 5 \
  --ratio 16:9 \
  --resolution 720p \
  --model seedance2.0_fast_direct
```

5. 自动等待并下载：

```bash
python3 skills/xiaoyunque-video/scripts/xiaoyunque_video_job.py wait-result \
  --thread-id <thread_id> \
  --run-id <run_id> \
  --download-dir outputs/xiaoyunque-video/<job_slug>/output \
  --job-json outputs/xiaoyunque-video/<job_slug>/job.json
```

`wait-result` 默认最多等待 10 分钟，每 60 秒查询一次；成功、provider 报错或超时才退出。

## 关键规则

- 官方 CLI 必须安装；缺少 CLI 时只准备任务包，不编造 API。
- 使用 `$HOME/.npm-global/bin/pippit-tool-cli` 绝对路径。
- 提交真实生成前必须确认本次模型、时长、比例、参考素材和费用风险。
- 多参考图按传入顺序绑定：第一条 `--image` 是 `Image 1 / 第一张参考图`，第二条是 `Image 2 / 第二张参考图`；不要依赖文件名作为模型绑定依据。
- 参考图、视频、音频的角色要写清楚：起始帧、结束帧、主体身份、风格、镜头运动、音频等。
- 生成后必须检查主体一致性、动作顺序、镜头稳定性、比例、时长、文字水印、音频和严重变形。

## 提示词隐私

送入模型的提示词只写视频内容、创作意图、参考素材角色、约束和验收标准。不要把小云雀/Seedance/CLI/skill/API/key、模型测试、接口验证、本地路径、job id、费用说明、内部项目名等执行信息写进提示词。

这些执行信息应该放在 `job.json`、`submit_notes.md`、`review.md` 或项目笔记里。即使只是测试，也要把 `视频用途` 写成内容相关表达，例如 `车辆与无人机编队公路追踪短片`，不要写 `小云雀模型测试`。

## 推荐输出结构

```text
outputs/xiaoyunque-video/<job_slug>/
  prompt.md
  job.json
  review.md
  submit_notes.md
  references/
  output/
```

`job.json` 只记录任务元数据、环境变量名、任务 ID、状态和输出路径，不应该记录 key、cookie、登录态或临时下载 URL。

## 安全约束

- 不要把 API key 写进项目文件、README、prompt、job.json、日志或聊天记录。
- 不要提交 `.env`、CLI 日志、生成输出、缓存、临时下载链接或账号凭证。
- 不要把私有 Lark 链接、内部文档内容或未脱敏请求头发布到公开仓库。
- 不要在没有用户确认的情况下提交真实视频生成请求。
- 不要使用未验证的私有 API、cookie、CSRF token 或浏览器会话来绕过官方 CLI。
