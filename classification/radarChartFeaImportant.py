import numpy as np
import matplotlib.pyplot as plt

# 标签
labels = np.array(['Distance', '85thV', 'MaxV1', 'MaxV2', 'MedianV', 'MinV',
                   'MeanV', 'Ev', 'Dv', 'HVR', 'MVR',
                   'LVR', '85thA', 'MaxA1', 'MaxA2', 'MedianA',
                   'MinA', 'MeanA', 'Ea', 'Da', 'HAR', 'MAR',
                   'LAR', 'TS', 'ACR', 'BSR', 'ACP', 'HCR', 'SR',
                   'VCR'])
# 数据个数
dataLenth = len(labels)
# 数据
data = np.array([4.6165, 10.501, 2.076438, 2.3706596, 6.0653, 1.8108588,
                 7.06278475, 5.28236521, 4.917403, 5.44433, 6.63058447,
                 8.751993, 1.63081, 1.7161647, 1.77280736, 1.59987,
                 1.27414, 1.72476, 1.7521, 2.301, 1.67848, 1.56358,
                 1.365, 0.2, 2.07975, 1.045268, 2.878, 3.4058, 3.546,
                 3.03805])

angles = np.linspace(0, 2 * np.pi, dataLenth, endpoint=False)
data = np.concatenate((data, [data[0]]))  # 闭合
angles = np.concatenate((angles, [angles[0]]))  # 闭合

fig = plt.figure()
ax = fig.add_subplot(111, polar=True)  # polar参数！！
ax.plot(angles, data, color='r')  # 画线
ax.fill(angles, data, facecolor='r', alpha=0.25)  # 填充
# ax.set_thetagrids(angles * 180 / np.pi, labels, fontproperties="SimHei")
# ax.set_title("matplotlib雷达图", va='bottom', fontproperties="SimHei")
ax.set_thetagrids(angles * 180 / np.pi, labels)
ax.set_rlim(0, 11)
ax.grid(True)
plt.show()
