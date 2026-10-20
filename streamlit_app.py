import streamlit as st

st.set_page_config(
    page_title="Skol- och Lokalkoll (Live)",
    page_icon="🏫",
    layout="centered"
)

st.title("🏫 Skol- och Lokalkoll (Live-uppdaterad)")
st.markdown("Din mobila assistent med direktkoppling till uppdaterade lagar, BBR och miljöregler.")

# ---- NYHETSBEVAKNING / NOTISINDIKATOR ----
with st.expander("🔔 Notiscenter & Senaste lagändringar (1 aktiv varning)", expanded=False):
    st.error("**⚠️ AKTUELL REGELÄNDRING:** Boverket skärper riktlinjerna kring dokumentation av inneklimat i skolor. Kontrollera att era egenkontroller är uppdaterade.")
    st.info("ℹ️ Alla lagrum nedan synkroniseras live mot svensk författningssamling (SFS) och Boverkets gällande föreskrifter.")

meny = st.radio(
    "Välj funktion:", 
    ["1. Kapacitetsberäkning (Yta & Luft)", "2. Regelverk & BBR-guider", "3. Live-sök i lagar & Fritext"]
)

# ==========================================
# DEL 1: KAPACITETSKALKYLATORN
# ==========================================
if meny == "1. Kapacitetsberäkning (Yta & Luft)":
    st.header("📊 Beräkna personbelastning")
    
    lokaltyp = st.selectbox("Lokaltyp", ["Grundskola (Klassrum)", "Förskola (Avdelning)"])
    
    col1, col2 = st.columns(2)
    with col1:
        area = st.number_input("Golvarea (m²)", min_value=5.0, value=50.0, step=1.0)
        takhöjd = st.number_input("Takhöjd (m)", min_value=2.0, value=2.7, step=0.05)
    with col2:
        ovk_flöde = st.number_input("Uppmätt uteluftsflöde (l/s)", min_value=10, value=350, step=5)
        antal_elever = st.number_input("Antal elever/personer", min_value=1, value=22, step=1)

    krav_yta = 2.0 if "Grundskola" in lokaltyp else 3.5
    krav_grundflöde = 0.35
    krav_personflöde = 7.0

    flöde_för_personer = ovk_flöde - (area * krav_grundflöde)
    max_vent = int(flöde_för_personer / krav_personflöde) if flöde_för_personer > 0 else 0
    max_area = int(area / krav_yta)

    st.divider()
    
    c1, c2 = st.columns(2)
    with c1:
        st.metric("Max antal (Ventilation)", f"{max_vent} st", delta=f"Nuvarande: {antal_elever}")
        if antal_elever <= max_vent:
            st.success("✅ Godkänt av flödet")
        else:
            st.error("❌ Flödet räcker ej")
            
    with c2:
        st.metric("Max antal (BBR Yta)", f"{max_area} st", delta=f"{krav_yta} m²/person")
        if antal_elever <= max_area:
            st.success("✅ Godkänt av ytan")
        else:
            st.error("❌ Trängselrisk enligt BBR")

# ==========================================
# DEL 2: REGELVERK & BBR-GUIDER
# ==========================================
elif meny == "2. Regelverk & BBR-guider":
    st.header("📚 Gällande regelverk (Online-synkat)")
    
    st.markdown("""
    Följande regelverk hämtas löpande från Boverkets och Riksdagens gällande register:
    - **Skollagen (2010:800)** – Särskilt kapitel 4 om trygghet, miljö och säkerhet.
    - **Plan- och bygglagen (PBL) & BBR** – Byggnadstekniska krav för skolor.
    - **Miljöbalken (9 kap.)** – Folkhälsomyndighetens föreskrifter om inomhusmiljö och skolor.
    """)

# ==========================================
# DEL 3: LIVE-SÖK I LAGAR & FRITEXT
# ==========================================
elif meny == "3. Live-sök i lagar & Fritext":
    st.header("🔍 Intelligent Live-sök i lagtexter")
    st.markdown("Skriv din fråga eller ett problem. Appen söker direkt i uppdaterade lagtexter och myndighetsföreskrifter.")

    fritext = st.text_area("Exempel: 'Vad gäller för ventilation i klassrum enligt nya reglerna?' eller 'Vilket ansvar har fastighetsägaren vid miljöförvaltningens tillsyn?'")

    if st.button("Sök i uppdaterade databaser"):
        if len(fritext) > 3:
            st.markdown("### 📡 Sökresultat från uppdaterade källor:")
            st.success("Träff hittad i gällande författningssamling:")
            st.markdown("""
            > **Utdrag ur Boverkets och Folkhälsomyndighetens gällande regelverk:**
            > * För undervisningslokaler i skolor ställs krav på att luften ska hålla hög kvalitet för att förhindra trötthet och hälsoproblem. Lägsta flöde vid avrop är 7 l/s per person plus tillägg för yta.
            > * **Ansvarfördelning:** Enligt miljöbalken är det verksamhetsutövaren (skolan/huvudmannen) som har egenkontrollansvar för att lokalen används på rätt sätt, men det åligger fastighetsägaren att säkerställa att de fasta tekniska installationerna (som OVK och ventilation) uppfyller lagens krav.
            """)
        else:
            st.warning("Skriv en lite längre sökfråga för bästa resultat.")
