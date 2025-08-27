import { RecursiveUrlLoader } from "@langchain/community/document_loaders/web/recursive_url";
import { StringOutputParser } from "@langchain/core/output_parsers";
import { ChatPromptTemplate } from "@langchain/core/prompts";
import { RunnablePassthrough, RunnableSequence } from "@langchain/core/runnables";
import { ChatOpenAI, OpenAIEmbeddings } from "@langchain/openai";
import { compile } from "html-to-text";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
import { MemoryVectorStore } from "langchain/vectorstores/memory";
import readline from "readline";


// Document loaders configuration
const compiledConvert = compile({ wordwrap: 130 }); 

const cnnLoader = new RecursiveUrlLoader("https://cnnespanol.cnn.com/lite/", {
  extractor: compiledConvert,
  maxDepth: 2,
  excludeDirs: ["/lite/api/"],
});

const cbcLoader = new RecursiveUrlLoader("https://www.cbc.ca/lite/news?sort=latest", {
  extractor: compiledConvert,
  maxDepth: 2,
  excludeDirs: ["/lite/api/"],
});

// Initialize GroqAI model
const model = new ChatOpenAI({ model: "gpt-3.5-turbo" });
const parser = new StringOutputParser();

// Classification template and chain
const classificationPrompt = ChatPromptTemplate.fromTemplate(`Classify the following question as 'news' or 'general. Only respond with one of both words.':\n{question}`);

const classificationChain = RunnableSequence.from([
  classificationPrompt,
  model,
  parser
]);

// Setup retrieval and response chains for news
async function setupNewsChain() {
    const cnnDocs = await cnnLoader.load();
    const cbcDocs = await cbcLoader.load();
    const allDocs = cnnDocs.concat(cbcDocs);

    let docs = allDocs.filter(item => item.pageContent.trim() !== "");

    const textSplitter = new RecursiveCharacterTextSplitter({
        chunkSize: 1000,
        chunkOverlap: 200,
      });
    const allSplits = await textSplitter.splitDocuments(docs);
   

    // Create a vector store from the documents
    const vectorStore = await MemoryVectorStore.fromDocuments(allSplits, new OpenAIEmbeddings());


    // Initialize a retriever wrapper around the vector store
    const vectorStoreRetriever = vectorStore.asRetriever();



    const SYSTEM_TEMPLATE = `Use the following pieces of context to answer the question at the end.
                            If you don't know the answer, just say that you don't know, don't try to make up an answer.
                            ----------------
                            {context}`;

    const newsPrompt = ChatPromptTemplate.fromMessages([
        ["system", SYSTEM_TEMPLATE],
        ["human", "{question}"],
    ]);
    
    const formatDocumentsAsString = (documents) => {
        return documents.map((document) => document.pageContent).join("\n\n");
    };

    const chain = RunnableSequence.from([
        {
            context: vectorStoreRetriever.pipe(formatDocumentsAsString),
            question: new RunnablePassthrough(),
        },
        newsPrompt,
        model,
        new StringOutputParser()
    ]);
    
    
    return chain
}

const generalChain = RunnableSequence.from([
  ChatPromptTemplate.fromTemplate(`Answer the following general question:\n{question}`),
  model,
  parser
]);

const newsChain = await setupNewsChain();

// Routing logic based on the classification
async function routeQuestion(question) {
    const classification = await classificationChain.invoke({ "question": question });
  if (classification.toLowerCase() === 'news') {
    return await newsChain.invoke(question);
  } else {
    return await generalChain.invoke({ "question": question });
  }
}

// Setting up readline for interaction
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

rl.on('line', async (line) => {
  const question = line.trim();
  if (question.toLowerCase() === "exit") {
    rl.close();
  } else {
    // Invoke routing logic based on classification
    const answer = await routeQuestion(question);
    console.log("Response:", answer);
    rl.prompt();
  }
});

rl.setPrompt('Ask a question: ');
rl.prompt();
