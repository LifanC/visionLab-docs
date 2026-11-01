"""圖片處理：畫框、加文字，以及準備物件裁切圖片。"""

import cv2

# OpenCV 使用 B、G、R 順序，而非一般常見的 R、G、B。
COLORS = {"green": (0, 255, 0), "red": (0, 0, 255), "blue": (255, 0, 0)}

def draw_label(
    image, start, end, label,
    color=(0, 255, 0), thickness=3, font_scale=0.8,
):
    """直接在傳入圖片上畫一筆標註；座標格式為 (x, y)。"""
    cv2.rectangle(image, start, end, color, thickness)
    # putText 的座標是文字左下角；盡量放在方框上方，避免太靠近圖片頂端。
    text_position = (start[0], max(start[1] - 10, 25))
    cv2.putText(
        image,
        label,
        text_position,
        cv2.FONT_HERSHEY_SIMPLEX,
        font_scale,
        color,
        2,
        cv2.LINE_AA,
    )


def render_results(
    image, results,
    color=(0, 255, 0), thickness=3, font_scale=0.8,
    show_confidence=True,
):
    """回傳標註完成的副本，保留原圖供裁切與左右比較。"""
    output = image.copy()
    for item in results:
        left, top, right, bottom = item["box"]
        text = item["label"]
        if show_confidence:
            # :.0% 將 0.92 顯示為 92%，不保留小數。
            text += f" {item['confidence']:.0%}"
        draw_label(
            output,
            (left, top),
            (right, bottom),
            text,
            color=color,
            thickness=thickness,
            font_scale=font_scale,
        )
    return output


def prepare_crops(image, results, output_dir):
    """先驗證所有裁切範圍，不在這個階段寫入檔案。"""
    height, width = image.shape[:2]
    crops = []
    for index, item in enumerate(results, start=1):
        left, top, right, bottom = item["box"]
        # 把座標限制在圖片邊界內，避免裁切範圍越界。
        left, right = max(0, min(left, width)), max(0, min(right, width))
        top, bottom = max(0, min(top, height)), max(0, min(bottom, height))
        if left >= right or top >= bottom:
            raise ValueError(f"第 {index} 筆結果的裁切範圍無效")
        path = output_dir / f"crop_{index:03d}.jpg"
        # 陣列裁切先寫上下，再寫左右；: 的結束位置不包含在內。
        crops.append((path, image[top:bottom, left:right]))
    return crops
