# eVTOL 可视化程序部署说明

本文档用于把本项目发送给导师或在其他 Windows 电脑上运行。

## 1. 项目内容

本项目是一个本地运行的 Streamlit 可视化程序，包含两个模块：

- 第一模块：二维平面 eVTOL 起降点选址，包括需求点生成、K-means 候选点生成、GA 综合优化选址和结果可视化。
- 第二模块：路径规划与算法对比，包括客户起降点到机场接驳点的 A*、RRT* 路径规划、动态搜索过程展示和量化指标对比。

程序不需要联网运行。只有第一次安装 Python 依赖时需要联网下载依赖包。

## 2. 发送给导师前的打包方式

请把整个项目文件夹打包为 zip：

```text
eVTOL_site_selection
```

建议包含以下文件和文件夹：

```text
eVTOL_site_selection
├─ main.py
├─ requirements.txt
├─ run_app.bat
├─ README.md
├─ DEPLOYMENT.md
└─ evtol
   ├─ __init__.py
   ├─ scene.py
   ├─ fields.py
   ├─ clustering.py
   ├─ ga.py
   ├─ visualization.py
   ├─ path_planning.py
   ├─ path_analysis.py
   └─ path_visualization.py
```

不建议打包以下内容：

```text
.venv
__pycache__
*.pyc
```

原因是 `.venv` 是你电脑上的虚拟环境，导师电脑上的路径和 Python 版本可能不同，复制过去反而容易报错。

## 3. 导师电脑环境要求

推荐环境：

- Windows 10 或 Windows 11
- Python 3.10 或更高版本
- Chrome、Edge 或其他现代浏览器
- 能够访问互联网，用于第一次安装依赖

## 4. 安装 Python

如果导师电脑已经安装 Python，可以跳过本节。

如果没有安装，请访问：

[https://www.python.org/downloads/](https://www.python.org/downloads/)

下载并安装 Python 3.10 或更高版本。

安装时请务必勾选：

```text
Add python.exe to PATH
```

安装完成后，打开 PowerShell，输入：

```powershell
python --version
```

如果能看到类似下面的输出，说明 Python 安装成功：

```text
Python 3.12.x
```

如果 `python` 命令不可用，也可以尝试：

```powershell
py -3 --version
```

## 5. 一键运行方式

导师收到 zip 后，请按以下步骤操作：

1. 解压 `eVTOL_site_selection.zip`。
2. 进入解压后的 `eVTOL_site_selection` 文件夹。
3. 双击 `run_app.bat`。
4. 第一次运行时，脚本会自动创建 `.venv` 虚拟环境并安装依赖。
5. 安装完成后，浏览器会自动打开程序页面。

如果浏览器没有自动打开，请在命令行窗口中找到类似下面的地址：

```text
Local URL: http://localhost:8501
```

把该地址复制到浏览器地址栏打开即可。

## 6. 命令行运行方式

如果不想双击脚本，也可以用 PowerShell 手动运行。

进入项目目录：

```powershell
cd 项目所在路径\eVTOL_site_selection
```

创建虚拟环境：

```powershell
python -m venv .venv
```

激活虚拟环境：

```powershell
.\.venv\Scripts\activate
```

安装依赖：

```powershell
pip install -r requirements.txt
```

启动程序：

```powershell
streamlit run main.py
```

如果 `streamlit` 命令无法识别，可以使用：

```powershell
python -m streamlit run main.py
```

## 7. 依赖包说明

项目依赖写在 `requirements.txt` 中：

```text
streamlit
numpy
pandas
plotly
```

其中：

- `streamlit` 用于交互式网页界面。
- `numpy` 用于数值计算、风险场和路径规划。
- `pandas` 用于表格数据和 CSV 导出。
- `plotly` 用于交互式二维图、热力图、路径图和对比柱状图。

## 8. 程序使用说明

程序启动后，会看到两个主标签页：

- `第一模块：起降点选址`
- `第二模块：路径规划与算法对比`

### 第一模块

可调整：

- 需求点数量
- 随机种子
- K-means 聚类数
- GA 最终选址数量
- GA 种群规模和迭代次数
- 需求、风险、成本权重
- 风险热点数量和强度
- 成本分布模式

可查看：

- 原始需求点图
- K-means 聚类图
- 风险场和成本场
- GA 最终选址结果
- GA 收敛曲线
- 候选点和最终选址数据

### 第二模块

可调整：

- 客户侧起降点起点
- 算法运行方式：算法对比、A* 算法、RRT* 算法
- 路径长度权重
- 风险权重
- 成本权重
- A* 网格分辨率和启发函数
- RRT* 迭代次数、步长、邻域半径和目标偏置概率
- 动态搜索进度

可查看：

- 风险热力图
- 障碍区域
- 客户起降点
- 机场接驳终点
- A* open list / closed list 搜索过程
- RRT* 采样点和搜索树
- 最终路径
- A* 与 RRT* 指标对比
- 批量起点路径对比

## 9. 常见问题

### 问题 1：双击 `run_app.bat` 后提示 Python was not found

原因：导师电脑没有安装 Python，或安装时没有勾选 `Add python.exe to PATH`。

解决方式：

1. 安装 Python 3.10 或更高版本。
2. 安装时勾选 `Add python.exe to PATH`。
3. 重新打开 PowerShell 或重新双击 `run_app.bat`。

### 问题 2：安装依赖很慢或失败

原因：网络较慢，或无法访问默认 Python 包源。

可以尝试使用国内镜像安装：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

然后再运行：

```powershell
.\.venv\Scripts\python.exe -m streamlit run main.py
```

### 问题 3：提示 streamlit 不是内部或外部命令

解决方式：

在项目目录下运行：

```powershell
.\.venv\Scripts\python.exe -m streamlit run main.py
```

或者直接双击 `run_app.bat`。

### 问题 4：浏览器没有自动打开

解决方式：

在命令行窗口中复制 `Local URL`，例如：

```text
http://localhost:8501
```

然后手动粘贴到浏览器地址栏打开。

### 问题 5：提示端口 8501 被占用

可以换一个端口运行：

```powershell
.\.venv\Scripts\python.exe -m streamlit run main.py --server.port 8502
```

然后打开：

```text
http://localhost:8502
```

### 问题 6：页面显示旧内容

解决方式：

- 在浏览器中按 `Ctrl + F5` 强制刷新。
- 关闭原来的 Streamlit 终端窗口，重新运行 `run_app.bat`。

## 10. 给导师的最简运行说明

如果导师只想快速运行，可以按下面三步：

```text
1. 安装 Python 3.10 或更高版本，安装时勾选 Add python.exe to PATH。
2. 解压 eVTOL_site_selection.zip。
3. 双击 run_app.bat。
```

第一次运行会自动安装依赖，完成后浏览器会打开程序页面。

