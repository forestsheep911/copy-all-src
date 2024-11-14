# 项目拷贝工具

这是一个用于拷贝整个项目代码和文件夹结构的工具。它会将项目的目录结构和文件内容复制到剪贴板。
一个容易想到的，适用性很高的的使用场景，是复制你的项目给你正在用的 `大语言模型` 看，方便它了解你整个项目。这在调整功能跨多文件时，以及文件结构需要告知AI的时候，非常有用。

此工具会先制作出目录结构的文本样式，再遍历各个文本文件，最终把他们全部拷贝到剪贴板中。

# 效果示例

譬如，对此项目本身执行的话，会得到这样的文本（省略每个文件太长部分）

```sh
$ python src/main.py # 用python的方式执行，普通用户应使用 Release 中的对应平台的可执行文件
9 folders 7 files 13.26 KB copied # 显示拷贝成功的信息，总字节数对消耗 token 的大小控制有帮助
```

```plaintext
D:\usr\bxu\dev\github\-copy-all-src
/
│   ├── README.md
│   ├── requirements.txt
│   ├── .github/
│   │   ├── workflows/
│   │   │   ├── build.yml
│   ├── src/
│   │   ├── build.py
│   │   ├── main.py


=== README.md ===
# 项目拷贝工具

这是一个用于拷贝整个项目代码和文件夹结构的工具。它会将项目的目录结构和文件内容复制到剪贴板。
...

=== requirements.txt ===
pyperclip
pyinstaller

=== .github\workflows\build.yml ===
name: Build and Release

on:
  release:
    types: [published]
...

=== src\build.py ===
import os
import shutil
import stat


def build():
...


=== src\main.py ===
import os
import pyperclip
import argparse
import fnmatch
import mimetypes


def get_directory_structure_with_file_contents(
...

```

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

我们提供了一个 GitHub Actions 工作流文件 .github/workflows/build.yml，它可以在不同操作系统上自动生成可执行文件。现在的触发条件是：“当 Release 创建出来时，会生成三个系统的可执行文件并附加到当前 Release 中。

# 下载可执行文件

你可以从 GitHub Release 页面下载预编译的可执行文件。请根据你的操作系统选择相应的文件：

- Windows 用户：下载 cpsrc-win.exe
- macOS 用户：下载 cpsrc-mac
- Linux 用户：下载 cpsrc-linux

# 执行可执行文件

## Windows

下载 `cpsrc-win.exe`，双击运行或在命令提示符中运行：

```sh
cpsrc-win.exe
```

你也可以将 `cpsrc-win.exe` 改成方便的名字，并拷贝到常用的可执行文件夹下，这个文件夹应该加入到系统的 PATH 环境变量中，以便将来可以在任何地方运行它。

## macOS

下载 cpsrc-mac，在终端中运行以下命令授予执行权限，然后运行：

```sh
chmod +x cpsrc-mac
./cpsrc-mac
```

你也可以将可执行文件移动到 /usr/local/bin 目录中，以便在任何地方运行它：

```sh
sudo mv cpsrc-mac /usr/local/bin/cpsrc
cd your-project-dir
cpsrc
```

## Linux

和 macOS 相似，不赘述

# 忽略功能

我们提供了一些项目中常见的需要忽略的文件和文件夹，还有一些明显不是文本文件也会被忽略。

## 额外的忽略文件和目录

你现在可以通过命令行参数指定额外的忽略模式（类似于 .gitignore 的格式）。例如：

```sh
python src/main.py --ignore "*.txt" "*.log" "test/" "tmp/"
```

你还可以通过 --igfile 参数指定一个包含忽略规则的文件。其书写规则等同于 `.gitignore` 例如：

```sh
python src/main.py --igfile your-ingnore-config-file
```

## 指定只包含的文件和目录

你可以通过 --include 参数指定只包含的文件和目录。当指定这个参数时，只处理这些指定的文件或目录，并忽略其他所有文件和目录。例如：

```sh
python src/main.py --include src/main.py src/utils.py
```

当指定的是文件夹时，会遵守内置的忽略条件，如果不想忽略某些文件的，请以文件名形式传递。

## 命令行参数说明

- ignore: 额外的忽略文件模式（以文件通配符匹配字符串传参）。
- igfile: 额外的忽略文件模式（以忽略文件名传参）
- include: 指定只包含的文件和目录。
- verbose: 显示详细的调试信息。
- max-size: 能复制到剪贴板最大大小上限，纯数字不用带单位，单位内置固定为KB。（缺省默认：64KB）

# 提醒
如果你觉得生成的文本量太大，可以在项目相关需要 AI 修改的子目录下执行该工具。例如：

```sh
cd path/to/src/subdirectory
cpsrc
```

或者还是使用 `--include` 参数，因为是可以加多个值的，所以还是比较方便

```sh
cpsrc --include src config public .vscode
```

这样可以仅获取子目录的结构和文件内容，当然用忽略的配置文件是更完备的一种节省文本量的方式。