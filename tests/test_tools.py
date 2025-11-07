"""Test Layer 2 - Tools (websearch, scraper, parser)"""

import sys
from pathlib import Path

# Add parent directory to path so we can import src
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print("="*80)
print("LAYER 2 TOOLS TEST")
print("="*80)

# Test 1: Configuration
print("\n[TEST 1] Checking configuration...")
try:
    from src.utils.config import settings
    print(f"✅ Config loaded successfully")
    print(f"   - OpenAI API key: {'*' * 20}{settings.openai_api_key[-4:]}")
    print(f"   - Tavily API key: {'*' * 20}{settings.tavily_api_key[-4:]}")
    print(f"   - Max search results: {settings.max_search_results}")
    print(f"   - Chunk size: {settings.chunk_size}")
except Exception as e:
    print(f"❌ Config failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Web Search
print("\n" + "="*80)
print("[TEST 2] Testing TavilySearch...")
print("="*80)
try:
    from src.tools.websearch import TavilySearch
    
    search = TavilySearch()
    print("✅ TavilySearch initialized")
    
    test_query = "artificial intelligence applications"
    print(f"\n🔍 Searching for: '{test_query}'")
    results = search.search(test_query)
    
    if results:
        print(f"✅ Search successful! Found {len(results)} results")
        print(f"\n📄 First result:")
        print(f"   URL: {results[0].get('url', 'N/A')}")
        print(f"   Title: {results[0].get('title', 'N/A')[:80]}...")
        print(f"   Score: {results[0].get('score', 'N/A')}")
        test_urls = [r['url'] for r in results[:2]]
    else:
        print("❌ Search returned no results")
        sys.exit(1)
except Exception as e:
    print(f"❌ TavilySearch test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Web Scraper
print("\n" + "="*80)
print("[TEST 3] Testing WebScraper...")
print("="*80)
try:
    from src.tools.scraper import WebScraper
    
    scraper = WebScraper()
    print("✅ WebScraper initialized")
    
    test_url = test_urls[0]
    print(f"\n🕷️  Scraping: {test_url}")
    content = scraper.scrape_url(test_url)
    
    if content:
        print(f"✅ Scraping successful!")
        print(f"   Content length: {len(content)} characters")
        print(f"   Preview: {content[:200]}...")
        test_content = content
    else:
        print("⚠️  First URL failed, trying second...")
        content = scraper.scrape_url(test_urls[1])
        if content:
            print(f"✅ Second URL successful!")
            test_content = content
        else:
            print("❌ Both URLs failed")
            sys.exit(1)
except Exception as e:
    print(f"❌ WebScraper test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 4: Document Parser
print("\n" + "="*80)
print("[TEST 4] Testing DocumentParser...")
print("="*80)
try:
    from src.tools.parser import DocumentParser
    
    parser = DocumentParser()
    print("✅ DocumentParser initialized")
    
    print(f"\n✂️  Chunking content ({len(test_content)} chars)...")
    metadata = {'url': test_url, 'title': 'Test', 'source': 'web'}
    chunks = parser.chunk_document(test_content, metadata)
    
    print(f"✅ Chunking successful!")
    print(f"   Total chunks: {len(chunks)}")
    print(f"   First chunk: {len(chunks[0]['text'])} chars")
    print(f"   Metadata: {chunks[0]['metadata']}")
except Exception as e:
    print(f"❌ DocumentParser test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Summary
print("\n" + "="*80)
print("✅ ALL LAYER 2 TESTS PASSED!")
print("="*80)
print("\nLayer 2 (Tools) working:")
print("  ✅ TavilySearch")
print("  ✅ WebScraper")
print("  ✅ DocumentParser")
print("\n🚀 Ready for Layer 3 (RAG)!")
print("="*80)