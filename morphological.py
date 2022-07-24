import MeCab
import math
from collections import Counter

training_data = [
    ['''Python（パイソン）は、オランダ人のグイド・ヴァンロッサムが作ったオープンソースのプログラミング言語。
オブジェクト指向スクリプト言語の一種であり、Perlとともに欧米で広く普及している。イギリスのテレビ局 BBC が製作したコメディ番組『空飛ぶモンティパイソン』にちなんで名付けられた。
Python は英語で爬虫類のニシキヘビの意味で、Python言語のマスコットやアイコンとして使われることがある。Pythonは汎用の高水準言語である。プログラマの生産性とコードの信頼性を重視して設計されており、核となるシンタックスおよびセマンティクスは必要最小限に抑えられている反面、利便性の高い大規模な標準ライブラリを備えている。
Unicode による文字列操作をサポートしており、日本語処理も標準で可能である。多くのプラットフォームをサポートしており（動作するプラットフォーム）、また、豊富なドキュメント、豊富なライブラリがあることから、産業界でも利用が増えつつある。''', 'Python'],
    ['''Ruby（ルビー）は、まつもとゆきひろ（通称Matz）により開発されたオブジェクト指向スクリプト言語であり、従来 Perlなどのスクリプト言語が用いられてきた領域でのオブジェクト指向プログラミングを実現する。Rubyは当初1993年2月24日に生まれ、 1995年12月にfj上で発表された。名称のRubyは、プログラミング言語Perlが6月の誕生石であるPearl（真珠）と同じ発音をすることから、まつもとの同僚の誕生石（7月）のルビーを取って名付けられた。''', 'Ruby'],
    ['''豊富な機械学習（きかいがくしゅう、Machine learning）とは、人工知能における研究課題の一つで、人間が自然に行っている学習能力と同様の機能をコンピュータで実現させるための技術・手法のことである。ある程度の数のサンプルデータ集合を対象に解析を行い、そのデータから有用な規則、ルール、知識表現、判断基準などを抽出する。データ集合を解析するため、統計学との関連も非常に深い。
機械学習は検索エンジン、医療診断、スパムメールの検出、金融市場の予測、DNA配列の分類、音声認識や文字認識などのパターン認識、ゲーム戦略、ロボット、など幅広い分野で用いられている。応用分野の特性に応じて学習手法も適切に選択する必要があり、様々な手法が提案されている。それらの手法は、 Machine Learning や IEEE Transactions on Pattern Analysis and Machine Intelligence などの学術雑誌などで発表されることが多い。''', '機械学習'],
]


tagger = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd/')
# help(tagger)


def parse(sentence):
    node = tagger.parseToNode(sentence)

    texts = []
    while node:
        # 名詞のみ
        # if node.posid < 34 or node.posid > 68:
        # 動詞・副詞・名詞・連体詞のみ
        if node.posid < 32:
            node = node.next
            continue

        texts.append(node.surface.lower())
        node = node.next

    return texts


vocabularies = set()
word_count = dict()
category_count = Counter()

def train(training_data):
    for td in training_data:
        sentence = td[0]
        category = td[1]
        words = parse(sentence)
        for word in words:
            word_count.setdefault(category, {})
            word_count[category].setdefault(word, 0)
            word_count[category][word] += 1
            vocabularies.add(word)
        category_count[category] += 1


# P(category)
def get_prior_prob(category):
    return category_count[category] / sum(category_count.values())

def _is_in_category(word, category):
    if word in word_count[category]:
        return word_count[category][word]
    return 0

# P(word|category)
def get_word_prob(word, category):
    return (_is_in_category(word, category) + 0.1) / (sum(word_count[category].values()) + len(vocabularies))

def get_score(words, category):
    score = math.log(get_prior_prob(category))
    for word in words:
        print(category, ':', word, '->', get_word_prob(word, category))
        score += math.log(get_word_prob(word, category))
    print('  score:', score)
    return score

def classifier(doc):
    print('-----------------------------')
    print(doc)
    print('---->')
    best = None

    max_prob = -9999999999999999

    words = parse(doc)
    for category in category_count.keys():
        prob = get_score(words, category)
        if prob > max_prob:
            max_prob = prob
            best = category
    return best



train(training_data)
print('vocabularies', len(vocabularies))
for key, value in word_count.items():
    print('-------------')
    print(key)
    print(value)
print('categorycount', category_count)

# Python
doc = 'ヴァンロッサム氏によって開発されました.'
print('ANSWER:', classifier(doc))

doc = '豊富なドキュメントや豊富なライブラリがあります.'
print('ANSWER:', classifier(doc))

# Ruby
doc = '純粋なオブジェクト指向言語です.'
print('ANSWER:', classifier(doc))

doc = 'Rubyはまつもとゆきひろ氏(通称Matz)により開発されました.'
print('ANSWER:', classifier(doc))

# 機械学習
doc = '「機械学習 はじめよう」が始まりました.'
print('ANSWER:', classifier(doc))

doc = '検索エンジンや画像認識に利用されています.'
print('ANSWER:', classifier(doc))

doc = 'Python'
print('ANSWER:', classifier(doc))

doc = 'Ruby'
print('ANSWER:', classifier(doc))

doc = 'machine'
print('ANSWER:', classifier(doc))

doc = 'IEEE'
print('ANSWER:', classifier(doc))

