// Montage : chaque scène joue un extrait, se fige sur une étiquette produit, puis on coupe.
// Positions en pixels sur une image 1920×1080. Prix relevés sur ikea.com/fr le 29/10/2026.

export type Tag = {
  num: string;
  type: string;
  nom: string;
  accroche: string;
  infos: string;
  prix: string;
};

export type Scene = {
  clip: string;
  de: number; // début de l'extrait (s)
  gel: number; // instant figé (s)
  pause: number; // durée du gel (s)
  reprise?: number; // durée de lecture après le gel (s)
  repliques: {son: string; a: number; vol?: number}[]; // a : secondes depuis le début de la scène
  tag: Tag;
  carte: {x: number; y: number; rot: number};
  cible: [number, number];
};

export const SCENES: Scene[] = [
  {
    clip: "25578", de: 9.0, gel: 14.5, pause: 2.8,
    repliques: [{son: "voix/l1r.wav", a: 0.5}, {son: "voix/l2r.wav", a: 2.7}],
    tag: {num: "N°1", type: "Sac", nom: "FRAKTA", accroche: "71 litres. Pile la taille d'une rupture.", infos: "Grand sac · 55×37×35 cm · 71 l", prix: "1 €"},
    carte: {x: 70, y: 330, rot: -2.5}, cible: [1300, 800],
  },
  {
    clip: "46377", de: 0.3, gel: 3.5, pause: 2.6,
    repliques: [{son: "voix/l3r.wav", a: 0.15, vol: 0.8}, {son: "sfx/565.mp3", a: 1.75, vol: 0.7}, {son: "sfx/scream_tv.wav", a: 1.9, vol: 0.55}],
    tag: {num: "N°2", type: "Saladier", nom: "TRYGG", accroche: "Tient tout le film d'horreur. Vos nerfs, moins.", infos: "Saladier en verre · Ø 28 cm", prix: "2,99 €"},
    carte: {x: 1240, y: 150, rot: 2}, cible: [1065, 840],
  },
  {
    clip: "45735", de: 1.3, gel: 4.5, pause: 2.6,
    repliques: [{son: "voix/l4r.wav", a: 0.45}],
    tag: {num: "N°3", type: "Chaise gaming", nom: "HUVUDSPELARE", accroche: "Encaisse les défaites. Et les cris.", infos: "Chaise gaming · noir", prix: "79,99 €"},
    carte: {x: 60, y: 660, rot: -2}, cible: [330, 420],
  },
  {
    clip: "39536", de: 0.3, gel: 3.5, pause: 2.6,
    repliques: [{son: "voix/l5r.wav", a: 0.25}],
    tag: {num: "N°4", type: "Oreiller", nom: "SANDGRÄSMAL", accroche: "Conçu pour dormir. Utilisé pour se venger.", infos: "Oreiller · 65×65 cm", prix: "4,49 €"},
    carte: {x: 1250, y: 620, rot: 2.5}, cible: [1010, 600],
  },
  {
    clip: "41325", de: 9.0, gel: 12.0, pause: 2.6,
    repliques: [{son: "voix/l6r.wav", a: 0.45}],
    tag: {num: "N°5", type: "Canapé", nom: "KLIPPAN", accroche: "A tout vu. Ne dira rien.", infos: "Canapé 2 places", prix: "279 €"},
    carte: {x: 1240, y: 70, rot: -2}, cible: [1420, 820],
  },
  {
    clip: "42245", de: 0.0, gel: 2.2, pause: 2.6, reprise: 4.4,
    repliques: [{son: "voix/l7r.wav", a: 0.05}, {son: "voix/l8r.wav", a: 2.2 + 2.6 + 1.9}],
    tag: {num: "N°6", type: "Matelas", nom: "VESTMARKA", accroche: "Après 4 h de montage, vous l'avez mérité.", infos: "Matelas à ressorts · 140×200 cm · ferme", prix: "169 €"},
    carte: {x: 1250, y: 70, rot: 2}, cible: [330, 830],
  },
];

export const FIN = 5.2; // carte de fin (s)

export const dureeScene = (s: Scene) => s.gel - s.de + s.pause + (s.reprise ?? 0);
export const DUREE = SCENES.reduce((t, s) => t + dureeScene(s), 0) + FIN;
