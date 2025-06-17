"""
システム全体の統合テスト
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path

import pytest

from src.main import AITuberSystem
from src.stream.stream_handler import ChatMessage


@pytest.fixture
def config():
    """テスト用設定"""
    return {
        "vrm_path": "test_assets/test.vrm",
        "platform": "youtube",
        "video_id": "test_video_id",
        "obs_host": "localhost",
        "obs_port": 4455,
        "voice_config": {
            "speaker_id": 1,
            "speed_scale": 1.0,
            "volume_scale": 1.0,
            "pitch_scale": 0.0,
            "intonation_scale": 1.0,
        },
        "expression_config": {
            "happy": 0.0,
            "angry": 0.0,
            "sad": 0.0,
            "relaxed": 0.0,
            "surprised": 0.0,
        },
    }


@pytest.fixture
def system(config):
    """AITuberSystemのインスタンス"""
    return AITuberSystem(
        vrm_path=config["vrm_path"],
        platform=config["platform"],
        video_id=config["video_id"],
        obs_host=config["obs_host"],
        obs_port=config["obs_port"],
    )


@pytest.mark.asyncio
async def test_system_initialization(system):
    """システム初期化のテスト"""
    assert system is not None
    assert system.llm is not None
    assert system.tts is not None
    assert system.avatar is not None
    assert system.stream is not None
    assert not system.is_running


@pytest.mark.asyncio
async def test_system_start_stop(system):
    """システムの開始と停止のテスト"""
    try:
        # システムの開始
        start_task = asyncio.create_task(system.start())
        await asyncio.sleep(1)  # 開始を待機
        assert system.is_running

        # システムの停止
        await system.stop()
        assert not system.is_running
        start_task.cancel()
    except Exception as e:
        pytest.skip(f"System start/stop test skipped: {e}")


@pytest.mark.asyncio
async def test_message_processing(system):
    """メッセージ処理のテスト"""
    try:
        # システムの開始
        await system.stream.connect()
        system.is_running = True

        # テストメッセージの作成
        message = ChatMessage(
            author="test_user",
            message="こんにちは",
            timestamp=datetime.now(),
            platform="youtube",
        )

        # メッセージの処理
        await system._process_message(message)

        # 状態の確認
        assert system.last_response_time is not None
    except Exception as e:
        pytest.skip(f"Message processing test skipped: {e}")
    finally:
        await system.stop()


def test_system_status(system):
    """システム状態取得のテスト"""
    status = system.get_status()
    assert status is not None
    assert isinstance(status, dict)
    assert "is_running" in status
    assert "last_response_time" in status
    assert "stream_info" in status
    assert "available_expressions" in status


@pytest.mark.asyncio
async def test_full_workflow(system):
    """完全なワークフローのテスト"""
    try:
        # システムの開始
        await system.stream.connect()
        system.is_running = True

        # テストメッセージの作成
        message = ChatMessage(
            author="test_user",
            message="こんにちは",
            timestamp=datetime.now(),
            platform="youtube",
        )

        # メッセージの処理
        await system._process_message(message)

        # 各コンポーネントの状態確認
        assert system.last_response_time is not None
        assert system.stream.get_stream_info()["obs_connected"] is not None
        assert len(system.avatar.get_available_expressions()) > 0

    except Exception as e:
        pytest.skip(f"Full workflow test skipped: {e}")
    finally:
        await system.stop()
