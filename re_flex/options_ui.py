import reflex as rx

class State(rx.State):
    """
    - 모든 변수(vars)와 이를 변경하는 함수(func)를 지정하는 역할을 한다.
    -
    """
    # Define var
    object_type: str = ""

	# Define func
    def house_selector(self):
        self.object_type = "house"
    def tree_selector(self):
        self.object_type = "tree"
    def man_selector(self):
        self.object_type = "man"
    def woman_selector(self):
        self.object_type = "woman"


def index():
    return rx.hstack(
        rx.button(
            "집",
            color_scheme="house",
            on_click=State.house_selector,
        ),
        rx.button(
            "나무",
            color_scheme="ruby",
            on_click=State.tree_selector,
        ),
        rx.button(
            "남자",
            color_scheme="man",
            on_click=State.man_selector,
        ),
        rx.button(
            "여자",
            color_scheme="woman",
            on_click=State.woman_selector,
        ),
    )

app = rx.App()
app.add_page(index)