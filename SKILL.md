---
name: xiaoyunque-video
description: Create, package, submit, query, download, and review AI video-generation jobs through the official Xiaoyunque/Pippit CLI and Seedance models. Use when Codex needs to install or verify @pippit-dev/cli, use pippit-tool-cli generate-video/query-result, prepare Xiaoyunque video prompts, choose Seedance 2.0/1.5 model variants, work with text-to-video or image/video-reference generation, package reproducible job files, inspect generated videos, or document Xiaoyunque video generation attempts safely.
---

# Xiaoyunque Video

Use this skill for Xiaoyunque / Pippit video generation work, especially Seedance-based "immersive short film", "one-take", image-to-video, multi-reference video, short-drama, and viral-replication tasks.

## Core Rules

- Prefer the official Xiaoyunque CLI route from the local guide: install with `npx @pippit-dev/cli@latest install`, then call the executable by absolute path. Default to `$HOME/.npm-global/bin/pippit-tool-cli` for `generate-video`, `query-result`, and CLI help so the skill does not depend on shell `PATH`.
- Treat the official CLI as required for real generation. If `pippit-tool-cli` is missing, stop after prompt/job-package preparation and strongly recommend installing it; do not fall back to an invented API or unofficial provider.
- Prefer the locally exported `XYQ_ACCESS_KEY` for CLI/API-backed workflows. On first use, if the key is not visible inside Codex, tell the user to type `/quit`, return to the same terminal, run `export XYQ_ACCESS_KEY="..."`, then reopen/resume Codex from that terminal before formal video generation. Accept `XIAOYUNQUE_API_KEY` only as a compatibility fallback that the helper may map to `XYQ_ACCESS_KEY` for the CLI process. Never ask the user to paste the key into chat, prompts, job files, or command arguments. If the CLI installer requires interactive secret entry, ask the user to paste it into the installer prompt, not into project files.
- Use the Xiaoyunque website for login, key creation, and fallback manual generation; do not treat browser bundles as API documentation.
- Do not invent private API endpoints, cookies, tokens, request bodies, or hidden headers.
- Never store login cookies, bearer tokens, API keys, session ids, or account credentials in the skill or project files.
- Save project-bound prompts, job metadata, outputs, and reviews into the current workspace with versioned names.
- Keep provider, CLI, testing, account, path, and job-tracking metadata out of prompt text sent to the video model. Put execution details in `job.json`, `submit_notes.md`, `review.md`, project briefs, or the user report. The model prompt must describe only the visible video content, creative intent, reference roles, constraints, and acceptance criteria unless the requested video visibly needs those words.
- Treat real video generation as expensive. Before any provider submission, state the exact model, mode, duration/aspect ratio, reference set, and whether the action may consume credits; require explicit user confirmation for that exact run unless the user already gave it.
- Treat video provider calls, video upload/download, async result polling, video inspection, frame extraction, audio inspection, and pixel-derived checks as media/provider work. In projects that use chief-worker isolation, run those tasks in a disposable worker. The main session may prepare prompt/job files and read text logs, but must not submit or poll real video provider jobs directly unless the user explicitly bypasses worker isolation.
- For reference videos/images/audio, state each input role before generation: edit target, start frame, end frame, character identity, style, camera motion, audio, storyboard, or negative reference.
- Bind image/video references by CLI input order. Treat the first repeated `--image` as `Image 1`, the second as `Image 2`, and so on; do not rely on filenames for model binding. When drafting prompts, explicitly write `Image 1 / 第一张参考图`, `Image 2 / 第二张参考图`, etc., and keep the CLI argument order identical to the prompt numbering.
- Do not mark a generated video approved until the user accepts that exact output.
- If a task only asks for a plan, prompt, shot list, or job package, stop after creating that artifact. Do not continue to provider generation without explicit permission.

## Files

- Job package / doctor / project brief script: `scripts/xiaoyunque_video_job.py`
- Source notes and live-site observations: `references/sources.md`
- Prompting guide: `references/prompting.md`
- Web workflow and API placeholder notes: `references/usage.md`
- Seedance prompt template catalog: `references/prompt-template-library.md`

Read `references/usage.md` before installing the CLI, running `generate-video`, querying results, or operating Xiaoyunque manually. Read `references/prompting.md` before writing non-trivial video prompts, especially multi-shot, one-take, reference-image/video, identity-continuity, or audio-aware prompts. Read `references/prompt-template-library.md` when choosing a reusable prompt shape or adapting examples from the awesome Seedance prompt collection. Read `references/sources.md` when checking what is known from the exported CLI guide, public pages, and Lark sources.

## Workflow

1. **Load project memory.** For project-bound work, look for `VIDEO_PROJECT_BRIEF.md` at the workspace root. If missing, create it with:

```bash
python3 <skill_dir>/scripts/xiaoyunque_video_job.py brief --path VIDEO_PROJECT_BRIEF.md
```

2. **Align the task.** Restate the goal as an actionable video request: subject, duration target if known, aspect ratio, model preference, input references, motion/camera intent, audio/text requirements, and what must remain fixed.
3. **Check secrets safely.** For API-backed work, verify the environment without printing secrets:

```bash
python3 <skill_dir>/scripts/xiaoyunque_video_job.py doctor
```

If neither `XYQ_ACCESS_KEY` nor compatibility fallback `XIAOYUNQUE_API_KEY` is visible, stop and ask the user to export `XYQ_ACCESS_KEY` locally. Do not accept the key in chat.
4. **Verify the official CLI for real generation.** Run `$HOME/.npm-global/bin/pippit-tool-cli -h`. If missing, install with `npx @pippit-dev/cli@latest install` after user approval, then use the absolute CLI path.
5. **Choose the route.**
   - Official CLI generation: default route for real Xiaoyunque work.
   - Job package only: use when the user wants prompts/files prepared for later manual submission.
   - Web generation: use for key creation, login, or fallback when CLI is unavailable.
   - Raw API route: use only after the user provides verified API documentation beyond the CLI guide.
6. **Select model, resolution, and ratio.** Use current CLI ids for runnable commands and public Xiaoyunque labels only as UI-facing names. Recommend `seedance2.0_fast_direct`, `720p`, and `5s` for general smoke tests or cost/speed balance; recommend `seedance2.0_direct` when quality matters more than speed. Use VIP-only `seedance2.0_fast_vision` or `seedance2.0_vision` only when the account supports them; use `seedance2.0_vision` for `1080p`. Prefer `16:9` for storyboard/cinematic preview, `9:16` for vertical social video, and `3:4` or `4:3` for product/detail or half-body subjects when accepted by the current CLI. Treat ratios not shown in current CLI help, such as `1:1`, as account/version dependent until tested.
7. **Prepare inputs.** For each reference, record path/link, order index, role, allowed inheritance, forbidden inheritance, and priority. Bind prompt language to CLI order: the first `--image` is `Image 1`, the second is `Image 2`, and filenames are only for human review. For media-inspection workflows, use worker observations rather than main-session media loading unless explicitly authorized.
8. **Choose a prompt template.** For non-trivial prompts, read `references/prompt-template-library.md`, pick one template family, then draft with `references/prompting.md`.
9. **Write a production prompt.** Use the structure in `references/prompting.md`: concept, visual style, scene beats, camera/motion, subject continuity, audio, constraints, aspect ratio, and avoid list. Before saving, remove execution metadata such as provider names, CLI/tool names, model validation wording, local paths, job ids, cost notes, API/key terminology, and private project labels unless they are intended to appear in the video. If the run is only a technical test, keep the prompt content-facing, for example `车辆与无人机编队公路追踪短片`, and record the test purpose in job metadata instead.
10. **Create a job package.** For project-bound work, create a job package before any paid submission:

```bash
python3 <skill_dir>/scripts/xiaoyunque_video_job.py create \
  --name <job_slug> \
  --prompt-file <prompt.md> \
  --out-dir <workspace_output_dir> \
  --model "Seedance 2.0 Fast" \
  --mode "immersive-short" \
  --aspect-ratio "16:9"
```

Use `--cost-confirmation user-confirmed` only when the user has explicitly approved the exact paid run. Otherwise keep `not-confirmed` and stop before provider submission.

11. **Submit only if authorized and isolated.** In chief-worker projects, delegate real `generate-video` submission to a disposable worker. Use `$HOME/.npm-global/bin/pippit-tool-cli generate-video` only after confirmation. Capture `thread_id` and `run_id`.
12. **Wait in one programmatic loop.** Do not manually ask for confirmation before each status check. Use the helper's async wait loop, defaulting to 10 minutes and one check per minute:

```bash
python3 <skill_dir>/scripts/xiaoyunque_video_job.py wait-result \
  --thread-id <thread_id> \
  --run-id <run_id> \
  --download-dir <job_output_dir> \
  --job-json <job.json>
```

The command exits when completed and downloaded, fails on provider error, or times out.
13. **Review before reporting success.** Check prompt obedience, reference role obedience, subject identity, motion continuity, camera stability, aspect ratio, duration, text, audio, and unwanted artifacts. Report `pass | fail | uncertain`; do not treat `uncertain` as pass.
14. **Record the run.** Save final prompt, model label, website/API route, reference list, output path, review notes, provider failure class, and reusable lessons. Update `VIDEO_PROJECT_BRIEF.md` after substantial work with durable project style rules, accepted model choices, reference roles, continuity constraints, and failure patterns.

## Failure Handling

- `auth-blocked`: Xiaoyunque requires login or membership; stop and ask the user to log in or provide accessible docs.
- `docs-blocked`: the user-provided Lark document is inaccessible; use public-source workflow and list missing API facts.
- `cli-missing`: `$HOME/.npm-global/bin/pippit-tool-cli` is not installed; real generation is blocked until installing with `npx @pippit-dev/cli@latest install` after user approval.
- `key-missing`: `XYQ_ACCESS_KEY` is not visible to the current process; tell the user to `/quit`, export it in the same terminal, reopen/resume Codex, and retry `doctor`. `XIAOYUNQUE_API_KEY` is only a compatibility fallback for older local setup.
- `cost-unconfirmed`: a real provider call would consume credits but the exact run was not explicitly confirmed; stop before submission.
- `provider-pending`: web job has not finished; report the job URL/status and continue only when asked.
- `download-blocked`: output exists in browser but download is blocked; ask for browser/session help rather than scraping credentials.
- `reference-drift`: character, product, setting, or layout from references changed; retry with fewer references and stricter role labels.
- `motion-failure`: camera path, one-take continuity, subject action, or physics is wrong; simplify beats or split into shorter clips.
- `text-audio-failure`: subtitle, logo, speech, or music misses requirements; move exact text/audio requirements into a dedicated prompt section or handle deterministic overlays externally when appropriate.

## Reporting

When finishing a generation task, report:

- Final video path(s) and job package path.
- Model id/label, duration, resolution, ratio, and whether the route was official CLI, web/manual, or raw API.
- `thread_id` and `run_id` when a CLI job was submitted.
- Prompt file path and final prompt summary.
- Reference roles used.
- Review result with failures first.
- Any missing Lark/API facts that prevented automation.
