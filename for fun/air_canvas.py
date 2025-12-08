import cv2
import numpy as np
import mediapipe as mp
import os

# --- 配置参数 ---
brush_thickness = 15
eraser_thickness = 50
# 颜色定义 (B, G, R) 格式
draw_color = (255, 0, 255)  # 默认紫色
eraser_color = (0, 0, 0)  # 橡皮擦实际上是画黑色（如果不使用Mask技巧）或者透明处理

# --- 初始化 MediaPipe ---
mp_hands = mp.solutions.hands
# max_num_hands=1 只需要一只手绘画
# min_detection_confidence 检测置信度
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_draw = mp.solutions.drawing_utils

# --- 初始化摄像头 ---
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # 宽度
cap.set(4, 720)  # 高度

# --- 创建画布 ---
# 创建一个与摄像头分辨率相同的全黑画布
img_canvas = np.zeros((720, 1280, 3), np.uint8)

# 上一帧的坐标点 (初始化为 0,0)
xp, yp = 0, 0

print("程序启动中... 按 'q' 键退出程序")

while True:
    # 1. 读取摄像头画面
    success, img = cap.read()
    if not success:
        print("无法读取摄像头")
        break

    # 翻转画面，使其像镜子一样（不然左右是反的，画起来很别扭）
    img = cv2.flip(img, 1)

    # 2. 寻找手部关键点
    # MediaPipe 需要 RGB 图像
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    # 3. 如果检测到了手
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # 获取关键点坐标列表
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w, c = img.shape
                # 将归一化的坐标 (0-1) 转换为像素坐标
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append([id, cx, cy])

            if len(lm_list) != 0:
                # 获取食指指尖 (Id 8) 和 中指指尖 (Id 12) 的坐标
                x1, y1 = lm_list[8][1:]  # 食指
                x2, y2 = lm_list[12][1:]  # 中指

                # --- 检查手指状态 ---
                # 简单逻辑：如果指尖 y 坐标小于指节 y 坐标，则认为手指竖起
                # 这里的逻辑主要判断食指和中指
                fingers = []

                # 拇指 (Id 4) 比较特殊，这里主要看食指和中指，简化处理
                # 食指判断 (Tip 8 < Pip 6) 注意：y轴向下是正方向，所以竖起是 <
                if lm_list[8][2] < lm_list[6][2]:
                    fingers.append(1)  # 食指竖起
                else:
                    fingers.append(0)

                # 中指判断 (Tip 12 < Pip 10)
                if lm_list[12][2] < lm_list[10][2]:
                    fingers.append(1)  # 中指竖起
                else:
                    fingers.append(0)

                # --- 模式 1: 选择模式 (食指和中指都竖起) ---
                if fingers[0] == 1 and fingers[1] == 1:
                    xp, yp = 0, 0  # 重置绘画起点，避免切模式时连线

                    print("选择模式")
                    # 在指尖之间画个矩形表示正在选择
                    cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), draw_color, cv2.FILLED)

                    # 检测是否点击了顶部的颜色区域
                    if y1 < 125:
                        if 250 < x1 < 450:
                            draw_color = (255, 0, 255)  # 紫色
                            print("选择了紫色")
                        elif 550 < x1 < 750:
                            draw_color = (255, 0, 0)  # 蓝色
                            print("选择了蓝色")
                        elif 800 < x1 < 950:
                            draw_color = (0, 255, 0)  # 绿色
                            print("选择了绿色")
                        elif 1050 < x1 < 1200:
                            draw_color = (0, 0, 0)  # 橡皮擦 (黑色)
                            print("选择了橡皮擦")

                # --- 模式 2: 绘画模式 (只有食指竖起) ---
                if fingers[0] == 1 and fingers[1] == 0:
                    cv2.circle(img, (x1, y1), 15, draw_color, cv2.FILLED)
                    print("绘画模式")

                    # 如果是第一次开始画，将起点设为当前点
                    if xp == 0 and yp == 0:
                        xp, yp = x1, y1

                    # 在画布上画线
                    if draw_color == (0, 0, 0):
                        # 橡皮擦逻辑：画粗黑线
                        cv2.line(img, (xp, yp), (x1, y1), draw_color, eraser_thickness)
                        cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, eraser_thickness)
                    else:
                        # 正常绘画
                        cv2.line(img, (xp, yp), (x1, y1), draw_color, brush_thickness)
                        cv2.line(img_canvas, (xp, yp), (x1, y1), draw_color, brush_thickness)

                    # 更新起点
                    xp, yp = x1, y1
                else:
                    # 如果手指没竖起或者姿势不对，重置起点
                    xp, yp = 0, 0

    # --- 图像融合处理 ---
    # 为了让画出来的线条看起来在视频之上，我们需要进行掩膜处理

    # 1. 将画布转换为灰度图
    img_gray = cv2.cvtColor(img_canvas, cv2.COLOR_BGR2GRAY)

    # 2. 创建反向掩膜 (有颜色的地方是黑，黑色的地方是白)
    _, img_inv = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY_INV)

    # 3. 将反向掩膜转换为BGR以便合并
    img_inv = cv2.cvtColor(img_inv, cv2.COLOR_GRAY2BGR)

    # 4. 在原图中“挖空”画布上有颜色的位置 (使用按位与)
    img = cv2.bitwise_and(img, img_inv)

    # 5. 将原图和画布合并 (画布上有颜色的部分会填入刚才挖空的位置)
    img = cv2.bitwise_or(img, img_canvas)

    # --- 绘制顶部 UI 界面 ---
    # 绘制顶部的颜色选择框
    cv2.rectangle(img, (250, 10), (450, 100), (255, 0, 255), cv2.FILLED)  # 紫
    cv2.rectangle(img, (550, 10), (750, 100), (255, 0, 0), cv2.FILLED)  # 蓝
    cv2.rectangle(img, (800, 10), (950, 100), (0, 255, 0), cv2.FILLED)  # 绿
    cv2.rectangle(img, (1050, 10), (1200, 100), (0, 0, 0), cv2.FILLED)  # 橡皮擦
    cv2.putText(img, "Eraser", (1085, 65), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # 显示画面
    cv2.imshow("Air Canvas", img)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

