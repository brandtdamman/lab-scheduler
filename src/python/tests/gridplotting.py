from matplotlib import pyplot

# def randrange_float(start, stop, step):
#     return random.randint(0, int((stop - start) / step)) * step + start

# randrange_float(2.1, 4.2, 0.3) # returns 2.4

if __name__=="__main__":
    import random
    # data = [[randrange_float(0, 1, 0.5) for x in range(0,8)], # row 1
    #         [random.randint(a=0,b=1) for x in range(0,8)], # row 2
    #         [random.randint(a=0,b=1) for x in range(0,8)], # row 3
    #         [random.randint(a=0,b=1) for x in range(0,8)], # row 4
    #         [random.randint(a=0,b=1) for x in range(0,8)], # row 5
    #         [random.randint(a=0,b=1) for x in range(0,8)], # row 6
    #         [random.randint(a=0,b=1) for x in range(0,8)], # row 7
    #         [random.randint(a=0,b=1) for x in range(0,8)]] # row 8

    data = [[random.randint(a=0,b=1) for x in range(0,10)], # row 1
            [random.randint(a=0,b=1) for x in range(0,10)], # row 2
            [random.randint(a=0,b=1) for x in range(0,10)], # row 3
            [random.randint(a=0,b=1) for x in range(0,10)], # row 4
            [random.randint(a=0,b=1) for x in range(0,10)], # row 5
            [random.randint(a=0,b=1) for x in range(0,10)], # row 6
            [random.randint(a=0,b=1) for x in range(0,10)], # row 7
            [random.randint(a=0,b=1) for x in range(0,10)], # row 8
            [random.randint(a=0,b=1) for x in range(0,10)],
            [random.randint(a=0,b=1) for x in range(0,10)],
            [random.randint(a=0,b=1) for x in range(0,10)],
            [random.randint(a=0,b=1) for x in range(0,10)],
            [random.randint(a=0,b=1) for x in range(0,10)],
            [random.randint(a=0,b=1) for x in range(0,10)],
            [random.randint(a=0,b=1) for x in range(0,10)],
            [random.randint(a=0,b=1) for x in range(0,10)],
            [random.randint(a=0,b=1) for x in range(0,10)],
            [random.randint(a=0,b=1) for x in range(0,10)],
            [random.randint(a=0,b=1) for x in range(0,10)],
            [random.randint(a=0,b=1) for x in range(0,10)]]

    print(data)

    pyplot.figure(figsize=(7,5))
    pyplot.imshow(data)
    pyplot.show()