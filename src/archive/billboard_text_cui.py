
import os
import time

def billboardText(text):


    # hello
    # elloh
    # llohe
    # lohel
    # ohell
    # hello

    dst = text

    # 변화추이 확인
    # print(dst)
    # dst = f'{dst[1:]}{dst[0]}'
    # print(dst)
    # dst = f'{dst[1:]}{dst[0]}'
    # print(dst)
    # dst = f'{dst[1:]}{dst[0]}'
    # print(dst)
    # dst = f'{dst[1:]}{dst[0]}'
    # print(dst)
    # dst = f'{dst[1:]}{dst[0]}'
    # print(dst)

    # # 반복문 간소화
    # while True:
    #     os.system('clear')
    #     print(dst)
    #     # dst = f'{dst[1:]}{dst[0]}'
    #     dst = dst[1:] + dst[0]

    #     # 딜레이가 필요
    #     time.sleep(1)

    # 버블정렬
    textLength = len(dst)

    # 문자열을 문자 하나씩 나누어 리스트에 담기 => 'hello' -> ['h','e','l','l','o']
    
    # #1 for문을 이용
    # charList = []
    # for c in dst:
    #     charList.append(c)

    # 2 
    # charList = [c for c in dst]

    # 3 형변환
    charList = list(dst)
    while True:
        os.system('clear')
        # print(charList) # ['h','e','l','l','o']
        print(''.join(charList)) # 'hello'

        # ['h','e','l','l','o']
        # 1회전하면 결과는 가장앞 0번 인덱스의 문자가 가장뒤로 이동하게되고
        # 1번 인덱스부터 끝까지의 문자들은 앞으로 한칸씩 당겨짐
        for i in range(0, textLength-1):
            v1 = charList[i] #v1 = 'h'
            v2 = charList[i+1] #v2 = 'e'

            charList[i] = v2
            charList[i+1] = v1

        # 딜레이가 필요
        time.sleep(1)
        pass

        
    
if __name__ == '__main__':

    billboardText('hello')

    # self.quit()
    # self.wait(5000) #5000ms = 5s

    pass