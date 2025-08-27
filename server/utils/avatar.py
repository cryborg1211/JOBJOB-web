import base64


def placeholder_avatar(name: str) -> str:
    initials = ''.join([part[0].upper() for part in (name or 'NA').split()[:2]]) or 'NA'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="256">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#14b8a6"/>
      <stop offset="100%" stop-color="#22d3ee"/>
    </linearGradient>
  </defs>
  <circle cx="128" cy="128" r="128" fill="url(#g)"/>
  <text x="50%" y="55%" text-anchor="middle" font-size="88" font-family="Arial, Helvetica, sans-serif" fill="#00100f" dy=".35em">{initials}</text>
</svg>'''
    b64 = base64.b64encode(svg.encode('utf-8')).decode('ascii')
    return f'data:image/svg+xml;base64,{b64}'


