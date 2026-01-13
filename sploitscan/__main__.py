#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Указываем Python, что это пакет
__package__ = "sploitscan"

# Добавляем корень проекта в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем
from sploitscan.cli import cli

if __name__ == "__main__":
    cli()