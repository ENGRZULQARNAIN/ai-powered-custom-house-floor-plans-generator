from langchain.schema.output_parser import BaseOutputParser, OutputParserException
import re

class SVGOutputParser(BaseOutputParser):
    """Parser for extracting SVG content from LLM responses."""
    
    def parse(self, text: str) -> str:
        """Extract SVG content from the text.
        
        Args:
            text: The text to parse, potentially containing SVG.
            
        Returns:
            The extracted SVG as a string.
            
        Raises:
            OutputParserException: If no SVG content is found.
        """
        # Look for SVG content between <svg> and </svg> tags (including the tags)
        svg_pattern = r'(<svg[\s\S]*?<\/svg>)'
        match = re.search(svg_pattern, text, re.IGNORECASE)
        
        if match:
            return match.group(1)
        else:
            raise OutputParserException(f"Could not extract SVG from provided text: {text}")