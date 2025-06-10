# AITuber Development Environment

このプロジェクトは、完全ローカル環境でのAITuberシステム開発環境を提供します。

## システム要件

- OS: Linux (Ubuntu 22.04 LTS推奨)
- GPU: NVIDIA GPU 8GB以上推奨（CPUでも動作可能）
- RAM: 16GB以上推奨
- ストレージ: 50GB以上の空き容量

## インストール済みコンポーネント

- Ollama (LLM実行環境)
- uv (Pythonパッケージマネージャー)

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

# 依存関係のインストール
uv pip install -r requirements.txt
```

3. VOICEVOXのセットアップ:
```bash
# VOICEVOXのダウンロードと展開
wget https://github.com/VOICEVOX/voicevox_engine/releases/download/0.14.4/voicevox_engine-linux-cpu-0.14.4.tar.gz
tar -xzf voicevox_engine-linux-cpu-0.14.4.tar.gz
```

4. システムの起動:
```bash
# VOICEVOXの起動
./voicevox_engine-linux-cpu-0.14.4/run.sh

# メインアプリケーションの起動
python main.py
```

## プロジェクト構造

```
.
├── .cursor/              # 開発環境設定
├── docs/                 # ドキュメント
├── src/                  # ソースコード
│   ├── llm/             # LLM関連
│   ├── tts/             # 音声合成
│   ├── avatar/          # アバター制御
│   └── stream/          # 配信関連
├── tests/               # テストコード
├── requirements.txt     # 依存関係
└── README.md           # このファイル
```

## 開発ガイド

詳細な開発ガイドは `docs/development.md` を参照してください。

## ライセンス

MIT License
