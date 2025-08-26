# Streamlit App: Pendeteksi Rumor Right Issue & Aksi Korporasi (IDX)
# ---------------------------------------------------------------
# Fitur utama:
# - Mengumpulkan berita dari Google News (RSS) berbasis kata kunci Indonesia
# - Menyaring berdasarkan rentang tanggal & kategori aksi korporasi
# - Ekstraksi kandidat ticker emiten (3–4 huruf, contoh: BBCA, TLKM, CUAN)
# - Skor kecurigaan per emiten + daftar bukti (tautan berita)
# - Tampilan ringkas (tabel) + detail per emiten
# - Ekspor hasil ke CSV
#
# Catatan:
# - Ini *detektor rumor* (bukan konfirmasi resmi). Selalu verifikasi ke sumber resmi (IDX/OJK/Emiten).
# - Akses internet diperlukan ketika aplikasi berjalan (untuk mengambil RSS Google News dan artikel).
# - Instal dependensi di environment Anda: pip install streamlit feedparser pandas requests beautifulsoup4 python-dateutil tldextract
#
# Menjalankan:
#   streamlit run streamlit_rumor_corporate_action_idx.py

import re
import io
import time
import json
import math
import html
import tldextract
import requests
import feedparser
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
from urllib.parse import quote_plus
from dateutil import parser as dateparser

import streamlit as st

st.set_page_config(page_title="Rumor Right Issue & Aksi Korporasi IDX", layout="wide")
st.title("📰 Backdoor Listing and Corporate Action Scanner ")
st.caption(
    "Alat ini membantu menyaring **rumor** dari berita. Mohon **verifikasi** ke pengumuman resmi IDX/OJK/emitmen sebelum mengambil keputusan.")

# ==========================
# WHITELIST EMITEN (DARI PENGGUNA)
# ==========================
ALLOWED_TICKERS_RAW = """
AADI
AALI
ABBA
ABDA
ABMM
ACES
ACRO
ACST
ADCP
ADES
ADHI
ADMF
ADMG
ADMR
ADRO
AEGS
AGAR
AGII
AGRO
AGRS
AHAP
AIMS
AISA
AKKU
AKPI
AKRA
AKSI
ALDO
ALII
ALKA
ALMI
ALTO
AMAG
AMAN
AMAR
AMFG
AMIN
AMMN
AMMS
AMOR
AMRT
ANDI
ANJT
ANTM
APEX
APIC
APII
APLI
APLN
ARCI
AREA
ARGO
ARII
ARKA
ARKO
ARMY
ARNA
ARTA
ARTI
ARTO
ASBI
ASDM
ASGR
ASHA
ASII
ASJT
ASLC
ASLI
ASMI
ASPI
ASPR
ASRI
ASRM
ASSA
ATAP
ATIC
ATLA
AUTO
AVIA
AWAN
AXIO
AYAM
AYLS
BABP
BABY
BACA
BAIK
BAJA
BALI
BANK
BAPA
BAPI
BATA
BATR
BAUT
BAYU
BBCA
BBHI
BBKP
BBLD
BBMD
BBNI
BBRI
BBRM
BBSI
BBSS
BBTN
BBYB
BCAP
BCIC
BCIP
BDKR
BDMN
BEBS
BEEF
BEER
BEKS
BELI
BELL
BESS
BEST
BFIN
BGTG
BHAT
BHIT
BIKA
BIKE
BIMA
BINA
BINO
BIPI
BIPP
BIRD
BISI
BJBR
BJTM
BKDP
BKSL
BKSW
BLES
BLOG
BLTA
BLTZ
BLUE
BMAS
BMBL
BMHS
BMRI
BMSR
BMTR
BNBA
BNBR
BNGA
BNII
BNLI
BOAT
BOBA
BOGA
BOLA
BOLT
BOSS
BPFI
BPII
BPTR
BRAM
BREN
BRIS
BRMS
BRNA
BRPT
BRRC
BSBK
BSDE
BSIM
BSML
BSSR
BSWD
BTEK
BTEL
BTON
BTPN
BTPS
BUAH
BUDI
BUKA
BUKK
BULL
BUMI
BUVA
BVIC
BWPT
BYAN
CAKK
CAMP
CANI
CARE
CARS
CASA
CASH
CASS
CBDK
CBMF
CBPE
CBRE
CBUT
CCSI
CDIA
CEKA
CENT
CFIN
CGAS
CHEK
CHEM
CHIP
CINT
CITA
CITY
CLAY
CLEO
CLPI
CMNP
CMNT
CMPP
CMRY
CNKO
CNMA
CNTB
CNTX
COAL
COCO
COIN
COWL
CPIN
CPRI
CPRO
CRAB
CRSN
CSAP
CSIS
CSMI
CSRA
CTBN
CTRA
CTTH
CUAN
CYBR
DAAZ
DADA
DART
DATA
DAYA
DCII
DEAL
DEFI
DEPO
DEWA
DEWI
DFAM
DGIK
DGNS
DGWG
DIGI
DILD
DIVA
DKFT
DKHH
DLTA
DMAS
DMMX
DMND
DNAR
DNET
DOID
DOOH
DOSS
DPNS
DPUM
DRMA
DSFI
DSNG
DSSA
DUCK
DUTI
DVLA
DWGL
DYAN
EAST
ECII
EDGE
EKAD
ELIT
ELPI
ELSA
ELTY
EMDE
EMTK
ENAK
ENRG
ENVY
ENZO
EPAC
EPMT
ERAA
ERAL
ERTX
ESIP
ESSA
ESTA
ESTI
ETWA
EURO
EXCL
FAPA
FAST
FASW
FILM
FIMP
FIRE
FISH
FITT
FLMC
FMII
FOLK
FOOD
FORE
FORU
FPNI
FUJI
FUTR
FWCT
GAMA
GDST
GDYR
GEMA
GEMS
GGRM
GGRP
GHON
GIAA
GJTL
GLOB
GLVA
GMFI
GMTD
GOLD
GOLF
GOLL
GOOD
GOTO
GOTOM
GPRA
GPSO
GRIA
GRPH
GRPM
GSMF
GTBO
GTRA
GTSI
GULA
GUNA
GWSA
GZCO
HADE
HAIS
HAJJ
HALO
HATM
HBAT
HDFA
HDIT
HEAL
HELI
HERO
HEXA
HGII
HILL
HITS
HKMU
HMSP
HOKI
HOME
HOMI
HOPE
HOTL
HRME
HRTA
HRUM
HUMI
HYGN
IATA
IBFN
IBOS
IBST
ICBP
ICON
IDEA
IDPR
IFII
IFSH
IGAR
IIKP
IKAI
IKAN
IKBI
IKPM
IMAS
IMJS
IMPC
INAF
INAI
INCF
INCI
INCO
INDF
INDO
INDR
INDS
INDX
INDY
INET
INKP
INOV
INPC
INPP
INPS
INRU
INTA
INTD
INTP
IOTF
IPAC
IPCC
IPCM
IPOL
IPPE
IPTV
IRRA
IRSX
ISAP
ISAT
ISEA
ISSP
ITIC
ITMA
ITMG
JARR
JAST
JATI
JAWA
JAYA
JECC
JGLE
JIHD
JKON
JMAS
JPFA
JRPT
JSKY
JSMR
JSPT
JTPE
KAEF
KAQI
KARW
KAYU
KBAG
KBLI
KBLM
KBLV
KBRI
KDSI
KDTN
KEEN
KEJU
KETR
KIAS
KICI
KIJA
KING
KINO
KIOS
KJEN
KKES
KKGI
KLAS
KLBF
KLIN
KMDS
KMTR
KOBX
KOCI
KOIN
KOKA
KONI
KOPI
KOTA
KPIG
KRAS
KREN
KRYA
KSIX
KUAS
LABA
LABS
LAJU
LAND
LAPD
LCGP
LCKM
LEAD
LFLO
LIFE
LINK
LION
LIVE
LMAS
LMAX
LMPI
LMSH
LOPI
LPCK
LPGI
LPIN
LPKR
LPLI
LPPF
LPPS
LRNA
LSIP
LTLS
LUCK
LUCY
MABA
MAGP
MAHA
MAIN
MANG
MAPA
MAPB
MAPI
MARI
MARK
MASA
MASB
MAXI
MAYA
MBAP
MBMA
MBSS
MBTO
MCAS
MCOL
MCOR
MDIA
MDIY
MDKA
MDKI
MDLA
MDLN
MDRN
MEDC
MEDS
MEGA
MEJA
MENN
MERI
MERK
META
MFIN
MFMI
MGLV
MGNA
MGRO
MHKI
MICE
MIDI
MIKA
MINA
MINE
MIRA
MITI
MKAP
MKNT
MKPI
MKTR
MLBI
MLIA
MLPL
MLPT
MMIX
MMLP
MNCN
MOLI
MORA
MPIX
MPMX
MPOW
MPPA
MPRO
MPXL
MRAT
MREI
MSIE
MSIN
MSJA
MSKY
MSTI
MTDL
MTEL
MTFN
MTLA
MTMH
MTPS
MTRA
MTSM
MTWI
MUTU
MYOH
MYOR
MYTX
NAIK
NANO
NASA
NASI
NATO
NAYZ
NCKL
NELY
NEST
NETV
NFCX
NICE
NICK
NICL
NIKL
NINE
NIRO
NISP
NOBU
NPGF
NRCA
NSSS
NTBK
NUSA
NZIA
OASA
OBAT
OBMD
OCAP
OILS
OKAS
OLIV
OMED
OMRE
OPMS
PACK
PADA
PADI
PALM
PAMG
PANI
PANR
PANS
PART
PBID
PBRX
PBSA
PCAR
PDES
PDPP
PEGE
PEHA
PEVE
PGAS
PGEO
PGJO
PGLI
PGUN
PICO
PIPA
PJAA
PKPK
PLAN
PLAS
PLIN
PMJS
PMMP
PMUI
PNBN
PNBS
PNGO
PNIN
PNLF
PNSE
POLA
POLI
POLL
POLU
POLY
POOL
PORT
POSA
POWR
PPGL
PPRE
PPRI
PPRO
PRAY
PRDA
PRIM
PSAB
PSAT
PSDN
PSGO
PSKT
PSSI
PTBA
PTDU
PTIS
PTMP
PTMR
PTPP
PTPS
PTPW
PTRO
PTSN
PTSP
PUDP
PURA
PURE
PURI
PWON
PYFA
PZZA
RAAM
RAFI
RAJA
RALS
RANC
RATU
RBMS
RCCC
RDTX
REAL
RELF
RELI
RGAS
RICY
RIGS
RIMO
RISE
RMKE
RMKO
ROCK
RODA
RONY
ROTI
RSCH
RSGK
RUIS
RUNS
SAFE
SAGE
SAME
SAMF
SAPX
SATU
SBAT
SBMA
SCCO
SCMA
SCNP
SCPI
SDMU
SDPC
SDRA
SEMA
SFAN
SGER
SGRO
SHID
SHIP
SICO
SIDO
SILO
SIMA
SIMP
SINI
SIPD
SKBM
SKLT
SKRN
SKYB
SLIS
SMAR
SMBR
SMCB
SMDM
SMDR
SMGA
SMGR
SMIL
SMKL
SMKM
SMLE
SMMA
SMMT
SMRA
SMRU
SMSM
SNLK
SOCI
SOFA
SOHO
SOLA
SONA
SOSS
SOTS
SOUL
SPMA
SPRE
SPTO
SQMI
SRAJ
SRIL
SRSN
SRTG
SSIA
SSMS
SSTM
STAA
STAR
STRK
STTP
SUGI
SULI
SUNI
SUPR
SURE
SURI
SWAT
SWID
TALF
TAMA
TAMU
TAPG
TARA
TAXI
TAYS
TBIG
TBLA
TBMS
TCID
TCPI
TDPM
TEBE
TECH
TELE
TFAS
TFCO
TGKA
TGRA
TGUK
TIFA
TINS
TIRA
TIRT
TKIM
TLDN
TLKM
TMAS
TMPO
TNCA
TOBA
TOOL
TOPS
TOSK
TOTL
TOTO
TOWR
TOYS
TPIA
TPMA
TRAM
TRGU
TRIL
TRIM
TRIN
TRIO
TRIS
TRJA
TRON
TRST
TRUE
TRUK
TRUS
TSPC
TUGU
TYRE
UANG
UCID
UDNG
UFOE
ULTJ
UNIC
UNIQ
UNIT
UNSP
UNTD
UNTR
UNVR
URBN
UVCR
VAST
VERN
VICI
VICO
VINS
VISI
VIVA
VKTR
VOKS
VRNA
VTNY
WAPO
WEGE
WEHA
WGSH
WICO
WIDI
WIFI
WIIM
WIKA
WINE
WINR
WINS
WIRG
WMPP
WMUU
WOMF
WOOD
WOWS
WSBP
WSKT
WTON
YELO
YOII
YPAS
YULE
YUPI
ZATA
ZBRA
ZINC
ZONE
ZYRX
"""
ALLOWED_TICKERS = set(ALLOWED_TICKERS_RAW.split())

# ==========================
# KONFIGURASI & KATA KUNCI
# ==========================
KEYWORD_CATEGORIES = {
    "Right Issue (HMETD)": [
        "right issue", "rights issue", "hmetd", "penambahan modal dengan hmetd",
        "isu right issue", "rencana right issue", "hak memesan efek terlebih dahulu"
    ],
    "Private Placement (PMTHMETD)": [
        "private placement", "pmthmetd", "penambahan modal tanpa hmetd", "non pre-emptive"
    ],
    "Akuisisi / Merger": [
        "akuisisi", "merger", "pengambilalihan", "takeover", "backdoor listing"
    ],
    "Stock Split / Reverse": [
        "stock split", "pemecahan saham", "reverse stock", "reverse stock split", "penggabungan saham"
    ],
    "Buyback": ["buyback", "pembelian kembali saham"],
    "Waran / Konversi": ["waran", "warrant", "obligasi konversi", "mandatory convertible"],
    "Dividen": ["dividen", "pembagian dividen", "dividend"],
    "RUPS / RUPSLB": ["rups", "rupslb", "rapat umum pemegang saham"]
}

# Stopwords (uppercase) yang sering salah terdeteksi sebagai ticker
STOPWORDS = set([
    "IPO", "IHSG", "IDX", "BEI", "USD", "IDR", "BANK", "PT", "TBK",
    "OJK", "ETF", "RUPS", "PMTHMETD", "HMETD", "PMBN", "PP", "PS",
    "TAX", "BI", "BUMN", "JCI", "JAKARTA", "ASEAN", "ASIA", "INDO",
])

# Pola deteksi ticker (umum 3–4 huruf kapital). Tambah dukungan ".JK" bila ada.
TICKER_REGEX = re.compile(r"\b([A-Z]{3,4})(?:\.JK)?\b")
# Pola nama perusahaan Indonesia
PT_NAME_REGEX = re.compile(r"PT\s+([A-Za-z\s.&-]{3,80}?)(?:\s+Tbk)?\b", re.IGNORECASE)

# ==========================
# SIDEBAR FILTERS
# ==========================
st.sidebar.header("Filter Pencarian")
min_days = 30
max_days = 365
range_days = st.sidebar.slider("Jangka waktu (hari ke belakang)", 7, max_days, min_days, help="Rentang publikasi berita yang disaring.")
end_date = date.today()
start_date = end_date - timedelta(days=range_days)

selected_categories = st.sidebar.multiselect(
    "Kategori aksi korporasi",
    list(KEYWORD_CATEGORIES.keys()),
    default=["Right Issue (HMETD)", "Private Placement (PMTHMETD)", "Akuisisi / Merger"],
)

extra_keywords = st.sidebar.text_input(
    "Kata kunci tambahan (opsional)", value="",
    placeholder="mis. 'rights issue jumbo', 'akuisisi nikel'",
)

max_results_per_query = st.sidebar.number_input(
    "Batas item per query (RSS)", min_value=10, max_value=200, value=50, step=10,
    help="Semakin besar, semakin banyak berita yang diproses.")

# Batasi subset whitelist (opsional)
subset_allowed = st.sidebar.multiselect(
    "Batasi hanya ke emiten tertentu (opsional)",
    sorted(ALLOWED_TICKERS),
    default=sorted(ALLOWED_TICKERS),
    help="Pilih subset whitelist untuk difokuskan.")
subset_allowed = set(subset_allowed) if subset_allowed else ALLOWED_TICKERS

include_official = st.sidebar.checkbox(
    "Cek sumber resmi IDX (eksperimental)", value=False,
    help="Mencoba memindai area pengumuman resmi. Fitur eksperimental — bisa tidak stabil.")

show_raw_articles = st.sidebar.checkbox("Tampilkan semua artikel mentah", value=False)

st.sidebar.markdown("---")
export_btn_placeholder = st.sidebar.empty()

# ==========================
# UTILITIES
# ==========================

def within_range(dt: datetime) -> bool:
    d = dt.date()
    return start_date <= d <= end_date


def google_news_rss(query: str, hl: str = "id", gl: str = "ID", ceid: str = "ID:id") -> str:
    """Bangun URL RSS Google News untuk suatu query."""
    return f"https://news.google.com/rss/search?q={quote_plus(query)}&hl={hl}&gl={gl}&ceid={ceid}"


def fetch_rss_entries(query: str, limit: int = 100):
    url = google_news_rss(query)
    feed = feedparser.parse(url)
    # feed.entries sudah terurut terbaru → lama (biasanya)
    return feed.entries[:limit]


def extract_domain(url: str) -> str:
    try:
        ext = tldextract.extract(url)
        domain = f"{ext.domain}.{ext.suffix}" if ext.suffix else ext.domain
        return domain.lower()
    except Exception:
        return ""


def extract_datetime(entry) -> datetime | None:
    # feedparser biasanya menyertakan published_parsed / updated_parsed
    dt_candidates = []
    if hasattr(entry, "published"):
        try:
            dt_candidates.append(dateparser.parse(entry.published))
        except Exception:
            pass
    if hasattr(entry, "updated"):
        try:
            dt_candidates.append(dateparser.parse(entry.updated))
        except Exception:
            pass
    return max(dt_candidates) if dt_candidates else None


def guess_tickers(text: str) -> set[str]:
    """Deteksi ticker hanya dari whitelist, mendukung 3–5 huruf."""
    tickers = set()
    upper = text.upper()
    # Tokenisasi sederhana: ganti non-huruf menjadi spasi, lalu split
    cleaned = re.sub(r"[^A-Z]", " ", upper)
    for token in cleaned.split():
        if token in ALLOWED_TICKERS:
            tickers.add(token)
    return tickers


def guess_company_name(text: str) -> str | None:
    m = PT_NAME_REGEX.search(text)
    if m:
        name = m.group(0)
        return name.strip()
    return None


def score_from_categories(categories: set[str]) -> float:
    # bobot ringan per kategori unik
    return 1.0 + 0.25 * len(categories)


def scrape_article_title(url: str, timeout: int = 8) -> str | None:
    """Ambil judul halaman ketika feed tidak memberi cukup konteks."""
    try:
        resp = requests.get(url, timeout=timeout, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome Safari"
        })
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, "html.parser")
            if soup.title and soup.title.text:
                return soup.title.text.strip()
    except Exception:
        return None
    return None

# ==========================
# PENGAMBILAN DATA
# ==========================
@st.cache_data(show_spinner=False, ttl=1800)
def run_collection(selected_categories: list[str], extra_keywords: str, limit_per_query: int):
    all_articles = []  # list of dict
    # Susun query per kategori
    for cat in selected_categories:
        kws = KEYWORD_CATEGORIES.get(cat, [])
        if extra_keywords.strip():
            # Tambah seluruh extra keywords sebagai OR tambahan di belakang
            # Contoh: (kw1 OR kw2) (extra)
            extra = extra_keywords.strip()
        else:
            extra = ""

        # Untuk setiap keyword di kategori, jalankan query sendiri-sendiri
        for kw in kws:
            # Perkaya query agar relevan ke emiten Indonesia
            query = f"(\"{kw}\") (emiten OR IDX OR \"Bursa Efek Indonesia\")"
            if extra:
                query += f" ({extra})"

            entries = fetch_rss_entries(query, limit=limit_per_query)
            for e in entries:
                published_dt = extract_datetime(e)
                if not published_dt or not within_range(published_dt):
                    continue
                title = html.unescape(getattr(e, "title", "").strip())
                summary = html.unescape(getattr(e, "summary", "").strip())
                link = getattr(e, "link", "").strip()
                source = extract_domain(link)

                # fallback: kalau judul kosong, coba scrap singkat
                if not title:
                    fetched = scrape_article_title(link)
                    if fetched:
                        title = fetched

                fulltext = f"{title} \n {summary}"
                tickers = guess_tickers(fulltext)
                pt_name = guess_company_name(fulltext)

                all_articles.append({
                    "category": cat,
                    "keyword": kw,
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "source": source,
                    "published": published_dt,
                    "tickers": list(tickers),
                    "company_hint": pt_name,
                })
    return all_articles

# (Eksperimental) contoh cek pengumuman resmi — endpoint bisa berubah.
@st.cache_data(show_spinner=False, ttl=1800)
def try_fetch_official_idx_announcements(max_items: int = 100):
    """Mengembalikan list pengumuman dari area publik IDX bila tersedia.
    *Endpoint/HTML dapat berubah sewaktu-waktu.*
    """
    try:
        url = "https://www.idx.co.id/id/pengumuman/"
        resp = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code != 200:
            return []
        soup = BeautifulSoup(resp.text, "html.parser")
        items = []
        # Heuristik ambil tautan pengumuman
        for a in soup.select("a"):
            href = a.get("href", "")
            text = (a.text or "").strip()
            if not href or not text:
                continue
            # Filter tipis terkait aksi korporasi
            low = text.lower()
            if any(k in low for k in ["right issue", "hmetd", "private placement", "rups", "stock split", "merger", "akuisisi", "dividen", "buyback"]):
                items.append({"title": text, "link": href, "source": "idx.co.id", "published": None, "category": "Resmi (indikatif)"})
            if len(items) >= max_items:
                break
        return items
    except Exception:
        return []

# ==========================
# EKSEKUSI PENCARIAN
# ==========================
run_btn = st.button("🚀 Cari Rumor Sekarang", type="primary")

if run_btn:
    with st.spinner("Mengumpulkan berita dari Google News RSS…"):
        articles = run_collection(selected_categories, extra_keywords, max_results_per_query)
        if include_official:
            official_items = try_fetch_official_idx_announcements()
        else:
            official_items = []

    st.success(f"Selesai. Ditemukan {len(articles)} artikel rumor + {len(official_items)} indikasi pengumuman resmi (jika tersedia).")

    # ==========================
    # AGREGASI PER EMITEN
    # ==========================
    emiten_map: dict[str, dict] = {}

    for a in articles:
        candidate_tickers = [t for t in (a["tickers"] or []) if t in subset_allowed]
        if not candidate_tickers:
            continue

        for tk in candidate_tickers:
            rec = emiten_map.setdefault(tk, {
                "ticker": tk,
                "company_names": set(),
                "categories": set(),
                "articles": [],
                "sources": set(),
                "first_seen": None,
                "last_seen": None,
                "raw_hits": 0,
            })

            if a["company_hint"]:
                rec["company_names"].add(a["company_hint"])
            rec["categories"].add(a["category"])
            rec["articles"].append(a)
            rec["sources"].add(a["source"])
            rec["raw_hits"] += 1
            if a["published"]:
                if not rec["first_seen"] or a["published"] < rec["first_seen"]:
                    rec["first_seen"] = a["published"]
                if not rec["last_seen"] or a["published"] > rec["last_seen"]:
                    rec["last_seen"] = a["published"]
                    rec["last_seen"] = a["published"]

    # Buat dataframe ringkasan
    rows = []
    for tk, rec in emiten_map.items():
        if tk == "(NON-TICKER)":
            continue  # sembunyikan baris tanpa ticker di ringkasan
        score = rec["raw_hits"] * score_from_categories(rec["categories"])
        rows.append({
            "Ticker": tk,
            "Nama (indikatif)": "; ".join(sorted(rec["company_names"]))[:120] or "—",
            "Kategori": ", ".join(sorted(rec["categories"])),
            "Jumlah Artikel": rec["raw_hits"],
            "Sumber Unik": len(rec["sources"]),
            "Skor": round(score, 2),
            "Terakhir Terlihat": rec["last_seen"].strftime("%Y-%m-%d %H:%M") if rec["last_seen"] else "—",
        })

    df = pd.DataFrame(rows).sort_values(["Skor", "Jumlah Artikel"], ascending=[False, False])

    st.subheader("📈 Ringkasan Kandidat Emiten Terindikasi Rumor")
    if df.empty:
        st.info("Tidak ada kandidat emiten yang terdeteksi di periode & kategori terpilih.")
    else:
        st.dataframe(df, use_container_width=True, height=420)

    # Ekspor CSV
    if not df.empty:
        csv_buf = io.StringIO()
        df.to_csv(csv_buf, index=False)
        export_btn_placeholder.download_button(
            label="📥 Unduh Ringkasan (CSV)",
            data=csv_buf.getvalue(),
            file_name=f"rumor_idx_{start_date}_{end_date}.csv",
            mime="text/csv",
        )

    # ==========================
    # DETAIL PER EMITEN
    # ==========================
    st.markdown("---")
    st.subheader("🔎 Detail & Bukti Artikel per Emiten")

    selected_ticker = st.selectbox(
        "Pilih Ticker untuk melihat bukti",
        [r["Ticker"] for r in rows] if rows else [],
        index=0 if rows else None,
        placeholder="Pilih ticker…",
    )

    if selected_ticker:
        rec = emiten_map.get(selected_ticker)
        if not rec:
            st.warning("Data tidak tersedia untuk ticker terpilih.")
        else:
            st.markdown(
                f"**Ticker:** `{rec['ticker']}`  ")
            st.markdown(
                f"**Nama (indikatif):** {('; '.join(sorted(rec['company_names'])) or '—')}  ")
            st.markdown(
                f"**Kategori Terindikasi:** {', '.join(sorted(rec['categories']))}  ")
            st.markdown(
                f"**Periode:** {start_date} s.d. {end_date}  ")

            # Daftar artikel
            for i, art in enumerate(sorted(rec["articles"], key=lambda x: x["published"] or datetime.min, reverse=True), start=1):
                with st.expander(f"{i}. {art['title'][:140] if art['title'] else '(tanpa judul)'}"):
                    st.write(f"**Tanggal:** {art['published'].strftime('%Y-%m-%d %H:%M') if art['published'] else '—'}")
                    st.write(f"**Sumber:** {art['source'] or '—'} | **Kategori:** {art['category']}")
                    if art["summary"]:
                        st.write(art["summary"])
                    st.write(f"[Baca Artikel]({art['link']})")

    # ==========================
    # ARTIKEL MENTAH & SUMBER RESMI
    # ==========================
    if show_raw_articles:
        st.markdown("---")
        st.subheader("🧾 Semua Artikel Mentah (Disaring tanggal)")
        raw_df = pd.DataFrame([
            {
                "Tanggal": a["published"].strftime("%Y-%m-%d %H:%M") if a["published"] else "—",
                "Kategori": a["category"],
                "Keyword": a["keyword"],
                "Judul": a["title"],
                "Ticker?": ", ".join(a["tickers"]) or "—",
                "Perusahaan?": a["company_hint"] or "—",
                "Sumber": a["source"],
                "Link": a["link"],
            }
            for a in articles
        ])
        st.dataframe(raw_df, use_container_width=True, height=500)

    if include_official:
        st.markdown("---")
        st.subheader("📜 Indikasi Pengumuman Resmi IDX (Eksperimental)")
        if not official_items:
            st.info("Tidak ditemukan atau endpoint berubah.")
        else:
            for i, it in enumerate(official_items, start=1):
                st.write(f"{i}. [{it['title']}]({it['link']}) — {it['source']}")

else:
    st.info(
        "Pilih kategori, atur jangka waktu, lalu klik **‘🚀 Cari Rumor Sekarang’**.\n\n"
        "Tips: tambah kata kunci spesifik (mis. sektor, komoditas) untuk mempersempit hasil.")

# ==========================
# DISCLAIMER
# ==========================
st.markdown(
    "---\n"
    "**Disclaimer:** Aplikasi ini memanfaatkan pencarian berita publik untuk *indikasi rumor*. "+
    "Informasi ini **bukan** nasihat investasi dan tidak menggantikan pengumuman resmi. "+
    "Selalu lakukan *due diligence* dan cek dokumen resmi (prospektus, keterbukaan informasi IDX/OJK).")
