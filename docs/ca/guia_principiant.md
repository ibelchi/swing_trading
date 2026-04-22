# radarcore: Guia d'Inversió (Conceptes i Pràctica)

Benvingut a **radarcore**. Aquest manual t'ajudarà a entendre com funciona l'estratègia **Buy the Recovery** (Comprar la Recuperació) i com pots utilitzar aquest programari per aprendre sobre finances i swing trading des de zero.

---

## 1. Què és l'estratègia "Buy the Recovery"?

Històricament, molta gent ha sentit l'expressió "Buy the Dip" (comprar la caiguda). A RadarCore l'anomenem **Buy the Recovery** perquè és més precisa: no comprem quan l'acció baixa (un "ganivet que cau"), sinó quan ja ha trobat un terra i comença a recuperar-se.

L'objectiu és aprofitar que el preu tendeix a tornar a la seva mitjana després d'un ensurt temporal.

---

## 2. Abans de començar: Configurant l'Escàner

Quan configures l'escàner, veus una sèrie de paràmetres. Aquí tens què signifiquen en llenguatge planer:

*   **Lookback Days (Dies de recerca)**: És quant de temps enrere mirem el passat per buscar el punt més alt de l'acció. Si poses 60 dies, busquem el "Rècord" de preu d'aquells 2 mesos per comparar-lo amb el preu d'avui.
*   **Min Drop % (Caiguda mínima)**: Quant "descompte" vols que tingui l'acció abans d'avisar-te. Si pones 15%, només busquem empreses que hagin caigut almenys un 15% des del seu màxim de 60 dies.
*   **Min Rebound % (Rebot mínim)**: És la confirmació de que ja no estem caient. Si pones 2%, vols que l'acció ja hagi pujat un 2% des del seu punt més baix.
*   **Symbol Limit**: Quantes empreses del mercat vols analitzar (0 per analitzar-les totes).

---

## 3. El Model de Cubells (Buckets) i Fases

En lloc d'una sola estratègia rígida, RadarCore classifica cada acció en un **Cubell** (Patró) i una **Fase** (Timing).

### Els Cubells Principals (Buckets)
*   **SWING**: La configuració clàssica. Una caiguda profunda seguida d'un rebot clar.
*   **RISE**: L'acció ja està en una tendència alcista constant. Menys recorregut de creixement però més estable.
*   **LATERAL**: L'acció es mou de costat. Fase d'acumulació.

### El Cicle de Vida (Fases)
El programa t'indica en quin moment del "viatge" de tornada als màxims et trobes:
*   🟢 **VALLEY (Vall)**: Ets al fons. Màxim benefici potencial, però màxim risc.
*   🟡 **MID (Punt mig)**: La recuperació està confirmada. Ets al "punt dolç" de la tendència.
*   🟠 **MATURE (Madur)**: La major part de la recuperació ja ha passat. Compte a l'hora d'entrar ara.
*   🔴 **LATE (Tard)**: L'acció ja ha tornat als seus màxims. L'oportunitat s'ha esgotat.

---

## 4. Conceptes Financers Clau

### Stop Loss (SL)
És el teu **fre de mà de seguretat**. Imagina que compres una acció a 10$. Si de sobte l'empresa segueix anant malament, l'Stop Loss és una ordre que diu al teu banc: "Si l'acció torna a baixar fins a 9$, ven-la immediatament". 
*   **Per què serveix?** Perquè si l'empresa fa fallida, tu només hauràs perdut l'1$ (del 10 al 9), però t'hauràs salvat de perdre els 10$ sencers. RadarCore et marca aquesta línia en vermell als gràfics.

### Objectius (T1 i T2)
Són les teves "metes de venda" on reculls els guanys.
*   **T1 (Objectiu Conservador)**: És un punt mig de recuperació (habitualment al 85% del màxim anterior). On pots vendre la meitat per assegurar beneficis.
*   **T2 (Objectiu Ideal)**: Quan l'acció torna exactament al preu màxim que tenia abans de caure. L'estratègia s'ha completat amb èxit.

### Mercats de Referència (L'S&P 500)
Encara que escanegis altres mercats, el programa sempre fa servir el "Mercat Americà" (**SPY / S&P 500**) com a referència global. Si la borsa americana cau fort, és difícil que qualsevol acció pugi de forma sana. Serveix de termòmetre per saber si la caiguda és un cas aïllat o una crisi mundial.

---

## 5. Cas Pràctic: Interpretant els Gràfics

Quan obris un gràfic a RadarCore, busca aquests colors:

1.  **La Muntanya (Or)**: Mostra la tendència de 2 anys. Busca formes de "U" o "V".
2.  **Triangles Verds (Valls)**: Són els terres. El triangle verd més recent marca l'inici de la recuperació actual.
3.  **Triangles Vermells (Pics)**: Són els sostres. Mostren on l'acció va trobar resistència anteriorment.

## Regla d'Or: Diversificació
Mai posis tots els teus estalvis en una sola acció. L'estratègia correcta consisteix a tenir, per exemple, 10 operacions diferents a la vegada. Així, si una surt malament i salta l'**Stop Loss**, les altres 9 poden seguir el seu curs cap al **T2** i donar-te beneficis globals.
