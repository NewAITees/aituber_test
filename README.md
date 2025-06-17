# AITuber Development Environment

このプロジェクトは、完全ローカル環境でのAITuberシステム開発環境を提供します。

## システム要件

- OS: Linux (Ubuntu 22.04 LTS推奨)
- GPU: NVIDIA GPU 8GB以上推奨（CPUでも動作可能）
- RAM: 16GB以上推奨
- ストレージ: 50GB以上の空き容量
- Python: 3.11以上（3.12未満）

## インストール済みコンポーネント

- Ollama (LLM実行環境)
- uv (Pythonパッケージマネージャー)
- VOICEVOX (音声合成エンジン)

## セットアップ手順

1. リポジトリのクローン:
```bash
git clone [repository-url]
cd aituber_test
```

2. 環境のセットアップ:
```bash
# uvのインストール（既にインストール済みの場合はスキップ）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 依存関係のインストール（開発用ツールも含む）
uv sync --all-extras --dev

# 開発用ツールのセットアップ
uv run pre-commit install
```

3. VOICEVOXのセットアップ:
```bash
# VOICEVOXのダウンロードと展開
wget https://github.com/VOICEVOX/voicevox_engine/releases/download/0.14.4/voicevox_engine-linux-cpu-0.14.4.tar.gz
tar -xzf voicevox_engine-linux-cpu-0.14.4.tar.gz
```

4. 設定ファイルの作成:
```bash
# config.jsonの作成（テンプレートを参考に設定）
cp config.example.json config.json
# 必要に応じて設定を編集
```

5. システムの起動:
```bash
# VOICEVOXの起動（別ターミナルで実行）
./voicevox_engine-linux-cpu-0.14.4/run.sh

# メインアプリケーションの起動
uv run python src/main.py
```

## プロジェクト構造

```
.
├── .cursor/              # 開発環境設定
├── .devcontainer/        # DevContainer設定
├── .github/              # GitHub Actions設定
├── docs/                 # ドキュメント
├── src/                  # ソースコード
│   ├── llm/             # LLM関連
│   ├── tts/             # 音声合成
│   ├── avatar/          # アバター制御
│   └── stream/          # 配信関連
├── tests/               # テストコード
├── pyproject.toml       # プロジェクト設定
├── uv.lock              # 依存関係ロックファイル
└── README.md           # このファイル
```

## 開発ガイド

詳細な開発ガイドは `docs/development.md` を参照してください。

## コード品質とテスト

```bash
# コードフォーマット
uv run ruff format .

# リンター実行
uv run ruff check --fix .

# 型チェック
uv run mypy src/

# テスト実行
uv run pytest tests/

# カバレッジレポート
uv run pytest --cov=src --cov-report=term-missing tests/
```

## ライセンス

MIT License
