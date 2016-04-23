#!/usr/local/bin/python

import csv

class Record:
	industry = "Industry Unknown"

	def __init__(self, name, symbol, market_cap, pe_ratio, roa_ttm):
		self.name = name
		self.symbol = symbol
		self.market_cap = market_cap
		self.pe_ratio = float(pe_ratio)
		self.roa_ttm = float(roa_ttm)

	def __str__(self):
		return "%s (%s); MC: %s | PE: %s | ROA: %s" % (self.name, self.symbol, self.market_cap, self.pe_ratio, self.roa_ttm)

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

companies = []
with open('input.csv', 'rb') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		rec = Record(row[0], row[1], row[3], row[4], row[5])
		# print rec
		companies.append(rec)

loadIndustries(companies)

sorted_by_pe = sorted(companies, key=lambda rec: rec.pe_ratio)

i = 1
for rec in sorted_by_pe:
	rec.pe_rank = i
	i = i + 1

sorted_by_roa = sorted(sorted_by_pe, key=lambda rec: 0 - rec.roa_ttm)

i = 1
for rec in sorted_by_roa:
	rec.roa_rank = i
	i = i + 1
	rec.simple_score = rec.pe_rank + rec.roa_rank

sorted_by_score = sorted(sorted_by_roa, key=lambda rec: rec.simple_score)

for rec in sorted_by_score:
	print "%s (%s): %s (PE: %s, ROA: %s) - %s" % (rec.name, rec.symbol, rec.simple_score, rec.pe_ratio, rec.roa_ttm, rec.industry)


print "Done!"

