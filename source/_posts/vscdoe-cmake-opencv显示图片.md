---
title: vscdoe+cmake+opencv显示图片
tags: cmake c++
abbrlink: 16809
date: 2024-10-03 14:20:03
---
> **[参考教程](https://www.cnblogs.com/xiyin/p/16618245.html)是这个，不过有几处不同,我用的是[opencv4.80](https://opencv.org/releases/)，现在已经出到4.10了，[cmake是3.28](https://cmake.org/download/)，前提是你的**
>
> **opencv和cmake下载好然后环境已经配好，这些教程网上都有，我就不写了，编译器可以使用msys2进行下载这个教程**
>
> **很详细**

**我用的编译器是这个，用的参考教程的编译器老是报错就换成这个了**

![编译器](/images/gcc.jpg)

## vscode要装的插件如下

![插件](/images/tools.jpg)

> **opencv的环境一定要按照我给的参考教程配置，不然会报错。**


## CMakeLists.txt 配置

```
cmake_minimum_required(VERSION 3.5.0)
project(opencv VERSION 0.1.0 LANGUAGES C CXX)

add_executable(opencv main.cpp)

include(CTest)
enable_testing()
find_package(OpenCV REQUIRED)
include_directories(${OpenCV_INCLUDE_DIRS})
target_link_libraries(opencv ${OpenCV_LIBS})
set(CPACK_PROJECT_NAME ${PROJECT_NAME})
set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
include(CPack)

```

## main.cpp程序

```
#include <iostream>
#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>
using namespace cv;
using namespace std;

int main() {
    // 指定图片路径
    string imagePath = "D:/Users/huang/Desktop/opencv_demo/1.jpg";  // 替换为你的图片路径
  
    // 输出图片路径以确认是否正确
    cout << "Loading image from: " << imagePath << endl;

    Mat image = imread(imagePath, IMREAD_COLOR);  // 读取文件

    if (image.empty()) {  // 检查图像是否成功加载
        cout << "Could not open or find the image" << endl;
        return -1;
    }

    namedWindow("Display window", WINDOW_AUTOSIZE);  // 创建窗口用于显示
    imshow("Display window", image);  // 在窗口中显示图像
    waitKey(0);  // 等待按键按下
    return 0;
}

```

## 编译运行

到这里编译运行大概率会报错，是因为**缺少由于找不到qt6core.dll,无法继续执行代码，**大概率是这个原因，这时候就要用到msys2

来安装qt6了

```
pacman -S mingw-w64-x86_64-qt6
```

安装完之后把 `D:\msys2\mingw64\include\qt6`这个路径添加到环境变量，这时候再编译运行图片就出来了
