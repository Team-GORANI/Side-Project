import reflex as rx




class UploadExample(rx.State):
    uploading: bool = False
    progress: int = 0
    total_bytes: int = 0

    @rx.event
    async def handle_upload(
        self, files: list[rx.UploadFile]
    ):
        # File Upload
        for file in files:
            self.total_bytes += len(await file.read())

    @rx.event
    def handle_upload_progress(self, progress: dict):
        self.uploading = True
        self.progress = round(progress["progress"] * 100)
        if self.progress >= 100:
            self.uploading = False

    @rx.event
    def cancel_upload(self):
        self.uploading = False
        return rx.cancel_upload("upload3")

class State(rx.State):
    """The app state."""

    # The images to show.
    img: list[str]

    @rx.event
    async def handle_upload(
        self, files: list[rx.UploadFile]
    ):
        """Handle the upload of file(s).

        Args:
            files: The uploaded files.
        """
        for file in files:
            upload_data = await file.read()
            outfile = rx.get_upload_dir() / file.filename

            # Save the file.
            with outfile.open("wb") as file_object:
                file_object.write(upload_data)

            # Update the img var.
            self.img.append(file.filename)


color = "rgb(107,99,246)" # Color palette


def index():
    """The main view
    - Define all layouts in the apps
    -
    """
    return rx.vstack(
        rx.upload(
            rx.vstack(
                rx.button(
                    "Select File",
                    color=color,
                    bg="white",
                    border=f"1px solid {color}",
                ),
                rx.text(
                    "Drag and drop files here or click to select files"
                ),
            ),
            id="upload1",
            border=f"1px dotted {color}",
            padding="5em",
        ),
        rx.hstack(
            rx.foreach(
                rx.selected_files("upload1"), rx.text
            )
        ),
        rx.button(
            "Upload",
            on_click=State.handle_upload(
                rx.upload_files(upload_id="upload1")
            ),
        ),
        rx.button(
            "Clear",
            on_click=rx.clear_selected_files("upload1"),
        ),
        rx.foreach(
            State.img,
            lambda img: rx.image(
                src=rx.get_upload_url(img)
            ),
        ),
        padding="5em",
    )

##### DIVIDE LINE #####

class Output_Selecter(rx.State):
    object: str = ''

    @rx.event
    def tree_select(self):
        self.object = 'tree'

    @rx.event
    def house_select(self):
        self.object = 'house'

    @rx.event
    def man_select(self):
        self.object = 'man'

    @rx.event
    def woman_select(self):
        self.object = 'woman'

def type_selecter():
    return rx.vstack(
        rx.flex(
            rx.button(
                "나무",
                color_scheme="red",
                on_click=Output_Selecter.tree_select,
            ),
            rx.button(
                "집",
                color_scheme="gray",
                on_click=Output_Selecter.house_select,
            ),
            rx.button(
                "남자 사람",
                color_scheme="red",
                on_click=Output_Selecter.man_select,
            ),
            rx.button(
                "여자 사람",
                color_scheme="gray",
                on_click=Output_Selecter.woman_select,
            )
        ),
        """
        rx.upload(
            rx.text("심리 검사를 진행할 사진을 등록 해주세요."),
            id="upload3",
            padding="5em",
        )
        """
    )