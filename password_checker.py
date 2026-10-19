"""密碼強度檢查器（HW2）。僅使用標準函式庫，Python 3.8+。"""
import re
from typing import List

SPECIALS = "!@#$%^&*"

# 每條規則：（驗證失敗時顯示的訊息，通過時回傳 True 的判斷式）。
# 刻意使用 ASCII 範圍，避免「²」或全形數字被 str.isdigit()/isupper() 誤判為有效。
RULES = [
    ("至少 8 個字元",
     lambda p: len(p) >= 8),
    ("至少一個大寫字母（A-Z）",
     lambda p: any("A" <= c <= "Z" for c in p)),
    ("至少一個小寫字母（a-z）",
     lambda p: any("a" <= c <= "z" for c in p)),
    ("至少一個數字（0-9）",
     lambda p: any("0" <= c <= "9" for c in p)),
    ("至少一個特殊字元（" + SPECIALS + "）",
     lambda p: any(c in SPECIALS for c in p)),
    # (.)\1\1 = 某字元連續出現三次（區分大小寫）。
    ("不可有連續重複 3 次以上的相同字元",
     lambda p: not re.search(r"(.)\1\1", p, re.DOTALL)),
]

QUIT_COMMANDS = ("quit",)


def check_password(password: str) -> List[str]:
    """回傳所有未通過規則的訊息；空列表表示密碼強度足夠。"""
    return [message for message, passed in RULES if not passed(password)]


def is_quit_command(text: str) -> bool:
    return text.strip().lower() in QUIT_COMMANDS


def main() -> None:
    try:
        while True:
            raw = input("請輸入密碼（輸入 quit 離開）：")

            # 優先檢查是否為離開指令，避免將「quit」當作密碼驗證。
            if is_quit_command(raw):
                print("再見。")
                return

            # 空值判斷使用 strip()，但下方驗證使用原始輸入，
            # 因此前後空白仍計入字元數。
            if not raw.strip():
                print("密碼不可為空白。")
                continue

            failures = check_password(raw)
            if not failures:
                print("密碼符合強度要求。")
                return

            print("密碼未符合以下要求：")
            for message in failures:
                print("  - " + message)
    except (KeyboardInterrupt, EOFError):
        print("\n再見。")


if __name__ == "__main__":
    main()
