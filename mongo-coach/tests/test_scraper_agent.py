from src.agents.scraper_agent import ScraperAgent

def test_scraper_agent_smoke():
    agent = ScraperAgent()
    assert agent is not None
