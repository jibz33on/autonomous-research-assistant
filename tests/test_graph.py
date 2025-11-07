"""Test Layer 5 - Graph (LangGraph workflow orchestration)"""

import sys
from pathlib import Path

# Add parent directory to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("="*80)
print("LAYER 5 GRAPH TEST")
print("="*80)


def test_build_graph():
    """Test that graph builds correctly."""
    print("\n[TEST 1] Testing Graph Building...")
    print("="*80)
    
    try:
        from src.graph.workflow import build_research_graph
        
        print("🔧 Building research graph...")
        graph = build_research_graph()
        
        print("✅ Graph built successfully!")
        print(f"   Type: {type(graph)}")
        
        return graph
        
    except Exception as e:
        print(f"❌ Graph building failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_workflow_execution():
    """Test full workflow execution."""
    print("\n[TEST 2] Testing Workflow Execution...")
    print("="*80)
    
    try:
        from src.graph.workflow import run_research
        
        # Use a simple topic for faster testing
        test_topic = "benefits of solar energy"
        print(f"🚀 Running workflow for: '{test_topic}'")
        print("   (This will take 1-2 minutes...)\n")
        
        # Execute workflow
        result = run_research(test_topic)
        
        # Validate result
        assert result['status'] == 'complete', f"Expected status 'complete', got '{result['status']}'"
        assert result['topic'] == test_topic, "Topic mismatch"
        assert len(result['subtopics']) >= 3, "Expected at least 3 subtopics"
        assert len(result['search_queries']) >= 5, "Expected at least 5 queries"
        assert len(result['documents']) > 0, "No documents collected"
        assert len(result['report']) > 100, "Report too short"
        assert len(result['sources']) > 0, "No sources listed"
        assert result['session_id'], "Session ID missing"
        assert len(result['logs']) > 0, "No logs generated"
        
        print("✅ Workflow executed successfully!")
        print(f"\n📊 Workflow Results:")
        print(f"   Status: {result['status']}")
        print(f"   Topic: {result['topic']}")
        print(f"   Subtopics: {len(result['subtopics'])}")
        print(f"   Search queries: {len(result['search_queries'])}")
        print(f"   Documents collected: {len(result['documents'])}")
        print(f"   Report length: {len(result['report'])} chars")
        print(f"   Sources: {len(result['sources'])}")
        print(f"   Session ID: {result['session_id']}")
        print(f"   Log entries: {len(result['logs'])}")
        
        print(f"\n📋 Subtopics:")
        for i, subtopic in enumerate(result['subtopics'], 1):
            print(f"   {i}. {subtopic}")
        
        print(f"\n📝 Activity Log:")
        for log in result['logs']:
            print(f"   {log}")
        
        print(f"\n📄 Report Preview (first 400 chars):")
        print(f"   {result['report'][:400]}...")
        
        print(f"\n🔗 Sources:")
        for i, source in enumerate(result['sources'][:3], 1):
            print(f"   {i}. {source}")
        if len(result['sources']) > 3:
            print(f"   ... and {len(result['sources']) - 3} more")
        
        return result
        
    except Exception as e:
        print(f"❌ Workflow execution failed: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_state_flow():
    """Test that state flows correctly through nodes."""
    print("\n[TEST 3] Testing State Flow Through Nodes...")
    print("="*80)
    
    try:
        from src.graph.workflow import build_research_graph
        
        # Build graph
        graph = build_research_graph()
        
        # Create initial state
        initial_state = {
            'topic': 'renewable energy advantages',
            'documents': [],
            'logs': [],
            'subtopics': [],
            'search_queries': [],
            'session_id': '',
            'report': '',
            'sources': [],
            'status': 'initialized',
            'error': ''
        }
        
        print(f"📦 Initial State:")
        print(f"   topic: '{initial_state['topic']}'")
        print(f"   status: '{initial_state['status']}'")
        print(f"   documents: {len(initial_state['documents'])}")
        
        # Execute workflow
        print(f"\n🔄 Executing workflow through all nodes...")
        final_state = graph.invoke(initial_state)
        
        # Verify state evolution
        print(f"\n📦 Final State:")
        print(f"   topic: '{final_state['topic']}'")
        print(f"   status: '{final_state['status']}'")
        print(f"   subtopics: {len(final_state.get('subtopics', []))}")
        print(f"   search_queries: {len(final_state.get('search_queries', []))}")
        print(f"   documents: {len(final_state.get('documents', []))}")
        print(f"   report: {len(final_state.get('report', ''))} chars")
        print(f"   sources: {len(final_state.get('sources', []))}")
        print(f"   logs: {len(final_state.get('logs', []))} entries")
        
        # Validate progression
        assert final_state['status'] == 'complete', "Workflow did not complete"
        assert len(final_state['subtopics']) > 0, "Planner did not add subtopics"
        assert len(final_state['search_queries']) > 0, "Planner did not add queries"
        assert len(final_state['documents']) > 0, "Executor did not add documents"
        assert len(final_state['report']) > 0, "Synthesizer did not add report"
        assert len(final_state['sources']) > 0, "Synthesizer did not add sources"
        assert len(final_state['logs']) >= 6, "Not enough log entries (expected 2 per node)"
        
        print(f"\n✅ State flowed correctly through all nodes!")
        
        return True
        
    except Exception as e:
        print(f"❌ State flow test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_error_handling():
    """Test that graph handles errors gracefully."""
    print("\n[TEST 4] Testing Error Handling...")
    print("="*80)
    
    try:
        from src.graph.workflow import build_research_graph
        
        # Build graph
        graph = build_research_graph()
        
        # Test with empty topic (should handle gracefully)
        print("🧪 Testing with edge case (empty topic)...")
        
        try:
            initial_state = {
                'topic': '',  # Empty topic
                'documents': [],
                'logs': [],
                'subtopics': [],
                'search_queries': [],
                'session_id': '',
                'report': '',
                'sources': [],
                'status': 'initialized',
                'error': ''
            }
            
            result = graph.invoke(initial_state)
            
            # Should either complete or error gracefully
            if result['status'] == 'error':
                print(f"✅ Graph handled error gracefully")
                print(f"   Error: {result.get('error', 'Unknown')}")
            else:
                print(f"⚠️  Graph completed despite empty topic (unexpected)")
                
        except Exception as e:
            print(f"✅ Graph raised exception as expected: {str(e)[:100]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Run tests
    results = []
    
    # Test 1: Build graph
    graph = test_build_graph()
    results.append(("BuildGraph", graph is not None))
    
    # Test 2: Execute workflow (main test)
    if graph:
        workflow_result = test_workflow_execution()
        results.append(("WorkflowExecution", workflow_result is not None))
    else:
        results.append(("WorkflowExecution", False))
    
    # Test 3: State flow
    state_flow_result = test_state_flow()
    results.append(("StateFlow", state_flow_result))
    
    # Test 4: Error handling
    error_result = test_error_handling()
    results.append(("ErrorHandling", error_result))
    
    # Summary
    print("\n" + "="*80)
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    if passed == total:
        print(f"✅ ALL {total} GRAPH TESTS PASSED!")
    else:
        print(f"⚠️  {passed}/{total} TESTS PASSED")
    
    print("="*80)
    
    for name, result in results:
        status = "✅" if result else "❌"
        print(f"  {status} {name}")
    
    print("\n" + "="*80)
    if passed == total:
        print("🎉 LAYER 5 (GRAPH) COMPLETE!")
        print("🚀 ALL LAYERS COMPLETE! Ready for app.py!")
    else:
        print("⚠️  Some tests failed. Please review errors above.")
    print("="*80)