## Install

```sh
$ brew install mecab  # mecabのインストール
$ pip3 install mecab-python3  # バインディングのインストール
$ brew install mecab-ipadic  # 辞書のインストール
$ cd ..  # 新語の辞書のインストール。別のディレクトリでインストールしたい
$ git clone git@github.com:neologd/mecab-ipadic-neologd.git
$ ./bin/install-mecab-ipadic-neologd -n  # 結構時間がかかる。このインストールの最中にsudoでの動作が入るので注意(mecab-ipadicを先に入れないときとか)
# $ pip3 install unidic  # 辞書管理ツールのインストール
# $ python3 -m unidic download
$ mecab -D  # mecab dictionaryのcharsetがutf8かどうか確認
filename:       /usr/local/lib/mecab/dic/ipadic/sys.dic
version:        102
charset:        utf8
type:   0
size:   392126
left size:      1316
right size:     1316
```

### インストール時にはまったこと

- mecab-python3のマニュアルには`unidic`使った方がいいよって書いてあるけど、なんかみんなipadic使っているっぽい？？ unidicを使わない方針にした
- `$ brew install mecab-ipadic-utf8` はHomebrewのFormulaがないけど`$ brew install mecab-ipadic`でutf8のものが入る
- 新語の辞書を作ってくれている方がいたのでそれを使うことに
    - https://hibiki-press.tech/python/mecab/5153 からたどった
    - https://github.com/neologd/mecab-ipadic-neologd/blob/master/README.ja.md
