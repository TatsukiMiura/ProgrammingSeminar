# プロファイラとは
プロファイラとは，プログラムについての様々な統計値を算出し，プログラムの実行効率を調べるためのプログラム．  
Python標準ライブラリは`cProfile`, `profile`などのモジュールによりプロファイラ機能を提供している．  
* `cProfile` : ほとんどのユーザーに推奨される．オーバーヘッドが小さい．
* `profile` : オーバーヘッドが大きい．自分でプロファイラを拡張する場合に適する．

# 決定論的プロファイリング
上記のプロファイラはプログラムに対する決定論的プロファイリングを行う．  
決定論的プロファイリングとは，関数の呼び出し，戻り値，例外発生のタイミングを全て正確に記録する方法．  
(統計的プロファイリングというものもある．こちらはランダムにサンプリングを行うためオーバヘッドが小さいが詳細さに欠ける．)  
決定論的プロファイリングによる情報は，コード中のバグの発見，最適化すべき箇所(実行回数の多い箇所)の特定，エラー検知に役立つ．  
以下，cProfileについて説明する．

# インタプリタ上で指定した関数をプロファイルする
    def f(x):
        ...
        ...
        return
    import cProfile
    cProfile.run('f(x)')
f(x)が実行され，同時にプロファイル結果が表示される．  

    def f(x):
        ...
        ...
        return
    import cProfile
    cProfile.run('f(x)', 'output_file')
第2引数でファイル名を指定してプロファイル結果を出力できる．

# スクリプトファイル全体をプロファイルする
    python -m cProfile sample.py
とするとsample.py全体をプロファイルできる

    python -m cProfile -o output_file sample.py
というようにオプション引数を書くとファイルに出力できる．

    python -m cProfile -s sort_order sample.py
というようにオプション引数を書くとプロファイル結果をソートして表示できる．(利用可能なソートは後述．また，-oとの併用は不可．)

# プロファイル結果の例
例として次のようなプログラムを用意した．

    def f1(n):
        counter = 0
        for i in range(n):
            counter += 1
        return counter

    def f2(n):
        counter = 0
        for i in range(n):
            for j in range(n):
                counter += 1
        return counter

    def f3(n):
        counter = 0
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    counter += 1
        return counter

    f1(1000)
    f2(1000)
    f3(1000)
f1はO(n)，f2はO(n<sup>2</sup>)，f3はO(n<sup>3</sup>)である．  
そして，

    python -m cProfile -o sample/sample_result sample/sample.py
を実行し，次のようなプロファイル結果を得た．

    6 function calls in 42.656 seconds

    Random listing order was used

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    1    0.000    0.000    0.000    0.000 {method 'disable' of '\_lsprof.Profiler' objects}
    1    0.045    0.045    0.045    0.045 sample/sample.py:7(f2)
    1    0.000    0.000    0.000    0.000 sample/sample.py:1(f1)
    1    0.000    0.000   42.656   42.656 sample/sample.py:1(<module>)
    1    0.000    0.000   42.656   42.656 {built-in method builtins.exec}
    1   42.611   42.611   42.611   42.611 sample/sample.py:14(f3)

最初の行は2706回の関数呼び出しがあったことを表す．また，このうち2004回はプリミティブな(再帰でない)関数呼び出しであったことを表す．  
'Ordered by: standard name'は，ソート順を表す．
* ncalls : 呼び出し回数 43/3は1番目の値が呼び出し回数，2番目の値がプリミティブな呼び出し回数を表す．
* tottime : この関数が消費した時間の合計(下位の関数は除く)
* percall　tottimeをncallsで割った値
* cumtime 下位の関数を含むこの関数の消費時間の合計
* percall cumtimeをプリミティブな呼び出し回数で割った値
* filename:lineno(function) : その関数のファイル名，行番号，関数名


# 出力したプロファイル結果を確認する
    import pstats
    p = pstats.Stats('output')
と書いてStatsクラスのインスタンスを生成する．
