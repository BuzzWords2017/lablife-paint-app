# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line


class MyPaintWidget(Widget):

	def on_touch_down(self, touch):
		with self.canvas:
			Color(1, 1, 1)
			touch.ud['line'] = Line(points=(touch.x, touch.y))

	def on_touch_move(self, touch):
		touch.ud['line'].points += [touch.x, touch.y]

class MyPaintLayout(BoxLayout):
	def __init__(self, **kwargs):
		super(MyPaintLayout, self).__init__(**kwargs)

		# 全消去用のモーダルウィンドウ
		self.clear_modal_view = Factory.ClearModal()
		modal_layout = BoxLayout(orientation='vertical')
		modal_layout.add_widget(Label(text='Do you really want to clear?'))
		modal_layout.add_widget(Button(
			text='Yes', 
			on_press=lambda button: [self.ids.paint.canvas.clear(), self.clear_modal_view.dismiss()]
		))
		modal_layout.add_widget(Button(
			text='No', 
			on_press=lambda button: self.clear_modal_view.dismiss()
		))
		self.clear_modal_view.add_widget(modal_layout)

class ClearModal(ModalView):
	pass

class lablifepaintApp(App):
	pass

if __name__ == '__main__':
	lablifepaintApp().run()
