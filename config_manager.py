"""Quản lý cấu hình người dùng cho MKV Processor."""
from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict


DEFAULT_CONFIG: Dict[str, Any] = {
    "input_folder": ".",
    "auto_upload": False,
    "repo": "HThanh-how/Subtitles",
    "branch": "main",
    "logs_dir": "logs",
    "subtitle_dir": "subtitles",
    "token": "",
}


def get_config_dir() -> Path:
    if os.name == "nt":
        base = Path(os.getenv("APPDATA", str(Path.home() / "AppData" / "Roaming")))
    elif xdg := os.getenv("XDG_CONFIG_HOME"):
        base = Path(xdg)
    else:
        base = Path.home() / ".config"
    config_dir = base / "MKVProcessor"
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_config_path() -> Path:
    return get_config_dir() / "config.json"


def load_user_config() -> Dict[str, Any]:
    config = DEFAULT_CONFIG.copy()
    path = get_config_path()
    if path.exists():
        try:
            user_cfg = json.loads(path.read_text(encoding="utf-8"))
            config.update(user_cfg)
        except Exception as exc:
            print(f"[CONFIG] Không thể đọc config: {exc}")
    return config


def save_user_config(data: Dict[str, Any]) -> None:
    merged = DEFAULT_CONFIG.copy()
    merged.update(data)
    path = get_config_path()
    path.write_text(json.dumps(merged, ensure_ascii=False, indent=2), encoding="utf-8")


def reset_config() -> None:
    path = get_config_path()
    if path.exists():
        path.unlink()

