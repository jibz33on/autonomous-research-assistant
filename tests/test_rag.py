"""Test Layer 3 - RAG (embeddings, vector_store, retriever)"""

import sys
from pathlib import Path
import uuid

# Add parent directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("="*80)
print("LAYER 3 RAG TEST")
print("="*80)

# Test 1: Embeddings
print("\n[TEST 1] Testing Embeddings...")
print("="*80)
try:
    from src.rag.embeddings import get_embedding_function
    
    embedding_fn = get_embedding_function()
    print("✅ Embedding function created")
    print(f"   Type: {type(embedding_fn)}")
    
except Exception as e:
    print(f"❌ Embeddings test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Vector Store
print("\n[TEST 2] Testing VectorStore...")
print("="*80)
try:
    from src.rag.vector_store import VectorStore
    
    # Initialize
    store = VectorStore()
    print("✅ VectorStore initialized")
    
    # Create test collection
    test_collection = f"test_{uuid.uuid4().hex[:8]}"
    print(f"\n📦 Creating collection: {test_collection}")
    store.create_collection(test_collection)
    print("✅ Collection created")
    
    # Add test documents
    test_chunks = [
        {
            'text': 'Artificial intelligence is transforming healthcare through machine learning.',
            'metadata': {'url': 'https://example.com/ai', 'source': 'web', 'chunk_index': 0}
        },
        {
            'text': 'Deep learning models can detect diseases from medical images with high accuracy.',
            'metadata': {'url': 'https://example.com/ml', 'source': 'web', 'chunk_index': 0}
        },
        {
            'text': 'Natural language processing helps analyze medical records and patient data.',
            'metadata': {'url': 'https://example.com/nlp', 'source': 'web', 'chunk_index': 0}
        }
    ]
    
    print(f"\n📝 Adding {len(test_chunks)} chunks to collection")
    store.add_documents(test_collection, test_chunks)
    print("✅ Documents added")
    
    # Query collection
    test_query = "How is AI used in medical diagnosis?"
    print(f"\n🔍 Querying: '{test_query}'")
    results = store.query_collection(test_collection, test_query, top_k=2)
    
    if results:
        print(f"✅ Query successful! Retrieved {len(results)} chunks")
        print(f"\n📄 Top result:")
        print(f"   {results[0][:100]}...")
    else:
        print("❌ Query returned no results")
        sys.exit(1)
    
    # List collections
    collections = store.list_collections()
    print(f"\n📋 Total collections: {len(collections)}")
    
    # Cleanup
    print(f"\n🗑️  Deleting test collection")
    store.delete_collection(test_collection)
    print("✅ Collection deleted")
    
except Exception as e:
    print(f"❌ VectorStore test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Retriever
print("\n[TEST 3] Testing Retriever...")
print("="*80)
try:
    from src.rag.retriever import Retriever
    
    # Initialize
    retriever = Retriever()
    print("✅ Retriever initialized")
    
    # Create test documents
    test_session = f"session_{uuid.uuid4().hex[:8]}"
    test_documents = [
        {
            'url': 'https://example.com/quantum',
            'title': 'Quantum Computing Basics',
            'content': '''Quantum computing uses quantum mechanics to process information. 
            Unlike classical computers that use bits (0 or 1), quantum computers use qubits 
            that can exist in superposition. This allows quantum computers to solve certain 
            problems exponentially faster than classical computers. Applications include 
            cryptography, drug discovery, and optimization problems.''',
            'source': 'web'
        },
        {
            'url': 'https://example.com/blockchain',
            'title': 'Blockchain Technology',
            'content': '''Blockchain is a distributed ledger technology that ensures data 
            integrity through cryptographic hashing. Each block contains transactions and 
            a reference to the previous block, creating an immutable chain. Blockchain 
            enables decentralized applications and cryptocurrencies. Key benefits include 
            transparency, security, and removal of intermediaries.''',
            'source': 'web'
        }
    ]
    
    # Store documents
    print(f"\n📦 Storing {len(test_documents)} documents (session: {test_session})")
    retriever.store_documents(test_documents, test_session)
    print("✅ Documents stored successfully")
    
    # Retrieve relevant chunks
    test_queries = [
        "What is quantum computing?",
        "How does blockchain work?",
        "What are the applications of quantum computers?"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        chunks = retriever.retrieve(query, test_session, top_k=3)
        print(f"✅ Retrieved {len(chunks)} chunks")
        print(f"   First chunk preview: {chunks[0][:80]}...")
    
    # Cleanup
    print(f"\n🗑️  Deleting test session")
    retriever.delete_session(test_session)
    print("✅ Session deleted")
    
except Exception as e:
    print(f"❌ Retriever test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Full RAG Pipeline
print("\n[TEST 4] Testing Full RAG Pipeline...")
print("="*80)
try:
    print("🔄 Running: Store → Retrieve → Query")
    
    # Create new session
    pipeline_session = f"pipeline_{uuid.uuid4().hex[:8]}"
    
    # Simulate agent workflow
    print("\n1️⃣ Agent collects documents from web...")
    agent_documents = [
        {
            'url': 'https://example.com/ml-healthcare',
            'title': 'Machine Learning in Healthcare',
            'content': '''Machine learning algorithms are revolutionizing healthcare diagnosis. 
            CNN models achieve 95% accuracy in detecting lung cancer from CT scans. Random forests 
            predict patient readmission risks. NLP extracts insights from electronic health records. 
            Challenges include data privacy, model interpretability, and regulatory approval. 
            Future directions include federated learning and explainable AI for medical decisions.''',
            'source': 'web'
        },
        {
            'url': 'https://example.com/ai-drug-discovery',
            'title': 'AI in Drug Discovery',
            'content': '''Artificial intelligence accelerates drug discovery by predicting molecular 
            properties and interactions. Deep learning models screen millions of compounds in days 
            instead of years. AlphaFold predicts protein structures with remarkable accuracy. 
            Generative models design novel drug candidates. AI reduces development costs and time. 
            Major pharmaceutical companies now have dedicated AI research divisions.''',
            'source': 'web'
        }
    ]
    
    # Store
    print("2️⃣ Storing documents in RAG system...")
    retriever.store_documents(agent_documents, pipeline_session)
    
    # Retrieve for report generation
    print("3️⃣ Retrieving context for report generation...")
    report_query = "What are the main applications of AI in healthcare?"
    context = retriever.retrieve(report_query, pipeline_session, top_k=5)
    print(f"   Retrieved {len(context)} context chunks")
    
    # Retrieve for Q&A
    print("4️⃣ Answering follow-up question...")
    qa_query = "What are the challenges of using AI in healthcare?"
    answer_context = retriever.retrieve(qa_query, pipeline_session, top_k=3)
    print(f"   Retrieved {len(answer_context)} chunks for answer")
    print(f"   Relevant chunk: {answer_context[0][:100]}...")
    
    # Cleanup
    print("5️⃣ Cleaning up...")
    retriever.delete_session(pipeline_session)
    
    print("\n✅ FULL RAG PIPELINE SUCCESSFUL!")
    
except Exception as e:
    print(f"❌ Full pipeline test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Summary
print("\n" + "="*80)
print("✅ ALL LAYER 3 TESTS PASSED!")
print("="*80)
print("\nLayer 3 (RAG) working:")
print("  ✅ Embeddings - OpenAI embedding function")
print("  ✅ VectorStore - ChromaDB operations")
print("  ✅ Retriever - High-level RAG interface")
print("  ✅ Full Pipeline - Store → Query → Retrieve")
print("\n🚀 Ready for Layer 4 (Agents)!")
print("="*80)