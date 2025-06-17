"""
配信システムの基本実装
YouTube/Twitchのチャット取得とOBS統合を担当
"""

import asyncio
import json
from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Optional

import pytchat
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """チャットメッセージのモデル"""

    author: str = Field(..., description="投稿者名")
    message: str = Field(..., description="メッセージ内容")
    timestamp: datetime = Field(..., description="投稿時刻")
    platform: str = Field(..., description="配信プラットフォーム")


class StreamHandler:
    """配信システムのメインクラス"""

    def __init__(
        self,
        video_id: str,
        platform: str = "youtube",
        obs_host: str = "localhost",
        obs_port: int = 4455,
        obs_password: str | None = None,
    ) -> None:
        """
        Args:
            video_id: 配信ID
            platform: 配信プラットフォーム ("youtube" or "twitch")
            obs_host: OBS WebSocketのホスト
            obs_port: OBS WebSocketのポート
            obs_password: OBS WebSocketのパスワード
        """
        self.video_id = video_id
        self.platform = platform
        self.obs_host = obs_host
        self.obs_port = obs_port
        self.obs_password = obs_password
        self._chat = None
        self._obs_connected = False

    async def connect(self) -> None:
        """配信プラットフォームとOBSに接続"""
        if self.platform == "youtube":
            self._chat = pytchat.create(video_id=self.video_id)
        elif self.platform == "twitch":
            # TODO: Twitch接続の実装
            pass

        if self.obs_websocket_url:
            # TODO: OBS WebSocket接続の実装
            self._obs_connected = True

    async def get_chat_messages(self) -> AsyncGenerator[ChatMessage, None]:
        """チャットメッセージを取得

        Yields:
            チャットメッセージ
        """
        if not self._chat:
            await self.connect()

        while self._chat.is_alive():
            try:
                data = await self._chat.get()
                for item in data.sync_items():
                    yield ChatMessage(
                        author=item.author.name,
                        message=item.message,
                        timestamp=item.timestamp,
                        platform=self.platform,
                    )
            except Exception as e:
                print(f"Error getting chat messages: {e}")
                break

    async def send_to_obs(self, message: str) -> None:
        """OBSにメッセージを送信

        Args:
            message: 送信するメッセージ
        """
        if not self._obs_connected:
            return

        # TODO: OBS WebSocketを使用したメッセージ送信の実装
        pass

    async def disconnect(self) -> None:
        """接続を切断"""
        if self._chat:
            self._chat.terminate()
            self._chat = None

        if self._obs_connected:
            # TODO: OBS WebSocket接続の切断処理を実装
            self._obs_connected = False

    def get_stream_info(self) -> dict:
        """配信情報を取得

        Returns:
            配信情報を含む辞書
        """
        # TODO: 配信情報取得の実装
        return {
            "platform": self.platform,
            "video_id": self.video_id,
            "obs_connected": self._obs_connected,
        }
