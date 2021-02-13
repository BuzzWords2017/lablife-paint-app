# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.clock import Clock, ClockEvent
from kivy.uix.actionbar import ActionBar, ActionButton, ActionDropDown, ActionPrevious, ActionView, ActionLabel
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line

class ActionPenPreview(ActionLabel):
	def __init__(self, **kwargs):
		super(ActionPenPreview, self).__init__(**kwargs)

		# TODO: もっと正しく初期のプレビューを配置する方法があれば差し替える
		Clock.schedule_once(lambda _: self.update_current_pen(), 2)

	def update_current_pen(self, r=1, g=1, b=1, w=1):
		self.canvas.clear()
		with self.canvas:
			Color(r, g, b)
			Line(points=((self.x+self.width/10), self.center_y, (self.right-self.width/10), self.center_y), 
				width=w, cap='round', joint='round')

class PenPreview(Label):
	def __init__(self, **kwargs):
		super(PenPreview, self).__init__(**kwargs)

	def update_current_pen(self, r=1, g=1, b=1, w=1):
		self.canvas.clear()
		with self.canvas:
			Color(r, g, b)
			Line(points=((self.x+self.width/10), self.center_y, (self.right-self.width/10), self.center_y), 
				width=w, cap='round', joint='round')


class MyPaintWidget(Widget):
	def __init__(self, **kwargs):
		super(MyPaintWidget, self).__init__(**kwargs)

		self.current_width = 1

		# 戻る・やり直しボタン用
		self.back_redo_log = []

		self.red = 1
		self.green = 1
		self.blue = 1


	def on_touch_down(self, touch):
		with self.canvas:
			Color(self.red, self.green, self.blue)
			touch.ud['line'] = Line(points=(touch.x, touch.y), 
				width=self.current_width, cap='round', joint='round')

		# 戻るボタンのログをリセット
		if len(self.back_redo_log) > 0:
			self.back_redo_log.clear()

	def on_touch_move(self, touch):
		try:
			touch.ud['line'].points += [touch.x, touch.y]
		except KeyError:
			pass

	def set_current_width(self, width):
		self.current_width = width
	
	def back_action(self):
		if len(self.canvas.children) >= 3:
			self.back_redo_log.append(self.canvas.children.pop(-3))
			self.back_redo_log.append(self.canvas.children.pop(-2))
			self.back_redo_log.append(self.canvas.children.pop(-1))

	def redo_action(self):
		if len(self.back_redo_log) >= 3:
			self.canvas.children.append(self.back_redo_log.pop(-3))
			self.canvas.children.append(self.back_redo_log.pop(-2))
			self.canvas.children.append(self.back_redo_log.pop(-1))


class PenWidthDropDown(ActionDropDown):
	pass

class MyPaintLayout(BoxLayout):
	def __init__(self, **kwargs):
		super(MyPaintLayout, self).__init__(**kwargs)

		# 変数・設定
		self.orientation = 'vertical'
		self.pen_width_dropdown = PenWidthDropDown()

		# ウィジェットの定義
		self.paint = MyPaintWidget()
		self.action_bar = ActionBar()
		self.action_view = ActionView()
		self.action_previous = ActionPrevious()
		self.pen_preview = ActionPenPreview()

		# 戻る・やり直しボタン
		self.back_action_button = ActionButton(text='Back', on_press=lambda _:
			self.paint.back_action()
		)

		self.redo_action_button = ActionButton(text='Redo', on_press=lambda _:
			self.paint.redo_action()
		)

		# 色の決定用のモーダルウィンドウ
		self.pen_color_modal_view = ModalView(size_hint=(0.8, 0.8))
		self.clr_picker = ColorPicker(size_hint_y=9)
		self.clr_picker.bind(color=lambda _, color: self.change_pen_color(color))
		self.pen_color_modal_layout = BoxLayout(orientation='vertical')
		self.pen_color_modal_layout.add_widget(self.clr_picker)

		self.pen_color_modal_layout.add_widget(Button(
			text='Close', 
			on_press=self.pen_color_modal_view.dismiss, 
			size_hint_y=1
		))
		self.pen_color_modal_view.add_widget(self.pen_color_modal_layout)
		

		# 全消去用のモーダルウィンドウ
		self.clear_modal_view = ModalView(size_hint=(0.7, 0.7))
		self.clear_modal_layout = BoxLayout(orientation='vertical')
		self.clear_modal_layout.add_widget(Label(text='Do you really want to clear?'))
		self.clear_modal_layout.add_widget(Button(
			text='Yes', 
			on_press=lambda button: [self.paint.canvas.clear(), self.paint.back_redo_log.clear(), self.clear_modal_view.dismiss()]
		))
		self.clear_modal_layout.add_widget(Button(
			text='No', 
			on_press=lambda button: self.clear_modal_view.dismiss()
		))
		self.clear_modal_view.add_widget(self.clear_modal_layout)

		# ペンの太さのモーダルウィンドウ
		self.pen_width_modal_view = ModalView(size_hint=(0.7, 0.5))
		self.pen_width_modal_layout = BoxLayout(orientation='vertical')
		self.pen_width_label = Label(text="Width: "+str(int(self.paint.current_width)))
		self.pen_width_slider = Slider(min=1, max=20, value=self.paint.current_width, step=1, 
			on_touch_move=lambda x, y : self.change_pen_width(self.pen_width_slider.value))
		self.pen_width_modal_layout.add_widget(self.pen_width_label)
		self.pen_width_modal_layout.add_widget(self.pen_width_slider)
		self.pen_width_modal_layout.add_widget(Button(
			text='Close', 
			on_press=self.pen_width_modal_view.dismiss
		))
		self.pen_width_modal_view.add_widget(self.pen_width_modal_layout)

		self.pen_color_btn = ActionButton(text='Color', on_press=lambda _: 
			self.pen_color_modal_view.open()
		)

		self.pen_width_btn = ActionButton(text='width: ' + str(int(self.paint.current_width)), on_press=self.pen_width_modal_view.open)
		self.clear_btn = ActionButton(text='Clear', on_press=self.clear_modal_view.open)

		# ウィジェットの配置
		self.action_view.add_widget(self.action_previous)
		self.action_view.add_widget(self.pen_preview)
		self.action_view.add_widget(self.back_action_button)
		self.action_view.add_widget(self.redo_action_button)
		self.action_view.add_widget(self.pen_color_btn)
		self.action_view.add_widget(self.pen_width_btn)
		self.action_view.add_widget(self.clear_btn)
		self.action_bar.add_widget(self.action_view)
		self.add_widget(self.paint)
		self.add_widget(self.action_bar)

	def change_pen_width(self, width):
		self.paint.set_current_width(width)
		self.pen_width_btn.text = "width: " + str(width)
		self.pen_width_label.text = "Width: " + str(width)
		self.pen_preview.update_current_pen(
			self.paint.red, self.paint.green, self.paint.blue, self.paint.current_width
		)


	def change_pen_color(self, color):
		self.paint.red = color[0]
		self.paint.green = color[1]
		self.paint.blue = color[2]
		self.pen_preview.update_current_pen(
			self.paint.red, self.paint.green, self.paint.blue, self.paint.current_width
		)


class lablifepaintApp(App):
	def build(self):

		return MyPaintLayout()


if __name__ == '__main__':
	lablifepaintApp().run()
