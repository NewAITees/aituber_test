"""
アバター制御システムの基本実装
VRMモデルの制御とリップシンクを担当
"""

from typing import Dict, List, Optional, Tuple
import json
import math
from dataclasses import dataclass
import numpy as np
import librosa
from pydantic import BaseModel, Field


@dataclass
class LipSyncData:
    """リップシンクデータ"""
    phoneme: str
    start_time: float
    end_time: float
    intensity: float


class ExpressionConfig(BaseModel):
    """表情設定のモデル"""
    happy: float = Field(default=0.0, description="喜び")
    angry: float = Field(default=0.0, description="怒り")
    sad: float = Field(default=0.0, description="悲しみ")
    relaxed: float = Field(default=0.0, description="リラックス")
    surprised: float = Field(default=0.0, description="驚き")


class AvatarController:
    """アバター制御システムのメインクラス"""

    def __init__(
        self,
        vrm_path: str,
        expression_config: Optional[ExpressionConfig] = None,
    ):
        """
        Args:
            vrm_path: VRMモデルのパス
            expression_config: 表情設定
        """
        self.vrm_path = vrm_path
        self.expression_config = expression_config or ExpressionConfig()
        self._load_vrm()
        self._setup_lip_sync()

    def _load_vrm(self) -> None:
        """VRMモデルを読み込む"""
        try:
            with open(self.vrm_path, 'rb') as f:
                self.vrm_data = json.load(f)
            
            # ブレンドシェイプの初期化
            self.blend_shapes = {
                "happy": 0.0,
                "angry": 0.0,
                "sad": 0.0,
                "relaxed": 0.0,
                "surprised": 0.0,
            }
            
            # リップシンク用の音素マッピング
            self.phoneme_map = {
                "a": "あ",
                "i": "い",
                "u": "う",
                "e": "え",
                "o": "お",
                "n": "ん",
            }
        except Exception as e:
            print(f"Error loading VRM model: {e}")
            raise

    def _setup_lip_sync(self) -> None:
        """リップシンクの初期設定"""
        # 音素認識用のパラメータ
        self.sample_rate = 44100
        self.hop_length = 512
        self.win_length = 2048
        
        # 音素認識用のモデル（簡易実装）
        self.phoneme_model = {
            "a": [0.8, 0.2, 0.0, 0.0, 0.0],
            "i": [0.0, 0.8, 0.2, 0.0, 0.0],
            "u": [0.0, 0.0, 0.8, 0.2, 0.0],
            "e": [0.2, 0.0, 0.0, 0.8, 0.0],
            "o": [0.0, 0.0, 0.0, 0.0, 0.8],
            "n": [0.0, 0.0, 0.0, 0.0, 0.0],
        }

    def set_expression(self, expression: ExpressionConfig) -> None:
        """表情を設定

        Args:
            expression: 表情設定
        """
        self.expression_config = expression
        # ブレンドシェイプの更新
        self.blend_shapes.update({
            "happy": expression.happy,
            "angry": expression.angry,
            "sad": expression.sad,
            "relaxed": expression.relaxed,
            "surprised": expression.surprised,
        })

    def lip_sync(self, audio_data: bytes) -> List[LipSyncData]:
        """音声データからリップシンクデータを生成

        Args:
            audio_data: 音声データ

        Returns:
            リップシンクデータのリスト
        """
        # 音声データをnumpy配列に変換
        audio_array = np.frombuffer(audio_data, dtype=np.float32)
        
        # 音声解析
        mfcc = librosa.feature.mfcc(
            y=audio_array,
            sr=self.sample_rate,
            n_mfcc=13,
            hop_length=self.hop_length,
            win_length=self.win_length
        )
        
        # 音素認識（簡易実装）
        lip_sync_data = []
        frame_duration = self.hop_length / self.sample_rate
        
        for i in range(mfcc.shape[1]):
            # 現在のフレームの特徴量
            frame_features = mfcc[:, i]
            
            # 最も近い音素を特定
            best_phoneme = "n"
            best_score = float('inf')
            
            for phoneme, features in self.phoneme_model.items():
                score = np.linalg.norm(frame_features - features)
                if score < best_score:
                    best_score = score
                    best_phoneme = phoneme
            
            # リップシンクデータの生成
            lip_sync_data.append(
                LipSyncData(
                    phoneme=best_phoneme,
                    start_time=i * frame_duration,
                    end_time=(i + 1) * frame_duration,
                    intensity=1.0 - (best_score / 10.0)  # スコアを強度に変換
                )
            )
        
        return lip_sync_data

    def update_pose(
        self,
        position: Tuple[float, float, float],
        rotation: Tuple[float, float, float],
    ) -> None:
        """アバターの姿勢を更新

        Args:
            position: 位置 (x, y, z)
            rotation: 回転 (x, y, z)
        """
        # 位置と回転の更新
        self.current_position = position
        self.current_rotation = rotation
        
        # VRMモデルの更新
        if hasattr(self, 'vrm_data'):
            # 位置の更新
            self.vrm_data['nodes'][0]['translation'] = list(position)
            
            # 回転の更新（クォータニオンに変換）
            qx = math.sin(rotation[0]/2) * math.cos(rotation[1]/2) * math.cos(rotation[2]/2) - \
                 math.cos(rotation[0]/2) * math.sin(rotation[1]/2) * math.sin(rotation[2]/2)
            qy = math.cos(rotation[0]/2) * math.sin(rotation[1]/2) * math.cos(rotation[2]/2) + \
                 math.sin(rotation[0]/2) * math.cos(rotation[1]/2) * math.sin(rotation[2]/2)
            qz = math.cos(rotation[0]/2) * math.cos(rotation[1]/2) * math.sin(rotation[2]/2) - \
                 math.sin(rotation[0]/2) * math.sin(rotation[1]/2) * math.cos(rotation[2]/2)
            qw = math.cos(rotation[0]/2) * math.cos(rotation[1]/2) * math.cos(rotation[2]/2) + \
                 math.sin(rotation[0]/2) * math.sin(rotation[1]/2) * math.sin(rotation[2]/2)
            
            self.vrm_data['nodes'][0]['rotation'] = [qx, qy, qz, qw]

    def get_available_expressions(self) -> List[str]:
        """利用可能な表情の一覧を取得

        Returns:
            表情名のリスト
        """
        return list(self.blend_shapes.keys())

    def export_animation(self, output_path: str) -> None:
        """アニメーションデータをエクスポート

        Args:
            output_path: 出力ファイルパス
        """
        animation_data = {
            "blend_shapes": self.blend_shapes,
            "position": self.current_position if hasattr(self, 'current_position') else [0, 0, 0],
            "rotation": self.current_rotation if hasattr(self, 'current_rotation') else [0, 0, 0],
        }
        
        with open(output_path, 'w') as f:
            json.dump(animation_data, f, indent=2) 