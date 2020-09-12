# juejin-integral-database

简单的 KV 数据库，以实现 markdown 积分表的快速管理及数据统计

### Schema

<div align=center>
<img src="./schema.png" width="500px" />
</div>

### Feature List

- [x] 解析 `integrals.md` 并构建 KV 数据库
- [ ] 校验历史积分
- [x] 增加作者功能
- [x] 增加积分奖励功能
- [x] 增加文章功能
- [ ] 增加积分兑换功能
- [x] 增加统计功能
- [x] 将数据库导出为 `integrals.md` 文件
- [ ] 外部 API，用于后续模型



### 生成近期文章列表

```bash
python3 script_generate_catalog.py --label=前端
```

### 将生成的近期文章列表与历史文章列表合并

作用：因为之前有一些文章没有标签，无法通过前面的脚本获取，因此需要根据文章名为 uid 做一次合并。

```bash
python3 script_merge_catalog.py --source=前端.md --target=front-end.md
```

会生成 new_front-end.md，source 文件的内容在前面，target 文件的内容在后面。