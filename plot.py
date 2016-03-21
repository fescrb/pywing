from matplotlib import pyplot

def plot_chances(title, xlabel, **chances_label_pairs):
	if len(chances_label_pairs) > 14:
		print("Too many plots.")
		return
	x_axis = [0, 1, 2, 3, 4, 5, 6, 7]
	colours = ["k", "r", "b", "g", "c", "m", "y"] 
	colour_index = 0
	handle_list = []
	highest_number_with_nonzero_prob = 0
	for l,c in chances_label_pairs.iteritems():
		for i in range(len(c)):
			if (c[i] > 0.0) and (i > highest_number_with_nonzero_prob):
				highest_number_with_nonzero_prob = i
		this_handle, = pyplot.plot(x_axis, c, colours[colour_index], label=l)
		colour_index = colour_index+1
		handle_list.append(this_handle)
	pyplot.legend(handles=handle_list)
	pyplot.axis([0, highest_number_with_nonzero_prob, 0, 1])
	pyplot.xlabel(xlabel)
	pyplot.ylabel('Probability')
	pyplot.title(title)
	pyplot.show()