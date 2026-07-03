import React, { useState, useEffect, useMemo } from 'react';
import { 
  Brain, 
  Layers, 
  Search, 
  BarChart3, 
  RotateCcw, 
  Check, 
  AlertCircle, 
  ChevronRight, 
  GraduationCap, 
  Trash2, 
  CheckCircle2, 
  Clock, 
  ArrowRight, 
  BookOpen, 
  Calendar,
  Sparkles
} from 'lucide-react';
import './App.css';
import flashcardsData from './flashcards.json';

const CATEGORIES = [
  'All',
  'Overview & Document Model',
  'CRUD Operations',
  'Indexes & Performance',
  'Data Modeling',
  'Tools & Tooling',
  'MongoDB Drivers & PyMongo'
];

export default function App() {
  const [cards, setCards] = useState(flashcardsData);
  const [progress, setProgress] = useState({});
  const [activeTab, setActiveTab] = useState('study'); // 'study' | 'browse' | 'stats'
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [isFlipped, setIsFlipped] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [studyAhead, setStudyAhead] = useState(false);
  const [currentQueueIndex, setCurrentQueueIndex] = useState(0);
  const [todayStudiedCount, setTodayStudiedCount] = useState(0);

  // Load progress on mount
  useEffect(() => {
    const stored = localStorage.getItem('mongodb_anki_progress');
    const studiedCount = localStorage.getItem('mongodb_anki_today_count');
    if (stored) {
      setProgress(JSON.parse(stored));
    }
    if (studiedCount) {
      setTodayStudiedCount(parseInt(studiedCount, 10));
    }
  }, []);

  // Save progress helper
  const saveProgressState = (newProgress) => {
    setProgress(newProgress);
    localStorage.setItem('mongodb_anki_progress', JSON.stringify(newProgress));
  };

  // Merge default cards with progress data
  const cardsWithSRS = useMemo(() => {
    return cards.map(card => {
      const cardProgress = progress[card.id] || {
        reps: 0,
        interval: 0,
        ease: 2.5,
        nextReview: 0,
        history: []
      };
      return {
        ...card,
        ...cardProgress
      };
    });
  }, [cards, progress]);

  // SM-2 Spaced Repetition Algorithm
  // quality: 0 = Again, 1 = Hard, 2 = Good, 3 = Easy
  const calculateSM2 = (card, quality) => {
    let { reps, interval, ease } = card;
    reps = reps || 0;
    interval = interval || 0;
    ease = ease || 2.5;

    if (quality === 0) {
      // Again: Reset repetitions
      reps = 0;
      interval = 1 / 1440; // 1 minute (1/1440 of a day)
    } else {
      if (quality === 1) {
        // Hard: increase reps, keep short interval, decrease ease
        reps = 1;
        interval = interval === 0 ? 1 : interval * 1.2;
        ease = Math.max(1.3, ease - 0.15);
      } else if (quality === 2) {
        // Good: standard spacing
        if (reps === 0) {
          interval = 1;
        } else if (reps === 1) {
          interval = 3;
        } else {
          interval = interval * ease;
        }
        reps += 1;
      } else if (quality === 3) {
        // Easy: accelerated spacing, increase ease
        if (reps === 0) {
          interval = 3;
        } else if (reps === 1) {
          interval = 6;
        } else {
          interval = interval * ease * 1.3;
        }
        ease = Math.min(3.0, ease + 0.15);
        reps += 1;
      }
    }

    const now = Date.now();
    const msInDay = 24 * 60 * 60 * 1000;
    const nextReview = now + Math.round(interval * msInDay);

    return { reps, interval, ease, nextReview };
  };

  // Anki intervals preview helper
  const getIntervalPreview = (card, quality) => {
    let { reps, interval, ease } = card;
    reps = reps || 0;
    interval = interval || 0;
    ease = ease || 2.5;

    if (quality === 0) return '< 1m';
    
    let nextInt = 0;
    if (quality === 1) {
      nextInt = interval === 0 ? 1 : interval * 1.2;
    } else if (quality === 2) {
      if (reps === 0) nextInt = 1;
      else if (reps === 1) nextInt = 3;
      else nextInt = interval * ease;
    } else if (quality === 3) {
      if (reps === 0) nextInt = 3;
      else if (reps === 1) nextInt = 6;
      else nextInt = interval * ease * 1.3;
    }

    return formatInterval(nextInt);
  };

  const formatInterval = (days) => {
    if (days < 1) {
      const mins = Math.round(days * 1440);
      if (mins < 1) return '< 1m';
      return `${mins}m`;
    }
    const rounded = Math.round(days * 10) / 10;
    if (rounded >= 30) {
      const months = Math.round((rounded / 30) * 10) / 10;
      return `${months}mo`;
    }
    return `${rounded}d`;
  };

  // Compile queues based on selected category
  const filteredCardsSRS = useMemo(() => {
    return cardsWithSRS.filter(c => {
      if (selectedCategory === 'All') return true;
      return c.category === selectedCategory;
    });
  }, [cardsWithSRS, selectedCategory]);

  // Anki standard study queue: Due cards or New cards
  const studyQueue = useMemo(() => {
    const now = Date.now();
    
    // Sort logic: Due cards first (older nextReview), then New cards, then already reviewed
    const due = filteredCardsSRS.filter(c => c.nextReview > 0 && c.nextReview <= now);
    const newCards = filteredCardsSRS.filter(c => c.reps === 0);
    const learning = filteredCardsSRS.filter(c => c.interval > 0 && c.interval < 1 && c.nextReview > now); // short-term loop

    if (studyAhead) {
      // In study ahead mode, we sort all cards in the category by nextReview time
      // so cards due soonest or new cards come first
      return [...filteredCardsSRS].sort((a, b) => {
        if (a.reps === 0 && b.reps !== 0) return -1;
        if (b.reps === 0 && a.reps !== 0) return 1;
        return a.nextReview - b.nextReview;
      });
    }

    // Combine due queue
    return [...due, ...newCards];
  }, [filteredCardsSRS, studyAhead]);

  // Sidebar count badges
  const sidebarCounts = useMemo(() => {
    const now = Date.now();
    const allFiltered = filteredCardsSRS;
    return {
      new: allFiltered.filter(c => c.reps === 0).length,
      due: allFiltered.filter(c => c.nextReview > 0 && c.nextReview <= now).length,
      learning: allFiltered.filter(c => c.reps > 0 && c.nextReview > now && c.interval < 1).length
    };
  }, [filteredCardsSRS]);

  const currentCard = studyQueue[currentQueueIndex] || null;

  const handleResponse = (quality) => {
    if (!currentCard) return;

    // Calculate new SM2 scheduling
    const newSrs = calculateSM2(currentCard, quality);
    const updatedProgress = {
      ...progress,
      [currentCard.id]: newSrs
    };

    saveProgressState(updatedProgress);

    // Increment count studied today
    const newStudiedCount = todayStudiedCount + 1;
    setTodayStudiedCount(newStudiedCount);
    localStorage.setItem('mongodb_anki_today_count', newStudiedCount.toString());

    // Reset card flip and move to next
    setIsFlipped(false);
    
    // In spaced repetition, once a card is answered:
    // If "Again" was clicked, in Anki it stays in the short term queue and appears again.
    // To mimic this, if quality === 0, we can push it to the end of the current queue or keep index same.
    // If they graduate it (Good/Easy), it is removed from the active due/new queue.
    if (quality === 0) {
      // Reposition at the end of the queue or keep in queue
      // For simplicity, let's keep index same (since this card is updated, if it stays at front it repeats)
      // or advance to see other cards, and this one will show up again.
      // Let's just advance index to keep flow moving.
      if (studyQueue.length > 1) {
        setCurrentQueueIndex((prev) => (prev + 1) % studyQueue.length);
      }
    } else {
      // Remove from active queue or advance
      if (currentQueueIndex >= studyQueue.length - 1) {
        setCurrentQueueIndex(0);
      }
    }
  };

  const handleStudyCardDirectly = (cardId) => {
    const idx = studyQueue.findIndex(c => c.id === cardId);
    if (idx !== -1) {
      setCurrentQueueIndex(idx);
    } else {
      // If card isn't in current standard queue, toggle study ahead to force it to show up
      setStudyAhead(true);
      const forcedIdx = filteredCardsSRS.findIndex(c => c.id === cardId);
      if (forcedIdx !== -1) {
        setCurrentQueueIndex(forcedIdx);
      }
    }
    setIsFlipped(false);
    setActiveTab('study');
  };

  const resetAllProgress = () => {
    if (window.confirm("Are you sure you want to clear all your Anki flashcard study records? This cannot be undone.")) {
      setProgress({});
      setTodayStudiedCount(0);
      localStorage.removeItem('mongodb_anki_progress');
      localStorage.removeItem('mongodb_anki_today_count');
      setCurrentQueueIndex(0);
      setIsFlipped(false);
    }
  };

  // Search filtered library list
  const browsedCards = useMemo(() => {
    return cardsWithSRS.filter(c => {
      const q = searchQuery.toLowerCase();
      const matchesSearch = 
        c.title.toLowerCase().includes(q) ||
        c.question.toLowerCase().includes(q) ||
        c.answer.toLowerCase().includes(q) ||
        c.subheading.includes(q);

      if (selectedCategory === 'All') return matchesSearch;
      return c.category === selectedCategory && matchesSearch;
    });
  }, [cardsWithSRS, searchQuery, selectedCategory]);

  // Stats Breakdown Calculations
  const statsOverview = useMemo(() => {
    const total = cardsWithSRS.length;
    const mastered = cardsWithSRS.filter(c => c.interval >= 21).length; // Interval 21+ days
    const learning = cardsWithSRS.filter(c => c.reps > 0 && c.interval < 21).length;
    const unseen = cardsWithSRS.filter(c => c.reps === 0).length;

    return { total, mastered, learning, unseen };
  }, [cardsWithSRS]);

  // Render inline formatting (bold, code)
  const renderInlineStyle = (text) => {
    const parts = [];
    const regex = /\*\*(.*?)\*\*|`(.*?)`/g;
    let lastIndex = 0;
    let match;
    let keyIdx = 0;

    while ((match = regex.exec(text)) !== null) {
      const plainText = text.substring(lastIndex, match.index);
      if (plainText) {
        parts.push(<span key={`plain-${keyIdx++}`}>{plainText}</span>);
      }

      if (match[1]) {
        parts.push(<strong key={`bold-${keyIdx++}`} className="bold-text">{match[1]}</strong>);
      } else if (match[2]) {
        parts.push(<code key={`code-${keyIdx++}`} className="inline-code">{match[2]}</code>);
      }
      lastIndex = regex.lastIndex;
    }

    const remaining = text.substring(lastIndex);
    if (remaining) {
      parts.push(<span key={`plain-end`}>{remaining}</span>);
    }

    return parts.length > 0 ? parts : text;
  };

  // Custom block markdown parser
  const renderMarkdown = (text) => {
    if (!text) return null;
    const lines = text.split('\n');
    let inCodeBlock = false;
    let codeLines = [];
    let codeLang = '';
    const elements = [];

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const trimmed = line.trim();

      if (trimmed.startsWith('```')) {
        if (inCodeBlock) {
          elements.push(
            <div key={`code-${i}`} className="code-block-container">
              <div className="code-block-header">
                <span className="code-lang-label">{codeLang.toUpperCase() || 'MONGODB'}</span>
                <span className="code-editor-dots"></span>
              </div>
              <pre className="code-block-content">
                <code>{codeLines.join('\n')}</code>
              </pre>
            </div>
          );
          codeLines = [];
          inCodeBlock = false;
        } else {
          inCodeBlock = true;
          codeLang = trimmed.replace('```', '').trim();
        }
      } else if (inCodeBlock) {
        codeLines.push(line);
      } else {
        if (trimmed.startsWith('## ')) {
          elements.push(<h2 key={`h2-${i}`} className="md-h2">{renderInlineStyle(trimmed.replace('## ', ''))}</h2>);
        } else if (trimmed.startsWith('### ')) {
          elements.push(<h3 key={`h3-${i}`} className="md-h3">{renderInlineStyle(trimmed.replace('### ', ''))}</h3>);
        } else if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
          elements.push(
            <div key={`bullet-${i}`} className="bullet-row">
              <span className="bullet-dot">•</span>
              <span className="bullet-text">{renderInlineStyle(trimmed.substring(2))}</span>
            </div>
          );
        } else if (trimmed.startsWith('`o` ') || trimmed.startsWith('o ')) {
          elements.push(
            <div key={`bullet-${i}`} className="bullet-row">
              <span className="bullet-dot">•</span>
              <span className="bullet-text">{renderInlineStyle(trimmed.substring(2))}</span>
            </div>
          );
        } else if (trimmed === '') {
          elements.push(<div key={`space-${i}`} className="md-space" />);
        } else {
          elements.push(<p key={`p-${i}`} className="md-p">{renderInlineStyle(line)}</p>);
        }
      }
    }

    if (inCodeBlock && codeLines.length > 0) {
      elements.push(
        <div key="code-end" className="code-block-container">
          <div className="code-block-header">{codeLang.toUpperCase() || 'MONGODB'}</div>
          <pre className="code-block-content">
            <code>{codeLines.join('\n')}</code>
          </pre>
        </div>
      );
    }

    return elements;
  };

  return (
    <div className="app-container">
      {/* Sidebar Panel */}
      <aside className="sidebar">
        <div className="sidebar-brand">
          <div className="logo-icon-bg">
            <Brain size={24} className="logo-icon" />
          </div>
          <div>
            <h1 className="brand-title">Anki Mongo</h1>
            <span className="brand-subtitle">C100DEV Flashcards</span>
          </div>
        </div>

        {/* Anki Card Queue Counts */}
        <div className="queue-box">
          <div className="queue-header">CURRENT QUEUE</div>
          <div className="queue-row">
            <div className="queue-item new-badge">
              <span className="queue-count">{sidebarCounts.new}</span>
              <span className="queue-label">New</span>
            </div>
            <div className="queue-item learn-badge">
              <span className="queue-count">{sidebarCounts.learning}</span>
              <span className="queue-label">Learn</span>
            </div>
            <div className="queue-item due-badge">
              <span className="queue-count">{sidebarCounts.due}</span>
              <span className="queue-label">Due</span>
            </div>
          </div>
          <div className="studied-stat">
            <Clock size={12} style={{ marginRight: 6 }} />
            Studied {todayStudiedCount} cards today
          </div>
        </div>

        {/* Sidebar Nav Links */}
        <nav className="sidebar-nav">
          <button 
            className={`nav-link ${activeTab === 'study' ? 'active' : ''}`}
            onClick={() => setActiveTab('study')}
          >
            <Layers size={18} className="nav-icon" />
            Study Deck
          </button>
          <button 
            className={`nav-link ${activeTab === 'browse' ? 'active' : ''}`}
            onClick={() => setActiveTab('browse')}
          >
            <Search size={18} className="nav-icon" />
            Browse Library
          </button>
          <button 
            className={`nav-link ${activeTab === 'stats' ? 'active' : ''}`}
            onClick={() => setActiveTab('stats')}
          >
            <BarChart3 size={18} className="nav-icon" />
            Progress & Stats
          </button>
        </nav>

        {/* Category Filters inside sidebar */}
        <div className="category-section">
          <div className="section-title-label">TOPIC REGION</div>
          <div className="category-list">
            {CATEGORIES.map(cat => (
              <button
                key={cat}
                className={`category-pill-sidebar ${selectedCategory === cat ? 'active' : ''}`}
                onClick={() => {
                  setSelectedCategory(cat);
                  setCurrentQueueIndex(0);
                  setIsFlipped(false);
                }}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>
      </aside>

      {/* Main Panel */}
      <main className="main-content-panel">
        
        {/* Study Deck Tab */}
        {activeTab === 'study' && (
          <div className="tab-pane">
            <header className="pane-header">
              <div>
                <h2 className="pane-title">Study Session</h2>
                <p className="pane-subtitle">
                  Category: <span className="text-cyan font-semibold">{selectedCategory}</span>
                </p>
              </div>

              {/* Study ahead toggle */}
              <div className="study-ahead-toggle-wrapper">
                <span className="toggle-label">Study Ahead Mode</span>
                <label className="switch-toggle">
                  <input 
                    type="checkbox" 
                    checked={studyAhead} 
                    onChange={(e) => {
                      setStudyAhead(e.target.checked);
                      setCurrentQueueIndex(0);
                      setIsFlipped(false);
                    }} 
                  />
                  <span className="slider-toggle rounded-toggle"></span>
                </label>
              </div>
            </header>

            {/* Study Container */}
            {studyQueue.length > 0 && currentCard ? (
              <div className="study-arena">
                
                {/* Progress bar info */}
                <div className="study-progress-bar-row">
                  <span className="queue-position-info">
                    Card {currentQueueIndex + 1} of {studyQueue.length}
                  </span>
                  
                  {currentCard.reps > 0 && (
                    <span className="interval-tag">
                      Ease: {currentCard.ease.toFixed(2)}x | Reps: {currentCard.reps} | Interval: {formatInterval(currentCard.interval)}
                    </span>
                  )}
                </div>

                {/* Flip Card Component */}
                <div className="card-wrapper" onClick={() => setIsFlipped(!isFlipped)}>
                  <div className={`card-inner ${isFlipped ? 'flipped' : ''}`}>
                    
                    {/* Front Face */}
                    <div className="card-face card-front">
                      <div className="card-top-header">
                        <span className="card-category-label">{currentCard.category}</span>
                        <span className="topic-badge">Topic {currentCard.subheading}</span>
                      </div>
                      <div className="card-body scrollable-y">
                        <p className="question-content">{currentCard.question}</p>
                      </div>
                      <div className="card-footer-tip">
                        <Sparkles size={14} className="sparkle-icon" />
                        <span>Click card or spacebar to reveal answer</span>
                      </div>
                    </div>

                    {/* Back Face */}
                    <div className="card-face card-back" onClick={(e) => e.stopPropagation()}>
                      <div className="card-top-header">
                        <span className="card-category-label">{currentCard.category}</span>
                        <span className="topic-badge back-badge">ANSWER SHEET</span>
                      </div>
                      <div className="card-body scrollable-y">
                        <div className="concept-summary-header">
                          Detailed Concept & Trap Guide
                        </div>
                        <div className="card-divider"></div>
                        {renderMarkdown(currentCard.answer)}
                      </div>
                      <div className="card-footer-tip back-footer-tip" onClick={() => setIsFlipped(false)}>
                        <RotateCcw size={14} style={{ marginRight: 6 }} />
                        <span>Click here to view question again</span>
                      </div>
                    </div>

                  </div>
                </div>

                {/* Anki Review Buttons (only visible when flipped) */}
                <div className="response-action-panel">
                  {isFlipped ? (
                    <div className="anki-buttons-bar">
                      
                      <button 
                        className="anki-btn btn-again"
                        onClick={() => handleResponse(0)}
                      >
                        <span className="anki-btn-time">{getIntervalPreview(currentCard, 0)}</span>
                        <span className="anki-btn-label">Again</span>
                      </button>

                      <button 
                        className="anki-btn btn-hard"
                        onClick={() => handleResponse(1)}
                      >
                        <span className="anki-btn-time">{getIntervalPreview(currentCard, 1)}</span>
                        <span className="anki-btn-label">Hard</span>
                      </button>

                      <button 
                        className="anki-btn btn-good"
                        onClick={() => handleResponse(2)}
                      >
                        <span className="anki-btn-time">{getIntervalPreview(currentCard, 2)}</span>
                        <span className="anki-btn-label">Good</span>
                      </button>

                      <button 
                        className="anki-btn btn-easy"
                        onClick={() => handleResponse(3)}
                      >
                        <span className="anki-btn-time">{getIntervalPreview(currentCard, 3)}</span>
                        <span className="anki-btn-label">Easy</span>
                      </button>

                    </div>
                  ) : (
                    <button className="reveal-large-btn" onClick={() => setIsFlipped(true)}>
                      Show Answer
                    </button>
                  )}
                </div>

              </div>
            ) : (
              <div className="empty-study-state">
                <CheckCircle2 size={64} className="success-icon" />
                <h3 className="empty-title">All Caught Up!</h3>
                <p className="empty-desc">
                  You have studied all cards due for review in this category.
                </p>
                <div className="empty-actions">
                  <button 
                    className="secondary-btn" 
                    onClick={() => {
                      setStudyAhead(true);
                      setCurrentQueueIndex(0);
                    }}
                  >
                    Study Ahead Mode
                  </button>
                  <button 
                    className="primary-btn" 
                    onClick={() => setSelectedCategory('All')}
                  >
                    Switch to All Topics
                  </button>
                </div>
              </div>
            )}
          </div>
        )}

        {/* Browse Tab */}
        {activeTab === 'browse' && (
          <div className="tab-pane">
            <header className="pane-header">
              <div>
                <h2 className="pane-title">Library Browser</h2>
                <p className="pane-subtitle">Browse and search through all 43 exam objectives.</p>
              </div>
            </header>

            {/* Search Input */}
            <div className="search-bar-wrapper">
              <Search className="search-pane-icon" size={18} />
              <input
                type="text"
                placeholder="Search by operators ($set, $elemMatch), index constraints, or driver code..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="search-pane-input"
              />
            </div>

            {/* Library list */}
            <div className="browse-list-container">
              {browsedCards.length > 0 ? (
                <div className="library-table-wrapper">
                  <table className="library-table">
                    <thead>
                      <tr>
                        <th width="80px">Objective</th>
                        <th width="180px">Exam Domain</th>
                        <th>Topic Title</th>
                        <th width="150px">Next Review</th>
                        <th width="120px">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {browsedCards.map(card => {
                        const isDue = card.nextReview > 0 && card.nextReview <= Date.now();
                        const isNew = card.reps === 0;
                        
                        let srsStatus = 'New';
                        let srsClass = 'status-new';
                        if (isDue) {
                          srsStatus = 'Due Now';
                          srsClass = 'status-due';
                        } else if (card.reps > 0) {
                          srsStatus = `in ${formatInterval((card.nextReview - Date.now()) / (24 * 60 * 60 * 1000))}`;
                          srsClass = 'status-learning';
                        }

                        return (
                          <tr key={card.id}>
                            <td className="font-semibold text-purple">{card.subheading}</td>
                            <td className="text-secondary-small">{card.category}</td>
                            <td className="text-title-bold">{card.title}</td>
                            <td>
                              <span className={`status-badge-web ${srsClass}`}>
                                {srsStatus}
                              </span>
                            </td>
                            <td>
                              <button 
                                className="study-card-btn"
                                onClick={() => handleStudyCardDirectly(card.id)}
                              >
                                Study Now
                                <ArrowRight size={12} style={{ marginLeft: 6 }} />
                              </button>
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              ) : (
                <div className="empty-study-state">
                  <AlertCircle size={48} className="warn-icon" />
                  <h3 className="empty-title">No Cards Found</h3>
                  <p className="empty-desc">Adjust your search parameters and filters.</p>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Stats Tab */}
        {activeTab === 'stats' && (
          <div className="tab-pane scrollable-pane">
            <header className="pane-header">
              <div>
                <h2 className="pane-title">Performance Analytics</h2>
                <p className="pane-subtitle">Visualize your readiness and card scheduler intervals.</p>
              </div>
            </header>

            <div className="stats-dashboard-grid">
              {/* Card stats */}
              <div className="stats-metric-card">
                <div className="metric-box">
                  <div className="metric-large-circle">
                    <span className="metric-percent-val">
                      {Math.round((statsOverview.mastered / statsOverview.total) * 100) || 0}%
                    </span>
                    <span className="metric-circle-lbl">Graduated</span>
                  </div>
                  
                  <div className="metric-list-details">
                    <div className="metric-detail-item">
                      <span className="legend-dot status-new"></span>
                      <span className="detail-lbl">Unseen (New)</span>
                      <span className="detail-val">{statsOverview.unseen}</span>
                    </div>
                    <div className="metric-detail-item">
                      <span className="legend-dot status-learning"></span>
                      <span className="detail-lbl">Learning</span>
                      <span className="detail-val">{statsOverview.learning}</span>
                    </div>
                    <div className="metric-detail-item">
                      <span className="legend-dot status-due"></span>
                      <span className="detail-lbl">Graduated (21d+)</span>
                      <span className="detail-val">{statsOverview.mastered}</span>
                    </div>
                    <div className="metric-detail-item total-item">
                      <span className="detail-lbl">Total Deck Size</span>
                      <span className="detail-val">{statsOverview.total} objectives</span>
                    </div>
                  </div>
                </div>

                {/* Progress bar */}
                <div className="bar-progress-stacked">
                  <div 
                    className="stacked-segment segment-mastered" 
                    style={{ width: `${(statsOverview.mastered / statsOverview.total) * 100}%` }}
                    title="Graduated"
                  ></div>
                  <div 
                    className="stacked-segment segment-learning" 
                    style={{ width: `${(statsOverview.learning / statsOverview.total) * 100}%` }}
                    title="Learning"
                  ></div>
                  <div 
                    className="stacked-segment segment-unseen" 
                    style={{ width: `${(statsOverview.unseen / statsOverview.total) * 100}%` }}
                    title="Unseen"
                  ></div>
                </div>
              </div>

              {/* Spaced repetition schedule preview */}
              <div className="stats-metric-card schedule-card">
                <h3 className="metric-card-title">REVIEW DISTRIBUTION</h3>
                <p className="metric-card-subtitle">Cards scheduled for review in future time blocks.</p>

                <div className="schedule-bar-chart">
                  {(() => {
                    const now = Date.now();
                    const dayMs = 24 * 60 * 60 * 1000;
                    
                    const distribution = [
                      { label: 'Due Now', count: cardsWithSRS.filter(c => c.reps > 0 && c.nextReview <= now).length },
                      { label: '1 Day', count: cardsWithSRS.filter(c => c.nextReview > now && c.nextReview <= now + dayMs).length },
                      { label: '2-3 Days', count: cardsWithSRS.filter(c => c.nextReview > now + dayMs && c.nextReview <= now + 3*dayMs).length },
                      { label: '4-7 Days', count: cardsWithSRS.filter(c => c.nextReview > now + 3*dayMs && c.nextReview <= now + 7*dayMs).length },
                      { label: '8+ Days', count: cardsWithSRS.filter(c => c.nextReview > now + 7*dayMs).length },
                    ];

                    const maxCount = Math.max(...distribution.map(d => d.count), 1);

                    return distribution.map(d => (
                      <div key={d.label} className="chart-column-row">
                        <span className="column-label-name">{d.label}</span>
                        <div className="bar-track-web">
                          <div 
                            className="bar-fill-web" 
                            style={{ width: `${(d.count / maxCount) * 100}%` }}
                          ></div>
                        </div>
                        <span className="column-label-value">{d.count}</span>
                      </div>
                    ));
                  })()}
                </div>
              </div>
            </div>

            {/* Domain breakdown */}
            <h3 className="section-header-web">SYLLABUS SUB-DOMAIN COVERAGE</h3>
            <div className="domain-breakdown-list">
              {CATEGORIES.slice(1).map(cat => {
                const catCards = cardsWithSRS.filter(c => c.category === cat);
                const total = catCards.length;
                const mastered = catCards.filter(c => c.interval >= 21).length;
                const learning = catCards.filter(c => c.reps > 0 && c.interval < 21).length;
                const percent = total > 0 ? Math.round(((mastered + learning) / total) * 100) : 0;

                return (
                  <div key={cat} className="domain-breakdown-row">
                    <div className="domain-row-meta">
                      <span className="domain-row-name">{cat}</span>
                      <span className="domain-row-percent">{percent}% Studied ({mastered + learning}/{total})</span>
                    </div>
                    <div className="domain-row-track">
                      <div className="domain-row-fill" style={{ width: `${percent}%` }}></div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Danger Zone */}
            <div className="danger-zone-box">
              <h3 className="danger-zone-title">RESET TOOL</h3>
              <p className="danger-zone-desc">This will erase all progress, ease modifiers, intervals, and study history.</p>
              <button className="clear-data-btn" onClick={resetAllProgress}>
                <Trash2 size={16} style={{ marginRight: 6 }} />
                Erase My Progress
              </button>
            </div>
          </div>
        )}

      </main>
    </div>
  );
}
