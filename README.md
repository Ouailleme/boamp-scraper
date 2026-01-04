# 🇫🇷 BOAMP Scraper

> Scrape French public tenders (BOAMP) in 3 lines of Python

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/boamp-scraper.svg)](https://badge.fury.io/py/boamp-scraper)

---

## 🚀 Quick Start

```bash
pip install boamp-scraper
```

```python
from boamp import TenderScraper

scraper = TenderScraper()
tenders = scraper.search(keywords=["cloud", "cybersécurité"], limit=10)

for tender in tenders:
    print(f"{tender.title} - {tender.budget}€")
```

That's it! 🎉

---

## 📖 Features

- ✅ **Simple API** - 3 lines of code to get started
- ✅ **Async-first** - Built with asyncio for performance
- ✅ **Type-safe** - Full Pydantic v2 models
- ✅ **Filters** - Keywords, budget, region, category
- ✅ **Free tier** - 50 API calls/month (no credit card)
- ✅ **Premium** - Unlimited calls + AI analysis ($500/mo)

---

## 🆓 Free vs 💰 Premium

| Feature | Free | Premium |
|---------|------|---------|
| **API calls/month** | 50 | Unlimited |
| **BOAMP scraping** | ✅ | ✅ |
| **Filter by keywords** | ✅ | ✅ |
| **Filter by budget/region** | ✅ | ✅ |
| **AI analysis (GO/NO-GO)** | ❌ | ✅ |
| **Multi-sources** | ❌ | ✅ |
| **Webhooks** | ❌ | ✅ |
| **Support** | Community | Priority (<24h) |
| **Price** | $0 | $500/mo |

---

## 📚 Documentation

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Advanced Usage](#advanced-usage)
- [API Reference](./docs/API_REFERENCE.md)
- [Contributing](./CONTRIBUTING.md)

---

## 🔧 Installation

### From PyPI (Recommended)

```bash
pip install boamp-scraper
```

### From Source

```bash
git clone https://github.com/algora/boamp-scraper.git
cd boamp-scraper
pip install -e .
```

---

## 💻 Usage Examples

### Basic Search

```python
from boamp import TenderScraper

scraper = TenderScraper()
tenders = scraper.search(keywords=["développement", "application"], limit=20)

for tender in tenders:
    print(tender.title)
    print(tender.organisme)
    print(tender.budget)
    print(tender.url)
    print("---")
```

### Advanced Filtering

```python
from boamp import TenderScraper, TenderCategory

scraper = TenderScraper()
tenders = scraper.search(
    keywords=["cloud", "aws", "azure"],
    category=TenderCategory.IT_DEVELOPMENT,
    budget_min=50000,
    budget_max=500000,
    region="Île-de-France",
    limit=50
)
```

### Async Usage

```python
import asyncio
from boamp import TenderScraper

async def main():
    scraper = TenderScraper()
    tenders = await scraper.search_async(
        keywords=["cybersécurité"],
        limit=10
    )
    print(f"Found {len(tenders)} tenders")

asyncio.run(main())
```

### Export to CSV

```python
import csv
from boamp import TenderScraper

scraper = TenderScraper()
tenders = scraper.search(keywords=["site web"], limit=100)

with open("tenders.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Title", "Organisme", "Budget", "URL"])
    
    for tender in tenders:
        writer.writerow([
            tender.title,
            tender.organisme,
            tender.budget,
            tender.url
        ])
```

---

## 🎯 Roadmap

- [x] **Phase 1: MVP** (Week 1-4)
  - [x] Core scraper
  - [ ] PyPI package
  - [ ] Documentation
  - [ ] Tests

- [ ] **Phase 2: Free Launch** (Week 5-8)
  - [ ] GitHub public
  - [ ] ProductHunt launch
  - [ ] Reddit posts
  - [ ] 100 free users

- [ ] **Phase 3: Premium** (Week 9-12)
  - [ ] AI analysis
  - [ ] Multi-sources
  - [ ] Webhooks
  - [ ] Stripe integration
  - [ ] 10 premium users ($5k MRR)

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

**Current needs:**
- 🐛 Bug reports
- 📝 Documentation improvements
- ✨ Feature requests
- 🧪 Tests

---

## 📜 License

MIT © Algora

---

## 🔗 Links

- **Website:** https://boamp-scraper.com (Coming soon)
- **GitHub:** https://github.com/algora/boamp-scraper
- **PyPI:** https://pypi.org/project/boamp-scraper (Coming soon)
- **Issues:** https://github.com/algora/boamp-scraper/issues
- **Discussions:** https://github.com/algora/boamp-scraper/discussions

---

## 💪 Why BOAMP Scraper?

**Problem:** Manually checking BOAMP for tenders is time-consuming (hours/day).

**Solution:** Automate it in 3 lines of Python.

**Result:** Save 10+ hours/week, never miss an opportunity.

---

**Built with ❤️ for French public procurement**

**Status:** 🚧 MVP Phase (Week 1)  
**Next milestone:** PyPI package (Week 4)

