"""檔案輸出：JSON、CSV、JPG 與覆寫保護。"""

import csv
import json

import cv2

from .drawing import prepare_crops

def save_results(results, path):
    """將結果清單寫入 JSON；with 結束時會自動關閉檔案。"""
    with path.open("w", encoding="utf-8") as file:
        # 保留中文字，並用兩個空白縮排，方便直接開啟檔案閱讀。
        json.dump(results, file, ensure_ascii=False, indent=2)

    print(f"已儲存 {len(results)} 筆結果")


def load_results(path):
    """將 JSON 內容轉回 Python 清單與字典。"""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_csv(results, path):
    """匯出表格；沒有結果時仍保留欄位名稱。"""
    # utf-8-sig 方便 Excel 辨識編碼，newline="" 避免 Windows 多出空白列。
    with path.open("w", encoding="utf-8-sig", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "label",
            "confidence",
            "left",
            "top",
            "right",
            "bottom",
        ])

        for item in results:
            writer.writerow([
                item["label"],
                item["confidence"],
                # * 將座標清單展開成四欄。
                *item["box"],
            ])


def save_image(path, image, jpg_quality=95):
    """統一 JPG 品質設定與存檔檢查。"""
    if not cv2.imwrite(
        str(path), image, [cv2.IMWRITE_JPEG_QUALITY, jpg_quality]
    ):
        raise OSError(f"圖片儲存失敗：{path}")


def ensure_outputs_available(paths, overwrite=False):
    """寫入前檢查所有目的路徑；即使允許覆寫，也不能寫到資料夾上。"""
    for path in paths:
        if path.is_dir():
            raise IsADirectoryError(f"輸出路徑是資料夾：{path}")
        if path.exists() and not overwrite:
            raise FileExistsError(
                f"輸出檔案已存在：{path}；"
                "請更換 --output-dir，或加上 --overwrite"
            )


def save_crops(image, results, output_dir, overwrite=False, jpg_quality=95):
    """可獨立呼叫的裁切存檔功能；main() 則將裁切圖納入整批輸出處理。"""
    crops = prepare_crops(image, results, output_dir)
    ensure_outputs_available([path for path, _ in crops], overwrite)
    for path, crop in crops:
        save_image(path, crop, jpg_quality)
