"""
ローカル音声合成システムの基本実装
VOICEVOXを使用した音声合成を担当
"""

import json
from pathlib import Path
from typing import Optional, Union

import requests
from pydantic import BaseModel, Field


class VoiceConfig(BaseModel):
    """音声設定のモデル"""

    speaker_id: int = Field(default=1, description="話者ID")
    speed_scale: float = Field(default=1.0, description="話速")
    volume_scale: float = Field(default=1.0, description="音量")
    pitch_scale: float = Field(default=0.0, description="音の高さ")
    intonation_scale: float = Field(default=1.0, description="イントネーション")


class LocalTTS:
    """ローカル音声合成システムのメインクラス"""

    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 50021,
        voice_config: VoiceConfig | None = None,
    ) -> None:
        """
        Args:
            host: VOICEVOXエンジンのホスト
            port: VOICEVOXエンジンのポート
            voice_config: 音声設定
        """
        self.base_url = f"http://{host}:{port}"
        self.voice_config = voice_config or VoiceConfig()

    def text_to_speech(self, text: str, output_path: str | None = None) -> bytes | str:
        """テキストを音声に変換

        Args:
            text: 変換するテキスト
            output_path: 出力ファイルパス(指定された場合)

        Returns:
            音声データ(バイナリ)または出力ファイルパス
        """
        # 音声クエリの生成
        query_response = requests.post(
            f"{self.base_url}/audio_query",
            params={
                "text": text,
                "speaker": self.voice_config.speaker_id,
            },
            timeout=30.0,
        )
        query_response.raise_for_status()
        audio_query = query_response.json()

        # 音声合成パラメータの設定
        audio_query["speedScale"] = self.voice_config.speed_scale
        audio_query["volumeScale"] = self.voice_config.volume_scale
        audio_query["pitchScale"] = self.voice_config.pitch_scale
        audio_query["intonationScale"] = self.voice_config.intonation_scale

        # 音声合成
        synthesis_response = requests.post(
            f"{self.base_url}/synthesis",
            params={"speaker": self.voice_config.speaker_id},
            data=json.dumps(audio_query),
            headers={"Content-Type": "application/json"},
            timeout=30.0,
        )
        synthesis_response.raise_for_status()
        audio_data = synthesis_response.content

        # 出力ファイルが指定されている場合は保存
        if output_path:
            with Path(output_path).open("wb") as f:
                f.write(audio_data)
            return output_path

        return audio_data

    def get_speakers(self) -> dict:
        """利用可能な話者の一覧を取得

        Returns:
            話者情報を含む辞書
        """
        response = requests.get(f"{self.base_url}/speakers", timeout=10.0)
        response.raise_for_status()
        return response.json()

    def get_version(self) -> str:
        """VOICEVOXエンジンのバージョンを取得

        Returns:
            バージョン文字列
        """
        try:
            response = requests.get(f"{self.base_url}/version", timeout=10.0)
            response.raise_for_status()
            result = response.json()
            if isinstance(result, dict):
                return result.get("version", "unknown")
            else:
                return str(result)
        except Exception:
            return "unknown"
