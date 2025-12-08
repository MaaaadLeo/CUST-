import cv2
import mediapipe as mp
import math
import numpy as np
import os
import random  # 【新增】用于生成随机粒子
from PIL import Image, ImageDraw, ImageFont


# ================= 0. 智能字体加载器 (保持不变) =================
def load_chinese_font(size=40):
    """
    优先加载项目目录下的 simhei.TTF，如果没有，再去找系统字体
    """
    candidate_paths = [
        "simhei.TTF",
        "simhei.ttf",
        "SimHei.ttf",
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/Heiti SC.ttc",
        "/System/Library/Fonts/Supplemental/Songti.ttc"
    ]
    selected_font = None
    for path in candidate_paths:
        if os.path.exists(path):
            try:
                selected_font = ImageFont.truetype(path, size)
                print(f"✅ 成功加载字体: {path}")
                break
            except Exception as e:
                continue
    if selected_font is None:
        print("❌ 未找到中文字体，使用默认字体")
        selected_font = ImageFont.load_default()
    return selected_font


# ================= 【新增】粒子动画类定义 =================
class HeartParticle:
    def __init__(self, x, y):
        """初始化一个粒子"""
        self.x = x
        self.y = y
        # 随机速度：让粒子向四面八方炸开
        self.vx = random.uniform(-8, 8)
        self.vy = random.uniform(-8, 8)
        # 初始大小和生长速度
        self.size = random.randint(5, 15)
        self.grow_speed = random.uniform(0.5, 1.5)
        # 寿命：粒子能存活多少帧
        self.life = random.randint(20, 40)
        # 颜色：带透明度的粉色 (R, G, B, Alpha透明度)
        self.color = (255, 105, 180, random.randint(150, 220))

    def update(self):
        """每一帧更新粒子的状态"""
        self.x += self.vx
        self.y += self.vy
        self.size += self.grow_speed
        self.life -= 1

    def is_alive(self):
        """检查粒子是否还活着"""
        return self.life > 0


# ================= 1. 初始化模型和全局变量 =================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils
TIP_IDS = [4, 8, 12, 16, 20]

# 【新增全局变量】
particles = []  # 存储活跃粒子的列表
gesture_was_active = False  # 记录上一帧是否触发了爱心，防止重复触发

# 【优化】预先加载大号字体，避免在动画循环中重复加载导致卡顿
main_font = load_chinese_font(size=80)


# ================= 2. 辅助函数 (保持不变) =================
def calculate_distance(p1, p2):
    return math.hypot(p1.x - p2.x, p1.y - p2.y)


def get_finger_status(hand_landmarks, hand_label):
    fingers = []
    # 大拇指
    if hand_label == 'Left':
        if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
            fingers.append(1)
        else:
            fingers.append(0)
    else:
        if hand_landmarks.landmark[4].x > hand_landmarks.landmark[3].x:
            fingers.append(1)
        else:
            fingers.append(0)
    # 其他四指
    for id in range(1, 5):
        if hand_landmarks.landmark[TIP_IDS[id]].y < hand_landmarks.landmark[TIP_IDS[id] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    return fingers


# ================= 3. 主程序 =================
cap = cv2.VideoCapture(0, cv2.CAP_AVFOUNDATION)

print("🚀 究极融合版系统启动中... 准备比心！")

while True:
    success, img = cap.read()
    if not success: break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    face_results = face_mesh.process(img_rgb)
    hand_results = hands.process(img_rgb)

    final_message = ""
    # 注意：为了配合 PIL 的 RGBA 绘图，这里颜色使用 RGB 格式
    message_color = (255, 255, 255)
    gesture_detected = False

    # 【新增】当前帧的爱心状态标记和中心点
    is_loving_now = False
    love_center = (w // 2, h // 2)

    # ----------------- 手势识别 -----------------
    if hand_results.multi_hand_landmarks:
        # 爱心检测
        if len(hand_results.multi_hand_landmarks) == 2:
            hand1 = hand_results.multi_hand_landmarks[0]
            hand2 = hand_results.multi_hand_landmarks[1]
            # 检查食指尖距离
            if calculate_distance(hand1.landmark[8], hand2.landmark[8]) < 0.1:
                final_message = "爱你捏 ❤️"
                message_color = (255, 105, 180)  # 粉色 RGB
                gesture_detected = True

                # 【新增】标记当前为爱心状态，并计算爆炸中心点（两食指中间）
                is_loving_now = True
                cx = int((hand1.landmark[8].x + hand2.landmark[8].x) / 2 * w)
                cy = int((hand1.landmark[8].y + hand2.landmark[8].y) / 2 * h)
                love_center = (cx, cy)

        # 单手检测 (保留你的原始逻辑)
        if not gesture_detected:
            for hand_landmarks, hand_info in zip(hand_results.multi_hand_landmarks, hand_results.multi_handedness):
                hand_label = hand_info.classification[0].label
                fingers = get_finger_status(hand_landmarks, hand_label)
                thumb_tip_y = hand_landmarks.landmark[4].y
                thumb_ip_y = hand_landmarks.landmark[3].y

                if fingers[1] == 0 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                    final_message = "你傻逼吗"
                    message_color = (255, 0, 0)  # 红色 RGB
                    gesture_detected = True
                elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 0 and fingers[4] == 0:
                    final_message = "耶✌️"
                    message_color = (255, 255, 0)  # 黄色 RGB
                    gesture_detected = True
                elif fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 0:
                    if thumb_tip_y < thumb_ip_y:
                        final_message = "太带派了！"
                        message_color = (255, 165, 0)  # 橙色 RGB
                        gesture_detected = True
                    elif thumb_tip_y > thumb_ip_y:
                        final_message = "太逊了"
                        message_color = (128, 128, 128)  # 灰色 RGB
                        gesture_detected = True
                elif fingers[1] == 0 and fingers[2] == 0 and fingers[3] == 0 and fingers[4] == 1:
                    final_message = "也就这样吧"
                    message_color = (100, 100, 100)  # 深灰 RGB
                    gesture_detected = True

                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # ----------------- 表情识别 (保留原始逻辑) -----------------
    if not gesture_detected and face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            left_y = face_landmarks.landmark[61].y * h
            right_y = face_landmarks.landmark[291].y * h
            lips_y = (face_landmarks.landmark[13].y * h + face_landmarks.landmark[14].y * h) / 2
            offset = lips_y - (left_y + right_y) / 2
            if offset > 8:
                final_message = "开心 :)"
                message_color = (0, 255, 0)  # 绿色 RGB
            elif offset < -8:
                final_message = "难过 :("
                message_color = (0, 0, 255)  # 蓝色 RGB

    # ================= 【核心修改】动画触发与渲染 =================

    # 1. 粒子触发逻辑：如果当前是爱心，且上一帧不是，则触发爆炸
    if is_loving_now and not gesture_was_active:
        for _ in range(60):  # 生成60个粒子
            particles.append(HeartParticle(love_center[0], love_center[1]))

    # 更新状态，供下一帧判断
    gesture_was_active = is_loving_now

    # 2. 开始渲染：将 OpenCV 图像转换为 PIL RGBA 模式 (带透明通道)
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)).convert("RGBA")

    # 3. 创建一个完全透明的图层，用于绘制粒子和文字
    overlay = Image.new('RGBA', pil_img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # 4. 更新并绘制所有活跃粒子到透明层上
    alive_particles = []
    for p in particles:
        p.update()
        if p.is_alive():
            # 画半透明圆形
            draw.ellipse(
                [p.x - p.size, p.y - p.size, p.x + p.size, p.y + p.size],
                fill=p.color, outline=None
            )
            alive_particles.append(p)
    particles = alive_particles  # 清理死掉的粒子

    # 5. 绘制文字到透明层上 (使用预加载的大号字体)
    if final_message:
        # 将 RGB 颜色转换为 RGBA (完全不透明)
        text_color_rgba = (message_color[0], message_color[1], message_color[2], 255)
        draw.text((50, 100), final_message, font=main_font, fill=text_color_rgba)

    # 6. 图层合成：将透明层叠加到视频背景层上
    # alpha_composite 是实现高质量半透明叠加的关键
    pil_img = Image.alpha_composite(pil_img, overlay)

    # 7. 转回 OpenCV 格式用于显示
    img_final = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGBA2BGR)

    cv2.imshow('Ultimate Gesture FX', img_final)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()