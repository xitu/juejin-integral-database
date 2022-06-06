import re
import os

catalogue = [
    {
        "name": "区块链",
        "file": "blockchain.md",
        "topK": 5,
        "delimiter": r"^(.*## 区块链\n\n).+?(\* \[所有区块链译文>>\].*)$"
    },
    {
       "name": "人工智能",
       "file": "AI.md",
       "topK": 5,
       "delimiter": r"^(.*## 人工智能\n\n).+?(\* \[所有 AI 译文>>\].*)$"
    },
    {
       "name": "Android",
       "file": "android.md",
       "topK": 5,
       "delimiter": r"^(.*## Android\n\n).+?(\* \[所有 Android 译文>>\].*)$"
    },
    {
       "name": "iOS",
       "file": "ios.md",
       "topK": 5,
       "delimiter": r"^(.*## iOS\n\n).+?(\* \[所有 iOS 译文>>\].*)$"
    },
    {
       "name": "前端",
       "file": "front-end.md",
       "topK": 8,
       "delimiter": r"^(.*## 前端\n\n).+?(\* \[所有前端译文>>\].*)$"
    },
    {
       "name": "后端",
       "file": "backend.md",
       "topK": 8,
       "delimiter": r"^(.*## 后端\n\n).+?(\* \[所有后端译文>>\].*)$"
    },
    {
       "name": "设计",
       "file": "design.md",
       "topK": 5,
       "delimiter": r"^(.*## 设计\n\n).+?(\* \[所有设计译文>>\].*)$"
    },
    {
       "name": "产品",
       "file": "product.md",
       "topK": 5,
       "delimiter": r"^(.*## 产品\n\n).+?(\* \[所有产品译文>>\].*)$"
    },
    {
       "name": "其他",
       "file": "others.md",
       "topK": 5,
       "delimiter": r"^(.*## 其他\n\n).+?(\* \[所有其他分类译文>>\].*)$"
    }
]


def generate_index():
    readme = open('../gold-miner/README.md').read()
    for clazz in catalogue:
        readme = re.sub(clazz['delimiter'], r'\1{}\2', readme, flags=re.DOTALL)
        new_content = os.popen(f'cat ../gold-miner/{clazz["file"]} | grep "^* \[" | head -n {clazz["topK"]}').read()
        readme = readme.format(new_content)
    open('../gold-miner/README.md', 'w').write(readme)


if __name__ == '__main__':
    generate_index()
