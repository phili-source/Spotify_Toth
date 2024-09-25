import pandas as pd
from tqdm import tqdm


pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.width', 1000)


def load_data(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        print("Die angegebene Datei wurde nicht gefunden.")
        return pd.DataFrame()


def save_data(file_path, data):
    try:
        data.to_csv(file_path, index=False)
        print("Daten erfolgreich gespeichert.")
    except Exception as e:
        print(f"Fehler beim Speichern der Daten: {e}")


def linear_search(data, column, query):
    results = data[data[column].str.contains(query, case=False, na=False)]
    return results

def binary_search(data, column, query):
    data_sorted = data.sort_values(by=column).reset_index(drop=True)
    low, high = 0, len(data_sorted) - 1
    query_lower = query.lower()

    while low <= high:
        mid = (low + high) // 2
        mid_value = data_sorted.loc[mid, column].lower()

        if mid_value == query_lower:
            return data_sorted.loc[[mid]]
        elif mid_value < query_lower:
            low = mid + 1
        else:
            high = mid - 1
    return pd.DataFrame()


def display_results(results):
    page_size = 10
    total_results = len(results)
    current_page = 0

    while True:
        start = current_page * page_size
        end = start + page_size
        page_results = results.iloc[start:end]

        print(f"\nZeige Ergebnisse {start + 1} bis {min(end, total_results)} von {total_results}:")
        print(page_results[['track_name', 'artists', 'album_name', 'track_genre']])

        if total_results <= page_size:
            break

        print("\nNavigiere durch die Ergebnisse:")
        print("n = nächste Seite, p = vorherige Seite, q = zurück zum Menü")
        action = input("Wähle eine Option: ").lower()

        if action == 'n' and end < total_results:
            current_page += 1
        elif action == 'p' and current_page > 0:
            current_page -= 1
        elif action == 'q':
            break
        else:
            print("Ungültige Eingabe.")


def bubble_sort(data, attribute):
    n = len(data)
    for i in tqdm(range(n), desc="Bubble Sort Fortschritt"):
        for j in range(0, n - i - 1):
            if str(data.iloc[j][attribute]) > str(data.iloc[j + 1][attribute]):
                data.iloc[j], data.iloc[j + 1] = data.iloc[j + 1], data.iloc[j]
    return data

def quick_sort(data, attribute, depth=0):
    if len(data) <= 1:
        return data
    pivot = str(data.iloc[len(data) // 2][attribute])
    left = data[data[attribute] < pivot]
    middle = data[data[attribute] == pivot]
    right = data[data[attribute] > pivot]

    tqdm.write(f"Quick Sort Tiefe {depth}: linke Größe: {len(left)}, mittlere Größe: {len(middle)}, rechte Größe: {len(right)}")
    sorted_left = quick_sort(left, attribute, depth+1)
    sorted_right = quick_sort(right, attribute, depth+1)

    return pd.concat([sorted_left, middle, sorted_right], ignore_index=True)


def display_all_songs(sorted_df):
    print("\nAlle Songs im DataFrame:")
    for index, row in sorted_df.iterrows():
        print(f"{index + 1}: {row['track_name']} von {row['artists']} (Album: {row['album_name']}, Genre: {row['track_genre']})")


def display_playlists(playlists):
    print("\nAlle Playlists:")
    for playlist, songs in playlists.items():
        print(f"\nPlaylist: {playlist}")
        if not songs:
            print("Keine Songs in dieser Playlist.")
        else:
            for song in songs:
                print(f"- {song['track_name']} von {song['artists']} (Album: {song['album_name']}, Genre: {song['track_genre']})")


def display_songs(data, sort_method):
    if sort_method == '1':  # Bubble Sort
        sorted_songs = bubble_sort(data.copy(), 'track_name')
    elif sort_method == '2':  # Quick Sort
        sorted_songs = quick_sort(data.copy(), 'track_name')
    else:
        print("Ungültige Sortiermethode.")
        return

    print("\nAlle Songs in der Datenbank:")
    display_results(sorted_songs)


def spotify_library(data, playlists):
    while True:
        print("\nSpotify Bibliothek:")
        print("1. Alle Playlists anzeigen")
        print("2. Alle Songs in der Datenbank anzeigen")
        print("3. Zurück zum Hauptmenü")

        choice = input("Wähle eine Option: ")

        if choice == '1':
            display_playlists(playlists)
        elif choice == '2':
            sort_method = input("Wähle eine Sortiermethode:\n1. Bubble Sort\n2. Quick Sort\nDeine Wahl: ")
            display_songs(data, sort_method)
        elif choice == '3':
            break
        else:
            print("Ungültige Eingabe. Bitte versuche es erneut.")


def search(data, column_name):
    search_method = input("Wähle eine Suchmethode:\n1. Ungenaue Suche (linear)\n2. Genaue Suche (binary)\nDeine Wahl: ")
    query = input(f"Gib den Suchbegriff für {column_name} ein: ")

    if search_method == '1':
        results = linear_search(data, column_name, query)
    elif search_method == '2':
        results = binary_search(data, column_name, query)
    else:
        print("Ungültige Suchmethode.")
        return

    if not results.empty:
        display_results(results)
    else:
        print(f"Keine Ergebnisse für '{query}' gefunden.")


def add_song_to_database(file_path):
    print("Bitte gib die Details des neuen Songs ein:")

    track_name = input("Track-Name: ").strip() or "n/A"
    artists = input("Künstler: ").strip() or "n/A"
    album_name = input("Album-Name: ").strip() or "n/A"
    track_genre = input("Genre: ").strip() or "n/A"

    new_song = pd.DataFrame({
        'track_name': [track_name],
        'artists': [artists],
        'album_name': [album_name],
        'track_genre': [track_genre]
    })


    data = load_data(file_path)

    data = pd.concat([data, new_song], ignore_index=True)

    save_data(file_path, data)

    print(f"Song '{track_name}' erfolgreich zur Datenbank hinzugefügt.\n")


def spotify_search_menu(data):
    while True:
        print("Spotify durchsuchen:")
        print("1. Songs suchen")
        print("2. Künstler suchen")
        print("3. Genre suchen")
        print("4. Album suchen")
        print("5. Zurück zum Hauptmenü")

        choice = input("Wähle eine Option: ")

        if choice == '1':
            search(data, 'track_name')
        elif choice == '2':
            search(data, 'artists')
        elif choice == '3':
            search(data, 'track_genre')
        elif choice == '4':
            search(data, 'album_name')
        elif choice == '5':
            break
        else:
            print("Ungültige Eingabe. Bitte versuche es erneut.")


def manage_playlists(playlists, data):
    while True:
        print("Playlists verwalten:")
        print("1. Playlist erstellen")
        print("2. Playlist löschen")
        print("3. Songs zu einer Playlist hinzufügen")
        print("4. Zurück zum Hauptmenü")

        choice = input("Wähle eine Option: ")

        if choice == '1':
            playlist_name = input("Gib den Namen der neuen Playlist ein: ")
            if playlist_name in playlists:
                print("Diese Playlist existiert bereits.")
            else:
                playlists[playlist_name] = []
                print(f"Playlist '{playlist_name}' wurde erstellt.")

        elif choice == '2':
            playlist_name = input("Gib den Namen der zu löschenden Playlist ein: ")
            if playlist_name in playlists:
                del playlists[playlist_name]
                print(f"Playlist '{playlist_name}' wurde gelöscht.")
            else:
                print("Playlist existiert nicht.")

        elif choice == '3':
            playlist_name = input("Gib den Namen der Playlist ein, zu der du Songs hinzufügen möchtest: ")
            if playlist_name in playlists:

                display_all_songs(data)

                song_index = input("Gib die Indexnummer des Songs ein, den du hinzufügen möchtest: ")
                try:
                    song_index = int(song_index)
                    if 0 <= song_index < len(data):
                        song = data.iloc[song_index]
                        playlists[playlist_name].append(song)
                        print(f"Song '{song['track_name']}' wurde zur Playlist '{playlist_name}' hinzugefügt.")
                    else:
                        print("Ungültiger Songindex.")
                except ValueError:
                    print("Bitte gib eine gültige Zahl ein.")
            else:
                print("Playlist existiert nicht.")

        elif choice == '4':
            break

        else:
            print("Ungültige Eingabe. Bitte versuche es erneut.")


def main_menu():
    print("\nSpotify:")
    print("1. Durchsuche Spotify")
    print("2. Füge neue Songs zur Datenbank hinzu")
    print("3. Playlists verwalten")
    print("4. Spotify Bibliothek anzeigen")
    print("5. Beenden")

    return input("Wähle eine Option: ")


def start_app():
    file_path = "spotify_dataframe_cleaned.csv"
    data = load_data(file_path)

    playlists = {}
    while True:
        choice = main_menu()
        if choice == '1':
            spotify_search_menu(data)
        elif choice == '2':
            add_song_to_database(file_path)
        elif choice == '3':
            manage_playlists(playlists, data)
        elif choice == '4':
            spotify_library(data, playlists)
        elif choice == '5':
            print("App wird beendet...")
            break
        else:
            print("Ungültige Eingabe. Bitte versuche es erneut.")


if __name__ == "__main__":
    start_app()













































