import streamlit as st
import breakwater as bw
from streamlit_extras.capture import stdout

st.title(":new_moon: Breakwater Design")
st.write(
    "A user-friendly app for conceptual breakwater design, powered by the open-source **breakwater** package."
)
st.write(
    "For more details about definition of parameters, equations, limitations, please check the [documentation](https://breakwater.readthedocs.io/)."
)

# 1 - Breakwater type
st.subheader("1. Select Breakwater type")
st.image(
    "https://github.com/Sander-w/breakwater/blob/8eeec8626f6a7549682472328658dda82fb69c99/doc/_figures/breakwater-types.png?raw=true"
)
st.caption(
    "Figure 1.1: Typical cross sections of various types of breakwaters, with the rubble mound types on the left and the monolithic types on the right. (Winkel, 2000. Redrawn from CIRIA, CUR, CETMEF, 2007, p.781)."
)
breakwater_type = st.selectbox(
    label="Select a breakwater type",
    options=[
        "Rock Rubble Mound (RRM)",
        "Concrete Rubble Mound (CRM)",
        "Caisson",
    ],
)
if breakwater_type == "Concrete Rubble Mound (CRM)":
    armour_type = st.selectbox(
        label="Select armour type",
        options=[
            "Xbloc",
            "Xbloc Plus",
        ],
    )
    if armour_type == "Xbloc":
        ArmourUnit = bw.Xbloc()
    elif armour_type == "Xbloc Plus":
        ArmourUnit = bw.XblocPlus()

# 2 Environmental Conditions
st.subheader("2. Define Envorinmental Conditions")
if breakwater_type == "Caisson":
    st.image(
        "https://github.com/Sander-w/breakwater/blob/master/doc/_figures/caisson.png?raw=true"
    )
    st.caption(
        "Figure 3.2: schematisation of a vertical or composite vertical wall with definitions of variables (Winkel, 2000)."
    )
else:
    st.image(
        "https://github.com/Sander-w/breakwater/blob/master/doc/_figures/rubble-mound.png?raw=true"
    )
    st.caption(
        "Figure 2.1: Schematisation of a rubble mound breakwater with definitions of variables (Winkel, 2000)."
    )

Hm0 = st.number_input("Hm0 -- Spectral wave height [m]", value=2.0)
if breakwater_type == "Caisson":
    h, d = st.columns(2)
    with h:
        h = st.number_input("h -- Water depth [m]", value=15)
    with d:
        d = st.number_input("d -- Caisson draft [m]", value=10)
else:
    h = st.number_input("h -- Water depth [m]", value=15)

slope_foreshore_v, slope_foreshore_h = st.columns(2)
with slope_foreshore_v:
    slope_foreshore_v = st.number_input(
        "Vertical component of the foreshore slope", value=1
    )
with slope_foreshore_h:
    slope_foreshore_h = st.number_input(
        "Horizontal component of the foreshore slope", value=100
    )

battjes = bw.BattjesGroenendijk(
    Hm0=Hm0, h=h, slope_foreshore=(slope_foreshore_v, slope_foreshore_h)
)
H2_per = battjes.get_Hp(0.02)

# 3 Ultimate Limit State
st.subheader("3. Define Ultimate Limit State")
if breakwater_type == "Caisson":
    st.image(
        "https://github.com/Sander-w/breakwater/blob/master/doc/_figures/C.png?raw=true"
    )
    st.caption("Figure 3.2: Definitions for a rubble mound breakwater (Winkel, 2000).")
else:
    st.image(
        "https://github.com/Sander-w/breakwater/blob/master/doc/_figures/RM.png?raw=true"
    )
    st.caption(
        "Figure 3.1: Definitions for a (composite) vertical breakwater (Winkel, 2000)."
    )

limit_Hm0 = Hm0
limit_q = st.number_input(
    "q -- Mean overtopping discharge per meter structure width [l/s per m]", value=20
)
limit_Hs, limit_Tp = st.columns(2)
with limit_Hs:
    limit_Hs = st.number_input("Hs -- Significant wave height [m]", value=2)
with limit_Tp:
    limit_Tp = st.number_input("Tp -- Peak wave period [s]", value=9.4)

if breakwater_type == "Rock Rubble Mound (RRM)":
    limit_Nod, limit_Sd = st.columns(2)
    with limit_Nod:
        limit_Nod = st.number_input(
            "(Optional) Nod -- Damage number, used in the formula for the toe stability",
            value=5,
        )
    with limit_Sd:
        limit_Sd = st.number_input(
            "(Optional) Sd -- Damage number parameter, used in Van der Meer formula",
            value=2,
        )
if breakwater_type == "Concrete Rubble Mound (CRM)":
    limit_Nod = st.number_input(
        "Nod -- Damage number, used in the formula for the toe stability", value=5
    )

if breakwater_type == "Caisson":
    limit_H13, limit_Hmax = bw.goda_wave_heights(
        h=h, d=12, Ho=limit_Hs, T=limit_Tp, slope_foreshore=(1, 100)
    )
ULS = bw.LimitState(
    h=h,
    label="Ultimate Limit State",
    **{
        k.lstrip("limit_"): v
        for k, v in locals().items()
        if k.startswith("limit_") and v is not None
    }
)
ULS.transform_periods(1)

# 3 Breakwater Configuration
st.subheader("4. Define Breakwater Configuration")
rho = st.number_input("Density of the armourstone [kg/m³]", value=2650)
NEN = bw.RockGrading(rho=rho)

if breakwater_type in ["Rock Rubble Mound (RRM)", "Concrete Rubble Mound (CRM)"]:
    slope_v, slope_h = st.columns(2)
    with slope_v:
        slope_v = st.number_input(
            "V -- Vertical component of the breakwater slope", value=2
        )
    with slope_h:
        slope_h = st.number_input(
            "H -- Horizontal component of the breakwater slope", value=3
        )
    rho_w, B = st.columns(2)
    with rho_w:
        rho_w = st.number_input("Density of water [kg/m³]", value=1025)
    with B:
        B = st.number_input("B -- Crest width [m]", value=5.5)
    N, Dn50_core = st.columns(2)
    with N:
        N = st.number_input(
            "N -- Number of incident waves at the toe of the breakwater structure [-]",
            value=2100,
        )
    with Dn50_core:
        Dn50_core = st.number_input(
            "Dn50 -- Nominal diameter for the stones in the core of the breakwater [m]",
            value=1,
        )
elif breakwater_type == "Caisson":
    Pc = st.slider(
        "Pc -- Ratio of concrete to the total mass of the caisson",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.01,
    )
    rho_c, rho_fill = st.columns(2)
    with rho_c:
        rho_c = st.number_input("Density of concrete [kg/m3]", value=2400)
    with rho_fill:
        rho_fill = st.number_input("Density of fill material [kg/m3]", value=1600)

    rho_w, Bm = st.columns(2)
    with rho_w:
        rho_w = st.number_input("Density of water [kg/m3]", value=1025)
    with Bm:
        Bm = st.number_input("Bm -- Width of the berm [m]", value=8)

    hb, layers = st.columns(2)
    with hb:
        hb = st.number_input("hb -- Height of the foundation layer [m]", value=2)
    with layers:
        layers = st.number_input("Number of foundation layer [-]", value=2)
    BermMaterial = st.selectbox(
        "Select Berm Material",
        options=["Rock", "Xbloc", "Xbloc Plus"],
    )
    if BermMaterial == "Rock":
        BermMaterial = NEN
    elif BermMaterial == "Xbloc":
        BermMaterial = bw.Xbloc()
    elif BermMaterial == "Xbloc Plus":
        BermMaterial = bw.XblocPlus()

    mu, beta = st.columns(2)
    with mu:
        mu = st.number_input(
            "Friction factor between the caisson and the foundation layer [-]",
            value=0.5,
        )
    with beta:
        beta = st.number_input(
            "Angle between direction of wave approach and a line normal to the breakwater [degrees]",
            value=15,
        )
if st.button("Design", use_container_width=True):
    if breakwater_type == "Rock Rubble Mound (RRM)":
        breakwater = bw.RockRubbleMound(
            slope=(slope_v, slope_h),
            slope_foreshore=(slope_foreshore_v, slope_foreshore_h),
            rho_w=rho_w,
            B=B,
            N=N,
            LimitState=ULS,
            Grading=NEN,
            Dn50_core=Dn50_core,
        )
    elif breakwater_type == "Concrete Rubble Mound (CRM)":
        breakwater = bw.ConcreteRubbleMound(
            slope=(slope_v, slope_h),
            slope_foreshore=(slope_foreshore_v, slope_foreshore_h),
            rho_w=rho_w,
            B=B,
            ArmourUnit=ArmourUnit,
            LimitState=ULS,
            Grading=NEN,
            Dn50_core=Dn50_core,
        )
    elif breakwater_type == "Caisson":
        breakwater = bw.Caisson(
            Pc=Pc,
            rho_c=rho_c,
            rho_fill=rho_fill,
            rho_w=rho_w,
            Bm=Bm,
            hb=hb,
            layers=layers,
            BermMaterial=BermMaterial,
            Grading=NEN,
            LimitState=ULS,
            slope_foreshore=(slope_foreshore_v, slope_foreshore_h),
            mu=mu,
            beta=beta,
        )

    breakwater.plot("all", save_name="plot")
    st.image("plot.png")

    output = st.empty()
    with stdout(output.code, terminator=""):
        breakwater.print_variant("all")

    output = st.empty()
    with stdout(output.code, terminator=""):
        breakwater.print_logger(level="warnings")

col1, col2 = st.columns(2)
with col1:
    st.caption("Breakwater package by [Sander Winkel](https://github.com/sander-w)")
with col2:
    st.caption("Streamlit app by [Ryan Alvita](https://github.com/ryanalvita)")
