import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "libs"))
import flet as ft
import ollama

query = sys.argv[1]

messages=[{'role': 'user', 'content': query}]

collected_messages = []
def streaming_window(page: ft.Page):
    # scrollable setting by ScrollMode

    page.scroll = ft.ScrollMode("auto")
    page.auto_scroll = True

    # fonts setting by page.fonts and ft.theme
    # page.fonts = {
    #     "Helvetica": os.path.join(
    #         os.path.dirname(__file__), "fonts", "Helvetica.ttc"
    #     )
    # }
    # page.theme = ft.Theme(font_family="Helvetica")

    # press Esc or cmd + w to close window
    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "Escape" or (e.key == "W" and e.meta):
            page.window_destroy()

    page.on_keyboard_event = on_keyboard

    # main TextField for reply
    t = ft.TextField(
        label="",
        multiline=True,
        value="",
        color="grey",
        border_color="transparent",
    )
    page.controls.append(t)
    page.update()


    collected_messages.append(f"Prompt: {query}\n\n")
    t.value = (
            f"{''.join([m for m in collected_messages])}▌"
    )
    t.update()

    # iterate the streamed reply
    # for chunk in response:
    for chunk in ollama.chat('llama2', messages=messages, stream=True):
        chunk_message = chunk['message']['content']

        collected_messages.append(chunk_message)

        # concatenate streamed result and add a left half block for ChatGPT-like cursor effect
        t.value = (
            f"{''.join([m for m in collected_messages])}▌"
        )
        t.update()

    # remove left half block since all results have been streamed
    t.value = t.value[:-1]
    # set cursor focus to TextField
    t.focus()
    t.update()



    # all content is loaded, the user should be able to scrolling freely
    page.auto_scroll = False
    page.update()

# show window
ft.app(target=streaming_window)
full_reply_content = "".join([m for m in collected_messages])
print(full_reply_content)
