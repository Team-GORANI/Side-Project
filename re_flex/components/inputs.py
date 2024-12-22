import reflex as rx
from styles.components import ComponentStyles
from styles.colors import Colors

class RadioInput:
    @staticmethod
    def create(radio_value: str) -> rx.Component:
        return rx.el.input(
            class_name="form-radio",
            type="radio",
            name="object",
            value=radio_value,
            **ComponentStyles.RADIO_INPUT
        )

class Label:
    @staticmethod
    def create_span(content: str) -> rx.Component:
        return rx.text.span(content, color=Colors.TEXT["primary"])

    @staticmethod
    def create_radio_label(radio_value: str, label_text: str) -> rx.Component:
        return rx.el.label(
            RadioInput.create(radio_value=radio_value),
            Label.create_span(content=label_text),
            display="flex",
            align_items="center",
            column_gap=Spacing.GAP["sm"]
        )

    @staticmethod
    def create_upload_button() -> rx.Component:
        return rx.el.label(
            " Upload Image ",
            **ComponentStyles.UPLOAD_BUTTON
        )
