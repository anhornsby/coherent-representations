# -*- coding: utf-8 -*-
# !/usr/bin/env python
# Adam Hornsby

import pandas as pd
import seaborn as sns

import matplotlib
matplotlib.use('Agg')
import matplotlib.pylab as plt

from matplotlib import rcParams

if __name__ == '__main__':

	effect_sizes = {
		'Democrats':

			{'All': 0.518, 
			 'Trade': 0.579, 
			 'Abortion': 0.512,
			'Immigration': 0.558
			},

		'Republicans': 

			{'All': 0.629,
			 'Trade': 0.699,
			 'Abortion': 0.593, 
			 'Immigration': 0.610}
	}

	# sns.set(rc={'figure.figsize':(4, 3)})
	# sns.set_style('ticks')
	# sns.set_context(rc={"font.size":7, "lines.linewidth":2})

	# cast to a dataframe
	effect_sizes = pd.DataFrame(effect_sizes)
	melted_es = pd.melt(effect_sizes.reset_index(), id_vars='index')

	# sns.set(rc={})
	
	sns.set_style('white')
	sns.set_context(rc={"font.size":8})
	# sns.set(rc={"font.size":7, "lines.linewidth":2, 'figure.figsize':(4, 2)})

	rcParams['figure.figsize'] = 4,1.5
	
	# sns.set_context(})

	g = sns.barplot(x=melted_es['index'], 
	            y=melted_es['value'], 
	            hue=melted_es['variable'],
	            palette=["#232066", "#E91D0E"],
	            linewidth=2,
	            saturation=0.6,
	            hue_order=['Democrats', 'Republicans'],
	            order=['All', 'Trade', 'Immigration', 'Abortion'],
	            )


	g.set_xticklabels(g.get_xticklabels(), rotation=0)

	plt.ylim([0.5, 0.9])
	sns.despine(left=True, bottom=True, right=True)
	plt.xlabel('');
	plt.ylabel('Effect size (abs)')
	plt.legend(ncol=1, fontsize=8, frameon=False, loc='upper center');

	# save it
	plt.savefig('plots/effect_size_plot.eps', 
		format='eps', 
		dpi=1000, 
		bbox_inches='tight')

