# a = [[173, 167, 163, 172, 168, 178, 176, 179, 177, 178, 150, 154, 149, 150, 148, 32, 33, 32, 33, 32, 172, 179, 34, 33, 177, 172, 179, 35, 36, 178, 175, 176, 32, 34, 177, 179, 30, 130]]

# def calculateAverage(a):
#     n = len(a)
#     averages = []

#     for i in range(n):
#         j = 0
#         k = 2

#         d = 1
#         m = 3
#         maxima_sum = a[i][j]
#         minima_sum = a[i][d]
#         maxima_count = 1
#         minima_count = 1
#         while k < len(a[i]):
#             if abs(a[i][j] - a[i][k]) <=30:
#                 maxima_sum += a[i][k]
#                 maxima_count += 1
#                 j = k
#                 k = k + 2
#             else:
#                 k = k + 2
#         while m < len(a[i]):    
#             if abs(a[i][d] - a[i][m]) <=30:
#                 minima_sum += a[i][m]
#                 minima_count += 1
#                 d = m 
#                 m = m + 2
#             else:
#                 m = m + 2
#         average_element = [maxima_sum/maxima_count,minima_sum/minima_count]
#         averages.append(average_element)
#     return averages



def calculateAverage(arr):
    minima_sum = 0
    maxima_sum = 0

    maxima_count = 0
    minima_count = 0

    ard = []
    
    n = len(arr)
    for i in range(0,n):
        for j in arr[i]:
            maximum_angle = max(arr[i])
            minimum_angle = min(arr[i])

            if abs(j - maximum_angle) <= 20:
                maxima_sum += j
                maxima_count += 1
            if abs(j - minimum_angle) <= 20:
                minima_sum += j
                minima_count += 1
        ard.append([maxima_sum/maxima_count, minima_sum/minima_count])
    return ard

# calculateAverage(a)
# b = [[174.75, 33.0]]
# a = [[179, 123, 134, 126, 128, 108, 175, 178, 153, 176, 178, 178, 175, 167, 175, 176, 167, 170, 169, 176, 6, 150, 44, 59, 38, 50, 33, 50, 29, 168, 173, 164, 169, 166, 176, 89, 90, 175, 175, 86, 158, 148, 175, 176, 176, 175, 178, 171], [103, 154, 136, 146, 138, 139, 126, 175, 174, 176, 177, 176, 132, 174, 179, 176, 179, 179, 178, 179, 164, 168, 167, 179, 178, 172, 12, 137, 93, 104, 0, 28, 10, 14, 13, 161, 104, 162, 86, 171, 58, 89, 4, 166, 160, 153, 160, 156, 163, 159, 160, 66, 166, 163, 166, 66, 69, 68, 168, 164, 65, 68, 66, 68, 67, 68, 165, 167, 165, 166, 165, 166, 62, 146, 129, 163, 164, 171, 170, 175, 173, 177, 179]]

# print(calculateAverage(a))