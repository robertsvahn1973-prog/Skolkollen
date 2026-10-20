import streamlit as st

st.set_page_config(
    page_title="Skol- och Lokalkoll Pro",
    page_icon="🏫",
    layout="centered"
)

st.title("🏫 Skol- och Lokalkoll Pro")
st.markdown("Din mobila assistent för kapacitetsberäkning, BBR och intelligent djuptolkning av regelverk för skolmiljö.")

meny = st.radio(
    "Välj funktion:", 
    [
        "1. Kapacitet & Vent-koll (BBR)", 
        "2. Intelligent Fritextsök & Djuptolk"
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
# DEL 2: INTELLIGENT FRITEXTSÖK & DJUPTOLK
# ==========================================
elif meny == "2. Intelligent Fritextsök & Djuptolk":
    st.header("🔍 Intelligent Fritextsök & Djuptolk")
    st.markdown("Ställ en specifik fråga om slöjd, NO/kemi, idrott, dörrar, decibel, takhöjd, ventilation eller brand. Systemet djupsöker mot Skolverket, Boverket, MSB och Miljöförvaltningen:")

    fritext = st.text_area("Din fråga (t.ex. 'vad ska slöjd i en skola innefatta' eller 'krav på kemisal'):")

    if st.button("Utför djupsökning och analys"):
        if len(fritext) > 2:
            s_text = fritext.lower()
            st.success("Djupsökning klar! Matchade myndigheter och krav:")

            matchningar = []

            # Slöjd (Trä, metall, textil) -> Skolverket & Arbetsmiljöverket & BBR
            if any(w in s_text for w in ["slöjd", "träslöjd", "metallslöjd", "textilslöjd"]):
                matchningar.append({
                    "myndighet": "Skolverket (Läroplan / Skollagen) & Arbetsmiljöverket / Boverket",
                    "detaljer": "Enligt Skolverkets kursplaner ska slöjdundervisningen erbjuda ändamålsenliga lokaler för både trä-, metall- och textilslöjd. Fastighets- och arbetsmiljökrav (AFS) ställer krav på: **Utsug och ventilation** för damm och ångor (särskilt vid maskiner och svets/lödning), **säkerhetsavstängning** (nödstopp för maskiner), ögonspolning, samt flamskyddade material och robusta ytskikt som tål tuff miljö och buller."
                })

            # NO / Kemi -> Skolverket & Miljöförvaltningen & MSB
            if any(w in s_text for w in ["kemi", "no", "laborator", "dragskåp", "kemikalie"]):
                matchningar.append({
                    "myndighet": "Skolverket, Miljöförvaltningen & MSB (Räddningstjänsten)",
                    "detaljer": "NO- och kemisalar ställer höga krav på lokalens utformning: **Dragskåp** med godkänd kontroll, särskilda kemikalieskåp med ventilation, flamsäkra ytor, golvbrunnar med slam-/syraavskiljare, samt snabbdusch och ögonspolning. Miljöförvaltningen och räddningstjänsten utövar tillsyn över förvaring av brandfarlig och hälsofarlig vara."
                })

            # Idrott -> Skolverket & BBR
            if any(w in s_text for w in ["idrott", "gymnastik", "hall", "omklädning"]):
                matchningar.append({
                    "myndighet": "Skolverket & Boverkets Byggregler (BBR)",
                    "detaljer": "Idrottshallar regleras utifrån Skolverkets krav på idrott och hälsa samt BBR för stora samlingslokaler. Viktiga parametrar är **takhöjd** (ofta minst 7 meter för bollsport), slagtåliga väggar, korrekt belysning, tillräcklig ventilation för ansträngande fysisk aktivitet samt funktionella omklädningsrum med våtrumskrav och god kapacitet på duschar."
                })

            # Ljud och Decibel på dörrar -> BBR & Miljöbalken
            if any(w in s_text for w in ["decibel", "db", "ljud", "ljudklass", "buller", "akustik", "dörr"]):
                matchningar.append({
                    "myndighet": "Boverket (BBR) & Miljöförvaltningen (Miljöbalken)",
                    "detaljer": "För dörrar till klassrum och undervisningslokaler ställs krav på ljudreduktion för att uppfylla BBR:s ljudklasskrav (normalt ljudklass B eller C). Klassrumsdörrar har typiskt krav på ljudreduktion **Rw 35 dB** (eller upp till Rw 40 dB mot högljudda utrymmen). Miljöbalken kräver att ekvivalenta ljudnivåer i klassrum inte överskrider riktvärden (max 30-35 dB(A))."
                })

            # Takhöjd -> Boverket
            if any(w in s_text for w in ["takhöjd", "rumshöjd", "höjd", "yta", "m2", "volym"]):
                matchningar.append({
                    "myndighet": "Boverkets Byggregler (BBR) / Boverket",
                    "detaljer": "Reglerar rumshöjder i skolor och förskolor. För vistelserum i skolor rekommenderas en fri takhöjd på minst **2,4 till 2,7 meter** (och betydligt högre för idrottshallar) för att säkerställa god luftvolym och rumsmiljö."
                })

            # Ventilation -> BBR & Miljöförvaltningen
            if any(w in s_text for w in ["luft", "ventilation", "koldioxid", "flöde", "ovk", "l/s"]):
                matchningar.append({
                    "myndighet": "Boverket (BBR) & Miljöförvaltningen (Miljöbalken 9 kap.)",
                    "detaljer": "Kräver lägsta uteluftsflöde om **0,35 l/s per m²** golvarea plus tillägg med **7,0 l/s per person** i standardlokaler (särskilda flöden kan krävas i slöjd och kemi)."
                })

            # Brandskydd -> MSB & Räddningstjänsten
            if any(w in s_text for w in ["brand", "brandskydd", "utrymning", "brandcell", "branddörr", "sba"]):
                matchningar.append({
                    "myndighet": "MSB & Lokala Räddningstjänsten (Lagen om skydd mot olyckor)",
                    "detaljer": "Utöver BBR:s byggnadstekniska brandkrav (t.ex. brandklassade dörrar som **EI30 / EI60**) ställer Räddningstjänsten operativa krav på utrymningsvägar, fria bredder och systematiskt brandskyddsarbete (SBA)."
                })

            # Skola / Trygghet / Generellt -> Skolverket & Skollagen
            if any(w in s_text for w in ["skollag", "skolverket", "trygghet", "elev", "förskola", "skola", "lokal"]):
                matchningar.append({
                    "myndighet": "Skolverket (Skollagen 2010:800)",
                    "detaljer": "Ställer övergripande krav på att skollokaler är ändamålsenliga för verksamheten, att läroplanens praktiska ämnen kan genomföras fullt ut, samt att miljön är trygg och säker för elever och personal."
                })

            if not matchningar:
                matchningar.append({
                    "myndighet": "Allmän fastighetsförvaltning & Skolverket",
                    "detaljer": "Ställ en mer specifik fråga (t.ex. om slöjd, kemisal, idrott, dörrar, flöden eller takhöjd) för att få exakta regelspecifikationer."
                })

            for m in matchningar:
                with st.expander(f"📌 {m['myndighet']}", expanded=True):
                    st.markdown(f"**Djupsökning & Gällande krav:**\n\n{m['detaljer']}")
                    st.markdown("---")
                    st.markdown("*Online-hänvisning:* Verifiera alltid mot Skolverkets läroplaner, Boverket, MSB eller kommunens miljöförvaltning.")

        else:
            st.warning("Skriv en lite fylligare fråga.")
