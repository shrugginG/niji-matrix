#!/usr/bin/env python3
"""Preview, reserve, consume, archive, or release globally unique Niji object IDs."""

from __future__ import annotations

import argparse
import fcntl
import os
import re
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from library_common import ROOT, load_objects


ID_SPECS = {
    "NJT": ("NJT-", 4),
    "NJS": ("NJS-", 3),
    "NJA": ("NJA-", 6),
    "REF": ("REF-", 6),
    "CLM": ("CLM-", 6),
    "CASE": ("CASE-", 6),
    "DET": ("DET-", 6),
    "MIT": ("MIT-", 6),
    "REL": ("REL-", 6),
}


def reservation_path(root: Path) -> Path:
    return root / "planning" / "id-reservations.yaml"


def load_reservations(root: Path) -> dict[str, Any]:
    path = reservation_path(root)
    if not path.is_file():
        return {
            "schema_version": "1.0.0",
            "type": "id-reservations",
            "reservations": [],
        }
    with path.open(encoding="utf-8") as handle:
        value = yaml.safe_load(handle)
    if (
        not isinstance(value, dict)
        or value.get("type") != "id-reservations"
        or not isinstance(value.get("reservations"), list)
    ):
        raise ValueError(f"invalid reservation registry: {path}")
    return value


def write_reservations(root: Path, value: dict[str, Any]) -> None:
    path = reservation_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = yaml.safe_dump(value, allow_unicode=True, sort_keys=False)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=".id-reservations-",
        suffix=".tmp",
        delete=False,
    ) as handle:
        handle.write(text)
        temporary = Path(handle.name)
    os.replace(temporary, path)


def existing_ids(root: Path) -> set[str]:
    objects, _ = load_objects(root)
    return set(objects)


def entity_for_id(object_id: str) -> str | None:
    if re.fullmatch(r"NJS-\d{4}-\d{3}", object_id):
        return "NJS"
    if re.fullmatch(r"NJS-\d{4}", object_id):
        return "NJS"
    for entity, (prefix, width) in ID_SPECS.items():
        if re.fullmatch(rf"{re.escape(prefix)}\d{{{width}}}", object_id):
            return entity
    return None


def next_ids(
    entity: str,
    count: int,
    occupied: set[str],
    parent: str | None = None,
) -> list[str]:
    if entity == "NJS":
        if not parent or not re.fullmatch(r"NJT-\d{4}", parent):
            raise ValueError("NJS allocation requires --parent NJT-xxxx")
        prefix = f"NJS-{parent.removeprefix('NJT-')}-"
        width = 3
    else:
        prefix, width = ID_SPECS[entity]
    values: list[str] = []
    existing_numbers = [
        int(object_id.removeprefix(prefix))
        for object_id in occupied
        if re.fullmatch(rf"{re.escape(prefix)}\d{{{width}}}", object_id)
    ]
    number = max(existing_numbers, default=0) + 1
    while len(values) < count:
        candidate = f"{prefix}{number:0{width}d}"
        if candidate not in occupied:
            values.append(candidate)
            occupied.add(candidate)
        number += 1
    return values


def occupied_ids(root: Path, registry: dict[str, Any]) -> set[str]:
    occupied = existing_ids(root)
    occupied.update(
        item["id"]
        for item in registry["reservations"]
        if isinstance(item, dict)
        and isinstance(item.get("id"), str)
    )
    return occupied


def lock_registry(root: Path):
    lock_path = root / "planning" / ".id-reservations.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    handle = lock_path.open("a+", encoding="utf-8")
    fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
    return handle


def command_next(args: argparse.Namespace) -> int:
    registry = load_reservations(args.root)
    for object_id in next_ids(
        args.entity,
        args.count,
        occupied_ids(args.root, registry),
        getattr(args, "parent", None),
    ):
        print(object_id)
    return 0


def command_reserve(args: argparse.Namespace) -> int:
    with lock_registry(args.root):
        registry = load_reservations(args.root)
        values = next_ids(
            args.entity,
            args.count,
            occupied_ids(args.root, registry),
            getattr(args, "parent", None),
        )
        now = datetime.now(timezone.utc).isoformat()
        registry["reservations"].extend(
            {
                "id": object_id,
                "entity": args.entity,
                "owner": args.owner,
                "status": "reserved",
                "created": now,
                "updated": now,
            }
            for object_id in values
        )
        write_reservations(args.root, registry)
    print("\n".join(values))
    return 0


def update_reservation(
    root: Path,
    object_id: str,
    owner: str | None,
    target_status: str,
) -> int:
    with lock_registry(root):
        registry = load_reservations(root)
        item = next(
            (
                candidate
                for candidate in registry["reservations"]
                if candidate.get("id") == object_id
            ),
            None,
        )
        if not item:
            raise ValueError(f"ID is not reserved: {object_id}")
        if owner and item.get("owner") != owner:
            raise ValueError(
                f"{object_id} belongs to {item.get('owner')}, not {owner}"
            )
        if target_status == "released" and item.get("status") != "reserved":
            raise ValueError(
                f"only reserved IDs can be released: {object_id} "
                f"is {item.get('status')}"
            )
        if target_status == "consumed" and item.get("status") in {"released", "archived"}:
            raise ValueError(
                f"{item.get('status')} ID cannot be consumed: {object_id}"
            )
        if target_status == "archived" and object_id in existing_ids(root):
            raise ValueError(
                f"canonical object must be moved before archiving ID: {object_id}"
            )
        if target_status == "consumed" and object_id not in existing_ids(root):
            raise ValueError(
                f"canonical object must exist before consuming ID: {object_id}"
            )
        if target_status == "released" and object_id in existing_ids(root):
            raise ValueError(f"an existing object ID cannot be released: {object_id}")
        item["status"] = target_status
        item["updated"] = datetime.now(timezone.utc).isoformat()
        write_reservations(root, registry)
    print(f"{object_id}: {target_status}")
    return 0


def command_list(args: argparse.Namespace) -> int:
    registry = load_reservations(args.root)
    values = registry["reservations"]
    if args.status:
        values = [item for item in values if item.get("status") == args.status]
    if not values:
        print("无 ID 预留记录。")
        return 0
    for item in values:
        print(
            f"{item.get('id', '-'):<12} {item.get('status', '-'):<9} "
            f"{item.get('owner', '-')}"
        )
    return 0


def command_sync(args: argparse.Namespace) -> int:
    with lock_registry(args.root):
        registry = load_reservations(args.root)
        existing = existing_ids(args.root)
        now = datetime.now(timezone.utc).isoformat()
        changed: list[str] = []
        for item in registry["reservations"]:
            if item.get("status") == "reserved" and item.get("id") in existing:
                item["status"] = "consumed"
                item["updated"] = now
                changed.append(item["id"])
        if changed:
            write_reservations(args.root, registry)
    print(f"已同步 {len(changed)} 个正式对象 ID。")
    for object_id in changed:
        print(object_id)
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    subparsers = parser.add_subparsers(dest="command", required=True)

    for command in ("next", "reserve"):
        child = subparsers.add_parser(command)
        child.add_argument("entity", choices=ID_SPECS)
        child.add_argument("--count", type=int, default=1)
        child.add_argument("--parent")
        if command == "reserve":
            child.add_argument("--owner", required=True)

    for command in ("consume", "release", "archive"):
        child = subparsers.add_parser(command)
        child.add_argument("object_id")
        child.add_argument("--owner")

    child = subparsers.add_parser("list")
    child.add_argument(
        "--status",
        choices=("reserved", "consumed", "archived", "released"),
    )
    subparsers.add_parser("sync")
    args = parser.parse_args()
    args.root = args.root.resolve()
    if getattr(args, "count", 1) < 1:
        parser.error("--count must be positive")
    if getattr(args, "entity", None) == "NJS" and not getattr(args, "parent", None):
        parser.error("NJS allocation requires --parent NJT-xxxx")
    if getattr(args, "parent", None) and getattr(args, "entity", None) != "NJS":
        parser.error("--parent is valid only for NJS allocation")
    return args


def main() -> int:
    args = parse_args()
    if args.command in {"next", "reserve"}:
        handler = command_next if args.command == "next" else command_reserve
        return handler(args)
    if args.command == "consume":
        if not entity_for_id(args.object_id):
            raise ValueError(f"unsupported object ID: {args.object_id}")
        return update_reservation(
            args.root,
            args.object_id,
            args.owner,
            "consumed",
        )
    if args.command in {"release", "archive"}:
        if not entity_for_id(args.object_id):
            raise ValueError(f"unsupported object ID: {args.object_id}")
        return update_reservation(
            args.root,
            args.object_id,
            args.owner,
            "released" if args.command == "release" else "archived",
        )
    if args.command == "sync":
        return command_sync(args)
    return command_list(args)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValueError as exc:
        raise SystemExit(f"ERROR: {exc}") from exc
