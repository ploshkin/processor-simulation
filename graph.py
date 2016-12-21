import matplotlib.pyplot as plt
from os.path import join, curdir, isdir
from os import mkdir


def graph_std_vs_n_proc(x, y, labels, distribution):
    colors = ['r', 'g', 'b']

    if len(x) != len(y):
        print('Error')
        return None
    else:
        n_samples = len(x)

    for i in range(n_samples):
        if len(x[i]) != len(y[i]):
            print('Error')
            return None
        else:
            if labels[i]:
                label = 'With priorities'
            else:
                label = 'Without priorities'
            plt.plot(x[i], y[i], color=colors[i], label=label, linewidth=2.0, alpha=0.5)

    plt.ylim([0, 10])
    plt.xlim([0, 21])

    plt.title('Relation with number of processes')

    plt.xlabel('number of processes')
    plt.ylabel('mean standard deviation of queue length')
    plt.grid()
    plt.legend(loc='upper right')

    plt.tight_layout()

    if not isdir(join(curdir, 'results')):
        mkdir(join(curdir, 'results'))

    plt.savefig(join(curdir, 'results', 'std_vs_n_{}.png'.format(distribution)), fmt='png')

    return None
