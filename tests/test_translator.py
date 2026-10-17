from facefusion import translator
from facefusion.locales import LOCALES
from facefusion.locales_zh_cn import TRANSLATIONS
import importlib
from pathlib import Path
from string import Formatter


def test_load() -> None:
	translator.load(LOCALES, __name__)

	assert __name__ in translator.LOCALE_POOL_SET


def test_get() -> None:
	assert translator.get('processing_stopped') == 'processing stopped'
	assert translator.get('help.run') == 'run the program'
	assert translator.get('invalid') is None


def test_simplified_chinese(monkeypatch) -> None:
	monkeypatch.setattr(translator, 'CURRENT_LANGUAGE', 'zh-CN')
	assert translator.get('processing_stopped') == '处理已停止'
	assert translator.get('uis.start_button') == '开始'
	assert translator.get('uis.model_dropdown', 'facefusion.processors.modules.face_swapper') == '换脸模型'
	assert translator.get('invalid') is None


def test_chinese_catalog_coverage_and_placeholders() -> None:
	def check(values) -> None:
		for value in values.values():
			if isinstance(value, dict):
				check(value)
			else:
				assert value in TRANSLATIONS, value
				def fields(text):
					return sorted(field for _, field, _, _ in Formatter().parse(text) if field is not None)
				assert fields(value) == fields(TRANSLATIONS[value]), value

	for path in (Path(__file__).resolve().parents[1] / 'facefusion').rglob('locales.py'):
		module_name = '.'.join(path.relative_to(Path(__file__).resolve().parents[1]).with_suffix('').parts)
		check(importlib.import_module(module_name).LOCALES['en'])


def test_translation_falls_back_to_english() -> None:
	from facefusion.locales_zh_cn import translate
	assert translate({ 'new': 'untranslated message' }) == { 'new': 'untranslated message' }
