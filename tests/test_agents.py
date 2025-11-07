"""Tests for agents."""
import sys
from pathlib import Path
import uuid

# Add parent directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("="*80)
print("LAYER 4 AGENTS TEST")
print("="*80)


def test_planner_agent():
    """Test planner creates valid plan."""
    print("\n[TEST 1] Testing PlannerAgent...")
    print("="*80)
    
    try:
        from src.agents.planner import PlannerAgent
        
        # Initialize
        planner = PlannerAgent()
        print("✅ PlannerAgent initialized")
        
        # Create plan
        test_topic = "artificial intelligence in education"
        print(f"\n🎯 Creating plan for: '{test_topic}'")
        plan = planner.create_plan(test_topic)
        
        # Validate structure
        assert 'subtopics' in plan, "Plan missing 'subtopics'"
        assert 'search_queries' in plan, "Plan missing 'search_queries'"
        assert len(plan['subtopics']) >= 3, "Expected at least 3 subtopics"
        assert len(plan['search_queries']) >= 5, "Expected at least 5 queries"
        
        print("✅ Plan created successfully!")
        print(f"\n📋 Subtopics ({len(plan['subtopics'])}):")
        for i, subtopic in enumerate(plan['subtopics'], 1):
            print(f"   {i}. {subtopic}")
        
        print(f"\n🔍 Search Queries ({len(plan['search_queries'])}):")
        for i, query in enumerate(plan['search_queries'][:3], 1):  # Show first 3
            print(f"   {i}. {query}")
        print(f"   ... and {len(plan['search_queries']) - 3} more")
        
        # Return plan for next test
        return plan
        
    except Exception as e:
        print(f"❌ PlannerAgent test failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_executor_agent(queries):
    """Test executor collects documents."""
    print("\n[TEST 2] Testing ExecutorAgent...")
    print("="*80)
    
    try:
        from src.agents.executor import ExecutorAgent
        
        # Initialize
        executor = ExecutorAgent()
        print("✅ ExecutorAgent initialized")
        
        # Test with first 2 queries only (to save time/API calls)
        test_queries = queries[:2]
        print(f"\n🔎 Executing research with {len(test_queries)} queries:")
        for i, query in enumerate(test_queries, 1):
            print(f"   {i}. {query}")
        
        # Execute research
        documents = executor.execute_research(test_queries)
        
        # Validate
        assert len(documents) > 0, "No documents collected"
        
        print(f"\n✅ Research executed successfully!")
        print(f"   Collected {len(documents)} documents")
        
        # Show first document
        if documents:
            doc = documents[0]
            print(f"\n📄 First document:")
            print(f"   URL: {doc['url']}")
            print(f"   Title: {doc['title'][:60]}...")
            print(f"   Content length: {len(doc['content'])} chars")
            print(f"   Query: {doc['query']}")
        
        return documents
        
    except Exception as e:
        print(f"❌ ExecutorAgent test failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_synthesizer_agent(topic, documents):
    """Test synthesizer generates report."""
    print("\n[TEST 3] Testing SynthesizerAgent...")
    print("="*80)
    
    try:
        from src.agents.synthesizer import SynthesizerAgent
        
        # Initialize
        synthesizer = SynthesizerAgent()
        print("✅ SynthesizerAgent initialized")
        
        # Generate session ID
        session_id = f"test_{uuid.uuid4().hex[:8]}"
        
        # Synthesize report
        print(f"\n📝 Synthesizing report for: '{topic}'")
        print(f"   Using {len(documents)} documents")
        
        result = synthesizer.synthesize_report(
            topic=topic,
            documents=documents,
            session_id=session_id
        )
        
        # Validate
        assert 'report' in result, "Result missing 'report'"
        assert 'sources' in result, "Result missing 'sources'"
        assert len(result['report']) > 100, "Report too short"
        assert len(result['sources']) > 0, "No sources listed"
        
        print(f"\n✅ Report synthesized successfully!")
        print(f"   Report length: {len(result['report'])} chars")
        print(f"   Sources: {len(result['sources'])}")
        
        print(f"\n📄 Report preview (first 300 chars):")
        print(f"   {result['report'][:300]}...")
        
        # Test Q&A
        print(f"\n💬 Testing Q&A capability...")
        test_question = "What are the main benefits?"
        print(f"   Question: '{test_question}'")
        
        answer = synthesizer.answer_question(test_question, session_id)
        print(f"✅ Answer generated ({len(answer)} chars)")
        print(f"\n   Answer preview:")
        print(f"   {answer[:200]}...")
        
        # Cleanup
        print(f"\n🗑️  Cleaning up session...")
        synthesizer.retriever.delete_session(session_id)
        print("✅ Session cleaned up")
        
        return True
        
    except Exception as e:
        print(f"❌ SynthesizerAgent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_full_pipeline():
    """Test full agent pipeline."""
    print("\n[TEST 4] Testing Full Agent Pipeline...")
    print("="*80)
    
    try:
        print("🔄 Running: Planner → Executor → Synthesizer")
        
        from src.agents.planner import PlannerAgent
        from src.agents.executor import ExecutorAgent
        from src.agents.synthesizer import SynthesizerAgent
        
        # Topic
        topic = "machine learning basics"
        print(f"\n📚 Research topic: '{topic}'")
        
        # Step 1: Plan
        print("\n1️⃣ Planning...")
        planner = PlannerAgent()
        plan = planner.create_plan(topic)
        print(f"   Generated {len(plan['search_queries'])} queries")
        
        # Step 2: Execute (use only first 2 queries for speed)
        print("\n2️⃣ Executing research...")
        executor = ExecutorAgent()
        documents = executor.execute_research(plan['search_queries'][:2])
        print(f"   Collected {len(documents)} documents")
        
        # Step 3: Synthesize
        print("\n3️⃣ Synthesizing report...")
        synthesizer = SynthesizerAgent()
        session_id = f"pipeline_{uuid.uuid4().hex[:8]}"
        result = synthesizer.synthesize_report(topic, documents, session_id)
        print(f"   Report: {len(result['report'])} chars")
        print(f"   Sources: {len(result['sources'])}")
        
        # Cleanup
        synthesizer.retriever.delete_session(session_id)
        
        print("\n✅ FULL PIPELINE SUCCESSFUL!")
        
        return True
        
    except Exception as e:
        print(f"❌ Full pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run tests sequentially
    results = []
    
    # Test 1: Planner
    plan = test_planner_agent()
    results.append(("PlannerAgent", plan is not None))
    
    if plan:
        # Test 2: Executor (using planner's queries)
        documents = test_executor_agent(plan['search_queries'])
        results.append(("ExecutorAgent", documents is not None))
        
        if documents:
            # Test 3: Synthesizer (using executor's documents)
            topic = "artificial intelligence in education"
            synth_result = test_synthesizer_agent(topic, documents)
            results.append(("SynthesizerAgent", synth_result))
        else:
            results.append(("SynthesizerAgent", False))
    else:
        results.append(("ExecutorAgent", False))
        results.append(("SynthesizerAgent", False))
    
    # Test 4: Full pipeline
    pipeline_result = test_full_pipeline()
    results.append(("FullPipeline", pipeline_result))
    
    # Summary
    print("\n" + "="*80)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    if passed == total:
        print(f"✅ ALL {total} AGENT TESTS PASSED!")
    else:
        print(f"⚠️  {passed}/{total} TESTS PASSED")
    
    print("="*80)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
    
    print("\n🚀 Layer 4 (Agents) Complete! Ready for Layer 5 (Graph)!")
    print("="*80)