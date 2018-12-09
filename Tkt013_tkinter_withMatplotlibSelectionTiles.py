# ----------------------------------------------------------------
# Adding "from tkinter.ttk import *" after "from tkinter import *"
# to make themed-tk to override tk
# ----------------------------------------------------------------

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk


# import matplotlib.pyplot as plt
# import matplotlib.pylab as plt
import numpy as np


class Tiles:
	def __init__(self, ax, canvas, height, width, margins = 0.5):
		self.ax = ax
		self.canvas = canvas
		self.height, self.width = height, width

		self.setAxTickRange(margins)
		self.fillGrayBG()
		self.customGridOn()

		import matplotlib.patches as patches
		self.rectA = self.ax.add_patch( patches.Rectangle((0,0), 1, 1, facecolor = 'navy', visible = False) )
		self.canvas.mpl_connect('button_press_event', self.on_press)
		# rectA.set_visible(True)
		# rectA.set_xy((1, 2))

	def setAxTickRange(self, margins = 0.5):
		x_range, y_range = range(self.width), range(self.height)
		self.ax.set_xticks(x_range)
		self.ax.set_yticks(y_range)
		self.ax.set_xticklabels(x_range)
		self.ax.set_yticklabels(y_range)
		self.ax.tick_params(axis='both', which = 'major', labelsize = 8)
		self.ax.set_xlim(-.5 - margins, self.width-.5 + margins)
		self.ax.set_ylim(-.5 - margins, self.height-.5 + margins)

	def fillGrayBG(self):
		x_st, x_end = self.ax.get_xlim()
		blackBg = self.ax.axvspan(x_st, x_end, alpha = 0.5, color = 'black')

	def customGridOn(self):
		# DBG : print(xs, ys)
		x = np.arange(-0.5, self.width, 1)
		y = np.arange(-0.5, self.height, 1)
		# grid = cur_ax.grid(which = 'major', axis = 'both', color = 'white', 
		#                    linestyle = 'solid', linewidth = 0.5, alpha = 0.5)
		self.ax.hlines(y, -.5, self.width-0.5, color = 'white', linestyle = '-', linewidth = 0.5, alpha = 0.5)
		self.ax.vlines(x, -.5, self.height-0.5, color = 'white', linestyle = '-', linewidth = 0.5, alpha = 0.5)

	def on_press(self, event):
		if self.ax == event.inaxes:
			self.rectA.set_visible(True)
			x, y = int(event.xdata + 0.5), int(event.ydata + 0.5)
			print(x, y)
			self.rectA.set_xy((x-0.5, y-0.5))
			self.canvas.draw()
			'''
			ax.draw_artist(ax.patch)
			'''






# +---+----+---+--+----+---+-+----+---+-+-+-----+----+
# ===================== 4 Steps ======================
# 1. Import the Tkinter module
# 2. Create the GUI application main window
# 3. Add one or more of the widget into the window
# 4. Enter the main event loop to take action against
#    each event triggered by the user.
# +---+----+---+--+----+---+-+----+---+-+-+-----+----+


class Window(Tk):
	def __init__(self, *args, **kwargs):
		Tk.__init__(self, *args, **kwargs)
		root = self
		root.geometry("500x500+300+50")	# or using "<width>x<height>" only
		root.title('Python tKinter : Prototype Dev. Use')
		self.frameLayout()
	def frameLayout(self):
		self.frame = Frame(self)
		root = self
		frame = self.frame
		
		# self.style.theme_create('shadow', parent = 'default')
		frame.pack(fill = BOTH, expand = True)
		
		note = Notebook(frame, takefocus = False)

		def TabWithMatplotlibEmbedded(note):
			tabContent = Frame(note, takefocus = False)

			pane = Panedwindow(tabContent, orient = HORIZONTAL)
			lf1 = Labelframe(pane, text = 'This is a demo Labelframe', width = 100, height = 100)
			pane.add(lf1)
			pane.grid(row = 0, column = 2, columnspan = 3, rowspan = 3)

			fig = Figure(figsize=(5,4), dpi = 100)
			ax = fig.add_subplot(111)
			# x = 10 * np.random.randn(3, 5)
			# ax.imshow(x, interpolation = 'nearest')
			# >> Take Figure & select root 
			canvas = FigureCanvasTkAgg(fig, lf1)
			canvas.show()
			canvas.get_tk_widget().pack(side = BOTTOM, fill = BOTH, expand = True)

			self.tiles = Tiles( ax, canvas, 5, 5 )

			return tabContent

		# >> Add Frame(s) to notebook
		tab = TabWithMatplotlibEmbedded(note)
		note.add( tab, text = "This is a demo tab", sticky = N+E+W+S)

		# >> Select page
		note.select(tab)

		# >> Position the notebook
		# note.place(x = 0, y = 0)
		note.pack(expand = True, fill = BOTH)

def main():
	app = Window()
	app.mainloop()

main()