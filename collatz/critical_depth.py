import matplotlib.pyplot as plt


def get_b_n(n, m, b_0):
    numerator_1 = 3**n * b_0
    numerator_2 = sum([(3**(n-i) * 2**(i*(1+m)-1)) for i in range(1, n+1)]) # the range is actually 1 to n
    denominator = (2**(n*(1+m)))
    b_n = (numerator_1 + numerator_2) / denominator
    return b_n


if __name__ == "__main__":
    n = range(1, 500)
    m = 0.6
    b_0 = 100.0
    b_n_values = [get_b_n(i, m, b_0) for i in n]
    # plotting the values
    plt.plot(n, b_n_values, marker='o')
    plt.title(f'b value in critical trajectory for m={m}, b_0={b_0}')
    plt.xlabel('n')
    plt.ylabel('b_n')
    plt.grid()
    # save the plot
    plt.savefig('critical_depth_plot.png')
