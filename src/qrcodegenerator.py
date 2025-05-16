import qrcode
from PIL import Image, ImageDraw, ImageTk
import tkinter as tk
from tkinter import ttk, filedialog, colorchooser, messagebox
import os

# Função para gerar o QR Code em tempo real
def atualizar_preview(event=None):
    texto = entrada_texto.get()
    cor_hex = entrada_cor.get().replace("#", "")
    if not texto:
        texto = "SEU TEXTO AQUI"

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=25,
            border=2,
        )
        qr.add_data(texto)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="#" + cor_hex, back_color="white").convert("RGBA")
        qr_img = qr_img.resize((250, 250))

        if entrada_logo.get():
            logo = Image.open(entrada_logo.get()).convert("RGBA")
            logo = logo.resize((80, 80))
            qr_img.paste(logo, ((qr_img.width - logo.width) // 2, (qr_img.height - logo.height) // 2), logo)

        qr_preview_tk = ImageTk.PhotoImage(qr_img)
        label_preview.config(image=qr_preview_tk)
        label_preview.image = qr_preview_tk

    except:
        pass

# Função para selecionar o logo
def selecionar_logo():
    caminho_logo = filedialog.askopenfilename()
    if caminho_logo:
        entrada_logo.delete(0, tk.END)
        entrada_logo.insert(0, caminho_logo)
        atualizar_preview()

# Função para selecionar a cor
def selecionar_cor():
    cor_selecionada = colorchooser.askcolor()[1]
    if cor_selecionada:
        entrada_cor.delete(0, tk.END)
        entrada_cor.insert(0, cor_selecionada.replace("#", ""))
        atualizar_preview()

# Função para limpar todos os campos
def limpar_campos():
    entrada_texto.delete(0, tk.END)
    entrada_cor.delete(0, tk.END)
    entrada_logo.delete(0, tk.END)
    entrada_cor.insert(0, "000000")
    atualizar_preview()

# Função para gerar e salvar o QR Code
def gerar_qrcode():
    atualizar_preview()  # Garantir que a pré-visualização esteja atualizada
    texto = entrada_texto.get()
    cor_hex = entrada_cor.get().replace("#", "")
    caminho_logo = entrada_logo.get()

    if not texto:
        texto = "SEU TEXTO AQUI"

    pasta_destino = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")], title="Salvar QR Code")
    if not pasta_destino:
        return

    try:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=25,
            border=2,
        )

        qr.add_data(texto)
        qr.make(fit=True)

        qr_img = qr.make_image(fill_color="#" + cor_hex, back_color="white").convert("RGBA")
        qr_img = qr_img.resize((1080, 1080))

        if caminho_logo:
            logo = Image.open(caminho_logo).convert("RGBA")
            logo = logo.resize((250, 250))
            qr_img.paste(logo, ((qr_img.width - logo.width) // 2, (qr_img.height - logo.height) // 2), logo)

        qr_img.save(pasta_destino)
        messagebox.showinfo("Sucesso", f"QR Code gerado e salvo em '{pasta_destino}'.")

    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao gerar QR Code: {str(e)}")

# Interface Gráfica
app = tk.Tk()
app.title("Gerador de QR Code - by Caio Carreira")
app.geometry("700x750")
app.configure(bg="#1e1e2d")

style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#1e1e2d", foreground="white", font=("Helvetica", 13))
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 13, "bold"), background="#1abc9c", foreground="white", padding=8)

label_titulo = ttk.Label(app, text="GERADOR DE QR CODE", font=("Helvetica", 16, "bold"), background="#1e1e2d", foreground="white")
label_titulo.pack(pady=10)

frame_campos = tk.Frame(app, bg="#1e1e2d")
frame_campos.pack(pady=15)

label_texto = ttk.Label(frame_campos, text="Texto ou URL:")
label_texto.grid(row=0, column=0, sticky="e", pady=8)
entrada_texto = ttk.Entry(frame_campos, width=35)
entrada_texto.grid(row=0, column=1, pady=8, padx=5)
entrada_texto.bind("<KeyRelease>", atualizar_preview)

label_cor = ttk.Label(frame_campos, text="Cor HEX (Ex: FF0000):")
label_cor.grid(row=1, column=0, sticky="e", pady=8)
entrada_cor = ttk.Entry(frame_campos, width=15)
entrada_cor.grid(row=1, column=1, padx=5, sticky="w")
entrada_cor.insert(0, "000000")
entrada_cor.bind("<KeyRelease>", atualizar_preview)

botao_cor = tk.Button(frame_campos, text="Selecionar Cor", command=selecionar_cor, relief="flat", bg="#8080ff", fg="#ffffff")
botao_cor.grid(row=1, column=2, padx=8, sticky="w")

label_logo = ttk.Label(frame_campos, text="Logo (Opcional):")
label_logo.grid(row=2, column=0, sticky="e", pady=2)
entrada_logo = ttk.Entry(frame_campos, width=35)
entrada_logo.grid(row=2, column=1, pady=8, padx=5)

botao_logo = tk.Button(frame_campos, text="Selecionar Logo", command=selecionar_logo)
botao_logo.grid(row=2, column=2)

label_preview = tk.Label(app, bg="#1e1e2d")
label_preview.pack(pady=10)

botao_gerar = tk.Button(app, text="Salvar QR Code", command=gerar_qrcode)
botao_gerar.pack(pady=10)

botao_limpar = tk.Button(app, text="EXCLUIR", command=limpar_campos)
botao_limpar.pack(pady=5)

atualizar_preview()  # Iniciar com pré-visualização
app.mainloop()
