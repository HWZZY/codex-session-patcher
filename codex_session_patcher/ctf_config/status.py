# -*- coding: utf-8 -*-
"""
CTF 配置状态检查
"""

import os
from dataclasses import dataclass
from typing import Optional


GLOBAL_MARKER = '# __csp_ctf_global__'


@dataclass
class CTFStatus:
    """CTF 配置状态"""
    installed: bool = False
    config_exists: bool = False
    prompt_exists: bool = False
    profile_available: bool = False
    global_installed: bool = False
    config_path: Optional[str] = None
    prompt_path: Optional[str] = None


def check_ctf_status() -> CTFStatus:
    """
    检查 CTF 配置的安装状态

    Returns:
        CTFStatus: 配置状态信息
    """
    # Codex 配置路径
    codex_dir = os.path.expanduser("~/.codex")
    config_path = os.path.join(codex_dir, "config.toml")
    prompts_dir = os.path.join(codex_dir, "prompts")
    prompt_path = os.path.join(prompts_dir, "security_mode.md")

    status = CTFStatus(
        config_path=config_path,
        prompt_path=prompt_path,
    )

    # 检查配置文件是否存在
    if os.path.exists(config_path):
        status.config_exists = True

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '[profiles.ctf]' in content:
                    status.profile_available = True
                if GLOBAL_MARKER in content:
                    status.global_installed = True
        except Exception:
            pass

    # 检查 prompt 文件是否存在
    if os.path.exists(prompt_path):
        status.prompt_exists = True

    # 判断是否已安装（两个文件都存在且有 ctf profile）
    status.installed = status.config_exists and status.prompt_exists and status.profile_available

    return status