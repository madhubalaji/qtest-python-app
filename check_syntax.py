#!/usr/bin/env python3
"""
構文エラーをチェックするためのスクリプト
"""
import ast
import sys


def check_syntax(filename):
    """ファイルの構文をチェックします"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # ASTを使用して構文をチェック
        ast.parse(content, filename=filename)
        print(f"✓ {filename}: 構文エラーなし")
        return True

    except SyntaxError as e:
        print(f"✗ {filename}: 構文エラー")
        print(f"  行 {e.lineno}, 列 {e.offset}: {e.msg}")
        if e.text:
            print(f"  問題のある行: {e.text.strip()}")
        return False
    except Exception as e:
        print(f"✗ {filename}: その他のエラー: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("使用方法: python check_syntax.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]
    success = check_syntax(filename)
    sys.exit(0 if success else 1)