# プロファイラとは
プロファイラとは，プログラムについての様々な統計値を算出し，プログラムの実行効率を調べるためのプログラムである．  
Python標準ライブラリは`cProfile`, `profile`などのモジュールによりプロファイラ機能を提供している．  
* `cProfile` : ほとんどのユーザーに推奨される．オーバーヘッドが小さい．
* `profile` : オーバーヘッドが大きい．自分でプロファイラを拡張する場合に適する．

上記のプロファイラはプログラムに対する決定論的プロファイリングを行う．  
決定論的プロファイリングとは，関数の呼び出し，戻り値，例外発生のタイミングを全て正確に記録する方法である．  
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
とするとsample.py全体をプロファイルできる．

    python -m cProfile -o output_file sample.py
というようにオプション引数を書くとファイルに出力できる．

    python -m cProfile -s sort_order sample.py
というようにオプション引数を書くとプロファイル結果をソートして表示できる．(利用可能なソートは後述．また，-oとの併用は不可．)

# プロファイル結果の例
    2706 function calls (2004 primitive calls) in 4.504 CPU seconds

    Ordered by: standard name

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
         2    0.006    0.003    0.953    0.477 pobject.py:75(save_objects)
      43/3    0.533    0.012    0.749    0.250 pobject.py:99(evaluate)
     ...
最初の行は2706回の関数呼び出しがあったことを表す．また，このうち2004回はプリミティブな(再帰でない)関数呼び出しであったことを表す．  
'Ordered by: standard name'は，標準名によってソートされたことを表す．
* ncalls : 呼び出し回数．43/3は1番目の値が呼び出し回数，2番目の値がプリミティブな呼び出し回数を表す．
* tottime : この関数が消費した時間の合計．(下位の関数は除く．)
* percall　: tottimeをncallsで割った値．
* cumtime : 下位の関数を含むこの関数の消費時間の合計．再帰的関数も計測可能．
* percall : cumtimeをプリミティブな呼び出し回数で割った値．
* filename:lineno(function) : その関数のファイル名，行番号，関数名．

# ファイルに出力したプロファイル結果の確認・操作
プロファイル結果はStatsクラスのメソッドを用いて整形出力されたものである．したがって，ファイルに出力したプロファイル結果を確認したり，何らかの操作を行う際にはStatsクラスのメソッドを用いる．以下，例を用いて説明する．次のようなプログラムsample.pyをsampleというディレクトリに用意した．

    def f1(n):
        counter = 0
        for i in range(n):
            counter += 1
        return counter

    def f2(n):
        counter = 0
        for j in range(n):
            f1(n)
        return counter

    def f3(n):
        counter = 0
        for k in range(n):
            f2(n)
        return counter

    f1(500)
    f2(500)
    f3(500)
そして，

    python -m cProfile -o sample/sample_output sample/sample.py
としてプロファイルを行い，sampleディレクトリに出力した．  出力したファイルを読み込むには，まず

    import pstats
    p = pstats.Stats('sample/sample_output')
を実行してStatsクラスのインスタンスを生成する．

    p.print_stats()
を実行するとプロファイル結果を表示できる．

    251006 function calls in 4.382 seconds

    Random listing order was used

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
    250501    4.340    0.000    4.340    0.000 sample/sample.py:1(f1)
         1    0.000    0.000    4.373    4.373 sample/sample.py:13(f3)
       501    0.041    0.000    4.382    0.009 sample/sample.py:7(f2)
         1    0.000    0.000    4.382    4.382 sample/sample.py:1(<module>)
         1    0.000    0.000    4.382    4.382 {built-in method builtins.exec}
<!--_-->

    p.strip_dirs()
を実行するとファイル名からパス部分を除去できる．

    251006 function calls in 4.382 seconds

    Random listing order was used

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    250501    4.340    0.000    4.340    0.000 sample.py:1(f1)
         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
         1    0.000    0.000    4.373    4.373 sample.py:13(f3)
         1    0.000    0.000    4.382    4.382 sample.py:1(<module>)
         1    0.000    0.000    4.382    4.382 {built-in method builtins.exec}
       501    0.041    0.000    4.382    0.009 sample.py:7(f2)
<!--_-->

    p.sort_stats(key)
により指定したキーでソートできる．2つ以上のキーを指定した場合は前のキーで等価だった場合の再ソートに用いられる．ソートは全て降順またはアルファベット順．
指定できるキーは以下の通り
* 'calls'，'ncalls' : 呼び出し回数
* 'pcalls' : プリミティブな呼び出し回数
* 'cumulative'，'cumtime' : 累積時間
* 'file'，'filename'，'module' : ファイル名
* 'module' : モジュール名
* 'pcalls' : プリミティブな呼び出し回数
* 'line' : 行番号
* 'name' : 関数名
* 'nfl' : 関数名/ファイル名/行番号
* 'stdname' : 標準名
* 'time'，'tottime' : それぞれの関数で消費された時間

また，数値を用いることもでき，-1，0,1，2はそれぞれ'stdname'，'calls'，'time'，'cumulative'として処理される．ただし，この場合2つ目以降の引数は無視される．

    p.sort_stats('calls', )
を実行し，呼び出し回数順にソートした．

    251006 function calls in 4.382 seconds

    Ordered by: call count

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    250501    4.340    0.000    4.340    0.000 sample.py:1(f1)
       501    0.041    0.000    4.382    0.009 sample.py:7(f2)
         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
         1    0.000    0.000    4.373    4.373 sample.py:13(f3)
         1    0.000    0.000    4.382    4.382 sample.py:1(<module>)
         1    0.000    0.000    4.382    4.382 {built-in method builtins.exec}
<!--_-->

    p.print_stats(3)
とすると上位3件の関数のみが表示される．(順序は直前のソートによる．)

    251006 function calls in 4.382 seconds

    Ordered by: call count
    List reduced from 6 to 3 due to restriction <3>

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    250501    4.340    0.000    4.340    0.000 sample.py:1(f1)
       501    0.041    0.000    4.382    0.009 sample.py:7(f2)
         1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
<!--_-->

    p.print_stats(.3, 'sample')
また，上のようにすると，上位30%の関数のみに制限され，かつファイル名，行番号，関数名の一部に文字列'sample'を含む関数のみが表示される．パーセンテージの指定は0.0 - 1.0である．制限の順番を変えることも可能．

    251006 function calls in 4.382 seconds

    Ordered by: call count
    List reduced from 6 to 2 due to restriction <0.3>

    ncalls  tottime  percall  cumtime  percall filename:lineno(function)
    250501    4.340    0.000    4.340    0.000 sample.py:1(f1)
       501    0.041    0.000    4.382    0.009 sample.py:7(f2)

    p.print_callers(.3, 'sample')
このように実行すると，上位30%でありかつファイル名，行番号，関数名の一部に文字列'sample'を含む関数が，どの関数に何回呼び出されたかを調べることができる．

    Ordered by: call count
    List reduced from 6 to 2 due to restriction <0.3>

    Function         was called by...
                      ncalls  tottime  cumtime
    sample.py:1(f1)  <-       1    0.000    0.000  sample.py:1(<module>)
                      250500    4.340    4.340  sample.py:7(f2)
    sample.py:7(f2)  <-       1    0.000    0.009  sample.py:1(<module>)
                         500    0.041    4.373  sample.py:13(f3)

# 参考文献
* [27.4. Python プロファイラ — Python 3.5.1 ドキュメント](http://docs.python.jp/3/library/profile.html)
