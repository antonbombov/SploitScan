#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

try:
    from .cli import cli
except ImportError:
    # Если не работает, импортируем напрямую
    import sys
    import os
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
    from cli import cli

if __name__ == "__main__":
    cli()