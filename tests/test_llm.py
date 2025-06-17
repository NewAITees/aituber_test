"""
LLMシステムのユニットテスト
"""

from unittest.mock import MagicMock, patch

import pytest

from src.llm.local_llm import LocalLLM, Message


def test_local_llm_initialization():
    """LocalLLMの初期化テスト"""
    llm = LocalLLM()
    assert llm is not None
    assert len(llm._message_history) == 0


def test_add_message():
    """メッセージ追加のテスト"""
    llm = LocalLLM()
    llm.add_message("user", "Hello")
    assert len(llm._message_history) == 1
    assert llm._message_history[0].role == "user"
    assert llm._message_history[0].content == "Hello"


def test_clear_history():
    """履歴クリアのテスト"""
    llm = LocalLLM()
    llm.add_message("user", "Hello")
    assert len(llm._message_history) == 1
    llm.clear_history()
    assert len(llm._message_history) == 0


@patch("ollama.chat")
def test_generate_response(mock_chat):
    """応答生成のテスト"""
    mock_chat.return_value = {"message": {"content": "Hello response"}}

    llm = LocalLLM()
    response = llm.generate_response("Hello")
    assert response is not None
    assert isinstance(response, str)
    assert response == "Hello response"


@patch("ollama.show")
def test_get_model_info(mock_show):
    """モデル情報取得のテスト"""
    mock_show.return_value = {"name": "llama2:7b", "version": "1.0"}

    llm = LocalLLM()
    model_info = llm.get_model_info()
    assert model_info is not None
    assert isinstance(model_info, dict)
    assert "name" in model_info
