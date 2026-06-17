# Usage

## Official CLI Route

Use the official Xiaoyunque CLI route for real generation. It comes from the exported guide `小云雀 CLI 体验指南.md`. Installing `pippit-tool-cli` is required for real generation and result querying; without it, this skill can only prepare prompts and job packages.

### Install Or Verify CLI

Install when `pippit-tool-cli` is missing:

```bash
npx @pippit-dev/cli@latest install
```

Inspect available commands with an absolute path.

macOS/Linux common path:

```bash
$HOME/.npm-global/bin/pippit-tool-cli -h
```

macOS/Linux path discovery when the common path is missing:

```bash
npm prefix -g
command -v pippit-tool-cli
```

Windows PowerShell path discovery:

```powershell
npm prefix -g
Get-Command pippit-tool-cli
```

Use the discovered absolute path for normal skill calls. On macOS/Linux this is commonly:

```bash
$HOME/.npm-global/bin/pippit-tool-cli
```

On Windows, use the full path returned by PowerShell. Do not rely on `PATH` for automated skill execution; absolute paths make Codex sessions and worker sessions behave consistently.

The CLI maintains local files under `~/.pippit_tool_cli/`, including daily logs at:

```text
~/.pippit_tool_cli/logs/YYYY-MM-DD.log
```

Installing with `npx` requires network access and may write to the user's home directory. In sandboxed Codex environments, request approval before running it. Strongly recommend installation to users who want actual Xiaoyunque generation; web fallback is only for login/key management or emergency manual use.

### Key Handling

Use the official local environment variable:

```bash
export XYQ_ACCESS_KEY="..."
```

Windows PowerShell:

```powershell
$env:XYQ_ACCESS_KEY="..."
```

For first-time setup in Codex, tell the user to type `/quit`, return to the same terminal, run the export command above, then reopen or resume Codex from that terminal. Environment variables exported after Codex is already running are usually not visible to the existing Codex process.

Do not print the value. Check visibility with:

```bash
python3 skills/xiaoyunque-video/scripts/xiaoyunque_video_job.py doctor
```

If the official installer prompts for a key, ask the user to enter it into that installer prompt rather than storing it in project files.

`XIAOYUNQUE_API_KEY` is accepted only as a compatibility fallback by this skill's helper; the official CLI error messages require `XYQ_ACCESS_KEY`.

### Generate Video

Run after job package creation and explicit cost confirmation:

```bash
$HOME/.npm-global/bin/pippit-tool-cli generate-video \
  --prompt "镜头推进，一只橘猫从沙发上跳下来" \
  --duration 5 \
  --ratio 9:16 \
  --resolution 720p \
  --model seedance2.0_fast_direct \
  --audio "~/audio/music.mp3" \
  --image "~/images/cat1.jpg" \
  --image "~/images/cat2.jpg" \
  --video "~/videos/cat1.mp4" \
  --video "~/videos/cat2.mp4"
```

### Parameter Rules

Current installed CLI checked: `pippit-tool-cli 1.0.8`.

`generate-video` flags from the current CLI help:

- `--prompt string`: video prompt text.
- `--duration int`: duration in seconds. Use an integer for the CLI, for example `5`. Seedance 2.0 public examples and prompt collections commonly describe 4-15 second clips; prefer 5 seconds for smoke tests and short prompt validation.
- `--ratio string`: target aspect ratio. CLI help examples list `9:16`, `16:9`, `3:4`, and `4:3`. Public Seedance examples also show `1:1`, but treat ratios not shown by CLI help as account/version dependent unless tested.
- `--resolution string`: target resolution, for example `720p` or `1080p`.
- `--model string`: CLI model id.
- `--image stringArray`: local reference image path; repeat for multiple images.
- `--video stringArray`: local reference video path; repeat for multiple videos.
- `--audio stringArray`: local reference audio path; repeat for multiple audios.

Reference binding rule:

- The CLI exposes repeated `--image` values as an ordered string array and does not expose a filename, role, or name binding flag.
- Use order binding as the skill convention: the first `--image` is `Image 1 / 第一张参考图`, the second is `Image 2 / 第二张参考图`, and so on.
- Prompt text must use the same numbering as the CLI argument order. Do not assume filenames are visible to the model or used for binding.
- Semantic filenames such as `image-01-start-frame.png` are still useful for human review, but the prompt should not rely on the filename.
- For exact start/end control, keep reference count low and write explicit authority language, for example `Image 1 是起始帧和主体身份权威，Image 2 是结束帧和目标构图权威`.

Reference limits from current CLI help:

- `--image`: repeat for multiple images, up to 9.
- `--video`: repeat for multiple videos, up to 3.
- `--audio`: repeat for multiple audios, up to 3.

Supported model ids from the exported guide:

- Normal users: `seedance2.0_direct`, `seedance2.0_fast_direct`
- VIP users: `seedance2.0_direct`, `seedance2.0_fast_direct`, `seedance2.0_vision`, `seedance2.0_fast_vision`

The exported guide also mentions `Seedance_2.0_mini` for VIP users, but `pippit-tool-cli generate-video --help` in v1.0.8 does not list it. Prefer the help output for runnable commands unless the current CLI version or account UI shows Mini support.

Resolution rule from the exported guide:

- `1080p` only supports `seedance2.0_vision`.

Recommendations:

- Start with `seedance2.0_fast_direct`, `720p`, 5 seconds, and no references for environment smoke tests.
- Use `seedance2.0_direct` when quality matters more than speed and VIP-only models are not available.
- Use `seedance2.0_fast_vision` or `seedance2.0_vision` only when the account supports VIP models; use `seedance2.0_vision` for `1080p`.
- Keep first reference-driven tests small: one or two images/videos, then add more references only if role binding remains stable.
- For social vertical video, use `9:16`; for storyboard, cinematic, or desktop preview, use `16:9`; for product/detail clips, `3:4` or `4:3` may be useful when the current CLI accepts them.
- Keep exact text/subtitle demands short. Prefer post-production overlays when exact typography matters.

Other CLI subcommands observed in v1.0.8:

- `download-result`: downloads a generated result URL. Use only when the CLI gives a result URL and `query-result` is not enough; do not store temporary URLs in job metadata.
- `get-thread` and `list-thread-file`: diagnostic thread inspection helpers.
- `short-drama`: separate short-drama workflow commands. Treat as an extension path, not the default Seedance `generate-video` route.
- `update`: updates the installed CLI and bundled skills; run only after user approval.

### Query And Download

`generate-video` returns `thread_id` and `run_id`. Use both to query the async result:

```bash
$HOME/.npm-global/bin/pippit-tool-cli query-result \
  --thread-id <thread_id> \
  --run-id <run_id> \
  --download-dir <download_dir>
```

Save downloaded videos under the job package `output/` folder and complete `review.md` before reporting success.

For normal async waiting, prefer the helper loop instead of manual repeated checks:

```bash
python3 skills/xiaoyunque-video/scripts/xiaoyunque_video_job.py wait-result \
  --thread-id <thread_id> \
  --run-id <run_id> \
  --download-dir outputs/xiaoyunque-video/<job_slug>/output \
  --job-json outputs/xiaoyunque-video/<job_slug>/job.json
```

Defaults:

- `--max-wait 600`: wait up to 10 minutes.
- `--interval 60`: query once per minute.
- exits immediately on success, provider error, or timeout.

## Web Fallback Route

Use the website route for key creation, account login, and fallback manual generation.

1. Prepare a prompt file and reference list.
2. Create or read `VIDEO_PROJECT_BRIEF.md` for project-bound work.
3. Create a job package.
4. Confirm the paid run with the user: exact model, mode, aspect ratio, duration, and references.
5. Open `https://xyq.jianying.com/`.
6. Log in manually if required. Do not ask Codex to store credentials.
7. Choose generation type, usually `沉浸式短片` for a general video.
8. Choose the model label. Default to `Seedance 2.0 Fast` when the user does not specify.
9. Upload reference images/videos/audio if the task uses them.
10. Paste the prompt.
11. Submit and wait for completion.
12. Download the video and save it in the job package folder.
13. Review with the checklist in `prompting.md`.

Use the Browser plugin/in-app browser when the user asks Codex to open, click, type, inspect, or screenshot the Xiaoyunque site. If browser login or captcha blocks progress, stop and ask the user to complete that step.

## Job Package Script

Create a reproducible local package before or instead of submitting:

Check the local key without printing it:

```bash
python3 skills/xiaoyunque-video/scripts/xiaoyunque_video_job.py doctor
```

Create the project video companion brief if missing:

```bash
python3 skills/xiaoyunque-video/scripts/xiaoyunque_video_job.py brief \
  --path VIDEO_PROJECT_BRIEF.md
```

```bash
python3 skills/xiaoyunque-video/scripts/xiaoyunque_video_job.py create \
  --name perfume-ad-v01 \
  --prompt-file prompt.md \
  --out-dir outputs/xiaoyunque-video \
  --model "Seedance 2.0 Fast" \
  --mode "immersive-short" \
  --aspect-ratio "9:16" \
  --duration "8s" \
  --require-key \
  --cost-confirmation not-confirmed \
  --reference hero.png:style \
  --reference product.png:product-identity
```

The script writes:

- `prompt.md`: copied final prompt.
- `job.json`: structured job metadata and reference roles.
- `review.md`: review checklist template.
- `submit_notes.md`: web-route submission notes.

The script does not call Xiaoyunque and does not inspect media.

Use `--cost-confirmation user-confirmed` only after the user approves the exact paid generation. Keep `not-confirmed` for preparation-only packages.

## Raw API Route

Only add or use raw API scripts after verified documentation is available beyond the official CLI guide. A verified raw API route must record:

- base URL and endpoint path
- authentication method, defaulting to `XYQ_ACCESS_KEY` from the local environment without storing the secret
- request schema
- upload/reference-file schema
- async task id and polling schema
- download URL schema
- status/error mapping
- exact model ids and supported parameters

Until then, API-related requests should use the official CLI route or result in a job package plus a note that raw API docs are not yet loaded.

## Output Organization

For project-bound work, prefer:

```text
outputs/xiaoyunque-video/<job_slug>/
  prompt.md
  job.json
  review.md
  submit_notes.md
  references/
  output/
```

Do not overwrite existing jobs. Create `job-v02`, timestamped folders, or a new slug.
