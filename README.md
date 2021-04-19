# 九宫格图片切分

运行脚本将图片进行切分。

参数：

* file(f): 待切分的图片文件路径
* mode(m): 切分模式（默认为抛弃长边）
* gap(g): 是否在切分时考虑图与图之间的小间隔 （默认为考虑）



支持的模式：

* `l`: 抛弃长边部分（默认）
* `s`: 将短边部分添加白色再切分

Bonus：

* `r`: 斑马线图，不切分为九宫格。在 lineNum 中修改线的数量。用过就知道了。



示例：

```
python image-cutter.py -m l -f myimg.jpg
```



输出：

一个与文件同名的文件夹，文件夹内包含九个切分好的图片。