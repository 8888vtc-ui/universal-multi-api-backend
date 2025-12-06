
import fs from 'fs';
import path from 'path';
import { SEO_ARTICLES } from './seo-articles';

const OUTPUT_DIR = path.resolve(__dirname, '../../backend/data/articles');

if (!fs.existsSync(OUTPUT_DIR)) {
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

console.log(`Starting migration script...`);
console.log(`Output directory: ${OUTPUT_DIR}`);
console.log(`Articles found: ${Object.keys(SEO_ARTICLES).length}`);


let count = 0;
for (const [slug, article] of Object.entries(SEO_ARTICLES)) {
    const filePath = path.join(OUTPUT_DIR, `${slug}.json`);

    // Add slug to the object if it's missing (useful context)
    const articleData = {
        slug,
        ...article
    };

    fs.writeFileSync(filePath, JSON.stringify(articleData, null, 2));
    count++;

    if (count % 100 === 0) {
        console.log(`Migrated ${count} articles...`);
    }
}

console.log(`✅ Successfully migrated ${count} articles.`);
