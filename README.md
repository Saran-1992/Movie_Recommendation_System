# 🎬 Movie Recommendation System

This is a **Content-Based Movie Recommendation System** built using Python, TF-IDF vectorization, and cosine similarity. The system provides movie suggestions based on a selected movie's overview, genres, cast, crew, and keywords.

> **Note:** The current dataset contains international movies, not Tamil movies.

---

## 📂 Datasets

The system uses two datasets:

1. **Movies dataset**
   - Contains metadata about movies (title, overview, genres, cast, crew, etc.)
   - Download link: [Movies Dataset](https://drive.google.com/file/d/15bXnYaCwRbh6T0C0-XuYscvqb7Tg8E1Z/view?usp=drive_link)

2. **Credits dataset**
   - Contains cast and crew information for movies
   - Download link: [Credits Dataset](https://drive.google.com/file/d/19NBuzDS6JRgs7tkjGuL93lvuhuHEdrHN/view?usp=drive_link)

> Both files should be placed in the same directory as the main Python script.

---

## 🛠 Features

- Content-based recommendations using **TF-IDF vectorization** on movie tags
- Cosine similarity to find top 10 similar movies
- Streamlit UI for interactive selection and display
- Posters fetched using **OMDb API**

---

## ⚡ How to Run

1. Clone the repository:

```bash
git clone <repo-url>
cd <repo-folder>
