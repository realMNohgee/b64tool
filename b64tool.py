#!/usr/bin/env python3
"""b64tool — Base64/32/16 encode, decode, and auto-detect."""

from __future__ import annotations

import argparse
import base64
import json
import sys


def encode_data(data: bytes, encoding: str) -> str:
    if encoding == "base64":
        return base64.b64encode(data).decode()
    elif encoding == "base32":
        return base64.b32encode(data).decode()
    elif encoding == "base16":
        return base64.b16encode(data).decode()
    else:
        return base64.b64encode(data).decode()


def decode_data(text: str, encoding: str | None = None) -> tuple[bytes, str]:
    text = text.strip()
    if encoding:
        mappings = {
            "base64": base64.b64decode,
            "base32": base64.b32decode,
            "base16": base64.b16decode,
        }
        return mappings[encoding](text), encoding

    # Auto-detect
    for name, decoder in [
        ("base64", base64.b64decode),
        ("base32", base64.b32decode),
        ("base16", base64.b16decode),
    ]:
        try:
            return decoder(text), name
        except Exception:
            continue
    raise ValueError("Could not decode with any encoding")


def detect_encoding(text: str) -> list[str]:
    text = text.strip()
    found = []
    for name, decoder in [
        ("base64", base64.b64decode),
        ("base32", base64.b32decode),
        ("base16", base64.b16decode),
    ]:
        try:
            decoder(text)
            found.append(name)
        except Exception:
            pass
    return found


def read_input(text_or_path: str, from_stdin: bool) -> str:
    if from_stdin:
        return sys.stdin.read()
    return text_or_path


def cmd_encode(args: argparse.Namespace) -> None:
    text = read_input(args.text, args.stdin)
    data = text.encode()
    result = encode_data(data, args.encoding)
    if args.format == "json":
        print(json.dumps({"encoding": args.encoding, "input": text, "output": result}))
    else:
        print(result)


def cmd_decode(args: argparse.Namespace) -> None:
    text = read_input(args.text, args.stdin)
    try:
        data, used_encoding = decode_data(text, args.encoding)
        result = data.decode("utf-8", errors="replace")
    except Exception as e:
        print(f"Error: decode failed — {e}", file=sys.stderr)
        sys.exit(1)
    if args.format == "json":
        print(json.dumps({"encoding": used_encoding, "input": text.strip(), "output": result}))
    else:
        print(result)


def cmd_detect(args: argparse.Namespace) -> None:
    text = read_input(args.text, args.stdin)
    encodings = detect_encoding(text)
    if args.format == "json":
        print(json.dumps({"input": text.strip(), "detected": encodings}))
    else:
        if encodings:
            print("Detected encodings: %s" % ", ".join(encodings))
        else:
            print("No valid encoding detected")
            sys.exit(1)


def main() -> None:
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--format", choices=["text", "json"], default="text")

    p = argparse.ArgumentParser(description="b64tool — Base64/32/16 encode, decode, and detect")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp_encode = sub.add_parser("encode", parents=[common], help="Encode text to base encoding")
    sp_encode.add_argument("text", help="Text to encode")
    sp_encode.add_argument("--encoding", choices=["base64", "base32", "base16"], default="base64")
    sp_encode.add_argument("--stdin", action="store_true", help="Read input from stdin (use '-' as text)")

    sp_decode = sub.add_parser("decode", parents=[common], help="Decode base-encoded text")
    sp_decode.add_argument("text", help="Encoded text to decode")
    sp_decode.add_argument("--encoding", choices=["base64", "base32", "base16"], default=None)
    sp_decode.add_argument("--stdin", action="store_true", help="Read input from stdin (use '-' as text)")

    sp_detect = sub.add_parser("detect", parents=[common], help="Auto-detect base encoding type")
    sp_detect.add_argument("text", help="Text to analyze")
    sp_detect.add_argument("--stdin", action="store_true", help="Read input from stdin (use '-' as text)")

    args = p.parse_args()

    handlers = {
        "encode": cmd_encode,
        "decode": cmd_decode,
        "detect": cmd_detect,
    }
    handlers[args.cmd](args)


if __name__ == "__main__":
    main()
