from __future__ import annotations

import requests
import time
import json
from typing import Any, Dict, List, Optional, Tuple


def fetch_nvd_exploits(cve_id: str, *, delay: float = 1.0) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    Fetch exploit references from NVD API for a given CVE.
    
    Returns:
        Tuple of (data_dict, error_string)
        data_dict format: {"exploits": [url1, url2, ...]}
    """
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"
    
    try:
        # Respect rate limiting
        time.sleep(delay)
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get('totalResults', 0) == 0:
            return {"exploits": []}, None
            
        vulnerabilities = data.get('vulnerabilities', [])
        if not vulnerabilities:
            return {"exploits": []}, None
            
        # Extract references with 'exploit' tag
        references = vulnerabilities[0]['cve'].get('references', [])
        exploits = set()
        
        for ref in references:
            tags = ref.get('tags', [])
            if any('exploit' in tag.lower() for tag in tags):
                exploits.add(ref['url'])
        
        return {"exploits": list(exploits)}, None
        
    except requests.exceptions.RequestException as e:
        return None, f"NVD API request failed: {e}"
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        return None, f"NVD data parsing failed: {e}"
    except Exception as e:
        return None, f"Unexpected error fetching NVD data: {e}"