# Примечание
Это старый код, который можно рефакторить с учётом классов из `custom`.
Например, для `0-intro.py` и `5-converge_to_any_number.py` функционал,
связанный с `shapes_to_background`, реализован в общем виде в 
в классе `custom.background.simple_shapes.BGSimpleShapes`. Однако используется
локально определённая функция `auxfuncs.shapes_to_background`


# Об использовании шрифтов
Чтобы использовать особый шрифт, нужно установить его в систему или временно
зарегистрировать его, указав путь

```python
with register_font(font_path):
    txt = Text('Удачи!', font=font_name)
    # ...
```