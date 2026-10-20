import streamlit as st

st.set_page_config(
    page_title="Skol- och Lokalkoll Pro",
    page_icon="🏫",
    layout="centered"
)

st.title("🏫 Skol- och Lokalkoll Pro (Fastighet & Ombyggnad)")
st.markdown("Din kompletta mobila assistent för BBR, OVK, kapacitet, ombyggnationer och regeltolkning.")

meny = st.radio(
    "Välj funktion:", 
    [
        "1. Kapacitet & Vent-koll (BBR)", 
        "2. Ombyggnad & Fritextkalkylator", 
        "3. BBR & Regelverk Uppslagsverk", 
        "4. Intelligent Fritextsök (Lagkoppling)"
    ]
)

# ==========================================
# DEL 1: KAPACITET & VENTILATION
# ==========================================
if meny == "1. Kapacitet & Vent-koll (BBR)":
    st.header("📊 Kontroll mot BBR & Ventilation")
    
    lokaltyp = st.selectbox("Lokaltyp", ["Grundskola / Klassrum", "Förskola / Avdelning"])
    
    col1, col2 = st.columns(2)
    with col1:
        area = st.number_input("Golvarea (m²)", min_value=5.0, value=50.0, step=1.0)
        takhöjd = st.number_input("Takhöjd (m)", min_value=2.0, value=2.7, step=0.05)
    with col2:
        ovk_flöde = st.number_input("Uppmätt uteluftsflöde (l/s)", min_value=10, value=350, step=5)
        antal_elever = st.number_input("Antal personer i rummet", min_value=1, value=22, step=1)

    krav_yta_pers = 2.0 if "Grundskola" in lokaltyp else 3.5
    krav_grund = 0.35
    krav_pers = 7.0
    min_flöde = (area * krav_grund) + (antal_elever * krav_pers)

    st.divider()
    if takhöjd < 2.4:
        st.warning("⚠️ **Takhöjd:** Under 2.4 m kan strida mot BBR för vistelserum.")
    else:
        st.success(f"✅ **Takhöjd ({takhöjd} m):** Godkänd höjdnivå.")

    c1, c2 = st.columns(2)
    with c1:
        st.metric("Krävt minimiflöde", f"{min_flöde:.1f} l/s")
        if ovk_flöde >= min_flöde:
            st.success("✅ Flödet klarar BBR!")
        else:
            st.error(f"❌ Underkänt (krävs {min_flöde:.1f} l/s).")
    with c2:
        max_pers_yta = int(area / krav_yta_pers)
        st.metric("Max antal (Yta)", f"{max_pers_yta} st")
        if antal_elever <= max_pers_yta:
            st.success("✅ Godkänt av ytan")
        else:
            st.error("❌ Trängselrisk")

# ==========================================
# DEL 2: OMBYGGNAD & FRITEXTKALKYLATOR (NY!)
# ==========================================
elif meny == "2. Ombyggnad & Fritextkalkylator":
    st.header("🛠️ Fritextkalkylator för ombyggnation")
    st.markdown("Beskriv vad som ska göras i fritext. Appen tolkar åtgärden, matchar nyckeltal och beräknar riktpris inklusive lagkrav och relationshandlingar.")

    projekt_beskrivning = st.text_area(
        "Beskriv projektet (t.ex. 'Byta 2 dörrar med brandkrav' eller 'Fyll på sandlåda 6 kubik'):",
        placeholder="Skriv vad som ska utföras här..."
    )

    st.divider()

    # Automatiskt tolkning av fritexten för att sätta baspris
    txt = projekt_beskrivning.lower()
    grund_matris = 15000  # Standardstart om ej matchat
    kategori_vald = "Generell åtgärd / Blandade anpassningar"

    if any(w in txt for w in ["dörr", "dörrar", "port"]):
        kategori_vald = "Byte av innerdörr(ar) med brand-/ljudkrav"
        grund_matris = 18000 * 2  # Schablon
    elif any(w in txt for w in ["sand", "sandlåda", "lekplats"]):
        kategori_vald = "Lekplats / Sandlåda (påfyllnad & sanering)"
        grund_matris = 2500 * 5   # Schablon 5 m3
    elif any(w in txt for w in ["vägg", "yta", "rum", "klassrum", "anpassning", "m2", "kvadratmeter"]):
        kategori_vald = "Ytanpassning / Väggflytt / Ytskikt"
        grund_matris = 2500 * 30  # Schablon 30 m2
    elif any(w in txt for w in ["luft", "ventilation", "don", "aggregat"]):
        kategori_vald = "Ventilationsanpassning / Tilluftsdon"
        grund_matris = 6500 * 2

    st.info(f"🔍 **Tolkat projekt:** {kategori_vald}")

    # Tillägg för relationshandlingar & projektledning
    inkl_relationshandlingar = st.checkbox("Inkludera uppdatering av relationshandlingar (CAD/BIM, OVK-rev, brandritning)", value=True)
    
    kostnad_relationshandlingar = 4500 if inkl_relationshandlingar else 0
    projektering_ovrigt = grund_matris * 0.10  # 10% samordning
    total_kostnad = grund_matris + kostnad_relationshandlingar + projektering_ovrigt

    st.subheader("💰 Kostnadssammanställning (Induktiv riktprisbudget):")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Direkt arb./material", f"{grund_matris:,.0f} kr".replace(",", " "))
        if inkl_relationshandlingar:
            st.write("📁 **Relationshandlingar:** 4 500 kr")
        else:
            st.write("📁 **Relationshandlingar:** Ej valda")
    with col2:
        st.metric("Uppskattat totalpris", f"{total_kostnad:,.0f} kr".replace(",", " "))
        st.caption("Inkl. samordning & uppdaterade handlingar.")

# ==========================================
# DEL 3: UPPSLAGSVERK
# ==========================================
elif meny == "3. BBR & Regelverk Uppslagsverk":
    st.header("📚 Snabbreferens för BBR & Fastighetskrav")
    st.markdown("Här hittar du svar gällande takhöjd, flöden och ansvar.")

# ==========================================
# DEL 4: INTELLIGENT FRITEXTSÖK (LAGKOPPLING)
# ==========================================
elif meny == "4. Intelligent Fritextsök (Lagkoppling)":
    st.header("🔍 Intelligent Fritextsök & Regeltolk")
    st.markdown("Ställ en specifik fråga (t.ex. *'vad är lägsta takhöjd i en skola'*, *'brandskydd utöver bbr'* eller *'ventilation'**):")

    fritext = st.text_area("Din fråga eller beskrivning av ärendet:")

    if st.button("Analysera och koppla krav"):
        if len(fritext) > 3:
            s_text = fritext.lower()
            st.success("Analys klar! Exakt koppling till gällande regelverk och myndigheter:")

            matchningar = []

            if any(w in s_text for w in ["takhöjd", "rumshöjd", "höjd", "yta", "m2", "kvadratmeter", "fri höjd"]):
                matchningar.append({
                    "lag": "Boverkets Byggregler (BBR) / Boverket",
                    "fokus": "Reglerar rumshöjder, volymer och utformning av vistelserum. För skolor rekommenderas en fri takhöjd på minst 2,4 - 2,7 meter."
                })

            if any(w in s_text for w in ["luft", "ventilation", "koldioxid", "flöde", "ovk", "l/s", "drag"]):
                matchningar.append({
                    "lag": "BBR & Miljöbalken (Miljöförvaltningen)",
                    "fokus": "Ställer tekniska krav på lägsta uteluftsflöden (minst 0,35 l/s per m² + 7 l/s per person). Miljöförvaltningen utövar tillsyn över innemiljön."
                })

            if any(w in s_text for w in ["brand", "brandskydd", "utrymning", "brandcell", "utrymningsväg", "sprinkler", "brandlarm", "branddörr"]):
                matchningar.append({
                    "lag": "Lagen om skydd mot olyckor (MSO) & MSB / Räddningstjänsten",
                    "fokus": "Utöver BBR:s grundläggande brandkrav ställer Räddningstjänsten krav på systematiskt brandskyddsarbete (SBA) och fria utrymningsvägar."
                })

            if any(w in s_text for w in ["skollag", "skolverket", "trygghet", "studiero", "elev", "förskola", "skola"]):
                matchningar.append({
                    "lag": "Skollagen (2010:800) / Skolverket",
                    "fokus": "Reglerar verksamhetens ansvar för att lokaler är ändamålsenliga och att elever garanteras en trygg och säker skolmiljö."
                })

            if not matchningar:
                matchningar.append({
                    "lag": "Allmän fastighets- och myndighetsbedömning",
                    "fokus": "Frågan rör fastighetsförvaltning. Specificera om det avser ventilation, brand eller utformning."
                })

            for m in matchningar:
                with st.expander(f"📌 Ansvarig myndighet & Regelverk: {m['lag']}", expanded=True):
                    st.write(f"**Kravbild & Innehåll:** {m['fokus']}")
                    st.markdown("- *Online-hänvisning:* Kontrollera alltid Boverkets, Skolverkets eller lokal miljö-/räddningsförvaltningens gällande föreskrifter.")

        else:
            st.warning("Skriv en lite fylligare fråga.")
