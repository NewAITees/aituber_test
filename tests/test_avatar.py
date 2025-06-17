"""
アバター制御システムのユニットテスト
"""

import os

import pytest

from src.avatar.avatar_controller import AvatarController, ExpressionConfig, LipSyncData


@pytest.fixture
def vrm_path():
    """テスト用VRMファイルのパス"""
    return "test_assets/test.vrm"


@pytest.fixture
def avatar_controller(vrm_path):
    """AvatarControllerのインスタンス"""
    return AvatarController(vrm_path)


def test_expression_config_initialization():
    """ExpressionConfigの初期化テスト"""
    config = ExpressionConfig()
    assert config.happy == 0.0
    assert config.angry == 0.0
    assert config.sad == 0.0
    assert config.relaxed == 0.0
    assert config.surprised == 0.0


def test_expression_config_custom_values():
    """ExpressionConfigのカスタム値設定テスト"""
    config = ExpressionConfig(
        happy=0.5,
        angry=0.3,
        sad=0.2,
        relaxed=0.8,
        surprised=0.1,
    )
    assert config.happy == 0.5
    assert config.angry == 0.3
    assert config.sad == 0.2
    assert config.relaxed == 0.8
    assert config.surprised == 0.1


def test_avatar_controller_initialization(avatar_controller):
    """AvatarControllerの初期化テスト"""
    assert avatar_controller is not None
    assert avatar_controller.vrm_path is not None
    assert avatar_controller.expression_config is not None


def test_set_expression(avatar_controller):
    """表情設定のテスト"""
    config = ExpressionConfig(
        happy=0.5,
        angry=0.3,
        sad=0.2,
        relaxed=0.8,
        surprised=0.1,
    )
    avatar_controller.set_expression(config)
    assert avatar_controller.expression_config == config


def test_lip_sync(avatar_controller):
    """リップシンクのテスト"""
    # テスト用の音声データ
    audio_data = b"test" * 1000
    lip_sync_data = avatar_controller.lip_sync(audio_data)
    assert lip_sync_data is not None
    assert isinstance(lip_sync_data, list)
    assert len(lip_sync_data) > 0
    assert all(isinstance(data, LipSyncData) for data in lip_sync_data)


def test_update_pose(avatar_controller):
    """姿勢更新のテスト"""
    position = (0.0, 1.0, 0.0)
    rotation = (0.0, 0.0, 0.0)
    avatar_controller.update_pose(position, rotation)
    assert hasattr(avatar_controller, "current_position")
    assert hasattr(avatar_controller, "current_rotation")
    assert avatar_controller.current_position == position
    assert avatar_controller.current_rotation == rotation


def test_get_available_expressions(avatar_controller):
    """利用可能な表情一覧取得のテスト"""
    expressions = avatar_controller.get_available_expressions()
    assert expressions is not None
    assert isinstance(expressions, list)
    assert len(expressions) > 0
    assert all(isinstance(expr, str) for expr in expressions)


def test_export_animation(avatar_controller, tmp_path):
    """アニメーションデータのエクスポートテスト"""
    output_path = tmp_path / "animation.json"
    avatar_controller.export_animation(str(output_path))
    assert output_path.exists()
    assert output_path.stat().st_size > 0
