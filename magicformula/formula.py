#!/usr/local/bin/python
import sys
import csv
import argparse

ROA_WEIGHT = 0.5

class Record:
	industry = "Industry Unknown"

	def __init__(self, name, symbol, market_cap, pe_ratio, roa_ttm, roa_5yr):
		self.name = name
		self.symbol = symbol
		self.market_cap = market_cap
		self.pe_ratio = float(pe_ratio)
		self.roa_ttm = float(roa_ttm)
		self.roa_5yr = float(roa_5yr)

	def __str__(self):
			return "%s (%s); MC: %s | PE: %s | ROA TTM: %s | ROA 5yr: %s" % (self.name, self.symbol, self.market_cap, self.pe_ratio, self.roa_ttm, self.roa_5yr)

def findCompanyBySymbol(companies, symbol):
	for current in (x for x in companies if x.symbol == symbol):
		return current
	return None

def loadIndustries(companies):
	with open('ref/industries.csv', 'rb') as industryfile:
		reader = csv.reader(industryfile)
		for row in reader:
			symbol = row[2]
			if not symbol.startswith("NYSE") and not symbol.startswith("Nasdaq") and not symbol.startswith("TSX"):
				continue
			symbol = symbol.split(":")[1]
			company = findCompanyBySymbol(companies, symbol)
			if company != None:
				company.industry = row[0]

# Parse input file from arguments
parser = argparse.ArgumentParser(description='Rank stocks from CSV.')
parser.add_argument('infile', metavar='FILE', help='The CSV file to source stocks from. See example format in example_input.csv.')

args = parser.parse_args()
infile = args.infile

companies = []
with open(infile, 'rb') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		rec = Record(row[0], row[1], row[3], row[4], row[5], row[6])
		# print rec
		companies.append(rec)

loadIndustries(companies)

sorted_by_pe = sorted(companies, key=lambda rec: rec.pe_ratio)

i = 1
for rec in sorted_by_pe:
	rec.pe_rank = i
	i = i + 1

sorted_by_roa_ttm = sorted(sorted_by_pe, key=lambda rec: 0 - rec.roa_ttm)

i = 1
for rec in sorted_by_roa_ttm:
	rec.roa_ttm_rank = i
	i = i + 1

sorted_by_roa_5yr = sorted(sorted_by_roa_ttm, key=lambda rec: 0 - rec.roa_5yr)

i = 1
for rec in sorted_by_roa_5yr:
	rec.roa_5yr_rank = i
	i = i + 1
	rec.simple_score = rec.pe_rank + ((rec.roa_ttm_rank + rec.roa_5yr_rank) * ROA_WEIGHT / 2.0)

sorted_by_score = sorted(sorted_by_roa_5yr, key=lambda rec: rec.simple_score)

wr = csv.writer(sys.stdout, delimiter='\t')

wr.writerow(["Company Name","Symbol","Simple Score","P/E Ratio","ROA TTM","ROA 5yr","Industry"])

for rec in sorted_by_score:
	wr.writerow([rec.name, rec.symbol, rec.simple_score, rec.pe_ratio, rec.roa_ttm, rec.roa_5yr, rec.industry])
	# print "%s (%s): %s (PE: %s, ROA: %s (TTM) %s (5YR)) - %s" % (rec.name, rec.symbol, rec.simple_score, rec.pe_ratio, rec.roa_ttm, rec.roa_5yr, rec.industry)


