# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Environment Setup
```bash
# Install dependencies using uv (preferred package manager)
uv sync --all-extras

# Development dependencies are automatically installed with --dev extras
uv sync --dev

# Activate virtual environment (auto-managed by uv)
# No manual activation needed - uv run handles this automatically
```

### Code Quality and Testing
```bash
# Format code with ruff
uv run ruff format .

# Check code style and fix automatically
uv run ruff check --fix .

# Type checking
uv run mypy src/

# Run tests
uv run pytest tests/

# Run tests with coverage
uv run pytest --cov=src --cov-report=term-missing tests/

# Run all pre-commit hooks
uv run pre-commit run --all-files

# Install pre-commit hooks
uv run pre-commit install
```

### Running the System
```bash
# Start VOICEVOX TTS engine (required dependency)
./voicevox_engine-linux-cpu-0.14.4/run.sh

# Start main application
uv run python main.py

# Or run with specific Python interpreter
uv run python src/main.py
```

## Architecture Overview

This is a complete local AITuber system with 4 main components:

### 1. Core System (`src/main.py`)
- **AITuberSystem**: Central orchestrator managing all components
- Async message processing with rate limiting (5-second intervals)
- Component lifecycle management and error recovery
- Real-time status monitoring

### 2. LLM Module (`src/llm/`)
- **LocalLLM**: Ollama-based local language model integration
- Conversation history management
- Streaming and non-streaming response modes
- No cloud dependencies - fully offline operation

### 3. TTS Module (`src/tts/`)
- **LocalTTS**: VOICEVOX integration for Japanese text-to-speech
- HTTP API communication with local VOICEVOX engine
- Voice parameter control (speed, pitch, volume, intonation)
- Speaker selection and audio file output

### 4. Avatar Module (`src/avatar/`)
- **AvatarController**: VRM 3D avatar control and animation
- Real-time lip sync generation from audio analysis
- Expression blending (happy, sad, angry, relaxed, surprised)
- Blender integration for pose and animation control

### 5. Stream Module (`src/stream/`)
- **StreamHandler**: Live streaming platform integration
- YouTube Live chat monitoring via pytchat
- WebSocket support for real-time communication
- OBS integration capabilities

## Key Technical Details

### Python Version
- **Strict requirement**: Python 3.11 (>=3.11,<3.12)
- Uses modern async/await patterns throughout

### Dependencies
- **Package Manager**: Use `uv` for all package management (10-100x faster than pip)
- **Core Dependencies**: Ollama, VOICEVOX, pytchat, librosa, bpy (Blender)
- **Type Safety**: Pydantic models for configuration validation
- **Code Quality**: ruff for linting and formatting, mypy for type checking
- **Testing**: pytest with asyncio support and coverage reporting

### Configuration
- **Runtime Config**: Expects `config.json` file for system configuration
- **Pydantic Models**: Strong type validation for all config objects
- **Environment**: Designed for Ubuntu 22.04 LTS with NVIDIA GPU support

### Testing Strategy
- **Framework**: pytest with asyncio support
- **Coverage**: Configured with coverage reporting
- **Mock Objects**: External dependencies are mocked in tests
- **Test Structure**: Unit tests for each component, integration tests for workflows

## Development Workflow

1. **Before Changes**: Always run `uv run mypy src/` to check types
2. **After Changes**: Run `uv run ruff format .` and `uv run ruff check --fix .`
3. **Before Commit**: Run `uv run pre-commit run --all-files`
4. **Component Dependencies**: Each module is designed to be independently testable
5. **Automated Quality**: pre-commit hooks ensure code quality on every commit

## Coding Standards

### Type Hints
- All functions must have complete type annotations
- Use pydantic models for data validation and configuration
- Avoid `Any` type - use specific types or protocols

### Error Handling
- Use specific exception classes, not generic `Exception`
- Log errors appropriately with context
- Provide user-friendly error messages

### Code Style
- Follow ruff configuration in pyproject.toml
- Use descriptive variable and function names
- Keep functions focused and small
- Document complex logic with comments (sparingly)

## System Requirements

- **OS**: Ubuntu 22.04 LTS (recommended)
- **GPU**: NVIDIA GPU 8GB+ (optional, CPU fallback available)
- **RAM**: 16GB+ recommended
- **Storage**: 50GB+ free space
- **External Services**: VOICEVOX engine must be running locally

## Important Notes

- This is a fully offline system - no cloud API dependencies
- All processing happens locally for privacy and reliability
- VRM standard compliance for cross-platform avatar compatibility
- Designed for 24/7 operation with monitoring and error recovery
- Japanese language support is primary focus (VOICEVOX TTS)
