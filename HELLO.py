"""
言葉を覚えるプログラム、"こんにちは"だったら、馬鹿っていう

"""

a = input("言葉を教えてね")
word_list=[]
def reply_func(input_word):
    if input_word not in word_list:
        word_list.append(input_word)
        if a == "こんにちは":
            reply_message = "馬鹿！"
        else:
            reply_message = input_word + "だね！" +" "+ "知らなかった、ありがとう"

    else:
        reply_message = "さっき聞いたよ！"
    return reply_message
reply_func(a)
