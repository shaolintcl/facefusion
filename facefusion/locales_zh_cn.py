"""Simplified Chinese catalog shared by the application and its processors."""

import json
from pathlib import Path
from typing import Any, Dict


with Path(__file__).with_suffix('.json').open(encoding = 'utf-8') as file:
	TRANSLATIONS : Dict[str, str] = json.load(file)


def translate(locales : Dict[str, Any]) -> Dict[str, Any]:
	return {
		key: translate(value) if isinstance(value, dict) else TRANSLATIONS.get(value, value)
		for key, value in locales.items()
	}
