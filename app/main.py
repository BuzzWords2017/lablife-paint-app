# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.actionbar import ActionBar, ActionButton, ActionDropDown, ActionPrevious, ActionView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line


class MyPaintWidget(Widget):
	def __init__(self, **kwargs):
		super(MyPaintWidget, self).__init__(**kwargs)

		self.current_width = 1

		self.red = 255
		self.green = 255
		self.blue = 255


	def on_touch_down(self, touch):
		with self.canvas:
			Color(self.red / 255, self.green / 255, self.blue / 255)
			touch.ud['line'] = Line(points=(touch.x, touch.y), 
				width=self.current_width, cap='round', joint='round')

	def on_touch_move(self, touch):
		try:
			touch.ud['line'].points += [touch.x, touch.y]
		except KeyError:
			pass

	def set_current_width(self, width):
		self.current_width = width

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
		self.action_previous = ActionPrevious(title='Current Color')

		# 色の決定用のモーダルウィンドウ
		self.pen_color_modal_view = ModalView(size_hint=(0.8, 0.8))
		self.pen_color_modal_layout = BoxLayout(orientation='vertical')
		self.current_color_label = Label(text='Current Color')
		self.r_label = Label(text="Red: "+str(self.paint.red))
		self.g_label = Label(text="Green: "+str(self.paint.green))
		self.b_label = Label(text="Blue: "+str(self.paint.blue))
		self.r_slider = Slider(min=0, max=255, value=self.paint.red, step=1, 
			on_touch_move=lambda x, y : self.change_pen_color_slider('red', self.r_slider.value))
		self.g_slider = Slider(min=0, max=255, value=self.paint.green, step=1, 
			on_touch_move=lambda x, y : self.change_pen_color_slider('green', self.g_slider.value))
		self.b_slider = Slider(min=0, max=255, value=self.paint.blue, step=1, 
			on_touch_move=lambda x, y : self.change_pen_color_slider('blue', self.b_slider.value))

		self.pen_color_modal_layout.add_widget(self.current_color_label)
		self.pen_color_modal_layout.add_widget(self.r_label)
		self.pen_color_modal_layout.add_widget(self.r_slider)
		self.pen_color_modal_layout.add_widget(self.g_label)
		self.pen_color_modal_layout.add_widget(self.g_slider)
		self.pen_color_modal_layout.add_widget(self.b_label)
		self.pen_color_modal_layout.add_widget(self.b_slider)
		self.pen_color_modal_layout.add_widget(Button(
			text='Close', 
			on_press=self.pen_color_modal_view.dismiss
		))
		self.pen_color_modal_view.add_widget(self.pen_color_modal_layout)

		# 全消去用のモーダルウィンドウ
		self.clear_modal_view = ModalView(size_hint=(0.7, 0.7))
		self.clear_modal_layout = BoxLayout(orientation='vertical')
		self.clear_modal_layout.add_widget(Label(text='Do you really want to clear?'))
		self.clear_modal_layout.add_widget(Button(
			text='Yes', 
			on_press=lambda button: [self.paint.canvas.clear(), self.clear_modal_view.dismiss()]
		))
		self.clear_modal_layout.add_widget(Button(
			text='No', 
			on_press=lambda button: self.clear_modal_view.dismiss()
		))
		self.clear_modal_view.add_widget(self.clear_modal_layout)

		self.pen_color_btn = ActionButton(text='Color', on_press=self.pen_color_modal_view.open)
		self.pen_width_btn = ActionButton(text='width: ' + str(self.paint.current_width))
		self.clear_btn = ActionButton(text='Clear', on_press=self.clear_modal_view.open)

		# サイズ決定用のActionDropDown
		self.pen_width_dropdown = ActionDropDown()

		self.pen_width_btn_1 = ActionButton(text="1", size_hint_y=None, 
			on_press=lambda button: self.change_pen_width(1))
		self.pen_width_dropdown.add_widget(self.pen_width_btn_1)

		self.pen_width_btn_2 = ActionButton(text="2", size_hint_y=None, 
			on_press=lambda button: self.change_pen_width(2))
		self.pen_width_dropdown.add_widget(self.pen_width_btn_2)

		self.pen_width_btn_3 = ActionButton(text="3", size_hint_y=None, 
			on_press=lambda button: self.change_pen_width(3))
		self.pen_width_dropdown.add_widget(self.pen_width_btn_3)

		self.pen_width_btn_4 = ActionButton(text="4", size_hint_y=None, 
			on_press=lambda button: self.change_pen_width(4))
		self.pen_width_dropdown.add_widget(self.pen_width_btn_4)

		self.pen_width_btn_5 = ActionButton(text="5", size_hint_y=None, 
			on_press=lambda button: self.change_pen_width(5))
		self.pen_width_dropdown.add_widget(self.pen_width_btn_5)

		self.pen_width_btn_6 = ActionButton(text="6", size_hint_y=None, 
			on_press=lambda button: self.change_pen_width(6))
		self.pen_width_dropdown.add_widget(self.pen_width_btn_6)

		self.pen_width_btn_7 = ActionButton(text="7", size_hint_y=None, 
			on_press=lambda button: self.change_pen_width(7))
		self.pen_width_dropdown.add_widget(self.pen_width_btn_7)

		self.pen_width_btn_8 = ActionButton(text="8", size_hint_y=None, 
			on_press=lambda button: self.change_pen_width(8))
		self.pen_width_dropdown.add_widget(self.pen_width_btn_8)

		self.pen_width_btn_9 = ActionButton(text="9", size_hint_y=None, 
			on_press=lambda button: self.change_pen_width(9))
		self.pen_width_dropdown.add_widget(self.pen_width_btn_9)

		self.pen_width_btn_10 = ActionButton(text="10", size_hint_y=None, 
			on_press=lambda button: self.change_pen_width(10))
		self.pen_width_dropdown.add_widget(self.pen_width_btn_10)

		self.pen_width_btn.bind(on_press=self.pen_width_dropdown.open)

		# ウィジェットの配置
		self.action_view.add_widget(self.action_previous)
		self.action_view.add_widget(self.pen_color_btn)
		self.action_view.add_widget(self.pen_width_btn)
		self.action_view.add_widget(self.clear_btn)
		self.action_bar.add_widget(self.action_view)
		self.add_widget(self.paint)
		self.add_widget(self.action_bar)

	def change_pen_width(self, width):
		self.paint.set_current_width(width)
		self.pen_width_btn.text = "width: " + str(width)
		self.pen_width_dropdown.dismiss()
	
	def change_pen_color_slider(self, color:str, num:int):
		if color=='red':
			self.paint.red = num
			self.r_label.text = "Red: "+str(self.paint.red)
		elif color=='green':
			self.paint.green = num
			self.g_label.text = "Green: "+str(self.paint.green)
		elif color=='blue':
			self.paint.blue = num
			self.b_label.text = "Blue: "+str(self.paint.blue)

		self.action_previous.color=(
			self.paint.red/255,
			self.paint.green/255,
			self.paint.blue/255,
		)

		self.current_color_label.color=(
			self.paint.red/255,
			self.paint.green/255,
			self.paint.blue/255,
		)


class lablifepaintApp(App):
	def build(self):

		return MyPaintLayout()


if __name__ == '__main__':
	lablifepaintApp().run()
