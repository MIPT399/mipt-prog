from bokeh.plotting import figure, output_file, show

# output to static HTML file
output_file("game.html")

# create a new plot
p = figure(
   tools="pan,box_zoom,reset,save",
   y_range=[0, 300],
   x_range=[0, 300]
)

# show the results
show(p)