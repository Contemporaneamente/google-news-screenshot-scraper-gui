from doctest import master
from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import scraperfunction as sf

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("400x600")
window.configure(bg = "#FFFFFF")
window.title("Google News Scraper")
window.iconbitmap("icon.ico")

canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 600,
    width = 400,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    36.0,
    31.0,
    365.0,
    569.0,
    fill="#F8F8F8",
    outline="")

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    200.0,
    174.0,
    image=entry_image_1
)

searchEntry = Entry(bd=0, bg="#E2E0E0", highlightthickness=0)
searchEntry.place(x=69.0, y=141.0, width=262.0, height=64.0)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    200.0,
    292.0,
    image=entry_image_2
)

keywordsEntry = Entry(bd=0, bg="#E2E0E0", highlightthickness=0)
keywordsEntry.place(x=69.0, y=259.0, width=262.0, height=64.0)

canvas.create_text(
    108.0,
    115.0,
    anchor="nw",
    text="Argomento Principale",
    fill="#4B88FD",
    font=("RobotoRoman Bold", 18 * -1)
)

canvas.create_text(
    161.0,
    230.0,
    anchor="nw",
    text="Keywords",
    fill="#4B88FD",
    font=("RobotoRoman Bold", 18 * -1)
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: MakeSearch(),
    relief="flat"
)
button_1.place(
    x=86.0,
    y=462.0420227050781,
    width=230.0,
    height=59.91596984863281
)

def MakeSearch():
    search = searchEntry.get()
    keywords = keywordsEntry.get()
    
    keywordsArray = sf.SplitKeywords(keywords)
    inputStringArray = []

    for keyword in keywordsArray:
        inputStringArray.append(search + " " + keyword)

    for inputString in inputStringArray:
        queryString, pagesLinks = sf.MakeQueryString(inputString, 5)

        webDriver = sf.OpenBrowser(queryString)

        sf.TakeScreenshotForPage(webDriver, pagesLinks, inputString)
        sf.CreatePdf(search)
    
    print("Processo concluso")

window.resizable(False, False)
window.mainloop()

