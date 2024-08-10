def calculate_average_min_max(a):
    n = len(a)
    averages = []

    for i in range(n):
        maxima_sum = 0
        minima_sum = 0
        maxima_count = 0
        minima_count = 0

        # Calculate maxima
        j = 0
        while j < len(a[i]):
            k = j + 2
            maxima_sum += a[i][j]
            maxima_count += 1
            while k < len(a[i]):
                if abs(a[i][j] - a[i][k]) <= 30:
                    maxima_sum += a[i][k]
                    maxima_count += 1
                    j = k
                    k += 2
                else:
                    k += 2
            j += 2

        # Calculate minima
        d = 1
        while d < len(a[i]):
            m = d + 2
            minima_sum += a[i][d]
            minima_count += 1
            while m < len(a[i]):
                if abs(a[i][d] - a[i][m]) <= 30:
                    minima_sum += a[i][m]
                    minima_count += 1
                    d = m
                    m += 2
                else:
                    m += 2
            d += 2

        average_element = [maxima_sum / maxima_count, minima_sum / minima_count]
        averages.append(average_element)

    # Calculate the overall average maxima and minima
    average_maxima = sum([avg[0] for avg in averages]) / n
    average_minima = sum([avg[1] for avg in averages]) / n

    return [[average_minima, average_maxima]]

# Example usage
a = [[173, 167, 163, 172, 168, 178, 176, 179, 177, 178, 150, 154, 149, 150, 148, 32, 33, 32, 33, 32, 172, 179, 34, 33, 177, 172, 179, 35, 36, 178, 175, 176, 32, 34, 177, 179, 30, 130]]
print(calculate_average_min_max(a))
