 import unicodedata
from pathlib import Path

import streamlit as st
from PIL import Image

ICON = Image.open(Path(__file__).parent / "icon.png")

st.set_page_config(page_title="Madeleine Digital", page_icon=ICON, layout="centered")

# ---------- Thème blanc & rose ----------
st.markdown(
    """
    <style>
    .stApp { background: linear-gradient(180deg, #FFFFFF 0%, #FFF0F5 100%); }
    h1, h2, h3 { color: #D6336C !important; }
    .card {
        background: #FFFFFF; border: 2px solid #F8BBD0; border-radius: 20px;
        padding: 1.2rem 1.5rem; margin: 1rem 0;
        box-shadow: 0 4px 14px rgba(231, 84, 128, 0.15);
    }
    .big { font-size: 3.5rem; font-weight: 800; color: #E75480; text-align: center; line-height: 1; }
    .label { text-align: center; color: #A0617A; font-size: .9rem; }
    .stButton > button {
        background: #E75480; color: white; border: none; border-radius: 999px;
        padding: .5rem 1.6rem; font-weight: 600;
    }
    .stButton > button:hover { background: #D6336C; color: white; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Numérologie (table pythagoricienne) ----------
LETTRES = {c: (i % 9) + 1 for i, c in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ")}
VOYELLES = set("AEIOUY")

SIGNIFICATIONS = {
    1: ("Le Leader", "Indépendant(e), ambitieux(se), pionnier(ère). Tu aimes ouvrir la voie."),
    2: ("Le Diplomate", "Sensible, coopératif(ve), à l'écoute. Tu crées l'harmonie autour de toi."),
    3: ("Le Créatif", "Joyeux(se), expressif(ve), sociable. L'artiste du groupe."),
    4: ("Le Bâtisseur", "Fiable, organisé(e), persévérant(e). Tu construis du solide."),
    5: ("L'Aventurier", "Curieux(se), libre, adaptable. Le changement te nourrit."),
    6: ("Le Protecteur", "Aimant(e), responsable, dévoué(e). Tu prends soin des autres."),
    7: ("Le Sage", "Analytique, intuitif(ve), spirituel(le). Tu cherches le sens profond."),
    8: ("Le Stratège", "Puissant(e), déterminé(e), tourné(e) vers la réussite."),
    9: ("L'Humaniste", "Généreux(se), idéaliste, compatissant(e). Tu veux rendre le monde meilleur."),
    11: ("Le Visionnaire (nombre maître)", "Intuition forte, inspiration, idéal élevé."),
    22: ("Le Grand Bâtisseur (nombre maître)", "Capable de transformer de grands rêves en réalité."),
    33: ("Le Guide (nombre maître)", "Dévouement, amour inconditionnel, enseignement."),
}


def normaliser(texte: str) -> str:
    texte = unicodedata.normalize("NFD", texte.upper())
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    return "".join(c for c in texte if c in LETTRES)


def reduire(n: int) -> int:
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(d) for d in str(n))
    return n


def analyser(prenom: str):
    p = normaliser(prenom)
    total = sum(LETTRES[c] for c in p)
    ame = sum(LETTRES[c] for c in p if c in VOYELLES)
    perso = total - ame
    return p, total, reduire(total), reduire(ame), reduire(perso)


# ---------- Interface ----------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(ICON, use_container_width=True)

st.title("🌸 Madeleine Digital")
st.caption("Découvre la valeur cachée de ton prénom.")

prenom = st.text_input("Entre un prénom", placeholder="Ex : Madeleine")
go = st.button("Révéler la valeur ✨")

if go or prenom:
    if not normaliser(prenom):
        st.info("Écris un prénom pour commencer 💕")
    else:
        lettres, total, valeur, ame, perso = analyser(prenom)
        titre, texte = SIGNIFICATIONS[valeur]

        st.markdown(
            f"""
            <div class="card">
              <div class="label">Valeur du prénom « {prenom.strip().title()} »</div>
              <div class="big">{valeur}</div>
              <h3 style="text-align:center">{titre}</h3>
              <p style="text-align:center">{texte}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        c1, c2, c3 = st.columns(3)
        c1.metric("Somme brute", total)
        c2.metric("💗 Âme (voyelles)", ame)
        c3.metric("🎀 Image (consonnes)", perso)

        with st.expander("Voir le détail du calcul"):
            st.write(" + ".join(f"{c}={LETTRES[c]}" for c in lettres) + f" = **{total}** → **{valeur}**")
            st.write(f"**Âme {ame}** : {SIGNIFICATIONS[ame][0]}")
            st.write(f"**Image {perso}** : {SIGNIFICATIONS[perso][0]}")

st.markdown("---")
st.caption("Madeleine Digital · À but ludique, la numérologie n'a pas de valeur scientifique 💕")

