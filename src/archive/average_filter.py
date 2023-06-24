import random
import time


num_of_sample = 0
prev_average = 0.0

# 3
# [4,4,4]
# avg = 4
# 

def avgFilterForRecursive(x:float):

    global num_of_sample, prev_average

    average, alpha = 0.0, 0.0

    # 샘플 수 +1 (+1 the number of sample)
    num_of_sample += 1

    # 평균 필터의 alpha 값 (alpha of average filter)
    # 현단계의 샘플 수 비례 이전 샘플 수의 비율을 알파라 정의
    alpha = (num_of_sample - 1) / num_of_sample

    # 평균 필터의 재귀식 (recursive expression of average filter)
    # 알파 비율을 이용해 이전 평균이 갖는 평균값의 비율과 현재 제시된 값이 차지할 비율로 계산된 값을 더해서 평균구함 (전체 100%)
    # 총합은 1(100%)
    average = (alpha * prev_average) + ((1 - alpha) * x)

    # 평균 필터의 이전 상태값 업데이트 (update previous state value of average filter)
    prev_average = average

    return average


total_val = 0.0

def avgFilterForBatch(x:float):

    global num_of_sample, total_val

    num_of_sample += 1
    total_val += x

    return total_val / num_of_sample


def movingAvgFilterForBatch(samples:list, x:float, n:int):

    # if len(samples) < n:
    #     return 0

    if len(samples) >= n:
        samples.pop(0)
    
    samples.append(x)

    return sum(samples) / len(samples)


def movingAvgFilterForRecursive(x:float, pre_x:float, n:int):

    global prev_average

    avg = prev_average + ((x - pre_x) / n)
    prev_average = avg

    return avg



while True:
    randVal = random.randrange(100,200) * 0.01
    # print(f'val: {randVal:0.2f}, avg: {avgFilterForRecursive(randVal):0.2f}')
    print(f'val: {randVal:0.2f}, avg: {avgFilterForBatch(randVal):0.2f}')
    time.sleep(0.5)
