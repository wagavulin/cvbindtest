# OpenCVバインディングメモ

## 機能と実装状況

### 全体

* グローバル関数
* クラス
* コンストラクタ
* デストラクタ
* インスタンスメソッド
* クラスメソッド (static)
* enum
* cv以下の名前空間
* 仮想関数
* 純粋仮想関数
* インターフェース (純粋仮想関数を持つクラス)

### 引数・戻り値

* out (ポインタ)
* in/out (ポインタ)
* out (参照)
* in/out (参照)

### 引数・戻り値型

* int
* float
* ...


## gen2rb.py内部クラス

`CppHeaderParser.parse()`の戻り値は6要素のリストのリスト

```python
decls = parser.parse(hdr)
for decl in decls:
    print(decl[0]) #=> method name
```

* クラス・構造体
  * decl[0]: 名前 "class cv.Foo"
  * decl[1]: 親クラス ": cv::Algorithm"
  * decl[2]: ? []
  * decl[3]: ? []
  * decl[4]: ? None
  * decl[5]: ? "". docstring?
* 関数
  * decl[0]: 名前 "cv.Foo.method1"
  * decl[1]: 戻り値 "int". ただし`cv::MyTemplate1<cv::Foo>`のときは"MyTemplate1_Foo"
  * decl[2]: 修飾子 `["/S"]`, `["/V", "/PV"]`など
  * decl[3]: 引数 `[["int", "a", "", []], ["int", "b", "", []]]`. 各要素は4要素のリスト
    * item[0]: 型 "int", "float*", "Foo", "string"など. 名前空間cv, stdは省略される
    * item[1]: 仮引数 "a"
    * item[2]: デフォルト値 "123"
    * item[3]: 修飾子 `["/Ref"]`, `["/C", "/Ref"]`など. "/C": const, "/Ref": 参照
  * decl[4]: 戻り値 "int", `"cv::MyTemplate1<cv::Foo>"`など
  * decl[5]: ? "". docstring?
* enum
  * decl[0]:
  * decl[1]:
  * decl[2]:
  * decl[3]:
  * decl[4]:
  * decl[5]:
