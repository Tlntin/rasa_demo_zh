### 参考说明
- 参考自：https://github.com/RasaHQ/retail-demo
### 使用说明
1. 安装numpy 1.18.5
```bash
pip install numpy==1.18.5
```
2. 安装tensorflow-gpu==2.3.2
```bash
pip install tensorflow-gpu==2.3.2
```
3. 安装rasa x
```bash
pip install --use-deprecated=legacy-resolver --user rasa-x --extra-index-url https://pypi.rasa.com/simple
```
4. 安装其它模块
```bash
pip install -r requirements.txt
```
5. 修改rasa源码，使得其支持zh。
```bash
UnsupportedLanguageError: component 'LanguageModelTokenizer' does not support language 'zh'.
```
修改路径为：/home/tlntin/anaconda3/envs/rasa2/lib/python3.8/site-packages/rasa/nlu/tokenizers/whitespace_tokenizer.py
去除`not_supported_language_list = ["zh", "ja", "th"]`中的zh。
6. 设置rasa x密码
```bash
export RASA_X_PASSWORD=< you password>
```
7. 运行自定义actions
```bash
rasa run actions
```
8. 手动去HuggingFace下载模型[链接](https://huggingface.co/bert-base-chinese/tree/main)
9. 启动实体标注器
```bash
docker run -p 8000:8000 --name duck rasa/duckling
```
10. 运行rasa x，实现前端可视化
```bash
rasa x
```

### 当前进度
- [x] 订单查询
- [x] 取消订单
- [x] 我要退货
- [ ] 关注收藏
- [x] 查询库存
- [x] 评分系统

### 常见action
```bash
 - action_listen
 - action_restart
 - action_session_start
 - action_default_fallback
 - action_deactivate_loop
 - action_revert_fallback_events
 - action_default_ask_affirmation
 - action_default_ask_rephrase
 - action_two_stage_fallback
 - action_back

```