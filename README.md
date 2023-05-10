## Scope
To upload a raw order transaction file(raw_data.csv), the service will eventually gererate rfm-segments.csv. (Please check the sample files)

Ref: [RFM Analysis](https://joaocorreia.io/blog/rfm-analysis-increase-sales-by-segmenting-your-customers.html)

## Services
- /web: Django, port 8000, expose to public tunnel
- /api: FastAPI, port 8001
- postgres: port 5432, expose to containers only
