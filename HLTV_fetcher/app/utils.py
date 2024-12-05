

def extract_id_from_url(url: str) -> int:
    return int(str(url).split('/')[2])