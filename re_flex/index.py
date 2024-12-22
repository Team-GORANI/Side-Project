import reflex as rx
from components.containers import ObjectDetectionContainer
from styles.colors import Colors

def index() -> rx.Component:
    return rx.fragment(
        rx.box(
            rx.flex(
                ObjectDetectionContainer.create(),
                background_color=Colors.BACKGROUND,
                display="flex",
                flex_direction="column",
                align_items="center",
                justify_content="center",
                min_height="100vh"
            )
        )
    )
