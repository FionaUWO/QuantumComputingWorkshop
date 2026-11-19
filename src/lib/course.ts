import { getCollection, type CollectionEntry } from 'astro:content';
import { lectures, type LectureInfo } from '../data/lectures';
import { url } from './url';

export interface Section {
  slug: string;      // URL segment, e.g. "the-bloch-sphere"
  num: number;       // position within the lecture, from 1
  title: string;
  href: string;
  entry: CollectionEntry<'lectures'>;
}

export interface Lecture extends LectureInfo {
  href: string;      // the lecture's opening page
  sections: Section[];
}

// Every lecture with its sections in order. A lecture without section files has an empty list.
export async function getCourse(): Promise<Lecture[]> {
  const entries = await getCollection('lectures');
  return lectures.map((info) => {
    const sections = entries
      .filter((e) => e.id.startsWith(`${info.slug}/`))
      .sort((a, b) => a.id.localeCompare(b.id))
      .map((entry, i) => {
        const slug = entry.id.slice(info.slug.length + 1).replace(/^\d+-/, '');
        return { slug, num: i + 1, title: entry.data.title, href: url(`lectures/${info.slug}/${slug}/`), entry };
      });
    return { ...info, href: url(`lectures/${info.slug}/`), sections };
  });
}
