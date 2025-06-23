![image](https://github.com/user-attachments/assets/4a6a49bf-3917-4088-afc8-5fbc5fcb664d)
# 🎓 Aplikasi Prediksi Gaya Belajar Mahasiswa - Felder-Silverman

Aplikasi ini dirancang untuk mengidentifikasi **gaya belajar mahasiswa** berdasarkan model **Felder-Silverman Learning Style Model (FSLSM)**. Aplikasi ini menggunakan **metode Naive Bayes** untuk memprediksi kecenderungan gaya belajar dari hasil kuisioner yang dijawab oleh mahasiswa.

---

## 📌 Fitur Utama

- 📝 Form kuisioner 44 soal berdasarkan 4 dimensi FSLSM:
  - **Processing:** Aktif vs Reflektif
  - **Perception:** Sensitif vs Intuitif
  - **Input:** Visual vs Verbal
  - **Understanding:** Sekuensial vs Global
- 🔍 Prediksi gaya belajar berdasarkan jawaban pengguna
- 📊 Menampilkan hasil prediksi secara jelas dan informatif
- 🗃 Menyimpan hasil ke database untuk keperluan analisis lanjutan
- 📤 Export data hasil (opsional)

---

## 🧠 Teknologi yang Digunakan

- **Python**
- **Flask** – Web Framework
- **HTML/CSS** – Tampilan antarmuka
- **SQLite/MySQL** – Penyimpanan data responden
- **Scikit-learn** – Implementasi Naive Bayes
- **Pandas, NumPy** – Manipulasi dan analisis data

---

## 🚀 Cara Menjalankan Aplikasi

### 1. Clone repositori

```bash
git clone https://github.com/hanatyani/gaya-belajar-app.git
cd gaya-belajar-app
pip install -r requirements.txt
python app.py



