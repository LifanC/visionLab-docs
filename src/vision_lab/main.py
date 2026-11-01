"""程式入口：依序讀圖、取得結果、畫框與匯出。先從 main() 閱讀。"""

import sys
from datetime import datetime
from pathlib import Path
from time import perf_counter
from uuid import uuid4

import cv2

if __package__ in (None, ""):
    # 保留直接執行 main.py 的用法，讓 Python 找得到 src 下的 vision_lab 套件。
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from vision_lab.cli import parse_args
from vision_lab.detection import detect_objects, filter_results
from vision_lab.drawing import COLORS, prepare_crops, render_results
from vision_lab.exporter import (
    ensure_outputs_available, load_results, save_csv, save_image, save_results,
)

# 預設圖片與 outputs 都以專案根目錄為起點。
PROJECT_DIR = Path(__file__).resolve().parents[2]


def main() -> None:
    """安排整體流程；-> None 表示這個函式不回傳處理結果。"""
    # 1. 取得參數與路徑；perf_counter 適合量測一段處理所花的時間。
    args = parse_args()
    started_at = perf_counter()
    image_path = args.image.resolve()
    if args.output_dir is None:
        # 本地時間方便辨識，隨機識別碼降低同一秒執行時撞名的機會。
        run_name = f"{datetime.now():%Y-%m-%d_%H-%M-%S}_{uuid4().hex[:8]}"
        output_dir = PROJECT_DIR / "outputs" / run_name
    else:
        output_dir = args.output_dir.resolve()
    img = cv2.imread(str(image_path))
    # 讀取失敗會回傳 None；必須先檢查，才能安全地使用 shape 或 copy。
    if img is None:
        print(
            f"讀不到圖片，請確認檔案存在且為有效圖片：{image_path}",
            file=sys.stderr,
        )
        raise SystemExit(1)

    height, width = img.shape[:2]

    # 2. 先過濾分數，再篩選名稱、面積，最後取前 K 筆。
    results = detect_objects(img, threshold=args.threshold)
    results = filter_results(results, args.label, args.min_area, args.top_k)

    # 3. 準備所有輸出路徑與裁切資料，檢查完成前不寫入結果。
    results_path = output_dir / "results.json"
    csv_path = output_dir / "results.csv"
    preview_path = output_dir / "preview.jpg"
    crops = prepare_crops(img, results, output_dir) if args.save_crops else []
    output_paths = [
        results_path, csv_path,
        output_dir / "meme_boxed.jpg",
        output_dir / "meme_restored.jpg",
        # crops 每筆是 (路徑, 圖片)；_ 表示這裡不需要使用圖片。
        *[path for path, _ in crops],
    ]
    if args.save_preview:
        output_paths.append(preview_path)
    # 所有預定輸出都檢查完後，才開始寫入。
    ensure_outputs_available(output_paths, args.overwrite)
    if image_path in [path.resolve() for path in output_paths]:
        raise ValueError("輸出路徑與輸入圖片相同，請更換 --output-dir")
    output_dir.mkdir(parents=True, exist_ok=True)

    # 4. 準備標註背景；裁切仍使用未加工的彩色原圖 img。
    background = img
    if args.grayscale:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 灰階再轉回三通道，才能在灰階背景上畫出彩色文字與方框。
        background = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    render_options = {
        "color": COLORS[args.box_color],
        "thickness": args.line_thickness,
        "font_scale": args.font_scale,
        "show_confidence": not args.hide_confidence,
    }
    # ** 將字典展開成具名參數，讓兩次畫框共用相同樣式。
    boxed = render_results(background, results, **render_options)
    save_results(results, results_path)
    save_csv(results, csv_path)
    # 5. 讀回實際儲存的 JSON，確認能用保存的資料重新繪製。
    saved_results = load_results(results_path)
    restored = render_results(background, saved_results, **render_options)

    for item in saved_results:
        print(f"名稱：{item['label']}")
        print(f"信心分數：{item['confidence']:.0%}")
        print(f"方框座標：{item['box']}")

    # 6. 統一儲存標註圖、裁切圖，以及選擇性輸出的左右對照圖。
    for filename, image in (
        ("meme_boxed.jpg", boxed),
        ("meme_restored.jpg", restored),
    ):
        output_path = output_dir / filename
        save_image(output_path, image, args.jpg_quality)

    for path, crop in crops:
        save_image(path, crop, args.jpg_quality)
    if args.save_preview:
        save_image(preview_path, cv2.hconcat([img, boxed]), args.jpg_quality)

    # 在開啟視窗前結算耗時，不把等待使用者按鍵的時間算進去。
    elapsed = perf_counter() - started_at

    if not args.no_show:
        try:
            cv2.imshow("Boxed", boxed)
            cv2.imshow("Restored", restored)
            cv2.waitKey(0)
        finally:
            # 即使顯示途中出錯，也嘗試清理已開啟的視窗。
            cv2.destroyAllWindows()

    # 7. 顯示摘要，方便在 CMD 核對本次參數與輸出位置。
    print("\n執行完成")
    print(f"輸入圖片：{image_path}")
    print(f"圖片尺寸：{width} × {height} 像素")
    print(f"信心分數門檻：{args.threshold:.0%}")
    print(f"保留結果：{len(results)} 筆")
    print(f"輸出資料夾：{output_dir}")
    print(f"處理耗時：{elapsed:.3f} 秒")


def cli() -> None:
    """直接執行與安裝後的指令入口共用錯誤處理。"""
    try:
        main()
    except (OSError, ValueError, cv2.error) as error:
        # stderr 專門輸出錯誤，代碼 1 讓 CMD 知道執行失敗。
        print(f"執行失敗：{error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    cli()
