import pandas as pd
import math
import datetime

#1.Load csv data: 
filepath = input("Enter path to your CSV file: ").strip() #Example: C:/Users/yourname/Desktop/myfile.csv
df = pd.read_csv(filepath)
#2.Basic cleaning and formatting
#Remove extra spaces from column headrs
df.columns = df.columns.str.strip()
#Convert 'Date' column to datetime format (MM/DD/YY)
df['Date'] = pd.to_datetime(df['Date'], dayfirst=False, errors='coerce')
#Sort the data by most recent dates first
df = df.sort_values(by='Date', ascending=False).reset_index(drop=True)
#3.Filter out unwanted summary rows
df = df[df['Price'].astype(str).str.contains('Highest|Lowest|Change|Difference') == False]
df = df[df['Vol.'].astype(str).str.contains('Highest|Lowest|Change|Difference') == False]
#Clean and convert the Price column to float
df['Price'] = df['Price'].astype(str).str.replace(',', '').str.strip()
df = df[df['Price'].str.replace('.', '', 1).str.isnumeric()]
df['Price'] = df['Price'].astype(float)
#4.change volume column into numeric form
def change_volume(val):
    if isinstance(val, float):
        return val
    val = val.replace(',', '').strip()
    if val.endswith('K'):
        return float(val[:-1]) * 1_000
    elif val.endswith('M'):
        return float(val[:-1]) * 1_000_000
    elif val.endswith('B'):
        return float(val[:-1]) * 1_000_000_000
    else:
        return float(val)
#Apply change_volume and drop missing rows
df['Volume'] = df['Vol.'].astype(str).apply(change_volume)
df = df[df['Volume'].notna()].reset_index(drop=True)
#Sort again to ensure latest data is first
df = df.sort_values(by='Date', ascending=False).reset_index(drop=True)
#Keep only the latest 56 records for analysis
df = df.head(56).reset_index(drop=True)
#DEBUG: Show cleaned data preview 
print(df[['Date', 'Price', 'Volume']].head(6))
print("Total rows BEFORE cleaning:", len(pd.read_csv(filepath)))
print("Total rows AFTER cleaning:", len(df))

#5.Assign data
if len(df) < 56 :
    raise Exception("not enough data")

volatilityprices = df['Price'].astype(float).tolist()[6:]   # First 50 (past)
fivedaydf = df.iloc[1:6]                                     # 5 days before today
todayrow = df.iloc[0]                                        # Today data
fiveday = fivedaydf['Price'].astype(float).tolist()
fivedayvolume = fivedaydf['Volume'].astype(float).tolist()
todayprice = float(todayrow['Price'])
todayvol = todayrow['Volume']
myscore = 0
mydays = 5

#6.Volatility filter using average true range(ATR) (user-provided)
print("please enter the atr of the most recent trading session")
atr = float(input())

if atr/todayprice >= 0.04 and atr/todayprice < 0.06: ####
    print(f"good atr {atr/todayprice}")
    myscore += 1
elif atr/todayprice >= 0.06 :
    print(f"a very strong atr {atr/todayprice}")
    myscore +=1
else:
    print(f"bad atr to price ratio of {atr/todayprice}")

#7.Volume spike check
stockvolumes = fivedayvolume

avgvol = sum(fivedayvolume) / len(fivedayvolume)

print(f"Today volume: {todayvol}")
print(f"5-day volumes: {fivedayvolume}")
print(f"Avg vol: {avgvol}, 1.2x: {avgvol * 1.2}, 2x: {avgvol * 2}")


if todayvol >= (avgvol * 2) :
    print("today volume is more than or equal x2 avgvol")
    volsignal = True
elif todayvol >= (avgvol * 1.2) and float(todayvol) < (avgvol * 2) :
    print("today volume is more than or equal x1.2 avgvol") 
    volsignal = True
else :
    print("volume doesnt support signal")
    volsignal = False

#8.Breakout logic
myhigh = 0

for h in fiveday :
    if float(h) > myhigh :
        myhigh = float(h)
print(f"highest price the stock reached during {mydays} was {myhigh}")

if float(todayprice) < (myhigh * 0.98) :
    print("no breakout!")
    breakout = False
elif float(todayprice) >= (myhigh * 0.98) : 
    print("a breakout likely to happen !!")
    breakout = True

#9.Z-Score calculation (momentum detection)

psum = 0
for p in fiveday :
    psum += p
themean = psum / float(mydays) # because days = n of prices
print(f"the mean of {mydays} == {themean}")

stdsum = 0
for closings in fiveday :
    thediff = float(closings) - themean
    stdsum += pow(thediff, 2)
thestdv = math.sqrt(stdsum / (float(mydays) - 1))
print(f"the stock stdv during {mydays} days is {thestdv}")

zdiff = float(todayprice) - themean
zscore = zdiff / thestdv

if zscore >= 0.7 and zscore < 1.5 : 
    print(f"breakout incoming with zscore of {zscore}")
elif zscore >= 1.5 and zscore <= 2.5 :
    print(f"break out might already happened !! ...zscore of {zscore} ")
elif zscore > 2.5 :
    print(f"might be a fake breakout due to very high zscore = {zscore}")
else :
    print(f"zscore is too low{zscore}")

#10.Volatility Ratio Preparation
day50means = []
fps = [float(p) for p in volatilityprices]

#Calculate rolling 5-day averages

for f in range(len(fps) - 4) :
    day50means.append(sum(fps[f:f+5])/5)

#Compute standard deviation for each 5-day window
totalstdv = 0
variance = 0
for std in range(len(day50means)) :
    window = fps[std:std+5]
    for vs in window :
        variance += pow(vs - day50means[std], 2)
    totalstdv += math.sqrt(variance / 4)
    variance = 0


#11.Volatility Ratio Analysis
avrgstdv = totalstdv / len(day50means)
volratio = thestdv / avrgstdv

if volratio >= 1.1 and volratio < 1.5: 
    print(f"a breakout likely to happen with volatility of {volratio}")
    myscore += 1
elif volratio >= 1.5 :
    print(f"a strong breakout likely to happen with volatility of {volratio}")
    myscore += 1
else :
    print(f"low volratio of {volratio}")

#12.Signal Evaluation

if volsignal == True and breakout == True :
    print("strong confirmation")
elif volsignal == False and breakout == True :
    print("there is a break out but volume is weak!")
#Points added to volatility ratio and atr
if breakout == True :
    myscore += 1
if volsignal == True :
    myscore += 1
if zscore >= 0.7 and zscore <= 2.5 :
    myscore += 1
#Final confidence output
if myscore == 5 :
    print("5/5 confidence")
elif myscore == 4:
    print("4/5 confidence")
elif myscore == 3:
    print("3/5 confidence")
else:
    print(f"low confidence signal {myscore}/5")
