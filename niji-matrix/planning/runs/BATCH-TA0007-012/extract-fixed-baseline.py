"""Mechanically extract the five fixed workbook parents and their child rows."""
from pathlib import Path
import json
import re
import xml.etree.ElementTree as ET
import zipfile

RUN = Path(__file__).resolve().parent
WORKSPACE = RUN.parents[3]
SOURCE = WORKSPACE / 'data/mitre-attck/enterprise/v19.1/excel/enterprise-attack-v19.1-techniques.xlsx'
NS = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
      'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships'}
with zipfile.ZipFile(SOURCE) as archive:
    strings = [''.join(x.itertext()) for x in ET.fromstring(archive.read('xl/sharedStrings.xml'))] if 'xl/sharedStrings.xml' in archive.namelist() else []
    workbook = ET.fromstring(archive.read('xl/workbook.xml'))
    links = {x.attrib['Id']: x.attrib['Target'] for x in ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))}
    sheet = next(x for x in workbook.find('s:sheets', NS) if x.attrib['name'] == 'techniques')
    location = links[sheet.attrib['{' + NS['r'] + '}id']]
    location = location.lstrip('/') if location.startswith('/') else 'xl/' + location
    rows = []
    for row in ET.fromstring(archive.read(location)).findall('s:sheetData/s:row', NS):
        result = {}
        for cell in row.findall('s:c', NS):
            value, inline = cell.find('s:v', NS), cell.find('s:is', NS)
            text = value.text if value is not None else ''.join(inline.itertext()) if inline is not None else ''
            result[re.sub(r'\d', '', cell.attrib['r'])] = strings[int(text)] if cell.attrib.get('t') == 's' and text else text
        rows.append(result)
    headers = rows[0]
    records = [{headers[k]: value for k, value in row.items() if k in headers} for row in rows[1:]]
inventory = []
for attack_id in ['T1033', 'T1007', 'T1124', 'T1673', 'T1497']:
    selected = [row for row in records if row.get('ID') == attack_id or str(row.get('ID', '')).startswith(attack_id + '.')]
    children = [row['ID'] for row in selected if '.' in row['ID']]
    data = {'source': str(SOURCE.relative_to(WORKSPACE)), 'sheet': 'techniques', 'attack_version': '19.1',
            'rows': selected, 'attack_subtechnique_count': len(children), 'attack_subtechnique_ids': children}
    (RUN / f'fixed-baseline-{attack_id}.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    inventory.append({'parent': attack_id, 'children': children})
(RUN / 'fixed-baseline-inventory.json').write_text(json.dumps(inventory, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(inventory))
