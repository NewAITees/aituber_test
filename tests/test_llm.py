"""
LLMシステムのユニットテスト
"""

import pytest
from src.llm.local_llm import LocalLLM, Message


def test_local_llm_initialization():
    """LocalLLMの初期化テスト"""
    llm = LocalLLM()
    assert llm is not None
    assert len(llm.messages) == 0


def test_add_message():
    """メッセージ追加のテスト"""
    llm = LocalLLM()
    message = Message(role="user", content="Hello")
    llm.add_message(message)
    assert len(llm.messages) == 1
    assert llm.messages[0].role == "user"
    assert llm.messages[0].content == "Hello"


def test_clear_history():
    """履歴クリアのテスト"""
    llm = LocalLLM()
    message = Message(role="user", content="Hello")
    llm.add_message(message)
    assert len(llm.messages) == 1
    llm.clear_history()
    assert len(llm.messages) == 0


def test_generate_response():
    """応答生成のテスト"""
    llm = LocalLLM()
    response = llm.generate_response("Hello")
    assert response is not None
    assert isinstance(response, str)
    assert len(response) > 0


def test_get_model_info():
    """モデル情報取得のテスト"""
    llm = LocalLLM()
    model_info = llm.get_model_info()
    assert model_info is not None
    assert isinstance(model_info, dict)
    assert "name" in model_info
    assert "version" in model_info 