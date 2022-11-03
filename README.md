### 参考说明
- 参考自：https://github.com/RasaHQ/retail-demo
### 使用说明
1. 安装numpy 1.18.5
```bash
pip install numpy==1.18.5
```
2. 安装tensorflow==2.3.1(注意，除非是你源码编译的，否则直接装CPU版就行了), pytorch==1.8.1(可选值，可以不装，这个是spacy需要，建议装一下)，理论上CPU版的就够用了。
```bash
pip install tensorflow==2.3.1
pip install torch==1.8.1
```
3. 安装rasa以及rasa-sdk。
```bash
pip install rasa==2.8.1
pip install rasa-sdk==2.8.1
```
4. 编译或者直接安装xmlsec库，否则pip安装的xmlsec的时候必报错。
```bash
sudo apt install libxmlsec1-dev libtool-bin
# 或者源码安装也行
# 源码下载地址 https://github.com/lsh123/xmlsec/tags
# 解压源码，进入对应目录后。执行下面操作进行安装(j8根据你的CPU核心线程数，可以为j+其它数字)
./autogen.sh
make -j8
```
5. 安装剩余python模块
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --extra-index-url https://pypi.rasa.com/simple
```

6. 安装spacy与中文模型
```bash
pip install spacy
python -m spacy download zh_core_web_trf
```

7. 设置rasa x密码
```bash
export RASA_X_PASSWORD=< you password>
```
8. 运行自定义actions
```bash
rasa run actions
```
9. 手动去HuggingFace下载模型[链接](https://huggingface.co/bert-base-chinese/tree/main), 将tensorflow的权重，放到data/model文件夹下面,参考结果如下
```bash
data/model/config.json
data/model/pytorch_model.bin(可选)
data/model/tf_model.h5
data/model/vocab.txt
```
10. 启动实体标注器
```bash
docker run -p 8000:8000 --name duck rasa/duckling
```
11. 运行rasa x，实现前端可视化
```bash
rasa x
```
12. 启动api服务
```bash
rasa run -m models --enable-api --cors "*" --debug
```
13. html前端界面（用nginx装一下或者用浏览器打开html都可以测试）
```bash
https://github.com/JiteshGaikwad/Chatbot-Widget
```
```bash
export TOKENIZERS_PARALLELISM=true
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