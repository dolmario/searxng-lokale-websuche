"""Save a real search response from a local SearXNG service without overwriting."""
from pathlib import Path
import argparse, hashlib, json
from urllib.parse import urlencode, urlsplit
from urllib.request import urlopen

def search(base: str, query: str, output: Path) -> dict:
    address=urlsplit(base)
    if (address.scheme!='http' or address.hostname not in ('127.0.0.1','localhost','::1')
        or address.username or address.password or address.path not in ('','/')
        or address.query or address.fragment):
        raise ValueError('Use your own plain HTTP loopback base address')
    if not query.strip():raise ValueError('Enter a public search query')
    if output.exists():raise FileExistsError('Choose a new output filename')
    url=base.rstrip('/')+'/search?'+urlencode({'q':query,'format':'json'})
    with urlopen(url,timeout=45) as response:
        result=json.load(response)
    if not isinstance(result,dict) or not isinstance(result.get('results'),list):
        raise ValueError('Expected SearXNG results')
    body=(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode('utf-8')
    with output.open('xb') as stream:stream.write(body)
    for row in result['results'][:5]:print(row['title']+'\n'+row['url']+'\n')
    print('Engine messages:',json.dumps(result.get('unresponsive_engines',[]),ensure_ascii=False))
    print('Saved:',str(output.resolve()),'SHA256:',hashlib.sha256(body).hexdigest())
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--base-url',default='http://127.0.0.1:18080')
    parser.add_argument('--query',default='SearXNG search API documentation')
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args();search(args.base_url,args.query,args.output)

if __name__=='__main__':main()
