import os
import re
from rapidfuzz import fuzz

TARGET_EXT = {".zip", ".rar"}

# ================================
# ① ファイル名の解析（抽出）
# ================================
FILENAME_PATTERN = re.compile(
    r"""
    ^(?:\([^)]*\)\s*)?          # (イベント名) → 任意
    

\[([^]]+)\]

\s*              # [サークル名] → 必須
    ([^(

\[]+?)\s*               # タイトル → 必須
    (?:\([^)]*\)\s*)?           # (ジャンル) → 任意
    (?:

\[[^]]*\]

\s*)?           # [情報] → 任意
    \.(zip|rar)$                # 拡張子 → 必須
    """,
    re.VERBOSE | re.IGNORECASE
)

def extract_circle_title(filename):
    m = FILENAME_PATTERN.match(filename)
    if not m:
        return None
    return m.group(1).strip(), m.group(2).strip()


# ================================
# ② 前編／後編／中編の判定
# ================================
def detect_part(title):
    return bool(re.search(r"(前編|後編|中編|前|中|後)", title))


# ================================
# ③ タイトル正規化（数字除去のみ）
# ================================
def normalize_title(title):
    t = title

    # 数字除去（比較用）
    t = re.sub(r"\b\d+\b", "", t)

    # ローマ数字除去
    t = re.sub(r"\b[IVXLC]+\b", "", t)

    # 丸数字除去
    t = re.sub(r"[①②③④⑤⑥⑦⑧⑨⑩]", "", t)

    # 前後編は除去しない（別作品扱いするため）
    t = re.sub(r"\s+", " ", t).strip()

    return t


# ================================
# ④ ナンバリング抽出
# ================================
def extract_number(title):
    m = re.search(r"\b(\d+)\b", title)
    return m.group(1) if m else None


# ================================
# ⑤ サブフォルダ走査
# ================================
def scan_folder_recursive(base_folder):
    results = []
    for root, dirs, files in os.walk(base_folder):
        for f in files:
            _, ext = os.path.splitext(f)
            if ext.lower() in TARGET_EXT:
                parsed = extract_circle_title(f)
                if parsed:
                    circle, title = parsed
                    full_path = os.path.join(root, f)
                    results.append((full_path, circle, title))
    return results


# ================================
# ⑥ rapidfuzz 類似クラスタリング
# ================================
def cluster_titles(items, threshold=80):
    groups = []
    used = set()

    for i in range(len(items)):
        if i in used:
            continue

        base = items[i]
        base_path, base_circle, base_title = base
        base_norm = normalize_title(base_title)
        base_num = extract_number(base_title)
        base_part = detect_part(base_title)

        group = [base]
        used.add(i)

        for j in range(i + 1, len(items)):
            if j in used:
                continue

            other = items[j]
            other_path, other_circle, other_title = other
            other_norm = normalize_title(other_title)
            other_num = extract_number(other_title)
            other_part = detect_part(other_title)

            # ★ サークル名が違う → 絶対に同じグループにしない
            if base_circle != other_circle:
                continue

            # ★ 前編／後編が混ざっていたら絶対に同じグループにしない
            if base_part != other_part:
                continue

            # 正規化タイトルで比較
            score = fuzz.ratio(base_norm, other_norm)

            # 類似している OR 同じ番号なら同一作品
            if score >= threshold or (base_num and other_num and base_num == other_num):
                group.append(other)
                used.add(j)

        groups.append(group)

    return groups


# ================================
# ⑦ TXT 出力（ユニーク除外）
# ================================
def export_clusters_to_txt(groups, output_file="similar_titles.txt"):
    with open(output_file, "w", encoding="utf-8") as f:
        group_index = 1

        for group in groups:
            if len(group) <= 1:
                continue  # ユニークは除外

            f.write(f"=== Group {group_index} ===\n")
            group_index += 1

            for item in group:
                full_path = item[0]
                filename = os.path.basename(full_path)
                name_without_ext, _ = os.path.splitext(filename)
                f.write(f"{name_without_ext}\n")

            f.write("\n")

    print(f"出力: {output_file}")


# ================================
# ⑧ メイン処理（デフォルト＝スクリプトの場所）
# ================================
def main(folder=None):
    if folder is None:
        folder = os.path.dirname(os.path.abspath(__file__))

    items = scan_folder_recursive(folder)
    groups = cluster_titles(items)
    export_clusters_to_txt(groups)


if __name__ == "__main__":
    main()
