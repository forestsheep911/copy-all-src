# 项目拷贝工具

这是一个用于拷贝整个项目代码和文件夹结构的工具。它会将项目的目录结构和文件内容复制到剪贴板。

## 安装依赖

首先，你需要安装项目所需的依赖。你可以使用以下命令安装：

```sh
pip install -r requirements.txt
```

# 使用方法
## 直接运行

你可以直接运行 src/main.py 脚本来获取当前目录的结构和文件内容：

```sh
python src/main.py
```

## 生成可执行文件

你可以使用 PyInstaller 将脚本打包成可执行文件。我们已经提供了一个 build.py 脚本来简化这个过程。运行以下命令生成可执行文件：

```sh
python build.py
```

生成的可执行文件会保存在 dist 目录中。

## 使用 GitHub Actions 进行自动化构建

我们提供了一个 GitHub Actions 工作流文件 .github/workflows/build.yml，它可以在不同操作系统上自动生成可执行文件。你只需将代码推送到 GitHub 仓库，GitHub Actions 会自动运行并生成可执行文件。

# 新功能

## 额外的忽略文件和目录

你现在可以通过命令行参数指定额外的忽略文件和目录。例如：

```sh
python src/main.py --ignore "*.txt" "*.log" --ignore-dir "test" "tmp"
```

## 命令行参数说明

- ignore: 额外的忽略文件模式（支持通配符）。
- ignore-dir: 额外的忽略目录。

示例

```sh
python src/main.py --ignore "*.txt" --ignore-dir "test"
```

这将忽略所有 .txt 文件和 test 目录。