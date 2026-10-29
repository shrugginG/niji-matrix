from __future__ import annotations

import sys
import tempfile
import unittest
from argparse import Namespace
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from allocate_id import (  # noqa: E402
    command_reserve,
    load_reservations,
    next_ids,
    update_reservation,
)
from audit_duplicates import audit  # noqa: E402
from library_common import (  # noqa: E402
    build_catalog,
    canonicalize_url,
    extract_doi,
)
from pipeline_status import build_status  # noqa: E402


class LibraryInfrastructureTest(unittest.TestCase):
    def test_catalog_indexes_global_libraries_and_reverse_usage(self) -> None:
        catalog = build_catalog(ROOT)
        self.assertGreaterEqual(catalog["counts"]["reference"], 19)
        self.assertGreaterEqual(catalog["counts"]["claim"], 9)
        references = {
            item["id"]: item
            for item in catalog["libraries"]["reference"]
        }
        self.assertEqual(
            references["REF-000006"]["doi"],
            "10.1371/journal.pone.0204507",
        )
        self.assertIn("NJT-0001", references["REF-000006"]["used_by"])

    def test_reference_identity_normalization(self) -> None:
        self.assertEqual(
            canonicalize_url(
                "HTTPS://Example.COM:443/report/?utm_source=test&b=2&a=1#page"
            ),
            "https://example.com/report?a=1&b=2",
        )
        self.assertEqual(
            extract_doi("https://doi.org/10.1371/JOURNAL.PONE.0204507"),
            "10.1371/journal.pone.0204507",
        )

    def test_duplicate_audit_has_no_exact_conflicts(self) -> None:
        self.assertEqual(audit(ROOT)["exact"], [])

    def test_allocator_skips_occupied_ids(self) -> None:
        self.assertEqual(
            next_ids("NJT", 2, {"NJT-0001", "NJT-0002"}),
            ["NJT-0003", "NJT-0004"],
        )
        self.assertEqual(
            next_ids("REF", 2, {"REF-000001", "REF-000003"}),
            ["REF-000004", "REF-000005"],
        )
        self.assertEqual(
            next_ids("NJA", 2, {"NJA-000001"}),
            ["NJA-000002", "NJA-000003"],
        )
        self.assertEqual(
            next_ids(
                "NJS",
                2,
                {"NJS-0042-001"},
                parent="NJT-0042",
            ),
            ["NJS-0042-002", "NJS-0042-003"],
        )
        with self.assertRaises(ValueError):
            next_ids("NJS", 1, set())

    def test_reservation_registry_is_monotonic_and_releasable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with redirect_stdout(StringIO()):
                command_reserve(
                    Namespace(
                        root=root,
                        entity="REF",
                        count=2,
                        owner="BATCH-TEST-001",
                    )
                )
                update_reservation(
                    root,
                    "REF-000002",
                    "BATCH-TEST-001",
                    "released",
                )
                command_reserve(
                    Namespace(
                        root=root,
                        entity="REF",
                        count=1,
                        owner="BATCH-TEST-002",
                    )
                )
            registry = load_reservations(root)
            self.assertEqual(
                [item["id"] for item in registry["reservations"]],
                ["REF-000001", "REF-000002", "REF-000003"],
            )
            self.assertEqual(
                registry["reservations"][1]["status"],
                "released",
            )

    def test_pipeline_reports_existing_plans(self) -> None:
        status = build_status(ROOT)
        tactics = {item["id"]: item for item in status["tactics"]}
        self.assertEqual(tactics["TA0043"]["plan_status"], "review")
        self.assertEqual(tactics["TA0005"]["plan_status"], "active")
        self.assertEqual(tactics["TA0043"]["inventory_status"], "complete")
        self.assertGreaterEqual(tactics["TA0043"]["techniques"], 3)
        self.assertGreaterEqual(tactics["TA0043"]["subtechniques"], 10)


if __name__ == "__main__":
    unittest.main()
