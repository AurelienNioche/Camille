import matplotlib.pyplot as plt
import numpy as np

import csv

from scipy.stats import mannwhitneyu
from statsmodels.sandbox.stats.multicomp import multipletests


def csv_import(file_name):

    data = []
    labels = None
    labels_that_matter = []
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        i = 0
        for row in csv_reader:

            if i == 0:
                labels = row
            else:
                f_row = []
                for j, r in enumerate(row):
                    label = labels[j]
                    if "AV" not in label and "AUJ" not in label:
                        continue
                    labels_that_matter.append(label)
                    if r:
                        r = r.replace(",", ".")
                        r = float(r)

                        if "RESSENTI" in labels[j]:
                            r /= 6
                        else:
                            r /= 5
                        f_row.append(r)
                if f_row:
                    data.append(f_row)

            i += 1

    return labels_that_matter, np.asarray(data)


def main():
    labels, data_hp = csv_import(file_name='data/hp.csv')
    labels, data_no_hp = csv_import(file_name='data/no_hp.csv')

    n_measure = data_hp.shape[1]

    p_values = []
    u_values = []

    for i in range(n_measure):

        title=labels[i]

        figure, axes = plt.subplots(nrows=3)

        ax_i = 0

        hp = data_hp[:, i]
        no_hp = data_no_hp[:, i]

        ax = axes[ax_i]
        ax.scatter(np.zeros(len(hp)), hp, color="orange", alpha=0.5)
        ax.scatter(np.ones(len(no_hp)), no_hp, color="blue", alpha=0.5)
        ax.set_ylim(0, 1)
        ax.set_title(title)

        ax.set_xticks((0, 1))
        ax.set_xticklabels(('HP', 'No-HP'))
        ax_i += 1

        ax = axes[ax_i]
        ax.bar(np.arange(2), (np.mean(hp), np.mean(no_hp)), color=("orange", "blue"),
               yerr=(np.std(hp), np.std(no_hp)), tick_label=("HP", "No-HP"))
        ax.set_ylim((0, 1))
        ax_i += 1

        ax = axes[ax_i]
        ax.boxplot([hp, no_hp])
        ax.set_ylim((0, 1))
        ax.set_xticklabels(('HP', 'No-HP'))
        ax_i += 1

        plt.savefig(f"fig/fig_{title}.pdf")
        u, p = mannwhitneyu(hp, no_hp)

        u_values.append(u)
        p_values.append(p)

    sign, p_adjusted, alphacSidak, alphacBonf = multipletests(p_values, method='bonferroni')
    # print(p_adjusted)

    for i in range(n_measure):
        s = sign[i]
        title = labels[i]
        u = u_values[i]
        p_raw = p_values[i]
        p = p_adjusted[i]
        print(title, f'u={u}', f'p_raw={p_raw:.3f}', f'p_corr={p:.3f}', s)


if __name__ == "__main__":
    main()
