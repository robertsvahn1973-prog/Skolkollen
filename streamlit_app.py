import streamlit as st

st.set_page_config(
    page_title="Skol- och Fastighetskoll Pro",
    page_icon="🏫",
    layout="centered"
)

st.title("🏫 Skol- & Fastighetskoll Pro")
st.markdown("Din mobila expertassistent för exakta lagrum, paragrafer, BBR, Jordabalken, brandskydd och skolmiljö.")

meny = st.radio(
    "Välj funktion:", 
    [
        "1. Kapacitet & Vent-koll (BBR)", 
        "2. Intelligent Fritextsök & Djuptolk (Med lagrum & paragrafer)"
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
elif meny == "2. Intelligent Fritextsök & Djuptolk (Med lagrum & paragrafer)":
    st.header("🔍 Intelligent Fritextsök & Djuptolk")
    st.markdown("Ställ vilken fråga som helst. Systemet plockar fram rätt myndighet, lag, kapitel och paragraf:")

    fritext = st.text_area("Din fråga (t.ex. 'vem ansvarar för skador enligt jordabalken', 'hur många i brandcell' eller 'krav på slöjdsal'):")

    if st.button("Utför djupsökning och analys"):
        if len(fritext) > 2:
            s_text = fritext.lower()
            st.success("Djupsökning klar! Exakta lagrum och myndighetskrav:")

            matchningar = []

            # 1. Fastighetsjuridik & Jordabalken (JB)
            if any(w in s_text for w in ["jordabalken", "jb", "hyra", "lokalhyra", "hyresgäst", "hyresvärd", "underhållsansvar", "avtal", "kontrakt", "skada"]):
                matchningar.append({
                    "lagrum": "Jordabalken (1970:994) – 12 kap. (Hyreslagen)",
                    "detaljer": "• **Hyresvärdens ansvar:** 12 kap. 9 § ställer krav på att hyresvärden ska tillhandahålla lokalen i fullt brukbart skick för det avsedda ändamålet och hålla den i detta skick under hyrestiden.\n• **Hyresgästens vårdplikt:** 12 kap. 24 § stipulerar att hyresgäst väl ska vårdas lokalen och ersätta skador som uppkommit genom vårdslöshet eller försummelse.\n• **Fel i lokal:** 12 kap. 11 § ger rätt till skälig nedsättning av hyra om lokalen är bristfällig."
                })

            # 2. Brandcell & Personantal (BBR & MSO)
            if any(w in s_text for w in ["brandcell", "hur många", "personantal", "antal personer", "kapacitet"]):
                matchningar.append({
                    "lagrum": "Boverkets Byggregler (BBR) & Lagen om skydd mot olyckor (2003:778)",
                    "detaljer": "• **Personantal & Utrymning:** Enligt BBR styrs max antal personer i en brandcell av utrymningsvägarnas dimensionering.\n• **1 utrymningsväg:** Max **50 personer** (förutsatt kort och säker utrymningsväg).\n• **2 oberoende utrymningsvägar:** Tillåter upp till **150+ personer** beroende på dörrarnas fria modulbredd."
                })

            # 3. Slöjd (Trä, metall, textil)
            if any(w in s_text for w in ["slöjd", "träslöjd", "metallslöjd", "textilslöjd"]):
                matchningar.append({
                    "lagrum": "Skollagen (2010:800) 2 kap. 36 § & Arbetsmiljöverkets föreskrifter (AFS)",
                    "detaljer": "• **Skollagen:** Lokaler för utbildningen ska vara ändamålsenliga.\n• **Arbetsmiljö och Säkerhet:** Kräver godkänd processventilation/utsug för damm och ångor (AFS), centrala nödstopp för maskiner, samt flamskyddade ytskikt och ögonspolning."
                })

            # 4. NO / Kemi
            if any(w in s_text for w in ["kemi", "no", "laborator", "dragskåp", "kemikalie"]):
                matchningar.append({
                    "lagrum": "Miljöbalken (1998:808) 9 kap. & MSB (Lag om brandfarliga och explosiva varor)",
                    "detaljer": "• **Hälsoskydd & Utrustning:** Krav på typgodkända dragskåp, ventilerade kemikalieskåp och golvbrunnar med slam-/syraavskiljare.\n• **Tillsyn:** Miljöförvaltningen utövar tillsyn över kemikaliehantering och ventilation för att förhindra olägenhet för människors hälsa."
                })

            # 5. Idrott
            if any(w in s_text for w in ["idrott", "gymnastik", "hall", "omklädning"]):
                matchningar.append({
                    "lagrum": "Skollagen (2010:800) & Boverkets Byggregler (BBR)",
                    "detaljer": "• **Utformning:** Krav på tillräcklig fri höjd (ofta minst 7 meter för bollsport), slagtåliga material samt ventilationssystem dimensionerade för hög fysisk aktivitet.\n• **Hygien:** Våtrumsklassade omklädnings- och duschutrymmen."
                })

            # 6. Ljud och Decibel på dörrar
            if any(w in s_text for w in ["decibel", "db", "ljud", "ljudklass", "buller", "akustik", "dörr"]):
                matchningar.append({
                    "lagrum": "Boverkets Byggregler (BBR) & Miljöbalken (1998:808) 9 kap.",
                    "detaljer": "• **BBR Ljudkrav:** Klassrumsdörrar har normalt krav på ljudreduktion **Rw 35 dB** (eller Rw 40 dB mot högljudda utrymmen) enligt standard SS 25267.\n• **Miljöbalken:** Riktvärden för ekvivalent ljudnivå i klassrum får maximalt uppgå till 30–35 dB(A) under pågående undervisning."
                })

            # 7. Takhöjd
            if any(w in s_text for w in ["takhöjd", "rumshöjd", "höjd", "yta", "m2", "volym"]):
                matchningar.append({
                    "lagrum": "Boverkets Byggregler (BBR) – Avsnitt om rumshöjd",
                    "detaljer": "• **Minsta höjd:** För vistelserum i skolor rekommenderas en fri rumshöjd på minst **2,4 till 2,7 meter** för att säkerställa tillräcklig luftvolym per person och förhindra dåligt inneklimat."
                })

            # 8. Ventilation & OVK
            if any(w in s_text for w in ["luft", "ventilation", "koldioxid", "flöde", "ovk", "l/s"]):
                matchningar.append({
                    "lagrum": "Plan- och bygglagen (2010:900) 8 kap. & BBR / OVK-normer",
                    "detaljer": "• **Flödeskrav:** Lägsta uteluftsflöde om **0,35 l/s per m²** golvarea plus tillägg med **7,0 l/s per person**.\n• **Intervall:** OVK (Obligatorisk ventilationskontroll) ska utföras regelbundet (ofta vart 3:e år för FTX-system i skolor)."
                })

            # 9. Brandskydd generellt
            if any(w in s_text for w in ["brand", "brandskydd", "utrymning", "branddörr", "sba"]):
                matchningar.append({
                    "lagrum": "Lagen om skydd mot olyckor (2003:778) & BBR",
                    "detaljer": "• **Byggnadstekniskt:** Krav på brandklassade dörrar (**EI30 / EI60**) och brandtätning.\n• **Operativt:** Fastighetsägare och verksamhetsutövare är skyldiga att bedriva Systematiskt brandskyddsarbete (SBA) samt hålla utrymningsvägar fria."
                })

            # 10. Skola / Skollag
            if any(w in s_text for w in ["skollag", "skolverket", "trygghet", "elev", "förskola", "skola", "lokal"]):
                matchningar.append({
                    "lagrum": "Skollagen (2010:800) – 4 kap. och 2 kap. 36 §",
                    "detaljer": "• **Ändamålsenlighet:** Huvudmannen är skyldig att se till att skollokalerna är ändamålsenliga för verksamheten och erbjuder en trygg, säker miljö fri från kränkningar."
                })

            # Fallback
            if not matchningar:
                matchningar.append({
                    "lagrum": "Allmän fastighetsförvaltning & Gällande rätt",
                    "detaljer": f"Frågan (*\"{fritext}\"*) berör fastighetsförvaltning. För fullständig juridisk prövning, kontrollera tillämplig lagtext i **Jordabalken**, **Plan- och bygglagen (PBL)** eller föreskrifter från Boverket och MSB."
                })

            for m in matchningar:
                with st.expander(f"📌 {m['lagrum']}", expanded=True):
                    st.markdown(f"**Exakt regeltolkning & Paragrafhänvisning:**\n\n{m['detaljer']}")
                    st.markdown("---")
                    st.markdown("*Officiell källhänvisning:* Sök alltid på angivet lagrum i Svensk författningssamling (SFS) eller Boverkets handböcker.")

        else:
            st.warning("Skriv en lite fylligare fråga.")
