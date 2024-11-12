Это старый код, который можно рефакторить с учётом классов из `custom`,
например:

1. 0-intro.py: функционал, связанный с `shapes_to_background`, реализован
в классе `custom.background.simple_shapes.BGSimpleShapes`



# Примечание
Чтобы использовать особый шрифт, нужно установить его в систему или временно
зарегистрировать его, указав путь

```python
with register_font(font_path):
    txt = Text('Удачи!', font=font_name)
    # ...
```