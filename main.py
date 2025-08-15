import flet as ft
import yt_dlp
import threading
import os


def main(page: ft.Page):
    page.title = "Video Downloader"
    page.window_width = 450
    page.window_height = 350
    page.theme_mode = ft.ThemeMode.DARK

    save_path = os.path.expanduser("~")

    link_input = ft.TextField(label="رابط الفيديو", width=400)
    quality_dropdown = ft.Dropdown(
        label="اختر الجودة",
        options=[
            ft.dropdown.Option("best"),
            ft.dropdown.Option("worst"),
            ft.dropdown.Option("audio")
        ],
        value="best",
        width=400
    )
    folder_input = ft.TextField(
        label="مسار الحفظ", value=save_path, width=400
    )
    status_text = ft.Text(value="", color="yellow")
    progress = ft.ProgressBar(width=400, visible=False)

    def choose_folder(e):
        try:
            dlg = ft.FilePicker(on_result=lambda res: folder_input.value = res.path)
        except:
            status_text.value = "ميزة اختيار المجلد غير مدعومة هنا"
            page.update()

    def download_video(e):
        url = link_input.value.strip()
        quality = quality_dropdown.value
        folder = folder_input.value.strip()

        if not url:
            status_text.value = "⚠️ يرجى إدخال رابط"
            page.update()
            return
        if not os.path.exists(folder):
            status_text.value = "⚠️ مسار الحفظ غير موجود"
            page.update()
            return

        def run_download():
            try:
                progress.visible = True
                status_text.value = "⬇️ جاري التحميل..."
                page.update()

                ydl_opts = {
                    'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
                    'noplaylist': True,
                }

                if quality == "audio":
                    ydl_opts["format"] = "bestaudio/best"
                    ydl_opts["postprocessors"] = [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                elif quality == "best":
                    ydl_opts["format"] = "best"
                elif quality == "worst":
                    ydl_opts["format"] = "worst"

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                status_text.value = "✅ تم التحميل بنجاح!"
            except Exception as ex:
                status_text.value = f"❌ خطأ: {ex}"
            finally:
                progress.visible = False
                page.update()

        threading.Thread(target=run_download).start()

    download_btn = ft.ElevatedButton("تحميل", on_click=download_video)

    page.add(
        link_input,
        quality_dropdown,
        folder_input,
        download_btn,
        progress,
        status_text
    )


ft.app(target=main)
