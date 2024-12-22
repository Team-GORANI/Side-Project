import reflex as rx
from styles.components import ComponentStyles
from styles.typography import Typography
from styles.spacing import Spacing
from .forms import ObjectSelectionForm
from .sections import DetectedObjectsSection

class ObjectDetectionContainer:
    @staticmethod
    def create() -> rx.Component:
        return rx.box(
            rx.heading(
                "Object Detection",
                margin_bottom=Spacing.MARGIN["lg"],
                text_align="center",
                **Typography.HEADING["h1"],
                as_="h1"
            ),
            ObjectSelectionForm.create(),
            DetectedObjectsSection.create(),
            **ComponentStyles.CONTAINER
        )
