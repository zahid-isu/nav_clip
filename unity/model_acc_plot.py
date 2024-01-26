import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('model_accuracies.csv')

sp_relations = df['sp_relation'].unique()
models = df['Model'].unique()
palette = sns.color_palette('husl', n_colors=len(models))

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12, 10), sharey=True)
axes = axes.flatten()

model_to_color = dict(zip(models, palette))
legend_artists = []  # List to hold the legend artists (bars)
legend_labels = []

for i, sp_relation in enumerate(sp_relations):
    sp_relation_df = df[df['sp_relation'] == sp_relation]
    ax = axes[i]
    barplot=sns.barplot(data=sp_relation_df, x='Model', y='Accuracy', hue='Model', ax=ax, palette=palette, width=0.5)

    ax.set_title(f'Spatial relation: {sp_relation.upper()}', fontsize=15, loc='center', y=-0.1)
    ax.set_ylabel('Accuracy', fontsize=15)
    ax.set_xlabel('') 
    ax.tick_params(axis='y', labelsize=15, length=8)
    ax.tick_params(axis='x', length=0, labelbottom=False)
    ax.set_ylim(0, 1.0)

    for bar in barplot.patches:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), f'{bar.get_height():.2f}', 
                ha='center', va='bottom', fontsize=12)

    # Add the artists and labels for the legend
    if not legend_artists:
        for patch in ax.patches:
            legend_artists.append(patch)
            legend_labels.append(patch.get_facecolor())
        legend_labels = [sp_relation_df['Model'].unique()[i] for i in range(len(legend_labels))]

# Create a global legend at the top of the figure with the saved handles
num_models = len(models)
ncols_for_legend = num_models // 2 if num_models % 2 == 0 else (num_models // 2) + 1
fig.legend(legend_artists, legend_labels, loc='upper center', bbox_to_anchor=(0.5, 1.05), ncol=ncols_for_legend, title='Models', fontsize=14, title_fontsize=14)
plt.tight_layout(rect=[0, 0, 1, 0.97]) 
fig.suptitle('Accuracy of VL models by spatial relation', fontsize=18, y=1.1)

fig.savefig('model_accuracies_plot.png', dpi=600, bbox_inches='tight')
plt.show()
