from __future__ import annotations

import requests
import time
from typing import Any, Dict, Optional, Tuple


def fetch_nvd_exploits(cve_id: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """
    NVD fetcher with 5 retry attempts and delays: 5, 10, 20, 30, 40 seconds.
    Shows retry messages and final failure.
    """
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?cveId={cve_id}"

    max_retries = 5
    delays = [5, 10, 20, 30, 40]

    for attempt in range(max_retries):
        try:
            # Ждем перед запросом
            wait_time = delays[attempt]
            if attempt > 0:
                print(f"⏳ NVD retry {attempt + 1}/{max_retries} для {cve_id}, ждем {wait_time}с...")
            time.sleep(wait_time)

            response = requests.get(url, timeout=30)

            if response.status_code == 429:
                if attempt < max_retries - 1:
                    print(f"⚠️ NVD 429 для {cve_id}, следующая попытка через {delays[attempt + 1]}с")
                    continue
                else:
                    print(f"❌ NVD rate limit для {cve_id} после {max_retries} попыток")
                    return {"exploits": []}, f"NVD rate limit (429) after {max_retries} attempts"

            if response.status_code >= 400:
                print(f"❌ NVD HTTP error {response.status_code} для {cve_id}")
                return {"exploits": []}, f"NVD HTTP error: {response.status_code}"

            response.raise_for_status()
            data = response.json()

            # Извлекаем эксплойты
            exploits = []
            if data.get('totalResults', 0) > 0:
                vulnerabilities = data.get('vulnerabilities', [])
                if vulnerabilities:
                    references = vulnerabilities[0]['cve'].get('references', [])

                    # Собираем все ссылки с тегом exploit
                    exploit_urls = []
                    for ref in references:
                        tags = ref.get('tags', [])
                        url_value = ref.get('url', '').strip()
                        if any('exploit' in tag.lower() for tag in tags) and url_value:
                            exploit_urls.append(url_value)

                    # Убираем дубликаты (сохраняя порядок)
                    exploits = list(dict.fromkeys(exploit_urls))

            if attempt > 0:
                print(f"✅ NVD для {cve_id} получен после {attempt + 1} попыток")

            return {"exploits": exploits}, None

        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                print(f"⚠️ NVD timeout для {cve_id}, повтор через {delays[attempt + 1]}с")
            else:
                print(f"❌ NVD timeout для {cve_id} после {max_retries} попыток")
                return {"exploits": []}, "NVD API timeout"

        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                print(f"⚠️ NVD error для {cve_id}: {e}, повтор через {delays[attempt + 1]}с")
            else:
                print(f"❌ NVD failed для {cve_id} после {max_retries} попыток: {e}")
                return {"exploits": []}, f"NVD API request failed: {e}"

        except Exception as e:
            if attempt == max_retries - 1:
                print(f"❌ NVD unexpected error для {cve_id}: {e}")
                return {"exploits": []}, f"NVD error: {e}"

    print(f"❌ NVD failed для {cve_id} после всех попыток")
    return {"exploits": []}, "NVD failed after all retries"