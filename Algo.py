def main():
    cluster = []
    for i in range(0, 4):
        ele = int(input("enter a number"))
        cluster.append(ele)

    time = [0, 0, 0, 0]
    tmp = 0
    tMax = 64

    for i in range(0, 4):
        curntLevel = cluster[i]
        if (curntLevel == 1):
            t = tMax / 8
            if (curntLevel == 2):
                tmp = tMax / (4 * 2)
            elif(curntLevel == 3):
                tmp = tMax / (2 * 2)
            t = t + tmp
            time[i] = t
        elif(curntLevel == 2):
            t = tMax / 4
            if (curntLevel == 3):
                tmp = tMax / (2 * 2)
            t = t + tmp
            time[i] = t
        elif(curntLevel == 3):
            t = tMax / 2
            time[i] = t

    print(time)

if __name__ == "__main__":
    main()
