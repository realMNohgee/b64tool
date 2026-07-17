# b64tool 🔣

**Base64, Base32, and Base16 encode/decode with auto-detection.** Zero dependencies, pure Python stdlib.

Encode text to any base encoding, decode with automatic format detection, or identify which encoding a string uses. Built on Python's `base64` stdlib with a clean CLI.

> Part of the **Trust & Reliability Layer for Agentic AI**

## Why it exists

Base encoding is everywhere — API tokens, config values, data serialization. b64tool handles all three common base encodings with auto-detection so you never have to guess which one you're looking at.

## One tool, many domains

| Domain | What b64tool does |
|---|---|
| 🔣 **Data Encoding** | Encode/decode between base64, base32, base16 |
| 🔍 **Debugging** | Auto-detect encoding type of unknown strings |
| 🔒 **Security** | Inspect encoded payloads and tokens |
| 🤖 **AI Agents** | Quick base conversion in agent pipelines |

## Install
```bash
git clone git@github.com:realMNohgee/b64tool.git
cd b64tool
python3 b64tool.py --help
```

## Quick start
```bash
python3 b64tool.py encode "Hello World"
python3 b64tool.py decode "SGVsbG8gV29ybGQ="
python3 b64tool.py detect "JBSWY3DP"
```

## License

MIT — see [LICENSE](LICENSE).

---
🧰 **[Tool on Hermtica Marketplace](https://hermtica.com/marketplace)** — the open, agent-agnostic marketplace for AI agent tools.
