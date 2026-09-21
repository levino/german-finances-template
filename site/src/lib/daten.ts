// Zugriff auf die JSONs, die site/scripts/generate-data.py schreibt.
// Kein Zustand, keine Mutation: alles hier ist lesen und ableiten.
import erklaerungJson from '../data/erklaerung.json';
import belegeJson from '../data/belege.json';
import aufgabenJson from '../data/aufgaben.json';
import metaJson from '../data/meta.json';

export type StatusName =
  | 'belegt' | 'kandidat' | 'offen' | 'zu-klaeren' | 'nicht-erklaeren' | 'ohne';

export const STATUS_TEXT: Record<StatusName, string> = {
  belegt: 'belegt',
  kandidat: 'Beleg fehlt',
  offen: 'offen',
  'zu-klaeren': 'zu entscheiden',
  'nicht-erklaeren': 'nicht angesetzt',
  ohne: '—',
};

export interface Buchung {
  datum: string;
  konto: string;
  payee: string;
  narration: string;
  betrag: string;
  belege: string[];
}

export interface Feld {
  zeile: string;
  feld: string;
  wert: string;
  quelle: string;
  quelle_belege: string[];
  status: StatusName;
  summe?: boolean;
  herleitung: Buchung[];
}

export interface Gruppe { titel: string; felder: Feld[]; }
export interface Block {
  titel: string; id: string; gruppen: Gruppe[];
  felder_gesamt: number; offen: number;
}
export interface Formular {
  titel: string; id: string; bloecke: Block[];
  felder_gesamt: number; offen: number;
}
export interface Jahr {
  jahr: string; dokumente: Formular[];
  felder_gesamt: number; belegt: number; vorlaeufig: number; offen: number;
}

export const erklaerung = erklaerungJson as unknown as Record<string, Jahr>;

export const belege = belegeJson as unknown as {
  belege: Array<{
    pfad: string; jahr: string; datum: string | null; bezeichnung: string;
    ausgangsrechnung: boolean;
    buchungen: Array<{ datum: string; payee: string; narration: string }>;
  }>;
  tote_verweise: Array<{ datum: string; verweis: string }>;
  kennzahlen: Record<string, number>;
};

export const aufgaben = aufgabenJson as unknown as
  Record<string, { offen: string[]; erledigt: string[] }>;

export const meta = metaJson as unknown as { erzeugt: string; jahre: string[] };

/** Alle Jahre, von denen etwas vorliegt — das jüngste zuerst. */
export const jahre: string[] = [...new Set([
  ...Object.keys(erklaerung),
  ...Object.keys(aufgaben),
  ...belege.belege.map((b) => b.jahr),
])].sort().reverse();

export const formulareVon = (jahr: string): Formular[] =>
  erklaerung[jahr]?.dokumente ?? [];

export const belegeVon = (jahr: string) =>
  belege.belege.filter((b) => b.jahr === jahr);

export const offeneAufgaben = (jahr: string): string[] =>
  aufgaben[jahr]?.offen ?? [];

export function formatDatum(iso: string | null): string {
  if (!iso) return '—';
  const [j, m, t] = iso.split('-');
  return `${t}.${m}.${j}`;
}
