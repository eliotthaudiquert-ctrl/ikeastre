import React from "react";
import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig, Easing} from "remotion";
import {loadFont} from "@remotion/fonts";
import {SCENES, FIN, Scene, Tag, dureeScene} from "./scenes";
import voix from "./voix.json";

loadFont({family: "Archivo Black", url: staticFile("fonts/ArchivoBlack.ttf")});
loadFont({family: "Archivo", url: staticFile("fonts/Archivo.ttf"), weight: "100 900"});
loadFont({family: "Archivo", url: staticFile("fonts/ArchivoItalic.ttf"), weight: "100 900", style: "italic"});

const JAUNE = "#FFDA1A";
const BLEU = "#0058A3";
const NOIR = "#111111";
const LARGEUR = 600;

// ---------- Étiquette produit ----------

const Etoile: React.FC<{taille: number}> = ({taille}) => {
  const n = 14, r1 = taille / 2, r2 = r1 * 0.84;
  const pts = Array.from({length: n * 2}, (_, i) => {
    const r = i % 2 ? r2 : r1, a = (Math.PI * i) / n;
    return `${r1 + r * Math.sin(a)},${r1 - r * Math.cos(a)}`;
  }).join(" ");
  return (
    <svg width={taille} height={taille} style={{position: "absolute", inset: 0, filter: "drop-shadow(0 6px 10px rgba(0,0,0,.35))"}}>
      <polygon points={pts} fill={BLEU} stroke={NOIR} strokeWidth={3} strokeLinejoin="round" />
    </svg>
  );
};

export const Etiquette: React.FC<{tag: Tag; t: number}> = ({tag, t}) => {
  const {fps} = useVideoConfig();
  const pop = spring({frame: t, fps, config: {damping: 11, stiffness: 170, mass: 0.7}});
  const badge = spring({frame: t - 0.22 * fps, fps, config: {damping: 9, stiffness: 200, mass: 0.6}});
  const tailleNom = Math.min(78, 520 / (tag.nom.length * 0.88));
  return (
    <div style={{position: "relative", width: LARGEUR, transform: `scale(${0.55 + 0.45 * pop})`, opacity: Math.min(1, pop * 2.2), transformOrigin: "30% 60%"}}>
      <div style={{background: JAUNE, border: `3px solid ${NOIR}`, borderRadius: 18, padding: "26px 30px 22px", boxShadow: "0 18px 40px rgba(0,0,0,.45)", color: NOIR}}>
        <div style={{display: "inline-block", background: NOIR, color: JAUNE, borderRadius: 999, padding: "6px 16px", fontFamily: "Archivo", fontWeight: 800, fontSize: 19, letterSpacing: 1.5, textTransform: "uppercase"}}>
          {tag.num} · {tag.type}
        </div>
        <div style={{fontFamily: "Archivo Black", fontSize: tailleNom, lineHeight: 1.02, marginTop: 14, letterSpacing: -0.5}}>{tag.nom}</div>
        <div style={{fontFamily: "Archivo", fontStyle: "italic", fontWeight: 800, fontSize: 29, lineHeight: 1.18, marginTop: 12, maxWidth: 500}}>{tag.accroche}</div>
        <div style={{height: 3, background: NOIR, margin: "18px 0 12px"}} />
        <div style={{fontFamily: "Archivo", fontWeight: 600, fontSize: 19}}>{tag.infos}</div>
      </div>
      <div style={{position: "absolute", right: -58, top: -86, width: 150, height: 150, transform: `scale(${badge}) rotate(${10 - 10 * badge + 8}deg)`}}>
        <Etoile taille={150} />
        <div style={{position: "absolute", inset: 0, display: "flex", alignItems: "center", justifyContent: "center", fontFamily: "Archivo Black", color: JAUNE, fontSize: tag.prix.length > 5 ? 34 : 46, letterSpacing: -0.5}}>
          {tag.prix}
        </div>
      </div>
    </div>
  );
};

// ---------- Flèche dessinée ----------

const Fleche: React.FC<{de: [number, number]; vers: [number, number]; progres: number}> = ({de, vers, progres}) => {
  const [x1, y1] = de, [x2, y2] = vers;
  const dx = x2 - x1, dy = y2 - y1, L = Math.hypot(dx, dy);
  // Courbe en arc, bombée vers le haut.
  let nx = -dy / L, ny = dx / L;
  if (ny > 0) { nx = -nx; ny = -ny; }
  const cx = (x1 + x2) / 2 + nx * L * 0.22, cy = (y1 + y2) / 2 + ny * L * 0.22;
  const d = `M ${x1} ${y1} Q ${cx} ${cy} ${x2} ${y2}`;
  const longueur = L * 1.15;
  const ang = Math.atan2(y2 - cy, x2 - cx);
  const tete = (s: number) => {
    const a1 = ang + Math.PI * 0.82, a2 = ang - Math.PI * 0.82;
    return `M ${x2 + Math.cos(a1) * s} ${y2 + Math.sin(a1) * s} L ${x2} ${y2} L ${x2 + Math.cos(a2) * s} ${y2 + Math.sin(a2) * s}`;
  };
  const off = longueur * (1 - progres);
  const teteOp = progres > 0.96 ? 1 : 0;
  return (
    <svg width={1920} height={1080} style={{position: "absolute", inset: 0, overflow: "visible"}}>
      <path d={d} fill="none" stroke={NOIR} strokeWidth={15} strokeLinecap="round" strokeDasharray={longueur} strokeDashoffset={off} />
      <path d={d} fill="none" stroke="#fff" strokeWidth={8} strokeLinecap="round" strokeDasharray={longueur} strokeDashoffset={off} />
      <path d={tete(34)} fill="none" stroke={NOIR} strokeWidth={15} strokeLinecap="round" strokeLinejoin="round" opacity={teteOp} />
      <path d={tete(34)} fill="none" stroke="#fff" strokeWidth={8} strokeLinecap="round" strokeLinejoin="round" opacity={teteOp} />
    </svg>
  );
};

const departFleche = (s: Scene, h: number): [number, number] => {
  const {x, y} = s.carte, [tx, ty] = s.cible;
  if (tx < x) return [x - 8, y + h * 0.55];
  if (tx > x + LARGEUR) return [x + LARGEUR + 8, y + h * 0.55];
  if (ty > y + h) return [x + LARGEUR * 0.35, y + h + 8];
  return [x + LARGEUR * 0.35, y - 8];
};

// ---------- Une scène ----------

const SceneVue: React.FC<{s: Scene}> = ({s}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const fGel = Math.round((s.gel - s.de) * fps);
  const fPause = Math.round(s.pause * fps);
  const tGel = frame - fGel;
  const fige = tGel >= 0 && tGel < fPause;
  const zoom = fige ? interpolate(tGel, [0, fPause], [1.0, 1.04], {easing: Easing.out(Easing.quad)}) : 1;
  const flash = fige ? interpolate(tGel, [0, 5], [0.45, 0], {extrapolateRight: "clamp"}) : 0;
  const hauteurCarte = 255;
  const fleche = interpolate(tGel, [0.32 * fps, 0.78 * fps], [0, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.inOut(Easing.cubic)});
  const sortie = interpolate(tGel, [fPause - 7, fPause], [1, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
  return (
    <AbsoluteFill style={{background: "#000"}}>
      <Sequence durationInFrames={fGel}>
        <OffthreadVideo src={staticFile(`clips/${s.clip}.mp4`)} trimBefore={Math.round(s.de * fps)} muted style={{width: "100%", height: "100%", objectFit: "cover"}} />
      </Sequence>
      <Sequence from={fGel} durationInFrames={fPause}>
        <AbsoluteFill style={{transform: `scale(${zoom})`, transformOrigin: `${s.cible[0]}px ${s.cible[1]}px`}}>
          <Img src={staticFile(`stills/${s.clip}.jpg`)} style={{width: "100%", height: "100%", objectFit: "cover"}} />
        </AbsoluteFill>
        <AbsoluteFill style={{background: "#fff", opacity: flash}} />
        <AbsoluteFill style={{opacity: sortie}}>
          <Fleche de={departFleche(s, hauteurCarte)} vers={s.cible} progres={fleche} />
          <div style={{position: "absolute", left: s.carte.x, top: s.carte.y, transform: `rotate(${s.carte.rot}deg)`}}>
            <Etiquette tag={s.tag} t={tGel - Math.round(0.1 * fps)} />
          </div>
        </AbsoluteFill>
      </Sequence>
      {s.reprise ? (
        <Sequence from={fGel + fPause}>
          <OffthreadVideo src={staticFile(`clips/${s.clip}.mp4`)} trimBefore={Math.round(s.gel * fps)} muted style={{width: "100%", height: "100%", objectFit: "cover"}} />
        </Sequence>
      ) : null}
      {/* Sons de la scène */}
      {s.repliques.map((r, i) => (
        <Sequence key={i} from={Math.round(r.a * fps)}>
          <Audio src={staticFile(r.son)} volume={r.vol ?? 1} />
        </Sequence>
      ))}
      <Sequence from={fGel}><Audio src={staticFile("sfx/1430.mp3")} volume={0.55} /></Sequence>
      <Sequence from={fGel - Math.round(0.25 * fps)}><Audio src={staticFile("sfx/1492.mp3")} volume={0.35} /></Sequence>
      <Sequence from={fGel + Math.round(0.1 * fps)}><Audio src={staticFile("sfx/2364.mp3")} volume={0.5} /></Sequence>
      <Sequence from={fGel + Math.round(0.32 * fps)}><Audio src={staticFile("sfx/2998.mp3")} volume={0.45} /></Sequence>
    </AbsoluteFill>
  );
};

// ---------- Carte de fin ----------

const POSITIONS = [
  {x: 70, y: 60, r: -6}, {x: 760, y: 30, r: 3}, {x: 1440, y: 70, r: 6},
  {x: 90, y: 760, r: 5}, {x: 780, y: 800, r: -3}, {x: 1450, y: 740, r: -6},
];

const Fin: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const titre = spring({frame: frame - 0.5 * fps, fps, config: {damping: 13, stiffness: 160}});
  const pill = spring({frame: frame - 0.9 * fps, fps, config: {damping: 12, stiffness: 180}});
  return (
    <AbsoluteFill style={{background: JAUNE}}>
      {SCENES.map((s, i) => (
        <div key={i} style={{position: "absolute", left: POSITIONS[i].x, top: POSITIONS[i].y, transform: `rotate(${POSITIONS[i].r}deg) scale(0.62)`, transformOrigin: "top left"}}>
          <Etiquette tag={s.tag} t={frame - i * 4} />
        </div>
      ))}
      <AbsoluteFill style={{alignItems: "center", justifyContent: "center"}}>
        <div style={{textAlign: "center", transform: `scale(${0.7 + 0.3 * titre})`, opacity: Math.min(1, titre * 2)}}>
          <div style={{fontFamily: "Archivo Black", fontSize: 84, lineHeight: 1.0, color: NOIR, letterSpacing: -1}}>
            DES MEUBLES POUR TOUS<br />LES REBONDISSEMENTS.
          </div>
        </div>
        <div style={{marginTop: 34, background: NOIR, color: JAUNE, borderRadius: 999, padding: "14px 34px", fontFamily: "Archivo", fontWeight: 800, fontSize: 30, transform: `scale(${pill})`}}>
          Tout est sur ikea.fr →
        </div>
      </AbsoluteFill>
      <div style={{position: "absolute", bottom: 26, width: "100%", textAlign: "center", fontFamily: "Archivo", fontWeight: 600, fontSize: 17, color: NOIR, opacity: 0.75}}>
        Prix relevés sur ikea.fr le 29/10/2026.
      </div>
      <Audio src={staticFile("sfx/1490.mp3")} volume={0.4} />
      {SCENES.map((_, i) => (
        <Sequence key={i} from={i * 4}><Audio src={staticFile("sfx/3005.mp3")} volume={0.35} /></Sequence>
      ))}
      <Sequence from={Math.round(0.5 * fps)}><Audio src={staticFile("sfx/2364.mp3")} volume={0.5} /></Sequence>
    </AbsoluteFill>
  );
};

// ---------- Montage ----------

const fenetresVoix = (fps: number) => {
  const f: [number, number][] = [];
  let t = 0;
  for (const s of SCENES) {
    for (const r of s.repliques) {
      const k = r.son.match(/voix\/(l\d)r/)?.[1] as keyof typeof voix | undefined;
      if (k) f.push([(t + r.a) * fps, (t + r.a + voix[k] + 0.15) * fps]);
    }
    t += dureeScene(s);
  }
  return f;
};

export const Reel: React.FC = () => {
  const {fps, durationInFrames} = useVideoConfig();
  const fen = fenetresVoix(fps);
  const volMusique = (f: number) => {
    const base = 0.6;
    let duck = 1;
    for (const [a, b] of fen) {
      const v = interpolate(f, [a - 8, a, b, b + 14], [1, 0.24, 0.24, 1], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
      duck = Math.min(duck, v);
    }
    const fondu = interpolate(f, [durationInFrames - 1.2 * fps, durationInFrames - 2], [1, 0], {extrapolateLeft: "clamp", extrapolateRight: "clamp"});
    return base * duck * fondu;
  };
  let debut = 0;
  return (
    <AbsoluteFill style={{background: "#000"}}>
      {SCENES.map((s, i) => {
        const d = Math.round(dureeScene(s) * fps);
        const el = (
          <Sequence key={i} from={debut} durationInFrames={d}>
            <SceneVue s={s} />
          </Sequence>
        );
        debut += d;
        return el;
      })}
      <Sequence from={debut} durationInFrames={Math.round(FIN * fps)}>
        <Fin />
      </Sequence>
      <Audio src={staticFile("musique.wav")} volume={volMusique} />
    </AbsoluteFill>
  );
};
