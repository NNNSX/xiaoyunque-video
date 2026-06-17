#!/usr/bin/env python3
"""Create reproducible Xiaoyunque video generation job packages."""

from __future__ import annotations

import argparse
import os
import json
import re
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

PRIMARY_KEY_ENV = "XYQ_ACCESS_KEY"
LEGACY_KEY_ENV = "XIAOYUNQUE_API_KEY"
DEFAULT_BRIEF = "VIDEO_PROJECT_BRIEF.md"

DEFAULT_REVIEW = """# Review Checklist

Mark each item `pass | fail | uncertain`.

- Subject identity stays consistent:
- Requested action happens in the correct order:
- Camera movement matches the brief:
- Reference roles are obeyed:
- Aspect ratio and duration are acceptable:
- No unwanted text/watermark:
- No unexpected characters/objects:
- Audio/speech/music matches or is acceptably absent:
- Motion is coherent, without severe flicker, morphing, or physics breaks:

Notes:
"""

DEFAULT_BRIEF_TEXT = """# Video Project Brief

This file is the project companion brief for Xiaoyunque/Seedance video work. Keep durable project video memory here; keep temporary candidates, one-off experiments, and long provider logs in analysis files.

## Operating Rules

- Use `skills/xiaoyunque-video` for Xiaoyunque/Pippit/Seedance video planning and generation tasks.
- Store secrets only in environment variables such as `XYQ_ACCESS_KEY`; never paste keys into prompts, job files, logs, or project docs.
- Treat real video generation as costly. Require an explicit user confirmation before submitting paid provider jobs unless the user has already authorized that exact run.
- Do not mark a video approved until the user accepts that exact output.

## Current Video Memory

- Record reusable style rules, accepted model choices, prompt patterns, reference roles, failure modes, and review criteria.
- Keep project-specific continuity constraints here rather than in the reusable skill.

## Reference And Asset Index

| Path or Link | Role | Notes | Last Verified |
| --- | --- | --- | --- |

## Prompt Style Rules

- Write video prompts as production briefs with action beats, camera motion, subject continuity, audio, constraints, and review criteria.
- Keep execution metadata out of model prompts. Provider/tool names, route tests, local paths, API/key terms, job ids, cost notes, and private project labels belong in job metadata or notes unless they must appear visibly in the generated video.
- For reference-driven generation, label each reference role and state allowed/forbidden inheritance.
- For expensive retries, change one major prompt or reference lever at a time and record why.

## Candidate Lessons

| Date | Task | Lesson | Link |
| --- | --- | --- | --- |
"""

PROMPT_HYGIENE_PATTERNS = [
    ("provider/tool metadata", re.compile(r"(?:小云雀|Xiaoyunque|Pippit|Seedance|CLI|provider|skill|API|thread_id|run_id|job_id)", re.I)),
    ("key/token terminology", re.compile(r"\b(?:XIAOYUNQUE_API_KEY|XYQ_ACCESS_KEY|api[_ -]?key|access[_ -]?key|token|Bearer)\b", re.I)),
    ("operator test wording", re.compile(r"(?:小云雀|模型|接口|路由|参考图顺序|顺序绑定|连通性|生成能力).{0,12}(?:测试|验证|实验|检查)|(?:测试|验证|实验|检查).{0,12}(?:小云雀|模型|接口|路由|参考图顺序|顺序绑定|连通性|生成能力)")),
    ("local path or output path", re.compile(r"(?:/Users/|\\\\Users\\\\|outputs/|skills/)")),
]


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    if not value:
        raise SystemExit("Job name must contain at least one ASCII letter, digit, dot, underscore, or hyphen.")
    return value[:96]


def parse_reference(raw: str) -> dict[str, str]:
    if ":" not in raw:
        return {"path": raw, "role": "reference"}
    path, role = raw.rsplit(":", 1)
    return {"path": path, "role": role or "reference"}


def unique_dir(base: Path) -> Path:
    if not base.exists():
        return base
    stem = base.name
    parent = base.parent
    for idx in range(2, 1000):
        candidate = parent / f"{stem}-v{idx:02d}"
        if not candidate.exists():
            return candidate
    raise SystemExit(f"Could not find a free versioned directory for {base}")


def key_status() -> dict[str, object]:
    primary = os.environ.get(PRIMARY_KEY_ENV)
    legacy = os.environ.get(LEGACY_KEY_ENV)
    active_env = PRIMARY_KEY_ENV if primary else LEGACY_KEY_ENV if legacy else PRIMARY_KEY_ENV
    active_value = primary or legacy or ""
    return {
        "env": active_env,
        "present": bool(active_value),
        "length": len(active_value),
        "primary_env": PRIMARY_KEY_ENV,
        "primary_present": bool(primary),
        "legacy_env": LEGACY_KEY_ENV,
        "legacy_present": bool(legacy),
    }


def prompt_hygiene_warnings(prompt_text: str) -> list[str]:
    warnings = []
    for label, pattern in PROMPT_HYGIENE_PATTERNS:
        if pattern.search(prompt_text):
            warnings.append(label)
    return warnings


def require_key_if_requested(require_key: bool) -> None:
    if require_key and not key_status()["present"]:
        raise SystemExit(
            f"{PRIMARY_KEY_ENV} is not set in this process. Export it locally before preparing CLI-backed jobs. "
            f"{LEGACY_KEY_ENV} is accepted only as a compatibility fallback."
        )


def cli_env() -> dict[str, str]:
    env = dict(os.environ)
    if not env.get(PRIMARY_KEY_ENV) and env.get(LEGACY_KEY_ENV):
        env[PRIMARY_KEY_ENV] = env[LEGACY_KEY_ENV]
    return env


def doctor(args: argparse.Namespace) -> None:
    status = key_status()
    response = {
        "key_env": status["env"],
        "key_present": status["present"],
        "primary_key_env": status["primary_env"],
        "primary_key_present": status["primary_present"],
        "legacy_key_env": status["legacy_env"],
        "legacy_key_present": status["legacy_present"],
        "key_length": status["length"] if args.show_length else "hidden",
        "safe_to_log": True,
        "message": "API key value was not printed.",
    }
    print(json.dumps(response, ensure_ascii=False, indent=2))


def ensure_brief(args: argparse.Namespace) -> None:
    path = Path(args.path).expanduser()
    if path.exists() and not args.force:
        print(path)
        return
    if path.exists() and args.force:
        path.write_text(DEFAULT_BRIEF_TEXT, encoding="utf-8")
    elif not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(DEFAULT_BRIEF_TEXT, encoding="utf-8")
    print(path)


def create(args: argparse.Namespace) -> None:
    require_key_if_requested(args.require_key)
    prompt_src = Path(args.prompt_file).expanduser()
    if not prompt_src.is_file():
        raise SystemExit(f"Prompt file not found: {prompt_src}")
    prompt_text = prompt_src.read_text(encoding="utf-8")
    hygiene_warnings = prompt_hygiene_warnings(prompt_text)
    for warning in hygiene_warnings:
        print(
            "warning: prompt may contain execution/private metadata "
            f"({warning}); keep provider/test/path/key/job details in job notes, not in the model prompt.",
            file=sys.stderr,
        )

    out_dir = Path(args.out_dir).expanduser()
    job_dir = unique_dir(out_dir / slugify(args.name))
    job_dir.mkdir(parents=True)
    (job_dir / "references").mkdir()
    (job_dir / "output").mkdir()

    prompt_dst = job_dir / "prompt.md"
    shutil.copyfile(prompt_src, prompt_dst)

    references = []
    for index, item in enumerate(args.reference, start=1):
        reference = parse_reference(item)
        reference["order"] = index
        references.append(reference)
    status = key_status()
    job = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "job_name": job_dir.name,
        "route": args.route,
        "model": args.model,
        "mode": args.mode,
        "aspect_ratio": args.aspect_ratio,
        "resolution": args.resolution,
        "duration": args.duration,
        "thread_id": "",
        "run_id": "",
        "prompt_file": "prompt.md",
        "references": references,
        "api_key_env": status["env"],
        "primary_api_key_env": PRIMARY_KEY_ENV,
        "legacy_api_key_env": LEGACY_KEY_ENV,
        "api_key_present_at_prepare_time": status["present"],
        "api_key_value_logged": False,
        "cost_confirmation": args.cost_confirmation,
        "estimated_cost_note": args.estimated_cost_note,
        "prompt_hygiene_warnings": hygiene_warnings,
        "status": "prepared-not-submitted",
        "notes": args.note,
    }
    (job_dir / "job.json").write_text(json.dumps(job, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (job_dir / "review.md").write_text(DEFAULT_REVIEW, encoding="utf-8")
    (job_dir / "submit_notes.md").write_text(
        "\n".join(
            [
                "# Xiaoyunque Web Submission Notes",
                "",
                "Preferred route: official Xiaoyunque CLI via a platform-specific absolute `pippit-tool-cli` path. On macOS/Linux, `$HOME/.npm-global/bin/pippit-tool-cli` is the common default. On Windows, locate it with PowerShell `Get-Command pippit-tool-cli` or `npm prefix -g`.",
                "",
                "1. Verify `XYQ_ACCESS_KEY` is exported locally; do not print it. If this is first use and Codex cannot see it, type `/quit`, export the key in the same terminal, then reopen/resume Codex from that terminal. `XIAOYUNQUE_API_KEY` is only a compatibility fallback.",
                "2. Verify the platform-specific absolute `pippit-tool-cli -h` path works, installing with `npx @pippit-dev/cli@latest install` only after approval.",
                f"3. Model: {args.model}",
                f"4. Mode/type: {args.mode}",
                f"5. Aspect ratio: {args.aspect_ratio}",
                f"6. Resolution: {args.resolution}",
                f"7. Duration target: {args.duration or 'not specified'}",
                "8. Upload/pass references according to `job.json` order and roles. For repeated `--image`, the first path is `Image 1`, the second is `Image 2`; keep prompt numbering and CLI order identical.",
                "9. Do not rely on filenames for model binding; semantic filenames are only human safeguards.",
                "10. Before any paid submission, verify the user explicitly confirmed this exact model/duration/reference set.",
                "11. Run the absolute `pippit-tool-cli generate-video ...` path and record returned `thread_id` and `run_id` in `job.json` or run notes.",
                "12. Prefer `python3 skills/xiaoyunque-video/scripts/xiaoyunque_video_job.py wait-result ...`; pass `--cli <absolute_cli_path>` on systems where the macOS/Linux default is not valid. It queries `pippit-tool-cli query-result` with a 10-minute default wait and 60-second interval.",
                "13. Complete `review.md` before reporting success.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    print(job_dir)


def update_job(path: Path, updates: dict[str, object]) -> None:
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    data.update(updates)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def sanitize_query_payload(payload: dict[str, object]) -> dict[str, object]:
    sanitized = dict(payload)
    videos = []
    for item in payload.get("videos") or []:
        if not isinstance(item, dict):
            continue
        videos.append({"output_path": item.get("output_path", "")})
    sanitized["videos"] = videos
    return sanitized


def wait_result(args: argparse.Namespace) -> None:
    require_key_if_requested(True)
    cli = Path(args.cli).expanduser()
    if not cli.exists():
        raise SystemExit(f"CLI not found: {cli}")
    out_dir = Path(args.download_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    deadline = started + args.max_wait
    attempt = 0
    last_payload: dict[str, object] | None = None
    while True:
        attempt += 1
        cmd = [
            str(cli),
            "query-result",
            "--thread-id",
            args.thread_id,
            "--run-id",
            args.run_id,
            "--download-dir",
            str(out_dir),
        ]
        proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=cli_env())
        if proc.returncode != 0:
            raise SystemExit(proc.stderr or proc.stdout or f"query-result failed with code {proc.returncode}")
        stdout = proc.stdout.strip()
        try:
            payload = json.loads(stdout)
        except json.JSONDecodeError as exc:
            raise SystemExit(f"query-result returned non-JSON output: {stdout}") from exc
        last_payload = payload
        now = time.monotonic()
        elapsed = int(now - started)
        print(
            json.dumps(
                {
                    "attempt": attempt,
                    "elapsed_seconds": elapsed,
                    "completed": payload.get("completed"),
                    "error_message": payload.get("error_message", ""),
                    "video_count": len(payload.get("videos") or []),
                },
                ensure_ascii=False,
            ),
            flush=True,
        )
        if payload.get("error_message"):
            if args.job_json:
                update_job(Path(args.job_json), {"status": "failed", "last_query_result": sanitize_query_payload(payload)})
            raise SystemExit(f"Xiaoyunque job failed: {payload.get('error_message')}")
        if payload.get("completed"):
            videos = payload.get("videos") or []
            if args.job_json:
                outputs = []
                for item in videos:
                    output_path = item.get("output_path")
                    if output_path:
                        try:
                            outputs.append(str(Path(output_path).relative_to(Path(args.job_json).parent)))
                        except ValueError:
                            outputs.append(str(output_path))
                update_job(
                    Path(args.job_json),
                    {
                        "status": "completed-downloaded",
                        "last_query_result": sanitize_query_payload(payload),
                        "outputs": outputs,
                    },
                )
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return
        if now >= deadline:
            if args.job_json:
                update_job(
                    Path(args.job_json),
                    {"status": "pending-timeout", "last_query_result": sanitize_query_payload(last_payload or {})},
                )
            raise SystemExit(f"Timed out after {args.max_wait} seconds waiting for Xiaoyunque result.")
        sleep_for = min(args.interval, max(1, int(deadline - now)))
        time.sleep(sleep_for)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    doctor_cmd = sub.add_parser("doctor", help="check local environment without printing secrets")
    doctor_cmd.add_argument("--show-length", action="store_true", help="show key length without printing the key")
    doctor_cmd.set_defaults(func=doctor)

    brief_cmd = sub.add_parser("brief", help="create a project video companion brief if missing")
    brief_cmd.add_argument("--path", default=DEFAULT_BRIEF, help="brief path")
    brief_cmd.add_argument("--force", action="store_true", help="overwrite an existing brief")
    brief_cmd.set_defaults(func=ensure_brief)

    create_cmd = sub.add_parser("create", help="create a Xiaoyunque video job package")
    create_cmd.add_argument("--name", required=True, help="job slug/name")
    create_cmd.add_argument("--prompt-file", required=True, help="final prompt file")
    create_cmd.add_argument("--out-dir", default="outputs/xiaoyunque-video", help="output root directory")
    create_cmd.add_argument("--route", default="official-cli", choices=["official-cli", "xiaoyunque-web", "verified-api", "job-package-only"], help="intended route")
    create_cmd.add_argument("--model", default="seedance2.0_fast_direct", help="Xiaoyunque CLI model id or public UI label")
    create_cmd.add_argument("--mode", default="immersive-short", help="generation mode/type label")
    create_cmd.add_argument("--aspect-ratio", default="16:9", help="target aspect ratio")
    create_cmd.add_argument("--resolution", default="720p", help="target resolution, e.g. 720p or 1080p")
    create_cmd.add_argument("--duration", default="", help="target duration metadata, e.g. 5s; pass an integer such as 5 to the real CLI")
    create_cmd.add_argument("--reference", action="append", default=[], help="reference path plus optional role, e.g. image.png:style")
    create_cmd.add_argument("--note", action="append", default=[], help="extra job note")
    create_cmd.add_argument("--require-key", action="store_true", help="fail if neither XYQ_ACCESS_KEY nor compatibility fallback XIAOYUNQUE_API_KEY is visible")
    create_cmd.add_argument("--cost-confirmation", default="not-confirmed", choices=["not-confirmed", "user-confirmed", "dry-run-only"], help="paid-run confirmation state")
    create_cmd.add_argument("--estimated-cost-note", default="", help="human-readable cost/credit note; do not include secrets")
    create_cmd.set_defaults(func=create)

    wait_cmd = sub.add_parser("wait-result", help="poll query-result until completion and download outputs")
    wait_cmd.add_argument("--thread-id", required=True, help="thread_id from generate-video")
    wait_cmd.add_argument("--run-id", required=True, help="run_id from generate-video")
    wait_cmd.add_argument("--download-dir", required=True, help="directory for downloaded videos")
    wait_cmd.add_argument("--job-json", default="", help="optional job.json to update")
    wait_cmd.add_argument("--max-wait", type=int, default=600, help="maximum wait seconds; default 600")
    wait_cmd.add_argument("--interval", type=int, default=60, help="poll interval seconds; default 60")
    wait_cmd.add_argument("--cli", default="~/.npm-global/bin/pippit-tool-cli", help="pippit-tool-cli path")
    wait_cmd.set_defaults(func=wait_result)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
