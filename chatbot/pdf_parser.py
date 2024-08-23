import os
import PyPDF2

# Шлях до папки з PDF-файлами
folder_path = "I:\interview_passer\data"  # Замініть на ваш шлях
# Шлях до папки, де будуть зберігатися текстові файли
output_folder = "I:\interview_passer\data"  # Замініть на ваш шлях
# Переконаємося, що папка для збереження текстових файлів існує
os.makedirs(output_folder, exist_ok=True)


def pdf_parser():
    # Проходимо по всіх файлах у папці
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            # Формуємо повний шлях до PDF-файлу
            file_path = os.path.join(folder_path, filename)

            # Відкриваємо PDF файл
            with open(file_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                text = ""

                # Витягуємо текст з усіх сторінок PDF
                for page in reader.pages:
                    text += page.extract_text()

                # Формуємо ім'я текстового файлу
                txt_filename = os.path.splitext(filename)[0] + ".txt"
                txt_file_path = os.path.join(output_folder, txt_filename)

                # Зберігаємо текст у текстовий файл
                with open(txt_file_path, "w", encoding="utf-8") as txt_file:
                    txt_file.write(text)

                print(f"Saved text from {filename} to {txt_filename}")

    # Відкриваємо файл з кодуванням ISO-8859-1 та читаємо вміст
    with open(
        "data/Python Package Management — PySpark 3.5.2 documentation.txt",
        "r",
        encoding="ISO-8859-1",
    ) as file:
        content = file.read()

    # Зберігаємо прочитаний вміст у новий файл з кодуванням UTF-8
    with open(
        "data/Python_Package_Management_PySpark_3.5.2_documentation_utf8.txt",
        "w",
        encoding="UTF-8",
    ) as file:
        file.write(content)

    print("Файл успішно перетворено та збережено у форматі UTF-8.")


if __name__ == "__main__":
    pdf_parser()
