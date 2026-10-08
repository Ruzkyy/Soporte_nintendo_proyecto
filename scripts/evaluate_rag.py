import sys
import os
import json
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
from datasets import Dataset
from ragas import evaluate
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)

# Wrapper function for Gemini model for Ragas (needs langchain/langchain-google-genai interface usually)
# For simplicity with Ragas v0.2.x, we recommend installing langchain-google-genai to pass the LLM.
# Wait, Ragas needs Langchain chat models. I need to make sure the user installs `langchain-google-genai`.
# I'll use the native Assistant to get answers, and Ragas only to evaluate.

from src.assistant import SupportAssistant

def main():
    print("Iniciando evaluación del pipeline RAG...")
    assistant = SupportAssistant()
    
    dataset_path = Path("data/eval_dataset.json")
    if not dataset_path.exists():
        print("Dataset de evaluación no encontrado.")
        return

    with open(dataset_path, "r", encoding="utf-8") as f:
        qa_data = json.load(f)

    questions = []
    ground_truths = []
    answers = []
    contexts = []

    print(f"Evaluando {len(qa_data)} preguntas...")
    for item in qa_data:
        q = item["question"]
        gt = item["ground_truth"]
        
        # Obtener respuesta del RAG
        # Primero necesitamos el contexto recuperado (simularemos la llamada o usaremos vector_store directo)
        retrieved_items = assistant.vector_store.retrieve(q, top_k=3)
        context_list = [c["chunk"] for c in retrieved_items] if retrieved_items else [""]
        
        # Obtener respuesta final
        resp = assistant.answer(q)
        answer_text = resp.get("resumen", "") + " " + resp.get("diagnostico", "")
        
        questions.append(q)
        ground_truths.append(gt)
        answers.append(answer_text)
        contexts.append(context_list)

    # Preparar el dataset para Ragas
    data_dict = {
        "question": questions,
        "answer": answers,
        "contexts": contexts,
        "ground_truth": ground_truths
    }
    
    dataset = Dataset.from_dict(data_dict)
    
    # IMPORTANTE: Ragas necesita variables de entorno OPENAI_API_KEY por defecto para evaluar, 
    # o configurar un LLM de Google. 
    # Aquí asumimos que tienen OPENAI_API_KEY o configuraremos Langchain Google LLM si es necesario.
    # Dado que es un script genérico, dejaremos que Ragas intente usar la config por defecto.
    # Para usar Gemini como juez en Ragas, se requiere langchain-google-genai.
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        
        gemini_model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")
        gemini_embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        print("Evaluando usando modelos de Gemini como juez...")
        result = evaluate(
            dataset=dataset,
            metrics=[
                context_precision,
                context_recall,
                faithfulness,
                answer_relevancy,
            ],
            llm=gemini_model,
            embeddings=gemini_embeddings
        )
    except ImportError:
        print("Aviso: langchain-google-genai no está instalado. Ragas intentará usar OpenAI (requiere OPENAI_API_KEY).")
        result = evaluate(
            dataset=dataset,
            metrics=[
                context_precision,
                context_recall,
                faithfulness,
                answer_relevancy,
            ]
        )

    df = result.to_pandas()
    df.to_csv("eval_results.csv", index=False)
    
    print("\nResultados de la Evaluación:")
    print(df[["question", "answer_relevancy", "faithfulness", "context_precision", "context_recall"]].mean())
    print("\nLos resultados completos se han guardado en eval_results.csv")

if __name__ == "__main__":
    main()
