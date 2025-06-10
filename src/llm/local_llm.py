"""
ローカルLLMシステムの基本実装
Ollamaを使用したローカルLLMの実行と応答生成を担当
"""

from typing import Dict, List, Optional
import ollama
from pydantic import BaseModel, Field


class Message(BaseModel):
    """チャットメッセージのモデル"""
    role: str = Field(..., description="メッセージの役割 (system, user, assistant)")
    content: str = Field(..., description="メッセージの内容")


class LocalLLM:
    """ローカルLLMシステムのメインクラス"""

    def __init__(
        self,
        model_name: str = "llama2:7b",
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ):
        """
        Args:
            model_name: 使用するモデル名
            system_prompt: システムプロンプト
            temperature: 生成の多様性を制御するパラメータ (0.0-1.0)
            max_tokens: 生成する最大トークン数
        """
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.temperature = temperature
        self.max_tokens = max_tokens
        self._message_history: List[Message] = []

    def add_message(self, role: str, content: str) -> None:
        """メッセージ履歴に新しいメッセージを追加

        Args:
            role: メッセージの役割
            content: メッセージの内容
        """
        self._message_history.append(Message(role=role, content=content))

    def clear_history(self) -> None:
        """メッセージ履歴をクリア"""
        self._message_history.clear()

    def generate_response(
        self, user_input: str, stream: bool = False
    ) -> str:
        """ユーザー入力に対する応答を生成

        Args:
            user_input: ユーザーからの入力
            stream: ストリーミング出力を使用するかどうか

        Returns:
            生成された応答テキスト
        """
        # システムプロンプトが設定されている場合は追加
        if self.system_prompt:
            self.add_message("system", self.system_prompt)

        # ユーザー入力を追加
        self.add_message("user", user_input)

        # Ollama APIを使用して応答を生成
        response = ollama.chat(
            model=self.model_name,
            messages=[msg.dict() for msg in self._message_history],
            stream=stream,
            options={
                "temperature": self.temperature,
                "num_predict": self.max_tokens,
            },
        )

        if stream:
            # ストリーミングモードの場合
            return response
        else:
            # 通常モードの場合
            response_text = response["message"]["content"]
            self.add_message("assistant", response_text)
            return response_text

    def get_model_info(self) -> Dict:
        """現在使用しているモデルの情報を取得

        Returns:
            モデル情報を含む辞書
        """
        return ollama.show(self.model_name) 