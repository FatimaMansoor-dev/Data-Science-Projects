import tkinter as tk
from PIL import ImageTk
from authtoken import auth_token 
import torch
from torch import autocast 
from diffusers import StableDiffusionPipeline 
import requests
import urllib3

# Suppressing InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

## create app 
app = tk.Tk()
app.geometry('532x622')
app.title('Stable Bud')

modelid = "CompVis/stable-diffusion-v1-4"
device = 'cpu'
pipe = StableDiffusionPipeline.from_pretrained(modelid, variant='fp16', use_auth_token=auth_token)
pipe.to(device)

def generate():
    try:
        with autocast(device):
            image = pipe(prompt.get(), guidance_scale=8.5)['sample'][0]
        img = ImageTk.PhotoImage(image)
        image.save('generated.png')
    except requests.exceptions.RequestException as e:
        print(f"An error occurred during file download: {e}")

prompt = tk.Entry(app, font=('Arial', 16), fg='black', bg='white')
prompt.place(x=10, y=10)

main = tk.Label(app, text='hi', height=512, width=512)  
main.place(x=10, y=110)

trigger = tk.Button(app, text='Generate Image', font=('Arial', 16), fg='white', bg='red', relief='raised', command=generate)
trigger.place(x=40, y=150)

app.mainloop()
