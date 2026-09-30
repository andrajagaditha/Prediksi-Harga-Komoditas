import streamlit as st
import pandas as pd
import numpy as np

st.title("prediksi harga komoditas pangan")
st.write("pantau tren dan peringatan dini harga cabai, bawang dan beras.")


@st.cache_data
def muat_data(path):
    # 1. Baca file Excel, semua isi dibaca sebagai teks dulu
    df = pd.read_excel(path, dtype=str)

    # 2. Ambil hanya baris "Kota Semarang"
    baris = df[df["Komoditas (Rp)"] == "Kota Semarang"].iloc[0]

    # 3. Buang 2 kolom pertama (No dan nama), sisanya tanggal dan harga
    seri = baris.drop(["No", "Komoditas (Rp)"])

    # 4. bersihkan tanggal dan harga
    tanggal = pd.to_datetime(seri.index.str.replace(" ", ""), format="%d/%m/%Y")
    harga_bersih = seri.str.replace(".", "", regex=False).str.replace(
        ",", "", regex=False
    )
    harga = pd.to_numeric(harga_bersih, errors="coerce").values

    # 5. susun jadi tabel
    return pd.DataFrame({"harga": harga}, index=tanggal).rename_axis("tanggal")


def rupiah(angka):
    return f"Rp{angka:,.0f}".replace(",", ".")


df = muat_data("harga_cabai_semarang.xlsx")

st.subheader("cabai rawit merah, kota semarang")

harga_terakhir = df["harga"].iloc[-1]
harga_minggu_lalu = df["harga"].iloc[-6]
selisih = harga_terakhir - harga_minggu_lalu

tanda = "+" if selisih > 0 else ""
st.metric(
    "harga terakhir per Kg",
    rupiah(harga_terakhir),
    delta=f"{tanda}{selisih:,.0f} dibanding seminggu lalu".replace(",", "."),
)

st.line_chart(df["harga"])

with st.expander("lihat tabel data"):
    st.dataframe(df)
