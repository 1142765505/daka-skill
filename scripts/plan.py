"""Parse a numbered-person request; visual presence must be supplied by the agent."""
import argparse
import json
from pathlib import Path
import re
import unicodedata
from datetime import datetime
import uuid

ROOT = Path(__file__).resolve().parents[1]
LIMITS = {"401": 10, "403": 4}


def ids(value, room):
    if value is None:
        return None
    if isinstance(value, str):
        if value.strip().lower() in ("none", "无", ""):
            return []
        pieces = re.split(r"[、,，\s]+", value.strip())
        if any(not re.fullmatch(r"[0-9]+", p) for p in pieces):
            raise ValueError("编号必须为用顿号或逗号分隔的整数")
        value = [int(p) for p in pieces]
    if any(type(n) is not int or not 1 <= n <= LIMITS[room] for n in value):
        raise ValueError(f"{room}编号仅允许1–{LIMITS[room]}")
    return sorted(set(value))


def parse(command):
    text = unicodedata.normalize("NFKC", command).strip()
    text = re.sub(r"^(?:使用\s*)?(?:打卡\s*skill|\$?daka-skill)\s*[,，:：]?\s*", "", text, flags=re.I)
    match = re.fullmatch(r"(?:(401|403)\s*)?增加\s*(全部|[0-9]+(?:\s*[、,，]\s*[0-9]+)*)[。！!]?", text)
    if not match:
        raise ValueError("请使用‘401增加3、4、5’、‘403增加1、2’或‘增加全部’")
    room = match[1] or "401"
    requested = list(range(1, LIMITS[room]+1)) if match[2] == "全部" else ids(match[2], room)
    return room, requested


def plan(command, has_input=False, present=None, uncertain=None):
    room, requested = parse(command)
    p = ids(present, room) if has_input else []
    u = ids(uncertain or [], room) if has_input else []
    if p is not None and set(p) & set(u):
        raise ValueError("同一编号不能既已存在又不确定")
    pending = sorted(set(requested) & set(u))
    state = "requires_visual_check" if has_input and p is None else "needs_clarification" if pending else "ready"
    skipped = sorted(set(requested) & set(p or []))
    additions = sorted(set(requested) - set(p or []) - set(u))
    if has_input and state == "ready" and not additions:
        state = "noop"
    return {"room": room, "mode": "edit" if has_input else "reconstruct", "state": state,
            "requested": requested, "present": p, "uncertain": u, "skipped": skipped,
            "to_add": additions if state in ("ready", "noop") else [],
            "final_numbered_people": sorted(set(p or []) | set(requested)) if has_input and state == "ready" else (p if state == "noop" else requested if not has_input else None),
            "preserve_unrequested_existing_people": has_input,
            "forbid_other_people": not has_input,
            "candidate_count": 1 if state == "ready" else 0,
            "provenance": "AI合成图；参考库不是已训练模型"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--command", required=True)
    parser.add_argument("--has-input", action="store_true")
    parser.add_argument("--present", help="实际视觉核对后的已有编号，无人则填none；省略表示未核对")
    parser.add_argument("--uncertain")
    parser.add_argument("--create-run", action="store_true")
    args = parser.parse_args()
    result = plan(args.command, args.has_input, args.present, args.uncertain)
    if args.create_run:
        if result["state"] != "ready":
            parser.error("当前任务无需生成或尚未核对，不能创建生成任务")
        run = ROOT / "output" / (datetime.now().strftime("%Y%m%d_%H%M%S") + "_" + result["room"] + "_" + "-".join(map(str,result["requested"])) + "_" + uuid.uuid4().hex[:6])
        run.mkdir(parents=True, exist_ok=False)
        (run / "request.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        result["run_directory"] = str(run)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
