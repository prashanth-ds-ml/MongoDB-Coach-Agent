from typing import List, Optional, Dict, Any
from dataclasses import dataclass, field

@dataclass
class Section:
    section_id: str
    heading: str
    heading_level: int
    content: str = ""
    code_blocks: List[str] = field(default_factory=list)
    subsections: List[Dict[str, Any]] = field(default_factory=list)

@dataclass
class ScrapedDoc:
    url: str
    doc_type: str
    method_name: Optional[str]
    title: str
    version: Optional[str]
    breadcrumbs: List[str]
    sections: List[Section]
    fetched_at: str
