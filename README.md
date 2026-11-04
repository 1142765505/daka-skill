# 打卡-skill
401和403打卡照自动生成
仅支持网页版、桌面版和移动版ChatGPT/codex


Codex 技能，技术名 `daka-skill`，中文调用“使用打卡skill”。401 编号1–10，403编号1–4。

| 输入 | 命令示例 | 行为 |
|---|---|---|
|一张401照片|使用打卡skill，401增加3|3号已存在则跳过并提示，否则新增|
|一张401照片|使用打卡skill，401增加3、4、5|只补缺席编号，保留原有其他人|
|无照片|使用打卡skill，401增加3、4、5|重建401场景，仅出现3/4/5|
|无照片|使用打卡skill，增加全部|默认401，生成1–10全员|
|有/无照片|使用打卡skill，403增加4|有底图只补缺席4号；无底图仅生成4号|
|无照片|使用打卡skill，403增加全部|生成403的1–4全员|

每次需编辑时生成3张独立候选，保存到技能目录 `output/`；全部目标已存在则不重复生成。输出为AI合成图，不提交考勤。

## 安装及本地照片

将仓库安装为 `~/.codex/skills/daka-skill`，或从该目录链接到本项目。仓库只包含通用规则、脚本和许可证，不含原始照片、身份裁图、外貌描述、人物坐标、工位映射或生成结果。

首次使用须按 `references/people.md` 在本机配置 `references/private/roster.json`、`references/private/people.md` 和自己的标注照片。缺少这些私有资料时技能会报告缺少参考，不能仅凭公开代码复现任何人的照片。

这是一套参考引导流程，不是微调模型；参考中的遮挡、远景或侧背面信息不能扩充成未经支持的清晰正脸。

```sh
python -m pip install -r requirements.txt
python scripts/build_library.py
python scripts/plan.py --command '使用打卡skill，401增加3、4、5' --has-input --present 3
python -m unittest discover -s tests
```

`--present` 和 `--uncertain` 必须来自 Codex 实际看图，脚本不做人脸识别。工具依赖为可用的图像编辑/生成能力；没有内置工具时会明确报告。

开源代码采用 MIT；原始照片、人物参考元数据、裁图和生成结果不属于此代码许可证授权范围，不进入Git仓库。文件名是照片索引，不是人物编号。
