"""
Original author is : Prx001
Git Repo : https://github.com/Prx001/QRoundProgressbar

This code is copied and modified for this application use.
"""

from PyQt5 import QtCore, QtGui, Qt, QtWidgets
import sys

from PyQt5.QtCore import Qt, pyqtSlot, pyqtProperty, pyqtSignal
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush  


class RoundProgressbar(QWidget):

	def __init__(
			self,
			parent=None,
			color: QColor = QColor(255, 255, 255),
			size: int = 100,
			thickness: int = 10,
			value: int = 24,
			maximum: int = 100,
			round_edge: bool = False,
			bg_circle_color: QColor = QColor(0, 0, 0, 0),
			fill_bg_circle: bool = False
	):
		if parent is not None:
			super().__init__(parent=parent)
		elif parent is None:
			super().__init__()
		self._circular_size = size
		self._thickness = thickness
		self.resize(self._circular_size + (self._thickness * 2), self._circular_size + (self._thickness * 2))
		self._color = color
		self._maximum = maximum
		self._value = value
		self._alen = (self._value / self._maximum) * 360
		self._a = -(self._alen - 90)
		self._round_edge = round_edge
		self._bg_circle_color = bg_circle_color
		self._fill_bg_circle = fill_bg_circle

	def paintEvent(self, paint_event):
		painter = QPainter()
		painter.begin(self)
		painter.setRenderHint(QPainter.Antialiasing)

		# Draw white outline around the progress bar first
		outline_thickness = 2  # thickness of the outline
		painter.setPen(QPen(Qt.white, outline_thickness))
		painter.setBrush(Qt.NoBrush)
		painter.drawEllipse(self._thickness - outline_thickness // 2, 
							self._thickness - outline_thickness // 2, 
							self._circular_size + outline_thickness, 
							self._circular_size + outline_thickness)

		# Continue with the original background circle drawing
		painter.setPen(QPen(self._bg_circle_color, self._thickness - 1, Qt.SolidLine))
		if self._fill_bg_circle:
			painter.setBrush(QBrush(self._bg_circle_color, Qt.SolidPattern))
		else:
			painter.setBrush(Qt.NoBrush)
		painter.drawEllipse(self._thickness, self._thickness, self._circular_size, self._circular_size)

		# Drawing the progress arc
		if self._round_edge:
			painter.setPen(QPen(self._color, self._thickness, Qt.SolidLine, Qt.RoundCap))
		else:
			painter.setPen(QPen(self._color, self._thickness, Qt.SolidLine, Qt.FlatCap))
		painter.setBrush(Qt.NoBrush)
		rect = QtCore.QRect(self._thickness, self._thickness, self._circular_size, self._circular_size)
		painter.drawArc(rect, int(self._a * 16), int(self._alen * 16))

		# Render the progress number
		font_size = int(self._thickness)
		font = painter.font()
		font.setPointSize(font_size)
		painter.setFont(font)
		painter.setPen(self._color)
		rect = QtCore.QRect(self._thickness, self._thickness, self._circular_size, self._circular_size)
		painter.drawText(rect, QtCore.Qt.AlignCenter, str(self._value) + "%")
		painter.end()

	def resizeEvent(self, event):
		super().resizeEvent(event)
		self._circular_size = (self.width() - (self._thickness * 2)) if self.width() < self.height() else (
				self.height() - (self._thickness * 2))

	def get_value(self):
		return self._value

	@pyqtSlot(int)
	def set_value(self, value: int):
		self._value = value
		self._alen = (self._value / self._maximum) * 360
		self._a = -(self._alen - 90)
		self.update()

	value = pyqtProperty(int, get_value, set_value)

	def get_maximum(self):
		return self._maximum

	@pyqtSlot(int)
	def set_maximum(self, value: int):
		self._maximum = value
		self._alen = (self._value / self._maximum) * 360
		self._a = -(self._alen - 90)
		self.update()

	maximum = pyqtProperty(int, get_maximum, set_maximum)

	def get_thickness(self):
		return self._thickness

	@pyqtSlot(int)
	def set_thickness(self, value: int):
		self._thickness = value
		self._circular_size = (self.width() - (self._thickness * 2)) if self.width() < self.height() else (
				self.height() - (self._thickness * 2))
		self.update()

	thickness = pyqtProperty(int, get_thickness, set_thickness)

	def get_color(self):
		return self._color

	@pyqtSlot(QColor)
	def set_color(self, color: QColor):
		self._color = color
		self.update()

	color = pyqtProperty(QColor, get_color, set_color)

	def get_bg_circle_color(self):
		return self._bg_circle_color

	@pyqtSlot(QColor)
	def set_bg_circle_color(self, color: QColor):
		self._bg_circle_color = color
		self.update()

	background_circle_color = pyqtProperty(QColor, get_bg_circle_color, set_bg_circle_color)

	def get_round_edge(self):
		return self._round_edge

	@pyqtSlot(bool)
	def set_round_edge(self, value: bool):
		self._round_edge = value
		self.update()

	round_edge = pyqtProperty(bool, get_round_edge, set_round_edge)

	def get_fill_bg_circle(self):
		return self._fill_bg_circle

	@pyqtSlot(bool)
	def set_fill_bg_circle(self, value: bool):
		self._fill_bg_circle = value
		self.update()
	
	fill_background_circle = pyqtProperty(bool, get_fill_bg_circle, set_fill_bg_circle)

           

if __name__ == "__main__":
	app = QtWidgets.QApplication(sys.argv)
	dlg = RoundProgressbar()
	dlg.set_value(75)
	dlg.show()
	sys.exit(app.exec_())