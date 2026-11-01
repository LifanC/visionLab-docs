"""辨識與篩選：目前使用模擬物件，之後可在此接入 AI。"""

def detect_objects(image, threshold=0.5):
    """產生模擬結果，保留分數至少等於 threshold 的物件。"""
    # 圖片陣列的順序是高度、寬度、色彩通道；[:2] 只取前兩個。
    height, width = image.shape[:2]
    # 每筆依序為：左上角、右下角、名稱、分數。// 是整數除法。
    # 方框按圖片比例計算，名稱和分數固定，尚未呼叫 AI。
    objects = [
        (
            (width // 10, height // 5),
            (width * 4 // 10, height * 4 // 5),
            "Object A",
            0.92,
        ),
        (
            (width * 6 // 10, height // 5),
            (width * 9 // 10, height * 4 // 5),
            "Object B",
            0.45,
        ),
    ]
    results = []
    for start, end, label, confidence in objects:
        if confidence < threshold:
            continue

        results.append({
            "label": label,
            "confidence": confidence,
            # 統一格式：左、上、右、下，單位為像素。
            "box": [start[0], start[1], end[0], end[1]],
        })
    return results


def filter_results(results, labels=None, min_area=0, top_k=None):
    """先依名稱與面積篩選，再選出分數最高的前 K 筆。"""
    filtered = []
    for item in results:
        if labels and item["label"] not in labels:
            continue
        left, top, right, bottom = item["box"]
        area = max(0, right - left) * max(0, bottom - top)
        if area >= min_area:
            filtered.append(item)
    if top_k is not None:
        # lambda 指定排序依據，reverse=True 由高到低，[:top_k] 取前 K 筆。
        filtered = sorted(
            filtered, key=lambda item: item["confidence"], reverse=True
        )[:top_k]
    return filtered
