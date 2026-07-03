import React, { useState, useEffect, useRef } from 'react';
import {
  StyleSheet,
  Text,
  View,
  ScrollView,
  TouchableOpacity,
  TextInput,
  Animated,
  Alert,
  SafeAreaView,
  Dimensions,
  StatusBar
} from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Ionicons } from '@expo/vector-icons';
import flashcardsData from './assets/flashcards.json';

const { width } = Dimensions.get('window');

// Color Palette
const COLORS = {
  BG_DARK: '#090A0F',
  BG_CARD: '#131520',
  BG_CARD_BACK: '#181A26',
  BORDER: '#21263D',
  TEXT_PRIMARY: '#FFFFFF',
  TEXT_SECONDARY: '#A0A5C0',
  CYAN: '#00E5FF',
  PURPLE: '#9D4EDD',
  GREEN: '#00F5D4',
  RED: '#FF4D6D',
  YELLOW: '#FFD166',
  TABS_BG: '#10121D',
};

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
  const [currentIdx, setCurrentIdx] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [activeTab, setActiveTab] = useState('deck'); // 'deck' | 'progress' | 'browse'
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [progress, setProgress] = useState({}); // cardId -> 'mastered' | 'review'

  // Card Flip Animation
  const animatedValue = useRef(new Animated.Value(0)).current;

  // Load progress from AsyncStorage on mount
  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      const storedProgress = await AsyncStorage.getItem('@certcoach_progress');
      if (storedProgress !== null) {
        setProgress(JSON.parse(storedProgress));
      }
    } catch (e) {
      console.error('Failed to load progress', e);
    }
  };

  const saveProgress = async (newProgress) => {
    try {
      await AsyncStorage.setItem('@certcoach_progress', JSON.stringify(newProgress));
    } catch (e) {
      console.error('Failed to save progress', e);
    }
  };

  // Filter cards based on selected category
  const filteredCards = cards.filter(card => {
    if (selectedCategory === 'All') return true;
    return card.category === selectedCategory;
  });

  // Filter cards for browse search
  const browsedCards = cards.filter(card => {
    const query = searchQuery.toLowerCase();
    const matchesSearch = 
      card.title.toLowerCase().includes(query) ||
      card.question.toLowerCase().includes(query) ||
      card.answer.toLowerCase().includes(query) ||
      card.subheading.includes(query) ||
      card.category.toLowerCase().includes(query);
      
    if (selectedCategory === 'All') return matchesSearch;
    return card.category === selectedCategory && matchesSearch;
  });

  const currentCard = filteredCards[currentIdx] || null;

  const flipCard = () => {
    if (isFlipped) {
      Animated.spring(animatedValue, {
        toValue: 0,
        friction: 8,
        tension: 10,
        useNativeDriver: true,
      }).start();
    } else {
      Animated.spring(animatedValue, {
        toValue: 180,
        friction: 8,
        tension: 10,
        useNativeDriver: true,
      }).start();
    }
    setIsFlipped(!isFlipped);
  };

  const resetCardRotation = () => {
    setIsFlipped(false);
    animatedValue.setValue(0);
  };

  const handleNext = () => {
    if (filteredCards.length === 0) return;
    resetCardRotation();
    setCurrentIdx((prev) => (prev + 1) % filteredCards.length);
  };

  const handlePrev = () => {
    if (filteredCards.length === 0) return;
    resetCardRotation();
    setCurrentIdx((prev) => (prev - 1 + filteredCards.length) % filteredCards.length);
  };

  const markProgress = (status) => {
    if (!currentCard) return;
    const newProgress = {
      ...progress,
      [currentCard.id]: status
    };
    setProgress(newProgress);
    saveProgress(newProgress);
    
    // Automatically advance to next card after marking
    setTimeout(() => {
      handleNext();
    }, 200);
  };

  const resetAllProgress = () => {
    Alert.alert(
      "Reset Progress",
      "Are you sure you want to clear all your flashcard study progress?",
      [
        { text: "Cancel", style: "cancel" },
        { 
          text: "Reset", 
          style: "destructive",
          onPress: async () => {
            setProgress({});
            await AsyncStorage.removeItem('@certcoach_progress');
          }
        }
      ]
    );
  };

  // Card Flip Interpolations
  const frontInterpolate = animatedValue.interpolate({
    inputRange: [0, 180],
    outputRange: ['0deg', '180deg'],
  });

  const backInterpolate = animatedValue.interpolate({
    inputRange: [0, 180],
    outputRange: ['180deg', '360deg'],
  });

  const frontAnimatedStyle = {
    transform: [{ rotateY: frontInterpolate }]
  };

  const backAnimatedStyle = {
    transform: [{ rotateY: backInterpolate }]
  };

  // Inline Style Parser helper for markdown rendering
  const renderInlineStyle = (text) => {
    const parts = [];
    const regex = /\*\*(.*?)\*\*|`(.*?)`/g;
    let lastIndex = 0;
    let match;
    let keyIdx = 0;

    while ((match = regex.exec(text)) !== null) {
      const plainText = text.substring(lastIndex, match.index);
      if (plainText) {
        parts.push(<Text key={`plain-${keyIdx++}`}>{plainText}</Text>);
      }

      if (match[1]) {
        parts.push(<Text key={`bold-${keyIdx++}`} style={styles.boldText}>{match[1]}</Text>);
      } else if (match[2]) {
        parts.push(
          <Text key={`inline-code-${keyIdx++}`} style={styles.inlineCode}>
            {match[2]}
          </Text>
        );
      }
      lastIndex = regex.lastIndex;
    }

    const remaining = text.substring(lastIndex);
    if (remaining) {
      parts.push(<Text key={`plain-end`}>{remaining}</Text>);
    }

    return parts.length > 0 ? parts : text;
  };

  // Custom Markdown block renderer for React Native
  const renderMarkdown = (text) => {
    if (!text) return null;
    const parts = [];
    const lines = text.split('\n');
    let inCodeBlock = false;
    let codeLines = [];
    let codeLang = '';

    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const trimmed = line.trim();
      
      if (trimmed.startsWith('```')) {
        if (inCodeBlock) {
          parts.push({
            type: 'code',
            content: codeLines.join('\n'),
            lang: codeLang,
            key: `code-${i}`
          });
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
          parts.push({ type: 'h2', content: trimmed.replace('## ', ''), key: `h2-${i}` });
        } else if (trimmed.startsWith('### ')) {
          parts.push({ type: 'h3', content: trimmed.replace('### ', ''), key: `h3-${i}` });
        } else if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
          parts.push({ type: 'bullet', content: trimmed.substring(2), key: `bullet-${i}` });
        } else if (trimmed.startsWith('`o` ') || trimmed.startsWith('o ')) {
          parts.push({ type: 'bullet', content: trimmed.substring(2), key: `bullet-${i}` });
        } else if (trimmed === '') {
          parts.push({ type: 'space', key: `space-${i}` });
        } else {
          parts.push({ type: 'paragraph', content: line, key: `p-${i}` });
        }
      }
    }

    if (inCodeBlock && codeLines.length > 0) {
      parts.push({
        type: 'code',
        content: codeLines.join('\n'),
        lang: codeLang,
        key: `code-end`
      });
    }

    return parts.map(part => {
      switch (part.type) {
        case 'h2':
          return <Text key={part.key} style={styles.mdH2}>{renderInlineStyle(part.content)}</Text>;
        case 'h3':
          return <Text key={part.key} style={styles.mdH3}>{renderInlineStyle(part.content)}</Text>;
        case 'bullet':
          return (
            <View key={part.key} style={styles.bulletRow}>
              <Text style={styles.bulletDot}>•</Text>
              <Text style={styles.bulletText}>{renderInlineStyle(part.content)}</Text>
            </View>
          );
        case 'code':
          return (
            <View key={part.key} style={styles.codeBlock}>
              <View style={styles.codeBlockHeader}>
                <Text style={styles.codeBlockLang}>{part.lang.toUpperCase() || 'MONGODB'}</Text>
              </View>
              <ScrollView horizontal showsHorizontalScrollIndicator={true} style={styles.codeScroll}>
                <Text style={styles.codeText}>{part.content}</Text>
              </ScrollView>
            </View>
          );
        case 'space':
          return <View key={part.key} style={styles.mdSpace} />;
        default:
          return <Text key={part.key} style={styles.mdParagraph}>{renderInlineStyle(part.content)}</Text>;
      }
    });
  };

  // Compute Statistics for Progress Screen
  const totalCount = cards.length;
  const masteredCount = Object.values(progress).filter(v => v === 'mastered').length;
  const reviewCount = Object.values(progress).filter(v => v === 'review').length;
  const unseenCount = totalCount - masteredCount - reviewCount;
  const masteredPercent = totalCount > 0 ? Math.round((masteredCount / totalCount) * 100) : 0;

  const getCategoryStats = (categoryName) => {
    const catCards = cards.filter(c => c.category === categoryName);
    const catTotal = catCards.length;
    const catMastered = catCards.filter(c => progress[c.id] === 'mastered').length;
    const catReview = catCards.filter(c => progress[c.id] === 'review').length;
    const catUnseen = catTotal - catMastered - catReview;
    const catPercent = catTotal > 0 ? Math.round((catMastered / catTotal) * 100) : 0;
    return { catTotal, catMastered, catReview, catUnseen, catPercent };
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" />
      
      {/* Header */}
      <View style={styles.header}>
        <View style={styles.headerTitleRow}>
          <Ionicons name="brain" size={26} color={COLORS.PURPLE} style={styles.headerIcon} />
          <Text style={styles.headerTitle}>CertCoach</Text>
          <Text style={styles.headerHighlight}>Flashcards</Text>
        </View>
        <Text style={styles.headerSubtitle}>MongoDB C100DEV Certification Study Tool</Text>
      </View>

      {/* Category Horizontal Filter (Shown in Deck & Browse tabs) */}
      {activeTab !== 'progress' && (
        <View style={styles.filterWrapper}>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.filterScroll}>
            {CATEGORIES.map((cat) => (
              <TouchableOpacity
                key={cat}
                style={[
                  styles.filterPill,
                  selectedCategory === cat && styles.filterPillActive
                ]}
                onPress={() => {
                  setSelectedCategory(cat);
                  setCurrentIdx(0);
                  resetCardRotation();
                }}
              >
                <Text
                  style={[
                    styles.filterText,
                    selectedCategory === cat && styles.filterTextActive
                  ]}
                >
                  {cat}
                </Text>
              </TouchableOpacity>
            ))}
          </ScrollView>
        </View>
      )}

      {/* Main Content Area */}
      <View style={styles.content}>
        {activeTab === 'deck' && (
          <View style={styles.tabContent}>
            {filteredCards.length > 0 && currentCard ? (
              <View style={styles.deckContainer}>
                
                {/* Progress Indicators */}
                <View style={styles.deckHeader}>
                  <Text style={styles.deckCount}>
                    Card {currentIdx + 1} of {filteredCards.length}
                  </Text>
                  
                  {/* Small card mastered indicator */}
                  {progress[currentCard.id] && (
                    <View style={[
                      styles.statusBadge, 
                      currentCard && progress[currentCard.id] === 'mastered' ? styles.badgeMastered : styles.badgeReview
                    ]}>
                      <Text style={styles.statusBadgeText}>
                        {progress[currentCard.id] === 'mastered' ? 'Mastered' : 'Needs Review'}
                      </Text>
                    </View>
                  )}
                </View>

                {/* 3D Flappable Card wrapper */}
                <TouchableOpacity activeOpacity={0.95} onPress={flipCard} style={styles.cardContainer}>
                  
                  {/* Front Card Face */}
                  <Animated.View style={[styles.card, styles.cardFront, frontAnimatedStyle, {
                    backfaceVisibility: 'hidden',
                  }]}>
                    <View style={styles.cardTagRow}>
                      <Text style={styles.cardCategory}>{currentCard.category}</Text>
                      <View style={styles.subheadingContainer}>
                        <Text style={styles.cardSubheading}>Topic {currentCard.subheading}</Text>
                      </View>
                    </View>
                    <ScrollView style={styles.cardScrollView} contentContainerStyle={styles.cardScrollContent}>
                      <Text style={styles.questionText}>{currentCard.question}</Text>
                    </ScrollView>
                    <View style={styles.cardFooter}>
                      <Ionicons name="eye-outline" size={16} color={COLORS.CYAN} />
                      <Text style={styles.flipPrompt}>Tap card to reveal answer</Text>
                    </View>
                  </Animated.View>

                  {/* Back Card Face */}
                  <Animated.View style={[styles.card, styles.cardBack, backAnimatedStyle, {
                    position: 'absolute',
                    top: 0,
                    backfaceVisibility: 'hidden',
                  }]}>
                    <View style={styles.cardTagRow}>
                      <Text style={styles.cardCategory}>{currentCard.category}</Text>
                      <View style={[styles.subheadingContainer, { backgroundColor: COLORS.CYAN }]}>
                        <Text style={[styles.cardSubheading, { color: COLORS.BG_DARK }]}>ANSWER</Text>
                      </View>
                    </View>
                    <ScrollView style={styles.cardScrollView} contentContainerStyle={styles.cardScrollContent}>
                      <Text style={styles.answerTitle}>Topic {currentCard.subheading} - Detailed Concept & Trap Guide</Text>
                      <View style={styles.divider} />
                      {renderMarkdown(currentCard.answer)}
                    </ScrollView>
                    <View style={styles.cardFooter}>
                      <Ionicons name="refresh-outline" size={16} color={COLORS.PURPLE} />
                      <Text style={[styles.flipPrompt, { color: COLORS.PURPLE }]}>Tap card to view question</Text>
                    </View>
                  </Animated.View>

                </TouchableOpacity>

                {/* Study Deck Control Bar */}
                <View style={styles.controlsRow}>
                  <TouchableOpacity onPress={handlePrev} style={styles.navButton}>
                    <Ionicons name="arrow-back" size={24} color={COLORS.TEXT_PRIMARY} />
                  </TouchableOpacity>

                  <View style={styles.actionButtons}>
                    <TouchableOpacity 
                      onPress={() => markProgress('review')} 
                      style={[styles.actionBtn, styles.btnReview]}
                    >
                      <Ionicons name="close-circle" size={20} color={COLORS.BG_DARK} style={styles.btnIcon} />
                      <Text style={styles.actionBtnText}>Review</Text>
                    </TouchableOpacity>

                    <TouchableOpacity 
                      onPress={() => markProgress('mastered')} 
                      style={[styles.actionBtn, styles.btnMastered]}
                    >
                      <Ionicons name="checkmark-circle" size={20} color={COLORS.BG_DARK} style={styles.btnIcon} />
                      <Text style={styles.actionBtnText}>Got It!</Text>
                    </TouchableOpacity>
                  </View>

                  <TouchableOpacity onPress={handleNext} style={styles.navButton}>
                    <Ionicons name="arrow-forward" size={24} color={COLORS.TEXT_PRIMARY} />
                  </TouchableOpacity>
                </View>

              </View>
            ) : (
              <View style={styles.emptyState}>
                <Ionicons name="alert-circle-outline" size={50} color={COLORS.TEXT_SECONDARY} />
                <Text style={styles.emptyText}>No flashcards match this category filter.</Text>
              </View>
            )}
          </View>
        )}

        {activeTab === 'browse' && (
          <View style={styles.tabContent}>
            
            {/* Search Bar */}
            <View style={styles.searchContainer}>
              <Ionicons name="search" size={20} color={COLORS.TEXT_SECONDARY} style={styles.searchIcon} />
              <TextInput
                style={styles.searchInput}
                placeholder="Search index limits, operators, syntax..."
                placeholderTextColor={COLORS.TEXT_SECONDARY}
                value={searchQuery}
                onChangeText={setSearchQuery}
                clearButtonMode="always"
              />
            </View>

            {/* List of cards */}
            {browsedCards.length > 0 ? (
              <ScrollView style={styles.browseList} contentContainerStyle={styles.browseListContent}>
                {browsedCards.map((card) => {
                  const cardIndexInFiltered = filteredCards.findIndex(fc => fc.id === card.id);
                  const isMatchSelectedCategory = selectedCategory === 'All' || card.category === selectedCategory;

                  return (
                    <TouchableOpacity
                      key={card.id}
                      style={styles.browseItem}
                      onPress={() => {
                        // Switch categories if needed
                        if (!isMatchSelectedCategory) {
                          setSelectedCategory('All');
                        }
                        
                        // We need to set the index to match the selected card's index in whatever deck will be loaded
                        const finalDeck = isMatchSelectedCategory ? filteredCards : cards;
                        const idx = finalDeck.findIndex(fc => fc.id === card.id);
                        if (idx !== -1) {
                          setCurrentIdx(idx);
                        }
                        resetCardRotation();
                        setActiveTab('deck');
                      }}
                    >
                      <View style={styles.browseItemLeft}>
                        <View style={styles.browseSubheadingCircle}>
                          <Text style={styles.browseSubheadingText}>{card.subheading}</Text>
                        </View>
                      </View>
                      
                      <View style={styles.browseItemMiddle}>
                        <Text style={styles.browseItemTitle} numberOfLines={2}>
                          {card.title}
                        </Text>
                        <Text style={styles.browseItemCategory}>{card.category}</Text>
                      </View>

                      <View style={styles.browseItemRight}>
                        {progress[card.id] ? (
                          <Ionicons 
                            name={progress[card.id] === 'mastered' ? "checkmark-circle" : "close-circle"} 
                            size={20} 
                            color={progress[card.id] === 'mastered' ? COLORS.GREEN : COLORS.RED} 
                          />
                        ) : (
                          <View style={styles.unseenDot} />
                        )}
                        <Ionicons name="chevron-forward" size={16} color={COLORS.BORDER} style={{ marginLeft: 8 }} />
                      </View>
                    </TouchableOpacity>
                  );
                })}
              </ScrollView>
            ) : (
              <View style={styles.emptyState}>
                <Ionicons name="search-outline" size={50} color={COLORS.TEXT_SECONDARY} />
                <Text style={styles.emptyText}>No cards match your search criteria.</Text>
              </View>
            )}
          </View>
        )}

        {activeTab === 'progress' && (
          <ScrollView style={styles.tabContent} contentContainerStyle={styles.progressScrollContent}>
            
            {/* Stats Dashboard Card */}
            <View style={styles.statsCard}>
              <Text style={styles.statsTitle}>OVERALL READINESS</Text>
              
              <View style={styles.mainProgressRow}>
                <View style={styles.circularPlaceholder}>
                  <Text style={styles.circularPercent}>{masteredPercent}%</Text>
                  <Text style={styles.circularLabel}>Ready</Text>
                </View>
                
                <View style={styles.statsGrid}>
                  <View style={styles.statGridItem}>
                    <Text style={[styles.statValue, { color: COLORS.GREEN }]}>{masteredCount}</Text>
                    <Text style={styles.statLabel}>Mastered</Text>
                  </View>
                  <View style={styles.statGridItem}>
                    <Text style={[styles.statValue, { color: COLORS.RED }]}>{reviewCount}</Text>
                    <Text style={styles.statLabel}>Needs Review</Text>
                  </View>
                  <View style={styles.statGridItem}>
                    <Text style={[styles.statValue, { color: COLORS.TEXT_SECONDARY }]}>{unseenCount}</Text>
                    <Text style={styles.statLabel}>Unseen</Text>
                  </View>
                </View>
              </View>

              {/* Progress Bar */}
              <View style={styles.progressBarWrapper}>
                <View style={styles.progressBarBackground}>
                  <View style={[styles.progressBarFill, { width: `${masteredPercent}%`, backgroundColor: COLORS.GREEN }]} />
                  <View style={[styles.progressBarFill, { 
                    width: `${totalCount > 0 ? Math.round((reviewCount / totalCount) * 100) : 0}%`, 
                    backgroundColor: COLORS.RED,
                    left: `${masteredPercent}%`,
                    position: 'absolute'
                  }]} />
                </View>
              </View>
            </View>

            {/* Category Progress Breakdown */}
            <Text style={styles.sectionHeader}>SYLLABUS TOPIC STATUS</Text>
            {CATEGORIES.slice(1).map((cat) => {
              const { catTotal, catMastered, catReview, catUnseen, catPercent } = getCategoryStats(cat);
              
              return (
                <View key={cat} style={styles.catStatRow}>
                  <View style={styles.catStatHeader}>
                    <Text style={styles.catStatTitle} numberOfLines={1}>{cat}</Text>
                    <Text style={styles.catStatCount}>
                      {catMastered}/{catTotal} Mastered ({catPercent}%)
                    </Text>
                  </View>
                  <View style={styles.progressBarBackgroundSmall}>
                    <View style={[styles.progressBarFill, { width: `${catPercent}%`, backgroundColor: COLORS.PURPLE }]} />
                  </View>
                </View>
              );
            })}

            {/* Clear Data Button */}
            <TouchableOpacity onPress={resetAllProgress} style={styles.resetButton}>
              <Ionicons name="trash-outline" size={18} color={COLORS.RED} style={{ marginRight: 8 }} />
              <Text style={styles.resetButtonText}>Reset Study Progress Data</Text>
            </TouchableOpacity>

          </ScrollView>
        )}
      </View>

      {/* Custom Bottom Tab Bar */}
      <View style={styles.tabBar}>
        <TouchableOpacity
          style={[styles.tabItem, activeTab === 'deck' && styles.tabItemActive]}
          onPress={() => setActiveTab('deck')}
        >
          <Ionicons 
            name={activeTab === 'deck' ? "albums" : "albums-outline"} 
            size={22} 
            color={activeTab === 'deck' ? COLORS.PURPLE : COLORS.TEXT_SECONDARY} 
          />
          <Text style={[styles.tabLabel, activeTab === 'deck' && styles.tabLabelActive]}>Deck</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.tabItem, activeTab === 'browse' && styles.tabItemActive]}
          onPress={() => setActiveTab('browse')}
        >
          <Ionicons 
            name={activeTab === 'browse' ? "search" : "search-outline"} 
            size={22} 
            color={activeTab === 'browse' ? COLORS.PURPLE : COLORS.TEXT_SECONDARY} 
          />
          <Text style={[styles.tabLabel, activeTab === 'browse' && styles.tabLabelActive]}>Browse</Text>
        </TouchableOpacity>

        <TouchableOpacity
          style={[styles.tabItem, activeTab === 'progress' && styles.tabItemActive]}
          onPress={() => setActiveTab('progress')}
        >
          <Ionicons 
            name={activeTab === 'progress' ? "bar-chart" : "bar-chart-outline"} 
            size={22} 
            color={activeTab === 'progress' ? COLORS.PURPLE : COLORS.TEXT_SECONDARY} 
          />
          <Text style={[styles.tabLabel, activeTab === 'progress' && styles.tabLabelActive]}>Progress</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.BG_DARK,
  },
  header: {
    paddingHorizontal: 20,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.BORDER,
  },
  headerTitleRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  headerIcon: {
    marginRight: 8,
  },
  headerTitle: {
    fontSize: 22,
    fontWeight: '800',
    color: COLORS.TEXT_PRIMARY,
  },
  headerHighlight: {
    fontSize: 22,
    fontWeight: '800',
    color: COLORS.PURPLE,
    marginLeft: 6,
  },
  headerSubtitle: {
    fontSize: 11,
    color: COLORS.TEXT_SECONDARY,
    marginTop: 2,
  },
  filterWrapper: {
    borderBottomWidth: 1,
    borderBottomColor: COLORS.BORDER,
  },
  filterScroll: {
    paddingHorizontal: 15,
    paddingVertical: 10,
  },
  filterPill: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: COLORS.BG_CARD,
    borderWidth: 1,
    borderColor: COLORS.BORDER,
    marginRight: 8,
  },
  filterPillActive: {
    backgroundColor: COLORS.PURPLE,
    borderColor: COLORS.PURPLE,
  },
  filterText: {
    fontSize: 12,
    color: COLORS.TEXT_SECONDARY,
    fontWeight: '600',
  },
  filterTextActive: {
    color: COLORS.TEXT_PRIMARY,
  },
  content: {
    flex: 1,
  },
  tabContent: {
    flex: 1,
  },
  deckContainer: {
    flex: 1,
    padding: 15,
    justifyContent: 'space-between',
  },
  deckHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 10,
  },
  deckCount: {
    fontSize: 13,
    color: COLORS.TEXT_SECONDARY,
    fontWeight: '600',
  },
  statusBadge: {
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 10,
  },
  badgeMastered: {
    backgroundColor: 'rgba(0, 245, 212, 0.15)',
    borderWidth: 1,
    borderColor: COLORS.GREEN,
  },
  badgeReview: {
    backgroundColor: 'rgba(255, 77, 109, 0.15)',
    borderWidth: 1,
    borderColor: COLORS.RED,
  },
  statusBadgeText: {
    fontSize: 10,
    fontWeight: '700',
    color: COLORS.TEXT_PRIMARY,
  },
  cardContainer: {
    flex: 1,
    height: 420,
    marginVertical: 10,
  },
  card: {
    width: '100%',
    height: '100%',
    backgroundColor: COLORS.BG_CARD,
    borderRadius: 16,
    borderWidth: 1,
    borderColor: COLORS.BORDER,
    padding: 20,
    shadowColor: COLORS.PURPLE,
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.15,
    shadowRadius: 10,
    elevation: 8,
    justifyContent: 'space-between',
  },
  cardFront: {
    // Styling specific to the front card face
  },
  cardBack: {
    backgroundColor: COLORS.BG_CARD_BACK,
    borderColor: COLORS.BORDER,
    shadowColor: COLORS.CYAN,
  },
  cardTagRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 15,
  },
  cardCategory: {
    fontSize: 11,
    fontWeight: '700',
    color: COLORS.TEXT_SECONDARY,
    textTransform: 'uppercase',
    letterSpacing: 1,
    flex: 1,
  },
  subheadingContainer: {
    backgroundColor: 'rgba(157, 78, 221, 0.2)',
    paddingHorizontal: 8,
    paddingVertical: 3,
    borderRadius: 6,
  },
  cardSubheading: {
    fontSize: 11,
    fontWeight: '700',
    color: COLORS.CYAN,
  },
  cardScrollView: {
    flex: 1,
  },
  cardScrollContent: {
    paddingBottom: 20,
  },
  questionText: {
    fontSize: 18,
    fontWeight: '600',
    color: COLORS.TEXT_PRIMARY,
    lineHeight: 28,
  },
  answerTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: COLORS.TEXT_PRIMARY,
    marginBottom: 5,
  },
  divider: {
    height: 1,
    backgroundColor: COLORS.BORDER,
    marginVertical: 10,
  },
  cardFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingTop: 10,
    borderTopWidth: 1,
    borderTopColor: COLORS.BORDER,
  },
  flipPrompt: {
    fontSize: 11,
    fontWeight: '600',
    color: COLORS.CYAN,
    marginLeft: 6,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  controlsRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingVertical: 10,
  },
  navButton: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: COLORS.BG_CARD,
    borderWidth: 1,
    borderColor: COLORS.BORDER,
    alignItems: 'center',
    justifyContent: 'center',
  },
  actionButtons: {
    flexDirection: 'row',
    flex: 1,
    marginHorizontal: 15,
    justifyContent: 'space-between',
  },
  actionBtn: {
    flex: 1,
    flexDirection: 'row',
    height: 44,
    borderRadius: 22,
    alignItems: 'center',
    justifyContent: 'center',
    marginHorizontal: 5,
  },
  btnIcon: {
    marginRight: 6,
  },
  btnReview: {
    backgroundColor: COLORS.RED,
  },
  btnMastered: {
    backgroundColor: COLORS.GREEN,
  },
  actionBtnText: {
    fontSize: 14,
    fontWeight: '700',
    color: COLORS.BG_DARK,
  },
  searchContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.BG_CARD,
    borderWidth: 1,
    borderColor: COLORS.BORDER,
    borderRadius: 10,
    margin: 15,
    paddingHorizontal: 10,
  },
  searchIcon: {
    marginRight: 8,
  },
  searchInput: {
    flex: 1,
    height: 44,
    color: COLORS.TEXT_PRIMARY,
    fontSize: 14,
  },
  browseList: {
    flex: 1,
  },
  browseListContent: {
    paddingHorizontal: 15,
    paddingBottom: 20,
  },
  browseItem: {
    flexDirection: 'row',
    backgroundColor: COLORS.BG_CARD,
    borderWidth: 1,
    borderColor: COLORS.BORDER,
    borderRadius: 12,
    padding: 12,
    marginBottom: 8,
    alignItems: 'center',
  },
  browseItemLeft: {
    marginRight: 12,
  },
  browseSubheadingCircle: {
    width: 38,
    height: 38,
    borderRadius: 19,
    backgroundColor: 'rgba(157, 78, 221, 0.15)',
    borderWidth: 1,
    borderColor: COLORS.PURPLE,
    alignItems: 'center',
    justifyContent: 'center',
  },
  browseSubheadingText: {
    color: COLORS.CYAN,
    fontSize: 12,
    fontWeight: '700',
  },
  browseItemMiddle: {
    flex: 1,
  },
  browseItemTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: COLORS.TEXT_PRIMARY,
  },
  browseItemCategory: {
    fontSize: 10,
    color: COLORS.TEXT_SECONDARY,
    marginTop: 2,
  },
  browseItemRight: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  unseenDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: COLORS.BORDER,
  },
  emptyState: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 30,
  },
  emptyText: {
    color: COLORS.TEXT_SECONDARY,
    fontSize: 14,
    marginTop: 10,
    textAlign: 'center',
  },
  progressScrollContent: {
    padding: 20,
    paddingBottom: 30,
  },
  statsCard: {
    backgroundColor: COLORS.BG_CARD,
    borderWidth: 1,
    borderColor: COLORS.BORDER,
    borderRadius: 16,
    padding: 20,
    marginBottom: 25,
    shadowColor: COLORS.CYAN,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  statsTitle: {
    fontSize: 11,
    fontWeight: '700',
    color: COLORS.TEXT_SECONDARY,
    letterSpacing: 1.5,
    marginBottom: 15,
  },
  mainProgressRow: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    marginBottom: 20,
  },
  circularPlaceholder: {
    width: 85,
    height: 85,
    borderRadius: 42.5,
    borderWidth: 6,
    borderColor: COLORS.PURPLE,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: 'rgba(157, 78, 221, 0.05)',
  },
  circularPercent: {
    fontSize: 20,
    fontWeight: '800',
    color: COLORS.TEXT_PRIMARY,
  },
  circularLabel: {
    fontSize: 9,
    color: COLORS.TEXT_SECONDARY,
    fontWeight: '600',
  },
  statsGrid: {
    flex: 1,
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginLeft: 15,
  },
  statGridItem: {
    alignItems: 'center',
  },
  statValue: {
    fontSize: 22,
    fontWeight: '800',
  },
  statLabel: {
    fontSize: 10,
    color: COLORS.TEXT_SECONDARY,
    marginTop: 4,
    fontWeight: '600',
  },
  progressBarWrapper: {
    marginTop: 5,
  },
  progressBarBackground: {
    height: 12,
    backgroundColor: COLORS.BORDER,
    borderRadius: 6,
    overflow: 'hidden',
    flexDirection: 'row',
    position: 'relative'
  },
  progressBarBackgroundSmall: {
    height: 6,
    backgroundColor: COLORS.BORDER,
    borderRadius: 3,
    overflow: 'hidden',
    marginTop: 6,
  },
  progressBarFill: {
    height: '100%',
  },
  sectionHeader: {
    fontSize: 12,
    fontWeight: '700',
    color: COLORS.TEXT_SECONDARY,
    letterSpacing: 1.5,
    marginBottom: 15,
  },
  catStatRow: {
    backgroundColor: COLORS.BG_CARD,
    borderWidth: 1,
    borderColor: COLORS.BORDER,
    borderRadius: 10,
    padding: 12,
    marginBottom: 10,
  },
  catStatHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  catStatTitle: {
    fontSize: 13,
    fontWeight: '600',
    color: COLORS.TEXT_PRIMARY,
    flex: 1,
    marginRight: 10,
  },
  catStatCount: {
    fontSize: 11,
    color: COLORS.CYAN,
    fontWeight: '600',
  },
  resetButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 20,
    paddingVertical: 15,
    borderWidth: 1,
    borderColor: 'rgba(255, 77, 109, 0.3)',
    borderRadius: 10,
    backgroundColor: 'rgba(255, 77, 109, 0.05)',
  },
  resetButtonText: {
    color: COLORS.RED,
    fontSize: 13,
    fontWeight: '700',
  },
  tabBar: {
    flexDirection: 'row',
    height: 56,
    backgroundColor: COLORS.TABS_BG,
    borderTopWidth: 1,
    borderTopColor: COLORS.BORDER,
    paddingBottom: 4,
  },
  tabItem: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 6,
  },
  tabItemActive: {
    borderTopWidth: 2,
    borderTopColor: COLORS.PURPLE,
  },
  tabLabel: {
    fontSize: 10,
    color: COLORS.TEXT_SECONDARY,
    marginTop: 2,
    fontWeight: '600',
  },
  tabLabelActive: {
    color: COLORS.TEXT_PRIMARY,
  },

  // Markdown Styles
  mdH2: {
    fontSize: 16,
    fontWeight: '700',
    color: COLORS.PURPLE,
    marginTop: 15,
    marginBottom: 6,
  },
  mdH3: {
    fontSize: 14,
    fontWeight: '700',
    color: COLORS.TEXT_PRIMARY,
    marginTop: 12,
    marginBottom: 4,
  },
  bulletRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    marginVertical: 3,
    paddingLeft: 5,
  },
  bulletDot: {
    color: COLORS.CYAN,
    fontSize: 14,
    marginRight: 6,
    lineHeight: 18,
  },
  bulletText: {
    color: COLORS.TEXT_SECONDARY,
    fontSize: 13,
    lineHeight: 18,
    flex: 1,
  },
  codeBlock: {
    backgroundColor: '#07080C',
    borderRadius: 8,
    borderWidth: 1,
    borderColor: COLORS.BORDER,
    marginVertical: 10,
    overflow: 'hidden',
  },
  codeBlockHeader: {
    backgroundColor: '#10121A',
    paddingVertical: 5,
    paddingHorizontal: 12,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.BORDER,
  },
  codeBlockLang: {
    color: COLORS.CYAN,
    fontSize: 9,
    fontWeight: '800',
    letterSpacing: 0.5,
  },
  codeScroll: {
    padding: 10,
  },
  codeText: {
    color: '#00E5FF',
    fontFamily: 'monospace',
    fontSize: 12,
  },
  mdSpace: {
    height: 10,
  },
  mdParagraph: {
    color: COLORS.TEXT_SECONDARY,
    fontSize: 13,
    lineHeight: 19,
    marginVertical: 4,
  },
  boldText: {
    fontWeight: '700',
    color: COLORS.TEXT_PRIMARY,
  },
  inlineCode: {
    fontFamily: 'monospace',
    color: COLORS.CYAN,
    backgroundColor: '#10121A',
    paddingHorizontal: 4,
    borderRadius: 4,
    fontSize: 12,
  },
});
