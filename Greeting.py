"""
GreetingBot完成
"""
#Greetingのbot作成

def greeting(strings):
    greet_list = ["こんにちは","こんばんは","こんばんわ","きょうはいいお日和ですね"]
    if strings in greet_list:
        print(strings)
    elif strings == "おはようございます":
        print(greet_list[3])
    else:
        if not strings in  greet_list:
            for str1 in greet_list:
                if str1 in input_word:
                    print(str1)
                    break
            else: #このelseはfor文に当てはまらなかったら、表示するものです。
                print("それは挨拶じゃないよ( ；´Д｀)")

#if __name__ == '__main()__':
input_word = input("挨拶してほしいな！")

greeting(input_word)
