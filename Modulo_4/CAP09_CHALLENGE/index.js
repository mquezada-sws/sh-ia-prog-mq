
import dotenv from "dotenv";
dotenv.config();

import fs from "fs";
import path from "path";
import fetch from "node-fetch";

// LangChain imports
import { OpenAI } from "langchain/llms/openai";
import { OpenAIEmbeddings } from "langchain/embeddings/openai";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";

// Attempt to import RecursiveUrlLoader. Depending on langchain version/path this may change.
let RecursiveUrlLoader;
try {
  // path used by docs: integrations/document_loaders/web_loaders/recursive_url_loader
  RecursiveUrlLoader = (await import("langchain/document_loaders/web/recursive_url_loader")).RecursiveUrlLoader;
} catch (e) {
  try {
    // alternative path
    RecursiveUrlLoader = (await import("langchain/document_loaders/web/recursive_url_loader/recursive_url_loader")).RecursiveUrlLoader;
  } catch (err) {
    RecursiveUrlLoader = null;
    console.warn("RecursiveUrlLoader no disponible en esta versión de langchain. Se usará fallback simple de fetch.");
  }
}

// --- Config
const SEED_URLS = [
  "https://cnnespanol.cnn.com/lite/",
  "https://www.cbc.ca/lite/news?sort=latest",
];
const MAX_CRAWL_DEPTH = 1; // aumentar según necesidad
const CHUNK_SIZE = 1000;
const CHUNK_OVERLAP = 200;
const TOP_K = 4;
const RELEVANCE_THRESHOLD = 0.70; // umbral (0..1) para decidir si hay contexto suficiente

// --- In-memory store: { id, text, metadata, embedding }
const INDEX = [];

// --- Helpers
function cosineSimilarity(a, b) {
  let dot = 0;
  let na = 0;
  let nb = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    na += a[i] * a[i];
    nb += b[i] * b[i];
  }
  if (na === 0 || nb === 0) return 0;
  return dot / (Math.sqrt(na) * Math.sqrt(nb));
}

// Simple fetch + extract text fallback (very naive HTML->text)
async function fetchPageText(url) {
  const res = await fetch(url, { headers: { "User-Agent": "news-bot/1.0" } });
  const html = await res.text();
  // strip tags (naive)
  const text = html.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, "")
                   .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, "")
                   .replace(/<[^>]+>/g, " ")
                   .replace(/\s+/g, " ")
                   .trim();
  return text;
}

// Load documents using RecursiveUrlLoader or fallback
async function loadDocuments(seedUrls = SEED_URLS, depth = MAX_CRAWL_DEPTH) {
  console.log("Cargando documentos desde:", seedUrls);
  let rawDocs = [];
  if (RecursiveUrlLoader) {
    const loader = new RecursiveUrlLoader({
      urls: seedUrls,
      maxDepth: depth,
      allowedDomains: ["cnnespanol.cnn.com", "www.cbc.ca"],
    });
    rawDocs = await loader.load(); // devuelve array de Document { pageContent, metadata }
  } else {
    // fallback: solo descarga semilla
    for (const url of seedUrls) {
      try {
        const text = await fetchPageText(url);
        rawDocs.push({ pageContent: text, metadata: { source: url } });
      } catch (e) {
        console.warn("Error fetch", url, e.message);
      }
    }
  }
  console.log(`Se cargaron ${rawDocs.length} documentos (raw).`);
  return rawDocs;
}

// Split, embed and index
async function indexDocuments(docs) {
  console.log("Indexando documentos...");
  const textSplitter = new RecursiveCharacterTextSplitter({
    chunkSize: CHUNK_SIZE,
    chunkOverlap: CHUNK_OVERLAP,
  });

  const embeddings = new OpenAIEmbeddings({ openAIApiKey: process.env.OPENAI_API_KEY });

  let idCounter = INDEX.length;
  for (const d of docs) {
    const chunks = await textSplitter.splitDocuments([{ pageContent: d.pageContent, metadata: d.metadata }]);
    for (const c of chunks) {
      const emb = await embeddings.embedQuery(c.pageContent);
      INDEX.push({ id: (++idCounter).toString(), text: c.pageContent, metadata: c.metadata || {}, embedding: emb });
    }
  }
  console.log(`INDEX contiene ahora ${INDEX.length} chunks.`);
}

// Query: decide whether to answer with news context or general knowledge
async function queryNews(question) {
  const embeddings = new OpenAIEmbeddings({ openAIApiKey: process.env.OPENAI_API_KEY });
  const llm = new OpenAI({ openAIApiKey: process.env.OPENAI_API_KEY, temperature: 0.0 });

  // embed question
  const qEmb = await embeddings.embedQuery(question);

  // compute similarities
  const sims = INDEX.map((item) => ({ id: item.id, score: cosineSimilarity(qEmb, item.embedding), text: item.text, metadata: item.metadata }));
  sims.sort((a, b) => b.score - a.score);
  const top = sims.slice(0, TOP_K);

  console.log("Top similitudes:", top.map(t => ({id: t.id, score: t.score.toFixed(3)})));

  if (top.length > 0 && top[0].score >= RELEVANCE_THRESHOLD) {
    // Usar contexto: concatenar los top-k textos (con cuidado de longitud)
    const contextPieces = top.map(t => `FUENTE: ${t.metadata.source || "desconocida"}\n${t.text.slice(0, 2000)}`);
    const context = contextPieces.join("\n\n---\n\n");

    const prompt = `Eres un asistente que responde preguntas sobre noticias. Usa SOLO la información proporcionada en CONTEXTO para responder con precisión. Si la respuesta no puede ser determinada a partir del contexto, di que no hay información suficiente y ofrece resumir lo que hay.

CONTEXT: ${context}

PREGUNTA: ${question}\n\nRESPUESTA (en español):`;

    const response = await llm.call(prompt);
    return { type: "news_specific", answer: response, top }; // response es texto plano
  } else {
    // Respuesta general (usar LLM sin contexto, permitir conocimiento general)
    const promptGeneral = `Eres un asistente que responde preguntas sobre noticias y contexto general. Responde la siguiente pregunta de forma clara y concisa en español:\n\nPREGUNTA: ${question}`;
    const response = await llm.call(promptGeneral);
    return { type: "general_knowledge", answer: response, top };
  }
}

// --- Ejecución de ejemplo
async function main() {
  if (!process.env.OPENAI_API_KEY) {
    console.error("Define OPENAI_API_KEY en .env");
    process.exit(1);
  }

  const rawDocs = await loadDocuments();
  await indexDocuments(rawDocs);

  // ejemplos de consulta
  const preguntas = [
    "¿Cuál es la noticia más reciente sobre economía en CNN Español?",
    "Explícame qué es la inflación y cómo afecta a los ciudadanos.",
  ];

  for (const p of preguntas) {
    console.log('\n=== PREGUNTA:', p);
    const r = await queryNews(p);
    console.log('Tipo de respuesta:', r.type);
    console.log('Respuesta:');
    console.log(r.answer);
  }
}

// Solo ejecutar si es el script principal
if (process.argv[1] && process.argv[1].endsWith(path.basename(import.meta.url))) {
  main();
}

export { loadDocuments, indexDocuments, queryNews, INDEX };
