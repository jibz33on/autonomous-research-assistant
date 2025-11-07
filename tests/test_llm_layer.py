"""
Test script for Layer 1 (LLM)
Tests clients.py and prompts.py independently
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

print("\n" + "="*70)
print("LAYER 1 TEST - LLM Client & Prompts")
print("="*70 + "\n")

# ============================================================================
# TEST 1: Import LLM Client
# ============================================================================
print("Test 1: Importing LLM Client...")
try:
    from src.llm.client import LLMClient
    print("✅ LLMClient imported successfully\n")
except Exception as e:
    print(f"❌ Failed to import LLMClient: {e}\n")
    sys.exit(1)

# ============================================================================
# TEST 2: Import Prompts
# ============================================================================
print("Test 2: Importing Prompts...")
try:
    from src.llm.prompts import (
        PLANNER_SYSTEM_PROMPT,
        PLANNER_USER_TEMPLATE,
        SYNTHESIZER_SYSTEM_PROMPT,
        SYNTHESIZER_USER_TEMPLATE,
        QA_SYSTEM_PROMPT,
        QA_USER_TEMPLATE
    )
    print("✅ All prompts imported successfully\n")
except Exception as e:
    print(f"❌ Failed to import prompts: {e}\n")
    sys.exit(1)

# ============================================================================
# TEST 3: Initialize LLM Client
# ============================================================================
print("Test 3: Initializing LLM Client...")
try:
    llm = LLMClient(temperature=0.7)
    print(f"✅ LLM Client initialized")
    print(f"   Model: {llm.model}")
    print(f"   Temperature: {llm.temperature}\n")
except Exception as e:
    print(f"❌ Failed to initialize LLM Client: {e}\n")
    sys.exit(1)

# ============================================================================
# TEST 4: Simple Text Invocation
# ============================================================================
print("Test 4: Testing simple text invocation...")
try:
    response = llm.invoke(
        system_prompt="You are a helpful assistant.",
        user_message="Say 'Hello, I am working!' in exactly 5 words."
    )
    print(f"✅ Text invocation successful")
    print(f"   Response: {response}\n")
except Exception as e:
    print(f"❌ Text invocation failed: {e}\n")
    sys.exit(1)

# ============================================================================
# TEST 5: JSON Invocation
# ============================================================================
print("Test 5: Testing JSON invocation...")
try:
    response = llm.invoke_with_json(
        system_prompt="You are a helpful assistant. Return JSON only.",
        user_message='Return JSON: {"status": "working", "test": true}'
    )
    print(f"✅ JSON invocation successful")
    print(f"   Response type: {type(response)}")
    print(f"   Response: {response}\n")
    
    if not isinstance(response, dict):
        print("⚠️  Warning: Response is not a dict")
except Exception as e:
    print(f"❌ JSON invocation failed: {e}\n")
    sys.exit(1)

# ============================================================================
# TEST 6: Prompt Template Formatting
# ============================================================================
print("Test 6: Testing prompt template formatting...")
try:
    # Test planner prompt
    user_prompt = PLANNER_USER_TEMPLATE.format(topic="Artificial Intelligence")
    print(f"✅ Planner prompt formatted successfully")
    print(f"   Preview: {user_prompt[:50]}...\n")
    
    # Test synthesizer prompt
    user_prompt = SYNTHESIZER_USER_TEMPLATE.format(
        topic="AI",
        context="[1] AI is growing. [2] AI has challenges."
    )
    print(f"✅ Synthesizer prompt formatted successfully")
    print(f"   Preview: {user_prompt[:50]}...\n")
    
    # Test QA prompt
    user_prompt = QA_USER_TEMPLATE.format(
        context="AI context here",
        question="What is AI?"
    )
    print(f"✅ QA prompt formatted successfully")
    print(f"   Preview: {user_prompt[:50]}...\n")
except Exception as e:
    print(f"❌ Prompt formatting failed: {e}\n")
    sys.exit(1)

# ============================================================================
# TEST 7: Real Planner-Style JSON Call
# ============================================================================
print("Test 7: Testing realistic planner-style JSON call...")
try:
    # Create a planner-style client
    planner_llm = LLMClient(temperature=0.3)
    
    topic = "Quantum Computing"
    user_message = PLANNER_USER_TEMPLATE.format(topic=topic)
    
    plan = planner_llm.invoke_with_json(
        system_prompt=PLANNER_SYSTEM_PROMPT,
        user_message=user_message
    )
    
    print(f"✅ Planner-style call successful")
    print(f"   Subtopics count: {len(plan.get('subtopics', []))}")
    print(f"   Queries count: {len(plan.get('search_queries', []))}")
    print(f"   Sample subtopic: {plan.get('subtopics', ['N/A'])[0]}")
    print(f"   Sample query: {plan.get('search_queries', ['N/A'])[0]}\n")
    
except Exception as e:
    print(f"❌ Planner-style call failed: {e}\n")
    sys.exit(1)

# ============================================================================
# SUMMARY
# ============================================================================
print("="*70)
print("✅ ALL TESTS PASSED!")
print("="*70)
print("\nLayer 1 (LLM) is working correctly!")
print("\nWhat was tested:")
print("  ✓ LLMClient imports correctly")
print("  ✓ All prompts import correctly")
print("  ✓ LLM client initializes")
print("  ✓ invoke() method works")
print("  ✓ invoke_with_json() method works")
print("  ✓ Prompt templates format correctly")
print("  ✓ Real planner-style JSON call works")
print("\nReady to move to Layer 2 (Tools)! 🚀")
print("="*70 + "\n")