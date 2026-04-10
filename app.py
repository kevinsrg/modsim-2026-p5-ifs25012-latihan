import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ===============================
# JUDUL APLIKASI
# ===============================
st.title("Simulasi Monte Carlo Proyek Konstruksi")

st.write("Simulasi ini digunakan untuk memperkirakan durasi proyek dan risiko keterlambatan.")

# ===============================
# INPUT USER
# ===============================
n_simulasi = st.slider("Jumlah Simulasi", 1000, 20000, 10000)
deadline = st.slider("Deadline Proyek (bulan)", 10, 30, 20)

st.subheader("Parameter Durasi Tiap Tahap")

col1, col2 = st.columns(2)

with col1:
    mean_perencanaan = st.number_input("Perencanaan (mean)", value=2.0)
    std_perencanaan = st.number_input("Perencanaan (std)", value=0.5)

    mean_pondasi = st.number_input("Pondasi (mean)", value=3.0)
    std_pondasi = st.number_input("Pondasi (std)", value=0.7)

    mean_struktur = st.number_input("Struktur (mean)", value=6.0)
    std_struktur = st.number_input("Struktur (std)", value=1.0)

with col2:
    mean_finishing = st.number_input("Finishing (mean)", value=4.0)
    std_finishing = st.number_input("Finishing (std)", value=0.8)

    mean_instalasi = st.number_input("Instalasi (mean)", value=3.0)
    std_instalasi = st.number_input("Instalasi (std)", value=0.6)

# ===============================
# SIMULASI MONTE CARLO
# ===============================
if st.button("Jalankan Simulasi"):

    # generate data
    perencanaan = np.random.normal(mean_perencanaan, std_perencanaan, n_simulasi)
    pondasi = np.random.normal(mean_pondasi, std_pondasi, n_simulasi)
    struktur = np.random.normal(mean_struktur, std_struktur, n_simulasi)
    finishing = np.random.normal(mean_finishing, std_finishing, n_simulasi)
    instalasi = np.random.normal(mean_instalasi, std_instalasi, n_simulasi)

    # total durasi
    total = perencanaan + pondasi + struktur + finishing + instalasi

    # ===============================
    # HASIL ANALISIS
    # ===============================
    st.subheader("Hasil Simulasi")

    rata2 = np.mean(total)
    minimum = np.min(total)
    maksimum = np.max(total)

    st.write(f"Rata-rata durasi proyek: {rata2:.2f} bulan")
    st.write(f"Durasi minimum: {minimum:.2f} bulan")
    st.write(f"Durasi maksimum: {maksimum:.2f} bulan")

    # risiko keterlambatan
    prob_terlambat = np.mean(total > deadline)
    st.write(f"Probabilitas terlambat dari {deadline} bulan: {prob_terlambat:.2%}")

    # probabilitas selesai
    st.write("Probabilitas selesai sebelum deadline:")
    st.write(f"<= 16 bulan: {np.mean(total <= 16):.2%}")
    st.write(f"<= 20 bulan: {np.mean(total <= 20):.2%}")
    st.write(f"<= 24 bulan: {np.mean(total <= 24):.2%}")

    # ===============================
    # CRITICAL PATH
    # ===============================
    st.subheader("Analisis Tahap Kritis")

    stds = {
        "Perencanaan": np.std(perencanaan),
        "Pondasi": np.std(pondasi),
        "Struktur": np.std(struktur),
        "Finishing": np.std(finishing),
        "Instalasi": np.std(instalasi)
    }

    tahap_kritis = max(stds, key=stds.get)

    st.write("Standar deviasi tiap tahap:")
    st.write(stds)

    st.write(f"Tahap paling kritis: **{tahap_kritis}**")

    # ===============================
    # VISUALISASI
    # ===============================
    st.subheader("Distribusi Durasi Proyek")

    fig, ax = plt.subplots()
    ax.hist(total, bins=50)
    ax.set_xlabel("Durasi (bulan)")
    ax.set_ylabel("Frekuensi")
    ax.set_title("Histogram Durasi Proyek")

    st.pyplot(fig)

    # ===============================
    # SIMULASI RESOURCE TAMBAHAN
    # ===============================
    st.subheader("Simulasi Penambahan Resource (Percepatan Struktur)")

    struktur_baru = np.random.normal(mean_struktur - 1, std_struktur * 0.8, n_simulasi)
    total_baru = perencanaan + pondasi + struktur_baru + finishing + instalasi

    rata_baru = np.mean(total_baru)

    st.write(f"Rata-rata setelah percepatan: {rata_baru:.2f} bulan")

    if rata_baru < rata2:
        st.success("Penambahan resource mempercepat proyek")
    else:
        st.warning("Penambahan resource tidak signifikan")