import json
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('ml_project.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

cells = nb['cells']
print(f'Total cells: {len(cells)}')
print('='*80)

for i, c in enumerate(cells):
    ct = c['cell_type']
    src = ''.join(c['source'])
    print(f'\n--- Cell {i} [{ct}] ---')
    print(src[:800])
    
    # Print outputs if code cell
    if ct == 'code' and c.get('outputs'):
        for out in c['outputs']:
            if out.get('output_type') == 'stream':
                print('  OUTPUT:', ''.join(out.get('text', []))[:500])
            elif out.get('output_type') in ('display_data', 'execute_result'):
                data = out.get('data', {})
                if 'text/plain' in data:
                    print('  RESULT:', ''.join(data['text/plain'])[:500])
