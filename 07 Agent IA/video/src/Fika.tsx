import React from "react";
import {AbsoluteFill, Audio, Easing, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from "remotion";
import {loadFont} from "@remotion/fonts";
import data from "./data.json";

loadFont({family: "Noto Sans", url: staticFile("fonts/NotoSans.ttf"), weight: "100 900"});
loadFont({family: "Noto Sans Mono", url: staticFile("fonts/NotoSansMono.ttf"), weight: "100 900"});

export const DUREE = 47;
const BLEU = "#0058A3";
const JAUNE = "#FFDA1A";
const CREME = "#F5F3EE";
const ENCRE = "#111418";
const ROUGE = "#D9472B";
const VERT = "#1F7A4D";
const SANS = "'Noto Sans', sans-serif";
const MONO = "'Noto Sans Mono', monospace";

type P = [number, number];
const s = (sec: number, fps: number) => Math.round(sec * fps);
const clamp = {extrapolateLeft: "clamp", extrapolateRight: "clamp"} as const;
const ease = Easing.bezier(0.22, 1, 0.36, 1);

const lenOf = (pts: P[]) => pts.slice(1).reduce((a, p, i) => a + Math.hypot(p[0] - pts[i][0], p[1] - pts[i][1]), 0);
const pointAlong = (pts: P[], t: number): P => {
  const total = lenOf(pts);
  let d = Math.max(0, Math.min(1, t)) * total;
  for (let i = 1; i < pts.length; i++) {
    const seg = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    if (d <= seg) {
      const k = seg === 0 ? 0 : d / seg;
      return [pts[i - 1][0] + (pts[i][0] - pts[i - 1][0]) * k, pts[i - 1][1] + (pts[i][1] - pts[i - 1][1]) * k];
    }
    d -= seg;
  }
  return pts[pts.length - 1];
};
const dOf = (pts: P[]) => pts.map((p, i) => `${i ? "L" : "M"}${p[0]},${p[1]}`).join(" ");

// ---------- petits composants ----------
const Trait: React.FC<{w?: number}> = ({w = 70}) => <div style={{width: w, height: 10, borderRadius: 5, background: JAUNE}} />;

const Apparait: React.FC<{debut: number; children: React.ReactNode; dy?: number; style?: React.CSSProperties}> = ({debut, children, dy = 40, style}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f - debut, fps, config: {damping: 200, mass: 0.7}});
  return <div style={{opacity: p, transform: `translateY(${(1 - p) * dy}px)`, ...style}}>{children}</div>;
};

const Tic: React.FC<{a: number; son?: string; vol?: number}> = ({a, son = "sfx/3005.mp3", vol = 0.4}) => (
  <Sequence from={a} durationInFrames={90}><Audio src={staticFile(son)} volume={vol} /></Sequence>
);

// ---------- scène 1 : nos chiffres fragiles ----------
const FRAGILES = [
  {t: "1 jeune sur 4 déménage chaque année", n: "étude régionale, 2022"},
  {t: "1 meuble sur 4 vendu d’occasion", n: "source tronquée"},
  {t: "150 millions de membres IKEA Family", n: "chiffre de 2020"},
];
const Scene1: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{background: CREME, padding: "150px 170px", fontFamily: SANS}}>
      <Apparait debut={0}><Trait /></Apparait>
      <Apparait debut={4}>
        <div style={{marginTop: 28, fontSize: 92, fontWeight: 800, color: BLEU, letterSpacing: -2, lineHeight: 1.05}}>Nos chiffres étaient fragiles.</div>
      </Apparait>
      <div style={{marginTop: 70, display: "flex", flexDirection: "column", gap: 26}}>
        {FRAGILES.map((x, i) => {
          const a = s(0.9 + i * 0.75, fps);
          const tampon = spring({frame: f - a - s(0.35, fps), fps, config: {damping: 12, stiffness: 180}});
          return (
            <Apparait key={i} debut={a} dy={30}>
              <div style={{display: "flex", alignItems: "center", gap: 34, background: "#fff", borderRadius: 22, padding: "26px 36px", borderTop: `8px solid ${JAUNE}`, width: 1580}}>
                <div style={{fontSize: 44, fontWeight: 700, color: ENCRE, flex: 1, whiteSpace: "nowrap"}}>{x.t}</div>
                <div style={{fontSize: 26, color: "#6b6f76"}}>{x.n}</div>
                <div style={{transform: `scale(${0.4 + tampon * 0.6}) rotate(${-8 + tampon * 4}deg)`, opacity: tampon, border: `5px solid ${ROUGE}`, color: ROUGE, fontWeight: 800, fontSize: 28, padding: "6px 16px", borderRadius: 10, fontFamily: MONO}}>À REVÉRIFIER</div>
              </div>
            </Apparait>
          );
        })}
      </div>
      <Apparait debut={s(3.6, fps)} style={{marginTop: 46}}>
        <div style={{fontSize: 38, color: "#5b5f66"}}>Et <b style={{color: ENCRE}}>0 entretien</b> terrain. Il fallait vérifier, vite et proprement.</div>
      </Apparait>
      {FRAGILES.map((_, i) => <Tic key={i} a={s(0.9 + i * 0.75 + 0.35, fps)} son="sfx/1430.mp3" vol={0.45} />)}
    </AbsoluteFill>
  );
};

// ---------- scène 2 : Fika ----------
const Scene2: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f - 8, fps, config: {damping: 14, stiffness: 120}});
  const lettres = "Fika".split("");
  return (
    <AbsoluteFill style={{background: BLEU, fontFamily: SANS, justifyContent: "center", alignItems: "center"}}>
      <Apparait debut={0}><div style={{fontSize: 42, color: "#cfe0f2", fontWeight: 500}}>Alors on a construit un agent IA.</div></Apparait>
      <div style={{display: "flex", marginTop: 20}}>
        {lettres.map((l, i) => {
          const q = spring({frame: f - 14 - i * 4, fps, config: {damping: 11, stiffness: 160}});
          return <span key={i} style={{fontSize: 300, fontWeight: 900, color: JAUNE, letterSpacing: -10, lineHeight: 1, transform: `translateY(${(1 - q) * 120}px)`, opacity: q, display: "inline-block"}}>{l}</span>;
        })}
      </div>
      <div style={{marginTop: 26, transform: `scaleX(${p})`, width: 520, height: 10, background: JAUNE, borderRadius: 5}} />
      <Apparait debut={s(1.3, fps)}><div style={{marginTop: 34, fontSize: 48, color: "#fff", fontWeight: 700}}>l’agent de recherche de l’équipe IKÉASTRE</div></Apparait>
      <Tic a={14} son="sfx/1492.mp3" vol={0.35} />
    </AbsoluteFill>
  );
};

// ---------- scène 3 : la mission ----------
const MISSION = [
  {k: "Rôle", v: "analyste data et veilleur de l’équipe"},
  {k: "Sources", v: "Insee, IKEA, instituts, presse : la meilleure d’abord"},
  {k: "Format", v: "un tableau sourcé et daté, ligne par ligne"},
  {k: "Règles", v: "zéro invention, extrait mot pour mot, dates obligatoires"},
];
const Scene3: React.FC = () => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{background: CREME, padding: "130px 170px", fontFamily: SANS}}>
      <Apparait debut={0}><div style={{fontFamily: MONO, fontSize: 30, color: BLEU, letterSpacing: 4, fontWeight: 700}}>ÉTAPE 0 · LA MISSION</div></Apparait>
      <Apparait debut={5}><div style={{marginTop: 18, fontSize: 84, fontWeight: 800, color: ENCRE, letterSpacing: -2}}>On lui donne une fiche, pas un vœu.</div></Apparait>
      <div style={{marginTop: 56, background: ENCRE, borderRadius: 28, padding: "44px 56px", width: 1580}}>
        {MISSION.map((m, i) => (
          <Apparait key={i} debut={s(0.8 + i * 0.55, fps)} dy={24}>
            <div style={{display: "flex", gap: 40, padding: "16px 0", borderBottom: i < 3 ? "1px solid #2c3138" : "none"}}>
              <div style={{width: 200, fontSize: 40, fontWeight: 800, color: JAUNE}}>{m.k}</div>
              <div style={{fontSize: 40, color: "#e9edf2"}}>{m.v}</div>
            </div>
          </Apparait>
        ))}
      </div>
      <Apparait debut={s(3.4, fps)} style={{marginTop: 34}}>
        <div style={{fontSize: 34, color: "#5b5f66"}}>Deux missions : <b style={{color: BLEU}}>vérifier nos hypothèses</b> et <b style={{color: BLEU}}>surveiller 5 concurrents</b>.</div>
      </Apparait>
      {MISSION.map((_, i) => <Tic key={i} a={s(0.8 + i * 0.55, fps)} vol={0.3} />)}
    </AbsoluteFill>
  );
};

// ---------- scène 4 : la boucle ----------
const NOEUDS = {
  plan: {x: 960, y: 300, n: "1", t: "Planifier", d: "découpe en étapes"},
  agir: {x: 1340, y: 560, n: "2", t: "Agir", d: "utilise un outil"},
  obs: {x: 960, y: 820, n: "3", t: "Observer", d: "lit la page"},
  verif: {x: 580, y: 560, n: "4", t: "Vérifier", d: "c’est sourcé ?"},
};
const W = 330, H = 116;
const P1: P[] = [[960 + W / 2, 300], [1340, 300], [1340, 560 - H / 2]];
const P2: P[] = [[1340, 560 + H / 2], [1340, 820], [960 + W / 2, 820]];
const P3: P[] = [[960 - W / 2, 820], [580, 820], [580, 560 + H / 2]];
const PR: P[] = [[580, 560 - H / 2], [580, 330], [960 - W / 2 - 4, 330]];
const PL: P[] = [[580 - W / 2, 560], [330, 560], [330, 800]];
const OUTILS = ["recherche web", "lecture de pages", "calcul", "tableur"];

const Noeud: React.FC<{k: keyof typeof NOEUDS; app: number; actif: number; couleur?: string}> = ({k, app, actif, couleur = BLEU}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const n = NOEUDS[k];
  const p = spring({frame: f - app, fps, config: {damping: 14, stiffness: 150}});
  return (
    <div style={{position: "absolute", left: n.x - W / 2, top: n.y - H / 2, width: W, height: H, background: actif > 0 ? "#fff" : "#fbfaf7",
      border: `${3 + actif * 3}px solid ${couleur}`, borderRadius: 18, padding: "14px 22px", transform: `scale(${p * (1 + actif * 0.06)})`, opacity: p,
      boxShadow: `0 ${8 + actif * 18}px ${20 + actif * 30}px rgba(0,40,90,${0.06 + actif * 0.12})`}}>
      <div style={{display: "flex", justifyContent: "space-between", alignItems: "baseline"}}>
        <span style={{fontFamily: MONO, fontSize: 28, color: couleur, fontWeight: 700}}>{n.n}</span>
        <span style={{fontSize: 38, fontWeight: 800, color: ENCRE}}>{n.t}</span>
      </div>
      <div style={{fontSize: 25, color: "#5b5f66", marginTop: 6}}>{n.d}</div>
    </div>
  );
};

const Scene4: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = f / fps;
  // chronologie (secondes dans la scène)
  const tour1 = [2.6, 3.9, 5.2, 6.5]; // départs : plan->agir, agir->obs, obs->verif, verif (refus)
  const reb = 7.6; // retour en arrière
  const tour2 = [8.8, 9.5, 10.2, 10.9]; // second tour plus rapide
  const fin = 11.6; // vers le livrable
  const seg = (a: number, d: number) => interpolate(t, [a, a + d], [0, 1], {...clamp, easing: ease});

  let pos: P = [NOEUDS.plan.x, NOEUDS.plan.y];
  let actif: keyof typeof NOEUDS | "" = "";
  if (t < tour1[0]) { pos = [NOEUDS.plan.x, NOEUDS.plan.y - H / 2 - 4]; actif = t > 2 ? "plan" : ""; }
  else if (t < tour1[1]) { pos = pointAlong(P1, seg(tour1[0], 0.8)); actif = seg(tour1[0], 0.8) >= 1 ? "agir" : ""; }
  else if (t < tour1[2]) { pos = pointAlong(P2, seg(tour1[1], 0.8)); actif = seg(tour1[1], 0.8) >= 1 ? "obs" : ""; }
  else if (t < reb) { pos = pointAlong(P3, seg(tour1[2], 0.8)); actif = seg(tour1[2], 0.8) >= 1 ? "verif" : ""; }
  else if (t < tour2[0]) { pos = pointAlong(PR, seg(reb, 0.9)); actif = seg(reb, 0.9) >= 1 ? "plan" : ""; }
  else if (t < tour2[1]) { pos = pointAlong(P1, seg(tour2[0], 0.55)); actif = "agir"; }
  else if (t < tour2[2]) { pos = pointAlong(P2, seg(tour2[1], 0.55)); actif = "obs"; }
  else if (t < fin) { pos = pointAlong(P3, seg(tour2[2], 0.55)); actif = "verif"; }
  else { pos = pointAlong(PL, seg(fin, 0.8)); actif = ""; }

  const refus = interpolate(t, [tour1[3], tour1[3] + 0.25, reb + 1.1, reb + 1.4], [0, 1, 1, 0], clamp);
  const oui = interpolate(t, [tour2[3], tour2[3] + 0.25], [0, 1], clamp);
  const flecheRetour = interpolate(t, [reb, reb + 0.9], [0, 1], clamp);
  const livrable = spring({frame: f - s(fin + 0.6, fps), fps, config: {damping: 13}});
  const outilsOn = interpolate(t, [tour1[0] + 0.8, tour1[0] + 1.0, tour1[1], tour1[1] + 0.2], [0, 1, 1, 0.35], clamp)
    + interpolate(t, [tour2[0] + 0.5, tour2[0] + 0.6, tour2[1], tour2[1] + 0.2], [0, 0.65, 0.65, 0], clamp);
  const outilIdx = Math.floor(interpolate(t, [tour1[0] + 0.8, tour1[1]], [0, 4], clamp));
  const compteur = (cible: number) => Math.round(interpolate(t, [fin + 0.8, fin + 2.2], [0, cible], {...clamp, easing: ease}));
  const ligneApp = (a: number) => interpolate(t, [a, a + 0.6], [0, 1], {...clamp, easing: ease});

  const trace = (pts: P[], prog: number, couleur: string, dash?: string) => {
    const L = lenOf(pts);
    return (
      <path d={dOf(pts)} fill="none" stroke={couleur} strokeWidth={6} strokeLinecap="round" strokeLinejoin="round"
        strokeDasharray={dash ?? `${L} ${L}`} strokeDashoffset={dash ? 0 : L * (1 - prog)} opacity={dash ? prog : 1}
        markerEnd={prog >= 0.999 ? `url(#pt-${couleur.slice(1)})` : undefined} />
    );
  };

  return (
    <AbsoluteFill style={{background: CREME, fontFamily: SANS}}>
      <div style={{position: "absolute", left: 120, top: 60}}>
        <div style={{fontFamily: MONO, fontSize: 26, color: BLEU, letterSpacing: 4, fontWeight: 700}}>COMMENT FIKA TRAVAILLE</div>
        <div style={{fontSize: 64, fontWeight: 800, color: ENCRE, letterSpacing: -1.5}}>La boucle de l’agent</div>
      </div>
      <svg width={1920} height={1080} style={{position: "absolute"}}>
        <defs>
          {[BLEU, VERT, ROUGE, ENCRE].map((c) => (
            <marker key={c} id={`pt-${c.slice(1)}`} markerWidth="4" markerHeight="4" refX="2.2" refY="2" orient="auto"><path d="M0,0 L4,2 L0,4 z" fill={c} /></marker>
          ))}
        </defs>
        {trace(P1, ligneApp(0.6), BLEU)}
        {trace(P2, ligneApp(0.9), BLEU)}
        {trace(P3, ligneApp(1.2), BLEU)}
        {trace(PL, ligneApp(fin), VERT)}
        <path d={dOf(PR)} fill="none" stroke={ROUGE} strokeWidth={5} strokeDasharray="16 14" opacity={flecheRetour} markerEnd={flecheRetour > 0.99 ? "url(#pt-D9472B)" : undefined} />
        <path d={dOf([[1340 + W / 2, 560], [1560, 560]])} stroke="#8a8d93" strokeWidth={4} strokeDasharray="8 10" opacity={ligneApp(1.4)} />
        <path d={dOf([[310, 272], [960 - W / 2 - 4, 272]])} stroke={ENCRE} strokeWidth={4} opacity={ligneApp(0.3)} markerEnd="url(#pt-111418)" />
      </svg>

      {/* Mission */}
      <Apparait debut={6} style={{position: "absolute", left: 60, top: 222}}>
        <div style={{width: 250, background: ENCRE, color: "#fff", borderRadius: 18, padding: "18px 22px"}}>
          <div style={{fontSize: 32, fontWeight: 800}}>Mission</div>
          <div style={{fontSize: 22, color: "#c9ced6", marginTop: 4}}>rôle, sources, format, règles</div>
        </div>
      </Apparait>

      {/* Modèle */}
      <div style={{position: "absolute", left: 960 - 120, top: 560 - 120, width: 240, height: 240, borderRadius: "50%", background: BLEU,
        display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", transform: `scale(${spring({frame: f - 10, fps, config: {damping: 15}}) * (1 + 0.03 * Math.sin(t * 4))})`}}>
        <div style={{fontSize: 46, fontWeight: 900, color: JAUNE}}>Modèle</div>
        <div style={{fontSize: 26, color: "#dbe7f4"}}>raisonne</div>
      </div>

      <Noeud k="plan" app={s(0.3, fps)} actif={actif === "plan" ? 1 : 0} />
      <Noeud k="agir" app={s(0.6, fps)} actif={actif === "agir" ? 1 : 0} />
      <Noeud k="obs" app={s(0.9, fps)} actif={actif === "obs" ? 1 : 0} />
      <Noeud k="verif" app={s(1.2, fps)} actif={actif === "verif" ? 1 : 0} couleur={t > tour1[3] && t < reb + 1.4 ? ROUGE : t > tour2[3] ? VERT : BLEU} />

      {/* Outils */}
      <Apparait debut={s(1.4, fps)} style={{position: "absolute", left: 1570, top: 440}}>
        <div style={{width: 300, background: "#fff", border: "3px dashed #9a9da3", borderRadius: 18, padding: "18px 24px"}}>
          <div style={{fontSize: 32, fontWeight: 800, color: ENCRE}}>Outils</div>
          {OUTILS.map((o, i) => (
            <div key={o} style={{fontSize: 25, marginTop: 6, display: "flex", alignItems: "center", gap: 10, color: outilsOn > 0.1 && i <= outilIdx ? BLEU : "#5b5f66", fontWeight: outilsOn > 0.1 && i <= outilIdx ? 800 : 400}}>
              <span style={{width: 12, height: 12, borderRadius: 6, background: outilsOn > 0.1 && i <= outilIdx ? JAUNE : "#d4d2cc"}} />{o}</div>
          ))}
        </div>
      </Apparait>

      {/* Refus */}
      <div style={{position: "absolute", left: 60, top: 680, opacity: refus, transform: `scale(${0.8 + refus * 0.2})`}}>
        <div style={{background: "#fff", border: `4px solid ${ROUGE}`, borderRadius: 14, padding: "14px 20px", width: 380}}>
          <div style={{fontFamily: MONO, fontSize: 26, color: ROUGE, fontWeight: 800}}>non : on reboucle</div>
          <div style={{fontSize: 18, color: "#5b5f66", marginTop: 2}}>test réel du garde-fou</div>
          <div style={{fontSize: 21, color: ENCRE, marginTop: 6, lineHeight: 1.3}}>{data.erreur_exemple}</div>
        </div>
      </div>
      <div style={{position: "absolute", left: 60, top: 600, opacity: oui, fontFamily: MONO, fontSize: 27, color: VERT, fontWeight: 800, lineHeight: 1.3}}>oui :<br />tout est<br />sourcé</div>

      {/* Livrable */}
      <div style={{position: "absolute", left: 120, top: 800, opacity: livrable, transform: `translateY(${(1 - livrable) * 30}px)`}}>
        <div style={{width: 420, background: VERT, color: "#fff", borderRadius: 18, padding: "18px 24px"}}>
          <div style={{fontSize: 34, fontWeight: 800}}>Livrable</div>
          <div style={{fontSize: 24, color: "#d8efe2"}}>tableau sourcé et daté</div>
        </div>
      </div>

      {/* Jeton */}
      <div style={{position: "absolute", left: pos[0] - 20, top: pos[1] - 20, width: 40, height: 40, borderRadius: "50%", background: JAUNE,
        border: `5px solid ${ENCRE}`, opacity: interpolate(t, [2, 2.3, fin + 0.8, fin + 1.0], [0, 1, 1, 0], clamp)}} />

      {/* Compteurs réels */}
      <div style={{position: "absolute", right: 70, bottom: 70, display: "flex", gap: 26, opacity: interpolate(t, [fin + 0.6, fin + 1], [0, 1], clamp)}}>
        {[{v: compteur(data.actions), l: "actions"}, {v: compteur(data.recherches), l: "recherches"}, {v: compteur(data.lectures), l: "pages lues"}, {v: compteur(data.boucles), l: "lignes sourcées"}].map((c) => (
          <div key={c.l} style={{background: "#fff", borderRadius: 14, padding: "10px 20px", borderTop: `6px solid ${JAUNE}`, textAlign: "center"}}>
            <div style={{fontSize: 48, fontWeight: 900, color: BLEU, lineHeight: 1.1}}>{c.v}</div>
            <div style={{fontSize: 20, color: "#5b5f66"}}>{c.l}</div>
          </div>
        ))}
      </div>

      {[0.3, 0.6, 0.9, 1.2].map((a) => <Tic key={a} a={s(a, fps)} vol={0.3} />)}
      {[tour1[0] + 0.8, tour1[1] + 0.8, tour1[2] + 0.8, tour2[0] + 0.55, tour2[1] + 0.55, tour2[2] + 0.55].map((a) => <Tic key={a} a={s(a, fps)} vol={0.35} />)}
      <Tic a={s(tour1[3], fps)} son="sfx/2202.mp3" vol={0.5} />
      <Tic a={s(tour2[3], fps)} son="sfx/1430.mp3" vol={0.55} />
      <Tic a={s(fin + 0.6, fps)} son="sfx/1430.mp3" vol={0.45} />
    </AbsoluteFill>
  );
};

// ---------- scène 5 : le tableau ----------
const COUL: Record<string, string> = {"Confirmé": "#D7EBDD", "Relevé": "#D7EBDD", "Nuancé": "#FFF1B3", "Infirmé": "#F6D2CC", "Non trouvé": "#E4E4E4"};
const Scene5: React.FC = () => {
  const {fps} = useVideoConfig();
  const cols = ["Id", "Question", "Chiffre", "Statut", "Source", "Date"];
  const larg = [220, 500, 230, 200, 330, 180];
  return (
    <AbsoluteFill style={{background: CREME, padding: "100px 120px", fontFamily: SANS}}>
      <Apparait debut={0}><Trait /></Apparait>
      <Apparait debut={4}><div style={{marginTop: 20, fontSize: 76, fontWeight: 800, color: BLEU, letterSpacing: -2}}>Le livrable : sourcé et daté.</div></Apparait>
      <div style={{marginTop: 46, background: "#fff", borderRadius: 22, overflow: "hidden", width: 1680, flexShrink: 0}}>
        <Apparait debut={s(0.5, fps)} dy={10}>
          <div style={{display: "flex", background: BLEU, color: "#fff", fontWeight: 800, fontSize: 30, padding: "18px 24px"}}>
            {cols.map((c, i) => <div key={c} style={{width: larg[i]}}>{c}</div>)}
          </div>
        </Apparait>
        {data.rangs.slice(0, 6).map((r, i) => (
          <Apparait key={r.id} debut={s(0.9 + i * 0.45, fps)} dy={20}>
            <div style={{display: "flex", alignItems: "center", fontSize: 30, padding: "18px 24px", borderBottom: "1px solid #ebe8e1", color: ENCRE}}>
              <div style={{width: larg[0], fontWeight: 800, color: BLEU, fontFamily: MONO}}>{r.id}</div>
              <div style={{width: larg[1], paddingRight: 20}}>{r.question}</div>
              <div style={{width: larg[2], fontWeight: 800, paddingRight: 20}}>{r.chiffre}</div>
              <div style={{width: larg[3]}}><span style={{background: COUL[r.statut] ?? "#eee", borderRadius: 8, padding: "4px 12px", fontWeight: 700, fontSize: 26}}>{r.statut}</span></div>
              <div style={{width: larg[4], color: BLEU, textDecoration: "underline", paddingRight: 16}}>{r.source}</div>
              <div style={{width: larg[5], fontFamily: MONO, fontSize: 24}}>{r.date}</div>
            </div>
          </Apparait>
        ))}
      </div>
      <Apparait debut={s(4.2, fps)} style={{marginTop: 30}}>
        <div style={{fontSize: 32, color: "#5b5f66"}}>Chaque extrait est recherché mot pour mot dans sa page par le contrôleur. Et quand Fika ne sait pas, il écrit <b style={{color: ENCRE, whiteSpace: "nowrap"}}>« Non trouvé »</b>.</div>
      </Apparait>
      {data.rangs.slice(0, 6).map((_, i) => <Tic key={i} a={s(0.9 + i * 0.45, fps)} vol={0.3} />)}
    </AbsoluteFill>
  );
};

// ---------- scène 6 : fin ----------
const Scene6: React.FC = () => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const p = spring({frame: f - 6, fps, config: {damping: 14}});
  return (
    <AbsoluteFill style={{background: BLEU, fontFamily: SANS, justifyContent: "center", alignItems: "center", textAlign: "center"}}>
      <div style={{fontSize: 120, fontWeight: 900, color: "#fff", letterSpacing: -3, transform: `scale(${0.9 + p * 0.1})`, opacity: p, lineHeight: 1.05}}>
        Zéro chiffre<br /><span style={{color: JAUNE}}>sans source.</span>
      </div>
      <Apparait debut={s(1.1, fps)}><div style={{marginTop: 44, fontSize: 40, color: "#dbe7f4"}}>Fika · l’agent de recherche IKÉASTRE</div></Apparait>
      <Apparait debut={s(1.6, fps)} style={{position: "absolute", bottom: 50}}>
        <div style={{fontSize: 22, color: "#a9c4e2"}}>Concept académique indépendant, non affilié à IKEA · B3CPD Ynov · Agent et vidéo réalisés avec l’IA · Musique : Vivaldi, Modena Chamber Orchestra (domaine public)</div>
      </Apparait>
      <Tic a={6} son="sfx/1492.mp3" vol={0.35} />
    </AbsoluteFill>
  );
};

// ---------- montage ----------
const PLAN: {c: React.FC; d: number}[] = [
  {c: Scene1, d: 6.2}, {c: Scene2, d: 4}, {c: Scene3, d: 6.3}, {c: Scene4, d: 16.5}, {c: Scene5, d: 8.5}, {c: Scene6, d: 5.5},
];
const Transition: React.FC<{children: React.ReactNode; d: number}> = ({children, d}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const o = interpolate(f, [0, 10, d * fps - 10, d * fps], [0, 1, 1, 0], clamp);
  const x = interpolate(f, [0, 14], [60, 0], {...clamp, easing: ease});
  return <AbsoluteFill style={{opacity: o, transform: `translateX(${x}px)`}}>{children}</AbsoluteFill>;
};

export const Fika: React.FC = () => {
  const {fps, durationInFrames} = useVideoConfig();
  let t = 0;
  const vol = (f: number) => interpolate(f, [0, 30, durationInFrames - 90, durationInFrames], [0, 0.32, 0.32, 0], clamp);
  return (
    <AbsoluteFill style={{background: CREME}}>
      {PLAN.map(({c: C, d}, i) => {
        const from = Math.round(t * fps);
        t += d;
        return (
          <Sequence key={i} from={from} durationInFrames={Math.round(d * fps)}>
            <Transition d={d}><C /></Transition>
          </Sequence>
        );
      })}
      <Audio src={staticFile("musique.wav")} volume={vol} />
    </AbsoluteFill>
  );
};
