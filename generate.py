from lxml import etree
import re
import os


word_re = re.compile('^(\d{5})\s+(.*)', re.UNICODE)
def get_wordlist(filename):
	if not filename:
		return {}
	try:
		with open(filename, encoding='utf-8', errors='ignore') as f:
			return {m.group(1): m.group(2) for m in map(word_re.match, f.readlines()) if m}
	except FileNotFoundError as e:
		return {}

def get_filename(filename):
	"""
	Using the given filename, find that file in the given location, or any of the parent directories until found 
	"""
	path, filename = os.path.split(filename)
	paths = ['', ] + list(filter(None, path.split(os.path.sep)))
	paths = list(map(lambda t: os.path.join(*paths[:len(paths)-t[0]], filename), enumerate(paths)))
	paths = list(filter(os.path.exists, paths))
	return paths[0] if paths else None

for path, dirs, files in os.walk('source'):
	for d in dirs:
		cwd = os.path.join(path, d)
		primary = get_wordlist(get_filename(os.path.join(cwd, 'primary.txt')))
		secondary = get_wordlist(get_filename(os.path.join(cwd, 'secondary.txt')))

		if not (primary or secondary):
			continue
		print('Generating SVG pages for', cwd)

		# # use an override template or fallback on global templates in each successive directory until the location of this script reached
		# paths = ['', ] + list(filter(None, cwd.split(os.path.sep)))
		# paths = list(map(lambda t: os.path.join(*paths[:len(paths)-t[0]], 'template.svg'), enumerate(paths)))
		# with open(list(filter(os.path.exists, paths))[0]) as f:
		with open(get_filename(os.path.join(cwd, 'template.svg'))) as f:
			tree = etree.parse(f)
			root = tree.getroot()
			def ns(name):
				return '{%s}' % root.nsmap[name] if name in root.nsmap else ''

			def update_cell(cell, code, lookup):
				"""
				cell: etree.Element
				code: [1, 2, 3, 4]
				lookup: {'12341': 'abc', ...}
				"""
				for child in cell.getchildren():
					cell.remove(child)
				# we have a four digit code, so generate the complete five digit codes and write them to the SVG element
				for word in map(lookup.get, [''.join(y) for y in [map(str, code+[x+1,]) for x in range(6)]]):
					child = etree.SubElement(cell, 'tspan', attrib={'{}role'.format(ns('sodipodi')): 'line'})
					child.text = word

			etree.tostring(root.find(".//*[@id]"))
			grid = root.find('.//*[@id="gCells"]')
			cell_re = re.compile("^gCell-(\d)(\d)$")
			for major, minor in [(x,y) for x in range(1,7) for y in range(1,7)]:
				# update words
				for cell in grid:
					m = cell_re.match(cell.get('id'))
					row, col = int(m.group(1)), int(m.group(2))
					code = [major, minor, row, col]
					for text in cell:
						if text.get('id').startswith('text-dw-'):
							# replace primary wordlist (diceware in english)
							update_cell(text, code, primary)
						elif text.get('id').startswith('text-eff-'):
							# replace secondary wordlist (eff in english)
							update_cell(text, code, secondary)
						elif text.get('id').startswith('text-'):
							# update the "1234-" text that indicates the first 4 numbers that match this cell
							text[0].text = '{}-'.format(''.join(map(str, code)))

				# update footer
				tabs = root.find('.//*[@id="gTabs"]')
				for child in tabs:
					style = dict([pair.split(':') for pair in child.get('style').split(';')]) if child.get('style') else {}
					if child.get('id') == 'gTab{}'.format(major):
						style['display'] = 'inline'
						child.find('.//*[@id="tab{}-text"]'.format(major))[0].text = '{}{}'.format(major, minor)
					else:
						style['display'] = 'none'
					child.set('style',  ';'.join([':'.join([k,v]) for k,v in style.items()]))

				# write file
				with open(os.path.join(cwd, 'page-{}{}.svg'.format(major, minor)), 'wb') as fout:
					tree.write(fout, xml_declaration=True, pretty_print=True)