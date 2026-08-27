#!/usr/bin/env python3
"""逐页调用 ocr.wmcloud.org 并落盘缓存。

用法: python3 ocr_fetch.py <起页> <止页>
页号是扫描件的幅号（Page:<书名>/<N> 里的 N），不是印刷页码。
"""
import json, os, sys, time, urllib.parse, urllib.request

# —— 改这三项 ——
FILE = "<书名>.pdf"     # Commons 上的文件名（空格写成下划线或原样均可）
HASH = "<h1>/<h1h2>"    # 文件名 md5 的 前1位/前2位，见 SKILL.md §2
WIDTH = 960             # 不得超过 imageinfo.width，否则 HTTP 400

ENGINE = "google"
UA = "wikisource OCR write-back script (contact: <你的维基用户页或邮箱>)"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "out", "ocr")


def thumb(page):
    f = urllib.parse.quote(FILE)
    return (f"https://upload.wikimedia.org/wikipedia/commons/thumb/{HASH}/{f}"
            f"/page{page}-{WIDTH}px-{f}.jpg")


def ocr(page):
    q = urllib.parse.urlencode({"engine": ENGINE, "image": thumb(page)})
    req = urllib.request.Request("https://ocr.wmcloud.org/api.php?" + q,
                                 headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)


def main():
    os.makedirs(OUT, exist_ok=True)
    for p in range(int(sys.argv[1]), int(sys.argv[2]) + 1):
        dest = os.path.join(OUT, f"{p}.txt")
        if os.path.exists(dest):
            print(p, "已缓存")
            continue
        for attempt in range(3):
            try:
                d = ocr(p)
                if "text" not in d:
                    raise RuntimeError(d.get("error", d))
                with open(dest, "w") as fh:
                    fh.write(d["text"])
                print(p, len(d["text"]), "字")
                break
            except Exception as e:
                print(p, "错误", e, file=sys.stderr)
                time.sleep(5 * (attempt + 1))
        time.sleep(1)


if __name__ == "__main__":
    main()
