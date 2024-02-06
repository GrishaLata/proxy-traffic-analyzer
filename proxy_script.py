from mitmproxy import ctx, http

def request(flow: http.HTTPFlow) -> None:
   
    ctx.log.info(f"Request: {flow.request.method} {flow.request.url}")
    for header, value in flow.request.headers.items():
        ctx.log.info(f"Request Header: {header}: {value}")
    if flow.request.content:
        ctx.log.info(f"Request Body: {flow.request.content.decode('utf-8', 'ignore')}")

def response(flow: http.HTTPFlow) -> None:
  
    ctx.log.info(f"Response: {flow.response.status_code} {flow.response.reason}")
    for header, value in flow.response.headers.items():
        ctx.log.info(f"Response Header: {header}: {value}")
    if flow.response.content:
        ctx.log.info(f"Response Body: {flow.response.content.decode('utf-8', 'ignore')}")
