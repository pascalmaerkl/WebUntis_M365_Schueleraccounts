import io

import pandas as pd
import streamlit as st

SHEET_NAME = "not_defined"
OUTPUT_SHEET_NAME = "Ergebnis"


def process_data(df: pd.DataFrame) -> pd.DataFrame:
    """Verarbeitet die eingelesenen Daten und liefert das Ergebnis."""
    benutzername = df.iloc[:, 1] # zweite Spalte der Excel
    return pd.DataFrame({
        "Benutzername": benutzername,
        "Office365-Identität": benutzername.astype(str) + "@gbg-winnenden.de",
    })
    

def dataframe_to_csv(df: pd.DataFrame) -> bytes:
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False, sep=";", encoding="utf-8-sig")
    return buffer.getvalue()


def read_daten_sheet(uploaded_file) -> pd.DataFrame:    
    global SHEET_NAME
    excel_file = pd.ExcelFile(uploaded_file, engine="xlrd")
    SHEET_NAME = excel_file.sheet_names[0]
    #if SHEET_NAME not in excel_file.sheet_names:
    #    available = ", ".join(excel_file.sheet_names)
    #    raise ValueError(
    #        f'Tabellenblatt "{SHEET_NAME}" wurde nicht gefunden. '
    #        f"Verfügbare Blätter: {available}"
    #    )
    return pd.read_excel(excel_file)


st.set_page_config(page_title="WebUntis → M365 Schüleraccounts", layout="wide")
st.title("WebUntis → M365 Schüleraccounts")

st.info("""
**Excel-Export aus Webuntis hochladen**

- Die Exportdatei erhält man aus WebUntis mit Adminrechten, dann unter _Administation > Benutzer_.
- Folgende Einstellungen:
  - Benutzergruppe: Schüler*innen
  - Aktive Benutzer anhaken
- Dann ganz unten _Berichte > xls_.
""")

uploaded_file = st.file_uploader(
    "Excel-Datei auswählen",
    type=["xlsx", "xls"]
)

if uploaded_file is not None:
    try:
        df_input = read_daten_sheet(uploaded_file)
        df_result = process_data(df_input)

        st.success(
            f'Tabellenblatt "{SHEET_NAME}" erfolgreich eingelesen '
            #f"({len(df_result)} Zeilen, {len(df_result.columns)} Spalten)."
        )

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Eingelesene Daten")
            st.dataframe(df_input, use_container_width=True)
        with col2:
            st.subheader("Ergebnis")
            st.dataframe(df_result, use_container_width=True)

        output_name = "webuntis_m365_eintragen.csv"
        download_data = dataframe_to_csv(df_result)
        st.success(
            f'WebUntis-Import-Datei erzeugt.'
        )
        st.download_button(
            label="CSV herunterladen",
            data=download_data,
            file_name=output_name,
            mime="text/csv",
        )
        
    except ValueError as exc:
        st.error(str(exc))
    except Exception as exc:
        st.error(f"Fehler beim Verarbeiten der Datei: {exc}")
