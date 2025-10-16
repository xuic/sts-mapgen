# 殺戮尖塔的地圖生成
根據 reddit 的這兩篇文章 

https://www.reddit.com/r/slaythespire/comments/ndqweh/i_have_reverseengineered_map_generation_algorithm/
https://www.reddit.com/r/slaythespire/comments/1jczl7v/ive_learned_how_the_sts_map_generation_works/

使用 python 粗糙的模擬殺戮尖塔的地圖生成 (之所以粗糙是因為我的實作方式會讓地圖生成左右不平衡)

圖例: M = 普怪, E = 菁英怪, ? = 事件, S = 商店, R = 營火, T = 寶箱

生成範例:
```
   
15  R  R     R  R       
      \|   /    |
14     M  ?     M
         \|   / | \
13        M  M  R  E
          | \  \|    \
12        M  ?  E     ?
          | \  \|     |
11        E  E  S     M
          |    \| \ /
10        S     M  R
        /     / |/ |
09     T     T  T  T
     /       | \| \  \
08  M        M  ?  E  R
    |          \| \  \|
07  R           R  R  M
    |         / |  |/ |
06  M        M  E  M  ?
      \      |  |/ |/
05     ?     M  ?  M
     /       |/  /   \
04  M        M  ?     M
    |      /   \|     |
03  M     ?     ?     M
      \   |   /   \ /
02     M  M  ?     M
     /    |  |       \
01  M     M  M        M
```

```
   
15  R  R  R  R
    |  |/ |    \
14  E  M  M     E
    |/ |/     /
13  R  E     M
    | \|       \
12  ?  M        E
    |/ | \    /
11  M  M  E  M
    |    \  \|
10  M     ?  S
    | \ /    | \
09  T  T     T  T
    |/ |     |    \
08  M  R     M     R
    | \  \     \   |
07  M  R  M     M  M
    | \|  |     |    \
06  ?  M  M     E     R
    |    \  \   |   /
05  ?     M  M  S  ?
    |   / |    \|    \
04  M  M  ?     M     ?
    |  |  |   /   \ /
03  M  ?  ?  ?     M
      \|    \  \ /
02     M     ?  M
     /         \  \
01  M           M  M
```
