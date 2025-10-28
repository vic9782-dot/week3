import streamlit as st
import random
import math
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------
# 1. 함수 정의 (App 로직보다 위에 위치해야 NameError 방지)
# ----------------------------------------------------
def random_palette_monochrome(k=5):
    """Returns k random monochrome (grey) shades."""
    colors = []
    for _ in range(k):
        # 0.1 (어두운 회색) ~ 0.9 (밝은 회색) 범위의 강도 선택
        intensity = random.uniform(0.1, 0.9)
        colors.append((intensity, intensity, intensity))
    return colors

def blob(center=(0.5, 0.5), r=0.3, points=200, wobble=0.15):
    """Generates a wobbly closed shape's coordinates."""
    angles = np.linspace(0, 2*math.pi, points)
    radii = r * (1 + wobble*(np.random.rand(points)-0.5))
    x = center[0] + radii * np.cos(angles)
    y = center[1] + radii * np.sin(angles)
    return x, y

# ----------------------------------------------------
# 2. Streamlit 앱 구성 및 로직
# ----------------------------------------------------
st.title("Generative Monochrome Poster")
st.write("슬라이더를 조절하여 흑백 톤의 추상 포스터를 생성하세요.")

# --- 위젯 설정 ---
# 레이어 수 조절 (기존 8개에서 더 넓은 범위로)
n_layers = st.slider("Number of Layers (Density)", 5, 25, 12)
# Wobble 강도 조절 (0.05 ~ 0.25 범위 제어)
wobble_max = st.slider("Wobble Intensity (Shape Roughness)", 0.0, 0.5, 0.2, 0.01)

# Streamlit 위젯이 변경될 때마다 새로운 이미지를 생성하기 위해 시드 설정
random.seed() 

# Matplotlib figure와 axes 생성
fig, ax = plt.subplots(figsize=(7, 10))
ax.axis('off')
# 배경색은 아주 밝은 회색으로 유지
ax.set_facecolor((0.95,0.95,0.95))

# --- 포스터 생성 루프 ---
palette = random_palette_monochrome(8) # 8가지 흑백 톤 사용

for i in range(n_layers):
    cx, cy = random.random(), random.random()
    rr = random.uniform(0.15, 0.45) # 크기
    
    # wobble 범위는 0.05부터 사용자가 설정한 최대치까지
    wobble_val = random.uniform(0.05, wobble_max) 
    
    x, y = blob(center=(cx, cy), r=rr, wobble=wobble_val)
    color = random.choice(palette)
    
    # 흑백의 미학을 위해 투명도를 높게 설정
    alpha = random.uniform(0.5, 0.8) 
    
    # Blob 그리기 (외곽선 없이)
    ax.fill(x, y, color=color, alpha=alpha, edgecolor=(0,0,0,0)) 

# 텍스트 라벨 추가
ax.text(0.05, 0.95, "Monochrome Layers", fontsize=18, weight='bold', transform=ax.transAxes, color='black')
ax.text(0.05, 0.91, "Generative Art Study", fontsize=11, transform=ax.transAxes, color='black')

ax.set_xlim(0,1); ax.set_ylim(0,1)

# Streamlit에 Matplotlib 그림 표시
st.pyplot(fig)