import urllib2
from urllib2 import urlopen
from bs4 import BeautifulSoup

class getEtfInfo:

	def __init__(self, etfSymbol):
		self.etfSymbol = etfSymbol

	def getData(self):
		#get document source code 
		website = urllib2.urlopen('http://www.etf.com/'+self.etfSymbol)
		sourceCode = website.read()
		#make soup a global var, so it can be accessed later
		global soup
		soup = BeautifulSoup(sourceCode)

	def getEtfName(self):
		#parse document to find etf name 
		etfName = soup.find('h1', class_="etf")
		#extract etfName contents (etfTicker & etfLongName)
		etfTicker = etfName.contents[0]
		etfLongName = etfName.contents[1]
		etfTicker = str(etfTicker)
		etfLongName = etfLongName.text
		etfLongName = str(etfLongName)
		print etfTicker + ' - ' + etfLongName

	def getTimeStamp(self):
		#get the time stamp for the data scraped 
		etfInfoTimeStamp = soup.find('div', class_="footNote")
		dataTimeStamp = etfInfoTimeStamp.contents[1]
		print 'As of ' + dataTimeStamp.text

	def getEtfRatings(self):
		#create vars 
		etfScores = []
		cleanEtfScoreList = []
		#parse document to find all divs with the class score
		etfScores = soup.find_all('div', class_="score")
		#loop through etfScores to clean them and add them to the cleanedEtfScoreList
		for etfScore in etfScores:
			strippedEtfScore = etfScore.string.extract()
			strippedEtfScore = str(strippedEtfScore)
			cleanEtfScoreList.append(strippedEtfScore)
		#turn cleanedEtfScoreList into a dictionary for easier access
		etfScoreDic = {'Efficiency': cleanEtfScoreList[0], 'Tradability': cleanEtfScoreList[1], 'Fit': cleanEtfScoreList[2]}
		print 'Efficiency', etfScoreDic['Efficiency']
		print 'Tradability', etfScoreDic['Tradability']
		print 'Fit', etfScoreDic['Fit']

	def getEtfPCV(self): #PCV -> Price, Today's Change, Today's Volume

		#get etf price data 
		etfPriceData = soup.find('div', class_="price")
		etfPriceDataList = etfPriceData.contents
		etfPriceHeader = etfPriceDataList[1]
		etfPrice = etfPriceDataList[4]
		#print etfPriceHeader.text + ' -> ' + etfPrice.text
	
		#get etf todays change data
		etfTodaysChangeData = soup.find('div', class_="todaysChange")
		etfTodaysChangeDataList = etfTodaysChangeData.contents
		etfTodaysChangeHeader = etfTodaysChangeDataList[1]
		etfTodaysChange = etfTodaysChangeDataList[4]
		etfTodaysChange = etfTodaysChange.text
		#split dollar change and percent change
		etfTodaysChange = str(etfTodaysChange)
		etfTCList = []
		etfTCList = etfTodaysChange.split(' ')
		print "Today's change: " + etfTCList[0]
		print "Today's percent change: " + etfTCList[1]

		#get etf todays volume data
		etfTodaysVolData = soup.find('div', class_="todaysVolume")
		etfTodaysVolDataList = etfTodaysVolData.contents
		etfTodaysVolHeader = etfTodaysVolDataList[1]
		etfTodaysVol = etfTodaysVolDataList[4]
		print etfTodaysVolHeader.text + ' -> ' + etfTodaysVol.text

	def getEtfEfficiencyData(self):
		#Portfolio Management Section
		#get the expense ratio name and value
		expenseRatioName = soup.find('a', id="ExpenseRatio")
		expenseRatio = soup.find('span', id="ExpenseRatioSpan")
		expenseRatio = expenseRatio.text
		expenseRatio = expenseRatio.strip()
		print expenseRatioName.text + ' -> ' + expenseRatio

		#get the median tracking difference (12 Mo)
		medianTrackingDiff = soup.find('span', id="MedianTrackingDifference12MoSpan")
		medianTrackingDiff = medianTrackingDiff.text
		medianTrackingDiff = medianTrackingDiff.strip()
		print 'Median Tracking Difference (12 Mo) -> ' + medianTrackingDiff

		#get the max upside deviation (12 Mo)
		maxUpSideDeviation  = soup.find('span', id="MaxUpsideDeviation12MoSpan")
		maxUpSideDeviation = maxUpSideDeviation.text
		maxUpSideDeviation = maxUpSideDeviation.strip()
		print 'Max Upside Deviation (12 Mo) -> ' + maxUpSideDeviation

		#Tax Exposures Section
			#Items to get:
				#Max LT/ST Capital Gains Rate
				#Capital Gains Distributions (3 Year)
				#Tax on Distributions
				#Distributes K1

		#Fund Structure Section
			#Items to get: 
				#Legal Structure
				#OTC Derivative Use
				#Securities Lending Active
				#Securities Lending Split (Fund/Issuer)
				#ETN Counterparty
				#ETN Counterparty Risk
				#Fund Closure Risk
				#Portfolio Disclosure


########################PRINT OUT RESULTS###################################
#ETF list to scrape for
etfList = ['spy', 'vti']
#loop through etfList and get data for each ETF
for etfSymbol in etfList:
	print '--------Starting Data Collection for ' + etfSymbol + '-----------'
	myEtf = getEtfInfo(etfSymbol)
	myEtf.getData()
	myEtf.getEtfName()
	myEtf.getTimeStamp()
	myEtf.getEtfRatings()
	myEtf.getEtfPCV()
	myEtf.getEtfEfficiencyData()
	print '--------Data Collection Complete-----------'