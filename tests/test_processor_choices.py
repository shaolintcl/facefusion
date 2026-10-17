import gradio

from facefusion import translator
from facefusion.uis.components import processors


def test_chinese_processor_choices_keep_internal_values(monkeypatch) -> None:
	monkeypatch.setattr(translator, 'CURRENT_LANGUAGE', 'zh-CN')
	choices = processors.get_processor_choices([ 'face_swapper' ])
	assert choices[0] == ('换脸', 'face_swapper')
	assert ('人脸增强', 'face_enhancer') in choices
	assert len(choices) == 11
	component = gradio.CheckboxGroup(choices = choices, value = [ 'face_swapper' ])
	assert component.preprocess([ 'face_swapper', 'face_enhancer' ]) == [ 'face_swapper', 'face_enhancer' ]


def test_processor_change_retains_translated_choices(monkeypatch) -> None:
	monkeypatch.setattr(translator, 'CURRENT_LANGUAGE', 'zh-CN')
	monkeypatch.setattr(processors, 'get_processors_modules', lambda names: [])
	monkeypatch.setattr(processors.state_manager, 'get_item', lambda name: [ 'face_enhancer' ])
	monkeypatch.setattr(processors.state_manager, 'set_item', lambda name, value: None)
	component = processors.update_processors([ 'face_enhancer' ])
	assert component.choices[0] == ('人脸增强', 'face_enhancer')
	assert component.value == [ 'face_enhancer' ]
