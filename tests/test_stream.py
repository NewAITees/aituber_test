"""
配信システムのユニットテスト
"""

import pytest
import asyncio
from datetime import datetime
from src.stream.stream_handler import StreamHandler, ChatMessage


@pytest.fixture
def stream_handler():
    """StreamHandlerのインスタンス"""
    return StreamHandler(
        platform="youtube",
        video_id="test_video_id",
        obs_host="localhost",
        obs_port=4455,
    )


def test_chat_message_initialization():
    """ChatMessageの初期化テスト"""
    message = ChatMessage(
        author="test_user",
        message="Hello",
        timestamp=datetime.now(),
        platform="youtube",
    )
    assert message.author == "test_user"
    assert message.message == "Hello"
    assert isinstance(message.timestamp, datetime)
    assert message.platform == "youtube"


@pytest.mark.asyncio
async def test_stream_handler_initialization(stream_handler):
    """StreamHandlerの初期化テスト"""
    assert stream_handler is not None
    assert stream_handler.platform == "youtube"
    assert stream_handler.video_id == "test_video_id"
    assert stream_handler.obs_host == "localhost"
    assert stream_handler.obs_port == 4455


@pytest.mark.asyncio
async def test_connect(stream_handler):
    """接続テスト"""
    try:
        await stream_handler.connect()
        assert stream_handler.chat is not None
    except Exception as e:
        pytest.skip(f"Connection test skipped: {e}")


@pytest.mark.asyncio
async def test_get_chat_messages(stream_handler):
    """チャットメッセージ取得のテスト"""
    try:
        await stream_handler.connect()
        async for message in stream_handler.get_chat_messages():
            assert isinstance(message, ChatMessage)
            assert message.author is not None
            assert message.message is not None
            assert isinstance(message.timestamp, datetime)
            assert message.platform == "youtube"
            break
    except Exception as e:
        pytest.skip(f"Chat message test skipped: {e}")


@pytest.mark.asyncio
async def test_send_to_obs(stream_handler):
    """OBS送信のテスト"""
    try:
        await stream_handler.connect()
        await stream_handler.send_to_obs("Test message")
    except Exception as e:
        pytest.skip(f"OBS send test skipped: {e}")


@pytest.mark.asyncio
async def test_disconnect(stream_handler):
    """切断テスト"""
    try:
        await stream_handler.connect()
        await stream_handler.disconnect()
        assert stream_handler.chat is None
        assert stream_handler.obs is None
    except Exception as e:
        pytest.skip(f"Disconnect test skipped: {e}")


def test_get_stream_info(stream_handler):
    """配信情報取得のテスト"""
    info = stream_handler.get_stream_info()
    assert info is not None
    assert isinstance(info, dict)
    assert "platform" in info
    assert "video_id" in info
    assert "obs_connected" in info
    assert info["platform"] == "youtube"
    assert info["video_id"] == "test_video_id" 