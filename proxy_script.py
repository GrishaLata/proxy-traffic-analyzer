from mitmproxy import ctx, http
import json
from urllib.parse import parse_qs, urlparse
from datetime import datetime

def format_headers(headers):
    return '\n'.join(f"{header}: {value}" for header, value in headers.items())

def try_parse_json(content):
    try:
        return json.dumps(json.loads(content), indent=4, sort_keys=True)
    except json.JSONDecodeError:
        return content

def request(flow: http.HTTPFlow) -> None:
    ctx.log.info(f"[{datetime.now()}] Request: {flow.request.method} {flow.request.url}")
    
   
    query_params = parse_qs(urlparse(flow.request.url).query)
    if query_params:
        ctx.log.info("Query Parameters:")
        for param, values in query_params.items():
            for value in values:
                ctx.log.info(f"    {param}: {value}")
                
    ctx.log.info("Request Headers:\n" + format_headers(flow.request.headers))
    
    
    content_type = flow.request.headers.get('Content-Type', '')
    if flow.request.content:
        if 'application/json' in content_type:
            ctx.log.info("Request Body (JSON):\n" + try_parse_json(flow.request.content.decode()))
        elif 'application/x-www-form-urlencoded' in content_type:
            ctx.log.info("Form Data:")
            form_data = parse_qs(flow.request.content.decode())
            for field, values in form_data.items():
                for value in values:
                    ctx.log.info(f"    {field}: {value}")
        else:
            ctx.log.info(f"Request Body:\n{flow.request.content.decode('utf-8', 'ignore')}")

def response(flow: http.HTTPFlow) -> None:
    ctx.log.info(f"[{datetime.now()}] Response: {flow.response.status_code} {flow.response.reason}")
    ctx.log.info("Response Headers:\n" + format_headers(flow.response.headers))
    
    content_type = flow.response.headers.get('Content-Type', '')
    if flow.response.content:
        if 'application/json' in content_type:
            ctx.log.info("Response Body (JSON):\n" + try_parse_json(flow.response.content.decode()))
        else:
            ctx.log.info(f"Response Body:\n{flow.response.content.decode('utf-8', 'ignore')}")
