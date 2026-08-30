from __future__ import annotations

import csv
import fnmatch
import hashlib
import json
import os
import subprocess
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

CONFIG_FILE = Path(__file__).with_name("config.json")


AUTO_FIELDS = [
    "file_id",
    "filepath",
    "filename",
    "extension",
    "size_bytes",
    "content_hash",
    "created_at",
    "last_modified",
    "last_accessed",
    "git_last_modified",
    "git_last_commit",
    "git_commit_count",
    "scanned_at",
    "status",
    "change_type",
    "rename_source",
    "rename_confidence",
    "previous_filepath",
]

MANUAL_FIELDS = [
    "manual_last_reviewed",
    "manual_last_updated",
    "manual_notes",
    "review_priority",
    "quality_score",
]

ALL_FIELDS = AUTO_FIELDS + MANUAL_FIELDS

HISTORY_FIELDS = [
    "scan_id",
    "scan_started_at",
    "scan_completed_at",
    "total_files",
    "new_files",
    "modified_files",
    "renamed_files",
    "deleted_files",
    "unchanged_files",
]


# ============================================================================
# Configuration
# ============================================================================

def load_config() -> dict[str, Any]:
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {CONFIG_FILE}"
        )

    with CONFIG_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


# ============================================================================
# Time
# ============================================================================

def now() -> str:
    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def format_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


# ============================================================================
# File identity
# ============================================================================

def generate_file_id(
    repository_path: Path,
    relative_path: str,
) -> str:

    identity = (
        f"{repository_path.resolve()}::{relative_path}"
    )

    return hashlib.sha256(
        identity.encode("utf-8")
    ).hexdigest()


# ============================================================================
# Hashing
# ============================================================================

def calculate_file_hash(
    file_path: Path,
    algorithm: str = "sha256",
) -> str:

    hasher = hashlib.new(algorithm)

    with file_path.open("rb") as file:
        while chunk := file.read(1024 * 1024):
            hasher.update(chunk)

    return hasher.hexdigest()


# ============================================================================
# Exclusion
# ============================================================================

def matches_pattern(
    filename: str,
    patterns: list[str],
) -> bool:

    return any(
        fnmatch.fnmatch(
            filename,
            pattern,
        )
        for pattern in patterns
    )


def should_exclude_file(
    file_path: Path,
    config: dict[str, Any],
) -> bool:

    exclude_files = config.get(
        "exclude_files",
        [],
    )

    exclude_extensions = {
        extension.lower()
        for extension in config.get(
            "exclude_extensions",
            [],
        )
    }

    if matches_pattern(
        file_path.name,
        exclude_files,
    ):
        return True

    if file_path.suffix.lower() in exclude_extensions:
        return True

    return False


# ============================================================================
# Git
# ============================================================================

def is_git_repository(
    repository_path: Path,
) -> bool:

    return (repository_path / ".git").exists()


def run_git(
    repository_path: Path,
    arguments: list[str],
) -> str | None:

    try:
        result = subprocess.run(
            [
                "git",
                "-C",
                str(repository_path),
                *arguments,
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )

        if result.returncode != 0:
            return None

        return result.stdout.strip()

    except (
        FileNotFoundError,
        OSError,
    ):
        return None


def get_git_metadata(
    repository_path: Path,
    relative_path: str,
) -> dict[str, str]:

    result = run_git(
        repository_path,
        [
            "log",
            "-1",
            "--format=%H|%cI",
            "--",
            relative_path,
        ],
    )

    if not result:
        return {
            "git_last_modified": "",
            "git_last_commit": "",
            "git_commit_count": "0",
        }

    try:
        commit, timestamp = result.split("|", 1)

        parsed_timestamp = datetime.fromisoformat(
            timestamp
        )

        formatted_timestamp = parsed_timestamp.strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    except ValueError:
        commit = ""
        formatted_timestamp = ""

    count_result = run_git(
        repository_path,
        [
            "rev-list",
            "--count",
            "HEAD",
            "--",
            relative_path,
        ],
    )

    return {
        "git_last_modified": formatted_timestamp,
        "git_last_commit": commit,
        "git_commit_count": count_result or "0",
    }


def parse_git_rename_status(
    repository_path: Path,
) -> list[dict[str, Any]]:
    """
    Ask Git to detect renames across repository history.

    Git's -M option enables rename detection.

    Returns records such as:

        {
            "old_path": "notes/Python.md",
            "new_path": "notes/Python — Language.md",
            "similarity": 92
        }
    """

    result = run_git(
        repository_path,
        [
            "log",
            "--all",
            "--name-status",
            "-M",
            "--diff-filter=R",
            "--format=",
        ],
    )

    if not result:
        return []

    renames: list[dict[str, Any]] = []

    for line in result.splitlines():

        line = line.strip()

        if not line:
            continue

        parts = line.split("\t")

        if len(parts) != 3:
            continue

        status, old_path, new_path = parts

        if not status.startswith("R"):
            continue

        try:
            similarity = int(
                status[1:]
            )
        except ValueError:
            similarity = 0

        renames.append(
            {
                "old_path": old_path,
                "new_path": new_path,
                "similarity": similarity,
            }
        )

    return renames


def parse_git_worktree_renames(
    repository_path: Path,
) -> list[dict[str, Any]]:
    """
    Detect renames that exist in the current Git working tree,
    including staged and unstaged changes.

    Example Git output:

        R  notes/Python.md -> notes/Python — Language.md
    """

    result = run_git(
        repository_path,
        [
            "status",
            "--porcelain=v1",
            "-M",
        ],
    )

    if not result:
        return []

    renames: list[dict[str, Any]] = []

    for line in result.splitlines():

        if not line:
            continue

        # Porcelain format:
        #
        # XY path
        #
        # Rename:
        #
        # XY old -> new
        #
        # We are interested in status beginning with R.
        status = line[:2]

        if "R" not in status:
            continue

        path_part = line[3:]

        if " -> " not in path_part:
            continue

        old_path, new_path = path_part.split(
            " -> ",
            1,
        )

        renames.append(
            {
                "old_path": old_path,
                "new_path": new_path,
                "similarity": 100,
            }
        )

    return renames


def detect_git_renames(
    repository_path: Path,
    previous_records: dict[str, dict[str, str]],
    current_records: list[dict[str, str]],
) -> set[str]:
    """
    Second-stage rename detection using Git.

    Stage 1:
        content hash

    Stage 2:
        Git rename detection

    Returns file IDs from the previous snapshot that have
    been identified as renamed.
    """

    git_renames = get_git_renames(
        repository_path
    )

    if not git_renames:
        return set()

    previous_by_path = {
        record["filepath"]: record
        for record in previous_records.values()
        if record.get("status") == "active"
    }

    current_by_path = {
        record["filepath"]: record
        for record in current_records
        if record.get("status") == "active"
    }

    renamed_previous_ids: set[str] = set()

    for rename in git_renames:

        old_path = rename["old_path"]
        new_path = rename["new_path"]

        previous = previous_by_path.get(
            old_path
        )

        current = current_by_path.get(
            new_path
        )

        # We need both sides to exist in the
        # expected snapshots.
        if previous is None:
            continue

        if current is None:
            continue

        # If they are already the same path,
        # this isn't useful for rename detection.
        if old_path == new_path:
            continue

        similarity = rename.get(
            "similarity",
            0,
        )

        current["change_type"] = "renamed"

        current["rename_source"] = "git"

        current["rename_confidence"] = (
            f"{similarity / 100:.2f}"
        )

        current["previous_filepath"] = old_path

        # Preserve manual metadata.
        for field in MANUAL_FIELDS:
            current[field] = previous.get(
                field,
                "",
            )

        renamed_previous_ids.add(
            previous["file_id"]
        )

    return renamed_previous_ids


# ============================================================================
# Existing metadata
# ============================================================================

def load_metadata(
    metadata_file: Path,
) -> dict[str, dict[str, str]]:

    if not metadata_file.exists():
        return {}

    records: dict[str, dict[str, str]] = {}

    with metadata_file.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            file_id = row.get("file_id")

            if not file_id:
                continue

            records[file_id] = {
                field: row.get(field, "")
                for field in ALL_FIELDS
            }

    return records


# ============================================================================
# File scanning
# ============================================================================

def scan_repository(
    repository_path: Path,
    config: dict[str, Any],
) -> list[dict[str, str]]:

    exclude_dirs = set(
        config.get(
            "exclude_dirs",
            [],
        )
    )

    follow_symlinks = config.get(
        "follow_symlinks",
        False,
    )

    calculate_hash = config.get(
        "calculate_content_hash",
        True,
    )

    hash_algorithm = config.get(
        "hash_algorithm",
        "sha256",
    )

    collect_git = (
        config.get(
            "collect_git_metadata",
            True,
        )
        and is_git_repository(repository_path)
    )

    scanned_at = now()

    records: list[dict[str, str]] = []

    for root, dirs, files in os.walk(
        repository_path,
        followlinks=follow_symlinks,
    ):

        root_path = Path(root)

        dirs[:] = [
            directory
            for directory in dirs
            if directory not in exclude_dirs
        ]

        for filename in files:

            file_path = root_path / filename

            if should_exclude_file(
                file_path,
                config,
            ):
                continue

            try:
                stat = file_path.stat(
                    follow_symlinks=follow_symlinks
                )

                relative_path = file_path.relative_to(
                    repository_path
                )

                relative_path_str = str(
                    relative_path
                )

            except (
                OSError,
                PermissionError,
            ) as exc:

                print(
                    f"[WARNING] Unable to inspect "
                    f"{file_path}: {exc}"
                )

                continue

            file_id = generate_file_id(
                repository_path,
                relative_path_str,
            )

            content_hash = ""

            if calculate_hash:

                try:
                    content_hash = calculate_file_hash(
                        file_path,
                        hash_algorithm,
                    )

                except (
                    OSError,
                    PermissionError,
                ) as exc:

                    print(
                        f"[WARNING] Unable to hash "
                        f"{file_path}: {exc}"
                    )

            git_metadata = {
                "git_last_modified": "",
                "git_last_commit": "",
                "git_commit_count": "0",
            }

            if collect_git:

                git_metadata = get_git_metadata(
                    repository_path,
                    relative_path_str,
                )

            record = {
                "file_id": file_id,

                "filepath": relative_path_str,

                "filename": file_path.name,

                "extension": file_path.suffix.lower(),

                "size_bytes": str(
                    stat.st_size
                ),

                "content_hash": content_hash,

                "created_at": format_timestamp(
                    stat.st_ctime
                ),

                "last_modified": format_timestamp(
                    stat.st_mtime
                ),

                "last_accessed": format_timestamp(
                    stat.st_atime
                ),

                "git_last_modified":
                    git_metadata[
                        "git_last_modified"
                    ],

                "git_last_commit":
                    git_metadata[
                        "git_last_commit"
                    ],

                "git_commit_count":
                    git_metadata[
                        "git_commit_count"
                    ],

                "scanned_at": scanned_at,

                "status": "active",

                "change_type": "unknown",

                "rename_source": "",
                "rename_confidence": "",
                "previous_filepath": "",

                # Manual fields initially empty.
                "manual_last_reviewed": "",
                "manual_last_updated": "",
                "manual_notes": "",
                "review_priority": "",
                "quality_score": "",
            }

            records.append(record)

    return records


# ============================================================================
# Rename detection
# ============================================================================

def detect_renames(
    previous_records: dict[str, dict[str, str]],
    current_records: list[dict[str, str]],
) -> set[str]:

    """
    Detect renames using content hash.

    If a previous file disappeared and a new file has the same
    content hash, treat it as a rename.
    """

    if not previous_records:
        return set()

    previous_by_hash: dict[str, list[dict[str, str]]] = {}

    for record in previous_records.values():

        if record.get("status") != "active":
            continue

        content_hash = record.get(
            "content_hash"
        )

        if not content_hash:
            continue

        previous_by_hash.setdefault(
            content_hash,
            [],
        ).append(record)

    current_by_hash: dict[str, list[dict[str, str]]] = {}

    for record in current_records:

        content_hash = record.get(
            "content_hash"
        )

        if not content_hash:
            continue

        current_by_hash.setdefault(
            content_hash,
            [],
        ).append(record)

    renamed_ids: set[str] = set()

    for content_hash, current_files in current_by_hash.items():

        previous_files = previous_by_hash.get(
            content_hash,
            [],
        )

        if len(current_files) != 1:
            continue

        if len(previous_files) != 1:
            continue

        previous = previous_files[0]
        current = current_files[0]

        if previous["filepath"] == current["filepath"]:
            continue

        current["change_type"] = "renamed"

        # Preserve manually maintained fields.
        for field in MANUAL_FIELDS:
            current[field] = previous.get(
                field,
                "",
            )

        renamed_ids.add(
            previous["file_id"]
        )

    return renamed_ids


# ============================================================================
# Change detection
# ============================================================================

def detect_changes(
    previous_records: dict[str, dict[str, str]],
    current_records: list[dict[str, str]],
) -> dict[str, int]:

    previous_by_path = {
        record["filepath"]: record
        for record in previous_records.values()
        if record.get("status") == "active"
    }

    current_by_path = {
        record["filepath"]: record
        for record in current_records
    }

    statistics = {
        "new": 0,
        "modified": 0,
        "renamed": 0,
        "deleted": 0,
        "unchanged": 0,
    }

    # ------------------------------------------------------------------
    # Current files
    # ------------------------------------------------------------------

    for current in current_records:

        previous = previous_by_path.get(
            current["filepath"]
        )

        if previous is None:

            current["change_type"] = "new"
            statistics["new"] += 1

            continue

        # Preserve manual metadata.
        for field in MANUAL_FIELDS:
            current[field] = previous.get(
                field,
                "",
            )

        content_changed = (
            previous.get("content_hash")
            != current.get("content_hash")
        )

        metadata_changed = any(
            previous.get(field, "")
            != current.get(field, "")
            for field in [
                "size_bytes",
                "last_modified",
            ]
        )

        if content_changed or metadata_changed:

            current["change_type"] = "modified"
            statistics["modified"] += 1

        else:

            current["change_type"] = "unchanged"
            statistics["unchanged"] += 1

    # ------------------------------------------------------------------
    # Deleted files
    # ------------------------------------------------------------------

    current_file_ids = {
        record["file_id"]
        for record in current_records
    }

    for file_id, previous in previous_records.items():

        if previous.get("status") != "active":
            continue

        if file_id in current_file_ids:
            continue

        deleted = {
            field: previous.get(
                field,
                "",
            )
            for field in ALL_FIELDS
        }

        deleted["status"] = "deleted"
        deleted["change_type"] = "deleted"
        deleted["scanned_at"] = now()

        current_records.append(
            deleted
        )

        statistics["deleted"] += 1

    return statistics


# ============================================================================
# Preserve manual metadata after rename
# ============================================================================

def preserve_manual_metadata_after_rename(
    previous_records: dict[str, dict[str, str]],
    current_records: list[dict[str, str]],
) -> None:

    previous_by_hash = {}

    for record in previous_records.values():

        content_hash = record.get(
            "content_hash"
        )

        if content_hash:
            previous_by_hash.setdefault(
                content_hash,
                [],
            ).append(record)

    for current in current_records:

        if current["change_type"] != "renamed":
            continue

        content_hash = current.get(
            "content_hash"
        )

        candidates = previous_by_hash.get(
            content_hash,
            [],
        )

        if len(candidates) != 1:
            continue

        previous = candidates[0]

        for field in MANUAL_FIELDS:
            current[field] = previous.get(
                field,
                "",
            )


# ============================================================================
# CSV writing
# ============================================================================

def write_metadata(
    metadata_file: Path,
    records: list[dict[str, str]],
) -> None:

    metadata_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    records.sort(
        key=lambda record: (
            record.get("status", ""),
            record.get("filepath", "").lower(),
        )
    )

    with metadata_file.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=ALL_FIELDS,
            extrasaction="ignore",
        )

        writer.writeheader()

        writer.writerows(records)


# ============================================================================
# Scan history
# ============================================================================

def append_scan_history(
    history_file: Path,
    scan_id: str,
    started_at: str,
    completed_at: str,
    statistics: dict[str, int],
) -> None:

    history_file.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    file_exists = history_file.exists()

    with history_file.open(
        "a",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=HISTORY_FIELDS,
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(
            {
                "scan_id": scan_id,
                "scan_started_at": started_at,
                "scan_completed_at": completed_at,
                "total_files":
                    statistics["new"]
                    + statistics["modified"]
                    + statistics["renamed"]
                    + statistics["unchanged"],
                "new_files":
                    statistics["new"],
                "modified_files":
                    statistics["modified"],
                "renamed_files":
                    statistics["renamed"],
                "deleted_files":
                    statistics["deleted"],
                "unchanged_files":
                    statistics["unchanged"],
            }
        )


# ============================================================================
# Reporting
# ============================================================================

def print_changes(
    records: list[dict[str, str]],
) -> None:

    changes = [
        record
        for record in records
        if record["change_type"]
        in {
            "new",
            "modified",
            "renamed",
            "deleted",
        }
    ]

    if not changes:
        print()
        print("No changes detected.")
        return

    print()
    print("=" * 70)
    print("CHANGES")
    print("=" * 70)

    for record in changes:

        change = record["change_type"].upper()

        if change == "DELETED":
            print(
                f"[{change:<9}] "
                f"{record['filepath']}"
            )

        else:
            print(
                f"[{change:<9}] "
                f"{record['filepath']}"
            )


def print_summary(
    statistics: dict[str, int],
) -> None:

    print()
    print("=" * 70)
    print("SCAN SUMMARY")
    print("=" * 70)

    print(
        f"New files        : "
        f"{statistics['new']}"
    )

    print(
        f"Modified files   : "
        f"{statistics['modified']}"
    )

    print(
        f"Renamed files    : "
        f"{statistics['renamed']}"
    )

    print(
        f"Deleted files    : "
        f"{statistics['deleted']}"
    )

    print(
        f"Unchanged files  : "
        f"{statistics['unchanged']}"
    )

    print("=" * 70)


# ============================================================================
# Main
# ============================================================================

def main() -> None:

    scan_id = str(
        uuid.uuid4()
    )

    scan_started_at = now()

    config = load_config()

    repository_path = Path(
        config["repository_path"]
    ).resolve()

    if not repository_path.exists():
        raise FileNotFoundError(
            f"Repository does not exist: "
            f"{repository_path}"
        )

    if not repository_path.is_dir():
        raise NotADirectoryError(
            f"Repository is not a directory: "
            f"{repository_path}"
        )

    metadata_file = Path(
        config.get(
            "metadata_file",
            ".repo-metadata\\repository_files.csv",
        )
    )

    if not metadata_file.is_absolute():
        metadata_file = (
            repository_path / metadata_file
        )

    history_file = Path(
        config.get(
            "scan_history_file",
            ".repo-metadata\\scan_history.csv",
        )
    )

    if not history_file.is_absolute():
        history_file = (
            repository_path / history_file
        )

    print("=" * 70)
    print("Repository Metadata Engine")
    print("=" * 70)

    print(
        f"Repository : {repository_path}"
    )

    print(
        f"Metadata   : {metadata_file}"
    )

    print(
        f"Scan ID    : {scan_id}"
    )

    # ------------------------------------------------------------------
    # Load previous state
    # ------------------------------------------------------------------

    previous_records = load_metadata(
        metadata_file
    )

    print()
    print(
        f"Previous records: "
        f"{len(previous_records)}"
    )

    # ------------------------------------------------------------------
    # Scan
    # ------------------------------------------------------------------

    print()
    print("Scanning repository...")

    current_records = scan_repository(
        repository_path,
        config,
    )

    print(
        f"Current files: "
        f"{len(current_records)}"
    )

    # ------------------------------------------------------------------
    # Change detection
    # ------------------------------------------------------------------

    statistics = detect_changes(
        previous_records,
        current_records,
    )

    renamed_previous_ids: set[str] = set()

    if config.get(
        "rename_detection",
        True,
    ):

        # --------------------------------------------------------------
        # Stage 1: Content hash
        # --------------------------------------------------------------

        renamed_previous_ids = detect_renames(
            previous_records,
            current_records,
        )

        # --------------------------------------------------------------
        # Stage 2: Git
        #
        # Handles cases where:
        #
        #     rename + content modification
        #
        # --------------------------------------------------------------

        git_renamed_previous_ids = (
            detect_git_renames(
                repository_path,
                previous_records,
                current_records,
            )
        )

        renamed_previous_ids.update(
            git_renamed_previous_ids
        )

        # --------------------------------------------------------------
        # Recalculate statistics
        # --------------------------------------------------------------

        statistics["renamed"] = sum(
            1
            for record in current_records
            if record["change_type"] == "renamed"
        )

        statistics["new"] = sum(
            1
            for record in current_records
            if record["change_type"] == "new"
        )

        # Remove deleted records which Git/hash
        # has identified as renamed.
        current_records[:] = [
            record
            for record in current_records
            if not (
                record["status"] == "deleted"
                and record["file_id"]
                in renamed_previous_ids
            )
        ]

        statistics["deleted"] = sum(
            1
            for record in current_records
            if record["change_type"] == "deleted"
        )

        # Recalculate rename count.
        statistics["renamed"] = sum(
            1
            for record in current_records
            if record["change_type"] == "renamed"
        )

        statistics["new"] = sum(
            1
            for record in current_records
            if record["change_type"] == "new"
        )

        # Files which were identified as renames should
        # not also remain as deleted files.
        current_records[:] = [
            record
            for record in current_records
            if not (
                record["status"] == "deleted"
                and record["file_id"]
                in renamed_previous_ids
            )
        ]

        statistics["deleted"] = sum(
            1
            for record in current_records
            if record["change_type"] == "deleted"
        )

    preserve_manual_metadata_after_rename(
        previous_records,
        current_records,
    )

    # ------------------------------------------------------------------
    # Save
    # ------------------------------------------------------------------

    write_metadata(
        metadata_file,
        current_records,
    )

    scan_completed_at = now()

    append_scan_history(
        history_file=history_file,
        scan_id=scan_id,
        started_at=scan_started_at,
        completed_at=scan_completed_at,
        statistics=statistics,
    )

    # ------------------------------------------------------------------
    # Report
    # ------------------------------------------------------------------

    print_changes(
        current_records
    )

    print_summary(
        statistics
    )

    print()
    print(
        f"Metadata saved to:\n"
        f"{metadata_file}"
    )

    print(
        f"History saved to:\n"
        f"{history_file}"
    )


if __name__ == "__main__":
    main()