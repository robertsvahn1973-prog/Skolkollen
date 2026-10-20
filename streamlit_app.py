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
        "2. Ombyggnad & Nyckeltal (Kalkylator)", 
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
# DEL 2: OMBYGGNAD & NYCKELTAL
# ==========================================
elif meny == "2. Ombyggnad & Nyckeltal (Kalkylator)":
    st.header("🛠️ Kalkylator för ombyggnation & åtgärder")
    st.markdown("Beräkna riktpriser inklusive lagkrav, montage och uppdatering av relationshandlingar.")

    atgard_typ = st.selectbox(
        "Välj typ av åtgärd / projekt:",
        [
            "Byte av innerdörr (med brand-/ljudkrav)",
            "Påfyllnad & sanering av lekplatssand (Sandlåda)",
            "Mindre ytanpassning / Väggflytt (per m²)",
            "Installera tilluftsdon / Vent-anpassning"
        ]
    )

    st.divider()

    if "innerdörr" in atgard_typ.lower():
        antal_dorrar = st.number_input("Antal dörrar som ska bytas", min_value=1, value=1, step=1)
        brandklass = st.checkbox("Krav på brandklass (EI30 / EI60) & ljudklass", value=True)
        styckpris = 18000 if brandklass else 12000
        grund_matris = antal_dorrar * styckpris
        
    elif "sandlåda" in atgard_typ.lower():
        volym_m3 = st.number_input("Uppskattad volym lekplatssand / påfyllnad (m³)", min_value=1.0, value=5.0, step=0.5)
        styckpris = 2500 
        grund_matris = volym_m3 * styckpris
        
    elif "ytanpassning" in atgard_typ.lower():
        ombyggnad_yta = st.number_input("Berörd golvarea för anpassningen (m²)", min_value=5.0, value=30.0, step=5.0)
        styckpris = 2500 
        grund_matris = ombyggnad_yta * styckpris
        
    else:
        antal_don = st.number_input("Antal nya/flyttade don", min_value=1, value=2, step=1)
        styckpris = 6500 
        grund_matris = antal_don * styckpris

    inkl_relationshandlingar = st.checkbox("Inkludera uppdatering av relationshandlingar (CAD/BIM, OVK-rev, brandritning)", value=True)
    kostnad_relationshandlingar = 4500 if inkl_relationshandlingar else 0
    projektering_ovrigt = grund_matris * 0.10 
    
    total_kostnad = grund_matris + kostnad_relationshandlingar + projektering_ovrigt

    st.subheader("💰 Kostnadssammanställning (Induktiv riktprisbudget):")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Direkt arb./material", f"{grund_matris:,.0f} kr".replace(",", " "))
        if inkl_relationshandlingar:
            st.write("📁 **Relationshandlingar:** 4 500 kr")
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
    st.markdown("Skriv en egen fråga (t.ex. *'vilka krav ställs på ventilationen i klassrum'* eller *'vad gäller för buller och innemiljö'*):")

    fritext = st.text_area("Din fråga eller beskrivning av ärendet:")

    if st.button("Analysera och koppla krav"):
        if len(fritext) > 3:
            s_text = fritext.lower()
            st.success("Analys klar! Koppling till gällande lagar och myndigheter:")

            # Regelmotor som matchar fritext mot BBR, Miljöbalken och Skollagen
            matchningar = []

            if any(ord in s_text for "luft", "ventilation", "koldioxid", "flöde", "ovk", "takhöjd", "volym", "rumshöjd"):
                matchningar.append({
                    "lag": "Boverkets Byggregler (BBR)",
                    "fokus": "Byggnadstekniska krav på innemiljö, uteluftsflöden (minst 0,35 l/s m² + 7 l/s per person) och rumshöjder."
                })

            if any(ord in s_text for "miljö", "hälsa", "buller", "ljud", "temperatur", "drag", "mögel", "fukt", "allergi", "städa", "renlighet"):
                matchningar.append({
                    "lag": "Miljöbalken (9 kap. - Hälsoskydd)",
                    "fokus": "Tillsyneras av Miljöförvaltningen. Kräver att skollokaler inte medför olägenhet för människors hälsa (ljudnivåer, termiskt anpassat inneklimat och ventilation)."
                })

            if any(ord in s_text for "trygg", "säkerhet", "kränkning", "ansvar", "skolmiljö", "elev", "förskola"):
                matchningar.append({
                    "lag": "Skollagen (2010:800 - 4 kap.)",
                    "fokus": "Ställer krav på att utbildningen bedrivs i en trygg miljö och att lokaler är ändamålsenliga för verksamheten."
                })

            # Om inga specifika nyckelord hittas, ge en generell heltäckande träff
            if not matchningar:
                matchningar.append({
                    "lag": "Samlad bedömning (BBR, Miljöbalken & Skollagen)",
                    "fokus": "Ärendet berör både fastighetens tekniska utformning (BBR) och verksamhetens egenkontroll (Miljöförvaltningen och Skollagen)."
                })

            for m in matchningar:
                with st.expander(f"📌 Kopplat regelverk: {m['lag']}", expanded=True):
                    st.write(f"**Innehåll & Krav:** {m['fokus']}")
                    st.markdown("- *Rekommendation:* Kontrollera alltid mot fastighetens senaste OVK-protokoll och samråd med miljöförvaltningen vid större lokaländringar.")

        else:
            st.warning("Skriv en lite fylligare fråga så att systemet kan göra en korrekt regeltolkning.")
