#!/usr/bin/env python3
"""Read-only delivery checks; these are not native AutoCAD or geometry checks."""

import argparse
import hashlib
import json
import math
import sys
import zipfile
from pathlib import Path, PurePosixPath


SIGNATURES = {"2004": b"AC1018", "2010": b"AC1024"}


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest()


def inspect_dwg(path, version):
    with path.open("rb") as stream:
        header = stream.read(6)
    expected = SIGNATURES.get(version)
    # A matching prefix never establishes that the full DWG is valid.
    signature_ok = header == expected if expected else (
        len(header) == 6 and header[:2] == b"AC" and header[2:].isdigit()
    )
    return {"name": path.name, "bytes": path.stat().st_size,
            "sha256": digest(path), "header": header.decode("ascii", "replace"),
            "expected_version": version, "signature_match": signature_ok,
            "native_open": "not_run"}


def inspect_pdf(path, expected_pages, paper_mm, tolerance):
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise RuntimeError("PDF checks require pypdf in this Python environment") from exc
    reader = PdfReader(str(path), strict=True)
    rows = []
    for index, page in enumerate(reader.pages, 1):
        # Include PDF /UserUnit and display rotation when reporting paper size.
        unit = float(page.get("/UserUnit", 1))
        box = page.mediabox
        width = float(box.width) * unit * 25.4 / 72
        height = float(box.height) * unit * 25.4 / 72
        if int(page.rotation) % 180 == 90:
            width, height = height, width
        actual = (width, height)
        valid_size = all(math.isfinite(v) and v > 0 for v in actual)
        match = valid_size and (paper_mm is None or all(
            abs(a - b) <= tolerance for a, b in zip(actual, paper_mm)
        ))
        rows.append({"page": index, "paper_mm": list(actual), "paper_match": match})
    count = len(rows)
    return {"name": path.name, "bytes": path.stat().st_size, "sha256": digest(path),
            "page_count": count, "page_count_match": count > 0 and (
                expected_pages is None or count == expected_pages), "pages": rows,
            "content_scale": "not_checked", "visual_review": "not_run"}


def inspect_zip(path, expected):
    members = []
    with zipfile.ZipFile(path) as archive:
        bad_member = archive.testzip()
        for source in expected:
            candidates = [info for info in archive.infolist() if not info.is_dir()
                          and PurePosixPath(info.filename).name == source.name]
            match = False
            if len(candidates) == 1:
                result = hashlib.sha256()
                with archive.open(candidates[0]) as stream:
                    for block in iter(lambda: stream.read(1024 * 1024), b""):
                        result.update(block)
                match = result.hexdigest() == digest(source)
            members.append({"name": source.name, "matching_names": len(candidates),
                            "matches_final_file": match})
    return {"name": path.name, "sha256": digest(path), "crc_ok": bad_member is None,
            "members": members}


def load_task_plan(path):
    """Resolve explicit task expectations; never infer tasks from filenames."""
    plan = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(plan, dict) or not isinstance(plan.get("tasks"), list) or not plan["tasks"]:
        raise ValueError("plan must contain a nonempty tasks list")
    base = path.resolve().parent

    def locate(value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("each artifact path must be a nonempty string")
        candidate = Path(value)
        return candidate.resolve() if candidate.is_absolute() else (base / candidate).resolve()

    identifiers, pdf_paths = set(), set()
    pdf_jobs = []
    for task in plan["tasks"]:
        if not isinstance(task, dict):
            raise ValueError("each task must be an object")
        identifier = task.get("id")
        if not isinstance(identifier, str) or not identifier.strip() or identifier in identifiers:
            raise ValueError("task IDs must be nonempty and unique")
        identifiers.add(identifier)
        pages = task.get("pages")
        if type(pages) is not int or pages <= 0:
            raise ValueError("each task must declare a positive integer pages value")
        paper = task.get("paper_mm")
        if paper is not None and (not isinstance(paper, list) or len(paper) != 2 or any(
                type(v) not in (int, float) or not math.isfinite(v) or v <= 0 for v in paper)):
            raise ValueError("paper_mm must contain two finite positive numbers")
        pdf_path = locate(task.get("pdf"))
        if pdf_path in pdf_paths:
            raise ValueError("per-task PDF paths must be distinct; a multi-page task uses one entry")
        pdf_paths.add(pdf_path)
        pdf_jobs.append((pdf_path, pages, paper, identifier))
    dwg_entries = plan.get("dwg", [])
    if not isinstance(dwg_entries, list):
        raise ValueError("plan dwg must be a list")
    dwg_jobs = []
    for entry in dwg_entries:
        if not isinstance(entry, dict):
            raise ValueError("each dwg entry must be an object")
        version = entry.get("version")
        if version is not None and version not in SIGNATURES:
            raise ValueError("DWG version must be 2004 or 2010 when specified")
        dwg_jobs.append((locate(entry.get("path")), version))
    all_paths = [j[0] for j in dwg_jobs + pdf_jobs]
    if len(all_paths) != len(set(all_paths)):
        raise ValueError("plan artifact paths must not be duplicated")
    archive = locate(plan["zip"]) if "zip" in plan else None
    return dwg_jobs, pdf_jobs, archive


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dwg", type=Path, action="append", default=[])
    parser.add_argument("--dwg-version", choices=sorted(SIGNATURES))
    parser.add_argument("--pdf", type=Path, action="append", default=[])
    parser.add_argument("--pages", type=int)
    parser.add_argument("--paper-mm", nargs=2, type=float, metavar=("WIDTH", "HEIGHT"))
    parser.add_argument("--tolerance-mm", type=float, default=0.2)
    parser.add_argument("--zip", type=Path, dest="archive")
    parser.add_argument("--plan", type=Path, help="JSON mapping each task to a PDF and expected pages")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if args.plan:
        if args.dwg or args.pdf or args.dwg_version or args.pages is not None or args.paper_mm or args.archive:
            parser.error("--plan cannot be combined with --dwg/--pdf or their expectations/--zip")
        try:
            dwg_jobs, pdf_jobs, args.archive = load_task_plan(args.plan)
        except (OSError, ValueError, TypeError) as exc:
            parser.error(f"invalid task plan: {exc}")
    else:
        dwg_jobs = [(path, args.dwg_version) for path in args.dwg]
        pdf_jobs = [(path, args.pages, args.paper_mm, None) for path in args.pdf]
    expected = [job[0] for job in dwg_jobs + pdf_jobs]
    if not expected:
        parser.error("provide --plan or at least one --dwg or --pdf")
    if args.pages is not None and args.pages <= 0:
        parser.error("--pages must be positive")
    if not math.isfinite(args.tolerance_mm) or args.tolerance_mm < 0:
        parser.error("--tolerance-mm must be finite and nonnegative")
    if args.paper_mm and any(not math.isfinite(v) or v <= 0 for v in args.paper_mm):
        parser.error("--paper-mm values must be finite and positive")
    inputs = expected + ([args.archive] if args.archive else []) + ([args.plan] if args.plan else [])
    if args.report and args.report.resolve() in {p.resolve() for p in inputs}:
        parser.error("--report must not overwrite an input")
    if args.archive and len({p.name for p in expected}) != len(expected):
        parser.error("ZIP checks require unique expected basenames")
    report = {"structural_checks_passed": False, "dwg": [], "pdf": [], "zip": None, "task_summary": None,
              "task_plan": {"name": args.plan.name, "sha256": digest(args.plan)} if args.plan else None,
              "errors": [], "limits": ["No native AutoCAD open or AUDIT",
              "No geometry, fonts, dimensions, content scale or visual checks",
              "A task plan does not establish completeness against the original assignment"]}
    for path, version in dwg_jobs:
        try:
            row = inspect_dwg(path, version)
            report["dwg"].append(row)
            if not row["signature_match"]:
                report["errors"].append(f"DWG signature mismatch: {path.name}")
        except Exception as exc:
            report["errors"].append(f"{path.name}: {type(exc).__name__}: {exc}")
    for path, pages, paper, task_id in pdf_jobs:
        try:
            row = inspect_pdf(path, pages, paper, args.tolerance_mm)
            if task_id is not None:
                row["task_id"] = task_id
            report["pdf"].append(row)
            if not row["page_count_match"] or not all(p["paper_match"] for p in row["pages"]):
                report["errors"].append(f"PDF page count or paper size mismatch: {path.name}")
        except Exception as exc:
            report["errors"].append(f"{path.name}: {type(exc).__name__}: {exc}")
    if args.archive:
        try:
            row = inspect_zip(args.archive, expected)
            report["zip"] = row
            if not row["crc_ok"] or not all(m["matches_final_file"] for m in row["members"]):
                report["errors"].append("ZIP is damaged, missing/ambiguous, or contains stale files")
        except Exception as exc:
            report["errors"].append(f"{type(exc).__name__}: {exc}")
    if args.plan:
        report["task_summary"] = {"planned_tasks": len(pdf_jobs), "expected_pdf_files": len(pdf_jobs),
                                  "read_pdf_files": len(report["pdf"]),
                                  "expected_total_pages": sum(j[1] for j in pdf_jobs),
                                  "actual_total_pages": sum(r["page_count"] for r in report["pdf"])}
    report["structural_checks_passed"] = not report["errors"]
    output = json.dumps(report, ensure_ascii=False, indent=2)
    print(output)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output + "\n", encoding="utf-8")
    return 0 if report["structural_checks_passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
