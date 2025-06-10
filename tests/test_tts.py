"""
TTSシステムのユニットテスト
"""

import pytest
from src.tts.local_tts import LocalTTS, VoiceConfig


def test_voice_config_initialization():
    """VoiceConfigの初期化テスト"""
    config = VoiceConfig()
    assert config.speaker_id == 1
    assert config.speed_scale == 1.0
    assert config.volume_scale == 1.0
    assert config.pitch_scale == 0.0
    assert config.intonation_scale == 1.0


def test_voice_config_custom_values():
    """VoiceConfigのカスタム値設定テスト"""
    config = VoiceConfig(
        speaker_id=2,
        speed_scale=1.2,
        volume_scale=1.5,
        pitch_scale=0.5,
        intonation_scale=1.2,
    )
    assert config.speaker_id == 2
    assert config.speed_scale == 1.2
    assert config.volume_scale == 1.5
    assert config.pitch_scale == 0.5
    assert config.intonation_scale == 1.2


def test_local_tts_initialization():
    """LocalTTSの初期化テスト"""
    tts = LocalTTS()
    assert tts is not None
    assert tts.voice_config is not None


def test_text_to_speech():
    """音声合成のテスト"""
    tts = LocalTTS()
    audio_data = tts.text_to_speech("こんにちは")
    assert audio_data is not None
    assert isinstance(audio_data, bytes)
    assert len(audio_data) > 0


def test_get_speakers():
    """話者一覧取得のテスト"""
    tts = LocalTTS()
    speakers = tts.get_speakers()
    assert speakers is not None
    assert isinstance(speakers, list)
    assert len(speakers) > 0


def test_get_version():
    """バージョン取得のテスト"""
    tts = LocalTTS()
    version = tts.get_version()
    assert version is not None
    assert isinstance(version, str)
    assert len(version) > 0 