# AITuber開発ガイド

このドキュメントは、AITuberシステムの開発に関する詳細なガイドラインを提供します。

## 開発環境のセットアップ

### 1. Python環境のセットアップ

```bash
# uvのインストール（既にインストール済みの場合はスキップ）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 仮想環境の作成と有効化
uv venv
source .venv/bin/activate

# 依存関係のインストール
uv pip install -r requirements.txt
```

### 2. 開発ツールのセットアップ

```bash
# 開発用ツールのインストール
uv pip install -r requirements-dev.txt

# コードフォーマッターの設定
black --config pyproject.toml .

# 型チェックの実行
mypy src/
```

## 依存パッケージの追加・インストール方法

uvでは、依存パッケージを一括でインストールするよりも、
下記のように個別に追加・インストールすることを推奨します。

```bash
uv pip install ollama-python
uv pip install transformers
uv pip install torch
uv pip install sounddevice
uv pip install numpy
uv pip install scipy
uv pip install librosa==0.10.1
uv pip install bpy
uv pip install pytchat
uv pip install websockets
uv pip install requests
uv pip install psutil
uv pip install GPUtil
uv pip install pytest
uv pip install black
uv pip install mypy
uv pip install pydantic
```

- requirements.txt/requirements-dev.txtは「参照用リスト」として活用してください。
- パッケージ追加時は`uv pip install パッケージ名`で都度追加し、問題があれば個別に対処してください。

## アーキテクチャ

### システム構成

```
[視聴者コメント] → [コメント取得] → [ローカルLLM] → [応答生成] → [ローカルTTS] → [音声出力] → [アバター制御] → [OBS] → [配信]
```

### 主要コンポーネント

1. **LLMシステム** (`src/llm/`)
   - Ollamaを使用したローカルLLM実行
   - プロンプトエンジニアリング
   - 応答生成の最適化

2. **音声合成システム** (`src/tts/`)
   - VOICEVOX API連携
   - 音声クローニング（RVC）
   - バイノーラル処理

3. **アバター制御システム** (`src/avatar/`)
   - VRMモデルの制御
   - リップシンク
   - 表情制御

4. **配信システム** (`src/stream/`)
   - YouTube/Twitch連携
   - チャット取得
   - OBS統合

## 開発フロー

### 1. 新機能の追加

1. 機能の要件定義
2. テストケースの作成
3. 実装
4. テスト実行
5. コードレビュー
6. マージ

### 2. テスト

```bash
# ユニットテストの実行
pytest tests/

# カバレッジレポートの生成
pytest --cov=src tests/
```

### 3. デプロイ

1. バージョン管理
2. 依存関係の更新
3. テストの実行
4. デプロイスクリプトの実行

## パフォーマンス最適化

### 1. LLM最適化

- 量子化の活用
- バッチ処理の実装
- キャッシュの活用

### 2. 音声処理最適化

- 非同期処理の実装
- バッファサイズの最適化
- GPUアクセラレーション

### 3. アバター最適化

- メッシュの最適化
- アニメーションの効率化
- リソース使用量の監視

## トラブルシューティング

### 1. 一般的な問題

- メモリ使用量の監視
- GPU使用率の確認
- ログの確認

### 2. コンポーネント別の問題

#### LLM
- モデルのロードエラー
- 推論速度の低下
- メモリリーク

#### 音声合成
- 音声品質の問題
- 遅延の発生
- API接続エラー

#### アバター
- モデルの読み込みエラー
- アニメーションの不具合
- パフォーマンスの低下

## セキュリティガイドライン

1. APIキーの管理
2. 環境変数の使用
3. アクセス制御の実装
4. ログの適切な管理

## メンテナンス

### 1. 定期的なメンテナンス

- 依存関係の更新
- ログのローテーション
- バックアップの作成

### 2. モニタリング

- システムリソースの監視
- エラーログの確認
- パフォーマンスメトリクスの収集

## 参考資料

- [技術ドキュメント](../technical_document.md)
- [API仕様書](./api.md)
- [トラブルシューティングガイド](./troubleshooting.md) 