"""
AITuberシステムのメイン実装
各コンポーネントの連携を担当
"""

import asyncio
import json
from typing import Optional
from datetime import datetime
from pathlib import Path

from src.llm.local_llm import LocalLLM
from src.tts.local_tts import LocalTTS, VoiceConfig
from src.avatar.avatar_controller import AvatarController, ExpressionConfig
from src.stream.stream_handler import StreamHandler, ChatMessage


class AITuberSystem:
    """AITuberシステムのメインクラス"""

    def __init__(
        self,
        vrm_path: str,
        platform: str,
        video_id: str,
        obs_host: str = "localhost",
        obs_port: int = 4455,
        obs_password: Optional[str] = None,
        voice_config: Optional[VoiceConfig] = None,
        expression_config: Optional[ExpressionConfig] = None,
    ):
        """
        Args:
            vrm_path: VRMモデルのパス
            platform: 配信プラットフォーム ("youtube" or "twitch")
            video_id: 動画ID
            obs_host: OBS WebSocketのホスト
            obs_port: OBS WebSocketのポート
            obs_password: OBS WebSocketのパスワード
            voice_config: 音声設定
            expression_config: 表情設定
        """
        # コンポーネントの初期化
        self.llm = LocalLLM()
        self.tts = LocalTTS(voice_config)
        self.avatar = AvatarController(vrm_path, expression_config)
        self.stream = StreamHandler(
            platform=platform,
            video_id=video_id,
            obs_host=obs_host,
            obs_port=obs_port,
            obs_password=obs_password,
        )

        # 状態管理
        self.is_running = False
        self.last_response_time = None
        self.response_interval = 5.0  # 秒

    async def start(self) -> None:
        """システムを開始"""
        try:
            # 各コンポーネントの接続
            await self.stream.connect()
            self.is_running = True

            # メインループ
            while self.is_running:
                async for message in self.stream.get_chat_messages():
                    await self._process_message(message)

        except Exception as e:
            print(f"Error in main loop: {e}")
        finally:
            await self.stop()

    async def stop(self) -> None:
        """システムを停止"""
        self.is_running = False
        await self.stream.disconnect()

    async def _process_message(self, message: ChatMessage) -> None:
        """チャットメッセージを処理

        Args:
            message: チャットメッセージ
        """
        # 応答間隔のチェック
        if self.last_response_time:
            elapsed = (datetime.now() - self.last_response_time).total_seconds()
            if elapsed < self.response_interval:
                return

        try:
            # LLMで応答を生成
            response = self.llm.generate_response(message.message)
            if not response:
                return

            # 音声合成
            audio_data = self.tts.text_to_speech(response)
            if not audio_data:
                return

            # リップシンクデータの生成
            lip_sync_data = self.avatar.lip_sync(audio_data)

            # アバターの更新
            self.avatar.set_expression(
                ExpressionConfig(
                    happy=0.3,  # 簡易的な感情表現
                    angry=0.0,
                    sad=0.0,
                    relaxed=0.7,
                    surprised=0.0,
                )
            )

            # OBSに送信
            await self.stream.send_to_obs(response)

            # 状態の更新
            self.last_response_time = datetime.now()

        except Exception as e:
            print(f"Error processing message: {e}")

    def get_status(self) -> dict:
        """システムの状態を取得

        Returns:
            システムの状態
        """
        return {
            "is_running": self.is_running,
            "last_response_time": self.last_response_time.isoformat() if self.last_response_time else None,
            "stream_info": self.stream.get_stream_info(),
            "available_expressions": self.avatar.get_available_expressions(),
        }


async def main():
    """メイン関数"""
    # 設定の読み込み
    config_path = Path("config.json")
    if not config_path.exists():
        raise FileNotFoundError("config.json not found")

    with open(config_path) as f:
        config = json.load(f)

    # システムの初期化
    system = AITuberSystem(
        vrm_path=config["vrm_path"],
        platform=config["platform"],
        video_id=config["video_id"],
        obs_host=config.get("obs_host", "localhost"),
        obs_port=config.get("obs_port", 4455),
        obs_password=config.get("obs_password"),
        voice_config=VoiceConfig(**config.get("voice_config", {})),
        expression_config=ExpressionConfig(**config.get("expression_config", {})),
    )

    # システムの開始
    try:
        await system.start()
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        await system.stop()


if __name__ == "__main__":
    asyncio.run(main()) 