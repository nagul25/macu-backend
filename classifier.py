"""
classifier.py - Azure OpenAI integration for classifying case summaries.
"""

import json
import os
from typing import List, Dict, Set, Tuple, Optional

from openai import AzureOpenAI


def get_azure_client() -> Tuple[AzureOpenAI, str]:
    """
    Create an Azure OpenAI client using environment variables.
    
    Required env vars:
        - AZURE_AI_FOUNDRY_ENDPOINT
        - AZURE_AI_FOUNDRY_KEY
        - AZURE_AI_FOUNDRY_DEPLOYMENT
        - AZURE_AI_FOUNDRY_API_VERSION
    
    Returns:
        Tuple of (client, deployment_name)
    """
    endpoint = os.environ.get("AZURE_AI_FOUNDRY_ENDPOINT")
    api_key = os.environ.get("AZURE_AI_FOUNDRY_KEY")
    deployment = os.environ.get("AZURE_AI_FOUNDRY_DEPLOYMENT", "gpt-5-mini")
    api_version = os.environ.get("AZURE_AI_FOUNDRY_API_VERSION", "2025-04-01-preview")
    
    if not endpoint:
        raise ValueError("AZURE_AI_FOUNDRY_ENDPOINT environment variable is required")
    if not api_key:
        raise ValueError("AZURE_AI_FOUNDRY_KEY environment variable is required")
    
    client = AzureOpenAI(
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version
    )
    
    return client, deployment


def build_prompt(case_summary: str, allowed_tags: List[str], top_k: int = 4) -> str:
    """
    Build a prompt for classifying a case summary into issue tags.
    
    Args:
        case_summary: The case summary text to classify
        allowed_tags: List of allowed tag values
        top_k: Maximum number of tags to return (default: 4)
    
    Returns:
        The prompt string
    """
    tags_list = "\n".join(f"- {tag}" for tag in allowed_tags)
    
    prompt = f"""You are a customer service issue classifier. Analyze the following case summary and classify it into the most relevant issue tags.

STRICT RULES:
1. Return ONLY valid JSON in this exact format: {{"tags": ["tag1", "tag2", ...]}}
2. Choose ONLY from the allowed tags list below - use exact spelling and case
3. Return between 0 and {top_k} tags (no more than {top_k})
4. No duplicate tags
5. Only include tags that are clearly relevant to the case
6. If unsure, return fewer tags rather than guessing
7. Do NOT include any explanation or text outside the JSON

ALLOWED TAGS:
{tags_list}

CASE SUMMARY:
{case_summary}

Respond with only the JSON object:"""
    
    return prompt


def call_llm(
    client: AzureOpenAI,
    deployment: str,
    prompt: str,
    max_retries: int = 3
) -> Dict:
    """
    Call the Azure OpenAI API and parse the JSON response.
    
    Args:
        client: Azure OpenAI client
        deployment: Deployment name
        prompt: The prompt to send
        max_retries: Maximum retries on JSON parse failure (default: 3)
    
    Returns:
        Dict with parsed response or error info:
            - On success: {"tags": [...], "raw_response": "...", "success": True}
            - On failure: {"tags": [], "raw_response": "...", "success": False, "error": "..."}
    """
    last_error = None
    last_response = ""
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": "You are a precise classification assistant that only outputs valid JSON."},
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = response.choices[0].message.content.strip()
            last_response = content
            
            # Try to parse as JSON
            parsed = json.loads(content)
            
            # Validate structure
            if "tags" not in parsed:
                raise ValueError("Response missing 'tags' key")
            
            if not isinstance(parsed["tags"], list):
                raise ValueError("'tags' must be a list")
            
            return {
                "tags": parsed["tags"],
                "raw_response": content,
                "success": True
            }
            
        except json.JSONDecodeError as e:
            last_error = f"JSON parse error: {e}"
        except ValueError as e:
            last_error = str(e)
        except Exception as e:
            last_error = f"API error: {e}"
    
    # All retries failed
    return {
        "tags": [],
        "raw_response": last_response,
        "success": False,
        "error": last_error
    }


def validate_and_normalize_tags(
    raw_tags: List,
    allowed_set: Set[str],
    lower_to_tag: Dict[str, str],
    top_k: int = 4
) -> Tuple[List[str], bool]:
    """
    Validate and normalize tags from LLM response.
    
    Args:
        raw_tags: List of tags from LLM (may contain invalid values)
        allowed_set: Set of allowed tag strings
        lower_to_tag: Dict mapping lowercase tag to original case
        top_k: Maximum number of tags to return
    
    Returns:
        Tuple of:
            - List of valid, normalized tags (deduplicated, max top_k)
            - needs_review flag (True if no valid tags remain)
    """
    valid_tags: List[str] = []
    seen_lower: Set[str] = set()
    
    for tag in raw_tags:
        # Skip non-string values
        if not isinstance(tag, str):
            continue
        
        tag_stripped = tag.strip()
        tag_lower = tag_stripped.lower()
        
        # Check if it's an exact match (case-sensitive)
        if tag_stripped in allowed_set:
            if tag_lower not in seen_lower:
                seen_lower.add(tag_lower)
                valid_tags.append(tag_stripped)
        # Check case-insensitive match
        elif tag_lower in lower_to_tag:
            normalized = lower_to_tag[tag_lower]
            if tag_lower not in seen_lower:
                seen_lower.add(tag_lower)
                valid_tags.append(normalized)
        # Invalid tag - skip it
    
    # Limit to top_k
    valid_tags = valid_tags[:top_k]
    
    # needs_review if no valid tags
    needs_review = len(valid_tags) == 0
    
    return valid_tags, needs_review


def classify_summary(
    client: AzureOpenAI,
    deployment: str,
    case_summary: str,
    allowed_tags: List[str],
    allowed_set: Set[str],
    lower_to_tag: Dict[str, str],
    tag_to_class: Dict[str, str],
    top_k: int = 4,
    max_retries: int = 3
) -> Dict:
    """
    Classify a single case summary into issue tags.
    
    Args:
        client: Azure OpenAI client
        deployment: Deployment name
        case_summary: Text to classify
        allowed_tags: List of allowed tags (for prompt)
        allowed_set: Set of allowed tags (for validation)
        lower_to_tag: Lowercase to original case mapping
        tag_to_class: Tag to classification mapping
        top_k: Max tags to return
        max_retries: Max LLM retries
    
    Returns:
        Dict with:
            - tags: List of valid tags
            - classifications: List of classification strings
            - needs_review: Boolean flag
            - raw_response: Raw LLM response
            - error: Error message if any
    """
    # Handle empty or NaN summaries
    if not case_summary or (isinstance(case_summary, float) and str(case_summary) == "nan"):
        return {
            "tags": [],
            "classifications": [],
            "needs_review": True,
            "raw_response": "",
            "error": "Empty case summary"
        }
    
    summary_str = str(case_summary).strip()
    if not summary_str:
        return {
            "tags": [],
            "classifications": [],
            "needs_review": True,
            "raw_response": "",
            "error": "Empty case summary"
        }
    
    # Build prompt and call LLM
    prompt = build_prompt(summary_str, allowed_tags, top_k)
    llm_result = call_llm(client, deployment, prompt, max_retries)
    
    # Handle LLM failure
    if not llm_result["success"]:
        return {
            "tags": [],
            "classifications": [],
            "needs_review": True,
            "raw_response": llm_result.get("raw_response", ""),
            "error": llm_result.get("error", "Unknown error")
        }
    
    # Validate and normalize tags
    valid_tags, needs_review = validate_and_normalize_tags(
        llm_result["tags"],
        allowed_set,
        lower_to_tag,
        top_k
    )
    
    # Map to classifications
    classifications = [tag_to_class.get(tag, "") for tag in valid_tags]
    
    return {
        "tags": valid_tags,
        "classifications": classifications,
        "needs_review": needs_review,
        "raw_response": llm_result["raw_response"],
        "error": None
    }


if __name__ == "__main__":
    # Quick test with mock data
    from dotenv import load_dotenv
    load_dotenv()
    
    test_tags = ["agent behavior", "card fraud", "technical issue"]
    test_set = set(test_tags)
    test_lower = {t.lower(): t for t in test_tags}
    
    print("Testing validate_and_normalize_tags...")
    
    # Test with valid tags
    result, needs_review = validate_and_normalize_tags(
        ["Agent Behavior", "card fraud"],
        test_set,
        test_lower
    )
    print(f"  Valid input: {result}, needs_review={needs_review}")
    
    # Test with invalid tags
    result, needs_review = validate_and_normalize_tags(
        ["invalid tag", "not a tag"],
        test_set,
        test_lower
    )
    print(f"  Invalid input: {result}, needs_review={needs_review}")
    
    # Test with mixed
    result, needs_review = validate_and_normalize_tags(
        ["Agent Behavior", "invalid", "technical issue"],
        test_set,
        test_lower
    )
    print(f"  Mixed input: {result}, needs_review={needs_review}")

