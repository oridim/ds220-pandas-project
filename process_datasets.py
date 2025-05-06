import csv


def clean_array(value):
    return ",".join(sorted(value.replace(", ", ",").split(",")))


def clean_string(value):
    return value.strip()


def has_value(value):
    return value is not None and value.strip() != ""


cleaned_movies = None

input_handle = open(
    "./datasets/alanvourch.tmdb-movies-daily-updates.csv",
    mode="r",
    newline="",
    encoding="utf-8",
)

csv_reader = csv.reader(input_handle)

# Skip header row.
next(csv_reader)

cleaned_movies = list(
    (
        {
            "id": clean_string(row[9]),  # row[9]: "imdb_id"
            "title": clean_string(row[1]),  # row[1]: "title"
            "rating": clean_string(row[25]),  # row[25]: "imdb_rating"
            "box_office": clean_string(row[6]),  # row[6]: "revenue"
            "budget": clean_string(row[8]),  # row[8]: "budget"
            "runtime": clean_string(row[7]),  # row[7]: "runtime"
            "genres": clean_array(clean_string(row[15]).lower()),  # row[15]: "genres"
        }
        for row in csv_reader
        if row[4] == "Released"  # row[4]: "status"
        and row[10] == "en"  # row[10]: "original_language"
        and row[18].lower().strip() == "english"  # row[18]: "spoken_languages"
        and has_value(row[1])  # row[1]: "title"
        and has_value(row[6])  # row[6]: "revenue"
        and has_value(row[7])  # row[7]: "runtime"
        and has_value(row[8])  # row[8]: "budget"
        and has_value(row[9])  # row[9]: "imdb_id"
        and has_value(row[15])  # row[15]: "genres"
        and not ("tv movie" in row[15].lower())
        and has_value(row[25])  # row[25]: "imdb_rating"
    )
)

input_handle.close()

column_names = cleaned_movies[0].keys()
output_handle = open(
    "./datasets/oridim.imdb.cleaned.csv", mode="w", newline="", encoding="utf-8"
)
output_writer = csv.DictWriter(output_handle, fieldnames=column_names)

output_writer.writeheader()
output_writer.writerows(cleaned_movies)

output_handle.close()
