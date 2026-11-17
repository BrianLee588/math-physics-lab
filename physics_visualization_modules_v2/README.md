# 物理視覺化模組

本專案以 Python 和 Matplotlib 製作兩個可互動的物理動畫，協助觀察牛頓第二運動定律，以及物體在斜面上的摩擦力與運動狀態。使用者可調整參數，並播放、暫停或重置動畫。

## 專案檔案

```text
physics_visualization_modules_v2/
├── main.py              # 程式入口與模組選單
├── visualizations.py    # 動畫、圖表、滑桿與播放控制
├── physics_models.py    # 牛頓第二定律與斜面物理模型
├── requirements.txt     # Python 第三方套件需求
├── README.md            # 本說明文件
└── README_v2.md         # 專案原有說明文件
```

`main.py` 會呼叫 `visualizations.py` 中的 `run_newton()` 或 `run_incline()`；`visualizations.py` 使用 `physics_models.py` 進行物理計算。`physics_models.py` 僅使用 Python 標準函式庫。

## 環境需求

- Python 3.10 或更新版本
- NumPy 1.24 以上且低於 3.0
- Matplotlib 3.7 以上且低於 4.0
- 可開啟 Matplotlib 互動視窗的桌面環境

第三方套件版本範圍列於 `requirements.txt`。本專案已在 Python 3.13、NumPy 2.4 及 Matplotlib 3.11 環境中完成匯入與畫面建構檢查。

## 安裝與執行

在專案目錄開啟終端機，建立並啟用虛擬環境：

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

安裝套件並啟動程式：

```powershell
python -m pip install -r requirements.txt
python main.py
```

程式會在終端機顯示選單：輸入 `1` 開啟牛頓第二運動定律模組，輸入 `2` 開啟斜面摩擦力模組。動畫視窗開啟後，可使用畫面上的滑桿與播放、暫停、重置按鈕操作。

若使用 macOS 或 Linux，虛擬環境啟用指令為 `source .venv/bin/activate`；安裝與啟動指令相同。

## 套件

| 套件 | 用途 |
| --- | --- |
| NumPy | 向量運算及圖表資料處理 |
| Matplotlib | 動畫、圖表、滑桿與按鈕介面 |

## 注意事項

程式需要能顯示互動式圖形視窗的 Matplotlib 後端；在無桌面顯示環境中，`python main.py` 無法開啟互動視窗。某些系統字型可能缺少播放或重置按鈕使用的圖示字元，Matplotlib 會顯示缺字型警告，但不影響按鈕功能。
