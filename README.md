# Anime-Qbittorrent
参考bangumi的信息通过qbittorrent下载单集动画的工具。

## 功能

- 搜索查询bangumi的信息，从而获取对应的subject_id。
- 自定义单集动画的文件名、文件保存的文件夹名以及动画的下载路径。
- 保存已添加动画的bangumi信息，包括日文名、中文名、动画发行的年月日，可用来对动画文件名进行自定义。

## 使用说明

- 通过search页面输入想要搜索的动画关键词，可找到想要下载的动画信息，右键可复制该动画的subject_id。
- 在torrent页面，可以选择已经添加的动画，或者点击`添加动画`按钮，并输入subject_id来添加动画到动画列表中，重新选择动画后，会根据bangumi的信息提供集数选择。
- 在torrent页面，可设置动画下载的tag，方便管理。
- 在torrent页面，选中`删除torrent文件`，则会在下载导入到qbittorrent后删除本地的torrent文件

- 在setting页面，可设置各种信息，其中动画文件夹和动画名可使用`[name]`、`[name_cn]`、`[year]`、`[month]`和`[day]`进行自定义名称，并提供预览效果。

![image-20230602095802263](http://raw.banned.top/img/2023/06/02/095802.png)

## todo

- [ ] rss订阅
- [ ] 一个季度动画下载
- [ ] 动画数据库管理
