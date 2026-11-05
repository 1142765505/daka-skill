# 姓名、编号与参考库

用户已授权公开本表与参考照片。401与403编号独立。工位、裁图坐标和补充视角见 [编号元数据](private/roster.json) 和 [参考选择](private/people.md)。private/ 为兼容旧版保留的目录名。

## 401

|编号|姓名|
|---|---|
|1|羊沐阳|
|2|李涛|
|3|耿芳东|
|4|世文富|
|5|芦强|
|6|陈子悦|
|7|张志扬|
|8|吕明辰|
|9|岳松涛|
|10|董林锐|

## 403

|编号|姓名|
|---|---|
|1|徐潇|
|2|张榆晗|
|3|项梓怡|
|4|崔旺|

## 配置与重建

roster.json 每个人含 id、name、identity_source、identity_box（原图归一化裁图范围）、scene_references、notes、visibility_policy；identity_references 可含多个 source/box/view，是补充视角，不是新底图坐标。401的7–10为 hair_or_forehead_allowed，其余为 reference_supported_view。

执行前实际看原始标注与参考，不按照片文件名当人物编号。运行 python scripts/build_library.py 重建全部原图概览、主身份裁图和补充裁图；prepare_references.py 输出所选身份板和可用补充视角板。缺资料须报告，脚本不训练模型或自动识别人脸。输入照片是否已存在人物须重新实际看图。
