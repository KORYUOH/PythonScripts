import os
import re
from rapidfuzz import fuzz
from multiprocessing import Pool, cpu_count
from collections import defaultdict

TARGET_EXT = {".zip", ".rar"}

# ================================
# ① ファイル名の解析（抽出）
# ================================
FILENAME_PATTERN = re.compile(
    r"""
    ^(?:\([^)]*\)\s*)?
    

\[([^]]+)\]

\s*
    ([^(

\[]+?)\s*
    (?:\([^)]*\)\s*)?
    (?:

\[[^]]*\]

\s*)?
    \.(zip|rar)$
    """,
    re.VERBOSE | re.IGNORECASE
)

def extract_circle_title(filename):
    m = FILENAME_PATTERN.match(filename)
    if not m:
        return None
    return m.group(1).strip(), m.group(2).strip()


# ================================
# ② 編作品の判定（前編・後編・中編・前・中・後）
# ================================
def detect_part_type(title):
    if re.search(r"(前編|後編|中編|前|中|後)", title):
        return "hen"  # 編作品
    return None       # 通常作品


# ================================
# ③ タイトル正規化（数字除去のみ）
# ================================
def normalize_title(title):
    t = title
    t = re.sub(r"\b\d+\b", "", t)
    t = re.sub(r"\b[IVXLC]+\b", "", t)
    t = re.sub(r"[①②③④⑤⑥⑦⑧⑨⑩]", "", t)
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
# ⑥ サークル名ごとクラスタリング（並列化対象）
# ================================
def cluster_by_circle(circle_items):
    groups = []
    used = set()

    for i in range(len(circle_items)):
        if i in used:
            continue

        base = circle_items[i]
        base_path, base_circle, base_title = base
        base_norm = normalize_title(base_title)
        base_num = extract_number(base_title)
        base_part = detect_part_type(base_title)
        base_folder = os.path.dirname(base_path)

        group = [base]
        used.add(i)

        for j in range(i + 1, len(circle_items)):
            if j in used:
                continue

            other = circle_items[j]
            other_path, other_circle, other_title = other
            other_norm = normalize_title(other_title)
            other_num = extract_number(other_title)
            other_part = detect_part_type(other_title)
            other_folder = os.path.dirname(other_path)

            # サークル名違い → 絶対に混ぜない
            if base_circle != other_circle:
                continue

            # 数字が両方ある → 数字違いは別作品
            if base_num and other_num and base_num != other_num:
                continue

            # 数字が片方だけ → 別作品
            if (base_num and not other_num) or (other_num and not base_num):
                continue

            # ★ 編作品（前後中編）はフォルダが違えば同一作品扱い
            if base_part == "hen" and other_part == "hen":
                if base_folder != other_folder:
                    group.append(other)
                    used.add(j)
                    continue
                else:
                    continue  # 同じフォルダ → 別作品扱い

            # 通常作品 → 正規化タイトルで比較
            score = fuzz.ratio(base_norm, other_norm)
            if score >= 80:
                group.append(other)
                used.add(j)

        groups.append(group)

    return groups


# ================================
# ⑦ TXT 出力（相対パス・./なし・拡張子除去）
# ================================
def export_clusters_to_txt(all_groups, base_folder, output_file="similar_titles.txt"):
    with open(output_file, "w", encoding="utf-8") as f:
        for groups in all_groups:
            for group in groups:
                if len(group) <= 1:
                    continue  # ユニーク除外

                circle_name = group[0][1]
                f.write(f"=== {circle_name} ===\n")

                for item in group:
                    full_path = item[0]

                    rel_path = os.path.relpath(full_path, base_folder)
                    rel_path = rel_path.lstrip("./")

                    name_without_ext, _ = os.path.splitext(rel_path)
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

    circle_groups = defaultdict(list)
    for item in items:
        circle_groups[item[1]].append(item)

    with Pool(cpu_count()) as pool:
        all_groups = pool.map(cluster_by_circle, circle_groups.values())

    export_clusters_to_txt(all_groups, folder)


if __name__ == "__main__":
    main()
