import os
import tkinter as tk
import requests
import json
from tkinter import messagebox
from PIL import Image, ImageTk
import io

os.environ['TCL_LIBRARY'] = r'C:\Users\ceren\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Users\ceren\AppData\Local\Programs\Python\Python313\tcl\tk8.6'

API_KEY = "e830f358"
SAVED_MOVIES_FILE = "saved_movies.json"


def load_saved_movies():
    if os.path.exists(SAVED_MOVIES_FILE):
        try:
            with open(SAVED_MOVIES_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []


def save_movie_to_file(movie_data):
    saved_movies = load_saved_movies()

    for movie in saved_movies:
        if movie.get('title') == movie_data.get('title'):
            messagebox.showwarning("Uyarı", "Bu film zaten kaydedilmiş!")
            return False

    saved_movies.append(movie_data)

    try:
        with open(SAVED_MOVIES_FILE, 'w', encoding='utf-8') as f:
            json.dump(saved_movies, f, ensure_ascii=False, indent=2)
        messagebox.showinfo("Başarılı", "Film başarıyla kaydedildi!")
        return True
    except Exception as e:
        messagebox.showerror("Hata", f"Film kaydedilirken hata oluştu: {e}")
        return False


def get_movie_info(film_name):
    url = f"http://www.omdbapi.com/?apikey={API_KEY}&t={film_name}"
    response = requests.get(url)
    data = response.json()

    if data.get("Response") == "True":
        title = data.get("Title", "Bilinmiyor")
        year = data.get("Year", "Bilinmiyor")
        plot = data.get("Plot", "Açıklama yok")
        poster = data.get("Poster", "Poster bulunamadı")
        return {
            'title': title,
            'year': year,
            'plot': plot,
            'poster': poster,
            'display_text': f"{title} ({year})\n\n{plot}"
        }
    else:
        return None


def search_movie():
    film_name = movie_input.get().strip()
    if not film_name:
        messagebox.showwarning("Uyarı", "Lütfen bir film adı girin.")
        return

    movie_data = get_movie_info(film_name)

    if movie_data:
        show_movie.config(state="normal")
        show_movie.delete(1.0, tk.END)
        show_movie.insert(tk.END, movie_data['display_text'])
        show_movie.config(state="disabled")

        save_button.config(state="normal")
        global current_movie_data
        current_movie_data = movie_data

        # Poster göster
        show_poster(movie_data['poster'])
    else:
        show_movie.config(state="normal")
        show_movie.delete(1.0, tk.END)
        show_movie.insert(tk.END, " Film bulunamadı. Lütfen başka bir isim deneyin.")
        show_movie.config(state="disabled")
        save_button.config(state="disabled")
        poster_label.config(image='')


def show_poster(poster_url):
    try:
        response = requests.get(poster_url)
        image_data = response.content
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((200, 300))
        photo = ImageTk.PhotoImage(image)

        poster_label.image = photo
        poster_label.config(image=photo)
    except:
        poster_label.config(image='')


def save_current_movie():
    global current_movie_data
    if current_movie_data:
        save_movie_to_file(current_movie_data)
    else:
        messagebox.showwarning("Uyarı", "Kaydedilecek film bulunamadı!")


def show_saved_movies():
    saved_window = tk.Toplevel(window)
    saved_window.title("Kaydedilen Filmler")
    saved_window.geometry("800x600")
    saved_window.resizable(True, True)

    title_label = tk.Label(saved_window, text=" Kaydedilen Filmler", font=('Arial', 16, "bold"))
    title_label.pack(pady=10)

    list_frame = tk.Frame(saved_window)
    list_frame.pack(fill="both", expand=True, padx=20, pady=10)

    text_frame = tk.Frame(list_frame)
    text_frame.pack(fill="both", expand=True)

    saved_text = tk.Text(text_frame, wrap="word", font=('Arial', 12))
    scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=saved_text.yview)
    saved_text.configure(yscrollcommand=scrollbar.set)

    saved_text.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    saved_movies = load_saved_movies()

    if not saved_movies:
        saved_text.insert(tk.END, "Henüz kaydedilmiş film bulunmuyor.")
    else:
        for i, movie in enumerate(saved_movies, 1):
            saved_text.insert(tk.END, f"{i}. {movie['title']} ({movie['year']})\n")
            saved_text.insert(tk.END, f"   {movie['plot']}\n")
            saved_text.insert(tk.END, f"   🎞 Poster: {movie.get('poster', 'Yok')}\n")
            saved_text.insert(tk.END, "-" * 80 + "\n\n")

    saved_text.config(state="disabled")


# === UI ===
window = tk.Tk()
window.title(" MovieMate - Film Arama ve Kaydetme")
window.geometry("850x850")
window.resizable(True, True)

search_frame = tk.Frame(window, padx=20, pady=20)
search_frame.grid(row=0, column=0, sticky="ew")

content_label = tk.Label(search_frame, text="Lütfen film adını girin:", font=('Arial', 14, "bold"))
content_label.grid(row=0, column=0, sticky="w", pady=(0, 10))

movie_input = tk.Entry(search_frame, width=40, font=('Arial', 13))
movie_input.grid(row=0, column=1, padx=(10, 0), pady=(0, 10))

search_button = tk.Button(search_frame, text="Ara", font=('Arial', 13, "bold"), width=10, command=search_movie)
search_button.config(fg="Green")
search_button.grid(row=0, column=2, padx=(10, 0), pady=(0, 10))

save_button = tk.Button(search_frame, text="Kaydet", font=('Arial', 13, "bold"), width=10,
                        command=save_current_movie, state="disabled")
save_button.config(fg="Blue")
save_button.grid(row=0, column=3, padx=(10, 0), pady=(0, 10))

saved_movies_button = tk.Button(search_frame, text=" Kaydedilenler", font=('Arial', 13, "bold"), width=15,
                                command=show_saved_movies)
saved_movies_button.config(fg="Purple")
saved_movies_button.grid(row=0, column=4, padx=(10, 0), pady=(0, 10))

result_frame = tk.Frame(window, padx=20, pady=10)
result_frame.grid(row=1, column=0, sticky="nsew")

show_movie = tk.Text(result_frame, width=80, height=18, font=('Arial', 13), wrap="word", borderwidth=2, relief="groove")
show_movie.grid(row=0, column=0, sticky="nsew")

# Poster göstermek için boş label
poster_label = tk.Label(result_frame)
poster_label.grid(row=1, column=0, pady=10)

window.grid_rowconfigure(1, weight=1)
window.grid_columnconfigure(0, weight=1)
result_frame.grid_rowconfigure(0, weight=1)
result_frame.grid_columnconfigure(0, weight=1)

window.mainloop()
