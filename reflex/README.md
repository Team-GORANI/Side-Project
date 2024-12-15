- Reference File tree structure : [Source Code](https://github.com/reflex-dev/templates/tree/main/ai_image_gen)
- Read more : [Reflex Docs](https://reflex.dev/docs/getting-started/introduction)
```
📦ai_image_gen
 ┣ 📂backend
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜generation.py
 ┃ ┗ 📜options.py
 ┣ 📂components
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜options_ui.py
 ┃ ┣ 📜prompt_list.py
 ┃ ┣ 📜react_zoom.py
 ┃ ┗ 📜styles_preset.py
 ┣ 📂pages
 ┃ ┣ 📜__init__.py
 ┃ ┗ 📜index.py
 ┣ 📂views # Visual UI
 ┃ ┣ 📜__init__.py
 ┃ ┣ 📜mobile_ui.py
 ┃ ┗ 📜sidebar.py
 ┣ 📜__init__.py
 ┣ 📜ai_image_gen.py # Main script file
 ┣ 📜rxconfig.py
 ┗ 📜styles.py #
 ```


### To-do list
- Button : Select from 'tree, house, human'
- Upload : Image upload
- rx.image : Sample image file
- Layout : Ratio of image files and blocks (ex. Button, Upload, rx.image)
- Image drawing은 구현하는 기능이 아직 없음. -> Only image upload