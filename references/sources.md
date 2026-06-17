# Sources And Known Facts

## Private Documentation Rule

Treat private Lark/wiki/doc links as inaccessible unless the user provides exported contents or explicitly authorizes a logged-in/manual review path. Do not store private document URLs in this reusable skill, and do not infer private API details from inaccessible links.

## Exported Xiaoyunque CLI Guide

Facts from the exported guide:

- The official package is installed with `npx @pippit-dev/cli@latest install`.
- After installation, the executable is `pippit-tool-cli`.
- `pippit-tool-cli generate-video` supports text-to-video and image/video-reference generation.
- `generate-video` parameters shown in the guide include `--prompt`, `--duration`, `--ratio`, `--resolution`, `--model`, repeated `--image`, and repeated `--video`.
- `generate-video` returns `thread_id` and `run_id`.
- `pippit-tool-cli query-result --thread-id <thread_id> --run-id <run_id> --download-dir <dir>` queries and downloads async results.
- Normal user model ids: `seedance2.0_direct`, `seedance2.0_fast_direct`.
- VIP model ids additionally include `seedance2.0_vision`, `seedance2.0_fast_vision`, and `Seedance_2.0_mini`.
- `1080p` only supports `seedance2.0_vision`.
- Local logs live under `~/.pippit_tool_cli/logs/YYYY-MM-DD.log`.
- The guide version notes mention v1.0.7 on 2026-06-16 adding Seedance 2.0 mini support, and v1.0.6 on 2026-06-09 adding video generation and result query commands.

## Installed CLI Help

Observed from `pippit-tool-cli 1.0.8` on 2026-06-17:

- Top-level commands include `generate-video`, `query-result`, `download-result`, `get-thread`, `list-thread-file`, `short-drama`, and `update`.
- `generate-video` flags include `--prompt`, `--duration`, `--ratio`, `--resolution`, `--model`, repeated `--image`, repeated `--video`, and repeated `--audio`.
- `--duration` is an integer number of seconds.
- Ratio examples shown by CLI help: `9:16`, `16:9`, `3:4`, and `4:3`.
- Resolution examples shown by CLI help: `720p`, `1080p`.
- Reference limits shown by CLI help: up to 9 images, up to 3 videos, and up to 3 audios.
- Model ids shown by CLI help: normal users can use `seedance2.0_direct` and `seedance2.0_fast_direct`; VIP users can additionally use `seedance2.0_vision` and `seedance2.0_fast_vision`.
- `Seedance_2.0_mini` appears in the exported guide but not in `generate-video --help` for CLI v1.0.8. Treat it as version/account dependent until current help or account UI confirms a runnable model id.
- `query-result` requires `--thread-id`, `--run-id`, and `--download-dir`.
- `download-result` accepts `--url`, `--updated-at`, `--output-path`, and `--workers`; do not persist temporary result URLs in job files.
- `get-thread` and `list-thread-file` are diagnostic helpers.
- `short-drama` has separate subcommands and should not be mixed into the default `generate-video` workflow without a dedicated workflow update.

## Public Xiaoyunque / Pippit Site

Observed source: `https://xyq.jianying.com/` after `https://www.pippit.ai/` redirected there for the current region.

Public page facts observed from server-rendered HTML on 2026-06-17:

- Brand/title: Xiaoyunque / 小云雀.
- Site description presents Xiaoyunque as an AI content creation agent for quickly generating videos and images from natural-language instructions.
- Main prompt input placeholder asks the user what they want to create.
- Default visible generation type: `沉浸式短片`.
- Default visible video model: `Seedance 2.0 Fast`.
- Feature cards include Seedance 2.0, short-drama agent, viral replication, and one-take generation.
- The public model config exposes video model labels: `Seedance 2.0 Mini`, `Seedance 2.0 Fast VIP`, `Seedance 2.0 VIP`, `Seedance 2.0 Fast`, `Seedance 2.0`, and `Seedance 1.5`.
- Public labels describe Seedance 2.0 variants as supporting multimodal references such as audio, video, text, and images. Treat this as UI guidance, not an API contract.

## Public Seedance Site

Observed source: `https://seed.bytedance.com/en/seedance2_0`.

The public Seedance page shows example prompts with:

- Multi-shot and one-take cinematic descriptions.
- Explicit camera movement, lighting, action beats, and audio cues.
- Multiple aspect ratios represented in examples, including `16:9`, `9:16`, `1:1`, and `3:4`.
- Some examples include `voice: true`, so audio-aware prompting is a useful prompt section when the chosen model/UI supports it.

## Public Prompt Collection

Observed source: `https://github.com/YouMind-OpenLab/awesome-seedance-2-prompts`.

Use this repository as an external prompt-pattern source for Seedance 2.0. The skill should not bulk-copy the collection into local files. Instead:

- Browse/search the repository when a task needs a specific genre or style.
- Adapt prompt structure and specificity rather than copying full examples blindly.
- Record successful reusable patterns in the project video brief or a project analysis note.
- Keep attribution/source links in notes when a pattern is meaningfully adapted.

## Reference Binding Status

No currently checked official source explicitly documents filename-based reference binding or exposes a CLI flag such as `--image-role`, `--image-name`, or `--reference-id`. The installed CLI exposes repeated `--image` values as an ordered string array. The local prompt templates and common prompt examples use ordered language such as `Image 1` and `Image 2` for start/end frames or attached references. Therefore this skill uses order binding as an engineering convention: first `--image` equals `Image 1`, second `--image` equals `Image 2`, etc. Treat this as the safest prompt/CLI convention, not as a verified hidden provider contract.

## Unverified / Needs Lark Or Logged-In Confirmation

These details must not be hard-coded until verified from accessible docs or logged-in network traces the user explicitly provides:

- Xiaoyunque private API endpoint paths.
- Required request headers, cookies, CSRF tokens, web ids, or account identifiers.
- Model ids beyond exported CLI guide and public UI values.
- Exact credit and membership limits.
- Whether reference inputs are accepted by API as local files, URLs, object-store ids, or web-upload ids.
- Whether any private API supports explicit reference role/name/id binding beyond CLI input order.
