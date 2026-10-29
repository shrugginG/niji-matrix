#!/usr/bin/env python3
"""Shared helpers for Niji Matrix global-library tooling."""

from __future__ import annotations

import hashlib
import json
import re
import unicodedata
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import yaml


ROOT = Path(__file__).resolve().parents[1]
CONTENT_PATHS = (
    "matrix.yaml",
    "matrix",
    "mechanisms",
    "references",
    "claims",
    "cases",
    "detections",
    "analytics",
    "mitigations",
    "relationships",
)
LIBRARY_TYPES = (
    "reference",
    "claim",
    "case",
    "detection-strategy",
    "detection-analytic",
    "mitigation",
    "relationship",
)
TRACKING_PARAMETERS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
    "ref",
    "source",
}
DOI_PATTERN = re.compile(r"10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)


def iter_yaml_files(root: Path = ROOT) -> Iterable[Path]:
    for name in CONTENT_PATHS:
        location = root / name
        if location.is_file():
            yield location
        elif location.exists():
            yield from sorted(location.rglob("*.yaml"))


def load_objects(root: Path = ROOT) -> tuple[dict[str, dict[str, Any]], dict[str, Path]]:
    root = root.resolve()
    objects: dict[str, dict[str, Any]] = {}
    paths: dict[str, Path] = {}
    for path in iter_yaml_files(root):
        with path.open(encoding="utf-8") as handle:
            value = yaml.safe_load(handle)
        if not isinstance(value, dict) or not isinstance(value.get("id"), str):
            continue
        object_id = value["id"]
        if object_id in objects:
            raise ValueError(f"duplicate object id: {object_id}")
        objects[object_id] = value
        paths[object_id] = path
    return objects, paths


def normalize_text(value: Any) -> str:
    text = unicodedata.normalize("NFKC", str(value or "")).casefold()
    text = re.sub(r"[^\w\u3400-\u9fff]+", " ", text, flags=re.UNICODE)
    return " ".join(text.split())


def extract_doi(value: dict[str, Any] | str | None) -> str | None:
    if isinstance(value, dict):
        explicit = value.get("identifiers", {}).get("doi")
        candidates = [
            explicit,
            value.get("url"),
            value.get("title_en"),
            value.get("title_zh"),
        ]
    else:
        candidates = [value]
    for candidate in candidates:
        if not candidate:
            continue
        match = DOI_PATTERN.search(str(candidate))
        if match:
            return match.group(0).rstrip(".,;:)]}").casefold()
    return None


def canonicalize_url(value: str | None) -> str | None:
    if not value:
        return None
    raw = value.strip()
    doi = extract_doi(raw)
    if doi and ("doi.org" in raw.casefold() or raw.casefold().startswith("doi:")):
        return f"https://doi.org/{doi}"
    try:
        parsed = urlsplit(raw)
    except ValueError:
        return raw
    if not parsed.scheme or not parsed.netloc:
        return raw
    scheme = parsed.scheme.casefold()
    hostname = (parsed.hostname or "").casefold()
    port = parsed.port
    netloc = hostname
    if port and not (
        (scheme == "http" and port == 80)
        or (scheme == "https" and port == 443)
    ):
        netloc = f"{hostname}:{port}"
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    if path != "/":
        path = path.rstrip("/")
    query = [
        (key, item)
        for key, item in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.casefold().startswith("utm_")
        and key.casefold() not in TRACKING_PARAMETERS
    ]
    return urlunsplit((scheme, netloc, path, urlencode(sorted(query)), ""))


def walk_object_ids(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for child in value.values():
            yield from walk_object_ids(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_object_ids(child)
    elif isinstance(value, str) and re.fullmatch(
        r"(?:TA\d{4}|NJT-\d{4}|NJS-\d{4}-\d{3}|NM-[A-Z]{2}|DEC-[A-Z0-9-]+|"
        r"CLM-\d{6}|CASE-\d{6}|DET-\d{6}|NJA-\d{6}|MIT-\d{6}|REL-\d{6}|REF-\d{6})",
        value,
    ):
        yield value


def display_names(value: dict[str, Any]) -> tuple[str, str]:
    nested = value.get("name")
    if isinstance(nested, dict):
        return str(nested.get("zh") or value.get("id", "")), str(
            nested.get("en") or value.get("id", "")
        )
    zh = (
        value.get("name_zh")
        or value.get("title_zh")
        or value.get("statement_zh")
        or value.get("id", "")
    )
    en = (
        value.get("name_en")
        or value.get("title_en")
        or value.get("statement_en")
        or value.get("id", "")
    )
    return str(zh), str(en)


def summary_values(value: dict[str, Any]) -> tuple[str, str]:
    nested = value.get("summary")
    if isinstance(nested, dict):
        return str(nested.get("zh", "")), str(nested.get("en", ""))
    object_type = value.get("type")
    field_pairs = {
        "reference": ("notes_zh", "notes_en"),
        "claim": ("statement_zh", "statement_en"),
        "case": ("description_zh", "description_en"),
        "relationship": ("description_zh", "description_en"),
    }
    zh_field, en_field = field_pairs.get(str(object_type), ("", ""))
    return str(value.get(zh_field, "")), str(value.get(en_field, ""))


def semantic_material(value: dict[str, Any]) -> dict[str, Any]:
    fields = {
        "claim": (
            "claim_type",
            "statement_zh",
            "statement_en",
            "evidence_mode",
        ),
        "case": (
            "name_zh",
            "name_en",
            "actor_or_campaign",
            "description_zh",
            "description_en",
            "time_range",
        ),
        "detection-strategy": (
            "summary",
            "description",
            "detects_refs",
            "analytic_refs",
        ),
        "detection-analytic": (
            "summary",
            "logic",
            "data_requirements",
            "observables",
            "correlation",
            "false_positives",
            "blind_spots",
        ),
        "mitigation": (
            "summary",
            "description",
            "measures",
            "applications",
        ),
        "relationship": (
            "relationship_type",
            "source_ref",
            "target_ref",
            "description_zh",
            "description_en",
        ),
    }.get(str(value.get("type")), ())
    return {field: value.get(field) for field in fields}


def normalized_structure(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: normalized_structure(value[key])
            for key in sorted(value)
        }
    if isinstance(value, list):
        normalized = (normalized_structure(item) for item in value)
        return sorted(
            normalized,
            key=lambda item: json.dumps(item, ensure_ascii=False, sort_keys=True),
        )
    if isinstance(value, str):
        return normalize_text(value)
    return value


def semantic_fingerprint(value: dict[str, Any]) -> str | None:
    material = semantic_material(value)
    if not material:
        return None
    payload = json.dumps(
        normalized_structure(material),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def identity_keys(value: dict[str, Any]) -> list[str]:
    if value.get("type") != "reference":
        fingerprint = semantic_fingerprint(value)
        return [f"semantic:{fingerprint}"] if fingerprint else []
    keys: list[str] = []
    doi = extract_doi(value)
    if doi:
        keys.append(f"doi:{doi}")
    identifiers = value.get("identifiers") or {}
    for kind in ("rfc", "arxiv", "attack_id"):
        identifier = normalize_text(identifiers.get(kind))
        if identifier:
            keys.append(f"identifier:{kind}:{identifier}")
    for identifier in identifiers.get("other", []):
        normalized = normalize_text(identifier)
        if normalized:
            keys.append(f"identifier:other:{normalized}")
    canonical_url = canonicalize_url(value.get("url"))
    if canonical_url:
        keys.append(f"url:{canonical_url}")
    title = normalize_text(value.get("title_en") or value.get("title_zh"))
    author = normalize_text((value.get("authors") or [""])[0])
    published = normalize_text(value.get("published"))
    if title:
        keys.append(f"bibliographic:{title}|{author}|{published}")
    return keys


def build_catalog(root: Path = ROOT) -> dict[str, Any]:
    root = root.resolve()
    objects, paths = load_objects(root)
    used_by: dict[str, set[str]] = defaultdict(set)
    for source_id, value in objects.items():
        for target_id in walk_object_ids(value):
            if target_id != source_id and target_id in objects:
                used_by[target_id].add(source_id)

    grouped: dict[str, list[dict[str, Any]]] = {
        object_type: [] for object_type in LIBRARY_TYPES
    }
    for object_id, value in objects.items():
        object_type = value.get("type")
        if object_type not in grouped:
            continue
        label_zh, label_en = display_names(value)
        summary_zh, summary_en = summary_values(value)
        entry: dict[str, Any] = {
            "id": object_id,
            "type": object_type,
            "path": paths[object_id].relative_to(root).as_posix(),
            "label_zh": label_zh,
            "label_en": label_en,
            "summary_zh": summary_zh,
            "summary_en": summary_en,
            "status": value.get("status")
            or value.get("lifecycle", {}).get("status"),
            "identity_keys": identity_keys(value),
            "semantic_fingerprint": semantic_fingerprint(value),
            "used_by": sorted(used_by.get(object_id, set())),
        }
        if object_type == "reference":
            entry.update(
                {
                    "doi": extract_doi(value),
                    "canonical_url": canonicalize_url(value.get("url")),
                    "source_type": value.get("source_type"),
                    "published": value.get("published"),
                    "authors": value.get("authors", []),
                }
            )
        grouped[object_type].append(entry)
    for values in grouped.values():
        values.sort(key=lambda item: item["id"])
    return {
        "catalog_schema_version": "1.0.0",
        "source_root": str(root),
        "counts": {key: len(value) for key, value in grouped.items()},
        "libraries": grouped,
    }


def flat_entries(catalog: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        item
        for values in catalog.get("libraries", {}).values()
        for item in values
    ]
